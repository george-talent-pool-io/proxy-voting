"""Retain every inference byte while correcting pre-label dataset grouping in a new DB.
Grouping/splits are not classifier inputs. This migration is forbidden after any review.
"""
import argparse
import hashlib
import json
from pathlib import Path
import sqlite3
from apps.api import store

def migrate(source,target,normalised,history_dir=None):
    source=Path(source);target=Path(target)
    if target.exists():raise ValueError('Migration target exists; preserve previous artifacts')
    with sqlite3.connect(source) as prior:
        if prior.execute('SELECT count(*) FROM reviews').fetchone()[0]:raise ValueError('Cannot regroup reviewed records')
        if prior.execute("SELECT count(*) FROM runs WHERE status='RUNNING'").fetchone()[0]:raise ValueError('Wait for active inference to finish')
        original={r[0]:(r[1],r[2],r[3],r[4]) for r in prior.execute('SELECT id,source_hash,text,group_id,split FROM notices')}
        history=Path(history_dir or 'data/history');history.mkdir(parents=True,exist_ok=True)
        backup=history/'pre-exact-grouping.sqlite'
        if backup.exists():raise ValueError('Existing grouping backup must be retained')
        with sqlite3.connect(backup) as dest:prior.backup(dest)
    store.initialise(str(target));store.import_normalised(normalised,str(target))
    with store.connect(str(target)) as c:
        current={r['id']:dict(r) for r in c.execute('SELECT * FROM notices')}
        if set(current)!=set(original):raise ValueError('Source input membership differs')
        for k,r in current.items():
            if (r['source_hash'],r['text'])!=original[k][:2]:raise ValueError('Model input differs; inference cannot be reused')
        c.execute('ATTACH DATABASE ? AS prior',(str(backup),))
        for table in ['runs','run_inputs','predictions']:
            cols=[r[1] for r in c.execute(f'PRAGMA table_info({table})')]
            names=','.join(cols)
            c.execute(f'INSERT INTO {table} ({names}) SELECT {names} FROM prior.{table}')
        # The inference ledger is byte-for-byte preserved. Dataset grouping gets its own revision ledger.
        c.execute('CREATE TABLE IF NOT EXISTS dataset_revisions(id TEXT PRIMARY KEY,created_at TEXT NOT NULL,metadata TEXT NOT NULL)')
        revision={'protocol':'exact-prefix-jaccard-v2','previous_protocol':'minhash-lsh-v1','source_backup':str(backup),
            'source_backup_sha256':hashlib.sha256(backup.read_bytes()).hexdigest(),'source_rows':len(current),
            'changed_group_rows':sum(r['group_id']!=original[k][2] for k,r in current.items()),
            'changed_split_rows':sum(r['split']!=original[k][3] for k,r in current.items()),
            'original_text_and_hashes_identical':True,'all_run_inputs_and_predictions_preserved':True,
            'reviews_before_migration':0,'inference_note':'Question/option order, source text, model and raw results unchanged. Grouping is not a model input. No human labels existed at migration.'}
        c.execute('INSERT INTO dataset_revisions VALUES (?,?,?)',('exact-prefix-jaccard-v2',store.now(),store.dumps(revision)))
        c.execute('CREATE TRIGGER immutable_dataset_revisions_update BEFORE UPDATE ON dataset_revisions BEGIN SELECT RAISE(ABORT,\'Dataset revision history is immutable\'); END')
        c.execute('CREATE TRIGGER immutable_dataset_revisions_delete BEFORE DELETE ON dataset_revisions BEGIN SELECT RAISE(ABORT,\'Dataset revision history is immutable\'); END')
    return revision
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--source',default='data/voting.sqlite');p.add_argument('--target',default='data/voting-v2.sqlite');p.add_argument('--input',default='data/normalised/public-v2.jsonl');a=p.parse_args()
    result=migrate(a.source,a.target,a.input)
    with open('artifacts/grouping-migration.json','x') as f:json.dump(result,f,indent=2)
    print(store.dumps(result))
