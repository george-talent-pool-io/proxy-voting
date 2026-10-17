"""Release/campaign contracts. All model doubles are explicitly labelled."""
import copy
import json
from pathlib import Path
from types import SimpleNamespace

import pytest

from training.framework import jobs, releases, campaigns, release_evaluation
from training.framework.bundle import write, sha
from semantic_pipeline.schema import PREDICATES
from semantic_pipeline.evidence import verify_evidence
from tests.unit.test_learning_comparison import result, dataset


@pytest.fixture
def registered(tmp_path, monkeypatch, db):
    from training.framework import runtime
    for name, family in [('laya', 'LAYA'), ('qwen', 'QWEN')]:
        p = jobs.member('jobs', name); p.mkdir(parents=True)
        write(p / 'model-manifest.json', {'job_id': name})
        (p / 'semantic-prompt.txt').write_text('EXPLICIT_TEST_DOUBLE_PROMPT')
    def verify(p):
        p = Path(p)
        return p, {'spec': {'backend': 'LAYA_SDK' if p.name == 'laya' else 'MLX_QLORA',
                           'family': 'LAYA' if p.name == 'laya' else 'QWEN',
                           'base_revision': 'TEST_ONLY', 'base_model_id': p.name}, 'bundle': str(p)}, {}
    monkeypatch.setattr(runtime, 'verify_checkpoint', verify)
    return tmp_path


def prepared(name='r1', mode='LAYA_QWEN', **kw):
    root = jobs.member('releases', name)
    releases.prepare({'mode': mode, 'laya_job': 'laya' if mode != 'QWEN_ONLY' else None,
                      'llm_job': 'qwen' if mode != 'LAYA_ONLY' else None, **kw}, root)
    return root


def validation(path, identity):
    path.mkdir()
    write(path / 'evaluation.json', {'role': 'VALIDATION', 'release_identity': identity})


def test_release_pins_all_models_sources_schema_and_rollback(registered, db):
    a = prepared(); b = prepared('r2', mode='LAYA_ONLY')
    for p in [a, b]:
        m = releases.verify(p); validation(p / 'valid', m['identity']); releases.seal(p, p / 'valid')
    first = releases.select('r1', actor='AI_TEST', reason='Contract verification', database=db)
    second = releases.select('r2', actor='AI_TEST', reason='Contract verification', expected_previous_id=first['id'], database=db)
    rolled = releases.select('r1', actor='AI_TEST', reason='Contract rollback', expected_previous_id=second['id'], rollback_id=first['id'], database=db)
    assert rolled['seal_sha256'] == first['seal_sha256'] and rolled['action'] == 'ROLLBACK'
    assert len(releases.history(db)) == 3
    with pytest.raises(ValueError, match='revision conflict'):
        releases.select('r2', actor='AI', reason='stale', expected_previous_id=first['id'], database=db)
    archive = next((a / 'source-snapshot').rglob('runtime.py')); archive.write_text('changed')
    with pytest.raises(ValueError, match='source changed'): releases.verify_seal(a)


@pytest.mark.parametrize('spec', [dict(mode='LAYA_ONLY'), dict(mode='QWEN_ONLY', laya_job='laya'),
                               dict(mode='LAYA_QWEN', laya_job='laya')])
def test_release_mode_requires_exact_dependencies(spec):
    with pytest.raises(ValueError): releases.ReleaseSpec(**spec)


def test_no_unqualified_constrained_gear_is_claimed():
    with pytest.raises(ValueError, match='no qualified'):
        releases.ReleaseSpec(mode='LAYA_ONLY', laya_job='laya', policy={'gear2': True})


class ExplicitModelDouble:
    calls = []
    values = {}
    def __init__(self, p): self.name = Path(p).name
    def analyse(self, text, **kw):
        self.calls.append(self.name)
        r = copy.deepcopy(result())
        for k, p in r['predicates'].items():
            value = self.values.get(self.name, {}).get(k, p['value'])
            choices = ['VOTABLE', 'NOT_VOTABLE', 'UNCERTAIN'] if k == 'votability' else ['YES', 'NO', 'UNKNOWN']
            p.update(value=value, scores={c: .998 if c == value else .001 for c in choices},
                     evidence=[verify_evidence(text, text)], source='EXPLICIT_MODEL_DOUBLE')
        return r
    def close(self): pass


def test_safe_laya_does_not_load_llm_and_retains_null_confidence(registered):
    root = prepared(); ExplicitModelDouble.calls = []; ExplicitModelDouble.values = {}
    model = releases.ReleaseModel(root, sealed=False, laya_factory=ExplicitModelDouble, llm_factory=ExplicitModelDouble)
    out = model.analyse('Notice', use_iso=False)
    assert ExplicitModelDouble.calls == ['laya'] and not out['escalation']['escalated']
    assert all(p['confidence'] is None for p in out['confidence'].values())
    assert out['decision']['manual_review_required'] and not out['automation_enabled']


def test_unknown_escalates_and_real_disagreement_routes_to_review(registered):
    root = prepared(); ExplicitModelDouble.calls = []
    ExplicitModelDouble.values = {'laya': {'share_blocking': 'UNKNOWN'}}
    model = releases.ReleaseModel(root, sealed=False, laya_factory=ExplicitModelDouble, llm_factory=ExplicitModelDouble)
    out = model.analyse('Notice', use_iso=False)
    assert ExplicitModelDouble.calls == ['laya', 'qwen']
    assert out['predicates']['share_blocking']['value'] == 'NO'
    ExplicitModelDouble.values = {'laya': {'share_blocking': 'YES'}, 'qwen': {'share_blocking': 'NO'}}
    # Force a supported but low-score Laya output to be examined by the LLM.
    class LowMargin(ExplicitModelDouble):
        def analyse(self, *a, **kw):
            r = super().analyse(*a, **kw)
            r['predicates']['share_blocking']['scores'] = {'YES': .4, 'NO': .35, 'UNKNOWN': .25}
            return r
    model = releases.ReleaseModel(root, sealed=False, laya_factory=LowMargin, llm_factory=ExplicitModelDouble)
    out = model.analyse('Notice', use_iso=False)
    assert out['predicates']['share_blocking']['value'] == 'UNKNOWN'
    assert 'share_blocking:MODEL_DISAGREEMENT' in out['reconciliation']['conflicts']


def test_independent_llm_only_never_loads_laya(registered):
    root = prepared(mode='QWEN_ONLY'); ExplicitModelDouble.calls = []; ExplicitModelDouble.values = {}
    model = releases.ReleaseModel(root, sealed=False, llm_factory=ExplicitModelDouble,
                                  laya_factory=lambda p: pytest.fail('Independent baseline saw Laya'))
    out = model.analyse('Notice', use_iso=False)
    assert ExplicitModelDouble.calls == ['qwen'] and out['laya'] is None


def test_release_evaluation_keys_open_only_after_durable_predictions(registered, tmp_path, monkeypatch):
    data = tmp_path / 'data'; dataset(data, 'CALIBRATION'); root = prepared(mode='QWEN_ONLY')
    output = tmp_path / 'eval'; original = Path.read_text
    def guarded(p, *a, **kw):
        if p.name == 'answer_keys.jsonl':
            receipt = json.loads(original(output / 'BLIND_PREDICTIONS_PERSISTED.json'))
            assert receipt['n'] == 4
            assert receipt['prediction_sha256'] == sha(output / 'predictions.jsonl')
        return original(p, *a, **kw)
    monkeypatch.setattr(Path, 'read_text', guarded)
    ExplicitModelDouble.values = {}
    factory = lambda p: releases.ReleaseModel(p, sealed=False, llm_factory=ExplicitModelDouble)
    report = release_evaluation.evaluate(data, root, output, role='CALIBRATION', model_factory=factory)
    assert report['metrics']['assertions'] == 36
    calibration = release_evaluation.calibrate(output, tmp_path / 'cal')
    assert not calibration['valid_predicates']
    assert all(r['status'] == 'INSUFFICIENT_CALIBRATION_SUPPORT' for r in calibration['reports'].values())
    assert all(r['accepted'] == 0 for r in release_evaluation.coverage(output, tmp_path / 'cal'))
    with pytest.raises(ValueError, match='before opening'):
        dataset2 = tmp_path / 'frozen'; dataset(dataset2, 'FROZEN_TEST')
        release_evaluation.evaluate(dataset2, root, tmp_path / 'frozen-out', role='FROZEN_TEST', model_factory=factory)


def test_validated_calibrator_persistence_identity_and_tampering(registered, tmp_path):
    from qwen_domain.confidence import CorrectnessCalibrator
    # Controlled statistical fixture, explicitly not real-model performance.
    records = []
    for fold, n in [('FIT', 220), ('EVALUATION', 120)]:
        for i in range(n):
            strong = i % 2 == 0
            correct = (i % 10 != 0) if strong else (i % 10 in (1, 3))
            records.append({'split': 'CALIBRATION', 'predicate': 'share_blocking', 'calibration_fold': fold,
                            'duplicate_group': f'{fold}-{i}', 'correct': correct,
                            'features': {'explicit_test_signal': strong}})
    root = prepared(); m = releases.verify(root); cal = CorrectnessCalibrator(m['identity'])
    reports = cal.fit(records)
    assert 'share_blocking' in cal.models
    c = tmp_path / 'cal'; c.mkdir(); cal.save(c / 'calibrator.joblib')
    write(c / 'calibration.json', {'release_identity': m['identity'], 'reports': reports})
    validation(root / 'valid', m['identity']); releases.seal(root, root / 'valid', c)
    loaded = releases.ReleaseModel(root, laya_factory=ExplicitModelDouble, llm_factory=ExplicitModelDouble)
    p = loaded.calibrator.predict('share_blocking', {'explicit_test_signal': True}, m['identity'])
    assert p is not None and 0 <= p <= 1
    ExplicitModelDouble.values = {}
    application_result = loaded.analyse('Controlled calibration fixture', use_iso=False)
    assert application_result['confidence']['share_blocking']['confidence'] is not None
    assert application_result['confidence']['share_blocking']['confidence_kind'] == 'CALIBRATED_ON_SYNTHETIC_POPULATION_ONLY'
    with pytest.raises(ValueError, match='another model'):
        loaded.calibrator.predict('share_blocking', {}, 'WRONG_IDENTITY')
    (root / 'calibrator.joblib').write_bytes(b'corrupt pickle never opened')
    with pytest.raises(ValueError, match='calibrator changed'): releases.ReleaseModel(root)


def test_campaign_cancel_and_dead_worker_require_new_campaign(registered, tmp_path):
    root = tmp_path / 'campaign'; root.mkdir(); write(root / 'campaign.json', {'spec': {}})
    jobs.events(root, {'state': 'PREPARED'})
    assert campaigns.cancel(root)['state'] == 'CANCELLED'
    with pytest.raises(ValueError, match='prepared'): campaigns.spawn(root)
    other = tmp_path / 'dead'; other.mkdir(); write(other / 'campaign.json', {'spec': {}})
    jobs.events(other, {'state': 'RUNNING', 'pid': 999999, 'pid_started': 1})
    assert campaigns.status(other)['state'] == 'INTERRUPTED'


def test_campaign_spec_rejects_unbound_stages():
    with pytest.raises(ValueError, match='dependency'):
        campaigns.CampaignSpec(bundle_id='test', dataset_id='test', actor='AI', stages=[{'name': 'base', 'reuse_job': 'qwen'}],
                               candidates=[{'name': 'test', 'mode': 'QWEN_ONLY', 'llm_stage': 'missing'}])


def test_mixed_legacy_answers_are_rejected_before_any_labels_are_read(tmp_path, monkeypatch):
    from training.framework.event_data import load_answers, load_inputs
    root = tmp_path / 'mixed'; dataset(root, 'VALIDATION')
    manifest, inputs = load_inputs(root, 'VALIDATION')
    manifest['roles']['FROZEN_TEST'] = 1
    original = Path.read_text
    def guarded(path, *a, **kw):
        if path.name == 'answer_keys.jsonl': pytest.fail('Mixed labels were read')
        return original(path, *a, **kw)
    monkeypatch.setattr(Path, 'read_text', guarded)
    with pytest.raises(ValueError, match='migration'): load_answers(root, manifest, 'VALIDATION', inputs)


def test_registered_passage_layer_retains_scores_and_exact_source(monkeypatch):
    from training.framework.passage_runtime import RegisteredPassages
    from training.framework.bundle import laya_questions
    text = 'Shareholders can vote. Shares will be blocked. No POA is required.'
    class Agent:
        def predict_batch(self, texts, questions, **kw):
            out = []
            for t in texts:
                answers = {}
                for k, q in questions.items():
                    v = ('VOTABLE' if k == 'votability' else 'YES' if k == 'share_blocking' and 'blocked' in t else 'NO')
                    answers[k] = {'choice': v, 'probabilities': {c: .998 if c == v else .001 for c in q['criteria']}}
                out.append({'answers': answers, 'usage': {'truncated': False}})
            return out
    class Model(ExplicitModelDouble):
        def __init__(self, job):
            self.name = 'laya'; self.spec = SimpleNamespace(backend='LAYA_SDK', max_length=4096)
            self.questions = laya_questions(); self.agent = Agent()
    p = RegisteredPassages('laya', model_factory=Model)
    out = p.analyse(text, use_iso=False)
    block = out['predicates']['share_blocking']
    assert block['value'] == 'YES' and block['native_score'] == .998 and block['confidence'] is None
    assert block['evidence'][0]['text'] in text and len(block['passage_states']) == 3


def test_complete_campaign_orders_selection_calibration_and_frozen_scoring(registered, tmp_path, monkeypatch, db):
    """Full orchestration with explicit doubles; real backends have separate receipts."""
    data = jobs.member('event-datasets', 'test'); data.mkdir(parents=True); (data / 'private').mkdir()
    from training.framework.bundle import jsonl
    from classifier.preprocessing import source_hash
    rows = [{'id': role, 'text': 'Notice', 'source_hash': source_hash('Notice'), 'snapshot_hash': role,
             'split': role, 'group_id': role, 'generation_family': role}
            for role in ['TRAIN', 'VALIDATION', 'CALIBRATION', 'FROZEN_TEST']]
    jsonl(data / 'inputs.jsonl', rows)
    jsonl(data / 'private/answer_keys.jsonl', [{'id': r['id'], 'snapshot_hash': r['snapshot_hash'],
          'target': {k: 'VOTABLE' if k == 'votability' else 'NO' for k in PREDICATES},
          'expected_final_status': 'VOTABLE', 'expected_deadline_status': 'OPEN', 'provenance': {'origin': 'AI_AUTHORED'}} for r in rows])
    write(data / 'manifest.json', {'roles': {r['split']: 1 for r in rows}, 'input_file': 'inputs.jsonl',
          'input_sha256': sha(data / 'inputs.jsonl'), 'answer_file': 'private/answer_keys.jsonl',
          'answer_sha256': sha(data / 'private/answer_keys.jsonl')})
    from training.framework.event_data import separate_answers
    legacy = tmp_path / 'legacy-dataset'; data.rename(legacy); separate_answers(legacy, data)
    bundle = jobs.member('bundles', 'test'); bundle.mkdir(parents=True); write(bundle / 'manifest.json', {})
    from types import SimpleNamespace
    monkeypatch.setattr(campaigns, 'load_bundle', lambda p: ({'label_origins': {'AI_AUTHORED': 2}},
          [SimpleNamespace(id=r['id'], source_hash=r['source_hash'], split=r['split']) for r in rows[:2]]))
    spec = {'bundle_id': 'test', 'dataset_id': 'test', 'actor': 'EXPLICIT_TEST_DOUBLE',
            'stages': [{'name': 'base', 'reuse_job': 'qwen'}],
            'candidates': [{'name': 'independent', 'mode': 'QWEN_ONLY', 'llm_stage': 'base'}]}
    root = jobs.member('campaigns', 'control'); campaigns.prepare(spec, root)
    original = releases.ReleaseModel; ExplicitModelDouble.values = {}
    monkeypatch.setattr(releases, 'ReleaseModel', lambda p, **kw: original(p, llm_factory=ExplicitModelDouble, **kw))
    report = campaigns.run(root, database=db)
    assert report['frozen']['metrics']['assertions'] == 9
    assert not report['calibration']['valid_predicates']
    assert (root / 'OPERATING_FREEZE.json').exists()
    assert campaigns.status(root)['state'] == 'COMPLETED'
    assert releases.history(db)[-1]['release_id'] == report['candidates']['independent']
    with pytest.raises(FileExistsError): campaigns.run(root, database=db)
