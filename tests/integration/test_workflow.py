import json
import sqlite3
from pathlib import Path
import pytest
from apps.api import store
from scripts.run_batch import run_batch
from classifier.laya_classifier import LayaClassifier
from tests.conftest import ContractAgent
from classifier.schema import Decision
from training.dataset import export_dataset
from training.train import train

def factory(config):return LayaClassifier(config,agent=ContractAgent())

def review(client,record='test',run=None,**kwargs):
    body={'record_id':record,'run_id':run,'reviewer':'Domain reviewer','decision':{'votable':'YES','deadline_status':'OPEN'},**kwargs}
    return client.post('/api/reviews',json=body)

def test_health_and_empty(client):
    assert client.get('/api/health').json()['external_inference'] is False
    assert client.get('/api/overview').json()['total']==3
    assert client.get('/api/performance').json()['accuracy'] is None
    assert client.get('/').status_code==200

def test_search_filters(client):
    assert client.get('/api/notices?q=train%20Issuer').json()['total']==1
    assert client.get('/api/notices?country=GB').json()['total']==0
    assert client.get('/api/notices?page=0').status_code==422
    assert client.get('/api/notices?page_size=500').status_code==422
    assert client.get('/api/notices?q=%27%20OR%201=1--').json()['total']==0

def test_full_review_metrics_history(client,db):
    run=run_batch(db,classifier_factory=factory)
    assert client.get('/api/notices?classification=VOTABLE').json()['total']==3
    d=client.get('/api/notice?id=test').json();assert d['prediction']['model_name'].startswith('convaiinnovations/laya')
    assert review(client,run=run).status_code==201
    assert client.get('/api/performance').json()['accuracy']==1
    assert client.get('/api/performance').json()['n']==1
    assert client.get('/api/notices?review=verified').json()['total']==1
    revision=client.get('/api/notice?id=test').json()['review']['id']
    assert review(client,run=run,decision={'votable':'NO'}).status_code==409
    changed=review(client,run=run,decision={'votable':'NO'},expected_revision=revision,notes='Corrected after source check')
    assert changed.status_code==201
    assert client.get('/api/performance').json()['accuracy']==0
    d=client.get('/api/notice?id=test').json();assert len(d['history'])==2
    assert d['prediction']['classification']=='VOTABLE'
    assert client.get('/api/notices?correct=incorrect').json()['total']==1
    assert len(client.get('/api/export?kind=golden').text.splitlines())==1
    assert len(client.get('/api/export?kind=audit').text.splitlines())==2
    assert len(client.get('/api/export').text.splitlines())==3
    store.initialise(db)
    assert client.get('/api/notice?id=test').json()['review']['id']==changed.json()['revision']

def test_invalid_review(client):
    assert review(client,decision={'votable':'MAYBE'}).status_code==422
    assert review(client,reviewer='').status_code==422
    assert review(client,reviewer='   ').status_code==422
    assert review(client,record='missing').status_code==404
    assert review(client,decision=None).status_code==422
    assert client.get('/api/notice?id=missing').status_code==404
    assert client.get('/api/export?kind=bad').status_code==422

def test_flag_not_golden(client):
    assert review(client,decision=None,action='FLAG').status_code==201
    assert client.get('/api/export?kind=golden').text==''

def test_reproduction_immutable(db,client):
    first=run_batch(db,classifier_factory=factory)
    second=run_batch(db,reproduce=first,classifier_factory=factory)
    assert first!=second
    runs=client.get('/api/runs').json()
    assert len(runs)==2 and runs[0]['dataset_hash']==runs[1]['dataset_hash']
    assert all(r['persisted']==3 for r in runs)
    assert runs[0]['benchmark']['failed_rows']==0
    with store.connect(db) as c:
        with pytest.raises(sqlite3.IntegrityError):c.execute("UPDATE predictions SET source_hash='x'")
        with pytest.raises(sqlite3.IntegrityError):c.execute('DELETE FROM predictions')

def test_golden_split_isolation(db,client,tmp_path):
    for s in ['train','test','validation']:assert review(client,record=s).status_code==201
    out=tmp_path/'export';m=export_dataset(out,db)
    assert m['counts']=={'train':1,'validation':1,'test':1}
    assert 'train Shareholders' in (out/'train.jsonl').read_text()
    assert 'test Shareholders' not in (out/'train.jsonl').read_text()
    assert 'validation Shareholders' not in (out/'train.jsonl').read_text()
    with pytest.raises(ValueError,match='20 distinct'):train(out,tmp_path/'model',dry_run=True)
    with pytest.raises(FileExistsError):export_dataset(out,db)

def test_immutable_reviews_and_source(db,client):
    review(client)
    with store.connect(db) as c:
        for query in ['DELETE FROM reviews',"UPDATE reviews SET reviewer='other'","UPDATE notices SET split='train'",'DELETE FROM notices']:
            with pytest.raises(sqlite3.IntegrityError):c.execute(query)

def test_csrf(client):
    assert client.post('/api/reviews',json={},headers={'Origin':'https://evil.example'}).status_code==403
    assert client.get('/api/health',headers={'Host':'evil.example'}).status_code==403

def test_csp(client):
    h=client.get('/').headers
    assert "connect-src 'self'" in h['content-security-policy']
    assert h['x-content-type-options']=='nosniff'

def test_failed_model_visible(db,client):
    class Broken:
        load_time_ms=0
        def classify_batch(self,x):raise RuntimeError('Device problem')
        def classify(self,x):raise RuntimeError('Device problem')
    run_batch(db,classifier_factory=lambda _:Broken())
    run=client.get('/api/runs').json()[0]
    assert run['status']=='COMPLETED_WITH_ERRORS'
    assert run['benchmark']['failed_rows']==3
    assert client.get('/api/overview').json()['analysed']==0
    assert client.get('/api/notices').json()['items'][0]['error']

def test_comparison(client,db):
    assert client.get('/api/comparison').json()==[]
    first=run_batch(db,classifier_factory=factory)
    assert review(client,run=first).status_code==201
    row=client.get('/api/comparison').json()[0]
    assert row['accuracy']==1 and row['verified_n']==1
    assert row['auto_coverage']==0

def test_other_reference_date_not_reused(client,db,config):
    import copy
    first=run_batch(db,classifier_factory=factory)
    assert review(client,run=first).status_code==201
    later=copy.deepcopy(config);later['evaluation_date']='2026-11-01'
    second=run_batch(db,config=later,classifier_factory=factory)
    assert client.get('/api/performance?run_id='+second).json()['n']==0
    assert client.get('/api/performance?run_id='+first).json()['n']==1

def test_full_factor_correctness_in_audit(client,db):
    run=run_batch(db,classifier_factory=factory)
    assert review(client,run=run,decision={'votable':'YES','deadline_status':'UNKNOWN'}).status_code==201
    d=client.get('/api/notice?id=test').json()
    assert d['review']['ai_correct']==0 # status remains VOTABLE but deadline differs
    assert json.loads(d['review']['context'])['evaluation_date']=='2026-10-16'

def test_foreign_origin_job_rejected(client):
    assert client.post('/api/runs',json={},headers={'Origin':'https://example.org'}).status_code==403

def test_exports_are_structured_json(client,db):
    run=run_batch(db,classifier_factory=factory)
    assert review(client,run=run).status_code==201
    r=json.loads(client.get('/api/export?kind=results').text.splitlines()[0])
    assert isinstance(r['result'],dict) and isinstance(r['metadata'],dict)
    golden=json.loads(client.get('/api/export?kind=golden').text.splitlines()[0])
    assert isinstance(golden['label'],dict) and isinstance(golden['context'],dict)
    assert golden['label']['votable']=='YES'
