import copy
import json
import pytest
from production import qualification as q, confidence
from semantic_pipeline.schema import PREDICATES


def controlled_records(n, groups=None):
    # Mathematical acceptance fixture, not model predictions or expert labels.
    truth = {k: 'VOTABLE' if k=='votability' else 'YES' for k in PREDICATES}
    return [{'id':str(i), 'group':str(i if groups is None else i%groups), 'truth':dict(truth),
             'prediction':dict(truth), 'accepted': True, 'exact_correct': True} for i in range(n)]


def test_small_perfect_sample_does_not_qualify_and_duplicate_groups_do_not_inflate_support():
    a = q.statistics(controlled_records(4), {})
    b = q.statistics(controlled_records(1000, groups=4), {})
    assert not a['statistical_gate_passed'] and not b['statistical_gate_passed']
    assert a['auto_precision_lower_bound'] == b['auto_precision_lower_bound']
    assert b['independent_groups'] == 4


def test_bound_and_critical_failure_gates():
    rows = controlled_records(1000)
    r = q.statistics(rows, {})
    assert r['statistical_gate_passed'] and r['auto_precision_lower_bound'] > .99
    for row in rows[:100]: row['prediction']['share_blocking']='NO'; row['exact_correct']=False
    r = q.statistics(rows, {})
    assert not r['statistical_gate_passed']
    assert r['critical']['share_blocking']['false_negatives'] == 100
    assert r['wrong_auto_processed'] == 100


def test_review_percentage_is_measured_target_not_promise():
    rows = controlled_records(1000)
    for r in rows[:200]: r['accepted']=False
    m = q.statistics(rows, {})
    assert not m['statistical_gate_passed'] and 'REVIEW_RATE_TARGET_NOT_MET' in m['reasons']
    assert m['review_rate'] == pytest.approx(.2)


def test_review_budget_includes_random_audits_of_accepted_decisions():
    rows=controlled_records(1000)
    for r in rows[:90]:r['accepted']=False
    m=q.statistics(rows,{})
    assert m['review_rate']==pytest.approx(.09)
    assert m['expected_total_review_rate_including_audits']==pytest.approx(.1082)
    assert 'REVIEW_RATE_TARGET_NOT_MET' in m['reasons']


def calibration_rows():
    values=[]
    for fold,n in [('FIT',500),('EVALUATION',200)]:
        for i in range(n):
            values.append({'id':fold+str(i), 'role':'CALIBRATION','fold':fold,'group':fold+str(i),
                           'predicate':'share_blocking','features':{'language':'en','signal':i%2},
                           'correct':i%10 < (8 if i%2 else 5),'origin':'AI_AUTHORED'})
    return values


def test_calibration_separate_folds_persistence_and_population_binding(tmp_path):
    rows=calibration_rows(); path=tmp_path/'calibrator.json'
    m=confidence.fit(rows,identity='MODEL_A',population='AI_FIXTURE',output=path)
    loaded=confidence.load(path,'MODEL_A')
    assert loaded==m and loaded['models']['share_blocking']
    f={'features':{'language':'en','signal':1},'force_review':False}
    p=confidence.predict(loaded,'share_blocking',f,identity='MODEL_A',population='AI_FIXTURE')
    assert 0<p<1
    assert confidence.predict(loaded,'share_blocking',{**f,'force_review':True},identity='MODEL_A',population='AI_FIXTURE') is None
    with pytest.raises(ValueError): confidence.predict(loaded,'share_blocking',f,identity='MODEL_A',population='OTHER')
    rows[-1]['group']=rows[0]['group']
    with pytest.raises(ValueError,match='leakage'): confidence.fit(rows,identity='X',population='X',output=tmp_path/'bad.json')
    raw=json.loads(path.read_text());raw['identity']='MODEL_B';path.write_text(json.dumps(raw))
    with pytest.raises(ValueError): confidence.load(path,'MODEL_B')


def test_insufficient_calibration_never_invents_number(tmp_path):
    m=confidence.fit(calibration_rows()[:20],identity='M',population='AI',output=tmp_path/'tiny.json')
    assert not m['models'] and m['reports']['share_blocking']['status']=='INSUFFICIENT_SUPPORT'
