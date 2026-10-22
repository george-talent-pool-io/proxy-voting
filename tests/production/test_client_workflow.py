"""Customer trust-boundary tests. No model-quality claim uses these fixtures."""
import copy
import json
import sqlite3
from pathlib import Path
import pytest
from fastapi.testclient import TestClient
from production import security, storage, service, worker


PASSWORD = 'controlled-test-password-47'


@pytest.fixture
def client_app(db, tmp_path, monkeypatch):
    users = {name: {'roles': roles, 'expert_attested': name == 'expert', 'password': security.password_record(PASSWORD)}
             for name, roles in [('owner', ['ADMIN']), ('trainer', ['TRAINER']), ('expert', ['REVIEWER']), ('auditor', ['AUDITOR'])]}
    path = tmp_path / 'users.json'; path.write_text(json.dumps(users))
    monkeypatch.setenv('VOTING_USERS_FILE', str(path)); monkeypatch.setenv('VOTING_PUBLIC_ORIGIN', 'http://localhost')
    monkeypatch.setenv('VOTING_ALLOW_LOCAL_HTTP', 'true')
    from apps.api.production import create_app
    with TestClient(create_app(), base_url='http://localhost') as client: yield client


def auth(name='owner'): return (name, PASSWORD)


def row(split='TRAIN', ident='meeting-a', text=None):
    return {'raw': text or 'Shareholders may vote at the meeting. No share blocking is required. Deadline 20 October 2026.',
            'sender': 'CONTROLLED_TEST', 'source_type': 'STANDARDS_DERIVED_SYNTHETIC', 'group_id': ident, 'family': ident,
            'split': split, 'source_reference': 'AI framework fixture, not customer data',
            'declared': {'corp': ident, 'seme': ident, 'function': 'NEWM'}, 'language': 'en', 'population': 'AI_FRAMEWORK'}


def body(view):
    from semantic_pipeline.schema import PREDICATES
    text = view['messages'][0]['raw_source']
    return {'snapshot_hash': view['snapshot_hash'], 'expected_revision': view['latest_review_revision'],
            'target': {**{k: 'VOTABLE' if k == 'votability' else 'NO' for k in PREDICATES},
                       'deadline_information': {'deadline_mentioned': False, 'deadline_text': None},
                       'evidence': {k: [text] for k in PREDICATES}, 'ambiguities': []},
            'expected_final_status': 'VOTABLE', 'expected_deadline_status': 'OPEN', 'evaluation_time': '2026-10-18T12:00:00+00:00'}


def imported(client, record=None, name='batch-a'):
    r = client.post('/api/client/imports', json={'id': name, 'rows': [record or row()]}, auth=auth('trainer'))
    assert r.status_code == 201, r.text
    assert r.json()['accepted'] == 1, r.text
    return r.json()['rows'][0]['event_id']


def test_fail_closed_startup_requires_named_users(monkeypatch):
    monkeypatch.delenv('VOTING_USERS_FILE', raising=False)
    with pytest.raises(KeyError): security.configuration()


def test_named_auth_roles_host_origin_and_research_api_absent(client_app):
    c = client_app
    assert c.get('/health/live').status_code == 200
    assert c.get('/api/client/status').status_code == 401
    assert c.get('/api/client/status', auth=('owner', 'wrong')).status_code == 401
    assert c.get('/api/client/status', auth=auth()).status_code == 200
    assert c.get('/api/learning/status', auth=auth()).status_code == 404
    assert c.get('/api/client/status', headers={'Host': 'attacker.invalid'}, auth=auth()).status_code == 403
    assert c.post('/api/client/imports', json={'id':'x','rows':[row()]}, auth=auth('auditor')).status_code == 403
    assert c.post('/api/client/imports', json={'id':'x','rows':[row()]}, auth=auth(), headers={'Origin':'https://evil.invalid'}).status_code == 403
    assert c.post('/api/client/imports', content=b'x', headers={'content-length':'20000000'}, auth=auth()).status_code == 413


def test_import_is_resumable_lossless_and_rejects_collisions(client_app):
    c = client_app; raw = 'A\r\nUnicode: é — vote\n\n  Original spacing  '
    payload = {'id':'lossless', 'rows':[row(text=raw), {'raw': ''}]}
    a = c.post('/api/client/imports', json=payload, auth=auth('trainer'))
    assert a.json()['accepted'] == 1 and a.json()['rejected'] == 1
    assert c.post('/api/client/imports', json=payload, auth=auth('trainer')).json() == a.json()
    eid = a.json()['rows'][0]['event_id']
    assert c.get('/api/client/events/'+eid, auth=auth()).json()['messages'][0]['raw_source'] == raw
    payload['rows'][0]['raw'] = 'A different message'
    assert c.post('/api/client/imports', json=payload, auth=auth()).status_code == 409
    assert storage.verify_audit()['valid']


def test_authenticated_labels_cannot_spoof_expertise_and_ai_remains_ai(client_app):
    c = client_app; eid = imported(c)
    v = c.get('/api/client/events/'+eid, auth=auth('expert')).json(); label = body(v)
    assert c.post(f'/api/client/events/{eid}/reviews', json=label, auth=auth('trainer')).status_code == 403
    forged = {**label, 'provenance': {'origin':'EXPERT_REVIEWED','author':'someone'}}
    assert c.post(f'/api/client/events/{eid}/reviews', json=forged, auth=auth('expert')).status_code == 422
    ai = c.post(f'/api/client/events/{eid}/ai-labels', json={**label,'model_id':'AI_CONTROLLED_FIXTURE'}, auth=auth('trainer'))
    assert ai.status_code == 201, ai.text
    assert ai.json()['payload']['provenance']['origin'] == 'AI_AUTHORED'
    assert not ai.json()['payload']['provenance']['expert_attested']
    assert c.post(f'/api/client/events/{eid}/reviews', json=label, auth=auth('expert')).status_code == 409
    label['expected_revision'] = ai.json()['id']
    human = c.post(f'/api/client/events/{eid}/reviews', json=label, auth=auth('expert'))
    assert human.status_code == 201, human.text
    assert human.json()['payload']['provenance']['author'] == 'expert'
    assert len(c.get('/api/client/events/'+eid, auth=auth()).json()['reviews']) == 2


def test_blind_holdout_and_immutable_freeze(client_app):
    c = client_app; eid = imported(c, row('FROZEN_TEST'))
    view = c.get('/api/client/events/'+eid, auth=auth('expert')).json()
    assert view['blind'] and view['reviews'] == [] and view['executions'] == []
    label = body(view)
    r = c.post(f'/api/client/events/{eid}/ai-labels', json={**label, 'model_id':'CONTROLLED_AI'}, auth=auth('trainer'))
    assert r.status_code == 201, r.text
    assert c.get('/api/client/events/'+eid, auth=auth('expert')).json()['reviews'] == []
    r = c.post('/api/client/datasets', json={'id':'locked','event_ids':[eid]}, auth=auth('trainer'))
    assert r.status_code == 201, r.text
    assert r.json()['version'] == 'event-dataset-v2'
    assert c.post(f'/api/client/events/{eid}/ai-labels', json={**label,'model_id':'CONTROLLED_AI'}, auth=auth()).status_code == 409
    r = c.post('/api/client/imports', json={'id':'locked-reimport','rows':[row('FROZEN_TEST')]}, auth=auth())
    assert r.json()['rejected'] == 1


def test_freeze_requires_every_declared_event_reviewed(client_app):
    c = client_app; eid = imported(c)
    r = c.post('/api/client/datasets', json={'id':'not-reviewed','event_ids':[eid]}, auth=auth())
    assert r.status_code == 409 and 'Every' in r.text


def test_audit_and_task_inputs_immutable(client_app):
    worker.submit('explicit', 'QUALIFICATION', {'id':'does-not-exist'}, 'trainer')
    assert worker.submit('explicit', 'QUALIFICATION', {'id':'does-not-exist'}, 'trainer')['state'] == 'QUEUED'
    with pytest.raises(ValueError): worker.submit('explicit', 'QUALIFICATION', {'id':'other'}, 'trainer')
    assert worker.run_once()
    assert worker.listing()[0]['state'] == 'FAILED'
    with store_connection() as c:
        with pytest.raises(sqlite3.IntegrityError): c.execute("UPDATE client_audit SET actor='forged'")
        with pytest.raises(sqlite3.IntegrityError): c.execute("UPDATE client_tasks SET payload='{}'")


def store_connection():
    from apps.api import store
    return store.connect()


def test_verified_random_audit_error_suspends_release_and_enters_revision_history(client_app):
    """Software-only receipt fixture; this does not manufacture a qualified model."""
    from apps.api import store
    from semantic_pipeline.schema import PREDICATES
    c=client_app;eid=imported(c)
    view=c.get('/api/client/events/'+eid,auth=auth('expert')).json();label=body(view)
    before={'predicates':{k:{'value':label['target'][k]} for k in PREDICATES},
            'decision':{'classification':'VOTABLE'},'deadline':{'status':'OPEN'},
            'evaluation_time':label['evaluation_time']}
    before['predicates']['share_blocking']['value']='YES'
    receipt={'id':'audit-receipt','event_id':eid,'execution_id':'audit-execution','snapshot_hash':view['snapshot_hash'],
             'decision':{'review_required':True,'qualification_id':'SOFTWARE_FIXTURE_NOT_A_CERTIFICATE',
                         'confidence':.995,'audit_selection':{'selected':True,'pre_audit_eligible':True}}}
    with store.connect() as db:
        db.execute('INSERT INTO learning_executions VALUES(?,?,?,?,?,?)',('audit-execution',eid,view['snapshot_hash'],store.now(),'fixture',store.dumps({'result':before})))
        db.execute('INSERT INTO client_decisions VALUES(?,?,?,?,?)',('audit-receipt',store.now(),eid,'audit-execution',store.dumps(receipt)))
    response=c.post(f'/api/client/events/{eid}/reviews',json=label,auth=auth('expert'))
    assert response.status_code==201,response.text
    with store.connect() as db:
        suspension=json.loads(db.execute('SELECT payload FROM client_suspensions').fetchone()[0])
    assert suspension['fields']==['share_blocking']
    state=c.get('/api/client/status',auth=auth('auditor')).json()
    assert state['monitoring']['random_audit_reviews']==1 and state['monitoring']['release_suspensions']==1
    assert state['monitoring']['other_review_decisions']==0
