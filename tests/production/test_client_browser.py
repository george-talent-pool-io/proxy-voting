"""Actual customer browser path; source/labels are controlled AI fixtures."""
import json
import os
from pathlib import Path
import socket
import subprocess
import sys
import time
import urllib.request
import pytest
from production.security import password_record
from tests.production.test_client_workflow import row, PASSWORD

pytestmark = pytest.mark.e2e


@pytest.fixture(scope='module')
def customer_browser(tmp_path_factory):
    from playwright.sync_api import sync_playwright
    tmp = tmp_path_factory.mktemp('client-browser')
    secret = tmp / 'users.json'
    secret.write_text(json.dumps({'operator': {'roles': ['ADMIN', 'TRAINER', 'REVIEWER'],
                                             'expert_attested': False, 'password': password_record(PASSWORD)}}))
    with socket.socket() as s: s.bind(('127.0.0.1', 0)); port = s.getsockname()[1]
    url = f'http://127.0.0.1:{port}'
    env = {**os.environ, 'VOTING_DB': str(tmp / 'db.sqlite'), 'VOTING_TRAINING_WORKSPACE': str(tmp / 'workspace'),
           'VOTING_USERS_FILE': str(secret), 'VOTING_PUBLIC_ORIGIN': url, 'VOTING_ALLOW_LOCAL_HTTP': 'true',
           'AUTOMATION_ENABLED': 'false', 'TRAINING_EXECUTION_ENABLED': 'false'}
    with (tmp / 'api.log').open('w') as log:
        p = subprocess.Popen([sys.executable, '-m', 'uvicorn', 'apps.api.production:app', '--host', '127.0.0.1', '--port', str(port)], env=env, stdout=log, stderr=log)
    try:
        for _ in range(100):
            try: urllib.request.urlopen(url + '/health/live', timeout=1); break
            except OSError: time.sleep(.1)
        else: raise RuntimeError((tmp / 'api.log').read_text())
        with sync_playwright() as pw:
            chrome = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
            browser = pw.chromium.launch(headless=True, executable_path=chrome if Path(chrome).exists() else None)
            page = browser.new_page(http_credentials={'username': 'operator', 'password': PASSWORD}, viewport={'width': 1440, 'height': 1000})
            errors = []; page.on('pageerror', lambda e: errors.append(str(e)))
            yield page, url, tmp, errors
            browser.close()
    finally: p.terminate(); p.wait(timeout=15)


def test_customer_import_review_trace_and_refresh(customer_browser):
    page, url, tmp, errors = customer_browser
    page.goto(url); page.get_by_text('CUSTOMER QUALITY GATE NOT MET', exact=False).wait_for()
    assert page.title() == 'Voting Intelligence Framework · Client workspace'
    assert page.locator('header strong').text_content() == 'Voting Intelligence Framework'
    file = tmp / 'import.jsonl'; file.write_text(json.dumps(row(text='Shareholders may vote. No blocking applies. <script>danger()</script>')) + '\n')
    page.locator('#import-id').fill('browser-corpus')
    page.locator('#import-file').set_input_files(file)
    page.locator('#import').click()
    page.get_by_role('button', name='meeting-a', exact=True).wait_for()
    page.get_by_role('button', name='meeting-a', exact=True).click()
    page.locator('#event').get_by_text('HEURISTIC', exact=False).count()
    page.get_by_role('heading', name='Original messages', exact=True).wait_for()
    assert '<script>danger()</script>' in page.locator('#event pre').first.text_content()
    page.locator('#label-votability').select_option('VOTABLE')
    page.locator('#evidence-votability').fill('["Shareholders may vote."]')
    page.locator('#ai-model').fill('AI_AUTHORED_BROWSER_FIXTURE')
    page.locator('#save-ai').click()
    page.get_by_text('Operation persisted.', exact=False).wait_for()
    assert 'AI_AUTHORED' in page.locator('#receipt').text_content()
    page.reload(); page.get_by_role('button', name='meeting-a', exact=True).click()
    page.get_by_role('heading', name='Verified facts', exact=True).wait_for()
    assert page.locator('#label-votability').input_value() == 'VOTABLE'
    Path('artifacts').mkdir(exist_ok=True)
    page.screenshot(path='artifacts/client-production-browser.png', full_page=True)
    assert errors == []
