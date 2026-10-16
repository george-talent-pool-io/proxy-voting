"""Readable delivery report formatting; all data here are software fixtures."""
from scripts.watch_cascade_completion import write_full_summary
from semantic_pipeline.metrics import summarize
from tests.unit.test_cascade_reporting import rows


def test_completion_summary_contains_priority_metrics_without_claiming_customer_accuracy(tmp_path):
    (tmp_path/'AGGREGATION_SELECTIVE_CASCADE_EVALUATION.md').write_text('Detailed SOFTWARE FIXTURE report.\n')
    m=summarize([rows()])
    value={'datasets':{'challenge':{'C1':m}},
        'transitions':{'challenge':{'C1':{'semantic_transitions':{'wrong -> correct':3,'correct -> wrong':1,'correct -> correct':4}}}},
        'aggregation_only_predicate_deltas':{'challenge':{}},'ORACLE_ROUTING':{},
        'primary_selection':{'selected':'SOFTWARE_FIXTURE_ONLY','ranking':'Validation-only fixture'},
        'routing_selection':{'selected':{'laya_only_coverage':.3,'semantic_agreement':.8},'always':{'semantic_agreement':.8}}}
    target=write_full_summary(value,tmp_path);text=target.read_text()
    assert '| C1 | 8 | 3 | 1 | 4 | 0 |' in text
    assert 'Critical-positive recall by predicate' in text
    assert 'Median / p95 seconds' in text and 'Selective coverage and oracle routing' in text
    assert 'Customer accuracy UNKNOWN' in text and 'Automation disabled' in text
    assert 'share_blocking' in text and 'poa_required' in text
    assert write_full_summary(value,tmp_path)==target
