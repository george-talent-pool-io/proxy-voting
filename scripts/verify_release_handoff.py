"""Execute a completed real campaign release through API, rollback and restart."""
import argparse
import json
import os
import socket
import subprocess
import sys
import time
import urllib.request
from pathlib import Path

from training.framework import jobs, campaigns
from training.framework.bundle import write, sha
from training.framework.event_data import load_inputs


def verify(ident, output):
    root = jobs.member('campaigns', ident); status = campaigns.status(root)
    if status['state'] != 'COMPLETED': raise ValueError('Campaign must complete first')
    report = status['report']; spec = status['plan']['spec']
    with socket.socket() as s:
        s.bind(('127.0.0.1', 0)); port = s.getsockname()[1]
    base = f'http://127.0.0.1:{port}/api/'
    env = {**os.environ, 'TRAINING_EXECUTION_ENABLED': 'true', 'AUTOMATION_ENABLED': 'false'}
    def call(path, body=None):
        req = urllib.request.Request(base + path, data=json.dumps(body).encode() if body is not None else None,
                                     headers={'Content-Type': 'application/json'})
        with urllib.request.urlopen(req, timeout=1200) as r: return json.load(r)
    def start():
        with Path('artifacts/release-handoff-api.log').open('ab') as log:
            p = subprocess.Popen([sys.executable, '-m', 'uvicorn', 'apps.api.main:app', '--host', '127.0.0.1', '--port', str(port)],
                                  env=env, stdout=log, stderr=log)
        for _ in range(100):
            try: call('health'); return p
            except OSError: time.sleep(.1)
        p.terminate(); p.wait(); raise RuntimeError('Handoff API startup failed')
    process = start(); receipt = {'campaign': ident, 'campaign_result_sha256': sha(root / 'result.json'),
                                 'executions': {}, 'automation_enabled': False, 'customer_accuracy': None}
    try:
        _, rows = load_inputs(jobs.member('event-datasets', spec['dataset_id']), 'VALIDATION')
        eid = rows[0]['id']; receipt['event_id'] = eid
        for name in ['TRAINED_LAYA', 'TRAINED_QWEN', 'CASCADE_CONSERVATIVE']:
            receipt['executions'][name] = call(f'learning/events/{eid}/analyse', {'release_id': report['candidates'][name]})
        trace = receipt['executions']['CASCADE_CONSERVATIVE']['payload']['result']
        assert trace['laya'] and trace['llm_stage'] and trace['release_identity']
        assert trace['laya']['passage_predictions']
        assert trace['decision']['manual_review_required'] and not trace['automation_enabled']
        history = call('learning/status')['release_history']
        cascade = call('learning/releases/select', {'release_id': report['candidates']['CASCADE_CONSERVATIVE'],
            'actor': 'AI engineering verification', 'reason': 'Explicit complete cascade serving verification',
            'expected_previous_id': history[-1]['id']})
        other = call('learning/releases/select', {'release_id': report['candidates']['TRAINED_LAYA'],
            'actor': 'AI engineering verification', 'reason': 'Exercise complete release switch', 'expected_previous_id': cascade['id']})
        rollback = call('learning/releases/select', {'release_id': cascade['release_id'], 'rollback_id': cascade['id'],
            'actor': 'AI engineering verification', 'reason': 'Verify full routing/model/calibration rollback', 'expected_previous_id': other['id']})
        assert rollback['seal_sha256'] == cascade['seal_sha256']
        restored = call('learning/releases/select', {'release_id': report['candidates'][report['selected']],
            'actor': 'AI engineering verification', 'reason': 'Restore the unchanged validation-selected release', 'expected_previous_id': rollback['id']})
        receipt['release_history'] = [cascade, other, rollback, restored]
        process.terminate(); process.wait(20); process = start()
        view = call('learning/events/' + eid)
        expected = {e['id'] for e in receipt['executions'].values()}
        assert expected <= {e['id'] for e in view['executions']}
        assert call('learning/status')['release_history'][-1]['id'] == restored['id']
        receipt.update(restart_persistence_verified=True, completed_at=jobs.now())
        write(output, receipt)
        print(json.dumps({'passed': True, 'event_id': eid, 'executions': sorted(receipt['executions']), 'receipt': str(output)}))
    finally:
        process.terminate(); process.wait(20)


if __name__ == '__main__':
    p = argparse.ArgumentParser(); p.add_argument('id'); p.add_argument('--output', required=True)
    a = p.parse_args(); verify(a.id, a.output)
