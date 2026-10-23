import copy
import pytest
from production.selection import evaluate,ranking
from semantic_pipeline.schema import PREDICATES
from tests.unit.test_learning_comparison import result


def test_selection_rejects_nonvalidation_truth():
    with pytest.raises(ValueError,match='VALIDATION only'):evaluate([],{},role='FROZEN_TEST')


def test_all_semantic_labels_right_does_not_mask_a_wrong_final_status():
    r=result();truth={'a':{'target':{k:r['predicates'][k]['value'] for k in PREDICATES},
                        'expected_final_status':r['decision']['classification'],'expected_deadline_status':r['deadline']['status']}}
    r['decision']['classification']='DEADLINE_PASSED'
    if truth['a']['expected_final_status']=='DEADLINE_PASSED':r['decision']['classification']='NOT_VOTABLE'
    d=evaluate([{'id':'a','result':r}],truth,role='VALIDATION')
    assert d['complete_output']=={'support':1,'correct':0}
    assert d['final_status']['correct']==0


def test_complete_output_model_beats_higher_field_accuracy_with_bad_decisions():
    metrics={'cases':100,'cases_satisfying_all_supplied_assertions':99,'correct_assertions':899,'assertions':900,'median_latency_ms':1}
    a={'metrics':metrics,'decision_evaluation':{'cases':100,'complete_output':{'support':100,'correct':50},'final_status':{'support':100,'correct':50}}}
    b=copy.deepcopy(a);b['metrics']['correct_assertions']=890
    b['decision_evaluation']['complete_output']['correct']=95;b['decision_evaluation']['final_status']['correct']=96
    assert ranking(b)['rank']>ranking(a)['rank']


def test_partial_final_labels_are_explicit_semantic_only_selection():
    report={'metrics':{'cases':57,'cases_satisfying_all_supplied_assertions':30,'correct_assertions':59,'assertions':95,'median_latency_ms':10},
            'decision_evaluation':{'cases':57,'complete_output':{'support':4,'correct':4},'final_status':{'support':4,'correct':4}}}
    r=ranking(report)
    assert r['scope']=='SEMANTIC_ONLY_INCOMPLETE_DECISION_TRUTH'
    assert r['rank'][0]==30/57
