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
