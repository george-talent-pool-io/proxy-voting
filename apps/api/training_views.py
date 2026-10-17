"""Framework status and immutable job preparation; no model is loaded by GET."""
import json
import re
import uuid
import os
import threading
from pathlib import Path
from typing import Literal

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from training.framework.jobs import WORKSPACE, prepare, status
from training.framework.schema import TrainSpec
from training.framework.trainers import versions

router = APIRouter(prefix='/api/training')
_execution_lock = threading.Lock()


def execution_tables(c):
    c.executescript('''CREATE TABLE IF NOT EXISTS framework_executions(
      id TEXT PRIMARY KEY,record_id TEXT REFERENCES notices(id),source_hash TEXT NOT NULL,
      raw_source TEXT NOT NULL,created_at TEXT NOT NULL,job_id TEXT NOT NULL,result TEXT NOT NULL);
      CREATE TRIGGER IF NOT EXISTS immutable_framework_update BEFORE UPDATE ON framework_executions
      BEGIN SELECT RAISE(ABORT,'Framework executions are immutable'); END;
      CREATE TRIGGER IF NOT EXISTS immutable_framework_delete BEFORE DELETE ON framework_executions
      BEGIN SELECT RAISE(ABORT,'Framework executions are immutable'); END;''')


def latest(record_id):
    from apps.api import store
    with store.connect() as c:
        if not c.execute("SELECT 1 FROM sqlite_master WHERE type='table' AND name='framework_executions'").fetchone(): return None
        r = c.execute('SELECT * FROM framework_executions WHERE record_id=? ORDER BY created_at DESC,rowid DESC LIMIT 1', (record_id,)).fetchone()
        return {**dict(r), 'result': json.loads(r['result'])} if r else None


@router.get('/executions/{ident}')
def execution(ident: str):
    from apps.api import store
    with store.connect() as c:
        if not c.execute("SELECT 1 FROM sqlite_master WHERE type='table' AND name='framework_executions'").fetchone():
            raise HTTPException(404, 'No saved candidate execution')
        row = c.execute('SELECT * FROM framework_executions WHERE id=?', (ident,)).fetchone()
        if not row: raise HTTPException(404, 'Saved candidate execution not found')
        return {**dict(row), 'result': json.loads(row['result'])}


def member(kind, name):
    if not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_-]{0,119}', name):
        raise ValueError('Invalid workspace identifier')
    path = (WORKSPACE / kind / name).resolve()
    if path.parent != (WORKSPACE / kind).resolve():
        raise ValueError('Workspace boundary violation')
    return path


@router.get('/status')
def overview():
    bundles = []
    for path in sorted((WORKSPACE / 'bundles').glob('*/manifest.json')):
        m = json.loads(path.read_text())
        bundles.append({'id': path.parent.name, 'counts': m['counts'], 'label_origins': m['label_origins'],
                        'predicates': m['predicates'], 'languages': m['languages']})
    jobs = [dict(id=p.parent.name, **status(p.parent)) for p in sorted((WORKSPACE / 'jobs').glob('*/plan.json'))]
    from apps.api import store
    with store.connect() as c:
        history = ([dict(r) for r in c.execute('SELECT id,job_id,created_at,source_hash,record_id FROM framework_executions ORDER BY created_at DESC LIMIT 20')]
                   if c.execute("SELECT 1 FROM sqlite_master WHERE type='table' AND name='framework_executions'").fetchone() else [])
    return {'bundles': bundles, 'jobs': jobs, 'versions': versions(), 'executions': history,
            'backends': ['LAYA_SDK', 'TRANSFORMERS_PEFT', 'MLX_QLORA'],
            'model_families': ['LAYA', 'QWEN', 'GLM'],
            'ai_labels_allowed_for_development': True, 'automation_enabled': False,
            'candidate_inference_enabled': os.environ.get('TRAINED_CANDIDATES_ENABLED', 'false').lower() == 'true',
            'customer_accuracy': None, 'scope': 'Training framework; label origin remains explicit'}


class Prepare(BaseModel):
    bundle_id: str
    spec: TrainSpec


@router.post('/jobs', status_code=201)
def prepare_job(body: Prepare):
    try:
        bundle = member('bundles', body.bundle_id)
        if not (bundle / 'manifest.json').exists():
            raise HTTPException(404, 'Training bundle not found')
        ident = str(uuid.uuid4())
        plan = prepare(bundle, body.spec, member('jobs', ident))
        return {'id': ident, 'plan': plan, 'execution_started': False}
    except ValueError as e:
        raise HTTPException(422, str(e))


@router.get('/jobs/{ident}')
def job(ident: str):
    try:
        path = member('jobs', ident)
        if not (path / 'plan.json').exists():
            raise HTTPException(404, 'Training job not found')
        return status(path)
    except ValueError as e:
        raise HTTPException(422, str(e))


class CandidateInput(BaseModel):
    record_id: str | None = None
    text: str | None = None
    reference: str = '2026-10-17T12:00:00+00:00'
    source_type: Literal['USER_PROVIDED','STANDARDS_DERIVED_SYNTHETIC','PUBLIC_EXAMPLE'] = 'USER_PROVIDED'


@router.post('/jobs/{ident}/analyse', status_code=201)
def analyse_candidate(ident: str, body: CandidateInput):
    from datetime import datetime
    from apps.api import store
    from training.framework.jobs import active_experiments, now
    from classifier.preprocessing import source_hash
    if os.environ.get('TRAINED_CANDIDATES_ENABLED', 'false').lower() != 'true':
        raise HTTPException(403, 'Trained-candidate execution is experimental and disabled by default')
    if bool(body.record_id) == bool(body.text): raise HTTPException(422, 'Supply either record_id or raw text')
    try:
        if datetime.fromisoformat(body.reference.replace('Z', '+00:00')).tzinfo is None: raise ValueError()
    except ValueError: raise HTTPException(422, 'Reference time requires an explicit timezone')
    if active_experiments(): raise HTTPException(409, 'Timed benchmark active; candidate inference deferred')
    if (WORKSPACE / 'model-training.lock').exists(): raise HTTPException(409, 'Training owns the local model resource; candidate inference deferred')
    try: path = member('jobs', ident)
    except ValueError as exc: raise HTTPException(422, str(exc))
    if not (path / 'model-manifest.json').exists(): raise HTTPException(409, 'No completed registered checkpoint')
    text = body.text
    if body.record_id:
        with store.connect() as c:
            row = c.execute('SELECT text FROM notices WHERE id=?', (body.record_id,)).fetchone()
            if not row: raise HTTPException(404, 'Notice not found')
            text = row['text']
    if not text or not text.strip() or len(text) > 2_000_000: raise HTTPException(422, 'Nonempty source within input limit required')
    if not _execution_lock.acquire(blocking=False): raise HTTPException(409, 'Candidate inference already running')
    model = None
    lease = None
    try:
        from training.framework.resources import model_resource
        lease = model_resource('registered-candidate-inference', workspace=WORKSPACE)
        lease.__enter__()
        from training.framework.runtime import RegisteredModel
        model = RegisteredModel(path)
        result = model.analyse(text, reference=body.reference)
        result['source_type'] = 'EXISTING_NOTICE' if body.record_id else body.source_type
        if result['input_hash'] != source_hash(text): raise ValueError('Candidate source hash mismatch')
        value = {'id': str(uuid.uuid4()), 'record_id': body.record_id, 'source_hash': source_hash(text),
                 'raw_source': text, 'created_at': now(), 'job_id': ident, 'result': result}
        with store.connect() as c:
            execution_tables(c)
            c.execute('INSERT INTO framework_executions VALUES(?,?,?,?,?,?,?)',
                      tuple(value[k] if k != 'result' else json.dumps(result, ensure_ascii=False, allow_nan=False)
                            for k in ['id','record_id','source_hash','raw_source','created_at','job_id','result']))
        return value
    except (ValueError, RuntimeError, OSError) as exc:
        raise HTTPException(503, str(exc))
    finally:
        try:
            if model is not None: model.close()
        finally:
            if lease is not None: lease.__exit__(None, None, None)
            _execution_lock.release()
