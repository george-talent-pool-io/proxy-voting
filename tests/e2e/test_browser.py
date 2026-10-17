"""Browser acceptance tests against an isolated SQLite copy; never review real demo data.
Run RUN_E2E=1 uv run pytest tests/e2e -q. Uses installed Chrome when available.
"""
import json
import os
from pathlib import Path
import socket
import sqlite3
import subprocess
import sys
import time
import urllib.request
import pytest

pytestmark=[pytest.mark.e2e,pytest.mark.skipif(os.environ.get('RUN_E2E')!='1',reason='RUN_E2E=1 enables isolated browser acceptance suite')]


@pytest.fixture(scope='module')
def browser_app(tmp_path_factory):
    from playwright.sync_api import sync_playwright
    from apps.api import store
    from classifier.preprocessing import source_hash
    from classifier.laya_classifier import LayaClassifier
    from tests.conftest import ContractAgent
    from scripts.run_batch import run_batch
    root=tmp_path_factory.mktemp('e2e')
    db=root/'e2e.sqlite'
    source=Path('data/voting.sqlite')
    if source.exists():
        with sqlite3.connect(source) as src,sqlite3.connect(db) as dst:src.backup(dst)
        with sqlite3.connect(db) as c:
            c.executescript('DROP TRIGGER IF EXISTS immutable_reviews_delete;DELETE FROM reviews;DROP TRIGGER IF EXISTS immutable_reviews_update;')
            # An active copied job is historical snapshot state, not an active E2E worker.
            c.execute("UPDATE runs SET status='INTERRUPTED' WHERE status='RUNNING'")
    else:
        store.initialise(str(db))
        rows=[dict(id='fixture',source_hash=source_hash('Synthetic test notice'),text='Synthetic test notice',group_id='fixture',split='test',issuer='E2E fixture',market='UNKNOWN',country='UNKNOWN',language='en',event_type='Synthetic fixture')]
        p=root/'input.jsonl';p.write_text(json.dumps(rows[0])+'\n');store.import_normalised(p,str(db))
        run_batch(str(db),classifier_factory=lambda config:LayaClassifier(config,agent=ContractAgent()))
    store.initialise(str(db))
    with sqlite3.connect(db) as c:
        total=c.execute('SELECT count(*) FROM notices').fetchone()[0]
        # Pick a real persisted prediction in a held-out test group.
        row=c.execute("SELECT n.id,n.metadata,length(n.text) FROM notices n JOIN predictions p ON p.record_id=n.id WHERE n.split='test' AND p.result IS NOT NULL AND p.run_id=(SELECT id FROM runs ORDER BY created_at DESC LIMIT 1) ORDER BY length(n.text) DESC LIMIT 1").fetchone()
        if not row:pytest.fail('Baseline must persist at least one test example before E2E')
        record,metadata,length=row;issuer=json.loads(metadata)['issuer']
    with socket.socket() as sock:sock.bind(('127.0.0.1',0));port=sock.getsockname()[1]
    env={**os.environ,'VOTING_DB':str(db)}
    def start():
        with (root/'server.log').open('ab') as log:
            p=subprocess.Popen([sys.executable,'-m','uvicorn','tests.e2e.server:app','--host','127.0.0.1','--port',str(port)],env=env,stdout=log,stderr=log)
        for i in range(100):
            try:
                urllib.request.urlopen(f'http://127.0.0.1:{port}/api/health',timeout=1);return p
            except Exception:time.sleep(.1)
        p.terminate();raise RuntimeError('Server did not start')
    process=start()
    with sync_playwright() as pw:
        chrome='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
        browser=pw.chromium.launch(headless=True,executable_path=chrome if Path(chrome).exists() else None)
        page=browser.new_page(viewport={'width':1440,'height':1000})
        errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
        context={'page':page,'url':f'http://127.0.0.1:{port}','record':record,'issuer':issuer,'total':total,'length':length,'errors':errors,'db':db,'start':start,'process':[process]}
        yield context
        browser.close()
    for p in context['process']:
        if p.poll() is None:p.terminate();p.wait(timeout=10)


def test_01_dashboard(browser_app):
    from playwright.sync_api import expect
    a=browser_app;p=a['page'];p.goto(a['url']);expect(p.get_by_role('heading',name='Voting intelligence',exact=True)).to_be_visible()
    assert p.request.get(a['url']+'/api/overview').json()['total']==a['total']
    expect(p.get_by_role('heading',name='Accuracy by processing stage',exact=True)).to_be_visible()
    for label in ['Parser accuracy','Semantic-model accuracy','End-to-end decision accuracy']:
        expect(p.get_by_text(label,exact=True)).to_be_visible()
    profile=Path('data/reports/profile.json')
    if profile.exists():assert a['total']==json.loads(profile.read_text())['records']==7683
    p.screenshot(path='artifacts/overview.png',full_page=True)


def test_02_search_filter_and_detail(browser_app):
    from playwright.sync_api import expect
    a=browser_app;p=a['page'];p.get_by_role('link',name='Notice explorer',exact=True).click()
    expect(p.get_by_role('heading',name='Notice explorer',exact=True)).to_be_visible()
    p.get_by_role('searchbox',name='Search notices').fill(a['record'])
    expect(p.locator('tbody tr')).to_have_count(1)
    p.locator('tbody tr').click();expect(p.get_by_role('heading',name=a['issuer'],exact=True)).to_be_visible()
    expect(p.get_by_text('Laya decision',exact=False)).to_be_visible()
    expect(p.locator('.decision-score')).to_have_text(__import__('re').compile(r'\d+\.\d+%'))
    expect(p.get_by_role('heading',name='Why?',exact=True)).to_be_visible()
    expect(p.get_by_role('region',name='Decision evidence').locator('li').first).to_be_visible()
    for item in p.get_by_role('region',name='Decision evidence').locator('li').all():
        assert item.get_by_role('link').count()>=1
    source=p.locator('.source-text').inner_text();assert len(source)==a['length']
    assert len(source)>1000 or a['total']==1
    p.get_by_text('Native model scores by factor',exact=True).click()
    expect(p.locator('.score-group')).to_have_count(5)
    p.screenshot(path='artifacts/notice-detail.png',full_page=True)


def test_03_correct_golden_and_persist(browser_app):
    from playwright.sync_api import expect
    a=browser_app;p=a['page']
    p.get_by_label('Reviewer',exact=True).fill('')
    p.get_by_role('button',name='Confirm / correct',exact=True).click()
    assert p.request.get(a['url']+'/api/export?kind=golden').text()==''
    p.get_by_label('Verified voting opportunity',exact=True).select_option('NO')
    p.get_by_label('Reviewer',exact=True).fill('Automated E2E — isolated database only')
    p.get_by_label('Reviewer notes',exact=True).fill('Synthetic workflow assertion; not a human expert verification.')
    p.get_by_role('button',name='Confirm / correct',exact=True).click()
    expect(p.get_by_role('button',name='Save new revision')).to_be_visible()
    assert 'golden label' in p.locator('#notice-content').inner_text().lower()
    p.get_by_role('button',name='Close notice').click()
    response=p.request.get(a['url']+'/api/export?kind=golden');assert response.status==200
    assert a['record'] in response.text()
    p.reload();expect(p.get_by_role('heading',name='Notice explorer',exact=True)).to_be_visible()
    p.get_by_role('searchbox',name='Search notices').fill(a['record']);expect(p.locator('tbody tr')).to_have_count(1)
    expect(p.locator('tbody tr').get_by_text('Verified',exact=True)).to_be_visible()


def test_04_performance_errors_confusion(browser_app):
    from playwright.sync_api import expect
    a=browser_app;p=a['page'];p.get_by_role('link',name='Model performance',exact=True).click()
    expect(p.get_by_role('heading',name='Confusion matrix',exact=True)).to_be_visible()
    expect(p.locator('.matrix tbody tr')).to_have_count(7)
    p.screenshot(path='artifacts/performance.png',full_page=True)
    p.get_by_role('link',name='Error analysis',exact=True).click()
    expect(p.get_by_role('heading',name='Error analysis',exact=True)).to_be_visible()
    p.get_by_role('button',name=__import__('re').compile('High confidence errors')).click()
    p.get_by_role('combobox',name='Group errors by').select_option('language')
    expect(p.get_by_role('heading',name='High confidence errors ≥98%',exact=True)).to_be_visible()


def test_05_invalid_search_and_class_filter(browser_app):
    from playwright.sync_api import expect
    a=browser_app;p=a['page'];p.get_by_role('link',name='Notice explorer',exact=True).click()
    p.get_by_role('searchbox',name='Search notices').fill('<script>alert(1)</script>')
    expect(p.get_by_text('No matching notices',exact=True)).to_be_visible()
    p.get_by_role('button',name='Reset',exact=True).click()
    p.get_by_role('combobox',name='All classifications',exact=True).select_option('NOT_VOTABLE')
    expect(p.locator('tbody tr').first).to_be_visible()
    assert all('Not votable' in x for x in p.locator('tbody tr').all_inner_texts())
    assert not a['errors']


def test_06_export_and_demo(browser_app):
    from playwright.sync_api import expect
    a=browser_app;p=a['page']
    with p.expect_download() as event:p.get_by_role('link',name='Export results',exact=True).click()
    download=event.value;assert download.suggested_filename=='laya-results.jsonl'
    p.get_by_role('checkbox',name='Demo mode').check();p.reload();expect(p.get_by_role('checkbox',name='Demo mode')).to_be_checked()
    p.get_by_role('link',name='Model runs & audit',exact=True).click();expect(p.get_by_role('heading',name='Model runs & audit',exact=True)).to_be_visible()
    p.get_by_role('link',name='Dataset & methodology',exact=True).click();expect(p.get_by_role('heading',name='Dataset & methodology',exact=True)).to_be_visible()
    p.screenshot(path='artifacts/methodology.png',full_page=True)


def test_07_batch_and_reproduction(browser_app):
    from playwright.sync_api import expect
    a=browser_app;p=a['page'];p.get_by_role('link',name='Model runs & audit',exact=True).click()
    expect(p.get_by_role('button',name='Run Laya baseline',exact=True)).to_be_visible()
    p.get_by_role('button',name='Run Laya baseline',exact=True).click()
    def completed():
        rows=p.request.get(a['url']+'/api/runs').json()
        return next((r for r in rows if r['model'].startswith('test-double-not-laya') and r['status']=='COMPLETED'),None)
    run=None
    for i in range(150):
        run=completed()
        if run:break
        time.sleep(.2)
    assert run and run['persisted']==a['total']
    p.reload();expect(p.get_by_role('heading',name='Model runs & audit',exact=True)).to_be_visible()
    p.locator('[data-reproduce="'+run['id']+'"]').click()
    reproduced=None
    for i in range(150):
        rows=p.request.get(a['url']+'/api/runs').json()
        reproduced=next((r for r in rows if r['manifest'].get('reproduces')==run['id'] and r['status']=='COMPLETED'),None)
        if reproduced:break
        time.sleep(.2)
    assert reproduced and reproduced['dataset_hash']==run['dataset_hash']
    assert reproduced['config_version']==run['config_version']
    assert reproduced['persisted']==a['total']


def test_08_restart_persistence(browser_app):
    a=browser_app
    a['process'][0].terminate();a['process'][0].wait(timeout=10)
    process=a['start']();browser_app['process'][0]=process
    with urllib.request.urlopen(a['url']+'/api/notice?id='+urllib.parse.quote(a['record'])) as response:d=json.load(response)
    assert d['review']['reviewer'].startswith('Automated E2E')


def test_09_research_evidence_and_error_explorer(browser_app):
    from playwright.sync_api import expect
    a=browser_app;p=a['page'];p.goto(a['url']+'/#performance')
    expect(p.get_by_role('heading',name='Supervised Laya experiment',exact=True)).to_be_visible()
    expect(p.get_by_text('QUALITY GATE NOT MET',exact=True)).to_be_visible()
    p.get_by_role('button',name='Errors',exact=True).last.click()
    expect(p.get_by_role('heading',name='Fine-Tuned Model → Errors',exact=True)).to_be_visible()
    errors=p.request.get(a['url']+'/api/experiment/errors?model=fine-tuned&dataset=challenge').json()['items']
    evidence=p.request.get(a['url']+'/api/experiment').json()
    if evidence['comparison'][1]['challenge_passed'] is not None:
        assert len(errors)==57-evidence['comparison'][1]['challenge_passed']
    p.get_by_role('button',name='High Confidence Wrong ≥98%',exact=True).click()
    high_count=sum(r['confidence']>=.98 for r in errors)
    expect(p.get_by_role('heading',name=f'{high_count} challenge failures',exact=True)).to_be_visible()
    if high_count:p.locator('details').first.locator('summary').click()
    p.screenshot(path='artifacts/research-errors.png',full_page=True)
    p.get_by_role('button',name='Show all',exact=True).click()
    p.get_by_role('combobox',name='Evaluation corpus').select_option('test')
    p.get_by_role('combobox',name='Evaluation corpus').select_option('challenge')
    p.get_by_role('combobox',name='Failed factor').select_option('poa_required')
    p.get_by_role('combobox',name='Expected synthetic result').select_option('YES')
    p.get_by_role('button',name='High Confidence Wrong ≥98%',exact=True).click()
    p.get_by_role('combobox',name='Experiment model').select_option('base')
    p.get_by_role('button',name='Public reviewed errors',exact=True).click()
    expect(p.get_by_role('heading',name='Error analysis',exact=True)).to_be_visible()
    assert not a['errors']


def test_10_evidence_links_highlight_exact_unicode_and_keep_context(browser_app):
    """Explicit browser-only fixture: never inserts invented data in the real corpus."""
    from playwright.sync_api import expect
    from apps.api.decision_evidence import decision_evidence,VERSION
    from classifier.preprocessing import source_hash
    from classifier.laya_classifier import load_config,LayaClassifier
    from tests.conftest import ContractAgent
    a=browser_app;p=a['page']
    payload=p.request.get(a['url']+'/api/notice?id='+urllib.parse.quote(a['record'])).json()
    text='🔎 Café. Registration is not required.\n<script>window.evidenceInjected=true</script>'
    payload.update(id='synthetic-browser-evidence-fixture',text=text,source_hash=source_hash(text),history=[],review=None,blind_review=False)
    payload['metadata'].update(issuer='Synthetic evidence browser fixture',event_type='Synthetic source fixture')
    payload['prediction']=LayaClassifier(load_config(),agent=ContractAgent()).classify(text).model_dump(mode='json')
    payload['decision_evidence']=decision_evidence(text,payload['metadata'],payload['prediction'],payload['evaluation_date'])
    payload['decision_evidence_version']=VERSION
    pattern='**/api/notice?*'
    p.route(pattern,lambda route:route.fulfill(json=payload))
    try:
        p.goto(a['url']+'/#explorer')
        expect(p.get_by_role('heading',name='Notice explorer',exact=True)).to_be_visible()
        p.locator('tr[data-record]').first.click()
        expect(p.get_by_role('heading',name='Synthetic evidence browser fixture',exact=True)).to_be_visible()
        p.get_by_role('link',name='View source passage',exact=True).click()
        expect(p.locator('#source-evidence-highlight')).to_have_text('Registration is not required.')
        assert p.locator('.source-text').text_content()==text
        assert p.evaluate('window.evidenceInjected') is None
        p.get_by_role('link',name='View source field',exact=True).click()
        expect(p.locator('#evidence-metadata-event_type')).to_be_visible()
        p.get_by_role('link',name='View model scores and criteria',exact=True).first.click()
        expect(p.locator('#evidence-factor-votable')).to_be_visible()
        assert p.url.endswith('#explorer') and p.locator('#notice-dialog').evaluate('(e)=>e.open')
        p.screenshot(path='artifacts/evidence-links.png',full_page=True)
    finally:
        p.unroute(pattern)


def test_11_hybrid_source_routing_and_evidence(browser_app):
    from playwright.sync_api import expect
    a=browser_app;p=a['page']
    if p.locator('#notice-dialog').evaluate('(el)=>el.open'):p.locator('#close-dialog').click()
    p.goto(a['url']+'/#performance')
    expect(p.get_by_role('heading',name='Hybrid architecture experiment',exact=True)).to_be_visible()
    p.get_by_role('button',name='Inspect clearstream-dscl-excerpt',exact=True).click()
    expect(p.get_by_role('heading',name='ISO15022 provenance example',exact=True)).to_be_visible()
    expect(p.locator('#notice-content')).to_contain_text('OFFICIAL_EXAMPLE')
    link=p.locator('[data-evidence-link="source"]').first;link.click()
    expect(p.locator('#source-evidence-highlight')).to_be_visible()
    assert ':20C::CORP//810651611' in p.locator('#source-evidence-highlight').inner_text()
    p.get_by_text('Field routing trace · unknown fields preserved',exact=True).click()
    expect(p.locator('#notice-content')).to_contain_text('UNKNOWN_FIELDS')
    p.screenshot(path='artifacts/iso-provenance.png',full_page=True)
    p.locator('#close-dialog').click()
    assert not a['errors']


def test_12_hybrid_errors_and_event_history(browser_app):
    from playwright.sync_api import expect
    a=browser_app;p=a['page'];p.goto(a['url']+'/#performance')
    expect(p.get_by_role('heading',name='Hybrid architecture experiment',exact=True)).to_be_visible()
    p.get_by_role('button',name='Fine-tuned narrow Laya → Errors',exact=True).click()
    expect(p.get_by_role('heading',name='Narrow Laya · Error explorer',exact=True)).to_be_visible()
    p.locator('#hybrid-errors-high').check()
    expect(p.locator('#notice-content')).to_contain_text('failures')
    p.locator('#hybrid-errors-search').fill('poa_required')
    p.screenshot(path='artifacts/iso-high-confidence-errors.png',full_page=True)
    p.locator('#close-dialog').click()
    if p.locator('#inspect-event-history').count():
        p.locator('#inspect-event-history').click()
        expect(p.get_by_role('heading',name='Event history · synthetic example',exact=True)).to_be_visible()
        expect(p.locator('#notice-content')).to_contain_text('2026-10-15')
        expect(p.locator('#notice-content')).to_contain_text('2026-10-18')
        expect(p.locator('#notice-content')).to_contain_text('Superseded')
        expect(p.locator('#notice-content')).to_contain_text('Current')
        p.locator('#close-dialog').click()
    assert not a['errors']


def test_13_local_llm_experiment_separates_metrics(browser_app):
    from playwright.sync_api import expect
    a=browser_app;p=a['page'];p.goto(a['url']+'/#performance')
    expect(p.get_by_role('heading',name='Controlled A–E local model experiment',exact=True)).to_be_visible()
    expect(p.get_by_text('Quality gate not met · automation disabled.',exact=True)).to_be_visible()
    expect(p.get_by_text('NOT BLIND / DEVELOPMENT ONLY',exact=True)).to_be_visible()
    expect(p.get_by_role('button',name='Errors & stage provenance',exact=True)).to_be_visible()
    response=p.request.get(a['url']+'/api/semantic/experiment').json()
    assert response['customer_accuracy'] is None
    assert not response['automation_enabled']
    p.screenshot(path='artifacts/local-llm-experiment.png',full_page=True)


def test_14_local_llm_stage_provenance_and_evidence(browser_app):
    from playwright.sync_api import expect
    a=browser_app;p=a['page'];p.goto(a['url']+'/#performance')
    expect(p.get_by_role('button',name='Errors & stage provenance',exact=True)).to_be_visible()
    p.locator('#semantic-arm').select_option('D')
    p.get_by_role('button',name='Errors & stage provenance',exact=True).click()
    expect(p.get_by_role('heading',name='Architecture D · Errors & provenance',exact=True)).to_be_visible()
    p.locator('#semantic-errors-only').uncheck()
    # Run after evaluation: these rows contain actual model results, never injected LLM output.
    expect(p.locator('[data-semantic-record]').first).to_be_visible(timeout=10000)
    p.locator('[data-semantic-record]').first.click()
    expect(p.get_by_role('heading',name='Local LLM',exact=True)).to_be_visible()
    assert 'Invoked: YES' in p.locator('#notice-content').inner_text()
    source=p.locator('.source-text').inner_text()
    for link in p.locator('.evidence-link[data-start]').all():
        start=int(link.get_attribute('data-start'));end=int(link.get_attribute('data-end'))
        assert 0<=start<end<=len(source)
        if link.inner_text().startswith('“'):assert source[start:end]==link.inner_text().strip('“”')
    p.screenshot(path='artifacts/local-llm-provenance.png',full_page=True)
    assert not a['errors']


def test_15_complete_synthetic_metrics_and_exact_structured_evidence(browser_app):
    from playwright.sync_api import expect
    a=browser_app;p=a['page']
    if p.locator('#notice-dialog').count() and p.locator('#notice-dialog').evaluate('(el)=>el.open'):p.locator('#close-dialog').click()
    p.goto(a['url']+'/#performance')
    expect(p.get_by_role('button',name='Field metrics & confusion matrices',exact=True)).to_be_visible()
    p.locator('#semantic-dataset').select_option('complete');p.locator('#semantic-arm').select_option('E')
    p.get_by_role('button',name='Field metrics & confusion matrices',exact=True).click()
    expect(p.get_by_role('heading',name='Architecture E · Field metrics',exact=True)).to_be_visible()
    p.locator('#semantic-metric-field').select_option('share_blocking')
    expect(p.get_by_role('heading',name='Confusion matrix · exact counts',exact=True)).to_be_visible()
    expect(p.locator('#notice-content')).to_contain_text('48 labelled assertions')
    assert p.locator('#notice-content .matrix tbody tr').count()>=2
    p.locator('#close-dialog').click();p.get_by_role('button',name='Errors & stage provenance',exact=True).click()
    p.locator('#semantic-errors-only').uncheck()
    expect(p.locator('[data-semantic-record="COMPLETE-041"]')).to_be_visible()
    p.locator('[data-semantic-record="COMPLETE-041"]').click()
    expect(p.get_by_role('heading',name='Parsed structure · exact source fields',exact=True)).to_be_visible()
    p.get_by_role('link',name='Controlling RDDT field',exact=True).click()
    expect(p.locator('#source-evidence-highlight')).to_contain_text(':98E::RDDT//20261124170000/0000')
    p.screenshot(path='artifacts/local-llm-structured-provenance.png',full_page=True)
    assert not a['errors']


def test_16_unverified_model_quotations_never_render(browser_app):
    """Browser-only hostile-output fixture; never changes saved model results."""
    from playwright.sync_api import expect
    a=browser_app;p=a['page']
    if p.locator('#notice-dialog').evaluate('(el)=>el.open'):p.locator('#close-dialog').click()
    row=p.request.get(a['url']+'/api/semantic/record?id=agm&dataset=challenge&architecture=D').json()
    llm=row['result']['llm']
    llm['parsed']['evidence']['share_blocking']=['FABRICATED-QUOTE-NOT-IN-SOURCE']
    llm['evidence_validation']['predicates']['share_blocking']=[{'valid':False,'reason':'Not an exact substring'}]
    llm['parsed']['deadline_information']['deadline_text']='FABRICATED-DEADLINE-NOT-IN-SOURCE'
    llm['evidence_validation']['deadline']={'valid':False,'reason':'Not an exact substring'}
    pattern='**/api/semantic/record?*';p.route(pattern,lambda route:route.fulfill(json=row))
    try:
        p.goto(a['url']+'/#performance')
        p.locator('#semantic-dataset').select_option('challenge');p.locator('#semantic-arm').select_option('D')
        p.get_by_role('button',name='Errors & stage provenance',exact=True).click()
        p.locator('#semantic-errors-only').uncheck()
        expect(p.locator('[data-semantic-record]').first).to_be_visible()
        p.locator('[data-semantic-record]').first.click()
        expect(p.get_by_role('heading',name='Local LLM',exact=True)).to_be_visible()
        text=p.locator('#notice-content').text_content()
        assert 'FABRICATED-QUOTE' not in text;assert 'FABRICATED-DEADLINE' not in text
        assert not a['errors']
    finally:p.unroute(pattern)


def test_17_model_lab_side_by_side_and_recorded_llm_usage(browser_app):
    from playwright.sync_api import expect
    a=browser_app;p=a['page']
    if p.locator('#notice-dialog').evaluate('(e)=>e.open'):p.get_by_role('button',name='Close notice').click()
    p.goto(a['url']+'/#model_lab')
    expect(p.get_by_role('heading',name='Model Lab',exact=True)).to_be_visible()
    expect(p.locator('#lab-prediction-table')).to_be_visible()
    headers=p.locator('#lab-prediction-table thead').inner_text()
    assert all(x in headers for x in ['A','B','C','D','E'])
    expect(p.get_by_role('heading',name='LLM usage · measured experiment')).to_be_visible()
    p.locator('#lab-case').select_option(index=1)
    expect(p.locator('#lab-comparison .source-text')).not_to_be_empty()
    p.locator('#lab-errors-only').check()
    p.screenshot(path='artifacts/model-lab-smoke.png',full_page=True)
    assert not a['errors'],a['errors']


def test_18_notice_configured_analysis_trace_persists_after_refresh(browser_app):
    from playwright.sync_api import expect
    a=browser_app;p=a['page'];p.goto(a['url']+'/#explorer')
    # Existing browser fixture record has a persisted legacy result; new execution stays separate.
    p.locator('#search').fill(a['record'])
    expect(p.locator('tbody tr[data-record]')).to_have_count(1)
    p.locator('tbody tr[data-record]').click()
    expect(p.get_by_role('button',name='Analyse notice with configured architecture')).to_be_visible()
    p.get_by_role('button',name='Analyse notice with configured architecture').click()
    expect(p.locator('#persisted-decision-trace')).to_have_attribute('open','',timeout=15000)
    expect(p.locator('#persisted-decision-trace')).to_contain_text('Architecture E')
    expect(p.locator('#persisted-decision-trace')).to_contain_text('Manual review: YES')
    record_id=p.locator('#analyse-configured-notice').get_attribute('data-record-id')
    before=p.request.get(a['url']+'/api/notice?id='+record_id).json()['semantic_execution']
    assert before['result']['laya']['checkpoint']=='TEST_DOUBLE'
    p.reload();p.locator('#search').fill(record_id)
    expect(p.locator('tbody tr[data-record]')).to_have_count(1)
    expect(p.locator('tbody tr[data-record]')).to_have_attribute('data-record',record_id)
    p.locator('tbody tr[data-record]').click()
    p.locator('#persisted-decision-trace summary').first.click()
    expect(p.locator('#persisted-decision-trace')).to_contain_text(before['run_id'])
    p.screenshot(path='artifacts/persisted-decision-trace-smoke.png',full_page=True)
    assert p.request.get(a['url']+'/api/notice?id='+record_id).json()['semantic_execution']==before
    assert not a['errors'],a['errors']


def test_19_phase_v2_separates_pending_study_from_historical_results(browser_app):
    from playwright.sync_api import expect
    a=browser_app;p=a['page']
    if p.locator('#notice-dialog').evaluate('(e)=>e.open'):p.get_by_role('button',name='Close notice').click()
    p.goto(a['url']+'/#model_lab')
    expect(p.get_by_role('heading',name='Aggregation & selective cascade · v2',exact=True)).to_be_visible()
    expect(p.get_by_text('Automation disabled. Customer accuracy unknown.',exact=False)).to_be_visible()
    expect(p.get_by_role('heading',name='Same source · same truth · five architectures',exact=True)).to_be_visible()
    r=p.request.get(a['url']+'/api/cascade/experiment').json()
    assert r['customer_accuracy'] is None;assert not r['automation_enabled']
    assert r['aggregation']['before_yes']==0;assert r['aggregation']['after_yes']==11
    p.screenshot(path='artifacts/cascade-v2-model-lab.png',full_page=True)
    assert not a['errors'],a['errors']


def test_20_domain_confidence_is_explicitly_not_customer_accuracy(browser_app):
    from playwright.sync_api import expect
    a=browser_app;p=a['page']
    p.goto(a['url']+'/#confidence')
    expect(p.get_by_role('heading',name='Confidence & Automation',exact=True)).to_be_visible()
    expect(p.get_by_text('AUTOMATION DISABLED · Customer accuracy UNKNOWN.',exact=True)).to_be_visible()
    expect(p.get_by_role('heading',name='Protected synthetic corpus',exact=True)).to_be_visible()
    response=p.request.get(a['url']+'/api/domain/status').json()
    assert response['customer_accuracy'] is None and response['confidence'] is None and not response['automation_enabled']
    p.screenshot(path='artifacts/domain-confidence-smoke.png',full_page=True)
    assert not a['errors'],a['errors']


def test_21_complete_predicate_review_persists_without_changing_legacy_label(browser_app):
    from playwright.sync_api import expect
    a=browser_app;p=a['page'];p.goto(a['url']+'/#explorer')
    p.locator('#search').fill(a['record']);expect(p.locator('tbody tr[data-record]')).to_have_count(1)
    record=p.locator('tbody tr[data-record]').get_attribute('data-record')
    legacy=p.request.get(a['url']+'/api/notice?id='+record).json()['review']
    p.locator('tbody tr[data-record]').click()
    p.locator('#domain-review-panel summary').click()
    expect(p.locator('#domain-review-revision')).to_have_text('No complete predicate label saved.')
    form=p.locator('#domain-review-form');form.locator('[name=reviewer]').fill('Browser domain reviewer')
    form.locator('[name=votability]').select_option('VOTABLE');form.locator('[name=poa_required]').select_option('YES')
    form.get_by_role('button',name='Save complete predicate review',exact=True).click()
    expect(p.locator('#domain-review-revision')).to_contain_text('saved')
    p.reload();p.locator('#search').fill(record);expect(p.locator('tbody tr[data-record]')).to_have_count(1);p.locator('tbody tr[data-record]').click()
    p.locator('#domain-review-panel summary').click()
    expect(p.locator('#domain-review-form [name=poa_required]')).to_have_value('YES')
    history=p.request.get(a['url']+'/api/domain/reviews/'+record).json()['items'];assert len(history)==1
    assert p.request.get(a['url']+'/api/notice?id='+record).json()['review']==legacy
    p.screenshot(path='artifacts/domain-full-review-smoke.png',full_page=True)
    assert not a['errors'],a['errors']


def test_22_laya_first_panel_shows_pending_and_no_customer_claim(browser_app):
    from playwright.sync_api import expect
    a=browser_app;p=a['page'];p.goto(a['url']+'/#model_lab')
    expect(p.get_by_role('heading',name='Laya-first cascade · measured experiment',exact=True)).to_be_visible()
    expect(p.get_by_text('Raw scores and token probabilities are not calibrated confidence.',exact=False)).to_be_visible()
    d=p.request.get(a['url']+'/api/fast-cascade/status').json()
    assert d['automation_enabled'] is False and d['customer_accuracy'] is None
    assert p.request.post(a['url']+'/api/fast-cascade/analyse',data={'record_id':a['record']}).status==403
    p.screenshot(path='artifacts/laya-first-model-lab.png',full_page=True)


def test_23_notice_renders_persisted_cascade_and_refresh_keeps_it(browser_app):
    from playwright.sync_api import expect
    from apps.api.fast_cascade_views import tables
    from fast_cascade.pipeline import Pipeline
    from fast_cascade.routing import Policy
    from fast_cascade.protocol import digest
    from semantic_pipeline.schema import PREDICATES
    from semantic_pipeline.evidence import verify_evidence
    a=browser_app;p=a['page']
    with sqlite3.connect(a['db']) as c:
        text=c.execute('SELECT text FROM notices WHERE id=?',(a['record'],)).fetchone()[0]
        preds={k:{'value':'VOTABLE' if k=='votability' else 'NO','scores':{'YES':.999 if k=='votability' else .0005,'NO':.0005 if k=='votability' else .999,'UNKNOWN':.0005},'evidence':[verify_evidence(text,text[:80])],'source':'BROWSER_CONTRACT_FIXTURE_NOT_A_MODEL'} for k in PREDICATES}
        raw={'predicates':preds,'input_hash':digest(text),'latency_ms':1.}
        result=Pipeline(Policy()).analyse(text,precomputed_laya=raw)
        tables(c);c.execute('INSERT INTO fast_cascade_executions VALUES(?,?,?,?,?)',('browser-cascade-contract',a['record'],digest(text),'2026-10-17T12:00:00+00:00',json.dumps(result)));c.commit()
    if p.locator('#notice-dialog').evaluate('(el)=>el.open'):p.get_by_role('button',name='Close notice').click()
    p.goto(a['url']+'/#explorer')
    p.get_by_role('searchbox',name='Search notices').fill(a['record'])
    expect(p.locator('tbody tr')).to_have_count(1)
    p.locator('tr[data-record]').first.click()
    expect(p.locator('#fast-cascade-trace')).to_be_visible()
    p.locator('#fast-cascade-trace summary').first.click()
    expect(p.locator('#fast-cascade-trace')).to_contain_text('browser-cascade-contract')
    expect(p.locator('#fast-cascade-trace')).to_contain_text('NOT INVOKED')
    expect(p.locator('#fast-cascade-trace')).to_contain_text('HEURISTIC / NOT YET CALIBRATED')
    d=p.request.get(a['url']+'/api/notice?id='+a['record']).json()
    assert d['fast_cascade_execution']['id']=='browser-cascade-contract'
    p.screenshot(path='artifacts/laya-first-persisted-trace.png',full_page=True)
    p.reload()
    assert p.request.get(a['url']+'/api/notice?id='+a['record']).json()['fast_cascade_execution']['id']=='browser-cascade-contract'

def test_24_training_framework_and_ai_review_provenance(browser_app):
    from playwright.sync_api import expect
    a = browser_app; p = a['page']
    p.goto(a['url'] + '/#model_lab')
    expect(p.get_by_role('heading', name='Training framework · Laya + local LLM', exact=True)).to_be_visible()
    expect(p.locator('#training-framework-panel')).to_contain_text('AI-authored and AI-reviewed labels')
    p.get_by_role('link', name='Notice explorer', exact=True).click()
    p.get_by_role('searchbox', name='Search notices').fill(a['record'])
    expect(p.locator('tbody tr')).to_have_count(1)
    p.locator('tbody tr').click()
    p.locator('#domain-review-panel summary').click()
    form = p.locator('#domain-review-form')
    expect(p.locator('#domain-review-revision')).not_to_contain_text('Loading')
    form.locator('[name=reviewer]').fill('AI workflow test — isolated database')
    form.locator('[name=label_origin]').select_option('AI_REVIEWED')
    form.locator('[name=reviewer_model]').fill('browser-contract-only-not-a-real-annotation-model')
    form.locator('[name=domain_expert_attested]').uncheck()
    form.get_by_role('button', name='Save complete predicate review', exact=True).click()
    expect(p.locator('#domain-review-revision')).to_contain_text('saved')
    last = p.request.get(a['url'] + '/api/domain/reviews/' + a['record']).json()['items'][-1]
    assert last['context']['label_origin'] == 'AI_REVIEWED'
    assert last['context']['validation_type'] == 'AI_ASSISTED_NOT_HUMAN_GOLD'
    assert not last['context']['domain_expert_attested']
    p.get_by_role('button', name='Close notice').click()


def test_25_registered_candidate_trace_persists_in_notice_detail(browser_app):
    from playwright.sync_api import expect
    from apps.api.training_views import execution_tables
    from classifier.preprocessing import source_hash
    from semantic_pipeline.schema import PREDICATES
    from semantic_pipeline.decision import decide
    a=browser_app;p=a['page']
    with sqlite3.connect(a['db']) as c:
        text=c.execute('SELECT text FROM notices WHERE id=?',(a['record'],)).fetchone()[0]
        f={k:{'value':'NOT_VOTABLE' if k=='votability' else 'NO','source':'BROWSER_CONTRACT_ONLY',
              'evidence':[],'confidence':None} for k in PREDICATES}
        result={'architecture':'REGISTERED_QWEN','input_type':'UNSTRUCTURED_NOTICE','parser':None,
                'reconciliation':{'predicates':f,'conflicts':[]},'decision':decide(f,{'status':'UNKNOWN'}),
                'deadline':{'status':'UNKNOWN'},'checkpoint_manifest_sha256':'browser-contract-only'}
        execution_tables(c)
        c.execute('INSERT INTO framework_executions VALUES(?,?,?,?,?,?,?)',('browser-trained-contract',a['record'],source_hash(text),text,
                  '2026-10-17T18:00:00+00:00','browser-contract-job',json.dumps(result)));c.commit()
    p.goto(a['url']+'/#explorer');p.get_by_role('searchbox',name='Search notices').fill(a['record'])
    expect(p.locator('tbody tr')).to_have_count(1);p.locator('tbody tr').click()
    trace=p.locator('.framework-decision-trace');trace.locator('summary').click()
    expect(trace).to_contain_text('browser-trained-contract')
    expect(trace).to_contain_text('Calibrated confidence unavailable')
    expect(trace).to_contain_text('Review required')
    p.screenshot(path='artifacts/registered-candidate-trace.png',full_page=True)
    p.reload()
    saved=p.request.get(a['url']+'/api/notice?id='+a['record']).json()['framework_execution']
    assert saved['id']=='browser-trained-contract'


def test_26_event_review_train_compare_select_rollback(browser_app):
    """Real browser/API/SQLite; server explicitly doubles ONLY model execution."""
    from playwright.sync_api import expect
    from scripts.build_event_learning_corpus import message
    from semantic_pipeline.schema import PREDICATES
    a=browser_app;p=a['page'];p.goto(a['url']+'/#model_lab')
    expect(p.get_by_role('heading',name='Event learning loop',exact=True)).to_be_visible()
    ids=[]
    for name,role,text,vote in [('TRAIN','TRAIN','Shareholders can vote. No share blocking is required.','VOTABLE'),
                                ('VALID','VALIDATION','This treasury advice reports only a distribution; there is no voting opportunity.','NOT_VOTABLE')]:
        form=p.locator('#learning-import-form');form.locator('xpath=..').evaluate('(el)=>el.open=true')
        payload={'raw':message('BROWSER'+name,'BROWSER'+name,'NEWM',text,voting=vote=='VOTABLE'),
                 'sender':'BROWSER-CONTRACT','source_type':'STANDARDS_DERIVED_SYNTHETIC','source_reference':'Isolated browser fixture',
                 'group_id':'browser-family-'+name,'family':'browser-family-'+name,'split':role}
        form.locator('[name=payload]').fill(json.dumps(payload));form.get_by_role('button').click()
        expect(p.locator('#learning-event-detail')).to_contain_text('BROWSER'+name)
        target={k:vote if k=='votability' else 'NO' for k in PREDICATES}
        target.update(evidence={k:['Shareholders can vote.'] if k=='votability' and vote=='VOTABLE' else [] for k in PREDICATES},
                      deadline_information={'deadline_mentioned':False,'deadline_text':None},ambiguities=[])
        review=p.locator('#learning-review-form');review.locator('[name=target]').fill(json.dumps(target))
        review.locator('[name=model_id]').fill('EXPLICIT_BROWSER_ANNOTATION_DOUBLE')
        review.get_by_role('button',name='Save event review revision').click()
        expect(p.locator('#learning-review-history')).to_contain_text('AI_REVIEWED')
        rows=p.request.get(a['url']+'/api/learning/status').json()['events'];ids.append(next(v['id'] for v in rows if v['corp']=='BROWSER'+name))
    export=p.locator('#learning-export-form');export.locator('xpath=..').evaluate('(el)=>el.open=true')
    export.locator('[name=id]').fill('browser-event-reviews');export.get_by_role('button',name='Export TRAIN / VALIDATION bundle',exact=True).click()
    expect(p.locator('#learning-feedback')).to_contain_text('VERSIONED_EVENT_REVIEWS')
    export.locator('[name=id]').fill('browser-event-dataset');export.get_by_role('button',name='Freeze all reviewed role assignments').click()
    expect(p.locator('#learning-feedback')).to_contain_text('event-dataset-v1')
    p.reload();expect(p.locator('#event-learning-panel')).to_be_visible()
    prepared=[]
    for _ in range(2):
        form=p.locator('#learning-prepare-form');form.locator('xpath=..').evaluate('(el)=>el.open=true')
        form.locator('[name=bundle_id]').select_option('browser-event-reviews')
        spec={'backend':'LAYA_SDK','family':'LAYA','model_path':str(Path(a['db']).parent/'framework/contract-base'),
              'base_model_id':'EXPLICIT_BROWSER_CONTRACT_DOUBLE','base_revision':'no-real-training'}
        form.locator('[name=spec]').fill(json.dumps(spec))
        with p.expect_response(lambda r:r.url.endswith('/api/training/jobs') and r.request.method=='POST') as response:
            form.get_by_role('button',name='Prepare immutable plan').click()
        prepared.append(response.value.json()['id'])
    p.reload();expect(p.locator('#event-learning-panel')).to_be_visible()
    for ident in prepared:
        with p.expect_response(lambda r:r.url.endswith(f'/api/learning/jobs/{ident}/enqueue')) as queued:
            p.locator(f'[data-learning-enqueue="{ident}"]').click()
        assert queued.value.json()['state']=='QUEUED'
    p.locator('#learning-dispatch').click()
    expect(p.locator('#learning-feedback')).to_contain_text('EXPLICIT_SYNCHRONOUS_BROWSER_DOUBLE')
    tasks=p.request.get(a['url']+'/api/learning/status').json()['tasks']
    assert all(t['state']=='COMPLETED' for t in tasks if t['job_id'] in prepared)
    p.reload();expect(p.locator('#event-learning-panel')).to_be_visible()
    form=p.locator('#learning-comparison-form');form.locator('xpath=..').evaluate('(el)=>el.open=true')
    form.locator('[name=dataset_id]').select_option('browser-event-dataset')
    form.locator('[name=first]').select_option(prepared[0]);form.locator('[name=second]').select_option(prepared[1])
    form.get_by_role('button',name='Run local same-input comparison').click()
    expect(p.locator('#learning-comparison')).to_contain_text('All-nine exact match')
    choose=p.locator('#learning-selection-form');choose.locator('xpath=..').evaluate('(el)=>el.open=true')
    choose.locator('[name=actor]').fill('Browser workflow double');choose.locator('[name=reason]').fill('Contract validation, no model-quality claim')
    selections=[]
    for ident in prepared:
        choose.locator('[name=job_id]').select_option(ident);choose.get_by_role('button',name='Select experimental checkpoint').click()
        expect(p.locator('#learning-feedback')).to_contain_text(ident)
        selections.append(p.request.get(a['url']+'/api/learning/status').json()['selections'][-1])
    p.locator('#learning-event-id').select_option(ids[0]);expect(p.locator('#learning-event-detail')).to_contain_text('BROWSERTRAIN')
    p.locator('#learning-analyse').click();expect(p.locator('#learning-event-executions')).to_contain_text('persisted decision trace')
    p.locator('#learning-event-executions details').first.evaluate('(el)=>el.open=true')
    expect(p.locator('#learning-event-executions')).to_contain_text('Calibrated confidence unavailable')
    source_link=p.locator('#learning-event-executions [data-learning-source]').first
    source_id=source_link.get_attribute('data-learning-source');source_link.click()
    expect(p.locator('#learning-message-'+source_id+' pre')).to_be_visible()
    assert p.url.endswith('#model_lab')
    p.reload();expect(p.locator('#event-learning-panel')).to_be_visible()
    p.locator(f'[data-learning-rollback="{selections[0]["id"]}"]').evaluate('(el)=>el.closest("details").open=true')
    p.locator(f'[data-learning-rollback="{selections[0]["id"]}"]').click()
    expect(p.locator('#learning-feedback')).to_contain_text('ROLLBACK')
    history=p.request.get(a['url']+'/api/learning/status').json()['selections']
    assert history[-1]['job_id']==prepared[0] and history[-1]['action']=='ROLLBACK'
    p.locator('#learning-event-id').select_option(ids[0]);expect(p.locator('#learning-review-history')).to_contain_text('AI_REVIEWED')
    p.screenshot(path='artifacts/event-learning-workflow.png',full_page=True)
    assert not a['errors']
