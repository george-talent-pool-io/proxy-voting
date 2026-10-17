"""Audit/review contracts use doubles; no semantic-quality claim."""
import sqlite3
from qwen_domain.protocol import digest

def label():
    from apps.api.domain_views import FullLabel
    return {k:'UNCERTAIN' if k=='votability' else 'UNKNOWN' for k in FullLabel.model_fields}

def test_domain_status_cannot_claim_customer_accuracy_or_enable_automation(client):
    r=client.get('/api/domain/status');assert r.status_code==200
    assert r.json()['customer_accuracy'] is None and r.json()['automation_enabled'] is False
    assert r.json()['confidence'] is None

def test_domain_analysis_is_disabled_by_default(client,monkeypatch):
    monkeypatch.delenv('DOMAIN_QWEN_ENABLED',raising=False)
    assert client.post('/api/domain/analyse',json={'record_id':'train'}).status_code==403

def test_complete_domain_labels_have_immutable_revisions_and_test_isolation(client,db):
    body={'record_id':'test','reviewer':'Reviewer','label':label(),'blind_review':True,'domain_expert_attested':True}
    first=client.post('/api/domain/reviews',json=body);assert first.status_code==201
    assert not first.json()['training_eligible']
    assert client.post('/api/domain/reviews',json=body).status_code==409
    body['expected_revision']=first.json()['revision'];body['label']['poa_required']='YES'
    second=client.post('/api/domain/reviews',json=body);assert second.status_code==201
    history=client.get('/api/domain/reviews/test').json()['items'];assert len(history)==2
    assert history[0]['label']['poa_required']=='UNKNOWN' and history[1]['previous_revision']==history[0]['id']
    assert history[1]['context']['blind_review_attested'] and not history[1]['context']['training_eligible']
    with sqlite3.connect(db) as c:
        import pytest
        with pytest.raises(sqlite3.IntegrityError):c.execute('DELETE FROM domain_reviews')

def test_complete_domain_labels_reject_missing_fields(client):
    r=client.post('/api/domain/reviews',json={'record_id':'train','reviewer':'R','label':{'votability':'VOTABLE'}})
    assert r.status_code==422

def test_canonical_identity_hash_and_domain_pipeline_before_calibration():
    from qwen_domain.pipeline import DomainPipeline
    from semantic_pipeline.schema import PREDICATES
    from semantic_pipeline.evidence import validate_all
    class Adapter:
        prompt_version='software-test-only'
        def analyse(self,**kwargs):
            parsed={k:'NOT_VOTABLE' if k=='votability' else 'NO' for k in PREDICATES}
            parsed.update(deadline_information={'deadline_mentioned':False,'deadline_text':None},evidence={k:['Information only.'] if k=='votability' else [] for k in PREDICATES},ambiguities=[])
            return {'valid':True,'parsed':parsed,'evidence_validation':validate_all(kwargs['original_text'],parsed),'schema_handling':{'repair_attempts':0}}
    assert digest({'b':2,'a':1})==digest({'a':1,'b':2})
    result=DomainPipeline(adapter=Adapter()).analyse('Information only.')
    assert result['decision']['classification']=='NOT_VOTABLE'
    assert all(c['confidence'] is None for c in result['confidence'].values())
    assert result['decision_confidence']['calibrated_decision_confidence'] is None and result['automation_enabled'] is False
