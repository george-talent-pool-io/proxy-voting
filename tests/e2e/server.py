"""Isolated browser-test server. Contract doubles never enter the demonstration DB."""
import os
from pathlib import Path
if Path(os.environ.get('VOTING_DB','')).name!='e2e.sqlite':raise RuntimeError('E2E server requires an isolated database')
from tests.conftest import ContractAgent
from classifier.laya_classifier import LayaClassifier,load_config
import scripts.run_batch as batches
original_run=batches.run_batch

def test_run(*args,**kwargs):
    config=load_config();config.update(checkpoint='test-double-not-laya',checkpoint_revision='automated-e2e-only')
    return original_run(*args,config=config,classifier_factory=lambda c:LayaClassifier(c,agent=ContractAgent()),**kwargs)
batches.run_batch=test_run
from apps.api.main import app

# Explicit software-contract fixture for persisted Notice Detail execution tests.
# Real-model inference is tested separately under the local_llm marker.
os.environ['CLASSIFICATION_ARCHITECTURE']='FULL_HYBRID'
os.environ['LLM_ENABLED']='false'
import semantic_pipeline.experiment as semantic_experiment
_original_laya_for=semantic_experiment.laya_for
class _SemanticContractModel:
    def analyse(self,text):
        from tests.unit.test_semantic_pipeline import specialist
        return specialist('UNKNOWN')
semantic_experiment.laya_for=lambda arm:_SemanticContractModel() if arm=='E' else _original_laya_for(arm)
from apps.api import semantic_views
semantic_views.ROOT=Path(os.environ['VOTING_DB']).parent
(semantic_views.ROOT/'data').mkdir(exist_ok=True)

# Event-lifecycle browser contracts use an isolated workspace and explicit model
# doubles. The separate real qualification receipt executes official models and
# the detached process worker; these browser doubles make NO model-quality claim.
import json
from apps.api import store, training_views
from training.framework import jobs, queue
from training.framework import trainers, runtime
from training.framework.bundle import create_bundle
from tests.unit.test_training_framework import example
jobs.WORKSPACE=Path(os.environ['VOTING_DB']).parent/'framework'
training_views.WORKSPACE=jobs.WORKSPACE
jobs.active_experiments=lambda:[]
os.environ['TRAINING_EXECUTION_ENABLED']='true'
queue.tables()
with store.connect() as c:
    for row in c.execute("SELECT id FROM learning_tasks WHERE state IN ('QUEUED','RUNNING')").fetchall():
        queue.transition(c,row['id'],'INTERRUPTED',{'reason':'Copied snapshot; no browser fixture may resume a real training task'})
    # A real application's selected release refers to artifacts outside this
    # isolated fixture workspace. Keep it inactive in the copied DB; the real
    # selection/restart path is qualified separately, without model doubles.
    if c.execute("SELECT 1 FROM sqlite_master WHERE type='table' AND name='learning_release_history'").fetchone():
        c.executescript('DROP TRIGGER IF EXISTS immutable_release_update; DROP TRIGGER IF EXISTS immutable_release_delete; DELETE FROM learning_release_history;')
_base=jobs.WORKSPACE/'contract-base';_base.mkdir(parents=True,exist_ok=True)
(_base/'EXPLICIT_TEST_DOUBLE.txt').write_text('Browser contract, not a pretrained model')
_bundle=jobs.WORKSPACE/'bundles/browser-seed'
if not _bundle.exists():create_bundle([example(),example('b','VALIDATION')],_bundle)
def _preflight(bundle,spec):
    from training.framework.bundle import load_bundle
    m,_=load_bundle(bundle)
    return {'ready':True,'reasons':[],'label_origins':m['label_origins'],'versions':{'runtime':'BROWSER_CONTRACT_DOUBLE'},'hardware':{'device':'TEST_DOUBLE'}}
jobs.preflight=_preflight
def _train(bundle,output,spec):
    output.mkdir();(output/'BROWSER_CONTRACT.txt').write_text('Explicit model execution double; no ML training')
    return {'runtime':'BROWSER_CONTRACT_DOUBLE','weights_updated':False}
trainers.train_laya=_train
def _dispatch(database=None):
    for t in queue.listing():
        if t['state']!='QUEUED':continue
        with store.connect() as c:queue.transition(c,t['id'],'RUNNING',{'backend':'EXPLICIT_BROWSER_DOUBLE'})
        jobs.execute(jobs.WORKSPACE/'jobs'/t['job_id'])
        with store.connect() as c:queue.transition(c,t['id'],'COMPLETED',{'backend':'EXPLICIT_BROWSER_DOUBLE'})
    return {'worker':'EXPLICIT_SYNCHRONOUS_BROWSER_DOUBLE'}
queue.spawn=_dispatch
class _RegisteredContract:
    def __init__(self,job):self.job=job
    def analyse(self,text,**kw):
        from tests.unit.test_learning_comparison import result
        from classifier.preprocessing import source_hash
        from semantic_pipeline.evidence import verify_evidence
        r=result();r.update(input_hash=source_hash(text),input_type='UNSTRUCTURED_NOTICE',parser=None,
                             checkpoint_manifest_sha256='BROWSER_CONTRACT_ONLY')
        if 'Shareholders can vote.' in text:r['predicates']['votability']['evidence']=[verify_evidence(text,'Shareholders can vote.')]
        return r
    def close(self):pass
runtime.RegisteredModel=_RegisteredContract
