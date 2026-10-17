"""Actual pinned weights/native logits/shared runtime; opt-in, never a mock."""
import os,pytest
pytestmark=[pytest.mark.local_llm,pytest.mark.model,pytest.mark.skipif(os.environ.get('RUN_FAST_CASCADE_LOCAL')!='1',reason='RUN_FAST_CASCADE_LOCAL=1 runs real local Laya + Qwen')]

def test_real_laya_native_qwen_and_full_qwen_share_pinned_runtime():
    from fast_cascade.laya import BatchedLaya
    from fast_cascade.models import SharedQwen
    from fast_cascade.pipeline import Pipeline
    from fast_cascade.routing import Policy
    qwen=SharedQwen();laya=BatchedLaya(8)
    # Fixed TRAIN-only software smoke. Thresholds force the full integration path;
    # these outputs never select a production routing policy or count as quality.
    text='Investor service memo: a ballot for the forthcoming class meeting is open. Lodgement of the proxy ballot locks the instructed position until the chair closes proceedings. The current voting cutoff is 26 November 2026.'
    result=Pipeline(Policy('INTEGRATION_FORCE_PATH',1.,1.,1.,1.,1.),laya=laya,qwen=qwen).analyse(text)
    assert result['gear2'] and result['full_qwen']['invoked'] and result['full_qwen']['valid']
    assert result['gear2']['runtime']['same_process_for_both_gears']
    assert result['full_qwen']['model_digest']=='25b843619e944cd0ae6069f94ff4e5e26a16e109ccbc0a66a0f05979ed70098e'
    for p in result['gear2']['predicates'].values():
        assert set(p['raw_model_probability'])=={'YES','NO','UNKNOWN'}
        assert sum(p['raw_model_probability'].values())==pytest.approx(1)
        assert p['confidence'] is None and p['raw_runtime_response']['tokens_predicted']==1
    assert result['manual_review_required'] and not result['automation_enabled']
