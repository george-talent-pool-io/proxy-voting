"""Local single-operator deployment checks and verified cold workspace restore.

Snapshots include registered adapters/checkpoints, plans, release/calibration
packages and an SQLite online backup. Large external base models remain pinned
prerequisites. Restore never overwrites an existing workspace or database.
"""
import json
import os
import shutil
import sqlite3
from pathlib import Path

from apps.api import store
from training.framework import jobs, queue, campaigns
from training.framework.bundle import sha, write
from training.framework.trainers import snapshot
from training.framework.resources import model_resource


def readiness(database=None):
    with store.connect(database) as c:
        integrity = c.execute('PRAGMA quick_check').fetchone()[0]
    tasks = queue.listing(database)
    return {'database_integrity': integrity, 'workspace': str(jobs.WORKSPACE),
            'training_execution_enabled': os.environ.get('TRAINING_EXECUTION_ENABLED', 'false').lower() == 'true',
            'authentication_configured': bool(os.environ.get('LOCAL_OPERATOR_PASSWORD')),
            'deployment_scope': 'LOOPBACK_SINGLE_OPERATOR', 'running_tasks': sum(t['state'] == 'RUNNING' for t in tasks),
            'campaigns': [{'id': c['id'], 'state': c['state']} for c in campaigns.listing()],
            'automation_enabled': False, 'customer_accuracy': None}


def backup(output, *, database=None):
    database = Path(database or store.DB_PATH).resolve(); workspace = jobs.WORKSPACE.resolve()
    output = Path(output).resolve()
    if output == workspace or workspace in output.parents: raise ValueError('Snapshot must be outside workspace')
    if any(t['state'] == 'RUNNING' for t in queue.listing(database)) or any(c['state'] in ('RUNNING', 'CANCEL_REQUESTED') for c in campaigns.listing()):
        raise ValueError('Quiesce training/campaign workers before snapshot')
    with model_resource('workspace-backup'):
        output.mkdir(parents=True, exist_ok=False)
        # Lease is an execution artefact, never restored as live ownership.
        ignored = {'model-training.lock', 'queue-worker.lock', 'campaign-worker.lock'}
        def inventory(root):
            return {str(p.relative_to(root)): sha(p) for p in root.rglob('*') if p.is_file() and p.name not in ignored}
        before = inventory(workspace)
        shutil.copytree(workspace, output / 'workspace', ignore=shutil.ignore_patterns(*ignored))
        with sqlite3.connect(database) as src, sqlite3.connect(output / 'database.sqlite') as dst:
            src.backup(dst)
            if dst.execute('PRAGMA integrity_check').fetchone()[0] != 'ok': raise ValueError('Snapshot database integrity failure')
        after = inventory(workspace)
        if before != after or inventory(output / 'workspace') != before:
            raise ValueError('Workspace changed during backup; partial snapshot is not certified')
        prerequisites = {}
        for p in workspace.glob('jobs/*/plan.json'):
            plan = json.loads(p.read_text())
            if plan.get('base_model_files'):
                prerequisites[plan['spec']['model_path']] = plan['base_model_files']
        receipt = {'created_at': jobs.now(), 'original_workspace': str(workspace), 'original_database': str(database),
                   'workspace_files': before, 'database_sha256': sha(output / 'database.sqlite'),
                   'external_base_models': prerequisites, 'restore_policy': 'Exact configured paths; empty destinations; explicit service restart only',
                   'automation_enabled': False}
        write(output / 'BACKUP.json', receipt)
        return receipt


def restore(source, *, workspace, database):
    source = Path(source).resolve(); workspace = Path(workspace).resolve(); database = Path(database).resolve()
    m = json.loads((source / 'BACKUP.json').read_text())
    if workspace.exists() or database.exists(): raise ValueError('Restore destinations must not exist; no overwrite')
    if str(workspace) != m['original_workspace'] or str(database) != m['original_database']:
        raise ValueError('Restore uses exact configured paths; immutable job plans are not silently rewritten')
    if snapshot(source / 'workspace') != m['workspace_files'] or sha(source / 'database.sqlite') != m['database_sha256']:
        raise ValueError('Backup integrity mismatch')
    for path, expected in m['external_base_models'].items():
        if snapshot(path) != expected: raise ValueError('Restore requires the pinned external base-model files')
    workspace.parent.mkdir(parents=True, exist_ok=True); database.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(source / 'workspace', workspace)
    shutil.copyfile(source / 'database.sqlite', database)
    with sqlite3.connect(database) as c:
        if c.execute('PRAGMA integrity_check').fetchone()[0] != 'ok': raise ValueError('Restored SQLite integrity failure')
    # Interrupted jobs are not restarted by restoring files or opening the API.
    return {'restored': True, 'workspace': str(workspace), 'database': str(database), 'automatic_resume': False,
            'automation_enabled': False}


def main():
    import argparse
    p = argparse.ArgumentParser(); sub = p.add_subparsers(dest='action', required=True)
    sub.add_parser('readiness')
    b = sub.add_parser('backup'); b.add_argument('output'); b.add_argument('--database')
    r = sub.add_parser('restore'); r.add_argument('source'); r.add_argument('--workspace', required=True); r.add_argument('--database', required=True)
    a = p.parse_args()
    if a.action == 'readiness': value = readiness()
    elif a.action == 'backup': value = backup(a.output, database=a.database)
    else: value = restore(a.source, workspace=a.workspace, database=a.database)
    print(json.dumps(value, indent=2))


if __name__ == '__main__': main()
