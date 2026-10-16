"""Append-only event ledger. Sender+CORP identity; never join by ISIN alone.

Arrival order is recorded but not used to resolve contradictory updates. A REPL
must identify the currently active notification with PREV; stale/unlinked updates
are quarantined. MT565 CANC is an instruction cancellation REQUEST, not event
cancellation or acceptance. Status/confirmation never imply an executed vote.
"""
import json,sqlite3,hashlib
from datetime import datetime,timezone
from hybrid.parser import parse,facts

class EventLedger:
    def __init__(self,path):
        self.path=str(path)
        with self.connect() as c:
            c.executescript('''
CREATE TABLE IF NOT EXISTS event_messages(id INTEGER PRIMARY KEY, sender TEXT NOT NULL, seme TEXT NOT NULL, corp TEXT, event_id TEXT, source_hash TEXT NOT NULL, received_at TEXT NOT NULL, state TEXT NOT NULL, previous_message_id INTEGER, payload TEXT NOT NULL, UNIQUE(sender,seme));
CREATE TRIGGER IF NOT EXISTS event_history_no_update BEFORE UPDATE ON event_messages BEGIN SELECT RAISE(ABORT,'Event history is immutable'); END;
CREATE TRIGGER IF NOT EXISTS event_history_no_delete BEFORE DELETE ON event_messages BEGIN SELECT RAISE(ABORT,'Event history is immutable'); END;
''')
    def connect(self):
        c=sqlite3.connect(self.path);c.row_factory=sqlite3.Row;return c
    def ingest(self,raw,sender,message_type=None,received_at=None):
        if not isinstance(sender,str) or not sender.strip():raise ValueError('Explicit sender namespace required')
        p=parse(raw,message_type)
        def unique(name):
            vals={f['value'] for f in facts(p,name)}
            return next(iter(vals)) if len(vals)==1 else None
        seme=unique('seme');corp=unique('corp');prev=unique('prev');fn=unique('function');mt=p['message_type']
        if not seme:raise ValueError('Unambiguous SEME required for persistent ingestion')
        eid=hashlib.sha256((sender+'\0'+corp).encode()).hexdigest() if corp else None
        state='APPLIED';prior=None;issues=[]
        with self.connect() as c:
            existing=c.execute('SELECT * FROM event_messages WHERE sender=? AND seme=?',(sender,seme)).fetchone()
            if existing:
                if existing['source_hash']!=p['source_hash']:raise ValueError('SEME collision: retain original; reject altered content')
                return dict(existing)
            linked=c.execute('SELECT * FROM event_messages WHERE sender=? AND seme=?',(sender,prev)).fetchone() if prev else None
            current=c.execute("SELECT * FROM event_messages WHERE event_id=? AND state='APPLIED' ORDER BY id",(eid,)).fetchall() if eid else []
            notifications=[r for r in current if json.loads(r['payload'])['parsed']['message_type']=='MT564']
            active=notifications[-1] if notifications else None
            if not corp or p['errors'] or mt not in {'MT564','MT565','MT566','MT567','MT568'}:issues.append('Missing identity, malformed or unsupported message')
            if fn in {'REPL','CANC'} and mt in {'MT564','MT568'}:
                if not linked or linked['event_id']!=eid or linked['state']!='APPLIED':issues.append('Unresolved lifecycle linkage')
                elif mt=='MT564' and (not active or active['id']!=linked['id']):issues.append('Replacement/cancellation references stale notification')
                else:prior=linked['id']
            if mt=='MT568' and not active:issues.append('Narrative has no known notification in this sender/CORP namespace')
            if mt=='MT564' and fn=='NEWM' and active:issues.append('Duplicate initial notification; no supersession reference')
            if mt=='MT565':state='INSTRUCTION_CANCEL_REQUEST' if fn=='CANC' else 'INSTRUCTION'
            elif mt=='MT567':state='STATUS'
            elif mt=='MT566':state='CONFIRMATION'
            if issues:state='QUARANTINED'
            payload={'parsed':p,'issues':issues,'function':fn,'previous_reference':prev}
            cur=c.execute('INSERT INTO event_messages(sender,seme,corp,event_id,source_hash,received_at,state,previous_message_id,payload) VALUES(?,?,?,?,?,?,?,?,?)',(sender,seme,corp,eid,p['source_hash'],received_at or datetime.now(timezone.utc).isoformat(),state,prior,json.dumps(payload)))
            return dict(c.execute('SELECT * FROM event_messages WHERE id=?',(cur.lastrowid,)).fetchone())
    def event(self,event_id):
        with self.connect() as c:rows=[dict(r) for r in c.execute('SELECT * FROM event_messages WHERE event_id=? ORDER BY id',(event_id,))]
        history=[];current={};cancelled=False;active_message=None
        for row in rows:
            p=json.loads(row['payload'])['parsed'];eligible=row['state']=='APPLIED'
            if eligible and p['message_type']=='MT564':
                fn=next((f['value'] for f in facts(p,'function')),None)
                if fn=='CANC':cancelled=True
                elif fn in {'NEWM','REPL'}:cancelled=False;active_message=row['id']
            for f in p['facts']:
                if f['name'] in {'sequence','seme','prev','function'}:continue
                key=(f['name'],tuple(f['path']))
                h={**f,'message_id':row['id'],'source_hash':row['source_hash'],'state':row['state'],'current':False}
                history.append(h)
                if eligible and p['message_type']=='MT564' and not cancelled:
                    # Only explicit values supersede. Omitted fields remain unresolved,
                    # not silently deleted. Provenance remains visible in history.
                    if key in current:current[key]['current']=False
                    h['current']=True;current[key]=h
                elif eligible and p['message_type']=='MT568' and f['name']=='narrative':
                    h['current']=True;current[(f['name'],row['id'],tuple(f['path']))]=h
        if cancelled:
            for h in current.values():h['current']=False
        return {'event_id':event_id,'cancelled':cancelled,'active_notification_id':active_message,'current_facts':[] if cancelled else list(current.values()),'history':history,'messages':[{**r,'payload':json.loads(r['payload'])} for r in rows],'manual_review_required':True,'policy':'Subset lifecycle policy; omitted replacement fields retained with original provenance, review required. MT568 supersession is not automatically merged.'}
