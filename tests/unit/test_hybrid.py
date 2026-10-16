import sqlite3
import pytest
from hybrid.rules import decide,RESTRICTIONS
from hybrid.events import EventLedger
from hybrid.semantics import passages,aggregate
from hybrid.pipeline import analyse
from hybrid.fallback import DisabledFallback

def clean():return {'votable':'YES','deadline_status':'OPEN',**dict.fromkeys(RESTRICTIONS,'NO')}
@pytest.mark.parametrize('key',RESTRICTIONS)
def test_restriction_rules(key):
    f=clean();f[key]='YES';assert decide(f)['classification']=='VOTABLE_WITH_RESTRICTION'
@pytest.mark.parametrize('overrides,expected',[({'conflict':True},'UNCERTAIN_MANUAL_REVIEW'),({'cancelled':True},'NOT_VOTABLE'),({'votable':'NO'},'NOT_VOTABLE'),({'votable':'UNCERTAIN'},'UNCERTAIN_MANUAL_REVIEW'),({'deadline_status':'PASSED'},'DEADLINE_PASSED'),({'deadline_status':'UNKNOWN'},'UNCERTAIN_MANUAL_REVIEW'),({},'VOTABLE')])
def test_rule_table(overrides,expected):
    out=decide({**clean(),**overrides});assert out['classification']==expected;assert out['manual_review_required'];assert not out['automation_enabled']
def test_unknown_restriction_review():assert decide({'votable':'YES','deadline_status':'OPEN'})['classification']=='UNCERTAIN_MANUAL_REVIEW'
def test_fallback_disabled():assert DisabledFallback().analyse('private',{},['poa_required'])['external_calls']==0

def msg(seme='ONE',fn='NEWM',prev=None,deadline='20261015170000,000/00',mt='564',corp='EVENT'):
    return f'{{2:I{mt}TEST}}{{4:\n:16R:GENL\n:20C::SEME//{seme}\n:20C::CORP//{corp}\n:23G:{fn}\n:22F::CAEV//MEET\n'+(f':16R:LINK\n:20C::PREV//{prev}\n:16S:LINK\n' if prev else '')+':16S:GENL\n:16R:CAOPTN\n:98E::RDDT//'+deadline+'\n:16S:CAOPTN\n-}'

def test_replacement_cancellation_history_and_restart(tmp_path):
    path=tmp_path/'events.sqlite';l=EventLedger(path)
    a=l.ingest(msg(),'BANK');b=l.ingest(msg('TWO','REPL','ONE','20261018170000,000/00'),'BANK')
    s=EventLedger(path).event(a['event_id']);dates=[h for h in s['history'] if h['name']=='rddt']
    assert [h['current'] for h in dates]==[False,True]
    assert dates[0]['value']['iso'].startswith('2026-10-15');assert dates[1]['message_id']==b['id']
    l.ingest(msg('THREE','CANC','TWO'),'BANK');s=l.event(a['event_id']);assert s['cancelled'];assert not s['current_facts'];assert len(s['messages'])==3
    with l.connect() as c:
        with pytest.raises(sqlite3.IntegrityError):c.execute('DELETE FROM event_messages')

def test_instruction_cancel_does_not_cancel_event(tmp_path):
    l=EventLedger(tmp_path/'x.sqlite');a=l.ingest(msg(),'BANK');l.ingest(msg('INSTR','CANC','ONE',mt='565'),'BANK');assert not l.event(a['event_id'])['cancelled']
def test_stale_replacement_quarantine(tmp_path):
    l=EventLedger(tmp_path/'x.sqlite');l.ingest(msg(),'BANK');l.ingest(msg('TWO','REPL','ONE'),'BANK');assert l.ingest(msg('THREE','REPL','ONE'),'BANK')['state']=='QUARANTINED'
def test_link_mt564_mt568(tmp_path):
    l=EventLedger(tmp_path/'x.sqlite');a=l.ingest(msg(),'BANK');b=l.ingest(msg('NARR','NEWM',mt='568'),'BANK');assert a['event_id']==b['event_id'];assert b['state']=='APPLIED'
def test_unlinked_mt568_quarantine(tmp_path):assert EventLedger(tmp_path/'x').ingest(msg(mt='568'),'BANK')['state']=='QUARANTINED'
def test_sender_namespace_and_collision(tmp_path):
    l=EventLedger(tmp_path/'x');a=l.ingest(msg(),'A');b=l.ingest(msg(),'B');assert a['event_id']!=b['event_id']
    assert l.ingest(msg(),'A')['id']==a['id']
    with pytest.raises(ValueError):l.ingest(msg(deadline='20261018170000,000/00'),'A')
def test_chunks_preserve_late_restriction():
    text=('Long unrelated sentence. '*200)+'Shares will be blocked.'
    chunks=list(passages(text));assert chunks[-1]['text']=='Shares will be blocked.'
    assert all(text[p['start']:p['end']]==p['text'] for p in chunks)
    assert max(len(p['text']) for p in passages('z'*5000))<=900

def test_aggregation_does_not_average_positive_away():
    no={'value':'NO','confidence':.99,'scores':{'NO':.99},'evidence':None};yes={'value':'YES','confidence':.8,'scores':{'YES':.8},'evidence':{'text':'blocking'}}
    assert aggregate([no]*30+[yes],'any_positive')['value']=='YES'
    assert aggregate([no,yes],'conflict_abstain')['value']=='UNKNOWN'
    assert aggregate([no,yes],'max_confidence')['value']=='NO'

def test_no_laya_without_narrative():
    class Crash:
        def analyse(self,*args):raise AssertionError('Structured fields sent to ML')
    assert not analyse(msg(),Crash())['metrics']['laya_executed']

def test_confirmation_does_not_imply_executed_vote(tmp_path):
    l=EventLedger(tmp_path/'x');a=l.ingest(msg(),'BANK');r=l.ingest(msg('CONFIRM',mt='566'),'BANK')
    assert r['state']=='CONFIRMATION';assert not l.event(a['event_id'])['cancelled']

def test_validated_linked_corpus_chain(tmp_path):
    import json
    from pathlib import Path
    l=EventLedger(tmp_path/'x');first=None
    for step in range(4):
        r=json.loads(Path(f'data/iso15022_corpus/standards_derived/chain-000-{step}.json').read_text())
        item=l.ingest(r['raw'],'SYNTHETIC',r['message_type']);first=first or item
        assert item['state']=='APPLIED'
    assert l.event(first['event_id'])['cancelled']

def test_unknown_event_never_infers_negative_meeting():
    from hybrid.service import inspect
    r=inspect(msg().replace('CAEV//MEET','CAEV//ZZZZ'))
    assert r['structured_facts']['meeting_event']=='UNKNOWN'
    assert r['parsed']['facts'];assert r['decision']['manual_review_required']
