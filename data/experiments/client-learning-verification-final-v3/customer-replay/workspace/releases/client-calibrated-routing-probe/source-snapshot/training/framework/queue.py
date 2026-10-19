"""Durable, explicitly dispatched local jobs. API restarts never launch training.

Workers survive API restarts. Interrupted attempts are terminal; restart creates
a NEW plan/job ID and starts from the base checkpoint, never an implied optimizer
resume. OS flock serialises dispatchers; the existing model lease protects work.
"""
import json
import os
import signal
import subprocess
import sys
import time
import uuid
import fcntl

import psutil
from apps.api import store
from training.framework import jobs


def tables(database=None):
    with store.connect(database) as c:
        c.executescript('''
        CREATE TABLE IF NOT EXISTS learning_tasks(
          id TEXT PRIMARY KEY,job_id TEXT NOT NULL UNIQUE,state TEXT NOT NULL,
          created_at TEXT NOT NULL,updated_at TEXT NOT NULL,pid INTEGER,pid_started REAL,
          cancel_requested INTEGER NOT NULL DEFAULT 0,detail TEXT NOT NULL);
        CREATE TABLE IF NOT EXISTS learning_task_history(
          id INTEGER PRIMARY KEY AUTOINCREMENT,task_id TEXT NOT NULL REFERENCES learning_tasks(id),
          created_at TEXT NOT NULL,state TEXT NOT NULL,detail TEXT NOT NULL);
        CREATE TRIGGER IF NOT EXISTS immutable_task_history_update BEFORE UPDATE ON learning_task_history
        BEGIN SELECT RAISE(ABORT,'Task history is immutable'); END;
        CREATE TRIGGER IF NOT EXISTS immutable_task_history_delete BEFORE DELETE ON learning_task_history
        BEGIN SELECT RAISE(ABORT,'Task history is immutable'); END;
        ''')


def transition(c, ident, state, detail):
    at = jobs.now()
    c.execute('UPDATE learning_tasks SET state=?,updated_at=?,detail=? WHERE id=?', (state, at, store.dumps(detail), ident))
    c.execute('INSERT INTO learning_task_history(task_id,created_at,state,detail) VALUES(?,?,?,?)', (ident, at, state, store.dumps(detail)))


def alive(pid, started):
    if not pid or started is None: return False
    try: return psutil.Process(pid).create_time() == started and psutil.Process(pid).status() != psutil.STATUS_ZOMBIE
    except (psutil.NoSuchProcess, psutil.AccessDenied): return False


def recover(database=None):
    tables(database)
    with store.connect(database) as c:
        c.execute('BEGIN IMMEDIATE')
        for r in c.execute("SELECT * FROM learning_tasks WHERE state='RUNNING'").fetchall():
            if not alive(r['pid'], r['pid_started']):
                transition(c, r['id'], 'INTERRUPTED', {'reason': 'Owning worker exited; explicit new attempt required', 'automatic_resume': False})


def listing(database=None):
    recover(database)
    with store.connect(database) as c:
        return [{**dict(r), 'detail': json.loads(r['detail'])} for r in c.execute('SELECT * FROM learning_tasks ORDER BY created_at DESC')]


def submit(job_id, database=None):
    root = jobs.member('jobs', job_id)
    _, plan = jobs.verify_plan(root)
    if jobs.status(root)['state'] != 'PREPARED' or not plan['preflight']['ready']:
        raise ValueError('Only a fresh ready PREPARED job can be queued')
    tables(database)
    with store.connect(database) as c:
        c.execute('BEGIN IMMEDIATE')
        old = c.execute('SELECT * FROM learning_tasks WHERE job_id=?', (job_id,)).fetchone()
        if old: return dict(old)
        ident = str(uuid.uuid4()); at = jobs.now()
        c.execute('INSERT INTO learning_tasks VALUES(?,?,?,?,?,?,?,?,?)', (ident, job_id, 'QUEUED', at, at, None, None, 0, '{}'))
        transition(c, ident, 'QUEUED', {'automatic_start': False, 'resume_mode': 'NEW_ATTEMPT_ONLY'})
        return dict(c.execute('SELECT * FROM learning_tasks WHERE id=?', (ident,)).fetchone())


def cancel(ident, database=None):
    tables(database)
    with store.connect(database) as c:
        c.execute('BEGIN IMMEDIATE')
        r = c.execute('SELECT * FROM learning_tasks WHERE id=?', (ident,)).fetchone()
        if not r: raise ValueError('Task not found')
        if r['state'] not in ('QUEUED', 'RUNNING'): return dict(r)
        c.execute('UPDATE learning_tasks SET cancel_requested=1 WHERE id=?', (ident,))
        if r['state'] == 'QUEUED': transition(c, ident, 'CANCELLED', {'reason': 'Cancelled before execution; no model loaded'})
        else:
            c.execute('INSERT INTO learning_task_history(task_id,created_at,state,detail) VALUES(?,?,?,?)',
                      (ident, jobs.now(), 'CANCEL_REQUESTED', '{}'))
        return dict(c.execute('SELECT * FROM learning_tasks WHERE id=?', (ident,)).fetchone())


def spawn(database=None):
    """Explicit dispatch only. Independent worker owns child training processes."""
    if jobs.active_experiments(): raise ValueError('Timed benchmark active; tasks remain queued')
    env = dict(os.environ, VOTING_TRAINING_WORKSPACE=str(jobs.WORKSPACE))
    jobs.WORKSPACE.mkdir(parents=True, exist_ok=True)
    log = (jobs.WORKSPACE / 'queue-worker.log').open('ab')
    try:
        p = subprocess.Popen([sys.executable, '-m', 'training.framework.queue', '--database',
                              str(__import__('pathlib').Path(database or store.DB_PATH).resolve())],
                             cwd=jobs.ROOT, env=env, stdout=log, stderr=log, start_new_session=True)
    finally: log.close()
    return {'worker_pid': p.pid, 'automatic_resume': False}


def run(database=None):
    jobs.WORKSPACE.mkdir(parents=True, exist_ok=True)
    with (jobs.WORKSPACE / 'queue-worker.lock').open('a') as lock:
        try: fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError: return
        recover(database)
        while True:
            if jobs.active_experiments() or (jobs.WORKSPACE / 'model-training.lock').exists(): return
            with store.connect(database) as c:
                c.execute('BEGIN IMMEDIATE')
                r = c.execute("SELECT * FROM learning_tasks WHERE state='QUEUED' AND cancel_requested=0 ORDER BY created_at,id LIMIT 1").fetchone()
                if not r: return
                ident = r['id']; root = jobs.WORKSPACE / 'jobs' / r['job_id']
                c.execute('UPDATE learning_tasks SET pid=?,pid_started=? WHERE id=?', (os.getpid(), psutil.Process().create_time(), ident))
                transition(c, ident, 'RUNNING', {'job': str(root), 'owner': 'DETACHED_LOCAL_WORKER'})
            interrupted = None
            try:
                with (root / 'worker.log').open('ab') as log:
                    child = subprocess.Popen([sys.executable, '-m', 'training.framework', 'execute', str(root)],
                                             cwd=jobs.ROOT, stdout=log, stderr=log, start_new_session=True)
                    while child.poll() is None:
                        with store.connect(database) as c:
                            requested = c.execute('SELECT cancel_requested FROM learning_tasks WHERE id=?', (ident,)).fetchone()[0]
                        if requested and interrupted is None:
                            interrupted = time.monotonic(); os.killpg(child.pid, signal.SIGINT)
                        elif interrupted and time.monotonic() - interrupted > 20:
                            os.killpg(child.pid, signal.SIGKILL)
                        time.sleep(.2)
                state = 'COMPLETED' if child.returncode == 0 else 'CANCELLED' if interrupted else 'FAILED'
                detail = {'returncode': child.returncode, 'job_state': jobs.status(root)['state'], 'partial_checkpoint_promoted': False}
                if interrupted:
                    # A forced termination can leave the model lease. Only reclaim
                    # the exact owned child PID after it has exited; retain receipt.
                    lease = jobs.WORKSPACE / 'model-training.lock'
                    if lease.exists() and json.loads(lease.read_text()).get('pid') == child.pid:
                        lease.unlink(); detail['owned_stale_resource_lease_reclaimed'] = True
            except Exception as exc:
                state = 'FAILED'; detail = {'error': f'{type(exc).__name__}: {exc}'}
            with store.connect(database) as c: transition(c, ident, state, detail)


if __name__ == '__main__':
    import argparse
    p = argparse.ArgumentParser(); p.add_argument('--database', required=True)
    run(p.parse_args().database)
