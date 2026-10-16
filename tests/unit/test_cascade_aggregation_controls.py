from cascade.aggregation import AggregationConfig,states
from cascade.aggregation_controls import matched_reduce
from tests.unit.test_evidence_aggregation import native


def test_equal_absence_policy_does_not_treat_unexplained_native_no_as_waiver():
    cfg=AggregationConfig(strategy='MAX_POSITIVE')
    irrelevant=states('Read the agenda.','share_blocking',native(['NO']))
    assert matched_reduce(irrelevant,cfg)['value']=='NO'
    relevant=states('Shares will be blocked.','share_blocking',native(['NO']))
    assert matched_reduce(relevant,cfg)['value']=='UNKNOWN'
    historical=states('Historically shares were blocked.','share_blocking',native(['NO']))
    assert matched_reduce(historical,cfg)['value']=='UNKNOWN'


def test_comparators_keep_their_original_disagreement_behavior():
    ps=states('Shares will be blocked. Shares will not be blocked.','share_blocking',native(['YES','NO']))
    assert matched_reduce(ps,AggregationConfig(strategy='MAX_POSITIVE'))['value']=='YES'
    assert matched_reduce(ps,AggregationConfig(strategy='SUPERSESSION_AWARE'))['value']=='UNKNOWN'
