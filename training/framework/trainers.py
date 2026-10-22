"""Offline trainers with explicit preflight and truthful execution receipts.

The installed Ollama GGUF is an inference artifact, not a PEFT training base.
The generic causal-LM backend supports compatible local Transformers checkpoints;
support for a particular Qwen/GLM architecture must pass its own smoke test.
"""
import importlib.metadata
import importlib.util
import json
import os
import platform
import random
import time
import subprocess
from pathlib import Path

from training.framework.bundle import load_bundle, sha, write
from training.framework.schema import TrainSpec


def training_label_support(data):
    """Expose absent/rare classes; epochs cannot create missing supervision."""
    from semantic_pipeline.schema import PREDICATES
    result={};warnings=[]
    for key in PREDICATES:
        labels=('VOTABLE','NOT_VOTABLE','UNCERTAIN') if key=='votability' else ('YES','NO','UNKNOWN')
        detail={}
        for role in ('TRAIN','VALIDATION'):
            rows=[e for e in data if e.split==role]
            detail[role]={label:{'examples':sum(getattr(e.target,key)==label for e in rows),
                'groups':len({e.group_id for e in rows if getattr(e.target,key)==label})} for label in labels}
        for label,support in detail['TRAIN'].items():
            if support['groups']<5:warnings.append(key+':'+label+(':NO_TRAINING_EXAMPLES' if not support['groups'] else ':FEWER_THAN_FIVE_TRAINING_GROUPS'))
        result[key]=detail
    return {'per_predicate':result,'warnings':warnings,
            'scope':'Training diagnostics only; five groups is a warning threshold, not a quality/automation qualification'}


def versions():
    result = {}
    for name in ['laya', 'torch', 'transformers', 'peft', 'tokenizers', 'safetensors']:
        try:
            result[name] = importlib.metadata.version(name)
        except importlib.metadata.PackageNotFoundError:
            result[name] = None
    return result


def offline():
    os.environ.update(HF_HUB_OFFLINE='1', TRANSFORMERS_OFFLINE='1',
                      HF_HUB_DISABLE_TELEMETRY='1', WANDB_DISABLED='true', USE_TF='0')


def snapshot(path):
    root = Path(path).resolve()
    return {str(p.relative_to(root)): sha(p) for p in sorted(root.rglob('*')) if p.is_file()}


def preflight(bundle, spec):
    spec = spec if isinstance(spec, TrainSpec) else TrainSpec.model_validate(spec)
    manifest, data = load_bundle(bundle)
    label_support=training_label_support(data)
    model = Path(spec.model_path).resolve()
    reasons = []
    parent = None
    if spec.parent_seed_path:
        from training.framework.seeds import verify
        parent = verify(spec.parent_seed_path)
        if (str(model) != parent['model_location'] or spec.initial_adapter_path != parent['adapter_location']
                or any(getattr(spec,key)!=parent['spec'][key] for key in ('backend','family','base_model_id','base_revision'))):
            raise ValueError('Training does not match its frozen starting checkpoint')
        if spec.initial_adapter_path and any(getattr(spec,k)!=parent['spec'][k] for k in
                                           ('lora_rank','lora_alpha','lora_layers','target_modules')):
            raise ValueError('Warm-start adapter architecture must match the frozen parent')
        if sha(Path(bundle) / 'semantic-prompt.txt') != parent['prompt_sha256'] or sha(Path(bundle) / 'laya-questions.json') != parent['questions_sha256']:
            raise ValueError('Customer bundle changed the frozen prompt/classification criteria')
    elif spec.initial_adapter_path:
        raise ValueError('Warm-start adapters require an immutable parent seed')
    if spec.base_revision.startswith('REPLACE_'):
        reasons.append('EXACT_BASE_REVISION_NOT_CONFIGURED')
    if not model.is_dir():
        reasons.append('LOCAL_TRAINABLE_CHECKPOINT_MISSING')
    elif not list(model.glob('*.safetensors')) and not list(model.glob('pytorch_model*.bin')):
        reasons.append('NO_TRAINABLE_WEIGHTS: Ollama/GGUF is not a Transformers/Laya training checkpoint')
    if spec.backend == 'TRANSFORMERS_PEFT' and importlib.util.find_spec('peft') is None:
        reasons.append('PEFT_NOT_INSTALLED: install the optional training environment')
    if spec.backend == 'TRANSFORMERS_PEFT' and importlib.util.find_spec('accelerate') is None:
        reasons.append('ACCELERATE_NOT_INSTALLED: install the optional training environment')
    if spec.backend == 'LAYA_SDK' and not (model / 'rl_agent_config.json').exists():
        reasons.append('LAYA_CONFIGURATION_MISSING')
    runtime = None
    if spec.backend == 'MLX_QLORA':
        try:
            runtime = probe_mlx(spec.runtime_python)
        except (OSError, ValueError, subprocess.SubprocessError) as exc:
            reasons.append('MLX_TRAINING_RUNTIME_UNAVAILABLE: ' + str(exc))
    import psutil
    memory = psutil.virtual_memory()
    weight_bytes = sum(p.stat().st_size for p in model.glob('*.safetensors')) if model.is_dir() else 0
    # A conservative feasibility screen, not a measured peak-memory prediction.
    if weight_bytes > memory.total * .60:
        reasons.append('BASE_WEIGHTS_EXCEED_LOCAL_TRAINING_BUDGET: use a quantised trainer or larger host')
    return {'ready': not reasons, 'reasons': reasons, 'spec': spec.model_dump(),
            'bundle_hash': sha(Path(bundle) / 'manifest.json'), 'counts': manifest['counts'],
            'label_origins': manifest['label_origins'], 'versions': versions(),
            'hardware': {'system': platform.platform(), 'machine': platform.machine(),
                         'memory_bytes': memory.total, 'available_bytes': memory.available},
            'local_weight_bytes': weight_bytes,
            'label_support':label_support,
            'parent_checkpoint_identity': parent['identity'] if parent else None,
            'training_runtime': runtime,
            'scope': 'Preflight checks prerequisites, not exact-model trainer compatibility or model quality',
            'automation_enabled': False, 'customer_accuracy': None}


def probe_mlx(python):
    if not python or not Path(python).is_file():
        raise ValueError('An isolated runtime_python is required')
    code = ('import json,importlib.metadata as m;import mlx.core as mx;'
            'print(json.dumps({"mlx":m.version("mlx"),"mlx_lm":m.version("mlx-lm"),'
            '"transformers":m.version("transformers"),'
            '"metal_available":mx.metal.is_available()}))')
    # Resolving a venv's python symlink bypasses that environment entirely.
    p = subprocess.run([str(Path(python).absolute()), '-c', code], capture_output=True,
                       text=True, timeout=30, check=True)
    value = json.loads(p.stdout)
    if not value['metal_available']:
        raise ValueError('MLX Metal runtime unavailable')
    return value


def train_mlx(bundle, output, spec):
    """Isolate MLX dependencies and process memory from FastAPI/Transformers."""
    output = Path(output)
    request = output.parent / 'mlx-training-request.json'
    write(request, {'bundle': str(Path(bundle).resolve()), 'output': str(output.resolve()),
                    'spec': spec.model_dump()})
    with (output.parent / 'trainer.log').open('xb') as log:
        p = subprocess.run([str(Path(spec.runtime_python).absolute()), '-m',
                'training.framework.mlx_worker', 'train', str(request)],
                cwd=Path(__file__).resolve().parents[2], stdin=subprocess.DEVNULL,
                stdout=log, stderr=subprocess.STDOUT, timeout=spec.training_timeout_seconds,
                env={**os.environ, 'HF_HUB_OFFLINE': '1', 'TRANSFORMERS_OFFLINE': '1',
                     'HF_HUB_DISABLE_TELEMETRY': '1', 'TOKENIZERS_PARALLELISM': 'false'})
    if p.returncode:
        raise RuntimeError(f'MLX training failed ({p.returncode}); preserved trainer.log')
    return json.loads((output.parent / 'mlx-training-result.json').read_text())


def encode_chat(tokenizer, messages, max_length):
    """Loss on assistant JSON only; reject silent truncation/template mismatch."""
    prompt = tokenizer.apply_chat_template(messages[:-1], tokenize=True,
                                          add_generation_prompt=True, enable_thinking=False)
    full = tokenizer.apply_chat_template(messages, tokenize=True,
                                        add_generation_prompt=False, enable_thinking=False)
    if hasattr(prompt, 'input_ids'):
        prompt, full = prompt.input_ids, full.input_ids
    if full[:len(prompt)] != prompt:
        # Qwen Direct appends an empty <think> block only at generation time.
        # Train the actual serving prefix + assistant JSON + EOS, not a
        # differently rendered chat completion. Unknown templates still fail.
        rendered = tokenizer.apply_chat_template(messages[:-1], tokenize=False,
                            add_generation_prompt=True, enable_thinking=False)
        if isinstance(rendered, str) and rendered.endswith('<think>\n\n</think>\n\n'):
            if messages[-1].get('role') != 'assistant' or tokenizer.eos_token_id is None:
                raise ValueError('Qwen Direct target requires assistant JSON and an EOS token')
            full = list(prompt) + tokenizer.encode(messages[-1]['content'], add_special_tokens=False) + [tokenizer.eos_token_id]
    if full[:len(prompt)] != prompt or len(full) <= len(prompt):
        raise ValueError('Chat template does not preserve the masked assistant prefix; exact-model adapter needed')
    if len(full) > max_length:
        raise ValueError(f'Training context {len(full)} exceeds max_length={max_length}; no truncation permitted')
    return {'input_ids': full, 'labels': [-100] * len(prompt) + full[len(prompt):]}


def laya_training_input(bundle, output, spec):
    """Explicit TRAIN-only task weighting; never inflate unique-example counts."""
    rows=[json.loads(line) for line in (Path(bundle)/'laya-train.jsonl').read_text().splitlines()]
    source=Path(bundle)/'laya-train.jsonl'
    budget={'unique_training_notices':len(rows),'source_sha256':sha(source),
            'multipliers':spec.laya_task_multipliers,'role':'TRAIN',
            'validation_resampled':False,'method':'Repeat official SDK question items; not new independent notices'}
    if not spec.laya_task_multipliers:
        return source,{**budget,'effective_question_items':sum(len(r['questions']) for r in rows)}
    from training.framework.bundle import jsonl
    effective=[]
    for row in rows:
        effective.append(row)
        for key,multiplier in sorted(spec.laya_task_multipliers.items()):
            if key not in row['questions'] or key not in row['expected']:raise ValueError('Weighted task absent from training row')
            effective.extend({'state':row['state'],'questions':{key:row['questions'][key]},
                              'expected':{key:row['expected'][key]}} for _ in range(multiplier-1))
    target=Path(output).parent/'laya-effective-train.jsonl'
    jsonl(target,effective)
    receipt={**budget,'effective_question_items':sum(len(r['questions']) for r in effective),
             'derived_sha256':sha(target)}
    write(Path(output).parent/'laya-training-sampling.json',receipt)
    return target,receipt


def train_laya(bundle, output, spec):
    from laya.train import TrainConfig, finetune
    offline()
    if spec.max_steps is not None:
        raise ValueError('Laya SDK backend uses epochs; max_steps is not supported')
    validate_laya_encoding(bundle, spec)
    training_input,sampling=laya_training_input(bundle,output,spec)
    config = TrainConfig(epochs=spec.epochs, seed=spec.seed, encoder_lr=spec.encoder_learning_rate or spec.learning_rate,
                         head_lr=spec.learning_rate, micro_batch=spec.batch_size,
                         grad_accum=spec.gradient_accumulation, max_len=spec.max_length,
                         head_max_len=256, freeze_encoder=spec.freeze_encoder,
                         calib_frac=0, calib_max=0, loss=spec.laya_loss, shuffle_options=('choice',),
                         gradient_checkpointing=spec.laya_gradient_checkpointing,
                         eval_data=str(Path(bundle) / 'laya-validation.jsonl') if spec.laya_sdk_validation else None)
    # Calibration is a separate stage. Validation is available only for validation
    # loss/model selection, never mixed into weight updates.
    import torch
    if spec.mps_memory_fraction is not None:torch.mps.set_per_process_memory_fraction(spec.mps_memory_fraction)
    try:
        result = finetune(str(training_input), spec.model_path,
                          str(output), config, device=spec.device)
    finally:
        if spec.mps_memory_fraction is not None:torch.mps.set_per_process_memory_fraction(1.)
    if any(result.get('skipped', {}).values()) or any(result.get('eval_skipped', {}).values()):
        raise ValueError('Official SDK skipped labelled items; inspect the preserved checkpoint/result')
    write(Path(output) / 'semantic-training-contract.json', {
        'questions': json.loads((Path(bundle) / 'laya-questions.json').read_text()),
        'schema': 'nine-semantic-predicates-v1', 'normalisation': 'UNCHANGED_SOURCE',
        'deadline_status': 'DETERMINISTIC_ONLY', 'automation_enabled': False})
    probe = json.loads((Path(bundle) / 'laya-validation.jsonl').read_text().splitlines()[0])
    parity = validate_laya_reload(output, probe, spec)
    return {'backend': 'LAYA_SDK', 'training': result, 'training_sampling':sampling,
            'validation_kind': ('Official SDK validation diagnostics; separate semantic evaluation required' if spec.laya_sdk_validation else
                                'SDK duplicate validation disabled; independent framework validation REQUIRED before sealing'),
            'reload_parity': parity}


def validate_laya_reload(output, probe, spec):
    import gc
    import laya
    results = []
    for _ in range(2):
        agent = laya.load(str(output), device=spec.device)
        raw = agent.predict_batch([probe['state']], probe['questions'], batch_size=1,
                                  max_len=spec.max_length, head_max_len=256)[0]
        results.append(raw['answers'])
        del agent
        gc.collect()
    max_delta = 0.0
    for key in probe['questions']:
        a, b = results[0][key], results[1][key]
        if a['choice'] != b['choice'] or set(a['probabilities']) != set(b['probabilities']):
            raise ValueError('Laya checkpoint reload changed labels/options')
        max_delta = max(max_delta, *(abs(v - b['probabilities'][k]) for k, v in a['probabilities'].items()))
    if max_delta > 1e-5:
        raise ValueError('Laya checkpoint reload changed native scores beyond tolerance')
    return {'passed': True, 'max_absolute_score_difference': max_delta,
            'absolute_tolerance': 1e-5, 'probe': 'First validation input, two fresh loads'}


def validate_laya_encoding(bundle, spec):
    """The SDK caps state tokens; reject that situation instead of hiding it."""
    from transformers import AutoTokenizer
    tokenizer = AutoTokenizer.from_pretrained(Path(spec.model_path) / 'tokenizer',
                                              local_files_only=True, trust_remote_code=False)
    for split in ['train', 'validation']:
        for i, line in enumerate((Path(bundle) / f'laya-{split}.jsonl').read_text().splitlines()):
            row = json.loads(line)
            ids = tokenizer.encode(row['state'], add_special_tokens=False)
            if len(ids) + 256 + 16 > spec.max_length:
                raise ValueError(f'Laya {split} row {i}: complete source plus head exceeds context; '
                                 'explicit chunked training examples or a supported larger context required')


def train_peft(bundle, output, spec):
    """Real LoRA optimiser, validation loss, adapter save/reload and parity probe."""
    offline()
    import torch
    from torch.utils.data import DataLoader
    from transformers import AutoTokenizer, AutoModelForCausalLM
    from peft import LoraConfig, TaskType, get_peft_model, PeftModel
    random.seed(spec.seed)
    torch.manual_seed(spec.seed)
    tokenizer = AutoTokenizer.from_pretrained(spec.model_path, local_files_only=True, trust_remote_code=False)
    if tokenizer.pad_token_id is None:
        if tokenizer.eos_token_id is None:
            raise ValueError('Tokenizer requires a pad or EOS token')
        tokenizer.pad_token = tokenizer.eos_token
    rows = {}
    for split in ['train', 'validation']:
        rows[split] = [encode_chat(tokenizer, json.loads(line)['messages'], spec.max_length)
                       for line in (Path(bundle) / f'llm-{split}.jsonl').read_text().splitlines()]
    dtype = getattr(torch, spec.dtype)
    base = AutoModelForCausalLM.from_pretrained(spec.model_path, local_files_only=True,
                                               trust_remote_code=False, dtype=dtype)
    from peft import PeftModel
    model = (PeftModel.from_pretrained(base, spec.initial_adapter_path, local_files_only=True, is_trainable=True)
             if spec.initial_adapter_path else get_peft_model(base, LoraConfig(task_type=TaskType.CAUSAL_LM,
                    r=spec.lora_rank, lora_alpha=spec.lora_alpha, lora_dropout=0.0,
                    target_modules=spec.target_modules, bias='none')))
    model.to(spec.device)
    if getattr(model.config, 'use_cache', None) is not None:
        model.config.use_cache = False

    def collate(batch):
        size = max(len(r['input_ids']) for r in batch)
        return {key: torch.tensor([r[key] + [fill] * (size - len(r[key])) for r in batch],
                                  device=spec.device) for key, fill in [
            ('input_ids', tokenizer.pad_token_id), ('labels', -100)]} | {
            'attention_mask': torch.tensor([[1] * len(r['input_ids']) + [0] * (size - len(r['input_ids']))
                                            for r in batch], device=spec.device)}

    generator = torch.Generator().manual_seed(spec.seed)
    train_loader = DataLoader(rows['train'], batch_size=spec.batch_size, shuffle=True,
                              generator=generator, collate_fn=collate)
    valid_loader = DataLoader(rows['validation'], batch_size=spec.batch_size, collate_fn=collate)
    params = [p for p in model.parameters() if p.requires_grad]
    optimiser = torch.optim.AdamW(params, lr=spec.learning_rate)
    curve = []
    steps = 0
    started = time.perf_counter()
    for epoch in range(spec.epochs):
        model.train()
        total_loss = 0.0
        tokens = 0
        optimiser.zero_grad(set_to_none=True)
        for i, batch in enumerate(train_loader):
            # Correctly scale the final, incomplete accumulation group.
            group_start = (i // spec.gradient_accumulation) * spec.gradient_accumulation
            accumulation = min(spec.gradient_accumulation, len(train_loader) - group_start)
            loss = model(**batch).loss
            if not torch.isfinite(loss):
                raise ValueError('Nonfinite training loss')
            (loss / accumulation).backward()
            n = int((batch['labels'][:, 1:] != -100).sum())
            total_loss += float(loss.detach()) * n
            tokens += n
            if (i + 1) % spec.gradient_accumulation == 0 or i + 1 == len(train_loader):
                torch.nn.utils.clip_grad_norm_(params, 1.0)
                optimiser.step()
                optimiser.zero_grad(set_to_none=True)
                steps += 1
                if spec.max_steps is not None and steps >= spec.max_steps:
                    break
        model.eval()
        valid_loss = valid_tokens = 0
        with torch.no_grad():
            for batch in valid_loader:
                loss = model(**batch).loss
                n = int((batch['labels'][:, 1:] != -100).sum())
                valid_loss += float(loss) * n
                valid_tokens += n
        curve.append({'epoch': epoch + 1, 'optimiser_steps': steps,
                      'train_token_cross_entropy': total_loss / max(1, tokens),
                      'validation_token_cross_entropy': valid_loss / max(1, valid_tokens)})
        if spec.max_steps is not None and steps >= spec.max_steps:
            break
    output = Path(output)
    output.mkdir(parents=True, exist_ok=False)
    model.save_pretrained(output, safe_serialization=True)
    tokenizer.save_pretrained(output)
    probe = collate([rows['validation'][0]])
    with torch.no_grad():
        before = model(**probe).logits[:, -1].float().cpu()
    # Unload the adapter, preserve the same frozen base, and read the saved weights.
    base = model.unload()
    reloaded = PeftModel.from_pretrained(base, str(output), local_files_only=True, is_trainable=False)
    reloaded.eval()
    with torch.no_grad():
        after = reloaded(**probe).logits[:, -1].float().cpu()
    tolerance = 1e-5 if spec.dtype == 'float32' else .005
    error = float((before - after).abs().max())
    parity = bool(torch.allclose(before, after, atol=tolerance, rtol=tolerance))
    if not parity:
        raise ValueError(f'Adapter reload parity failed; max logit delta={error}')
    return {'backend': 'TRANSFORMERS_PEFT', 'optimiser_steps': steps, 'curve': curve,
            'elapsed_seconds': time.perf_counter() - started,
            'trainable_parameters': sum(p.numel() for p in params),
            'validation_kind': 'Teacher-forced JSON token loss; not semantic classification accuracy',
            'reload_parity': {'passed': parity, 'max_absolute_logit_difference': error,
                              'absolute_relative_tolerance': tolerance,
                              'probe': 'First validation input, final-position logits'},
            'determinism': 'Seeded training; accelerator/kernel determinism is not guaranteed'}
