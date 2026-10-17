"""Bounded REAL Laya + Qwen lifecycle receipt, through the application API.

8 TRAIN, 4 VALIDATION, 4 CALIBRATION, 4 FROZEN_TEST are engineering qualification
samples, fixed before training. No challenge data. No production-quality claim.
"""
import argparse
import json
import os
import socket
import subprocess
import sys
import time
import urllib.request
from pathlib import Path

from training.framework import jobs, events, event_data
from training.framework.bundle import load_bundle, create_bundle, write, sha


def verify(output, *, version='event-loop-v1', reuse_qwen_job=None):
    if jobs.active_experiments(): raise RuntimeError('Timed benchmark must reach its cooperative stop before qualification')
    bundle_root = jobs.WORKSPACE / 'bundles'
    _, rows = load_bundle(bundle_root / 'event-reviews-v1')
    selected = []
    for split, count in [('TRAIN', 8), ('VALIDATION', 4)]:
        selected.extend(sorted((e for e in rows if e.split == split), key=lambda e: e.id)[:count])
    if not (bundle_root / version).exists(): create_bundle(selected, bundle_root / version, source_manifest={'purpose': 'Bounded real-backend engineering acceptance',
        'roles_read': ['TRAIN', 'VALIDATION'], 'held_out_answers_opened': False, 'original_bundle': 'event-reviews-v1'})
    ids = {e.id for e in selected}
    metadata = events.listing()
    for split in ['CALIBRATION', 'FROZEN_TEST']:
        ids.update(r['id'] for r in sorted((r for r in metadata if r['split'] == split), key=lambda r: r['id'])[:4])
    cohort = jobs.WORKSPACE / 'event-datasets' / version
    cohort_manifest = (json.loads((cohort / 'manifest.json').read_text()) if cohort.exists() else event_data.freeze_dataset(cohort, event_ids=ids))
    if not (jobs.WORKSPACE / (version + '-COHORT.json')).exists(): write(jobs.WORKSPACE / (version + '-COHORT.json'), {'dataset_manifest_sha256': sha(cohort / 'manifest.json'),
        'ids': sorted(ids), 'counts': cohort_manifest['roles'], 'selected_before_model_execution': True,
        'source_type': 'STANDARDS_DERIVED_SYNTHETIC', 'label_origin': 'AI_AUTHORED'})
    with socket.socket() as s:
        s.bind(('127.0.0.1', 0)); port = s.getsockname()[1]
    base = f'http://127.0.0.1:{port}/api/'
    env = dict(os.environ, TRAINING_EXECUTION_ENABLED='true')
    def call(path, body=None):
        request = urllib.request.Request(base + path, data=None if body is None else json.dumps(body).encode(),
                                         headers={'Content-Type': 'application/json'})
        with urllib.request.urlopen(request, timeout=900) as response: return json.load(response)
    def start():
        with Path('artifacts/event-learning-proof-server.log').open('ab') as log:
            p = subprocess.Popen([sys.executable, '-m', 'uvicorn', 'apps.api.main:app', '--host', '127.0.0.1', '--port', str(port)],
                                 env=env, stdout=log, stderr=log)
        for _ in range(100):
            try: call('health'); return p
            except OSError: time.sleep(.1)
        p.terminate(); p.wait(); raise RuntimeError('Qualification API did not start')
    process = start(); began = time.perf_counter(); receipt = {'version': version, 'cohort': cohort_manifest, 'jobs': {}}
    try:
        for family, filename in [('Laya', 'laya'), ('Qwen', 'qwen38-mlx')]:
            spec = json.loads(Path(f'training/framework/specs/{filename}.json').read_text())
            if family == 'Qwen' and reuse_qwen_job:
                _, reused_plan = jobs.verify_plan(jobs.WORKSPACE / 'jobs' / reuse_qwen_job, check_sources=False)
                assert reused_plan['bundle_manifest_sha256'] == sha(bundle_root / version / 'manifest.json')
                receipt['jobs'][family] = reuse_qwen_job
                continue
            spec.update(batch_size=1, gradient_accumulation=1)
            if family == 'Laya': spec['learning_rate'] = .0001
            else: spec['max_steps'] = 1
            r = call('training/jobs', {'bundle_id': version, 'spec': spec})
            if not r['plan']['preflight']['ready']: raise RuntimeError(r['plan']['preflight']['reasons'])
            receipt['jobs'][family] = r['id']
            call(f"learning/jobs/{r['id']}/enqueue", {})
        receipt['dispatch'] = call('learning/dispatch', {})
        # Restart FastAPI while the independent worker owns execution.
        time.sleep(2); process.terminate(); process.wait(20); process = start()
        deadline = time.monotonic() + 1800
        while True:
            tasks = call('learning/status')['tasks']
            ours = [t for t in tasks if t['job_id'] in receipt['jobs'].values()]
            if len(ours) != 2: raise RuntimeError('Task identity/count changed across API restart')
            if all(t['state'] == 'COMPLETED' for t in ours): break
            if any(t['state'] in ('FAILED', 'INTERRUPTED', 'CANCELLED') for t in ours): raise RuntimeError(ours)
            if time.monotonic() > deadline: raise TimeoutError('Bounded training did not finish')
            time.sleep(3)
        receipt['tasks'] = ours; receipt['api_restart_during_training_verified'] = True
        reports = {}
        for role in ['VALIDATION', 'CALIBRATION']:
            r = call('learning/comparisons', {'dataset_id': version, 'candidates': receipt['jobs'], 'role': role})
            reports[role] = r
        validation = reports['VALIDATION']['report']['metrics']
        # Development-only choice, fixed before the frozen comparison.
        best = max(validation, key=lambda name: (validation[name]['correct_assertions'], -validation[name]['median_latency_ms']))
        history = call('learning/status')['selections']; previous = history[-1]['id'] if history else None
        first_name = next(iter(receipt['jobs']))
        first = call('learning/selections', {'job_id': receipt['jobs'][first_name], 'actor': 'AI engineering qualification',
            'reason': 'Initial experimental selection for reversible deployment check; no production claim', 'expected_previous_id': previous})
        second = call('learning/selections', {'job_id': receipt['jobs'][best], 'actor': 'AI engineering qualification',
            'reason': 'Development validation assertion count, latency tie-break; engineering cohort only', 'expected_previous_id': first['id']})
        frozen = call('learning/comparisons', {'dataset_id': version, 'candidates': receipt['jobs'], 'role': 'FROZEN_TEST', 'selection_id': second['id']})
        reports['FROZEN_TEST'] = frozen
        event_id = next(e.id for e in selected if e.split == 'VALIDATION')
        receipt['application_executions'] = {}
        for name, job in receipt['jobs'].items():
            receipt['application_executions'][name] = call(f'learning/events/{event_id}/analyse', {'job_id': job})
        view = call('learning/events/' + event_id); last = view['reviews'][-1]
        target = last['payload']['target']
        review = call(f'learning/events/{event_id}/reviews', {'snapshot_hash': view['snapshot_hash'], 'expected_revision': last['id'],
            'target': target, 'notes': 'AI re-review of construction facts and exact source spans, following real trained-candidate inference; no expert claim.',
            'expected_deadline_status': last['payload'].get('expected_deadline_status'),
            'expected_final_status': last['payload'].get('expected_final_status'),
            'provenance': {'origin': 'AI_REVIEWED', 'author': 'GPT-6 / Codex', 'model_id': 'GPT-6 / Codex',
                           'method': 'AI-assisted operative-source evidence check', 'source_reference': event_id, 'revision': version}})
        assert review['payload']['previous_prediction'] and review['payload']['validation_type'] == 'AI_ASSISTED_NOT_HUMAN_GOLD'
        exported = call('learning/exports', {'id': version + '-reviewed'})
        receipt['review'] = review['id']; receipt['review_export'] = exported
        rollback = call('learning/selections', {'job_id': first['job_id'], 'actor': 'AI engineering qualification',
            'reason': 'Verify explicit rollback preserves checkpoint identity', 'expected_previous_id': second['id'], 'rollback_id': first['id']})
        assert rollback['manifest_sha256'] == first['manifest_sha256']
        # Leave the development-selected candidate selected, through another explicit record.
        selected_final = call('learning/selections', {'job_id': second['job_id'], 'actor': 'AI engineering qualification',
            'reason': 'Restore previously selected validation candidate after rollback verification', 'expected_previous_id': rollback['id']})
        # Exercise cancellation and explicit new-attempt semantics without training again.
        spare = call('training/jobs', {'bundle_id': version, 'spec': json.loads(Path('training/framework/specs/laya.json').read_text())})
        task = call(f"learning/jobs/{spare['id']}/enqueue", {})
        cancelled = call(f"learning/tasks/{task['id']}/cancel", {})
        restarted = call(f"learning/jobs/{spare['id']}/restart", {})
        assert restarted['id'] != spare['id'] and not restarted['execution_started'] and not restarted['optimizer_resume']
        receipt.update(reports={k: {'id': v['id'], 'metrics': v['report']['metrics'], 'repair_damage': v['report']['repair_damage']} for k, v in reports.items()},
                       selection_ids=[first['id'], second['id'], rollback['id'], selected_final['id']],
                       cancellation={'task': cancelled['id'], 'state': cancelled['state'], 'new_job': restarted['id']},
                       customer_accuracy=None, automation_enabled=False)
        process.terminate(); process.wait(20); process = start()
        restored = call('learning/events/' + event_id)
        expected_ids = {r['id'] for r in receipt['application_executions'].values()}
        assert expected_ids <= {r['id'] for r in restored['executions']}
        assert restored['reviews'][-1]['id'] == review['id']
        assert call('learning/status')['selections'][-1]['id'] == selected_final['id']
        receipt.update(restart_persistence_verified=True, total_seconds=time.perf_counter() - began, completed_at=jobs.now())
        write(output, receipt)
        print(json.dumps({'passed': True, 'jobs': receipt['jobs'], 'seconds': receipt['total_seconds']}, indent=2))
    finally:
        process.terminate(); process.wait(20)


if __name__ == '__main__':
    p = argparse.ArgumentParser(); p.add_argument('--output', default='artifacts/event-learning-real-proof-v1.json'); p.add_argument('--version', default='event-loop-v1')
    p.add_argument('--reuse-qwen-job')
    a = p.parse_args(); verify(a.output, version=a.version, reuse_qwen_job=a.reuse_qwen_job)
