import pytest
from evaluation.layer_metrics import measure_layers,diagnose_layers

def test_three_distinct_denominators_and_accuracies():
 m=measure_layers(parser_cases=[{'expected':{'CAEV':'MEET','RDDT':'20261020'},'observed':{'CAEV':'MEET','RDDT':'20261021'}}],semantic_cases=[{'expected':{'registration':True,'blocking':False},'observed':{'registration':True,'blocking':False}}],decision_cases=[{'expected':'VOTABLE_WITH_RESTRICTION','observed':'VOTABLE'}])
 assert m['parser']['accuracy']==.5 and m['parser']['total']==2
 assert m['semantic']['accuracy']==1 and m['semantic']['total']==2
 assert m['end_to_end']['accuracy']==0 and m['end_to_end']['total']==1
 assert m['parser']['exact_match_accuracy']==0

def test_no_reference_labels_means_unknown_not_zero_or_perfect():
 m=measure_layers()
 assert all(r['accuracy'] is None and r['total']==0 for r in m.values())

def test_missing_extraction_and_explicit_absence():
 m=measure_layers(parser_cases=[{'expected':{'CAEV':'MEET','RDDT':None},'observed':{'RDDT':'invented'}}])
 assert m['parser']['correct']==0 and m['parser']['total']==2
 with pytest.raises(ValueError,match='reference'):measure_layers(parser_cases=[{'expected':{},'observed':{}}])

def test_compensating_and_overlapping_errors_are_not_hidden():
 cases=[{'parser_correct':False,'semantic_correct':True,'final_correct':True},{'parser_correct':False,'semantic_correct':False,'final_correct':False},{'parser_correct':True,'semantic_correct':True,'final_correct':False},{'final_correct':False}]
 assert diagnose_layers(cases)=={'correct_final_with_intermediate_mismatch':1,'parser_and_semantic_mismatch':1,'business_rule_or_final_label_mismatch':1,'insufficient_reference_labels':1}

def test_software_deadline_is_not_a_semantic_model_prediction():
 from evaluation.layer_metrics import semantic_case
 d={'votable':'YES','share_blocking':False,'poa_required':False,'other_restriction':False,'deadline_status':'OPEN'}
 row={'true_decision':d,'decision':d,'scores':{k:{} for k in ['votable','share_blocking','poa_required','other_restriction','deadline_present']}}
 case=semantic_case(row)
 assert set(case['expected'])=={'votable','share_blocking','poa_required','other_restriction'}
 assert 'deadline_status' not in case['observed'] and 'deadline_present' not in case['expected']
