"""Intentional real-model smoke, separate from ordinary software tests."""
import os
import pytest
pytestmark=[pytest.mark.local_llm,pytest.mark.qwen_local,pytest.mark.model,
    pytest.mark.skipif(os.environ.get('RUN_DOMAIN_LOCAL')!='1',reason='RUN_DOMAIN_LOCAL=1 executes the pinned local Qwen model')]

def test_real_constrained_qwen_returns_every_allowed_native_score():
    from qwen_domain.runtime import select
    from qwen_domain.constrained import ConstrainedQwen
    select('CONSTRAINED_QWEN');model=ConstrainedQwen()
    result=model.classify('Custodian instruction: securities tendered for the vote are immobilised until the meeting closes.','share_blocking')
    assert result['valid'] and set(result['raw_model_probability'])=={'YES','NO','UNKNOWN'}
    assert sum(result['raw_model_probability'].values())==pytest.approx(1)
    assert result['confidence'] is None and result['raw_runtime_response']['tokens_predicted']==1
    assert result['prediction_rule'].startswith('ARGMAX')
