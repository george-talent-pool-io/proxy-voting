"""Production HTTP/UI workflow with explicitly labelled model-only doubles.

Real import, reviews, split isolation, jobs, releases, calibration, blind
qualification, task persistence and permission checks execute unchanged.
No learned weights or quality claim are produced by this browser fixture.
"""
import json
import os
from pathlib import Path
from types import SimpleNamespace

if os.environ.get('VOTING_BROWSER_CONTRACT') != 'ISOLATED_TEST_ONLY':
    raise RuntimeError('Customer browser doubles require an explicit isolated test environment')
if not Path(os.environ['VOTING_DB']).parent.name.startswith('client-browser'):
    raise RuntimeError('Never install browser doubles in a customer workspace')

from training.framework import jobs, seeds, releases, trainers
from production import learning, worker
from training.framework.bundle import write
from semantic_pipeline.schema import PREDICATES
from semantic_pipeline.evidence import verify_evidence
from tests.unit.test_learning_comparison import result

models = jobs.WORKSPACE.parent / 'models'
base = models / 'explicit-browser-double'
base.mkdir(parents=True, exist_ok=True)
if not (base / 'model.safetensors').exists():
    (base / 'model.safetensors').write_bytes(b'EXPLICIT_BROWSER_DOUBLE_NOT_MODEL_WEIGHTS')
    (base / 'rl_agent_config.json').write_text('{}')
seed = jobs.member('seeds', 'browser-foundation')
if not seed.exists():
    seeds.freeze({'backend':'LAYA_SDK', 'family':'LAYA', 'model_path':str(base),
                  'base_model_id':'EXPLICIT_BROWSER_DOUBLE_NOT_PRETRAINED',
                  'base_revision':'SOFTWARE_CONTRACT_ONLY', 'device':'cpu',
                  'max_length':512}, seed)


def train_double(bundle, output, spec):
    output.mkdir()
    (output / 'model.safetensors').write_bytes(b'EXPLICIT_BROWSER_CHECKPOINT_NOT_TRAINED_WEIGHTS')
    (output / 'rl_agent_config.json').write_text('{}')
    return {'backend':'EXPLICIT_BROWSER_DOUBLE', 'weights_updated':False,
            'semantic_quality_evaluated':False, 'reload_parity':{'passed':True,'scope':'SOFTWARE_DOUBLE_ONLY'}}


trainers.train_laya = train_double


class CompletedTraining:
    """Replace only the expensive training process, retain the real job engine."""
    def __init__(self, args, **kw):
        if args[1:4] != ['-m','training.framework','execute']:
            raise AssertionError('Unexpected subprocess in isolated browser training')
        jobs.execute(args[4])
        self.returncode = 0

    def poll(self):
        return self.returncode


learning.subprocess = SimpleNamespace(Popen=CompletedTraining)


class ModelDouble:
    def __init__(self, path):
        self.path = path

    def analyse(self, text, **kwargs):
        value = result()
        for key, pred in value['predicates'].items():
            choices = ['VOTABLE','NOT_VOTABLE','UNCERTAIN'] if key == 'votability' else ['YES','NO','UNKNOWN']
            pred.update(scores={c:.998 if c == pred['value'] else .001 for c in choices},
                        evidence=[verify_evidence(text,text)], source='EXPLICIT_BROWSER_MODEL_DOUBLE')
        return value

    def close(self):
        pass


OriginalReleaseModel = releases.ReleaseModel
releases.ReleaseModel = lambda root, **kw: OriginalReleaseModel(root, laya_factory=ModelDouble,
                                                               llm_factory=ModelDouble, **kw)


def run_campaign(root):
    learning.run(root)
    return {'completed':True, 'model_backend':'EXPLICIT_BROWSER_DOUBLE', 'automatic_resume':False}


learning.spawn = run_campaign
original_submit = worker.submit


def submit_and_execute(ident, kind, payload, actor):
    response = original_submit(ident, kind, payload, actor)
    if ident.startswith('execute-'):
        worker.run_once()
    return response


worker.submit = submit_and_execute
from apps.api.production import app
