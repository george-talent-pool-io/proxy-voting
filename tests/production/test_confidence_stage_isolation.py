import copy
import json
import pytest
from production import confidence, qualification
from production.storage import digest
from tests.unit.test_learning_comparison import result


def test_calibration_does_not_transfer_from_specialist_to_llm(tmp_path):
    f={'prediction':'YES','evidence_mode':'QUOTE','input_type':'UNSTRUCTURED_NOTICE',
       'language':'en','supersession_cue':False,'source':'LAYA_FROZEN_A'}
    rows=[{'id':fold+str(i),'role':'CALIBRATION','fold':fold,'group':fold+str(i),
           'predicate':'share_blocking','features':f,'correct':True,'origin':'AI_AUTHORED'}
          for fold,n in [('FIT',120),('EVALUATION',60)] for i in range(n)]
    cal=confidence.fit(rows,identity='RELEASE',population='AI',output=tmp_path/'cal.json')
    feature={'features':dict(f),'force_review':False}
    assert confidence.predict(cal,'share_blocking',feature,identity='RELEASE',population='AI') is not None
    feature['features']['source']='LOCAL_LLM_B'
    assert confidence.predict(cal,'share_blocking',feature,identity='RELEASE',population='AI') is None
    old=copy.deepcopy(cal);old['version']='customer-correctness-v3'
    old['sha256']=digest({k:v for k,v in old.items() if k!='sha256'})
    (tmp_path/'old.json').write_text(json.dumps(old))
    with pytest.raises(ValueError):confidence.load(tmp_path/'old.json','RELEASE')


def test_final_decision_calibration_separates_escalated_and_specialist_results():
    r=result();r['architecture']='CASCADE';r['llm']={'invoked':False}
    meta={'language':'en','input_type':'UNSTRUCTURED_NOTICE'}
    before=qualification.decision_feature('Notice',r,meta)
    r['llm']['invoked']=True
    after=qualification.decision_feature('Notice',r,meta)
    assert confidence.stratum(before['features'])!=confidence.stratum(after['features'])
    assert after['features']['source'].endswith(':LLM_INVOKED')
