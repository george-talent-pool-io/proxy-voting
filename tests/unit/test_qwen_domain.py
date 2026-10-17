"""Synthetic/software contracts. These tests do not claim real-model quality."""
import copy,json
from pathlib import Path
import pytest
from qwen_domain.corpus import render,validate_records
from qwen_domain.protocol import write,append,sha,load_training,load_inputs
from qwen_domain.confidence import features,confidence_output,calibration_metrics,CorrectnessCalibrator,decision_confidence
from qwen_domain.constrained import allowed_probabilities

@pytest.mark.parametrize('family',[0,12,32,64,65,66,67,68,88,89,92,95])
def test_constructed_pair_changes_one_semantic_fact_and_has_exact_evidence(family):
    data=[render(family,3,m) for m in [0,1]]
    q=validate_records(data)
    assert q['minimal_pairs']==1 and q['unique_texts']==2
    assert data[0]['generation_family']==data[1]['generation_family']

def test_deadline_pair_preserves_date_information():
    data=[render(0,0,m) for m in [0,1]]
    assert data[0]['expected']['deadline_status']==data[1]['expected']['deadline_status']=='UNKNOWN'
    assert data[0]['deadline_iso_truth']==data[1]['deadline_iso_truth'] is None

def test_training_loader_rejects_symlink_to_protected_answers(tmp_path):
    private=tmp_path/'private';private.mkdir();source=private/'FROZEN.labels.jsonl'
    append(source,{'id':'frozen','split':'TRAIN'})
    link=tmp_path/'train.jsonl';link.symlink_to(source)
    write(tmp_path/'manifest.json',{'splits':{'TRAIN':{'labels':'train.jsonl','labels_sha256':sha(link),'ids':['frozen']}}})
    with pytest.raises(ValueError,match='Protected'):load_training(tmp_path/'manifest.json')

def test_copied_frozen_membership_cannot_masquerade_as_training(tmp_path):
    path=tmp_path/'train.jsonl';append(path,{'id':'one','split':'SYNTHETIC_FROZEN_TEST'})
    write(tmp_path/'manifest.json',{'splits':{'TRAIN':{'labels':'train.jsonl','labels_sha256':sha(path),'ids':['one']}}})
    with pytest.raises(ValueError,match='membership'):load_training(tmp_path/'manifest.json')
    with pytest.raises(ValueError):load_training(tmp_path/'manifest.json','CALIBRATION')

def test_inference_input_reader_rejects_fact_specification(tmp_path):
    p=tmp_path/'inputs.jsonl';append(p,{'id':'one','text':'source','fact_specification':{'poa_required':'YES'}})
    write(tmp_path/'manifest.json',{'splits':{'VALIDATION':{'inputs':'inputs.jsonl','inputs_sha256':sha(p)}}})
    with pytest.raises(ValueError,match='Labels leaked'):load_inputs(tmp_path/'manifest.json','VALIDATION')

def test_no_numeric_confidence_before_calibration_and_unsupported_languages_force_review():
    p={'value':'YES','evidence':[{'valid':True,'text':'POA required.'}]}
    out=confidence_output('POA required.','poa_required',p)
    assert out['confidence'] is None and out['heuristic_band']=='HIGH' and out['manual_review_required']
    out=confidence_output('Vollmacht erforderlich.','poa_required',p,language='de')
    assert out['force_review'] and out['heuristic_band']=='LOW' and out['confidence'] is None

def test_raw_token_probability_is_only_an_observable_feature():
    p={'value':'YES','evidence':[],'raw_model_probability':{'YES':.98,'NO':.01,'UNKNOWN':.01}}
    out=features('A condition is stated.','poa_required',p)
    assert out['features']['raw_top_probability']==.98 and out['confidence'] is None
    assert out['heuristic_band']=='LOW'

def test_decision_trust_ignores_irrelevant_restriction_for_nonvotable():
    result=decision_confidence('NOT_VOTABLE',{'votability':{'value':'NOT_VOTABLE','confidence':.9},'poa_required':{'value':'UNKNOWN','confidence':None}})
    assert result['minimum_decisive_trust_score']==.9
    assert result['calibrated_decision_confidence'] is None

def test_calibration_metrics_have_hand_calculated_values():
    m=calibration_metrics([True,False],[.8,.2])
    assert m['brier']==pytest.approx(.04) and m['ece']==pytest.approx(.2)

def test_calibrator_refuses_fit_evaluation_group_leakage():
    data=[{'split':'CALIBRATION','duplicate_group':'same','calibration_fold':fold} for fold in ['FIT','EVALUATION']]
    with pytest.raises(ValueError,match='leakage'):CorrectnessCalibrator('model').fit(data)

def test_calibrator_persistence_and_model_identity(tmp_path):
    data=[]
    for fold,n in [('FIT',4000),('EVALUATION',200)]:
        for i in range(n):
            correct=i%2==0
            data.append({'predicate':'poa_required','split':'CALIBRATION','duplicate_group':fold+str(i),'calibration_fold':fold,'features':{'observed_evidence_quality':.9 if correct else .1},'correct':correct})
    c=CorrectnessCalibrator('test-model');report=c.fit(data)
    assert report['poa_required']['status']=='SYNTHETIC_POPULATION_CALIBRATION_VALIDATED'
    p=tmp_path/'cal.joblib';c.save(p);again=CorrectnessCalibrator.load(p,'test-model')
    assert again.predict('poa_required',{'observed_evidence_quality':.9},'test-model')==c.predict('poa_required',{'observed_evidence_quality':.9},'test-model')
    with pytest.raises(ValueError,match='identity'):CorrectnessCalibrator.load(p,'other-model')
    with pytest.raises(ValueError):c.save(p)

def test_perfect_fit_without_errors_does_not_invent_calibrated_probability():
    rows=[{'predicate':'share_blocking','split':'CALIBRATION','duplicate_group':str(i),'calibration_fold':'FIT' if i<150 else 'EVALUATION','features':{},'correct':True} for i in range(220)]
    c=CorrectnessCalibrator('model');c.fit(rows)
    assert c.predict('share_blocking',{},'model') is None

def test_all_allowed_native_scores_required_and_renormalisation_is_not_calibration():
    r={'completion_probabilities':[{'top_probs':[{'id':32,'token':'A','prob':.6},{'id':33,'token':'B','prob':.2},{'id':34,'token':'C','prob':.1}]}]}
    value=allowed_probabilities(r)
    assert value['raw_model_probability']['YES']==pytest.approx(2/3)
    assert value['native_allowed_token_mass']==pytest.approx(.9) and value['confidence'] is None
    r['completion_probabilities'][0]['top_probs'].pop()
    with pytest.raises(ValueError,match='all allowed'):allowed_probabilities(r)

def test_released_corpus_has_no_cross_split_group_or_family_or_source_hash():
    from qwen_domain.protocol import CORPUS,read,load_inputs,digest
    manifest=read(CORPUS/'MANIFEST.json');groups={};families={};hashes=set();n=0
    for role,entry in manifest['splits'].items():
        for family in entry['families']:
            assert family not in families;families[family]=role
        for row in load_inputs(CORPUS/'MANIFEST.json',role):
            assert row['source_hash']==digest(row['text']) and row['source_hash'] not in hashes
            hashes.add(row['source_hash']);n+=1
            assert groups.setdefault(row['duplicate_group'],role)==role
        assert sha(CORPUS/entry['labels'])==entry['labels_sha256']
    assert n==5760 and len(groups)==40
