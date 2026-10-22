import copy
import stat
import pytest
from production import monitoring, qualification
from semantic_pipeline.schema import PREDICATES


def decision():
    return {'review_required':False,'review_reasons':[],'automation_enabled':True,'qualification_id':'q'}


def test_audit_sampling_is_reproducible_nontrivial_and_has_no_confidence_input():
    values=[monitoring.select(str(i),.02,key=b'x'*32) for i in range(10000)]
    assert 130 < sum(v['selected'] for v in values) < 270
    assert monitoring.select('7',.02,key=b'x'*32)==values[7]
    assert monitoring.select('7',.02,key=b'y'*32)!=values[7]
    for rate in (0,.001,1):
        with pytest.raises(ValueError):monitoring.select('x',rate,key=b'x'*32)


def test_only_accepted_and_authorised_decisions_are_sampled():
    for d in ({**decision(),'review_required':True},{**decision(),'automation_enabled':False}):
        assert 'audit_selection' not in monitoring.apply(d,'x',.5,key=b'x'*32)
    identity=next(str(i) for i in range(100) if monitoring.select(str(i),.5,key=b'x'*32)['selected'])
    d=monitoring.apply(decision(),identity,.5,key=b'x'*32)
    assert d['review_required'] and d['audit_selection']['pre_audit_eligible']
    assert d['review_reasons']==['RANDOM_ACCEPTED_DECISION_AUDIT']


def test_key_survives_restart_and_is_private(tmp_path,monkeypatch):
    monkeypatch.setattr(monitoring.jobs,'WORKSPACE',tmp_path)
    key=monitoring.installation_key()
    assert monitoring.installation_key()==key and len(key)==32
    assert stat.S_IMODE((tmp_path/'audit-selection.key').stat().st_mode)==0o600
    (tmp_path/'audit-selection.key').write_bytes(b'broken')
    with pytest.raises(ValueError,match='Invalid audit'):monitoring.installation_key()


def test_random_audit_wrong_decision_still_suspends_and_time_elapsing_is_not_model_error():
    target={k:'VOTABLE' if k=='votability' else 'NO' for k in PREDICATES}
    source={'predicates':{k:{'value':v} for k,v in target.items()},'deadline':{'status':'OPEN'},
            'decision':{'classification':'VOTABLE'},'evaluation_time':'2026-10-22T12:00:00+00:00'}
    prior={'decision':{**decision(),'review_required':True,'audit_selection':{'pre_audit_eligible':True}}}
    # Correct at inference, deadline passed when reviewed later.
    assert monitoring.verified_errors(prior,source,target,reference='2026-11-22T12:00:00+00:00',
        expected_deadline='PASSED',expected_final='DEADLINE_PASSED')==[]
    assert monitoring.verified_errors(prior,source,target,reference=source['evaluation_time'],
        expected_deadline='PASSED',expected_final='DEADLINE_PASSED')==['deadline_status','final_status']
    source['predicates']['share_blocking']['value']='YES'
    assert monitoring.verified_errors(prior,source,target,reference=None)==['share_blocking']
    prior['decision'].pop('audit_selection')
    assert monitoring.verified_errors(prior,source,target,reference=None)==[]


def test_audit_rate_is_part_of_frozen_qualification_policy():
    assert qualification.Policy().random_audit_rate==.02
    with pytest.raises(ValueError):qualification.Policy(random_audit_rate=0)
