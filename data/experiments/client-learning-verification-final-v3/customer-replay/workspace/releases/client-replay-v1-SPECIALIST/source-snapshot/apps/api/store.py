"""Append-only prediction/review ledger backed by SQLite WAL."""
import json
import os
import sqlite3
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path

DB_PATH = os.environ.get('VOTING_DB', 'data/voting.sqlite')

def now(): return datetime.now(timezone.utc).isoformat()

def dumps(value): return json.dumps(value, ensure_ascii=False, allow_nan=False, sort_keys=True)

@contextmanager
def connect(path=None):
    dbpath = path or DB_PATH
    Path(dbpath).parent.mkdir(parents=True, exist_ok=True)
    con = sqlite3.connect(dbpath, timeout=30)
    con.row_factory = sqlite3.Row
    con.execute('PRAGMA foreign_keys=ON')
    try:
        yield con
        con.commit()
    except BaseException:
        con.rollback()
        raise
    finally: con.close()

def initialise(path=None):
    with connect(path) as c:
        c.execute('PRAGMA journal_mode=WAL')
        c.executescript('''
CREATE TABLE IF NOT EXISTS notices(id TEXT PRIMARY KEY, source_hash TEXT NOT NULL, group_id TEXT NOT NULL, split TEXT NOT NULL CHECK(split IN ('train','validation','test')), text TEXT NOT NULL, metadata TEXT NOT NULL, imported_at TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS runs(id TEXT PRIMARY KEY, created_at TEXT NOT NULL, status TEXT NOT NULL, model TEXT NOT NULL, model_version TEXT NOT NULL, config TEXT NOT NULL, config_version TEXT NOT NULL, dataset_hash TEXT NOT NULL, manifest TEXT NOT NULL, completed_at TEXT, benchmark TEXT);
CREATE TABLE IF NOT EXISTS run_inputs(run_id TEXT NOT NULL REFERENCES runs(id), record_id TEXT NOT NULL REFERENCES notices(id), source_hash TEXT NOT NULL, PRIMARY KEY(run_id,record_id));
CREATE TABLE IF NOT EXISTS predictions(run_id TEXT NOT NULL REFERENCES runs(id), record_id TEXT NOT NULL REFERENCES notices(id), source_hash TEXT NOT NULL, result TEXT, error TEXT, created_at TEXT NOT NULL, PRIMARY KEY(run_id,record_id));
CREATE TABLE IF NOT EXISTS reviews(id INTEGER PRIMARY KEY AUTOINCREMENT, record_id TEXT NOT NULL REFERENCES notices(id), run_id TEXT REFERENCES runs(id), previous_revision INTEGER, reviewer TEXT NOT NULL, reviewed_at TEXT NOT NULL, label TEXT, notes TEXT NOT NULL, action TEXT NOT NULL CHECK(action IN ('VERIFY','FLAG')), previous_prediction TEXT, ai_correct INTEGER, FOREIGN KEY(previous_revision) REFERENCES reviews(id));
CREATE TABLE IF NOT EXISTS policies(id INTEGER PRIMARY KEY AUTOINCREMENT, created_at TEXT NOT NULL, run_id TEXT NOT NULL REFERENCES runs(id), policy TEXT NOT NULL);
CREATE INDEX IF NOT EXISTS prediction_record ON predictions(record_id);
CREATE INDEX IF NOT EXISTS review_record ON reviews(record_id,id);
CREATE INDEX IF NOT EXISTS group_index ON notices(group_id);
CREATE TRIGGER IF NOT EXISTS immutable_run_inputs_update BEFORE UPDATE ON run_inputs BEGIN SELECT RAISE(ABORT,'Run inputs are immutable'); END;
CREATE TRIGGER IF NOT EXISTS immutable_run_inputs_delete BEFORE DELETE ON run_inputs BEGIN SELECT RAISE(ABORT,'Run inputs are immutable'); END;
CREATE TRIGGER IF NOT EXISTS immutable_run_metadata BEFORE UPDATE OF model,model_version,config,config_version,dataset_hash,manifest ON runs BEGIN SELECT RAISE(ABORT,'Run configuration is immutable'); END;
CREATE TRIGGER IF NOT EXISTS immutable_predictions_update BEFORE UPDATE ON predictions BEGIN SELECT RAISE(ABORT,'Predictions are immutable'); END;
CREATE TRIGGER IF NOT EXISTS immutable_predictions_delete BEFORE DELETE ON predictions BEGIN SELECT RAISE(ABORT,'Predictions are immutable'); END;
CREATE TRIGGER IF NOT EXISTS immutable_reviews_update BEFORE UPDATE ON reviews BEGIN SELECT RAISE(ABORT,'Review history is immutable'); END;
CREATE TRIGGER IF NOT EXISTS immutable_reviews_delete BEFORE DELETE ON reviews BEGIN SELECT RAISE(ABORT,'Review history is immutable'); END;
CREATE TRIGGER IF NOT EXISTS immutable_notices_update BEFORE UPDATE ON notices BEGIN SELECT RAISE(ABORT,'Source records and split assignments are immutable'); END;
CREATE TRIGGER IF NOT EXISTS immutable_notices_delete BEFORE DELETE ON notices BEGIN SELECT RAISE(ABORT,'Source records are immutable'); END;
''')
        if 'context' not in [r[1] for r in c.execute('PRAGMA table_info(reviews)')]:
            c.execute("ALTER TABLE reviews ADD COLUMN context TEXT NOT NULL DEFAULT '{}'")

def import_normalised(file, path=None):
    from classifier.preprocessing import source_hash
    from training.split import verify_isolation,duplicate_groups
    rows=[json.loads(x) for x in Path(file).read_text().splitlines() if x.strip()]
    if len({r['id'] for r in rows})!=len(rows):raise ValueError('Duplicate source IDs')
    verify_isolation(rows)
    inferred=duplicate_groups(rows)
    verify_isolation([{**r,'group_id':g} for r,g in zip(rows,inferred)])
    with connect(path) as c:
        # Freeze corpus membership once reviews exist, rather than regrouping a labelled dataset.
        if c.execute('SELECT count(*) FROM reviews').fetchone()[0]:
            raise ValueError('Corpus frozen after first review; create a new database for a new corpus')
        existing_ids={r[0] for r in c.execute('SELECT id FROM notices')}
        if existing_ids and set(r['id'] for r in rows)!=existing_ids:
            raise ValueError('Corpus membership is frozen; use a new database for a different corpus')
        for r in rows:
            if not isinstance(r.get('text'),str) or source_hash(r['text']) != r['source_hash']:
                raise ValueError('Invalid notice text or source hash')
            existing=c.execute('SELECT source_hash FROM notices WHERE id=?',(r['id'],)).fetchone()
            if existing and existing[0] != r['source_hash']: raise ValueError('Source ID collision')
            c.execute('INSERT OR IGNORE INTO notices VALUES (?,?,?,?,?,?,?)',
                (r['id'],r['source_hash'],r['group_id'],r['split'],r['text'],dumps({k:v for k,v in r.items() if k!='text'}),now()))
    return len(rows)

def latest_run(c):
    row=c.execute("SELECT * FROM runs ORDER BY created_at DESC LIMIT 1").fetchone()
    return dict(row) if row else None

def prediction(c, record_id, run_id=None):
    if not run_id:
        run=latest_run(c)
        run_id=run['id'] if run else None
    row=c.execute('SELECT result,error FROM predictions WHERE record_id=? AND run_id=?',(record_id,run_id)).fetchone()
    return json.loads(row['result']) if row and row['result'] else None

def latest_review(c, record_id):
    row=c.execute('SELECT * FROM reviews WHERE record_id=? ORDER BY id DESC LIMIT 1',(record_id,)).fetchone()
    if not row: return None
    r=dict(row)
    for key in ['label','previous_prediction']: r[key]=json.loads(r[key]) if r[key] else None
    return r
