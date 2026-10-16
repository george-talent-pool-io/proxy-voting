import json,sqlite3
from pathlib import Path
import pytest
from classifier.deadlines import extract_deadline
from classifier.preprocessing import source_hash,normalise
from training.study import challenge_guard,install,fingerprint,load_study
from evaluation.quality_gates import assess,load_gates
from evaluation.error_analysis import analyse_errors

@pytest.mark.parametrize('text,status',[
 ('Voting deadline: 10 October 2025.','PASSED'),
 ('Voting closes on 20 October 2026.','OPEN'),
 ('Instructions are due on 16 October 2026; no cutoff time is given.','UNKNOWN'),
 ('Meeting date: 1 October 2025.','UNKNOWN'),
 ('Record date: 1 October 2025.','UNKNOWN'),
 ('Fiscal year ended 1 October 2025.','UNKNOWN'),
 ('No instruction deadline is specified.','UNKNOWN'),
 ('Contact the custodian for voting deadline.','UNKNOWN'),
 ('Historic archive: voting deadline 1 October 2025.','UNKNOWN'),
 ('Voting deadline 31 February 2026.','UNKNOWN'),
 ('Voting deadline 1 October 2026 and 20 October 2026.','UNKNOWN'),
 ('Instructions must arrive by 2 November 2026.','OPEN'),
 ('Voting deadline 12 October 2026. Custodian deadline 1 October 2026.','PASSED'),
 ('The fiscal year ended 31 December 2025. Vote at the upcoming AGM; instructions must arrive by 2 November 2026.','OPEN')])
def test_deterministic_deadlines(text,status):assert extract_deadline(text,'2026-10-16')['status']==status

@pytest.mark.parametrize('reference,status', [('2026-10-16T07:59:00+00:00','OPEN'),('2026-10-16T08:01:00+00:00','PASSED'),('2026-10-16','UNKNOWN')])
def test_timezone(reference,status):assert extract_deadline('Voting deadline: 16 October 2026, 17:00 Tokyo time.',reference)['status']==status

def test_naive_timestamp_refused():
 with pytest.raises(ValueError,match='timezone'):extract_deadline('Voting deadline: 16 October 2026.','2026-10-16T12:00:00')

def test_semantic_deadline_uncertainty_not_overruled():
 assert extract_deadline('Voting deadline: 1 October 2026.','2026-10-16','UNCERTAIN')['status']=='UNKNOWN'

def test_challenge_not_training():
 case=json.loads(Path('tests/fixtures/semantic.json').read_text())[0]
 for r in [{'record_id':case['id']},{'record_id':'unrelated','normalised_hash':source_hash(normalise(case['text']))}]:
  with pytest.raises(ValueError,match='never'):challenge_guard([r])
 challenge_guard([{'record_id':'legitimate','normalised_hash':source_hash('unrelated human source')}])

def test_study_immutability(db):
 from apps.api.store import connect
 with connect(db) as c:
  install(c);m={'records':[]};c.execute('INSERT INTO studies VALUES(?,?,?,?)',('laya-supervised-v1','fixed',json.dumps(m),fingerprint(m)))
  for q in ['DELETE FROM studies',"UPDATE studies SET manifest='{}'"]:
   with pytest.raises(sqlite3.IntegrityError,match='immutable'):c.execute(q)
 assert load_study(db)==m

def test_no_labels_gate_fails():
 g=assess([],{},False)
 assert not g['passed'] and g['status']=='QUALITY GATE NOT MET' and not g['automation_enabled']
 assert any('locked' in x for x in g['reasons'])

def test_proposed_gate_pass_never_activates_automation():
 d=dict(votable='YES',share_blocking=True,poa_required=True,other_restriction=True,deadline_status='OPEN')
 rows=[dict(id=str(i),group_id=str(i),true_votable='YES',true_decision=d,decision=d,eligible=True,confidence=.99) for i in range(250)]
 g=assess(rows,{'actionable_voting_recall':1.,'macro_f1':1.},True,.98)
 assert g['passed'] and not g['automation_enabled']
 # Repeated rows never satisfy independent-support requirements.
 for r in rows:r['group_id']='same-filing'
 assert not assess(rows,{'actionable_voting_recall':1.,'macro_f1':1.},True,.98)['passed']

def test_factor_error_visible_when_status_unchanged():
 truth=dict(votable='NO',share_blocking=False,poa_required=False,other_restriction=False,deadline_status='UNKNOWN');pred={**truth,'share_blocking':True}
 r=dict(id='a',true='NOT_VOTABLE',predicted='NOT_VOTABLE',correct=True,true_decision=truth,decision=pred,confidence=.5,scores={'share_blocking':{'YES':.99,'NO':.005,'UNKNOWN':.005}})
 e=analyse_errors([r]);assert e['errors'][0]['failed_fields']==['share_blocking'] and e['high_confidence_factor_errors'][0]['id']=='a'

@pytest.mark.parametrize('notice,status',[
 ('Voting deadline: 17 October 2026, 00:30 Tokyo time.','UNKNOWN'),
 ('Voting deadline: 16 October 2026, 00:30 Tokyo time.','PASSED'),
 ('Voting deadline: 17 October 2026, 17:00 Tokyo time.','OPEN')])
def test_date_only_reference_timezone_boundary(notice,status):
 assert extract_deadline(notice,'2026-10-16')['status']==status
