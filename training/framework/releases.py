"""Immutable, locally executable model/routing/calibration release packages.

Selection and rollback switch the *whole* configuration. Neither publication nor
selection grants automation. Source or artifact drift fails closed.
"""
import copy
import hashlib
import json
import time
from dataclasses import asdict
from pathlib import Path
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator
from apps.api import store
from semantic_pipeline.schema import PREDICATES, SemanticResult
from semantic_pipeline.decision import decide, VERSION as DECISION_VERSION
from fast_cascade.routing import Policy, assess, reconcile
from training.framework import jobs, events
from training.framework.bundle import sha, write, ROOT
from production.evidence_basis import valid_negative_basis

VERSION = 'trainable-release-v1'


def digest(value):
    return hashlib.sha256(store.dumps(value).encode()).hexdigest()


class ReleaseSpec(BaseModel):
    model_config = ConfigDict(extra='forbid')
    mode: Literal['LAYA_ONLY', 'QWEN_ONLY', 'LAYA_QWEN']
    laya_job: str | None = None
    llm_job: str | None = None
    laya_seed: str | None = None
    llm_seed: str | None = None
    laya_inference: Literal['PASSAGES', 'WHOLE_NOTICE_WITH_PASSAGE_EVIDENCE', 'WHOLE_NOTICE_SCOPED_EVIDENCE'] = 'PASSAGES'
    laya_calibrator_id: str | None = None
    laya_operating_point_id: str | None = None
    policy: dict = Field(default_factory=lambda: asdict(Policy(gear2=False)))
    aggregation: dict = Field(default_factory=lambda: {'strategy': 'SUPERSESSION_AWARE', 'min_score': .7, 'min_margin': .2})

    @model_validator(mode='after')
    def compatible(self):
        if self.laya_job and self.laya_seed or self.llm_job and self.llm_seed:
            raise ValueError('Choose one frozen seed or derivative per model')
        if bool(self.laya_calibrator_id) != bool(self.laya_operating_point_id):
            raise ValueError('Calibrated routing needs both stage calibrator and operating point')
        if self.laya_calibrator_id and self.mode!='LAYA_QWEN':
            raise ValueError('Stage routing calibration belongs to the cascade')
        if bool(self.laya_job or self.laya_seed) != (self.mode in ('LAYA_ONLY', 'LAYA_QWEN')):
            raise ValueError('Release mode/Laya checkpoint mismatch')
        if bool(self.llm_job or self.llm_seed) != (self.mode in ('QWEN_ONLY', 'LAYA_QWEN')):
            raise ValueError('Release mode/LLM checkpoint mismatch')
        if Policy(**self.policy).gear2:
            raise ValueError('Registered MLX adapters have no qualified constrained-token backend; use two gears')
        from cascade.aggregation import AggregationConfig
        AggregationConfig(**self.aggregation)
        return self


def source_files():
    names = set()
    for folder in ['training/framework', 'iso_adapter', 'semantic_pipeline', 'production']:
        names.update(p.relative_to(ROOT).as_posix() for p in (ROOT / folder).glob('*.py'))
    names.update(['cascade/aggregation.py', 'hybrid/semantics.py', 'fast_cascade/aggregation.py',
                  'fast_cascade/routing.py', 'fast_cascade/laya.py', 'classifier/deadlines.py',
                  'classifier/preprocessing.py', 'qwen_domain/confidence.py',
                  'training/framework/schema_repair_v1.txt'])
    # Pin the JVM parser dependency/configuration as well as its Python adapter.
    names.add('tools/prowide/pom.xml')
    names.update(['pyproject.toml', 'uv.lock', 'training/framework/requirements-mlx.lock.txt', 'apps/api/store.py'])
    names.update(p.relative_to(ROOT).as_posix() for p in (ROOT / 'tools/prowide/src').rglob('*.java'))
    jar = ROOT / 'tools/prowide/target/prowide-helper-1.0.0.jar'
    if jar.exists(): names.add(jar.relative_to(ROOT).as_posix())
    return {name: sha(ROOT / name) for name in sorted(names)}


def prepare(spec, output):
    spec = ReleaseSpec.model_validate(spec)
    from training.framework.runtime import verify_checkpoint
    models = {}
    for kind, ident in [('laya', spec.laya_job), ('llm', spec.llm_job)]:
        if ident is None: continue
        path, plan, m = verify_checkpoint(jobs.member('jobs', ident))
        if (kind == 'laya') != (plan['spec']['backend'] == 'LAYA_SDK'):
            raise ValueError('Release checkpoint backend mismatch')
        models[kind] = {'job_id': ident, 'manifest_sha256': sha(path / 'model-manifest.json'),
                        'prompt_sha256': sha(Path(plan['bundle']) / 'semantic-prompt.txt'),
                        'base_revision': plan['spec']['base_revision'], 'base_model_id': plan['spec']['base_model_id']}
    from training.framework import seeds
    for kind, ident in [('laya', spec.laya_seed), ('llm', spec.llm_seed)]:
        if ident is None: continue
        path = jobs.member('seeds', ident); seed = seeds.verify(path)
        if (kind == 'laya') != (seed['spec']['backend'] == 'LAYA_SDK'):
            raise ValueError('Release seed backend mismatch')
        models[kind] = {'seed_id': ident, 'identity': seed['identity'], 'manifest_sha256': sha(path / 'seed.json'),
                        'prompt_sha256': seed['prompt_sha256'], 'base_revision': seed['spec']['base_revision'],
                        'base_model_id': seed['spec']['base_model_id']}
    sources = source_files()
    condition = {'version': VERSION, 'spec': spec.model_dump(), 'models': models, 'sources': sources,
                 'schema_sha256': digest(SemanticResult.model_json_schema()), 'event_policy': events.VERSION,
                 'rule_version': DECISION_VERSION,
                 'confidence_features': 'registered-release-confidence-v1'}
    if spec.laya_calibrator_id:
        from production.cascade_policy import load as load_routing
        cal_path=jobs.member('customer-calibrators',spec.laya_calibrator_id).with_suffix('.json')
        point_path=jobs.member('customer-operating-points',spec.laya_operating_point_id).with_suffix('.json')
        load_routing(cal_path,point_path,condition)
        condition['routing_artifacts']={'calibrator_sha256':sha(cal_path),'point_sha256':sha(point_path)}
    root = Path(output); root.mkdir(parents=True, exist_ok=False)
    for name in sources:
        archive = root / 'source-snapshot' / name; archive.parent.mkdir(parents=True, exist_ok=True)
        archive.write_bytes((ROOT / name).read_bytes())
    manifest = {**condition, 'identity': digest(condition), 'created_at': jobs.now(),
                'scope': 'AI_LABELLED_ENGINEERING_ONLY', 'automation_enabled': False, 'customer_accuracy': None}
    write(root / 'release.json', manifest)
    return manifest


def verify(root):
    root = Path(root)
    m = json.loads((root / 'release.json').read_text())
    condition = {k: m[k] for k in ['version', 'spec', 'models', 'sources', 'schema_sha256',
                                   'event_policy', 'rule_version', 'confidence_features']}
    if 'routing_artifacts' in m:condition['routing_artifacts']=m['routing_artifacts']
    if digest(condition) != m['identity']: raise ValueError('Release manifest identity changed')
    ReleaseSpec.model_validate(m['spec'])
    if m['spec'].get('laya_calibrator_id'):
        cal=jobs.member('customer-calibrators',m['spec']['laya_calibrator_id']).with_suffix('.json')
        point=jobs.member('customer-operating-points',m['spec']['laya_operating_point_id']).with_suffix('.json')
        if m['routing_artifacts']!={'calibrator_sha256':sha(cal),'point_sha256':sha(point)}:
            raise ValueError('Frozen stage routing artifacts changed')
        from production.cascade_policy import load as load_routing
        load_routing(cal,point,m)
    for name, expected in m['sources'].items():
        if sha(ROOT / name) != expected or sha(root / 'source-snapshot' / name) != expected:
            raise ValueError('Release source changed; build a new release (no silent source upgrade)')
    if m['event_policy'] != events.VERSION or m['schema_sha256'] != digest(SemanticResult.model_json_schema()):
        raise ValueError('Release event/schema identity mismatch')
    from training.framework.runtime import verify_checkpoint
    for model in m['models'].values():
        if model.get('seed_id'):
            from training.framework.seeds import verify as verify_seed
            path = jobs.member('seeds', model['seed_id']); seed = verify_seed(path)
            if seed['identity'] != model['identity'] or sha(path / 'seed.json') != model['manifest_sha256']:
                raise ValueError('Release seed changed')
            continue
        job = jobs.member('jobs', model['job_id']); _, plan, _ = verify_checkpoint(job)
        if sha(job / 'model-manifest.json') != model['manifest_sha256'] or sha(Path(plan['bundle']) / 'semantic-prompt.txt') != model['prompt_sha256']:
            raise ValueError('Release model/prompt changed')
    return m


def seal(root, validation, calibration=None):
    """Seal a complete release only after validation/calibration receipts exist."""
    root = Path(root); m = verify(root)
    report = json.loads((Path(validation) / 'evaluation.json').read_text())
    if report['role'] != 'VALIDATION' or report['release_identity'] != m['identity']:
        raise ValueError('Release needs its own validation receipt')
    payload = {'release_sha256': sha(root / 'release.json'), 'identity': m['identity'],
               'validation_path': str(Path(validation).resolve()), 'validation_sha256': sha(Path(validation) / 'evaluation.json'),
               'calibration': None, 'sealed_at': jobs.now(), 'automation_enabled': False}
    if calibration:
        c = Path(calibration)
        cal_report = json.loads((c / 'calibration.json').read_text())
        if cal_report['release_identity'] != m['identity']: raise ValueError('Calibrator identity mismatch')
        target = root / 'calibrator.joblib'
        with target.open('xb') as f: f.write((c / 'calibrator.joblib').read_bytes())
        payload['calibration'] = {'file': target.name, 'sha256': sha(target), 'report': cal_report}
    write(root / 'SEALED.json', payload)
    return payload


def verify_seal(root):
    root = Path(root); m = verify(root)
    sealed = json.loads((root / 'SEALED.json').read_text())
    if sealed['identity'] != m['identity'] or sealed['release_sha256'] != sha(root / 'release.json'):
        raise ValueError('Sealed release changed')
    if sha(Path(sealed['validation_path']) / 'evaluation.json') != sealed['validation_sha256']:
        raise ValueError('Release validation receipt changed')
    cal = sealed['calibration']
    if cal and (cal['file'] != 'calibrator.joblib' or sha(root / cal['file']) != cal['sha256']):
        raise ValueError('Release calibrator changed')
    return m, sealed


def history(database=None):
    with store.connect(database) as c:
        c.executescript('''CREATE TABLE IF NOT EXISTS learning_release_history(
          id INTEGER PRIMARY KEY AUTOINCREMENT,created_at TEXT NOT NULL,action TEXT NOT NULL,
          release_id TEXT NOT NULL,seal_sha256 TEXT NOT NULL,previous_id INTEGER,payload TEXT NOT NULL);
          CREATE TRIGGER IF NOT EXISTS immutable_release_update BEFORE UPDATE ON learning_release_history
          BEGIN SELECT RAISE(ABORT,'Release history is immutable'); END;
          CREATE TRIGGER IF NOT EXISTS immutable_release_delete BEFORE DELETE ON learning_release_history
          BEGIN SELECT RAISE(ABORT,'Release history is immutable'); END;''')
        return [{**dict(r), 'payload': json.loads(r['payload'])} for r in c.execute('SELECT * FROM learning_release_history ORDER BY id')]


def select(release_id, *, actor, reason, expected_previous_id=None, rollback_id=None, database=None):
    if not actor.strip() or not reason.strip(): raise ValueError('Release selection requires actor and reason')
    root = jobs.member('releases', release_id); manifest, _ = verify_seal(root)
    history(database)
    with store.connect(database) as c:
        c.execute('BEGIN IMMEDIATE')
        old = c.execute('SELECT * FROM learning_release_history ORDER BY id DESC LIMIT 1').fetchone()
        if (old['id'] if old else None) != expected_previous_id: raise ValueError('Release selection revision conflict')
        if rollback_id is not None:
            target = c.execute('SELECT * FROM learning_release_history WHERE id=?', (rollback_id,)).fetchone()
            if not target or target['release_id'] != release_id or target['seal_sha256'] != sha(root / 'SEALED.json'):
                raise ValueError('Complete-release rollback identity mismatch')
        payload = {'actor': actor, 'reason': reason, 'identity': manifest['identity'], 'rollback_id': rollback_id,
                   'scope': manifest['scope'], 'automation_enabled': False, 'customer_accuracy': None}
        cur = c.execute('INSERT INTO learning_release_history VALUES(NULL,?,?,?,?,?,?)',
                (jobs.now(), 'ROLLBACK' if rollback_id is not None else 'SELECT', release_id,
                 sha(root / 'SEALED.json'), expected_previous_id, store.dumps(payload)))
        return {**dict(c.execute('SELECT * FROM learning_release_history WHERE id=?', (cur.lastrowid,)).fetchone()), 'payload': payload}


class ReleaseModel:
    """Registered two-gear cascade; lazy LLM loading and explicit disagreements."""
    def __init__(self, root, *, sealed=True, laya_factory=None, llm_factory=None):
        self.root = Path(root)
        self.manifest, receipt = verify_seal(root) if sealed else (verify(root), None)
        self.spec = ReleaseSpec.model_validate(self.manifest['spec'])
        self.policy = Policy(**self.spec.policy); self.laya = None; self.llm = None
        from training.framework.passage_runtime import RegisteredPassages
        from training.framework.runtime import RegisteredModel
        from training.framework.seeds import FrozenModel
        from training.framework.whole_runtime import WholeNotice
        self.laya_factory = laya_factory or ((lambda job:WholeNotice(job,model_factory=FrozenModel if self.spec.laya_seed else RegisteredModel))
            if self.spec.laya_inference=='WHOLE_NOTICE_SCOPED_EVIDENCE' else (lambda job: RegisteredPassages(job, config=self.spec.aggregation,
                                               model_factory=FrozenModel if self.spec.laya_seed else RegisteredModel,
                                               whole_notice=self.spec.laya_inference != 'PASSAGES')))
        self.llm_factory = llm_factory or (FrozenModel if self.spec.llm_seed else RegisteredModel)
        self.calibrator = None
        self.stage_routing=None
        if self.spec.laya_calibrator_id:
            from production.cascade_policy import load as load_routing
            self.stage_routing=load_routing(jobs.member('customer-calibrators',self.spec.laya_calibrator_id).with_suffix('.json'),
                jobs.member('customer-operating-points',self.spec.laya_operating_point_id).with_suffix('.json'),self.manifest)
        if receipt and receipt['calibration']:
            from qwen_domain.confidence import CorrectnessCalibrator
            # Hash validation above precedes deserialisation of our own local file.
            self.calibrator = CorrectnessCalibrator.load(self.root / 'calibrator.joblib', self.manifest['identity'])

    def analyse(self, text, *, reference='2026-10-17T12:00:00+00:00', use_iso=True,
                structured_context=None, deadline_override=None, language='UNKNOWN', population='UNDECLARED',input_type_context=None):
        if not isinstance(text, str) or not text.strip() or len(text) > 2_000_000: raise ValueError('Invalid release input')
        if input_type_context not in (None,'UNSTRUCTURED_NOTICE','PROWIDE_PARSEABLE','LENIENT_ISO_RECOVERABLE','UNRECOGNISED'):
            raise ValueError('Unknown upstream input type')
        start = time.perf_counter(); parser = None; structured = structured_context or {}
        if use_iso:
            from iso_adapter.routing import route
            parser = route(text); structured = {**structured, **parser.get('structured_facts', {})}
            if parser['parser'] == 'PROWIDE':
                from iso_adapter.facts import deadline as iso_deadline
                explicit = iso_deadline(parser['structure'], reference)
                if explicit['comparisons']: deadline_override = explicit
        laya = None; llm = None; gates = {}; trace = []; conflicts = []
        effective_input_type=parser['input_type'] if parser else input_type_context or 'UNSTRUCTURED_NOTICE'
        if parser and input_type_context and parser['input_type']!=input_type_context:conflicts.append('INPUT_TYPE_CONTEXT_CONFLICT')
        current = {k: {'value': 'UNCERTAIN' if k == 'votability' else 'UNKNOWN', 'source': 'NOT_INVOKED',
                       'confidence': None, 'scores': {}, 'evidence': []} for k in PREDICATES}
        loads = {}
        if self.spec.laya_job or self.spec.laya_seed:
            if self.laya is None:
                loaded_at = time.perf_counter(); self.laya = self.laya_factory(jobs.member('seeds' if self.spec.laya_seed else 'jobs', self.spec.laya_seed or self.spec.laya_job))
                loads['laya_ms'] = (time.perf_counter() - loaded_at) * 1000
            laya = self.laya.analyse(text, use_iso=False, reference=reference)
            current = copy.deepcopy({k: laya['predicates'][k] for k in PREDICATES})
            gates = {k: assess(text, k, p, self.policy) for k, p in current.items() if k not in structured}
            if self.stage_routing:
                from production.cascade_policy import assess as calibrated_routing
                stage=calibrated_routing(text,laya,*self.stage_routing,language=language,
                        input_type=effective_input_type,population=population)
                gates={k:{'accepted_for_research':stage['accept'],'calibrated_routing':stage,'reasons':stage['reasons']} for k in current if k not in structured}
        pending = [k for k in PREDICATES if k not in structured and not gates.get(k, {}).get('accepted_for_research')]
        if (self.spec.llm_job or self.spec.llm_seed) and pending:
            if self.llm is None:
                loaded_at = time.perf_counter(); self.llm = self.llm_factory(jobs.member('seeds' if self.spec.llm_seed else 'jobs', self.spec.llm_seed or self.spec.llm_job))
                loads['llm_ms'] = (time.perf_counter() - loaded_at) * 1000
            llm = self.llm.analyse(text, use_iso=False, reference=reference, structured_context=structured)
            valid = not llm.get('execution_error') and not (llm.get('llm') and not llm['llm']['valid'])
            for key in pending:
                later = llm['predicates'][key]
                supported = valid and later['value'] not in ('UNKNOWN', 'UNCERTAIN', 'NOT_SUPPORTED') and (any(e.get('valid') for e in later.get('evidence', [])) or valid_negative_basis(text,later))
                merged, c, t = reconcile(current[key], later, key, right_accepted=supported)
                current[key] = merged; conflicts.extend(c); trace.append({'stage': 'LLM', **t, 'supported': supported})
            conflicts.extend(llm['reconciliation']['conflicts'])
        for key, fact in structured.items():
            if key not in PREDICATES: continue
            previous = current[key]
            if previous['value'] not in (fact['value'], 'UNKNOWN', 'UNCERTAIN'): conflicts.append(key + ':STRUCTURE_SEMANTIC_CONFLICT')
            current[key] = {**fact, 'semantic_diagnostic': previous}
        for k, p in current.items():
            if p.get('conflict'): conflicts.append(k + ':PASSAGE_CONFLICT')
        from classifier.deadlines import extract_deadline
        deadline = extract_deadline(text, reference)
        if llm and llm['deadline']['status'] != 'UNKNOWN': deadline = llm['deadline']
        if deadline_override:
            if deadline['status'] != 'UNKNOWN' and deadline['status'] != deadline_override['status']:
                conflicts.append('STRUCTURED_NARRATIVE_DEADLINE_CONFLICT')
            deadline = deadline_override
        preds = {**current, 'deadline_status': {'value': deadline['status'], 'source': 'DETERMINISTIC_RULES', 'confidence': None}}
        conflicts = sorted(set(conflicts)); decision = decide(current, deadline, conflicts)
        from qwen_domain.confidence import decision_confidence
        from training.framework.calibration import predicate_confidence
        confidence = {k: predicate_confidence(text, k, p, calibrator=self.calibrator, identity=self.manifest['identity'],
                       conflict=bool(conflicts)) for k, p in current.items()}
        decision_trust = decision_confidence(decision['classification'], confidence)
        unresolved = [k for k, p in current.items() if p['value'] in ('UNKNOWN', 'UNCERTAIN') or
                      (p.get('source') != 'PROWIDE' and not any(e.get('valid') for e in p.get('evidence', [])) and not valid_negative_basis(text,p))]
        return {'architecture': self.spec.mode, 'release_id': self.root.name, 'release_identity': self.manifest['identity'],
                'checkpoint_manifest_sha256': digest(self.manifest['models']), 'input_hash': hashlib.sha256(text.encode()).hexdigest(),
                'parser': parser, 'input_type': effective_input_type,
                'structured_facts': structured, 'predicates': preds, 'laya': laya, 'llm_stage': llm,
                'llm': llm.get('llm') if llm else None, 'gear1_gates': gates,
                'escalation': {'escalated': bool(llm), 'requested_predicates': pending,
                               'reasons': {k: gates.get(k, {'reasons': ['LLM_ONLY']})['reasons'] for k in pending}},
                'reconciliation': {'predicates': current, 'conflicts': conflicts, 'trace': trace},
                'deadline': deadline, 'decision': decision, 'confidence': confidence, 'decision_confidence': decision_trust,
                'semantic_review_required': bool(unresolved or conflicts or decision['classification'] == 'UNCERTAIN_MANUAL_REVIEW'),
                'confidence_identity': self.manifest['identity'], 'latencies': {'total_ms': (time.perf_counter() - start) * 1000},
                'model_load_times': loads, 'latency_scope': 'Actual request including cold stage loads when model_load_times is nonempty',
                'automation_enabled': False, 'customer_accuracy': None}

    def close(self):
        for m in [self.laya, self.llm]:
            if m: m.close()
