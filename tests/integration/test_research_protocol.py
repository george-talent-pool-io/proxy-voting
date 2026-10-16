import json,sqlite3
from pathlib import Path
import pytest
from training.study import create_study,load_study,lock_test_labels
from scripts.run_batch import run_batch
from tests.integration.test_workflow import factory
from training import synthetic_protocol as protocol

def test_frozen_cohort_before_labels(db,tmp_path):
 run_batch(db,classifier_factory=factory)
 m=create_study(tmp_path/'study',db,targets={'train':1,'validation':1,'test':1})
 assert len(m['records'])==3 and sum(r['selected'] for r in m['records'])==3
 assert next(r for r in m['records'] if r['split']=='test')['partition']=='FROZEN_TEST'
 assert load_study(db)==m
 with pytest.raises(ValueError,match='frozen'):create_study(tmp_path/'second',db)
 with pytest.raises(ValueError,match='verification'):lock_test_labels(db)

def test_protocol_reads_whitelisted_members_only(monkeypatch):
 seen=[];real=protocol.ZipFile
 class Spy:
  def __init__(self,*args):self.z=real(*args)
  def __enter__(self):return self
  def __exit__(self,*args):self.z.close()
  def read(self,name):seen.append(name);return self.z.read(name)
 monkeypatch.setattr(protocol,'ZipFile',Spy)
 assert len(protocol.rows('train'))==300 and len(protocol.rows('validation'))==100 and len(protocol.rows('blind'))==100
 assert seen==list(protocol.ALLOWED.values())
 with pytest.raises(KeyError):protocol.rows('all')

def test_answer_key_locked_until_complete_predictions(tmp_path,monkeypatch):
 monkeypatch.setattr(protocol,'ROOT',tmp_path)
 monkeypatch.setattr(protocol,'verify_freeze',lambda:{})
 opened=[]
 monkeypatch.setattr(protocol,'ZipFile',lambda *a:opened.append(a))
 with pytest.raises(FileNotFoundError):protocol.score()
 assert not opened

def test_predictions_cannot_be_overwritten(tmp_path):
 p=tmp_path/'p.json';protocol.write(p,{'old':1})
 with pytest.raises(FileExistsError):protocol.write(p,{'new':2})
 assert json.loads(p.read_text())=={'old':1}

def test_research_api(client):
 e=client.get('/api/experiment').json()
 assert not e['quality_gate']['passed'] and not e['quality_gate']['automation_enabled']
 assert 'synthetic' in e['provenance']
 assert client.get('/api/experiment/errors?model=llm').status_code==422
 assert client.get('/api/experiment/errors?field=fake').status_code==422
 assert client.get('/api/experiment/errors?min_confidence=nan').status_code==422


def test_blind_review_attestation_and_frozen_revision(client,db,tmp_path):
 from tests.integration.test_workflow import review
 from evaluation.evaluate import evaluate
 from apps.api import store
 run=run_batch(db,classifier_factory=factory)
 create_study(tmp_path/'study',db,targets={'train':1,'validation':1,'test':1})
 detail=client.get('/api/notice?id=test&blind=true').json()
 assert detail['prediction'] is None and detail['blind_review'] is True
 r=review(client,run=run,domain_expert_attested=True,blind_review=True)
 assert r.status_code==201
 locked=lock_test_labels(db)
 assert locked['labels'][0]['revision']==r.json()['revision']
 # A correction is kept as a new review, never silently used to rewrite locked test truth.
 correction=review(client,run=run,expected_revision=r.json()['revision'],decision={'votable':'NO'},notes='Later revision after test lock')
 assert correction.status_code==201
 assert evaluate(run,path=db)['accuracy']==1.
 assert evaluate(run,path=db)['label_revision_manifest'][0]['review_revision']==r.json()['revision']
 with store.connect(db) as c:
  with pytest.raises(sqlite3.IntegrityError,match='immutable'):c.execute('DELETE FROM study_label_locks')
 assert client.get('/api/notices?cohort=true').json()['total']==3


def test_semantic_challenge_cannot_enter_training(tmp_path):
 from tests.integration.test_training import dataset
 from training.train import train
 root=dataset(tmp_path);p=root/'manifest.json';m=json.loads(p.read_text())
 m['label_revisions'][0]['record_id']='agm';p.write_text(json.dumps(m))
 with pytest.raises(ValueError,match='challenge'):train(root,tmp_path/'forbidden',dry_run=True)


def test_supplied_exception_does_not_allow_arbitrary_rows(tmp_path):
 from tests.integration.test_training import dataset
 from training.train import train
 root=dataset(tmp_path)
 with pytest.raises(ValueError,match='exact original'):train(root,tmp_path/'forbidden',dry_run=True,supplied_synthetic_protocol=True)


def test_frozen_code_changes_detected_before_prediction(tmp_path,monkeypatch):
 monkeypatch.setattr(protocol,'ROOT',tmp_path)
 f=tmp_path/'criteria.json';f.write_text('original');archive=tmp_path/'source.zip';archive.write_bytes(b'fixed source')
 monkeypatch.setattr(protocol,'ARCHIVE',archive)
 protocol.write(tmp_path/'FREEZE.json',{'archive_sha256':protocol.sha(archive),'files':{str(f):protocol.sha(f)}})
 assert protocol.verify_freeze()['files']
 f.write_text('changed')
 with pytest.raises(ValueError,match='modified'):protocol.verify_freeze()


def test_decision_evidence_is_hidden_during_blind_review(client,db):
 run_batch(db,classifier_factory=factory)
 ordinary=client.get('/api/notice?id=test').json()
 assert ordinary['decision_evidence'] and ordinary['decision_evidence_version']=='source-summary-v2'
 blind=client.get('/api/notice?id=test&blind=true').json()
 assert blind['decision_evidence']==[] and blind['prediction'] is None


def test_customer_metrics_do_not_reuse_synthetic_or_derived_status_accuracy(client,db):
 from tests.integration.test_workflow import review
 run=run_batch(db,classifier_factory=factory)
 assert review(client,run=run).status_code==201
 stages=client.get('/api/metric-layers').json()
 assert stages['synthetic_included'] is False
 assert all(m['accuracy'] is None for m in stages['layers'].values())
 assert 'separately verified' in stages['layers']['end_to_end']['reason']
 assert client.get('/api/overview').json()['metric_layers']==stages
