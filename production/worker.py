"""Explicit durable inference/calibration/qualification queue, one local worker.

Completed event results survive process death. An interrupted task is never
silently retried under its original identity. SIGTERM stops after the active
notice and before the next notice. Training campaigns use their existing worker.
"""
import fcntl
import json
import os
import signal
import time
import threading
from pathlib import Path
from apps.api import store
from production.storage import audit, digest
from training.framework import jobs, events, releases
from training.framework.resources import model_resource

STOP = False


def initialise():
    with store.connect() as c:
        c.executescript('''CREATE TABLE IF NOT EXISTS client_tasks(
        id TEXT PRIMARY KEY,created_at TEXT NOT NULL,actor TEXT NOT NULL,kind TEXT NOT NULL,
        state TEXT NOT NULL,payload TEXT NOT NULL,progress INTEGER NOT NULL DEFAULT 0,error TEXT);
        CREATE TRIGGER IF NOT EXISTS immutable_client_task_input BEFORE UPDATE OF id,created_at,actor,kind,payload ON client_tasks
        BEGIN SELECT RAISE(ABORT,'Task input is immutable'); END;
        CREATE TRIGGER IF NOT EXISTS immutable_client_task_delete BEFORE DELETE ON client_tasks
        BEGIN SELECT RAISE(ABORT,'Task history is immutable'); END;
        CREATE TABLE IF NOT EXISTS client_worker_health(id INTEGER PRIMARY KEY CHECK(id=1),last_seen REAL NOT NULL,state TEXT NOT NULL);
        ''')


def heartbeat(state='ALIVE'):
    with store.connect() as c:
        c.execute('INSERT INTO client_worker_health VALUES(1,?,?) ON CONFLICT(id) DO UPDATE SET last_seen=excluded.last_seen,state=excluded.state', (time.time(),state))


def health():
    with store.connect() as c: row=c.execute('SELECT * FROM client_worker_health WHERE id=1').fetchone()
    age=time.time()-row['last_seen'] if row else None
    return {'healthy':bool(row and row['state']=='ALIVE' and 0<=age<30),
            'last_seen':row['last_seen'] if row else None,'age_seconds':age,'state':row['state'] if row else 'NOT_SEEN'}


def submit(ident, kind, payload, actor):
    jobs.member('client-tasks', ident)
    if kind not in ('INFERENCE', 'CALIBRATION', 'QUALIFICATION'): raise ValueError('Unknown task kind')
    initialise()
    with store.connect() as c:
        existing = c.execute('SELECT * FROM client_tasks WHERE id=?', (ident,)).fetchone()
        if existing:
            if existing['kind'] != kind or json.loads(existing['payload']) != payload or existing['actor'] != actor: raise ValueError('Task identity collision')
            return dict(existing)
        c.execute('INSERT INTO client_tasks(id,created_at,actor,kind,state,payload) VALUES(?,?,?,?,?,?)', (ident, store.now(), actor, kind, 'QUEUED', store.dumps(payload)))
    audit(actor, 'TASK_QUEUED', {'id': ident, 'kind': kind, 'input_hash': digest(payload)})
    return {'id': ident, 'state': 'QUEUED'}


def listing():
    initialise()
    with store.connect() as c: return [{**dict(r), 'payload': json.loads(r['payload'])} for r in c.execute('SELECT * FROM client_tasks ORDER BY created_at DESC LIMIT 200')]


def cancel(ident, actor):
    with store.connect() as c:
        r = c.execute('SELECT * FROM client_tasks WHERE id=?', (ident,)).fetchone()
        if not r: raise ValueError('Task not found')
        if r['state'] == 'QUEUED': c.execute("UPDATE client_tasks SET state='CANCELLED' WHERE id=?", (ident,))
        elif r['state'] == 'RUNNING': c.execute("UPDATE client_tasks SET state='CANCEL_REQUESTED' WHERE id=?", (ident,))
    audit(actor, 'TASK_CANCEL_REQUESTED', {'id': ident})
    return {'id': ident}


def check(ident):
    with store.connect() as c: state = c.execute('SELECT state FROM client_tasks WHERE id=?', (ident,)).fetchone()[0]
    if STOP or state == 'CANCEL_REQUESTED': raise InterruptedError('Cooperative stop after current notice')


def inference(task):
    from production.service import metadata
    from production import qualification
    payload = task['payload']; release = jobs.member('releases', payload['release_id'])
    if payload.get('review_only_unsealed') and (payload.get('qualification_id') or payload.get('calibrator_id')):
        raise ValueError('Unsealed bootstrap is review-only and cannot attach qualification/calibration')
    model = releases.ReleaseModel(release,sealed=False) if payload.get('review_only_unsealed') else releases.ReleaseModel(release)
    qualified = None; qualification_problem = None
    development_calibrator = None
    if payload.get('calibrator_id'):
        from production.confidence import load
        path = jobs.member('customer-calibrators', payload['calibrator_id']).with_suffix('.json')
        development_calibrator = load(path, model.manifest['identity'])
    if payload.get('qualification_id'):
        try:
            plan, certificate = qualification.verify(payload['qualification_id'])
            if plan['release_id'] != payload['release_id']: raise ValueError('Qualified release mismatch')
            from production.confidence import load
            qualified = (plan, certificate, load(qualification.root(payload['qualification_id']) / 'calibrator.json', plan['release_identity']))
        except (ValueError, FileNotFoundError): qualification_problem = 'QUALIFICATION_INVALID_OR_EXPIRED'
    try:
        for index, ident in enumerate(payload['event_ids']):
            check(task['id'])
            view = events.get(ident)
            if view['split'] in ('CALIBRATION', 'FROZEN_TEST'): raise ValueError('Protected data is evaluated only through the qualification workflow')
            meta=metadata(view)
            routing_context={k:meta[k] for k in ('language','population')} if getattr(getattr(model,'spec',None),'laya_calibrator_id',None) else None
            if routing_context:routing_context['input_type_context']=meta['input_type']
            execution = events.classify(ident, release, reference=store.now(), model=model, inference_context=routing_context)
            result = execution['payload']['result']
            decision = {'classification': result['decision']['classification'], 'confidence': None,
                        'evaluation_time': result.get('evaluation_time'),
                        'confidence_kind': 'HEURISTIC / NOT YET CALIBRATED', 'review_required': True,
                        'review_reasons': ['NO_CUSTOMER_QUALIFICATION'], 'automation_enabled': False,'calibration':None}
            if qualification_problem: decision['review_reasons'].append(qualification_problem)
            from production.confidence import feature_row
            meta = metadata(view)
            decision['predicate_confidence'] = {k: {'value': result['predicates'][k]['value'], 'confidence': None,
                'band': feature_row(view['current_text'], k, result['predicates'][k], language=meta['language'], input_type=meta['input_type'], conflicts=result['reconciliation']['conflicts'])['heuristic_band'],
                'evidence': result['predicates'][k].get('evidence', []), 'kind': 'HEURISTIC / NOT YET CALIBRATED'}
                for k in __import__('semantic_pipeline.schema', fromlist=['PREDICATES']).PREDICATES}
            from production.evidence_basis import valid_negative_basis
            for key,p in decision['predicate_confidence'].items():
                pred=result['predicates'][key]
                p['negative_basis']=pred.get('negative_basis') if valid_negative_basis(view['current_text'],pred) else None
            if qualified:
                plan, certificate, cal = qualified
                decision['assessment'] = qualification.assess(view['current_text'], result, metadata(view), cal, plan['release_identity'], plan['policy']['threshold'])
                decision['confidence'] = decision['assessment']['final_decision_confidence']
                decision['confidence_kind'] = 'CALIBRATED_IN_DECLARED_POPULATION' if decision['confidence'] is not None else decision['confidence_kind']
                decision['predicate_confidence'] = decision['assessment']['predicates']
                decision['calibration']={'version':cal['version'],'sha256':cal['sha256'],
                    'model_identity':cal['identity'],'population':cal['population'],'qualification_id':payload['qualification_id']}
                with store.connect() as c:
                    promotion = c.execute('SELECT * FROM client_promotions ORDER BY id DESC LIMIT 1').fetchone()
                    suspended = c.execute('SELECT 1 FROM client_suspensions WHERE qualification_id=?', (payload['qualification_id'],)).fetchone()
                from datetime import datetime, timezone
                current = datetime.now(timezone.utc) < datetime.fromisoformat(certificate['expires_at'])
                permission = (current and not suspended and certificate['customer_gate_passed'] and promotion and promotion['qualification_id'] == payload['qualification_id'] and os.environ.get('AUTOMATION_ENABLED', 'false') == 'true')
                reasons = list(decision['assessment']['review_reasons'])
                if not permission: reasons.append('CUSTOMER_AUTOMATION_NOT_AUTHORISED')
                decision.update(review_required=not (permission and decision['assessment']['eligible']), review_reasons=reasons,
                                automation_enabled=bool(permission), qualification_id=payload['qualification_id'])
            elif development_calibrator:
                assessment = qualification.assess(view['current_text'], result, meta, development_calibrator,
                                                   model.manifest['identity'], payload.get('simulation_threshold', .99))
                decision.update(confidence=assessment['final_decision_confidence'],
                                predicate_confidence=assessment['predicates'], assessment=assessment,
                                confidence_kind='CALIBRATED_IN_DECLARED_POPULATION' if assessment['final_decision_confidence'] is not None else decision['confidence_kind'],
                                would_auto_classify=assessment['eligible'], confidence_scope=development_calibrator['population'],
                                review_reasons=['REVIEW_SIMULATION_ONLY_NO_CUSTOMER_QUALIFICATION'] + assessment['review_reasons'])
                decision['calibration']={'version':development_calibrator['version'],'sha256':development_calibrator['sha256'],
                    'model_identity':development_calibrator['identity'],'population':development_calibrator['population'],
                    'calibrator_id':payload['calibrator_id']}
            if view['warnings']:
                decision['review_required'] = True; decision['review_reasons'] += view['warnings']
            fresh = events.get(ident)
            actual_snapshot = result['event_snapshot_hash']
            if fresh['snapshot_hash'] != actual_snapshot:
                decision['review_required'] = True; decision['review_reasons'].append('SOURCE_CHANGED_DURING_INFERENCE')
            saved = {'id': task['id'] + ':' + str(index), 'task_id': task['id'], 'event_id': ident,
                     'execution_id': execution['id'], 'snapshot_hash': actual_snapshot, 'release_id': payload['release_id'],
                     'decision': decision, 'latencies': result['latencies'], 'created_at': store.now()}
            with store.connect() as c:
                c.execute('BEGIN IMMEDIATE')
                latest_message = c.execute('SELECT max(id) FROM learning_messages WHERE event_id=?', (ident,)).fetchone()[0]
                if latest_message != fresh['messages'][-1]['id']:
                    decision['review_required'] = True; decision['review_reasons'].append('SOURCE_CHANGED_BEFORE_COMMIT')
                if decision['automation_enabled']:
                    promotion = c.execute('SELECT qualification_id FROM client_promotions ORDER BY id DESC LIMIT 1').fetchone()
                    suspended = c.execute('SELECT 1 FROM client_suspensions WHERE qualification_id=?', (payload['qualification_id'],)).fetchone()
                    if suspended or not promotion or promotion[0] != payload['qualification_id'] or datetime.now(timezone.utc) >= datetime.fromisoformat(certificate['expires_at']):
                        decision['review_required'] = True; decision['review_reasons'].append('AUTHORISATION_CHANGED_BEFORE_COMMIT')
                        decision['automation_enabled'] = False
                from production.monitoring import apply
                apply(decision, '|'.join([payload['release_id'], str(payload.get('qualification_id')), ident, saved['id']]),
                      qualified[0]['policy'].get('random_audit_rate', .02) if qualified else .02)
                c.execute('INSERT INTO client_decisions VALUES(?,?,?,?,?)', (saved['id'], saved['created_at'], ident, execution['id'], store.dumps(saved)))
                c.execute('UPDATE client_tasks SET progress=? WHERE id=?', (index + 1, task['id']))
    finally: model.close()


def run_once():
    initialise()
    with store.connect() as c:
        c.execute('BEGIN IMMEDIATE')
        row = c.execute("SELECT * FROM client_tasks WHERE state='QUEUED' ORDER BY created_at LIMIT 1").fetchone()
        if not row: return False
        c.execute("UPDATE client_tasks SET state='RUNNING' WHERE id=?", (row['id'],))
    task = {**dict(row), 'payload': json.loads(row['payload'])}
    if task.get('error') != 'DEVICE_BUSY_WAIT': audit('worker', 'TASK_STARTED', {'id': task['id']})
    state = 'COMPLETED'; error = None
    try:
        if os.environ.get('TRAINING_EXECUTION_ENABLED', 'false') != 'true': raise ValueError('Model execution disabled')
        from production.resources import device
        with device('client-task:' + task['id']), model_resource('client-task:' + task['id']):
            if task['kind'] == 'INFERENCE': inference(task)
            elif task['kind'] == 'CALIBRATION':
                from production.service import calibrate
                check(task['id']); calibrate(actor=task['actor'], check=lambda: check(task['id']), **task['payload'])
            else:
                from production.qualification import evaluate
                check(task['id']); evaluate(task['payload']['id'], check=lambda: check(task['id']))
    except InterruptedError: state = 'INTERRUPTED'; error = 'Cooperative stop; completed predictions retained; explicit new task required'
    except Exception as exc:
        if str(exc) == 'Managed model device busy': state = 'QUEUED'; error = 'DEVICE_BUSY_WAIT'
        else: state = 'FAILED'; error = type(exc).__name__ + ': ' + str(exc)[:400]
    with store.connect() as c: c.execute('UPDATE client_tasks SET state=?,error=? WHERE id=?', (state, error, task['id']))
    if state != 'QUEUED' or task.get('error') != 'DEVICE_BUSY_WAIT':
        audit('worker', 'TASK_' + state, {'id': task['id'], 'error_type': error.split(':')[0] if error else None})
    return state != 'QUEUED'


def main():
    from production.storage import initialise as init
    init(); initialise(); jobs.WORKSPACE.mkdir(parents=True, exist_ok=True)
    global STOP
    def stop(*_):
        global STOP
        STOP = True
    signal.signal(signal.SIGTERM, stop); signal.signal(signal.SIGINT, stop)
    with (jobs.WORKSPACE / 'client-worker.lock').open('a') as lock:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        # This lock proves no earlier worker survives. Never auto-retry a task
        # that might already have persisted partial model outputs.
        with store.connect() as c: c.execute("UPDATE client_tasks SET state='INTERRUPTED',error='Worker exited; explicit new task required' WHERE state IN ('RUNNING','CANCEL_REQUESTED')")
        ended=threading.Event()
        def pulse():
            while not ended.is_set():
                heartbeat()
                ended.wait(3)
        thread=threading.Thread(target=pulse,daemon=True);thread.start()
        try:
            while not STOP:
                if not run_once(): time.sleep(.5)
        finally:
            ended.set();thread.join(timeout=5);heartbeat('STOPPED')


if __name__ == '__main__': main()
