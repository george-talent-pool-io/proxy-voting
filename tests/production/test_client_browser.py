"""Actual customer browser path; source/labels are controlled AI fixtures."""
import json
import os
from pathlib import Path
import socket
import subprocess
import sys
import time
import urllib.request
from dataclasses import dataclass
import pytest
from production.security import password_record
from tests.production.test_client_workflow import row, PASSWORD

pytestmark = pytest.mark.e2e


@dataclass
class BrowserWorkspace:
    page: object
    url: str
    tmp: Path
    errors: list
    restart: object

    def __iter__(self):
        return iter((self.page, self.url, self.tmp, self.errors))


@pytest.fixture(scope='module')
def customer_browser(tmp_path_factory):
    from playwright.sync_api import sync_playwright
    tmp = tmp_path_factory.mktemp('client-browser')
    secret = tmp / 'users.json'
    secret.write_text(json.dumps({'operator': {'roles': ['ADMIN', 'TRAINER', 'REVIEWER'],
                                             'expert_attested': False, 'password': password_record(PASSWORD)},
                                 'auditor': {'roles':['AUDITOR'],'expert_attested':False,
                                             'password':password_record(PASSWORD)}}))
    with socket.socket() as s: s.bind(('127.0.0.1', 0)); port = s.getsockname()[1]
    url = f'http://127.0.0.1:{port}'
    env = {**os.environ, 'VOTING_DB': str(tmp / 'db.sqlite'), 'VOTING_TRAINING_WORKSPACE': str(tmp / 'workspace'),
           'VOTING_USERS_FILE': str(secret), 'VOTING_PUBLIC_ORIGIN': url, 'VOTING_ALLOW_LOCAL_HTTP': 'true',
           'AUTOMATION_ENABLED': 'false', 'TRAINING_EXECUTION_ENABLED': 'true',
           'VOTING_BROWSER_CONTRACT':'ISOLATED_TEST_ONLY', 'VOTING_MODELS_ROOT':str(tmp/'models')}
    def start():
        with (tmp / 'api.log').open('a') as log:
            child = subprocess.Popen([sys.executable, '-m', 'uvicorn', 'tests.e2e.customer_server:app', '--host', '127.0.0.1', '--port', str(port)], env=env, stdout=log, stderr=log)
        for _ in range(150):
            try: urllib.request.urlopen(url + '/health/live', timeout=1); return child
            except OSError: time.sleep(.1)
        child.terminate();child.wait(timeout=15)
        raise RuntimeError((tmp/'api.log').read_text())
    p = start()
    def restart():
        nonlocal p
        p.terminate();p.wait(timeout=15);p=start()
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
            yield BrowserWorkspace(page,url,tmp,errors,restart)
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


def post_from_ui(page, path, button):
    with page.expect_response(lambda r: path in r.url and r.request.method == 'POST') as received:
        page.locator(button).click()
    response = received.value
    from playwright.sync_api import expect
    expect(page.locator('body')).to_have_attribute('aria-busy','false')
    assert response.ok, response.text()
    return response.json()


def open_event(page, corp):
    from playwright.sync_api import expect
    page.locator('#events').get_by_role('button', name=corp, exact=True).click()
    # The old review form remains visible while the next event loads. Wait
    # for its identity, not merely for a form that could belong to another row.
    expect(page.locator('#event > h3').first).to_contain_text(corp)


def test_customer_qualification_journey_uses_production_http_and_persists_restart(customer_browser):
    """Expensive model kernels are doubles; every customer workflow stage is real."""
    from semantic_pipeline.schema import PREDICATES
    a=customer_browser;page,url,tmp,errors=a
    page.goto(url)
    page.get_by_text('CUSTOMER QUALITY GATE NOT MET',exact=False).wait_for()
    seed=page.request.get(url+'/api/client/starting-checkpoints').json()[0]
    assert seed['readiness']['status']=='FOUNDATION_ONLY_NOT_VOTING_DOMAIN_QUALIFIED'
    assert not seed['readiness']['domain_model_qualified']
    rows=[]
    texts=[
        ('TRAIN','Owners may cast proxy ballots for the Aurora annual assembly. The custodian accepts voting instructions until 18 November 2026 at 09:00 UTC.'),
        ('TRAIN','A dividend credit is being posted to the cash ledger. This advice offers no shareholder vote or instruction election.'),
        ('VALIDATION','Nominees can lodge voting directions on the merger resolutions at the special meeting. Custodian deadline: 21 November 2026 at 15:30 UTC.'),
        ('VALIDATION','The issuer announces a mandatory redemption of the outstanding notes. No ballot or shareholder meeting is involved.'),
        ('CALIBRATION','A class meeting will consider revised articles. Beneficial holders may instruct the nominee to vote by 23 November 2026 at 16:00 UTC.'),
        ('CALIBRATION','Settlement confirmation: the share subdivision was completed yesterday. This historical entry requires no shareholder decision.'),
        ('FROZEN_TEST','The company invites investors to its extraordinary general meeting and provides an electronic ballot. Voting closes on 25 November 2026 at 12:00 UTC.'),
        ('FROZEN_TEST','Custody statement: interest has accrued on the bond balance. This accounting report provides no voting opportunity.'),
    ]
    for i,(role,text) in enumerate(texts):
        rows.append(row(role,ident='JOURNEY-'+str(i),text=text))
    # Exercise the optional ISO adapter inside the complete learning journey,
    # alongside ordinary unstructured notices. This is a labelled standards-
    # derived fixture, not a genuine customer SWIFT message.
    from iso_adapter.benchmark import fin
    rows[0]['raw']=fin(':16R:GENL\n:20C::CORP//JOURNEY-0\n:20C::SEME//JOURNEY-0\n'
        ':23G:NEWM\n:22F::CAEV//MEET\n:16S:GENL\n:16R:CAOPTN\n'
        ':22F::CAOP//PROX\n:98E::RDDT//20261118090000/0000\n:16S:CAOPTN\n'
        ':16R:ADDINFO\n:70E::ADTX//'+texts[0][1]+'\n:16S:ADDINFO')
    file=tmp/'journey.jsonl';file.write_text(''.join(json.dumps(r)+'\n' for r in rows))
    page.locator('#import-id').fill('journey-import');page.locator('#import-file').set_input_files(file)
    imported=post_from_ui(page,'/imports','#import')
    ids=[r['event_id'] for r in imported['rows']]
    assert imported['accepted']==8
    for i,eid in enumerate(ids):
        open_event(page,'JOURNEY-'+str(i))
        page.get_by_role('heading',name='Verified facts',exact=True).wait_for()
        if rows[i]['split'] in ('CALIBRATION','FROZEN_TEST'):
            assert 'BLIND REVIEW' in page.locator('#event').text_content()
        vote='VOTABLE' if i%2==0 else 'NOT_VOTABLE'
        for key in PREDICATES:
            page.locator('#label-'+key).select_option(vote if key=='votability' else 'NO')
        page.locator('#evidence-votability').fill(json.dumps([texts[i][1]]))
        page.locator('#review-time').fill('2026-10-18T12:00:00+00:00')
        page.locator('#deadline-status').select_option('OPEN' if vote=='VOTABLE' else 'UNKNOWN')
        page.locator('#final-status').select_option(vote)
        page.locator('#ai-model').fill('EXPLICIT_BROWSER_LABEL_FIXTURE_NOT_EXPERT')
        saved=post_from_ui(page,'/ai-labels','#save-ai')
        assert saved['payload']['provenance']['origin']=='AI_AUTHORED'
    # Export includes all reviewed development events. Preserve any earlier
    # fixture event instead of deleting data to make the journey appear clean.
    for event in page.request.get(url+'/api/client/events').json()['items']:
        if event['id'] not in ids and event['split'] in ('TRAIN','VALIDATION'):
            if page.request.get(url+'/api/client/events/'+event['id']).json()['reviews']:
                ids.append(event['id'])
    page.locator('#dataset-id').fill('journey-dataset');page.locator('#dataset-events').fill('\n'.join(ids))
    frozen=post_from_ui(page,'/datasets','#freeze')
    assert frozen['roles']['CALIBRATION']==2 and frozen['roles']['FROZEN_TEST']==2
    # A frozen label cannot be overwritten through a second browser review.
    open_event(page,'JOURNEY-7')
    page.locator('#ai-model').fill('EXPLICIT_BROWSER_LABEL_FIXTURE_NOT_EXPERT')
    with page.expect_response(lambda r:'/ai-labels' in r.url and r.request.method=='POST') as locked:
        page.locator('#save-ai').click()
    assert locked.value.status==409
    page.locator('#bundle-id').fill('journey-bundle')
    exported=post_from_ui(page,'/training-bundles','#export')
    assert set(exported['counts'])=={'TRAIN','VALIDATION'}
    spec={**seed['spec'],'parent_seed_path':str(tmp/'workspace/seeds/browser-foundation'),'epochs':1}
    campaign={'bundle_id':'journey-bundle','dataset_id':'journey-dataset',
              'stages':[{'name':'laya','training':spec}],
              'candidates':[{'name':'SPECIALIST','mode':'LAYA_ONLY','laya_stage':'laya'}]}
    page.get_by_text('Prepare a reproducible learning campaign',exact=True).click()
    page.locator('#campaign-id').fill('journey-campaign');page.locator('#campaign-spec').fill(json.dumps(campaign))
    post_from_ui(page,'/campaigns/journey-campaign','#prepare')
    post_from_ui(page,'/campaigns/journey-campaign/start','#start')
    page.locator('#campaigns').get_by_text('COMPLETED',exact=True).wait_for()
    campaign_result=json.loads((tmp/'workspace/campaigns/journey-campaign/result.json').read_text())
    assert not campaign_result['calibration_or_test_answers_opened']
    page.get_by_text('Freeze a completed training checkpoint for the next learning round',exact=True).click()
    page.locator('#derivative-job').fill(campaign_result['stage_jobs']['laya'])
    page.locator('#derivative-id').fill('journey-next-start')
    derivative=post_from_ui(page,'/starting-checkpoints/from-job','#freeze-derivative')
    assert derivative['origin']=='AI_TEST_DERIVATIVE'
    assert derivative['lineage']['training_bundle_sha256']
    assert not derivative['automation_enabled']
    parent_weights=Path(derivative['model_location'])/'model.safetensors'
    original_weights=parent_weights.read_bytes()
    continued={**derivative['spec'],'parent_seed_path':str(tmp/'workspace/seeds/journey-next-start')}
    second={**campaign,'stages':[{'name':'laya','training':continued}]}
    page.locator('#campaign-id').fill('journey-round-two')
    page.locator('#campaign-spec').fill(json.dumps(second))
    post_from_ui(page,'/campaigns/journey-round-two','#prepare')
    post_from_ui(page,'/campaigns/journey-round-two/start','#start')
    campaign_result=json.loads((tmp/'workspace/campaigns/journey-round-two/result.json').read_text())
    assert not campaign_result['calibration_or_test_answers_opened']
    assert parent_weights.read_bytes()==original_weights
    second_plan=json.loads((tmp/'workspace/jobs'/campaign_result['stage_jobs']['laya']/'plan.json').read_text())
    assert second_plan['preflight']['parent_checkpoint_identity']==derivative['identity']
    release_id=campaign_result['selected_release']
    protected=page.request.post(url+'/api/client/tasks/protected-inference',data={'kind':'INFERENCE',
        'payload':{'release_id':release_id,'event_ids':[imported['rows'][7]['event_id']]}})
    assert protected.status==409 and 'Protected input' in protected.text()
    def task(ident,kind,payload):
        page.locator('#task-id').fill(ident);page.locator('#task-kind').select_option(kind)
        page.locator('#task-spec').fill(json.dumps(payload))
        post_from_ui(page,'/tasks/'+ident,'#queue-task')
        status=page.request.get(url+'/api/client/status').json()
        saved=next(t for t in status['tasks'] if t['id']==ident)
        assert saved['state']=='COMPLETED', saved
    task('execute-calibration','CALIBRATION',{'ident':'journey-calibrator','dataset_id':'journey-dataset',
         'release_id':release_id,'population':'AI_FRAMEWORK','reference':'2026-10-18T12:00:00+00:00'})
    cal=page.request.get(url+'/api/client/calibrators').json()[0]
    assert set(cal['reports'])=={*PREDICATES,'final_decision'}
    assert all(r['status']=='INSUFFICIENT_SUPPORT' for r in cal['reports'].values())
    cal_path=tmp/'workspace/customer-calibrators/journey-calibrator.json'
    page.get_by_text('Predeclare a customer qualification plan',exact=True).click()
    page.locator('#qualification-id').fill('journey-qualification')
    page.locator('#qualification-spec').fill(json.dumps({'release_id':release_id,'dataset_id':'journey-dataset',
        'calibrator_path':str(cal_path),'population':'AI_FRAMEWORK','reference':'2026-10-18T12:00:00+00:00','policy':{}}))
    post_from_ui(page,'/qualifications/journey-qualification','#qualification-plan')
    task('execute-qualification','QUALIFICATION',{'id':'journey-qualification'})
    qualified=page.request.get(url+'/api/client/qualifications').json()[0]
    assert not qualified['customer_gate_passed']
    assert 'SYNTHETIC_OR_NONEXPERT_TEST_LABELS' in qualified['reasons']
    page.locator('#promotion-id').fill('journey-qualification')
    with page.expect_response(lambda r:'/promotions/journey-qualification' in r.url) as failed:
        page.locator('#promote').click()
    assert failed.value.status==409
    task('execute-inference','INFERENCE',{'release_id':release_id,'event_ids':[ids[0]],'calibrator_id':'journey-calibrator'})
    decisions=page.request.get(url+'/api/client/decisions').json()
    assert len(decisions)==1 and decisions[0]['decision']['review_required']
    assert decisions[0]['decision']['confidence'] is None
    assert not decisions[0]['decision']['automation_enabled']
    open_event(page,'JOURNEY-0')
    assert 'HUMAN REVIEW REQUIRED' in page.locator('#event').text_content()
    assert 'HEURISTIC / NOT YET CALIBRATED' in page.locator('#event').text_content()
    trace=page.locator('#event details').filter(has=page.get_by_text('Persisted model and evidence trace',exact=True))
    assert 'release_identity' in trace.locator('pre').text_content()
    queued=page.request.post(url+'/api/client/tasks/cancel-this-inference',data={'kind':'INFERENCE',
        'payload':{'release_id':release_id,'event_ids':[ids[0]]}})
    assert queued.ok and queued.json()['state']=='QUEUED'
    assert page.request.post(url+'/api/client/tasks/cancel-this-inference/cancel',data={}).ok
    cancelled=next(t for t in page.request.get(url+'/api/client/status').json()['tasks'] if t['id']=='cancel-this-inference')
    assert cancelled['state']=='CANCELLED'
    a.restart();page.reload()
    page.get_by_text('CUSTOMER QUALITY GATE NOT MET',exact=False).wait_for()
    assert page.request.get(url+'/api/client/decisions').json()==decisions
    assert page.request.get(url+'/api/client/audit').json()['integrity']['valid']
    open_event(page,'JOURNEY-0')
    assert 'HUMAN REVIEW REQUIRED' in page.locator('#event').text_content()
    page.screenshot(path='artifacts/customer-qualification-journey.png',full_page=True)
    assert errors==[]


def test_customer_iso_parser_and_recovery_provenance_survive_the_browser(customer_browser):
    """Real Java parser and scanner run; no semantic model is requested."""
    page,url,tmp,errors=customer_browser
    example=json.loads(Path('tests/fixtures/prowide-mt564.json').read_text())
    official={**row(ident='D455103',text=example['raw']), 'declared':None,
              'source_type':'PUBLIC_EXAMPLE','source_reference':example['source_url']}
    partial=row(ident='PARTIAL-UI',text=':16R:ADDINFO\n:70E::ADTX//Registration must be received before the meeting.\nContinued narrative é.\n:99Z:UNKNOWN-CONTENT')
    plain=row(ident='PLAIN-UI',text='Ordinary shareholder meeting notice without a SWIFT envelope or field tags.')
    file=tmp/'parser-paths.jsonl';file.write_text(''.join(json.dumps(r)+'\n' for r in (official,partial,plain)))
    page.goto(url);page.locator('#import-id').fill('parser-paths');page.locator('#import-file').set_input_files(file)
    receipt=post_from_ui(page,'/imports','#import');assert receipt['accepted']==3,receipt
    for corp,parser,raw in [('D455103','PROWIDE',official['raw']),('PARTIAL-UI','LENIENT_RECOVERY',partial['raw']),('PLAIN-UI','NOT_APPLICABLE',plain['raw'])]:
        open_event(page,corp)
        source=page.locator('#event details').first
        assert parser in source.locator('summary').text_content()
        assert source.locator('pre').text_content()==raw
    official_id=receipt['rows'][0]['event_id']
    view=page.request.get(url+'/api/client/events/'+official_id).json()
    facts=view['facts']
    assert any(f['name']=='corp' and f['value']=='D455103' and f['source']=='PROWIDE' for f in facts)
    page.screenshot(path='artifacts/customer-parser-paths.png',full_page=True)
    assert errors==[]


def test_customer_auditor_can_inspect_but_cannot_train_or_author_labels(customer_browser):
    page,url,tmp,errors=customer_browser
    context=page.context.browser.new_context(http_credentials={'username':'auditor','password':PASSWORD})
    try:
        audit=context.new_page();audit.goto(url)
        audit.get_by_text('auditor · AUDITOR',exact=True).wait_for()
        assert not audit.locator('#learning').is_visible()
        assert not audit.locator('#queue-task').is_visible()
        assert audit.request.post(url+'/api/client/datasets',data={'id':'forbidden','event_ids':[]}).status==403
        assert audit.request.post(url+'/api/client/campaigns/forbidden',data={}).status==403
        assert audit.request.get(url+'/api/client/audit').json()['integrity']['valid']
    finally:context.close()
    assert errors==[]


def test_customer_delayed_event_response_cannot_replace_newer_selection(customer_browser):
    from playwright.sync_api import expect
    page,url,tmp,errors=customer_browser
    records=[row(ident='RACE-FIRST',text='First source record: an optional bond conversion.'),
             row(ident='RACE-SECOND',text='Second source record: a proxy voting meeting.')]
    file=tmp/'race.jsonl';file.write_text(''.join(json.dumps(r)+'\n' for r in records))
    page.goto(url);page.locator('#import-id').fill('race-records');page.locator('#import-file').set_input_files(file)
    imported=post_from_ui(page,'/imports','#import')
    first=imported['rows'][0]['event_id']
    saved=page.request.get(url+'/api/client/events/'+first).json()
    held=[]
    pattern='**/api/client/events/'+first
    page.route(pattern,lambda route:held.append(route))
    try:
        page.get_by_role('button',name='RACE-FIRST',exact=True).click()
        page.get_by_role('button',name='RACE-SECOND',exact=True).click()
        expect(page.locator('#event > h3').first).to_contain_text('RACE-SECOND')
        assert len(held)==1
        with page.expect_response(lambda r:r.url.endswith('/api/client/decisions')):
            held[0].fulfill(json=saved)
        expect(page.locator('#event > h3').first).to_contain_text('RACE-SECOND')
        assert 'Second source record' in page.locator('#event pre').first.text_content()
    finally:page.unroute(pattern)
    page.locator('#query').fill('RACE-SECOND');page.locator('#split').select_option('TRAIN')
    with page.expect_response(lambda r:'/api/client/events?q=' in r.url):
        page.locator('#search button').click()
    expect(page.locator('#events button')).to_have_count(1)
    expect(page.locator('#events button')).to_have_text('RACE-SECOND')
    assert errors==[]


def test_customer_invalid_import_fails_without_crashing(customer_browser):
    page,url,tmp,errors=customer_browser
    page.goto(url);page.get_by_text('CUSTOMER QUALITY GATE NOT MET',exact=False).wait_for()
    file=tmp/'invalid.jsonl';file.write_text('{bad JSON}\n')
    page.locator('#import-id').fill('invalid-ui');page.locator('#import-file').set_input_files(file)
    page.locator('#import').click()
    page.locator('#message').get_by_text('JSON',exact=False).wait_for()
    assert not page.request.get(url+'/api/client/events?q=invalid-ui').json()['items']
    assert errors==[]


def test_customer_random_audit_trace_and_original_evaluation_time(customer_browser):
    """Persisted UI receipt fixture; no model quality or automation certificate."""
    import sqlite3
    from playwright.sync_api import expect
    page,url,tmp,errors=customer_browser
    response=page.request.post(url+'/api/client/imports',data={'id':'audit-ui-import','rows':[row(ident='AUDIT-UI')]})
    assert response.ok,response.text()
    eid=response.json()['rows'][0]['event_id'];view=page.request.get(url+'/api/client/events/'+eid).json()
    decision={'id':'audit-ui','event_id':eid,'execution_id':'UI_FIXTURE','snapshot_hash':view['snapshot_hash'],
              'created_at':'2026-10-22T12:00:00+00:00','decision':{
                  'classification':'VOTABLE','confidence':None,'review_required':True,'automation_enabled':False,
                  'evaluation_time':'2026-10-18T12:00:00+00:00','predicate_confidence':{},
                  'review_reasons':['RANDOM_ACCEPTED_DECISION_AUDIT'],
                  'audit_selection':{'selected':True,'pre_audit_eligible':True,'rate':.02}}}
    with sqlite3.connect(tmp/'db.sqlite') as c:
        c.execute('INSERT INTO client_decisions VALUES(?,?,?,?,?)',('audit-ui',decision['created_at'],eid,'UI_FIXTURE',json.dumps(decision)))
    page.goto(url);open_event(page,'AUDIT-UI')
    expect(page.locator('#event').get_by_text('RANDOM ACCEPTED-DECISION AUDIT',exact=True)).to_be_visible()
    expect(page.locator('#review-time')).to_have_value('2026-10-18T12:00:00+00:00')
    expect(page.locator('#metrics')).to_contain_text('Random accepted-decision audits')
    customer_browser.restart();page.reload();open_event(page,'AUDIT-UI')
    expect(page.locator('#event')).to_contain_text('RANDOM ACCEPTED-DECISION AUDIT')
    assert errors==[]
