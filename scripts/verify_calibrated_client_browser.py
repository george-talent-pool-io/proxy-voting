"""Real persisted confidence through the authenticated UI and a server restart.

No model mocks and no new inference: consumes the isolated real-model replay DB.
Ephemeral local credential is removed on exit; no source data leaves loopback.
"""
import argparse
import base64
import json
import os
import socket
import subprocess
import sys
import time
import urllib.request
from pathlib import Path
from production.security import password_record
from training.framework.bundle import write


def run(replay, output):
    from playwright.sync_api import sync_playwright, expect
    replay=Path(replay).resolve();output=Path(output).resolve();output.mkdir(parents=True,exist_ok=False)
    source=json.loads((replay/'receipt.json').read_text())
    password=os.urandom(24).hex();secret=output/'ephemeral-users.json'
    secret.write_text(json.dumps({'qualifier':{'roles':['ADMIN','TRAINER','REVIEWER','AUDITOR'],
                                              'expert_attested':False,'password':password_record(password)}}));secret.chmod(0o600)
    with socket.socket() as s:s.bind(('127.0.0.1',0));port=s.getsockname()[1]
    url=f'http://127.0.0.1:{port}'
    env={**os.environ,'VOTING_DB':source['database'],'VOTING_TRAINING_WORKSPACE':source['workspace'],
         'VOTING_USERS_FILE':str(secret),'VOTING_PUBLIC_ORIGIN':url,'VOTING_ALLOW_LOCAL_HTTP':'true',
         'VOTING_REQUIRE_WORKER':'false','AUTOMATION_ENABLED':'false','TRAINING_EXECUTION_ENABLED':'false'}
    auth='Basic '+base64.b64encode(('qualifier:'+password).encode()).decode()
    def request(path):
        with urllib.request.urlopen(urllib.request.Request(url+path,headers={'Authorization':auth}),timeout=30) as r:return json.load(r)
    child=None
    def start():
        nonlocal child
        with (output/'server.log').open('ab') as log:
            child=subprocess.Popen([sys.executable,'-m','uvicorn','apps.api.production:app','--host','127.0.0.1','--port',str(port),
                                    '--no-access-log'],env=env,stdout=log,stderr=log)
        for _ in range(150):
            try:request('/api/client/status');return
            except OSError:time.sleep(.2)
        raise RuntimeError('Local console did not start')
    def stop():
        if child and child.poll() is None:
            child.terminate()
            try:child.wait(15)
            except subprocess.TimeoutExpired:child.kill();child.wait()
    try:
        start();decisions=request('/api/client/decisions')
        if len(decisions)!=source['saved_decisions']:raise ValueError('Persisted real-model decision count changed')
        numeric=[d for d in decisions if d['decision']['confidence'] is not None]
        selected=numeric[0] if numeric else decisions[0]
        with sync_playwright() as pw:
            chrome='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
            browser=pw.chromium.launch(headless=True,executable_path=chrome if Path(chrome).exists() else None)
            context=browser.new_context(http_credentials={'username':'qualifier','password':password},viewport={'width':1440,'height':1100})
            page=context.new_page();errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
            page.goto(url);expect(page.locator('#identity')).to_contain_text('qualifier')
            expect(page.locator('#calibrators')).to_contain_text('confidence calibration')
            event=request('/api/client/events/'+selected['event_id'])
            page.locator('#query').fill(event['corp']);page.locator('#search button').click()
            page.locator('[data-event="'+selected['event_id']+'"]').click()
            expect(page.locator('#event')).to_contain_text('HUMAN REVIEW REQUIRED')
            expect(page.locator('#event')).to_contain_text('Benchmark simulation:')
            expect(page.locator('#event')).to_contain_text('Persisted model and evidence trace')
            if numeric:
                expect(page.locator('#event')).to_contain_text(f"{selected['decision']['confidence']*100:.1f}% · calibrated")
                expect(page.locator('#event')).to_contain_text('Confidence provenance')
                if not selected['decision'].get('calibration',{}).get('sha256'):raise ValueError('Missing persisted calibrator identity')
            else:expect(page.locator('#event')).to_contain_text('HEURISTIC / NOT YET CALIBRATED')
            page.screenshot(path=str(output/'calibrated-decision.png'),full_page=True)
            page.reload();expect(page.locator('#identity')).to_contain_text('qualifier')
            if errors:raise ValueError('UI errors: '+str(errors))
            browser.close()
        stop();start();after=request('/api/client/decisions')
        if after!=decisions:raise ValueError('Persisted decisions changed across process restart')
        result={'actual_persisted_decisions':len(decisions),'numerical_confidence_decisions':len(numeric),
                'restart_byte_semantic_parity':True,'browser_errors':errors,'screenshot':'calibrated-decision.png',
                'automation_enabled':False,'transport':'Loopback only; temporary credential removed',
                'scope':'AI engineering replay, not a new customer quality evaluation'}
        write(output/'receipt.json',result);return result
    finally:stop();secret.unlink(missing_ok=True)


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('replay');p.add_argument('output');a=p.parse_args();run(a.replay,a.output)
