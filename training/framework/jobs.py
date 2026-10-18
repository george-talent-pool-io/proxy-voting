"""Immutable plans and versioned run events. Preparing a job never trains a model."""
import json
import os
import subprocess
import sys
import uuid
import re
from datetime import datetime, timezone
from pathlib import Path

from training.framework import VERSION
from training.framework.bundle import ROOT, sha, write, load_bundle
from training.framework.schema import TrainSpec
from training.framework.trainers import preflight, snapshot

WORKSPACE = Path(os.environ.get('VOTING_TRAINING_WORKSPACE', ROOT / 'data/training-workspace')).resolve()


def now():
    return datetime.now(timezone.utc).isoformat()


def member(kind, name):
    if not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_-]{0,119}', name):
        raise ValueError('Invalid workspace identifier')
    path = (WORKSPACE / kind / name).resolve()
    if path.parent != (WORKSPACE / kind).resolve(): raise ValueError('Workspace boundary violation')
    return path


def events(root, event):
    with (Path(root) / 'events.jsonl').open('a', encoding='utf-8') as f:
        f.write(json.dumps({'timestamp': now(), **event}, allow_nan=False) + '\n')
        f.flush()
        os.fsync(f.fileno())


def prepare(bundle, spec, output):
    spec = spec if isinstance(spec, TrainSpec) else TrainSpec.model_validate(spec)
    spec = spec.model_copy(update={'model_path': str(Path(spec.model_path).resolve())})
    bundle = Path(bundle).resolve()
    check = preflight(bundle, spec)
    output = Path(output).resolve()
    output.mkdir(parents=True, exist_ok=False)
    sources = {str(p.relative_to(ROOT)): sha(p) for p in sorted((ROOT / 'training/framework').glob('*.py'))}
    for name in sources:
        archive = output / 'source-snapshot' / name
        archive.parent.mkdir(parents=True, exist_ok=True)
        archive.write_bytes((ROOT / name).read_bytes())
    base_files = snapshot(spec.model_path) if check['ready'] else None
    plan = {'version': VERSION, 'job_id': str(uuid.uuid4()), 'created_at': now(),
            'bundle': str(bundle), 'bundle_manifest_sha256': sha(bundle / 'manifest.json'),
            'spec': spec.model_dump(), 'preflight': check, 'source_hashes': sources,
            'base_model_files': base_files,
            'git_commit': subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip(),
            'model_execution_started': False, 'automation_enabled': False, 'customer_accuracy': None}
    write(output / 'plan.json', plan)
    events(output, {'state': 'PREPARED' if check['ready'] else 'BLOCKED', 'reasons': check['reasons']})
    return plan


def verify_plan(root, *, check_sources=True):
    root = Path(root).resolve()
    plan = json.loads((root / 'plan.json').read_text())
    if sha(Path(plan['bundle']) / 'manifest.json') != plan['bundle_manifest_sha256']:
        raise ValueError('Planned dataset changed')
    load_bundle(plan['bundle'])
    for name, expected in plan['source_hashes'].items():
        archive = root / 'source-snapshot' / name
        if archive.exists() and sha(archive) != expected:
            raise ValueError('Archived trainer source changed')
        if check_sources and sha(ROOT / name) != expected:
            raise ValueError('Trainer source changed; prepare a new job')
    return root, plan


def active_experiments():
    """Do not overlap GPU training with timed local benchmark processes."""
    import psutil
    found = []
    for p in psutil.process_iter(['pid', 'cmdline']):
        try:
            cmd = ' '.join(p.info['cmdline'] or [])
            if p.pid != os.getpid() and any(s in cmd for s in [
                '-m scripts.run_laya_first', '-m scripts.run_qwen_domain', '-m qwen_domain.study']):
                found.append({'pid': p.pid, 'command': cmd})
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    return found


def execute(root):
    root, plan = verify_plan(root)
    # O_EXCL serialises this job across API restarts/processes. Never silently
    # restart a partially trained run under the original identity.
    lock = root / 'execution.lock'
    with lock.open('x') as f:
        f.write(str(os.getpid()))
    lease = WORKSPACE / 'model-training.lock'
    acquired = False
    try:
        active = active_experiments()
        if active:
            raise ValueError(f'Timed model experiment active; defer training: {active}')
        spec = TrainSpec.model_validate(plan['spec'])
        check = preflight(plan['bundle'], spec)
        if not check['ready']:
            raise ValueError('; '.join(check['reasons']))
        if check.get('parent_checkpoint_identity') != plan['preflight'].get('parent_checkpoint_identity'):
            raise ValueError('Frozen parent identity changed after preparation')
        lease.parent.mkdir(parents=True, exist_ok=True)
        try:
            with lease.open('x') as f:
                f.write(json.dumps({'pid': os.getpid(), 'job': str(root), 'created_at': now()}))
            acquired = True
        except FileExistsError:
            raise ValueError('Another training resource lease exists; inspect its PID before starting a new job')
        base = snapshot(spec.model_path)
        if plan.get('base_model_files') != base:
            raise ValueError('Base checkpoint changed after job preparation; prepare a new job')
        write(root / 'base-model-files.json', base)
        events(root, {'state': 'RUNNING', 'versions': check['versions'], 'hardware': check['hardware']})
        from training.framework.trainers import train_laya, train_peft, train_mlx
        trainer = {'LAYA_SDK': train_laya, 'TRANSFORMERS_PEFT': train_peft,
                   'MLX_QLORA': train_mlx}[spec.backend]
        result = trainer(plan['bundle'], root / 'checkpoint', spec)
        if snapshot(spec.model_path) != base:
            raise ValueError('Base checkpoint changed during training')
        write(root / 'result.json', result)
        artifacts = snapshot(root / 'checkpoint')
        model = {'job_id': plan['job_id'], 'created_at': now(), 'family': spec.family,
                 'backend': spec.backend, 'base_model_id': spec.base_model_id,
                 'base_revision': spec.base_revision, 'base_files_sha256': sha(root / 'base-model-files.json'),
                 'bundle_manifest_sha256': plan['bundle_manifest_sha256'],
                 'files': artifacts, 'label_origins': check['label_origins'],
                 'status': 'EXPERIMENTAL_NOT_PROMOTED', 'semantic_evaluation': 'PENDING',
                 'calibrator': None, 'automation_enabled': False, 'customer_accuracy': None}
        write(root / 'model-manifest.json', model)
        events(root, {'state': 'COMPLETED', 'model_manifest_sha256': sha(root / 'model-manifest.json')})
        return model
    except BaseException as exc:
        events(root, {'state': 'INTERRUPTED' if isinstance(exc, KeyboardInterrupt) else 'FAILED',
                      'error': f'{type(exc).__name__}: {exc}'})
        raise
    finally:
        if acquired:
            lease.unlink()


def status(root):
    root = Path(root)
    plan = json.loads((root / 'plan.json').read_text())
    records = [json.loads(line) for line in (root / 'events.jsonl').read_text().splitlines()]
    return {'job_id': plan['job_id'], 'family': plan['spec']['family'],
            'backend': plan['spec']['backend'], 'state': records[-1]['state'],
            'created_at': plan['created_at'], 'label_origins': plan['preflight']['label_origins'],
            'preflight': plan['preflight'], 'events': records,
            'automation_enabled': False, 'customer_accuracy': None}
