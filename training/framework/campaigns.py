"""Explicit, bounded learning campaigns. No resume or model promotion on GET.

Stages are fixed before execution. Train/validation chooses model/routing;
separate calibration fits correctness; selection is frozen before test scoring.
"""
import fcntl
import json
import os
import signal
import subprocess
import sys
import time
import uuid
from pathlib import Path

import psutil
from pydantic import BaseModel, ConfigDict, Field, model_validator
from training.framework import jobs, releases
from training.framework.bundle import write, sha, load_bundle
from training.framework.schema import TrainSpec
from training.framework.resources import model_resource


class Stage(BaseModel):
    model_config = ConfigDict(extra='forbid')
    name: str = Field(pattern=r'^[A-Za-z][A-Za-z0-9_-]{0,59}$')
    reuse_job: str | None = None
    training: TrainSpec | None = None

    @model_validator(mode='after')
    def one_source(self):
        if (self.reuse_job is None) == (self.training is None): raise ValueError('Use exactly one stage source')
        return self


class Candidate(BaseModel):
    model_config = ConfigDict(extra='forbid')
    name: str = Field(pattern=r'^[A-Za-z][A-Za-z0-9_-]{0,59}$')
    mode: str
    laya_stage: str | None = None
    llm_stage: str | None = None
    policy: dict = Field(default_factory=lambda: releases.ReleaseSpec(mode='QWEN_ONLY', llm_job='placeholder').policy)


class CampaignSpec(BaseModel):
    model_config = ConfigDict(extra='forbid')
    bundle_id: str
    dataset_id: str
    stages: list[Stage] = Field(min_length=1, max_length=12)
    candidates: list[Candidate] = Field(min_length=1, max_length=20)
    actor: str = Field(min_length=1)
    reference: str = '2026-10-17T12:00:00+00:00'
    max_seconds: int = Field(default=3600, ge=30, le=86400)

    @model_validator(mode='after')
    def dependencies(self):
        names = {s.name for s in self.stages}
        if len(names) != len(self.stages) or len({c.name for c in self.candidates}) != len(self.candidates):
            raise ValueError('Duplicate stage/candidate identity')
        for c in self.candidates:
            if any(n and n not in names for n in (c.laya_stage, c.llm_stage)): raise ValueError('Unknown campaign stage dependency')
            releases.ReleaseSpec(mode=c.mode, laya_job=c.laya_stage, llm_job=c.llm_stage, policy=c.policy)
        return self


def prepare(spec, output):
    spec = CampaignSpec.model_validate(spec)
    bundle = jobs.member('bundles', spec.bundle_id); manifest, examples = load_bundle(bundle)
    from training.framework.event_data import load_inputs
    dataset = jobs.member('event-datasets', spec.dataset_id)
    _, development = load_inputs(dataset, 'TRAIN'); _, validation = load_inputs(dataset, 'VALIDATION')
    dataset_manifest = json.loads((dataset / 'manifest.json').read_text())
    if 'answer_files' not in dataset_manifest:
        raise ValueError('Campaign requires role-isolated answer files; migrate legacy dataset explicitly')
    ids = {r['id']: r for r in development + validation}
    for e in examples:
        if e.id not in ids or ids[e.id]['source_hash'] != e.source_hash or ids[e.id]['split'] != e.split:
            raise ValueError('Campaign bundle/dataset membership mismatch')
    if {e.id for e in examples} != set(ids): raise ValueError('Campaign bundle must cover exactly its development cohort')
    for stage in spec.stages:
        if stage.reuse_job:
            from training.framework.runtime import verify_checkpoint
            _, p, _ = verify_checkpoint(jobs.member('jobs', stage.reuse_job))
            # Reused baselines can use a smaller prior development bundle but
            # still pass global protected-input checks via verify_checkpoint.
            if p['spec']['family'] not in ('LAYA', 'QWEN', 'GLM', 'OTHER_CAUSAL_LM'): raise ValueError('Unsupported baseline')
    root = Path(output); root.mkdir(parents=True, exist_ok=False)
    write(root / 'campaign.json', {'spec': spec.model_dump(), 'created_at': jobs.now(),
          'bundle_sha256': sha(bundle / 'manifest.json'), 'dataset_sha256': sha(dataset / 'manifest.json'),
          'source_hashes': releases.source_files(), 'label_origins': manifest['label_origins'],
          'automation_enabled': False, 'customer_accuracy': None})
    jobs.events(root, {'state': 'PREPARED', 'automatic_start': False})
    return status(root)


def status(root):
    root = Path(root)
    plan = json.loads((root / 'campaign.json').read_text())
    records = [json.loads(s) for s in (root / 'events.jsonl').read_text().splitlines()]
    state = records[-1]['state']
    if state in ('RUNNING', 'CANCEL_REQUESTED'):
        owner = next((e for e in reversed(records) if 'pid' in e), None)
        from training.framework.queue import alive
        if owner and not alive(owner['pid'], owner['pid_started']):
            jobs.events(root, {'state': 'INTERRUPTED', 'reason': 'Campaign worker exited; explicit new campaign required'})
            state = 'INTERRUPTED'
    return {'id': root.name, 'state': state, 'plan': plan, 'events': records,
            'report': json.loads((root / 'result.json').read_text()) if (root / 'result.json').exists() else None}


def listing():
    return [status(p.parent) for p in sorted((jobs.WORKSPACE / 'campaigns').glob('*/campaign.json'))]


def cancel(root):
    root = Path(root); s = status(root)
    if s['state'] not in ('PREPARED', 'RUNNING'): return s
    try: (root / 'STOP').touch(exist_ok=False)
    except FileExistsError: pass
    jobs.events(root, {'state': 'CANCELLED' if s['state'] == 'PREPARED' else 'CANCEL_REQUESTED', 'automatic_resume': False})
    return status(root)


def spawn(root, database=None):
    root = Path(root)
    if status(root)['state'] != 'PREPARED': raise ValueError('Only a prepared campaign can be dispatched')
    if jobs.active_experiments(): raise ValueError('Timed benchmark active; campaign deferred')
    env = dict(os.environ, VOTING_TRAINING_WORKSPACE=str(jobs.WORKSPACE), VOTING_DB=str(database or __import__('apps.api.store', fromlist=['DB_PATH']).DB_PATH))
    with (root / 'worker.log').open('ab') as log:
        p = subprocess.Popen([sys.executable, '-m', 'training.framework.campaigns', str(root)],
                             cwd=jobs.ROOT, env=env, stdout=log, stderr=log, start_new_session=True)
    return {'worker_pid': p.pid, 'automatic_resume': False}


def run(root, *, database=None):
    root = Path(root)
    with (root / 'execution.lock').open('x'):
        pass
    # A separate campaign lock serialises campaigns without blocking their own
    # training subprocess from acquiring the shared local model resource lease.
    with (jobs.WORKSPACE / 'campaign-worker.lock').open('a') as lock:
        try: fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            jobs.events(root, {'state': 'FAILED', 'reason': 'Another campaign owns execution'}); raise ValueError('Campaign resource busy')
        return _run(root, database=database)


def _run(root, *, database=None):
    plan = json.loads((root / 'campaign.json').read_text()); spec = CampaignSpec.model_validate(plan['spec'])
    began = time.monotonic(); bundle = jobs.member('bundles', spec.bundle_id); dataset = jobs.member('event-datasets', spec.dataset_id)
    def check():
        if (root / 'STOP').exists(): raise InterruptedError('Campaign cancellation requested')
        if time.monotonic() - began > spec.max_seconds: raise TimeoutError('Campaign time budget exceeded')
        if jobs.active_experiments(): raise ValueError('Timed benchmark active; campaign must be retried explicitly')
    def progress(phase, **extra):
        check(); jobs.events(root, {'state': 'RUNNING', 'phase': phase, **extra})
    jobs.events(root, {'state': 'RUNNING', 'pid': os.getpid(), 'pid_started': psutil.Process().create_time()})
    try:
        check()
        if sha(bundle / 'manifest.json') != plan['bundle_sha256'] or sha(dataset / 'manifest.json') != plan['dataset_sha256']:
            raise ValueError('Campaign dataset changed')
        if releases.source_files() != plan['source_hashes']: raise ValueError('Campaign source changed; prepare a new campaign')
        stage_jobs = {}
        for stage in spec.stages:
            progress('TRAINING', stage=stage.name)
            if stage.reuse_job:
                stage_jobs[stage.name] = stage.reuse_job
            else:
                ident = str(uuid.uuid4()); path = jobs.member('jobs', ident)
                jobs.prepare(bundle, stage.training, path)
                jobs.events(root, {'state': 'RUNNING', 'phase': 'JOB_PREPARED', 'stage': stage.name, 'job_id': ident})
                child = None
                try:
                    with (root / (stage.name + '-training.log')).open('xb') as log:
                        child = subprocess.Popen([sys.executable, '-m', 'training.framework', 'execute', str(path)],
                              cwd=jobs.ROOT, env={**os.environ, 'VOTING_TRAINING_WORKSPACE': str(jobs.WORKSPACE)},
                              stdout=log, stderr=log, start_new_session=True)
                        while child.poll() is None:
                            check(); time.sleep(.2)
                    if child.returncode != 0: raise RuntimeError('Training stage failed; inspect preserved log and job')
                finally:
                    if child and child.poll() is None:
                        os.killpg(child.pid, signal.SIGINT)
                        try: child.wait(timeout=20)
                        except subprocess.TimeoutExpired: os.killpg(child.pid, signal.SIGKILL); child.wait()
                        lease = jobs.WORKSPACE / 'model-training.lock'
                        if lease.exists() and json.loads(lease.read_text()).get('pid') == child.pid: lease.unlink()
                stage_jobs[stage.name] = ident
        from training.framework.release_evaluation import evaluate, calibrate, coverage
        candidates = {}; validation = {}
        for candidate in spec.candidates:
            progress('VALIDATION', candidate=candidate.name)
            ident = root.name + '-' + candidate.name; path = jobs.member('releases', ident)
            releases.prepare({'mode': candidate.mode, 'laya_job': stage_jobs.get(candidate.laya_stage),
                              'llm_job': stage_jobs.get(candidate.llm_stage), 'policy': candidate.policy}, path)
            candidates[candidate.name] = ident
            with model_resource('campaign-validation'):
                validation[candidate.name] = evaluate(dataset, path, root / ('validation-' + candidate.name), reference=spec.reference, check=check)
        # Predeclared interpretable objective: labelled-assertion correctness,
        # then measured validation latency. No frozen/test outcomes are read.
        baseline = next(iter(validation))
        baseline_misses = {(r['id'], r['predicate']) for r in validation[baseline]['critical_false_negatives']}
        damage_gates = {}
        for name, report in validation.items():
            introduced = [r for r in report['critical_false_negatives'] if (r['id'], r['predicate']) not in baseline_misses]
            damage_gates[name] = {'passed': not introduced, 'new_critical_false_negatives': introduced,
                                  'baseline': baseline, 'scope': 'Development selection gate, not customer qualification'}
        eligible = [k for k in validation if damage_gates[k]['passed']]
        winner = max(eligible, key=lambda k: (validation[k]['metrics']['correct_assertions'],
                                                -validation[k]['metrics']['median_latency_ms']))
        write(root / 'VALIDATION_SELECTION.json', {'winner': winner, 'release_id': candidates[winner],
              'objective': 'Maximum validation assertions; minimum latency tie-break',
              'critical_damage_gates': damage_gates,
              'validation_sha256': {k: sha(root / ('validation-' + k) / 'evaluation.json') for k in validation},
              'protected_answers_opened': False})
        selected = jobs.member('releases', candidates[winner]); progress('CALIBRATION', candidate=winner)
        with model_resource('campaign-calibration'):
            evaluate(dataset, selected, root / 'calibration-predictions', role='CALIBRATION', reference=spec.reference, check=check)
        calibrate(root / 'calibration-predictions', root / 'calibration')
        coverage(root / 'calibration-predictions', root / 'calibration')
        # All candidates get a complete seal; non-winners retain null calibration.
        for name, ident in candidates.items():
            releases.seal(jobs.member('releases', ident), root / ('validation-' + name), root / 'calibration' if name == winner else None)
        previous = releases.history(database)
        selected_history = releases.select(candidates[winner], actor=spec.actor,
              reason='Explicit opt-in engineering campaign; validation selection before frozen scoring',
              expected_previous_id=previous[-1]['id'] if previous else None, database=database)
        write(root / 'OPERATING_FREEZE.json', {'selection': selected_history, 'seal_sha256': sha(selected / 'SEALED.json'),
              'frozen_at': jobs.now(), 'automation_enabled': False})
        progress('FROZEN_TEST', candidate=winner)
        with model_resource('campaign-protected-evaluation'):
            frozen = evaluate(dataset, selected, root / 'frozen-test', role='FROZEN_TEST', reference=spec.reference,
                              selection_id=selected_history['id'], database=database, check=check)
        report = {'stage_jobs': stage_jobs, 'candidates': candidates, 'selected': winner,
                  'validation': validation, 'frozen': frozen, 'selection_id': selected_history['id'],
                  'critical_damage_gates': damage_gates,
                  'calibration': json.loads((root / 'calibration/calibration.json').read_text()),
                  'seconds': time.monotonic() - began, 'automation_enabled': False, 'customer_accuracy': None}
        write(root / 'result.json', report); jobs.events(root, {'state': 'COMPLETED', 'result_sha256': sha(root / 'result.json')})
        return report
    except BaseException as exc:
        jobs.events(root, {'state': 'INTERRUPTED' if isinstance(exc, (KeyboardInterrupt, InterruptedError)) else 'FAILED',
                          'error': f'{type(exc).__name__}: {exc}', 'automatic_resume': False})
        raise


if __name__ == '__main__':
    import argparse
    p = argparse.ArgumentParser(); p.add_argument('campaign')
    run(p.parse_args().campaign)
