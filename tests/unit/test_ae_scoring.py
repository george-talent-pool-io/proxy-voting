import copy
from evaluation.ae_scoring import project
from semantic_pipeline.models import factor


def test_new_schema_union_is_not_stale_legacy_auxiliary_head():
    from semantic_pipeline.schema import RESTRICTIONS
    preds={k:factor('NO','MODEL') for k in RESTRICTIONS}
    preds['registration_required']=factor('YES','LOCAL_LLM')
    preds['other_restriction']=factor('NO','LAYA_LEGACY_BROAD')
    row={'id':'x','result':{'reconciliation':{'predicates':preds}}}
    untouched=copy.deepcopy(row)
    corrected,audit=project([row],'C')
    assert row==untouched
    assert 'other_restriction' not in corrected[0]['result']['reconciliation']['predicates']
    assert audit[0]['canonical_broad_value']=='YES';assert audit[0]['value_changed']
    for arm in 'ABDE':assert project([row],arm)[0][0]==row


def test_wholly_unsupported_expanded_schema_keeps_supported_legacy_union():
    from semantic_pipeline.schema import RESTRICTIONS
    preds={k:factor('NOT_SUPPORTED','UNAVAILABLE') for k in RESTRICTIONS}
    preds['other_restriction']=factor('YES','LAYA_LEGACY_BROAD')
    row={'id':'x','result':{'reconciliation':{'predicates':preds}}}
    assert project([row],'C')[0][0]==row
