"""API provenance, review-to-export and job preparation; no model execution."""
import json
import sqlite3

from tests.unit.test_training_framework import example
from training.framework.bundle import create_bundle, load_bundle


def review_body(record='train'):
    from apps.api.domain_views import FullLabel
    return {'record_id': record, 'reviewer': 'AI development reviewer',
            'label': {k: 'UNCERTAIN' if k == 'votability' else 'UNKNOWN' for k in FullLabel.model_fields},
            'label_origin': 'AI_REVIEWED', 'reviewer_model': 'test-only-model-identity',
            'notes': 'AI-assisted fixture, not a human expert label'}


def test_ai_review_keeps_origin_and_can_export_train_validation_without_test_labels(client, db, tmp_path):
    for split in ['train', 'validation', 'test']:
        r = client.post('/api/domain/reviews', json=review_body(split))
        assert r.status_code == 201
    history = client.get('/api/domain/reviews/train').json()['items']
    assert history[0]['context']['label_origin'] == 'AI_REVIEWED'
    assert history[0]['context']['validation_type'] == 'AI_ASSISTED_NOT_HUMAN_GOLD'
    from training.framework.reviews import export_reviews
    output = tmp_path / 'bundle'
    result = export_reviews(output, db)
    assert result['label_origins'] == {'AI_REVIEWED': 2}
    m, rows = load_bundle(output)
    assert {r.id for r in rows} == {'train', 'validation'}
    assert m['source_manifest']['held_out_answers_opened'] is False


def test_ai_review_cannot_impersonate_expert_and_invalid_evidence_is_rejected(client):
    body = review_body(); body['domain_expert_attested'] = True
    assert client.post('/api/domain/reviews', json=body).status_code == 422
    body['domain_expert_attested'] = False; body['reviewer_model'] = None
    assert client.post('/api/domain/reviews', json=body).status_code == 422
    body['reviewer_model'] = 'test'; body['evidence'] = {'share_blocking': ['made-up evidence']}
    assert client.post('/api/domain/reviews', json=body).status_code == 422


def test_training_api_only_prepares_jobs(client, tmp_path, monkeypatch):
    from apps.api import training_views as views
    monkeypatch.setattr(views, 'WORKSPACE', tmp_path)
    create_bundle([example(), example('b', 'VALIDATION')], tmp_path / 'bundles/development')
    response = client.get('/api/training/status')
    assert response.status_code == 200 and response.json()['bundles'][0]['label_origins'] == {'AI_AUTHORED': 2}
    body = {'bundle_id': 'development', 'spec': {'backend': 'TRANSFORMERS_PEFT', 'family': 'QWEN',
            'model_path': str(tmp_path / 'missing'), 'base_model_id': 'unit-only', 'base_revision': 'test-only'}}
    response = client.post('/api/training/jobs', json=body)
    assert response.status_code == 201
    result = response.json()
    assert result['execution_started'] is False
    assert not result['plan']['preflight']['ready']
    status = client.get('/api/training/jobs/' + result['id']).json()
    assert status['state'] == 'BLOCKED' and status['automation_enabled'] is False
    assert client.get('/api/training/status').json()['customer_accuracy'] is None
    assert not list((tmp_path / 'jobs').glob('*/checkpoint'))


def test_workspace_traversal_is_rejected(client):
    response = client.post('/api/training/jobs', json={'bundle_id': '../other', 'spec': {
        'backend': 'LAYA_SDK', 'family': 'LAYA', 'model_path': 'missing',
        'base_model_id': 'unit', 'base_revision': 'unit'}})
    assert response.status_code == 422
