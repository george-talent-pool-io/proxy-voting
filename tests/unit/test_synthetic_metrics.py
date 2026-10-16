import copy
import json
from pathlib import Path
import pytest
from training.synthetic_protocol import supplied_status,decision,rows,field_metrics
from training.learning_curve import nested_order
from classifier.schema import Decision

@pytest.mark.parametrize('flags,status',[
 ({'share_blocking':True,'poa_required':True},'SHARE_BLOCKING'),
 ({'poa_required':True,'other_restriction':True},'POA_REQUIRED'),
 ({'other_restriction':True},'VOTABLE_WITH_RESTRICTION'),
 ({'share_blocking':None},'UNCERTAIN_MANUAL_REVIEW'),
 ({'votable':'NO','share_blocking':True},'NOT_VOTABLE'),
 ({'deadline_status':'PASSED','share_blocking':True},'DEADLINE_PASSED')])
def test_supplied_customer_policy_is_separate(flags,status):
 d=Decision(**{'votable':'YES',**flags});assert supplied_status(d.model_dump())==status

def test_supplied_mapping_matches_train_validation_only():
 data=rows('train')+rows('validation')
 assert all(supplied_status(decision(r).model_dump())==r['expected_customer_status'] for r in data)
 # Preserve authored challenge's distinct multi-restriction policy.
 assert Decision(votable='YES',share_blocking=True,poa_required=True).status().value=='VOTABLE_WITH_RESTRICTION'

def test_nested_training_subsets():
 data=rows('train');order=nested_order(data)
 assert {r['id'] for r in order}=={r['id'] for r in data}
 assert nested_order(list(reversed(data)))==order
 for n in [50,100,200]:assert {r['id'] for r in order[:n]}<={r['id'] for r in order[:n+50]}
 assert {r['id'] for r in order}.isdisjoint({r['id'] for r in rows('validation')})

def test_metrics_manual_counts():
 data=rows('validation')[:2];pred=[]
 for r in data:
  d=decision(r).model_dump();native={k:('UNKNOWN' if v is None else 'YES' if v is True else 'NO' if v is False else v) for k,v in d.items() if k!='manual_review_required'}
  scores={k:{v:1.} for k,v in native.items()}
  # Native scores with several possible options, as produced by a calibrated classifier.
  for k,v in native.items():
   options=['YES','NO','UNCERTAIN'] if k=='votable' else ['OPEN','PASSED','UNKNOWN'] if k=='deadline_status' else ['YES','NO','UNKNOWN'];scores[k]={x:1. if x==v else 0. for x in options}
  pred.append({'id':r['id'],'result':{'decision':d,'classification':Decision.model_validate(d).status().value,'scores':scores,'raw_answers':{},'confidence':1.,'processing_time_ms':1}})
 m=field_metrics(data,pred);assert m['all_field_exact_match_accuracy']==1. and m['customer_status_accuracy']==1.
 changed=copy.deepcopy(pred);v=changed[0]['result']['decision']['votable'];changed[0]['result']['decision']['votable']='NO' if v=='YES' else 'YES'
 m=field_metrics(data,changed);assert m['all_field_exact_match_accuracy']==.5 and m['fields']['votable']['accuracy']==.5
 assert len(m['failures'])==1
 with pytest.raises(ValueError,match='IDs'):field_metrics(data,pred[:1])
