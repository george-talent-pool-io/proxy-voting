"""Finish the bounded real campaign acceptance, serially and without retraining."""
import argparse
import json
import os
import subprocess
import sys
import time
import urllib.request
from pathlib import Path

from training.framework import campaigns, jobs
from training.framework.bundle import write, sha


def run(ident):
    root = jobs.member('campaigns', ident)
    deadline = time.monotonic() + 7200
    while True:
        state = campaigns.status(root)['state']
        if state == 'COMPLETED': break
        if state in ('FAILED', 'INTERRUPTED', 'CANCELLED'): raise RuntimeError('Campaign did not complete: ' + state)
        if time.monotonic() > deadline: raise TimeoutError('Campaign completion wait budget exceeded')
        time.sleep(10)
    def command(args, log, **env):
        with Path(log).open('xb') as f:
            p = subprocess.run([sys.executable, *args], cwd=jobs.ROOT, env={**os.environ, **env},
                               stdout=f, stderr=subprocess.STDOUT, timeout=2400)
        if p.returncode: raise RuntimeError('Verification failed; inspect ' + log)
    command(['-m', 'scripts.verify_release_handoff', ident, '--output', 'artifacts/release-framework-handoff.json'],
            'artifacts/release-framework-handoff.log')
    command(['-m', 'pytest', 'tests/classifier/test_registered_release_real.py', '-q'],
            'artifacts/release-framework-real-model-tests.log', RUN_RELEASE_REAL_MODEL='1', RELEASE_CAMPAIGN=ident)
    command(['-m', 'scripts.report_release_campaign', ident], 'artifacts/release-framework-report.log')
    from training.framework.operations import backup
    old_umask = os.umask(0o077)
    try:
        receipt = backup('artifacts/backups/learning-framework-verified-v1')
    finally: os.umask(old_umask)
    write('artifacts/release-framework-backup-receipt.json', {
        'workspace_file_count': len(receipt['workspace_files']), 'database_sha256': receipt['database_sha256'],
        'external_base_model_count': len(receipt['external_base_models']),
        'backup_root_permissions': oct(Path('artifacts/backups/learning-framework-verified-v1').stat().st_mode & 0o777),
        'scope': 'Verified real snapshot; cold restore separately qualified on isolated integration fixtures'})
    from playwright.sync_api import sync_playwright, expect
    handoff = json.loads(Path('artifacts/release-framework-handoff.json').read_text())
    with sync_playwright() as pw:
        chrome = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
        browser = pw.chromium.launch(headless=True, executable_path=chrome if Path(chrome).exists() else None)
        page = browser.new_page(viewport={'width': 1440, 'height': 1000}); errors = []
        page.on('pageerror', lambda e: errors.append(str(e)))
        page.goto('http://127.0.0.1:8000/#model_lab')
        page.locator('#learning-event-id').select_option(handoff['event_id'])
        expect(page.locator('#learning-event-executions')).to_contain_text('Complete release')
        traces = page.locator('#learning-event-executions .framework-decision-trace')
        traces.last.evaluate('(el)=>el.open=true'); traces.last.scroll_into_view_if_needed()
        expect(traces.last).to_contain_text('Release identity, routing and model stages')
        expect(traces.last).to_contain_text('Calibrated confidence unavailable')
        expect(page.locator('#learning-analyse')).to_be_disabled()
        page.screenshot(path='artifacts/release-framework-live.png')
        assert not errors
        write('artifacts/release-framework-live-browser.json', {'passed': True, 'browser_errors': errors,
              'persisted_real_execution_ids': [r['id'] for r in handoff['executions'].values()],
              'default_execution_disabled': True, 'source': 'REAL_MODEL_API_TRACES_NOT_BROWSER_DOUBLES'})
        browser.close()
    with urllib.request.urlopen('http://127.0.0.1:8000/api/learning/readiness') as response:
        ready = json.load(response)
    assert not ready['automation_enabled'] and not ready['running_tasks']
    write('artifacts/release-framework-completion.json', {'campaign_id': ident, 'completed_at': jobs.now(),
          'campaign_result_sha256': sha(root / 'result.json'), 'readiness': ready,
          'handoff_sha256': sha('artifacts/release-framework-handoff.json'),
          'real_model_test_log': 'artifacts/release-framework-real-model-tests.log',
          'regression_log': 'artifacts/release-isolated-regression.log', 'browser_log': 'artifacts/release-isolated-browser.log',
          'automation_enabled': False, 'customer_accuracy': None})
    print(json.dumps({'passed': True, 'campaign': ident, 'complete': True}), flush=True)


if __name__ == '__main__':
    p = argparse.ArgumentParser(); p.add_argument('id'); run(p.parse_args().id)
