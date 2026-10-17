"""Registered-candidate application path. Explicit doubles; no model-quality claim."""
import json
import sqlite3

import pytest
from classifier.preprocessing import source_hash
from semantic_pipeline.schema import PREDICATES


def test_candidate_execution_is_explicit_and_default_off(client):
    assert client.post('/api/training/jobs/none/analyse', json={'text': 'Notice'}).status_code == 403


def test_registered_candidate_persists_trace_and_review_links_prediction(client, db, tmp_path, monkeypatch):
    from apps.api import training_views as views
    from training.framework import runtime, jobs
    from semantic_pipeline.decision import decide
    monkeypatch.setattr(views, 'WORKSPACE', tmp_path)
    monkeypatch.setenv('TRAINED_CANDIDATES_ENABLED', 'true')
    monkeypatch.setattr(jobs, 'active_experiments', lambda: [])
    modeldir = tmp_path / 'jobs/contract-candidate'; modeldir.mkdir(parents=True)
    (modeldir / 'model-manifest.json').write_text('{}')
    closed = []
    class Candidate:
        def __init__(self, path): pass
        def analyse(self, text, **kwargs):
            f = {k: {'value': 'NOT_VOTABLE' if k == 'votability' else 'NO', 'source': 'EXPLICIT_TEST_DOUBLE',
                     'evidence': [], 'confidence': None} for k in PREDICATES}
            return {'architecture': 'REGISTERED_QWEN', 'input_hash': source_hash(text), 'predicates': f,
                    'decision': decide(f, {'status': 'UNKNOWN'}), 'parser': None,
                    'reconciliation': {'predicates': f, 'conflicts': []}}
        def close(self): closed.append(True)
    monkeypatch.setattr(runtime, 'RegisteredModel', Candidate)
    r = client.post('/api/training/jobs/contract-candidate/analyse', json={'record_id': 'train'})
    assert r.status_code == 201 and closed == [True]
    value = r.json(); assert value['result']['decision']['automation_enabled'] is False
    assert client.get('/api/training/executions/' + value['id']).json()['raw_source'] == value['raw_source']
    assert client.get('/api/training/status').json()['executions'][0]['id'] == value['id']
    detail = client.get('/api/notice?id=train').json()
    assert detail['framework_execution']['id'] == value['id']
    assert client.get('/api/notice?id=train&blind=true').json()['framework_execution'] is None
    with sqlite3.connect(db) as c:
        with pytest.raises(sqlite3.IntegrityError): c.execute('DELETE FROM framework_executions')
    from tests.integration.test_training_framework_api import review_body
    review = client.post('/api/domain/reviews', json=review_body('train'))
    assert review.status_code == 201
    revision = client.get('/api/domain/reviews/train').json()['items'][-1]
    assert revision['context']['previous_prediction_execution_id'] == value['id']
    assert revision['context']['previous_prediction_architecture'] == 'REGISTERED_QWEN'


def test_candidate_guard_rejects_active_benchmark_and_bad_reference(client, monkeypatch):
    import training.framework.jobs as jobs
    monkeypatch.setenv('TRAINED_CANDIDATES_ENABLED', 'true')
    monkeypatch.setattr(jobs, 'active_experiments', lambda: [{'pid': 12}])
    assert client.post('/api/training/jobs/none/analyse', json={'text': 'Notice'}).status_code == 409
    assert client.post('/api/training/jobs/none/analyse', json={'text': 'Notice', 'reference': '2026-01-01'}).status_code == 422
