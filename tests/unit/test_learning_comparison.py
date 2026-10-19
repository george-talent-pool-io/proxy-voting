"""Comparison order, calibration scope and selection history contracts."""
import json
from pathlib import Path
import pytest

from semantic_pipeline.schema import PREDICATES
from training.framework import comparison, event_data, jobs, selection, resources
from training.framework.bundle import write, jsonl, sha


def result():
    f = {k: {'value': 'VOTABLE' if k == 'votability' else 'NO', 'source': 'EXPLICIT_TEST_DOUBLE', 'evidence': [], 'scores': {}, 'confidence': None} for k in PREDICATES}
    return {'predicates': f, 'reconciliation': {'predicates': f, 'conflicts': []}, 'deadline': {'status': 'OPEN'},
            'decision': {'classification': 'VOTABLE', 'manual_review_required': True}, 'llm': None,
            'latencies': {'total_ms': 1}, 'escalation': {'escalated': False}}


def dataset(root, role):
    root.mkdir(); (root / 'private').mkdir()
    from classifier.preprocessing import source_hash
    inputs = [{'id': f'{role}-{i}', 'snapshot_hash': str(i), 'source_hash': source_hash('Notice'), 'text': 'Notice',
               'split': role, 'group_id': f'g{i}', 'generation_family': f'f{i}'} for i in range(4)]
    jsonl(root / 'inputs.jsonl', inputs)
    answers = [{'id': i['id'], 'snapshot_hash': i['snapshot_hash'], 'target': {k: 'VOTABLE' if k == 'votability' else 'NO' for k in PREDICATES},
                'expected_final_status': 'VOTABLE', 'expected_deadline_status': 'OPEN', 'provenance': {'origin': 'AI_AUTHORED'}} for i in inputs]
    jsonl(root / 'private/answer_keys.jsonl', answers)
    write(root / 'manifest.json', {'roles': {role: 4}, 'input_file': 'inputs.jsonl', 'input_sha256': sha(root / 'inputs.jsonl'),
                                  'answer_file': 'private/answer_keys.jsonl', 'answer_sha256': sha(root / 'private/answer_keys.jsonl')})


@pytest.mark.parametrize('role', ['VALIDATION', 'CALIBRATION', 'FROZEN_TEST'])
def test_all_predictions_persist_before_key_access_and_sparse_calibration_null(tmp_path, monkeypatch, role):
    root = tmp_path / 'dataset'; dataset(root, role)
    output = tmp_path / 'evaluation'; closed = []
    monkeypatch.setattr(comparison, 'identity', lambda p: {'checkpoint': str(p)})
    monkeypatch.setattr(jobs, 'verify_plan', lambda *a, **kw: (tmp_path, {'job_id': 'test'}))
    monkeypatch.setattr(jobs, 'events', lambda *a: None)
    monkeypatch.setattr(selection, 'history', lambda db=None: [{'id': 1}])
    original = Path.read_text
    def guarded(p, *a, **kw):
        if p.name == 'answer_keys.jsonl':
            receipt = json.loads(original(output / 'BLIND_PREDICTIONS_PERSISTED.json'))
            assert set(receipt['prediction_files']) == {'Laya', 'Qwen'}
            assert receipt['rows_per_candidate'] == 4
        return original(p, *a, **kw)
    monkeypatch.setattr(Path, 'read_text', guarded)
    class Model:
        def __init__(self, job): pass
        def analyse(self, text, **kwargs): return result()
        def close(self): closed.append(True)
    r = comparison.compare(root, {'Laya': 'laya', 'Qwen': 'qwen'}, output, role=role, selection_id=1, model_factory=Model)
    assert len(closed) == 2
    for m in r['metrics'].values():
        assert m['assertions'] == 36 and m['correct_assertions'] == 36
        assert m['final_status']['support'] == 4
        assert m['customer_accuracy'] is None
        if role == 'CALIBRATION':
            assert not m['calibrator_valid_predicates']
            assert all(v['status'] == 'INSUFFICIENT_CALIBRATION_SUPPORT' for v in m['calibration'].values())


def test_frozen_test_requires_prior_selection(tmp_path, monkeypatch):
    root = tmp_path / 'dataset'; dataset(root, 'FROZEN_TEST')
    monkeypatch.setattr(selection, 'history', lambda db=None: [])
    with pytest.raises(ValueError, match='selection'):
        comparison.compare(root, {'Laya': 'unused'}, tmp_path / 'out', role='FROZEN_TEST', model_factory=object)


def test_sdk_step_limit_rejected_before_job_is_prepared():
    from training.framework.schema import TrainSpec
    with pytest.raises(ValueError, match='uses epochs'):
        TrainSpec(backend='LAYA_SDK', family='LAYA', model_path='test', base_model_id='test', base_revision='test', max_steps=1)


def test_interrupted_artifact_cannot_serve(tmp_path, monkeypatch):
    from training.framework import runtime
    monkeypatch.setattr(runtime, 'verify_plan', lambda *a, **kw: (tmp_path, {}))
    monkeypatch.setattr(jobs, 'status', lambda p: {'state': 'INTERRUPTED'})
    with pytest.raises(ValueError, match='quarantined'): runtime.verify_checkpoint(tmp_path)


def test_renamed_challenge_input_is_rejected_without_reading_labels():
    from tests.unit.test_training_framework import example
    from classifier.preprocessing import source_hash
    row = json.loads(Path('tests/fixtures/semantic.json').read_text())[0]
    e = example(); e.text = row['text']; e.source_hash = source_hash(e.text)
    e.id = 'renamed-input'; e.group_id = 'new-group'; e.generation_family = 'new-family'
    with pytest.raises(ValueError, match='Protected event'): event_data.reject_protected([e])


def test_serving_archives_loaded_runtime_and_rejects_changed_archive(tmp_path, monkeypatch):
    from training.framework import runtime
    import laya
    root = tmp_path / 'job'; root.mkdir()
    (root / 'laya-questions.json').write_text('{}')
    plan = {'bundle': str(root), 'spec': {'backend': 'LAYA_SDK', 'family': 'LAYA',
            'model_path': 'test-only', 'base_model_id': 'TEST_DOUBLE', 'base_revision': 'test'}}
    monkeypatch.setattr(runtime, 'verify_checkpoint', lambda p: (root, plan, {}))
    monkeypatch.setattr(laya, 'load', lambda *a, **kw: None)
    runtime.RegisteredModel(root)
    archive = root / 'runtime-sources' / (runtime.RUNTIME_SHA256 + '.py')
    assert sha(archive) == runtime.RUNTIME_SHA256
    archive.write_text('changed')
    with pytest.raises(ValueError, match='runtime changed'): runtime.RegisteredModel(root)


def test_cross_process_resource_lease_is_exclusive_and_released(tmp_path, monkeypatch):
    monkeypatch.setattr(jobs, 'WORKSPACE', tmp_path)
    monkeypatch.setattr(jobs, 'active_experiments', lambda: [])
    with resources.model_resource('test'):
        assert (tmp_path / 'model-training.lock').exists()
        with pytest.raises(ValueError, match='already owned'):
            with resources.model_resource('other'): pass
    assert not (tmp_path / 'model-training.lock').exists()


def test_selection_rollback_is_append_only_and_identity_bound(db, tmp_path, monkeypatch):
    from apps.api import training_views
    from training.framework import runtime
    monkeypatch.setattr(training_views, 'WORKSPACE', tmp_path)
    monkeypatch.setattr(jobs, 'WORKSPACE', tmp_path)
    for name in ['one', 'two']:
        p = tmp_path / 'jobs' / name; p.mkdir(parents=True)
        write(p / 'model-manifest.json', {'job_id': name})
        (p / 'semantic-prompt.txt').write_text('fixed prompt')
        write(p / 'metrics.json', {'job_id': name})
    monkeypatch.setattr(runtime, 'verify_checkpoint', lambda p: (p, {'job_id': p.name, 'bundle': str(p)}, {}))
    monkeypatch.setattr(jobs, 'status', lambda p: {'events': [{'kind': 'VALIDATION_EVALUATION', 'evaluation_path': str(p), 'metrics_sha256': sha(p / 'metrics.json')}]})
    a = selection.choose('one', actor='AI developer', reason='Fixture validation', database=db)
    b = selection.choose('two', actor='AI developer', reason='Fixture validation', expected_previous_id=a['id'], database=db)
    c = selection.choose('one', actor='AI developer', reason='Explicit rollback', expected_previous_id=b['id'], rollback_id=a['id'], database=db)
    assert c['action'] == 'ROLLBACK' and c['manifest_sha256'] == a['manifest_sha256']
    assert len(selection.history(db)) == 3
    with pytest.raises(ValueError, match='revision conflict'):
        selection.choose('two', actor='AI', reason='Stale click', expected_previous_id=a['id'], database=db)
    assert c['payload']['calibrator'] is None and not c['payload']['automation_enabled']
