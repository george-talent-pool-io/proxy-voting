"""Same immutable 57 expectations against the frozen selected candidate.
Failures are retained scientific evidence; no alternate/relaxed expectations.
"""
import json,os
from pathlib import Path
import pytest
CASES=json.loads(Path('tests/fixtures/semantic.json').read_text())
pytestmark=[pytest.mark.model,pytest.mark.skipif(os.environ.get('RUN_FINETUNED_MODEL_TESTS')!='1',reason='Opt-in frozen candidate quality regression')]

@pytest.fixture(scope='module')
def fine_tuned():
 from training.synthetic_protocol import verify_freeze
 from classifier.laya_classifier import LayaClassifier
 return LayaClassifier(verify_freeze()['config'])

@pytest.mark.parametrize('case',CASES,ids=[c['id'] for c in CASES])
def test_frozen_candidate_semantics(fine_tuned,case):
 r=fine_tuned.classify(case['text']);observed={**r.decision.model_dump(),'classification':r.classification.value}
 for k,v in case['expected'].items():assert observed[k]==v,f'{k}: {observed[k]} != {v}'
