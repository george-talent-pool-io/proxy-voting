"""Load a registered experimental checkpoint into the common decision contract."""
import json
import hashlib
import math
import time
import re
from pathlib import Path

from classifier.deadlines import extract_deadline
from semantic_pipeline.decision import decide
from semantic_pipeline.evidence import validate_all
from semantic_pipeline.schema import PREDICATES, SemanticResult
from training.framework.bundle import messages, sha
from training.framework.jobs import verify_plan
from training.framework.schema import TrainSpec
from training.framework.trainers import offline, snapshot

_LOADED_SOURCE = Path(__file__).read_bytes()
RUNTIME_SHA256 = hashlib.sha256(_LOADED_SOURCE).hexdigest()


def normalise_json_wrapper(output):
    """Only unwrap a complete fenced response; never hunt for an inner object."""
    fenced = re.fullmatch(r'\s*```(?:json)?\s*\n([\s\S]*?)\n```\s*', output)
    return (fenced[1], 'WHOLE_RESPONSE_JSON_FENCE_V1') if fenced else (output, None)


def verify_checkpoint(job):
    root, plan = verify_plan(job, check_sources=False)
    from training.framework.jobs import status
    if status(root)['state'] != 'COMPLETED':
        raise ValueError('Only a completed registered job can serve; interrupted/failed artifacts remain quarantined')
    manifest = json.loads((root / 'model-manifest.json').read_text())
    if manifest['job_id'] != plan['job_id'] or manifest['bundle_manifest_sha256'] != plan['bundle_manifest_sha256']:
        raise ValueError('Checkpoint training lineage mismatch')
    if snapshot(root / 'checkpoint') != manifest['files']:
        raise ValueError('Registered checkpoint files changed')
    if snapshot(plan['spec']['model_path']) != plan['base_model_files']:
        raise ValueError('Registered base-model files changed')
    return root, plan, manifest


class RegisteredModel:
    """Both backends yield the same factors; numerical LLM confidence stays null."""
    def __init__(self, job):
        self.root, self.plan, self.manifest = verify_checkpoint(job)
        archive = self.root / 'runtime-sources' / (RUNTIME_SHA256 + '.py')
        archive.parent.mkdir(exist_ok=True)
        try:
            with archive.open('xb') as f: f.write(_LOADED_SOURCE)
        except FileExistsError:
            if sha(archive) != RUNTIME_SHA256: raise ValueError('Archived inference runtime changed')
        self.spec = TrainSpec.model_validate(self.plan['spec'])
        self.checkpoint_path = self.root / 'checkpoint'
        self.checkpoint_manifest_path = self.root / 'model-manifest.json'
        self._load_backend(adapter_path=str(self.checkpoint_path))

    def _load_backend(self, *, adapter_path=None):
        """Shared serving path for registered derivatives and dataset-free seeds."""
        offline()
        if self.spec.backend == 'LAYA_SDK':
            import laya
            import tempfile
            from training.framework.trainers import isolate_laya_base
            cache=Path(self.root).parent.parent/'runtime-cache';cache.mkdir(parents=True,exist_ok=True)
            self._laya_view=tempfile.TemporaryDirectory(prefix='laya-',dir=cache)
            view=Path(self._laya_view.name)/'model'
            isolate_laya_base(self.checkpoint_path,view)
            self.agent = laya.load(str(view), device=self.spec.device)
            self.questions = json.loads((Path(self.plan['bundle']) / 'laya-questions.json').read_text())
        elif self.spec.backend == 'MLX_QLORA':
            from training.framework.mlx_process import MlxProcess
            self.worker = MlxProcess(self.root, self.spec, checkpoint=adapter_path)
        else:
            import torch
            from transformers import AutoTokenizer, AutoModelForCausalLM
            from peft import PeftModel
            self.tokenizer = AutoTokenizer.from_pretrained(self.checkpoint_path, local_files_only=True,
                                                          trust_remote_code=False)
            base = AutoModelForCausalLM.from_pretrained(self.spec.model_path, local_files_only=True,
                                                       trust_remote_code=False, dtype=getattr(torch, self.spec.dtype))
            self.model = PeftModel.from_pretrained(base, adapter_path, local_files_only=True) if adapter_path else base
            self.model.to(self.spec.device).eval()

    def analyse(self, text, *, reference='2026-10-17T12:00:00+00:00', use_iso=True,
                structured_context=None, deadline_override=None):
        if not isinstance(text, str) or not text.strip():
            raise ValueError('Nonempty source required')
        started = time.perf_counter()
        parser = None
        structured = structured_context or {}
        if use_iso:
            from iso_adapter.routing import route
            parser = route(text)
            structured = {**structured, **parser.get('structured_facts', {})}
        if self.spec.backend == 'LAYA_SDK':
            raw = self.agent.predict_batch([text], self.questions, batch_size=1,
                        max_len=self.spec.max_length, head_max_len=256)[0]
            truncated = bool(raw.get('usage', {}).get('truncated'))
            factors = {}
            for k in PREDICATES:
                a = raw['answers'][k]; scores = a['probabilities']
                if (set(scores) != set(self.questions[k]['criteria']) or
                    any(not math.isfinite(v) or not 0 <= v <= 1 for v in scores.values()) or
                    abs(sum(scores.values()) - 1) > .002 or a['choice'] not in scores):
                    raise ValueError('Invalid native Laya distribution')
                factors[k] = {'value': ('UNCERTAIN' if k == 'votability' else 'UNKNOWN') if truncated else a['choice'],
                              'scores': scores, 'confidence': None, 'native_score': scores[a['choice']],
                              'source': 'REGISTERED_LAYA_WHOLE_NOTICE', 'evidence': [],
                              'evidence_status': 'UNAVAILABLE: this decision head does not extract quotations'}
            llm = None; conflicts = ['LAYA_CONTEXT_TRUNCATED'] if truncated else []
            if raw.get('usage',{}).get('truncated') is False:
                from production.evidence_basis import negative_basis
                for p in factors.values():
                    if p['value'] in ('NO','NOT_VOTABLE'):p['negative_basis']=negative_basis(text,sha(getattr(self,'checkpoint_manifest_path',self.root/'model-manifest.json')))
            deadline = extract_deadline(text, reference)
        else:
            prompt = (Path(self.plan['bundle']) / 'semantic-prompt.txt').read_text()
            system = prompt + '\n\nRequired JSON schema:\n' + json.dumps(SemanticResult.model_json_schema(), sort_keys=True)
            chat = [{'role': 'system', 'content': system}, {'role': 'user', 'content': json.dumps({
                'mode': 'INDEPENDENT', 'original_notice': text, 'narrative': text,
                'authoritative_structured_facts': structured}, ensure_ascii=False)}]
            generation_diagnostics = None
            if self.spec.backend == 'MLX_QLORA':
                generation_diagnostics = self.worker.generate(chat)
                output = generation_diagnostics['answer']
            else:
                import torch
                ids = self.tokenizer.apply_chat_template(chat, tokenize=True, add_generation_prompt=True,
                    enable_thinking=False, return_tensors='pt', return_dict=False).to(self.spec.device)
                if ids.shape[-1] + self.spec.generation_tokens > self.spec.max_length:
                    raise ValueError('Complete notice plus output exceeds the registered context; review required')
                with torch.no_grad():
                    generated = self.model.generate(ids, attention_mask=torch.ones_like(ids), max_new_tokens=self.spec.generation_tokens,
                                                do_sample=False, pad_token_id=self.tokenizer.pad_token_id)
                output = self.tokenizer.decode(generated[0, ids.shape[-1]:], skip_special_tokens=True)
            handling = {'first_pass_success': True, 'repair_attempts': 0, 'repair_success': False,
                        'normalisation': None, 'first_output_sha256': hashlib.sha256(output.encode()).hexdigest()}
            original_output = output
            output, handling['normalisation'] = normalise_json_wrapper(output)
            schema_valid = True
            try:
                parsed = SemanticResult.model_validate_json(output).model_dump()
            except ValueError as error:
                handling['first_pass_success'] = False
                handling['schema_errors'] = ([{'type': e['type'], 'loc': e['loc'], 'message': e['msg']}
                                              for e in error.errors(include_input=False)] if hasattr(error, 'errors') else [])
                if self.spec.backend == 'MLX_QLORA':
                    repair = Path(__file__).with_name('schema_repair_v1.txt').read_text()
                    handling.update(repair_attempts=1, repair_prompt_version='registered_schema_repair_v1:' + hashlib.sha256(repair.encode()).hexdigest())
                    try:
                        fixed = self.worker.generate(chat + [{'role': 'assistant', 'content': original_output},
                                                              {'role': 'user', 'content': repair}])
                        output = fixed['answer']
                        handling['repair_output_sha256'] = hashlib.sha256(output.encode()).hexdigest()
                        output, handling['repair_normalisation'] = normalise_json_wrapper(output)
                        handling['repair_generation'] = {k: v for k, v in fixed.items() if k != 'answer'}
                        parsed = SemanticResult.model_validate_json(output).model_dump()
                        handling['repair_success'] = True
                    except (ValueError, RuntimeError, OSError) as exc:
                        handling['repair_error'] = type(exc).__name__
                        schema_valid = False
                else:
                    schema_valid = False
            if not schema_valid:
                schema_valid = False
                parsed = {k: 'UNCERTAIN' if k == 'votability' else 'UNKNOWN' for k in PREDICATES}
                parsed.update(evidence={k: [] for k in PREDICATES},
                              deadline_information={'deadline_mentioned': False, 'deadline_text': None},
                              ambiguities=['LLM_OUTPUT_SCHEMA_FAILURE'])
            ev = validate_all(text, parsed)
            factors = {k: {'value': parsed[k], 'source': 'REGISTERED_LOCAL_LLM', 'confidence': None,
                           'scores': {}, 'evidence': [q for q in ev['predicates'][k] if q['valid']]} for k in PREDICATES}
            if schema_valid:
                from production.evidence_basis import negative_basis
                for p in factors.values():
                    if p['value'] in ('NO','NOT_VOTABLE') and not p['evidence']:
                        p['negative_basis']=negative_basis(text,sha(getattr(self,'checkpoint_manifest_path',self.root/'model-manifest.json')))
            conflicts = list(parsed['ambiguities'])
            if any(not q['valid'] for quotes in ev['predicates'].values() for q in quotes):
                conflicts.append('INVALID_LLM_EVIDENCE')
            llm = {'invoked': True, 'valid': schema_valid,
                   'schema_handling': handling,
                   'raw_output': output if schema_valid else None,
                   'raw_output_sha256': hashlib.sha256(output.encode()).hexdigest(),
                   'unvalidated_output_retained': False, 'parsed': parsed,
                   'evidence_validation': ev, 'model': self.spec.base_model_id,
                   'generation_diagnostics': {k: v for k, v in (generation_diagnostics or {}).items() if k != 'answer'},
                   'prompt_version': 'proxy_semantic_training_v1', 'confidence': None}
            passage = parsed['deadline_information']['deadline_text']
            if passage is not None and passage not in text:
                conflicts.append('INVALID_DEADLINE_EVIDENCE'); passage = None
            deadline = extract_deadline(passage or text, reference)
        for key, value in structured.items():
            if key not in PREDICATES or not isinstance(value, dict) or 'value' not in value:
                continue
            previous = factors[key]
            if previous['value'] not in (value['value'], 'UNKNOWN', 'UNCERTAIN'):
                conflicts.append(key + ':STRUCTURE_SEMANTIC_CONFLICT')
            factors[key] = {**value, 'semantic_diagnostic': previous}
        if parser and parser['parser'] == 'PROWIDE':
            from iso_adapter.facts import deadline as iso_deadline
            explicit = iso_deadline(parser['structure'], reference)
            if explicit['comparisons']:
                if deadline['status'] != 'UNKNOWN' and explicit['status'] != deadline['status']:
                    conflicts.append('STRUCTURED_NARRATIVE_DEADLINE_CONFLICT')
                deadline = explicit
        if deadline_override is not None:
            if deadline['status'] != 'UNKNOWN' and deadline['status'] != deadline_override['status']:
                conflicts.append('EVENT_STRUCTURE_NARRATIVE_DEADLINE_CONFLICT')
            deadline = deadline_override
        decision = decide(factors, deadline, conflicts)
        return {'architecture': 'REGISTERED_' + self.spec.family, 'job_id': self.plan['job_id'],
                'runtime_version': 'registered-candidate-v5', 'runtime_source_sha256': RUNTIME_SHA256,
                'checkpoint_manifest_sha256': sha(getattr(self, 'checkpoint_manifest_path', self.root / 'model-manifest.json')),
                'input_hash': hashlib.sha256(text.encode()).hexdigest(), 'parser': parser,
                'input_type': parser['input_type'] if parser else 'UNSTRUCTURED_NOTICE',
                'structured_facts': structured,
                'predicates': {**factors, 'deadline_status': {'value': deadline['status'], 'source': 'DETERMINISTIC_RULES', 'confidence': None}},
                'reconciliation': {'predicates': factors, 'conflicts': conflicts},
                'deadline': deadline, 'decision': decision, 'llm': llm,
                'escalation': {'escalated': False, 'reasons': ['TRAINED_CANDIDATE_BENCHMARK_ONLY']},
                'latencies': {'total_ms': (time.perf_counter() - started) * 1000},
                'automation_enabled': False, 'customer_accuracy': None}

    def close(self):
        if hasattr(self, 'worker'):
            self.worker.close()
        if hasattr(self,'agent'):del self.agent
        if getattr(self,'_laya_view',None):
            self._laya_view.cleanup();self._laya_view=None
