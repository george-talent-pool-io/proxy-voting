"""Operational receipts are append-only; source tables remain owned by learning."""
import hashlib
import json
import uuid
from apps.api import store

TABLES = ('client_audit', 'client_imports', 'client_metadata', 'client_review_identity',
          'client_freezes', 'client_decisions', 'client_qualification_plans', 'client_qualifications', 'client_promotions', 'client_suspensions')


def initialise():
    store.initialise()
    from training.framework import events
    events.initialise()
    with store.connect() as c:
        c.executescript('''
        CREATE TABLE IF NOT EXISTS client_audit(id INTEGER PRIMARY KEY AUTOINCREMENT,created_at TEXT NOT NULL,actor TEXT NOT NULL,action TEXT NOT NULL,payload TEXT NOT NULL,previous_hash TEXT NOT NULL,entry_hash TEXT NOT NULL);
        CREATE TABLE IF NOT EXISTS client_imports(id TEXT PRIMARY KEY,created_at TEXT NOT NULL,actor TEXT NOT NULL,request_hash TEXT NOT NULL,payload TEXT NOT NULL);
        CREATE TABLE IF NOT EXISTS client_metadata(event_id TEXT PRIMARY KEY,language TEXT NOT NULL,country TEXT NOT NULL,market TEXT NOT NULL,population TEXT NOT NULL);
        CREATE TABLE IF NOT EXISTS client_review_identity(review_id INTEGER PRIMARY KEY,actor TEXT NOT NULL,expert INTEGER NOT NULL,blind INTEGER NOT NULL,source_kind TEXT NOT NULL,evaluation_time TEXT);
        CREATE TABLE IF NOT EXISTS client_freezes(event_id TEXT PRIMARY KEY,snapshot_hash TEXT NOT NULL,review_id INTEGER NOT NULL,dataset_id TEXT NOT NULL);
        CREATE TABLE IF NOT EXISTS client_decisions(id TEXT PRIMARY KEY,created_at TEXT NOT NULL,event_id TEXT NOT NULL,execution_id TEXT NOT NULL,payload TEXT NOT NULL);
        CREATE TABLE IF NOT EXISTS client_qualifications(id TEXT PRIMARY KEY,created_at TEXT NOT NULL,payload TEXT NOT NULL);
        CREATE TABLE IF NOT EXISTS client_qualification_plans(id TEXT PRIMARY KEY,payload TEXT NOT NULL);
        CREATE TABLE IF NOT EXISTS client_promotions(id INTEGER PRIMARY KEY AUTOINCREMENT,created_at TEXT NOT NULL,qualification_id TEXT NOT NULL,previous_id INTEGER,payload TEXT NOT NULL);
        CREATE TABLE IF NOT EXISTS client_suspensions(id INTEGER PRIMARY KEY AUTOINCREMENT,created_at TEXT NOT NULL,qualification_id TEXT NOT NULL,review_id INTEGER NOT NULL,payload TEXT NOT NULL);
        ''')
        for name in TABLES:
            for action in ('UPDATE', 'DELETE'):
                c.execute(f"CREATE TRIGGER IF NOT EXISTS immutable_{name}_{action.lower()} BEFORE {action} ON {name} BEGIN SELECT RAISE(ABORT,'Client receipts are immutable'); END")


def digest(value): return hashlib.sha256(store.dumps(value).encode()).hexdigest()


def audit(actor, action, payload):
    with store.connect() as c:
        c.execute('BEGIN IMMEDIATE')
        previous = c.execute('SELECT entry_hash FROM client_audit ORDER BY id DESC LIMIT 1').fetchone()
        prior = previous[0] if previous else '0' * 64
        timestamp = store.now()
        entry = {'created_at': timestamp, 'actor': actor, 'action': action, 'payload': payload, 'previous_hash': prior}
        c.execute('INSERT INTO client_audit VALUES(NULL,?,?,?,?,?,?)', (timestamp, actor, action, store.dumps(payload), prior, digest(entry)))


def verify_audit():
    with store.connect() as c: rows = c.execute('SELECT * FROM client_audit ORDER BY id').fetchall()
    prior = '0' * 64
    for r in rows:
        entry = {k: r[k] for k in ('created_at', 'actor', 'action', 'previous_hash')}
        entry['payload'] = json.loads(r['payload'])
        if r['previous_hash'] != prior or digest(entry) != r['entry_hash']: raise ValueError('Audit chain integrity failure')
        prior = r['entry_hash']
    return {'entries': len(rows), 'head': prior, 'valid': True,
            'limitation': 'Export the head to customer-controlled immutable storage; a database administrator can rewrite an entire local database'}


def identifier(): return str(uuid.uuid4())
