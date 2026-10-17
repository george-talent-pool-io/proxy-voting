"""Local deployment controls, integrity rejection and cold restore."""
import json
import shutil
from pathlib import Path

import pytest

from training.framework import jobs, operations
from apps.api import store


def test_local_operator_authentication_protects_reads_writes_and_assets(client, monkeypatch):
    monkeypatch.setenv('LOCAL_OPERATOR_PASSWORD', 'controlled-test-secret')
    assert client.get('/api/health').status_code == 200
    assert client.get('/api/learning/status').status_code == 401
    assert client.get('/').status_code == 401
    assert client.post('/api/learning/dispatch').status_code == 401
    assert client.get('/api/learning/status', auth=('operator', 'wrong')).status_code == 401
    assert client.get('/api/learning/status', auth=('operator', 'controlled-test-secret')).status_code == 200
    assert client.get('/api/learning/status', headers={'authorization': 'Basic !invalid!'}).status_code == 401


def test_verified_backup_restore_and_no_automatic_execution(db, tmp_path):
    workspace = jobs.WORKSPACE; workspace.mkdir(parents=True)
    (workspace / 'registered.txt').write_text('Exact retained artefact')
    snapshot = tmp_path / 'snapshot'
    m = operations.backup(snapshot, database=db)
    assert m['workspace_files']['registered.txt']
    with pytest.raises(ValueError, match='must not exist'):
        operations.restore(snapshot, workspace=workspace, database=db)
    retired = tmp_path / 'original-offline'; workspace.rename(retired)
    Path(db).rename(tmp_path / 'original.sqlite')
    # Close/no service is running against this isolated test DB.
    for suffix in ['-wal', '-shm']:
        Path(db + suffix).unlink(missing_ok=True)
    receipt = operations.restore(snapshot, workspace=workspace, database=db)
    assert receipt['restored'] and not receipt['automatic_resume']
    assert (workspace / 'registered.txt').read_text() == 'Exact retained artefact'
    with store.connect(db) as c: assert c.execute('SELECT count(*) FROM notices').fetchone()[0] == 3
    assert not (workspace / 'model-training.lock').exists()


def test_corrupt_backup_is_rejected_before_restore(db, tmp_path):
    jobs.WORKSPACE.mkdir(parents=True); (jobs.WORKSPACE / 'value').write_text('before')
    output = tmp_path / 'snapshot'; operations.backup(output, database=db)
    (output / 'workspace/value').write_text('corrupt')
    jobs.WORKSPACE.rename(tmp_path / 'old-workspace'); Path(db).rename(tmp_path / 'old-db')
    with pytest.raises(ValueError, match='integrity mismatch'):
        operations.restore(output, workspace=jobs.WORKSPACE, database=db)
    assert not jobs.WORKSPACE.exists()


def test_execution_default_off_in_campaign_api(client):
    assert client.post('/api/learning/campaigns/unknown/dispatch').status_code == 403
    r = client.get('/api/learning/readiness')
    assert r.status_code == 200 and r.json()['database_integrity'] == 'ok'
    assert not r.json()['automation_enabled']
