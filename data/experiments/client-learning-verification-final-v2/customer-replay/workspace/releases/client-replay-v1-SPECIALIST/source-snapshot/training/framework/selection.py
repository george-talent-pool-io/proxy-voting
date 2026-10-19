"""Explicit, append-only experimental selection/rollback. No automatic promotion."""
import json
from apps.api import store
from training.framework.bundle import sha
from training.framework.jobs import now


def tables(c):
    c.executescript('''CREATE TABLE IF NOT EXISTS learning_selections(
      id INTEGER PRIMARY KEY AUTOINCREMENT,created_at TEXT NOT NULL,action TEXT NOT NULL,
      job_id TEXT NOT NULL,manifest_sha256 TEXT NOT NULL,previous_id INTEGER REFERENCES learning_selections(id),
      payload TEXT NOT NULL);
      CREATE TRIGGER IF NOT EXISTS immutable_selections_update BEFORE UPDATE ON learning_selections
      BEGIN SELECT RAISE(ABORT,'Selection history is immutable'); END;
      CREATE TRIGGER IF NOT EXISTS immutable_selections_delete BEFORE DELETE ON learning_selections
      BEGIN SELECT RAISE(ABORT,'Selection history is immutable'); END;''')


def history(database=None):
    with store.connect(database) as c:
        tables(c)
        return [{**dict(r), 'payload': json.loads(r['payload'])} for r in c.execute('SELECT * FROM learning_selections ORDER BY id')]


def choose(job_id, *, actor, reason, expected_previous_id=None, database=None, rollback_id=None):
    if not actor.strip() or not reason.strip(): raise ValueError('Selection requires actor and reason')
    from training.framework.jobs import member
    from training.framework.runtime import verify_checkpoint
    path, plan, manifest = verify_checkpoint(member('jobs', job_id))
    # Selection is made on development validation only, before frozen scoring.
    from training.framework.jobs import status
    evaluations = [e for e in status(path)['events'] if e.get('kind') == 'VALIDATION_EVALUATION']
    if not evaluations: raise ValueError('Validation evaluation required before experimental selection')
    e = evaluations[-1]
    from pathlib import Path
    metrics = Path(e['evaluation_path']) / 'metrics.json'
    if sha(metrics) != e['metrics_sha256']: raise ValueError('Validation receipt changed')
    if json.loads(metrics.read_text())['job_id'] != plan['job_id']: raise ValueError('Validation belongs to another model')
    with store.connect(database) as c:
        tables(c); c.execute('BEGIN IMMEDIATE')
        previous = c.execute('SELECT * FROM learning_selections ORDER BY id DESC LIMIT 1').fetchone()
        if (previous['id'] if previous else None) != expected_previous_id: raise ValueError('Selection revision conflict')
        if rollback_id is not None:
            target = c.execute('SELECT * FROM learning_selections WHERE id=?', (rollback_id,)).fetchone()
            if not target or target['job_id'] != job_id or target['manifest_sha256'] != sha(path / 'model-manifest.json'):
                raise ValueError('Rollback target/checkpoint mismatch')
        payload = {'actor': actor, 'reason': reason, 'rollback_target_id': rollback_id,
                   'validation_receipt_sha256': e['metrics_sha256'],
                   'prompt_sha256': sha(__import__('pathlib').Path(plan['bundle']) / 'semantic-prompt.txt'),
                   'rule_version': 'semantic-decision-2', 'calibrator': None,
                   'confidence': None, 'confidence_status': 'NOT_YET_CALIBRATED',
                   'scope': 'EXPERIMENTAL_ONLY', 'automation_enabled': False, 'customer_accuracy': None}
        cur = c.execute('INSERT INTO learning_selections(created_at,action,job_id,manifest_sha256,previous_id,payload) VALUES(?,?,?,?,?,?)',
                        (now(), 'ROLLBACK' if rollback_id is not None else 'SELECT', job_id, sha(path / 'model-manifest.json'), expected_previous_id, store.dumps(payload)))
        return {**dict(c.execute('SELECT * FROM learning_selections WHERE id=?', (cur.lastrowid,)).fetchone()), 'payload': payload}
