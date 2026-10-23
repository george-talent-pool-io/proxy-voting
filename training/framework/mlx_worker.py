"""Pinned local MLX worker. JSONL serving and real quantised LoRA training."""
import gc
import json
import math
import os
import sys
import time
from pathlib import Path

from training.framework.bundle import load_bundle, write
from training.framework.schema import TrainSpec


def train(request):
    import mlx.core as mx
    import mlx.optimizers as optim
    import numpy as np
    from mlx.utils import tree_flatten
    from mlx_lm import load
    from mlx_lm.tuner.utils import linear_to_lora_layers
    from mlx_lm.tuner.trainer import train as official_train, TrainingArgs, evaluate
    from training.framework.trainers import encode_chat
    spec = TrainSpec.model_validate(request['spec'])
    load_bundle(request['bundle'])
    output = Path(request['output']); output.mkdir(parents=True, exist_ok=False)
    started = time.perf_counter()
    mx.random.seed(spec.seed); np.random.seed(spec.seed)
    model, tokenizer = load(spec.model_path, tokenizer_config={'trust_remote_code': False})
    load_ms = (time.perf_counter() - started) * 1000
    rows = {}
    for split in ['train', 'validation']:
        values = []
        for line in (Path(request['bundle']) / f'llm-{split}.jsonl').read_text().splitlines():
            from training.framework.semantic_io import training_messages
            e = encode_chat(tokenizer, training_messages(json.loads(line)['messages'],spec.semantic_output_format), spec.max_length)
            offset = next(i for i, v in enumerate(e['labels']) if v != -100)
            values.append((e['input_ids'], offset))
        rows[split] = values
    model.freeze()
    lora = {'rank': spec.lora_rank, 'scale': spec.lora_alpha / spec.lora_rank,
            'dropout': 0.0, 'keys': spec.target_modules}
    if spec.initial_adapter_path:
        parent = json.loads((Path(spec.initial_adapter_path) / 'adapter_config.json').read_text())
        if parent['num_layers'] != spec.lora_layers or parent['lora_parameters'] != lora:
            raise ValueError('Warm-start LoRA configuration must match the frozen adapter')
        from mlx_lm.tuner.utils import load_adapters
        model = load_adapters(model, spec.initial_adapter_path)
    else:
        linear_to_lora_layers(model, spec.lora_layers, lora)
    leaves = dict(tree_flatten(model.trainable_parameters()))
    if not leaves:
        raise ValueError('No MLX adapter parameters matched requested modules')
    initial = {k: np.asarray(v).copy() for k, v in leaves.items()}
    write(output / 'adapter_config.json', {'fine_tune_type': 'lora', 'num_layers': spec.lora_layers,
                                           'lora_parameters': lora})
    updates = spec.max_steps or math.ceil(len(rows['train']) / spec.batch_size / spec.gradient_accumulation) * spec.epochs
    iterations = updates * spec.gradient_accumulation
    curve = []
    class Callback:
        def record(self, kind, value):
            item = {'kind': kind, **value}; curve.append(item)
            with (output.parent / 'training-curve.jsonl').open('a') as f:
                f.write(json.dumps(item) + '\n'); f.flush()
        def on_train_loss_report(self, value): self.record('TRAIN', value)
        def on_val_loss_report(self, value): self.record('VALIDATION', value)
    optimiser = optim.AdamW(learning_rate=spec.learning_rate)
    args = TrainingArgs(batch_size=spec.batch_size, iters=iterations, val_batches=-1,
            steps_per_report=1, steps_per_eval=iterations, steps_per_save=iterations,
            max_seq_length=spec.max_length, adapter_file=str(output / 'adapters.safetensors'),
            grad_accumulation_steps=spec.gradient_accumulation, grad_checkpoint=False,
            clear_cache_threshold=0)
    official_train(model, optimiser, rows['train'], rows['validation'], args=args, training_callback=Callback())
    model.eval()
    final_loss = evaluate(model, rows['validation'], spec.batch_size, -1, spec.max_length)
    if not math.isfinite(final_loss):
        raise ValueError('Nonfinite MLX validation loss')
    changed = any(not np.array_equal(initial[k], np.asarray(v)) for k, v in tree_flatten(model.trainable_parameters()))
    if not changed:
        raise ValueError('MLX optimiser did not change any adapter weights')
    # Keep a short held-out-input probe: save/reload identity, not model quality.
    probe = mx.array([rows['validation'][0][0][:128]])
    before = np.asarray(model(probe)[0, -1].astype(mx.float32)).copy()
    peak = mx.get_peak_memory()
    parameters = sum(v.size for v in leaves.values())
    del leaves, model, optimiser
    gc.collect(); mx.clear_cache()
    reloaded, _ = load(spec.model_path, adapter_path=str(output), tokenizer_config={'trust_remote_code': False})
    reloaded.eval()
    after = np.asarray(reloaded(probe)[0, -1].astype(mx.float32))
    delta = float(np.max(np.abs(before - after)))
    parity = bool(np.allclose(before, after, atol=.005, rtol=.005))
    if not parity:
        raise ValueError(f'MLX checkpoint reload logit mismatch: {delta}')
    result = {'backend': 'MLX_QLORA', 'optimiser_steps': updates, 'micro_batches': iterations,
              'trainable_parameters': parameters, 'weights_changed': changed, 'curve': curve,
              'validation_token_cross_entropy': final_loss, 'model_load_ms': load_ms,
              'peak_mlx_allocated_bytes': peak, 'elapsed_seconds': time.perf_counter() - started,
              'reload_parity': {'passed': parity, 'max_absolute_logit_difference': delta,
                                'absolute_relative_tolerance': .005, 'probe_tokens': 128},
              'validation_kind': 'Teacher-forced JSON loss; not semantic accuracy',
              'training_mask': 'Assistant JSON tokens only; complete source, no truncation'}
    write(output.parent / 'mlx-training-result.json', result)


def serve(request):
    import mlx.core as mx
    from mlx_lm import load, generate
    from mlx_lm.sample_utils import make_sampler
    spec = TrainSpec.model_validate(request['spec'])
    model, tokenizer = load(spec.model_path, adapter_path=request['checkpoint'],
                            tokenizer_config={'trust_remote_code': False})
    model.eval()
    print(json.dumps({'ready': True}), flush=True)
    for line in sys.stdin:
        try:
            value = json.loads(line)
            prompt = tokenizer.apply_chat_template(value['messages'], tokenize=True,
                      add_generation_prompt=True, enable_thinking=False)
            if len(prompt) + spec.generation_tokens > spec.max_length:
                raise ValueError('Complete notice plus output exceeds registered context; no truncation')
            started = time.perf_counter()
            answer = generate(model, tokenizer, prompt=prompt, max_tokens=spec.generation_tokens,
                              sampler=make_sampler(temp=0.0), verbose=False)
            out = {'answer': answer, 'prompt_tokens': len(prompt),
                   'generated_tokens': len(tokenizer.encode(answer, add_special_tokens=False)),
                   'latency_ms': (time.perf_counter() - started) * 1000,
                   'peak_mlx_allocated_bytes': mx.get_peak_memory()}
        except Exception as exc:
            out = {'error': f'{type(exc).__name__}: {exc}'}
        print(json.dumps(out, ensure_ascii=False), flush=True)


if __name__ == '__main__':
    os.environ.update(HF_HUB_OFFLINE='1', TRANSFORMERS_OFFLINE='1', TOKENIZERS_PARALLELISM='false')
    request = json.loads(Path(sys.argv[2]).read_text())
    (train if sys.argv[1] == 'train' else serve)(request)
