"""Model quality tests opt in. Failures are evidence; never replaced by a rule engine."""
import json
import os
from pathlib import Path
import pytest
CASES=json.loads(Path('tests/fixtures/semantic.json').read_text())

def test_challenge_manifest():
    assert len(CASES)>=50
    assert len({c['id'] for c in CASES})==len(CASES)
    assert all(c['reference_date']=='2026-10-16' and 'synthetic' in c['provenance'] for c in CASES)

@pytest.fixture(scope='module')
def real_laya():
    from classifier.laya_classifier import LayaClassifier
    return LayaClassifier()

@pytest.mark.model
@pytest.mark.skipif(os.environ.get('RUN_MODEL_TESTS')!='1',reason='Opt-in real-model challenge; use RUN_MODEL_TESTS=1, no weight downloads')
@pytest.mark.parametrize('case',CASES,ids=[c['id'] for c in CASES])
def test_real_model_semantics(real_laya,case):
    r=real_laya.classify(case['text'])
    observed={**r.decision.model_dump(),'classification':r.classification.value}
    for key,value in case['expected'].items():assert observed[key]==value,f'{key}: {observed[key]} != {value}'
