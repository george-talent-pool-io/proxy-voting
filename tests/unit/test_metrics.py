import copy
import pytest
from evaluation.metrics import compute_metrics,automation_curve,select_threshold,wilson_lower
from evaluation.error_analysis import analyse_errors

@pytest.fixture
def samples():
    from tests.conftest import ContractAgent
    from classifier.laya_classifier import LayaClassifier
    r=LayaClassifier(agent=ContractAgent()).classify('notice').model_dump()
    row={'id':'one','true':'VOTABLE','predicted':'VOTABLE','correct':True,'confidence':.99,'eligible':True,'action':'MANUAL_REVIEW',
        'true_votable':'YES','predicted_votable':'YES','true_decision':copy.deepcopy(r['decision']),'decision':r['decision'],'scores':r['scores'],'text':'shares may vote at a meeting',
        'country':'UNKNOWN','market':'UNKNOWN','language':'en','event_type':'AGM','group_id':'1'}
    bad=copy.deepcopy(row);bad.update(id='two',predicted='NOT_VOTABLE',correct=False,predicted_votable='NO');bad['decision']['votable']='NO'
    return [row,bad]

def test_empty():assert compute_metrics([])['accuracy'] is None

def test_hand_calculated(samples):
    m=compute_metrics(samples)
    assert m['accuracy']==.5 and m['balanced_accuracy']==.5
    assert m['per_category']['VOTABLE']['precision']==1
    assert m['per_category']['VOTABLE']['recall']==.5
    assert m['per_category']['VOTABLE']['f1-score']==pytest.approx(2/3)
    assert m['actionable_voting_recall']==.5
    assert sum(sum(row) for row in m['confusion_matrix'])==2
    assert m['false_negatives']==['two']
    assert m['auto_processed']==0 and m['manual_review']==2
    assert m['wrong_auto_processed']==0

def test_curve(samples):
    curve=automation_curve(samples)
    at=next(x for x in curve if x['threshold']==.98)
    assert at['auto_processed']==2 and at['wrong_auto_processed']==1 and at['coverage']==1 and at['accuracy']==.5
    assert curve[-1]['accuracy'] is None

def test_no_marketing_threshold(samples):assert select_threshold(samples) is None

def test_wilson_support(samples):
    assert wilson_lower(10,10)<.98
    assert wilson_lower(200,200)>.98
    assert select_threshold([samples[0]]*200) is None # duplicate support is not independent evidence
    independent=[{**samples[0],'id':str(i),'group_id':str(i)} for i in range(200)]
    assert select_threshold(independent)['coverage']==1

def test_errors(samples):
    e=analyse_errors(samples)
    assert e['high_confidence_errors']==['two']
    assert e['groups']['language'][0]['error_rate']==.5


def test_factor_error_with_same_status_is_wrong_auto(samples):
    row=copy.deepcopy(samples[0]);row['action']='AUTO_CLASSIFY'
    row['true_decision']['deadline_status']='UNKNOWN' # derived status stays VOTABLE
    assert row['true']==row['predicted']
    m=compute_metrics([row]);assert m['accuracy']==1 and m['all_factor_exact_match']==0
    assert m['wrong_auto_processed']==1
    assert next(x for x in m['curve'] if x['threshold']==.98)['wrong_auto_processed']==1

def test_curve_sweep_matches_threshold_definition():
    import random
    rng=random.Random(42)
    rows=[dict(id=str(i),group_id=str(i//3),correct=rng.choice([True,False]),eligible=rng.choice([True,False]),confidence=rng.choice([0,.4,.7,.98,1])) for i in range(50)]
    for point in automation_curve(rows):
        selected=[r for r in rows if r['eligible'] and r['confidence']>=point['threshold']]
        groups={r['group_id'] for r in selected}
        group_correct=sum(all(r['correct'] for r in selected if r['group_id']==g) for g in groups)
        assert point['auto_processed']==len(selected)
        assert point['wrong_auto_processed']==sum(not r['correct'] for r in selected)
        assert point['precision_lower_95']==wilson_lower(group_correct,len(groups))
