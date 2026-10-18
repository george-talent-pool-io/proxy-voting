"""Routing/identity contracts; fixtures do not establish model accuracy."""
import copy
import pytest
from production import cascade_policy
from training.framework import campaigns, releases


def manifest():
    return {'models':{'laya':{'manifest_sha256':'PINNED_TEST_WEIGHTS'}},
            'spec':{'mode':'LAYA_ONLY','aggregation':{'strategy':'SUPERSESSION_AWARE'},'laya_inference':'PASSAGES'},
            'sources':{'runtime.py':'PINNED_TEST_SOURCE'},'schema_sha256':'PINNED_SCHEMA'}


def test_stage_identity_independent_of_llm_but_not_specialist_runtime():
    a=manifest();b=copy.deepcopy(a);b['models']['llm']={'manifest_sha256':'OTHER'};b['spec']['mode']='LAYA_QWEN'
    assert cascade_policy.stage_identity(a)==cascade_policy.stage_identity(b)
    b['spec']['laya_inference']='WHOLE_NOTICE_WITH_PASSAGE_EVIDENCE'
    assert cascade_policy.stage_identity(a)!=cascade_policy.stage_identity(b)


def test_no_supported_operating_point_never_accepts_high_native_score():
    out=cascade_policy.assess('Notice',{},None,{'selection':None},language='en',input_type='UNSTRUCTURED_NOTICE',population='AI')
    assert not out['accept'] and out['confidence'] is None


def test_routing_and_final_output_calibration_are_distinct(monkeypatch):
    from production import qualification
    seen=[]
    def assessment(text,result,meta,cal,identity,threshold):
        seen.append((meta,identity,threshold));return {'eligible':True,'review_reasons':[],'final_decision_confidence':.995}
    monkeypatch.setattr(qualification,'assess',assessment)
    point={'identity':'STAGE_ONLY','sha256':'POINT','selection':{'threshold':.99}}
    out=cascade_policy.assess('Notice',{}, {},point,language='en',input_type='UNSTRUCTURED_NOTICE',population='CONTROLLED')
    assert out['accept'] and seen[0][1:] == ('STAGE_ONLY',.99)
    assert out['policy_sha256']=='POINT'


def test_campaign_frozen_baselines_do_not_require_fake_training_jobs():
    stage=campaigns.Stage(name='base',reuse_seed='frozen-foundation')
    assert stage.training is None and stage.reuse_job is None
    with pytest.raises(ValueError,match='one stage source'):
        campaigns.Stage(name='bad',reuse_seed='foundation',reuse_job='job')
    with pytest.raises(ValueError,match='both stage'):
        releases.ReleaseSpec(mode='LAYA_QWEN',laya_seed='a',llm_seed='b',laya_calibrator_id='cal')
