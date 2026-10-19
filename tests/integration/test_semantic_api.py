import json
import pytest
from pathlib import Path
from fastapi.testclient import TestClient
from apps.api.main import app
from apps.api import semantic_views


def test_experiment_status_never_claims_customer_accuracy(client):
    r=client.get('/api/semantic/experiment');assert r.status_code==200
    d=r.json();assert d['customer_accuracy'] is None;assert not d['automation_enabled']
    assert 'scope' in d;assert 'progress' in d


def test_invalid_architecture_and_missing_provenance(client):
    assert client.get('/api/semantic/records?architecture=../').status_code==400
    assert client.get('/api/semantic/record?id=missing').status_code==404
    assert client.post('/api/semantic/analyse',json={'text':'','architecture':'E'}).status_code==422
    assert client.post('/api/semantic/analyse',json={'text':'abc','architecture':'Z'}).status_code==422


def test_api_reads_saved_stage_history_without_model_loading(client,monkeypatch,tmp_path):
    monkeypatch.setattr(semantic_views,'EXPERIMENT',tmp_path)
    from tests.unit.test_semantic_pipeline import specialist,llm,TEXT
    from semantic_pipeline.pipeline import run
    class Model:
        def analyse(self,text):return specialist('UNKNOWN')
    class Fallback:
        def analyse(self,**kw):return llm()
    result=run(TEXT,'E',laya_model=Model(),fallback=Fallback())
    row={'id':'audit-example','run_id':'fixed-test-run','text':TEXT,'expected':{'poa_required':'YES'},'result':result}
    (tmp_path/'challenge-E.jsonl').write_text(json.dumps(row)+'\n')
    # An interrupted final append does not hide the preceding complete record.
    with (tmp_path/'challenge-E.jsonl').open('a') as f:f.write('{"incomplete":')
    d=client.get('/api/semantic/records?errors_only=true').json();assert d['total']==1
    assert d['items'][0]['llm_invoked'];assert d['items'][0]['failures'][0]['expected']=='YES'
    got=client.get('/api/semantic/record?id=audit-example').json()
    assert got['result']['laya']['predicates']['poa_required']['value']=='UNKNOWN'
    assert got['result']['llm']['parsed']['poa_required']=='NO'
    assert got['result']['reconciliation']['predicates']['poa_required']['value']=='NO'


def test_user_analysis_is_readable_without_reexecuting_models(client,monkeypatch,tmp_path):
    monkeypatch.setattr(semantic_views,'ROOT',tmp_path)
    folder=tmp_path/'data/semantic-runs';folder.mkdir(parents=True)
    identifier='b75f269c-8bcf-4d99-b190-40ddc9b9102f'
    row={'id':identifier,'run_id':identifier,'timestamp':'2026-10-16T12:00:00+00:00',
        'result':{'architecture':'E','decision':{'classification':'UNCERTAIN_MANUAL_REVIEW'},'llm':None}}
    (folder/(identifier+'.jsonl')).write_text(json.dumps(row)+'\n')
    assert client.get('/api/semantic/analyses').json()[0]['id']==identifier
    assert client.get('/api/semantic/analysis/'+identifier).json()==row
    assert client.get('/api/semantic/analysis/not-a-uuid').status_code==404


def test_configured_notice_execution_persists_trace_and_source(client,monkeypatch,tmp_path):
    from tests.unit.test_semantic_pipeline import specialist
    import semantic_pipeline.experiment as experiment
    import semantic_runtime.fallback as adapters
    from semantic_pipeline.fallback import DisabledFallback
    class Model:
        def analyse(self,text):return specialist('UNKNOWN')
    monkeypatch.setenv('CLASSIFICATION_ARCHITECTURE','FULL_HYBRID')
    monkeypatch.setattr(experiment,'laya_for',lambda arm:Model())
    monkeypatch.setattr(adapters,'configured_fallback',DisabledFallback)
    monkeypatch.setattr(semantic_views,'ROOT',tmp_path)
    (tmp_path/'data').mkdir()
    r=client.post('/api/semantic/analyse',json={'record_id':'train'});assert r.status_code==200,r.text
    row=r.json();assert row['record_id']=='train';assert row['result']['architecture']=='E'
    assert row['result']['decision']['manual_review_required'];assert not row['result']['automation_enabled']
    fetched=client.get('/api/notice?id=train').json();assert fetched['semantic_execution']==row
    assert fetched['classification_architecture']=='FULL_HYBRID'
    assert client.get('/api/notice?id=train&blind=true').json()['semantic_execution'] is None
    assert client.post('/api/semantic/analyse',json={'record_id':'train','text':'spoof'}).status_code==422
    assert client.post('/api/semantic/analyse',json={'record_id':'missing'}).status_code==404


@pytest.mark.requires_artifact('data/experiments/local-llm-v1/challenge-A.jsonl')
def test_comparison_exposes_identical_truth_and_missing_capabilities(client):
    r=client.get('/api/semantic/comparison-case?id=obvious-votable')
    # Resolve actual immutable ID; do not hardcode an assumed label or example.
    first=client.get('/api/semantic/records?architecture=A&page_size=1').json()['items'][0]
    row=client.get('/api/semantic/comparison-case',params={'id':first['id']}).json()
    assert set(row['architectures'])==set('ABCDE');assert row['ground_truth']
    assert set(row['evaluated'])==set('ABCDE')
    assert len({r['input_hash'] for r in row['architectures'].values()})==1
