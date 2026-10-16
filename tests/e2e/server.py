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
