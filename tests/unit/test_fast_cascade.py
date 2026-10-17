"""Routing/software contracts, not substituted model-quality measurements."""
import copy,pytest
from dataclasses import asdict
from semantic_pipeline.schema import PREDICATES
from semantic_pipeline.evidence import verify_evidence
from fast_cascade.routing import Policy,assess,reconcile
from fast_cascade.pipeline import Pipeline,confidence_features
from fast_cascade.evaluation import transition,oracles,summary
from fast_cascade.protocol import digest

TEXT='A current ballot is open to investors. No transfer immobilisation applies.'
def pred(value='NO',score=.999,evidence=True):
    scores={'YES':(1-score)/2,'NO':(1-score)/2,'UNKNOWN':(1-score)/2};scores[value if value in scores else {'VOTABLE':'YES','NOT_VOTABLE':'NO','UNCERTAIN':'UNKNOWN'}[value]]=score
    return {'value':value,'scores':scores,'confidence':score,'margin':score-(1-score)/2,'source':'CONTRACT_DOUBLE','evidence':[verify_evidence(TEXT,TEXT)] if evidence else []}
def laya():
    return {'input_hash':digest(TEXT),'predicates':{k:pred('VOTABLE' if k=='votability' else 'NO') for k in PREDICATES},'latency_ms':1.}
class Qwen:
    def __init__(self,p=None):self.calls=[];self.p=p or pred('YES')
    def constrained(self,text,requested,**kw):
        self.calls.append(('gear2',list(requested)));return {'predicates':{k:copy.deepcopy(self.p) for k in requested},'latency_ms':2.,'native_model_calls':len(requested)}
    def full(self,*args,**kwargs):self.calls.append(('full',None));return {'valid':False,'invoked':True,'error':'Contract schema failure','latency_ms':3.}

def test_gear1_supported_results_do_not_call_either_qwen():
    q=Qwen();r=Pipeline(Policy(),qwen=q).analyse(TEXT,precomputed_laya=laya())
    assert q.calls==[] and r['gear2'] is None and r['full_qwen'] is None
    assert r['manual_review_required'] and not r['automation_enabled']
    assert all(p['confidence'] is None for p in r['confidence'].values())

def test_gear2_only_receives_unresolved_predicate_and_can_stop():
    a=laya();a['predicates']['share_blocking']=pred('UNKNOWN');q=Qwen()
    r=Pipeline(Policy(),qwen=q).analyse(TEXT,precomputed_laya=a)
    assert q.calls==[('gear2',['share_blocking'])]
    assert r['full_qwen'] is None and r['predicates']['share_blocking']['value']=='YES'
    assert a['predicates']['share_blocking']['value']=='UNKNOWN' # earlier stage untouched

def test_gear2_unknown_calls_full_and_schema_failure_forces_review():
    a=laya();a['predicates']['share_blocking']=pred('UNKNOWN');q=Qwen(pred('UNKNOWN'))
    r=Pipeline(Policy(),qwen=q).analyse(TEXT,precomputed_laya=a)
    assert [c[0] for c in q.calls]==['gear2','full']
    assert r['semantic_review_required'] and 'FULL_QWEN_SCHEMA_FAILURE' in r['reconciliation']['conflicts']

def test_two_gear_skips_constrained():
    a=laya();a['predicates']['share_blocking']=pred('UNKNOWN');q=Qwen()
    Pipeline(Policy(gear2=False),qwen=q).analyse(TEXT,precomputed_laya=a)
    assert q.calls==[('full',None)]

def test_known_disagreement_has_no_automatic_model_winner():
    earlier=pred('NO');later=pred('YES')
    result,conflicts,trace=reconcile(earlier,later,'share_blocking',right_accepted=True)
    assert result['value']=='UNKNOWN' and conflicts and trace['rule']=='DISAGREEMENT_REVIEW'
    assert earlier['value']=='NO'

@pytest.mark.parametrize('support,win,damage,accepted',[(9,1.,0,False),(10,.89,0,False),(10,.9,1,False),(10,.9,0,True)])
def test_validation_preference_has_explicit_support_and_damage_gate(support,win,damage,accepted):
    r,c,t=reconcile(pred('NO'),pred('YES'),'share_blocking',right_accepted=True,preferences={'share_blocking':{'prefer':'LATER','support':support,'win_rate':win,'critical_damage':damage}})
    assert (r['value']=='YES')==accepted

@pytest.mark.parametrize('score,margin,passage_min,ok',[(.999,.998,.999,True),(.999,.998,.3,False)])
def test_absence_acceptance_uses_weakest_passage_not_max(score,margin,passage_min,ok):
    p={**pred('NO',score,evidence=False),'aggregation_reason':'DOCUMENT_ABSENCE_NOT_EXPLICIT_NEGATION','minimum_passage_no_score':passage_min,'minimum_passage_no_margin':passage_min}
    r=assess(TEXT,'share_blocking',p,Policy(allow_absence=True))
    assert r['accepted_for_research']==ok

@pytest.mark.parametrize('field,value',[('conflict',True),('truncated',True)])
def test_strong_score_cannot_bypass_conflict_or_truncation(field,value):
    p={**pred(),field:value};assert not assess(TEXT,'share_blocking',p,Policy())['accepted_for_research']

def test_positive_without_evidence_cannot_have_calibrated_confidence():
    r=confidence_features(TEXT,'share_blocking',pred('YES',evidence=False),stage='CONSTRAINED_QWEN')
    assert r['force_review'] and r['confidence'] is None

def test_raw_probability_not_calibrated_and_language_forces_review():
    p={**pred('YES'),'raw_model_probability':{'YES':.999,'NO':.0005,'UNKNOWN':.0005}}
    r=assess(TEXT,'share_blocking',p,Policy(),gear=2,language='nl')
    assert not r['accepted_for_research'] and not r['signals']['raw_scores_are_calibrated']

def test_batch_source_mismatch_rejected():
    with pytest.raises(ValueError,match='source hash'):Pipeline().analyse('Different source',precomputed_laya=laya())

def test_replay_requires_real_precomputed_later_outputs():
    a=laya();a['predicates']['share_blocking']=pred('UNKNOWN')
    with pytest.raises(ValueError,match='counterfactual Gear 2'):Pipeline().analyse(TEXT,precomputed_laya=a,replay=True)

def test_transition_damage_and_repairs_are_separate():
    assert transition(['YES','NO','YES','NO'],['NO','NO','YES','YES'],['YES','YES','YES','YES'])=={'earlier_wrong_later_correct':1,'earlier_correct_later_wrong':1,'both_correct':1,'both_wrong':1}

def test_partial_truth_denominator_never_fills_missing_labels():
    result={'predicates':{'share_blocking':{'value':'YES'}},'decision':{'classification':'VOTABLE_WITH_RESTRICTION'},'latency_ms':1.}
    m=summary([{'id':'x','expected':{'share_blocking':'YES'}}],[{'id':'x','result':result}])
    assert m['assertions']==m['correct_assertions']==1 and 'classification' not in m['fields'] and m['fully_labelled_semantic_cases']==0

def test_protected_truth_refused_before_selection(tmp_path,monkeypatch):
    import fast_cascade.study as s
    monkeypatch.setattr(s,'STUDY',tmp_path)
    with pytest.raises(ValueError,match='scoring-only'):s.label_cases('SYNTHETIC_FROZEN_TEST')
    with pytest.raises(ValueError,match='Frozen challenge'):s.label_cases('CHALLENGE')

def test_calibration_rejects_wrong_role_and_shared_groups():
    from qwen_domain.confidence import CorrectnessCalibrator
    cal=CorrectnessCalibrator('identity')
    with pytest.raises(ValueError,match='only use CALIBRATION'):cal.fit([{'split':'VALIDATION'}])
    with pytest.raises(ValueError,match='leakage'):cal.fit([{'split':'CALIBRATION','calibration_fold':f,'duplicate_group':'g'} for f in ['FIT','EVALUATION']])

def test_calibrator_identity_persistence_and_held_out_metrics(tmp_path):
    from qwen_domain.confidence import CorrectnessCalibrator
    records=[{'predicate':'share_blocking','split':'CALIBRATION','calibration_fold':fold,'duplicate_group':fold,'features':{'stage':'LAYA','margin':.7},'correct':i%5!=0} for fold,n in [('FIT',100),('EVALUATION',60)] for i in range(n)]
    c=CorrectnessCalibrator('model');report=c.fit(records)
    assert report['share_blocking']['evaluation']['n']==60
    path=tmp_path/'cal.joblib';c.save(path);loaded=CorrectnessCalibrator.load(path,'model')
    assert loaded.predict('share_blocking',{'stage':'LAYA','margin':.7},'model')==pytest.approx(.8,abs=.01)
    with pytest.raises(ValueError,match='identity'):CorrectnessCalibrator.load(path,'wrong')

def test_validation_selector_replays_identical_cases_without_frozen_truth(tmp_path,monkeypatch):
    import fast_cascade.study as s
    from fast_cascade.protocol import append
    cases=[{'id':str(i),'text':TEXT,'language':'en','expected':{**{k:'VOTABLE' if k=='votability' else 'NO' for k in PREDICATES},'deadline_status':'UNKNOWN','classification':'UNCERTAIN_MANUAL_REVIEW'}} for i in range(10)]
    monkeypatch.setattr(s,'STUDY',tmp_path);monkeypatch.setattr(s,'inputs',lambda split:cases)
    def labels(split):
        assert split=='VALIDATION';return cases
    monkeypatch.setattr(s,'label_cases',labels)
    for c in cases:
        a=laya();g={'predicates':{k:{**p,'latency_ms':2.} for k,p in a['predicates'].items()},'latency_ms':2.}
        f={**s.semantic_reference(c,a,'REFERENCE'),'raw':{'valid':False,'latency_ms':0.}}
        for name,result in [('LAYA',a),('GEAR2',g),('FULL',f)]:s.save('VALIDATION',name,c,result)
    r=s.select()
    assert len(r['policies'])==6 and r['reference']['assertions']==110
    assert r['model_identity'] and (tmp_path/'SELECTION.json').exists()

def test_calibration_folds_reconstructed_from_input_groups_without_answers():
    from fast_cascade.study import calibration_metadata
    data=[{'id':f'{g}-{i}','duplicate_group':g,'text':'Input only'} for g,n in [('a',240),('b',240),('c',120),('d',60)] for i in range(n)]
    out=calibration_metadata(data)
    groups={g:{r['calibration_fold'] for r in out if r['duplicate_group']==g} for g in ['a','b','c','d']}
    assert all(len(f)==1 for f in groups.values()) and {r['calibration_fold'] for r in out}=={'FIT','EVALUATION'}
    assert not any('expected' in r for r in out)

@pytest.mark.parametrize('words,value,expected',[
 ('Instructed holdings remain unavailable for transfer through the close of proceedings.','YES','YES'),
 ('The position is encumbered from ballot lodgement until conclusion.','YES','YES'),
 ('There is no share blocking for this event.','NO','NO'),
 ('Historically the position was encumbered for a ballot.','YES','UNKNOWN'),
])
def test_native_affirmative_evidence_is_not_vetoed_by_a_keyword_whitelist(words,value,expected):
    from fast_cascade.aggregation import aggregate
    n={'value':value,'scores':{k:1. if k==value else 0. for k in ['YES','NO','UNKNOWN']},'confidence':1.,'margin':1.,'truncated':False}
    result=aggregate(words,'share_blocking',[n])
    assert result['value']==expected
    assert result['passage_states'][0]['native_value']==value


def test_native_positive_aggregation_preserves_supersession_and_conflict():
    from fast_cascade.aggregation import aggregate
    def n(v):return {'value':v,'scores':{k:1. if k==v else 0. for k in ['YES','NO','UNKNOWN']},'confidence':1.,'margin':1.,'truncated':False}
    text='Voting positions are blocked.\n\nFinal terms: no share blocking applies.'
    result=aggregate(text,'share_blocking',[n('YES'),n('NO')]);assert result['value']=='NO' and not result['conflict']
    text='Voting positions are blocked.\n\nNo share blocking applies.'
    result=aggregate(text,'share_blocking',[n('YES'),n('NO')]);assert result['value']=='UNKNOWN' and result['conflict']
