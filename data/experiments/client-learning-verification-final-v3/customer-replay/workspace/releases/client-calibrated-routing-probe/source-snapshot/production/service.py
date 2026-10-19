"""Customer workflow orchestration over the verified training framework."""
import json
import os
import fcntl
from functools import wraps
from pathlib import Path
from pydantic import BaseModel, ConfigDict, Field
from typing import Literal

from apps.api import store
from production.storage import digest, audit
from training.framework import events, event_data, jobs, releases
from training.framework.bundle import write, sha
from semantic_pipeline.schema import PREDICATES


def reference_time(value):
    from datetime import datetime, timezone
    d = datetime.fromisoformat(value)
    if d.tzinfo is None: raise ValueError('Evaluation time must include timezone')
    return d.astimezone(timezone.utc).isoformat()


def workflow_write(fn):
    @wraps(fn)
    def guarded(*args, **kwargs):
        jobs.WORKSPACE.mkdir(parents=True, exist_ok=True)
        with (jobs.WORKSPACE / 'customer-workflow.lock').open('a') as lock:
            try: fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
            except BlockingIOError: raise ValueError('Customer workflow write busy; retry')
            return fn(*args, **kwargs)
    return guarded


class Message(BaseModel):
    model_config = ConfigDict(extra='forbid')
    raw: str = Field(min_length=1, max_length=2_000_000)
    sender: str = Field(min_length=1, max_length=120)
    source_type: Literal['STANDARDS_DERIVED_SYNTHETIC', 'PUBLIC_EXAMPLE', 'USER_PROVIDED']
    group_id: str = Field(min_length=1, max_length=120)
    family: str = Field(min_length=1, max_length=120)
    split: Literal['TRAIN', 'VALIDATION', 'CALIBRATION', 'FROZEN_TEST']
    source_reference: str = Field(min_length=1, max_length=1000)
    declared: dict | None = None
    language: str = Field(min_length=2, max_length=20)
    country: str = Field(default='UNKNOWN', max_length=80)
    market: str = Field(default='UNKNOWN', max_length=80)
    population: str = Field(min_length=1, max_length=120)


def metadata(view):
    with store.connect() as c: row = c.execute('SELECT * FROM client_metadata WHERE event_id=?', (view['id'],)).fetchone()
    value = dict(row) if row else {'language': 'UNKNOWN', 'population': 'UNDECLARED'}
    value['input_type'] = ('LENIENT_ISO_RECOVERABLE' if view['context_kind'] == 'RECOVERED_REVIEW_CONTEXT' else
                           'PROWIDE_PARSEABLE' if any(m['payload']['parser'] == 'PROWIDE' for m in view['messages']) else 'UNSTRUCTURED_NOTICE')
    return value


@workflow_write
def import_rows(ident, rows, actor):
    jobs.member('imports', ident)  # Same bounded identifier contract.
    request_hash = digest(rows)
    with store.connect() as c: old = c.execute('SELECT * FROM client_imports WHERE id=?', (ident,)).fetchone()
    if old:
        if old['request_hash'] != request_hash: raise ValueError('Import idempotency-key collision')
        return json.loads(old['payload'])
    if not 1 <= len(rows) <= 1000: raise ValueError('Import 1–1000 rows per resumable batch')
    results = []
    # A batch receipt explicitly reports partial success. A bad row cannot
    # silently discard an earlier accepted message; retry is source-idempotent.
    for index, row in enumerate(rows):
        try:
            value = Message.model_validate(row); data = value.model_dump()
            meta = {k: data.pop(k) for k in ('language', 'country', 'market', 'population')}
            from iso_adapter.routing import route
            from iso_adapter.facts import project
            parsed = route(value.raw)
            identity = value.declared or {}
            if parsed['parser'] == 'PROWIDE':
                corp = [f['value'] for f in project(parsed['structure']) if f['name'] == 'corp']
                if len(set(corp)) != 1: raise ValueError('Ambiguous CORP')
                identity = {'corp': corp[0]}
            event_id = __import__('classifier.preprocessing', fromlist=['source_hash']).source_hash(value.sender + '\0' + identity.get('corp', ''))
            with store.connect() as c:
                locked = c.execute('SELECT 1 FROM client_freezes WHERE event_id=?', (event_id,)).fetchone()
                existing = c.execute('SELECT * FROM client_metadata WHERE event_id=?', (event_id,)).fetchone()
            if locked: raise ValueError('Event belongs to a frozen dataset; create a new corpus version')
            if existing and any(existing[k] != v for k, v in meta.items()): raise ValueError('Event population metadata is immutable')
            r = events.ingest(**data)
            with store.connect() as c:
                c.execute('INSERT OR IGNORE INTO client_metadata VALUES(?,?,?,?,?)', (r['event_id'], meta['language'], meta['country'], meta['market'], meta['population']))
            results.append({'row': index + 1, 'message_id': r['id'], 'event_id': r['event_id'], 'state': r['state']})
        except (ValueError, TypeError) as exc:
            # Schema errors without source-bearing Pydantic reprs.
            message = 'Invalid message schema' if hasattr(exc, 'errors') else str(exc)
            results.append({'row': index + 1, 'error': message})
    receipt = {'id': ident, 'request_hash': request_hash, 'rows': results,
               'accepted': sum('error' not in r for r in results), 'rejected': sum('error' in r for r in results),
               'semantics': 'Resumable per-row commits; inspect quarantined lifecycle states separately'}
    with store.connect() as c: c.execute('INSERT INTO client_imports VALUES(?,?,?,?,?)', (ident, store.now(), actor, request_hash, store.dumps(receipt)))
    audit(actor, 'CORPUS_IMPORT', {'id': ident, 'accepted': receipt['accepted'], 'rejected': receipt['rejected'], 'request_hash': request_hash})
    return receipt


def source_view(ident, *, blind=False):
    value = events.get(ident)
    value['latest_review_revision'] = value['reviews'][-1]['id'] if value['reviews'] else None
    if blind or value['split'] in ('CALIBRATION', 'FROZEN_TEST'):
        value['reviews'] = []; value['executions'] = []; value['blind'] = True
    value['client_metadata'] = metadata(value)
    return value


@workflow_write
def review(ident, body, user, *, ai=False):
    with store.connect() as c:
        if c.execute('SELECT 1 FROM client_freezes WHERE event_id=?', (ident,)).fetchone(): raise ValueError('Frozen labels cannot be edited')
    view = events.get(ident); data = dict(body)
    reference = data.pop('evaluation_time', None)
    if data.get('expected_deadline_status') is not None or data.get('expected_final_status') is not None:
        if reference is None: raise ValueError('Evaluation time is required for deadline/final-status labels')
        reference = reference_time(reference)
    if data.get('expected_final_status') is not None:
        from semantic_pipeline.decision import decide
        factors = {k: {'value': data['target'][k]} for k in events.PREDICATES}
        derived = decide(factors, {'status': data.get('expected_deadline_status') or 'UNKNOWN'}, data['target'].get('ambiguities', []))
        if derived['classification'] != data['expected_final_status']:
            raise ValueError('Final-status truth conflicts with factor labels, deadline or ambiguities')
    # The caller never chooses a human identity, provenance origin, or expertise.
    if ai:
        model_id = data.pop('model_id', None)
        if not model_id: raise ValueError('AI model identity required')
        origin = 'AI_AUTHORED'; expert = False
    else:
        model_id = None; expert = user['expert_attested']; origin = 'EXPERT_REVIEWED' if expert else 'HUMAN_REVIEWED'
    data['provenance'] = {'origin': origin, 'author': user['name'], 'model_id': model_id,
                          'method': 'Authenticated blind source review' if view['split'] in ('CALIBRATION', 'FROZEN_TEST') else 'Authenticated source review',
                          'reviewed_at': store.now(), 'expert_attested': expert, 'source_reference': 'client-event:' + ident,
                          'revision': str(data.get('expected_revision') or 'initial')}
    r = events.review(ident, data)
    with store.connect() as c:
        c.execute('INSERT INTO client_review_identity VALUES(?,?,?,?,?,?)', (r['id'], user['name'], int(expert), int(view['split'] in ('CALIBRATION', 'FROZEN_TEST')), 'AI' if ai else 'HUMAN', reference))
        if not ai:
            decisions = c.execute('SELECT * FROM client_decisions WHERE event_id=?', (ident,)).fetchall()
            for d in decisions:
                prior = json.loads(d['payload'])
                if prior['snapshot_hash'] != view['snapshot_hash'] or prior['decision']['review_required']: continue
                execution = c.execute('SELECT payload FROM learning_executions WHERE id=?', (prior['execution_id'],)).fetchone()
                before = json.loads(execution[0])['result']
                wrong = [k for k in events.PREDICATES if before['predicates'][k]['value'] != data['target'][k]]
                if data.get('expected_final_status') and before['decision']['classification'] != data['expected_final_status']: wrong.append('final_status')
                if data.get('expected_deadline_status') and before['deadline']['status'] != data['expected_deadline_status']: wrong.append('deadline_status')
                if wrong:
                    c.execute('INSERT INTO client_suspensions VALUES(NULL,?,?,?,?)', (store.now(), prior['decision']['qualification_id'], r['id'],
                              store.dumps({'reason': 'POST_RELEASE_VERIFIED_AUTO_ERROR', 'event_id': ident, 'fields': wrong})))
    audit(user['name'], 'LABEL_REVISION', {'event_id': ident, 'review_id': r['id'], 'origin': origin, 'snapshot_hash': view['snapshot_hash']})
    return r


@workflow_write
def freeze(ident, event_ids, actor):
    if not event_ids or len(set(event_ids)) != len(event_ids): raise ValueError('Explicit unique corpus membership required')
    views = [events.get(eid) for eid in event_ids]
    if any(not any(r['snapshot_hash'] == v['snapshot_hash'] for r in v['reviews']) for v in views):
        raise ValueError('Every corpus event needs a current reviewed label')
    with store.connect() as c:
        if any(c.execute('SELECT 1 FROM client_freezes WHERE event_id=?', (eid,)).fetchone() for eid in event_ids):
            raise ValueError('Event already frozen; version the corpus')
    output = jobs.member('event-datasets', ident)
    manifest = event_data.freeze_dataset(output, event_ids=event_ids)
    with store.connect() as c:
        c.execute('BEGIN IMMEDIATE')
        for view in views:
            eid = view['id']
            latest = next(r for r in reversed(view['reviews']) if r['snapshot_hash'] == view['snapshot_hash'])
            existing = c.execute('SELECT * FROM client_freezes WHERE event_id=?', (eid,)).fetchone()
            if existing: raise ValueError('Event already frozen; version the corpus')
            c.execute('INSERT INTO client_freezes VALUES(?,?,?,?)', (eid, view['snapshot_hash'], latest['id'], ident))
    audit(actor, 'DATASET_FROZEN', {'id': ident, 'manifest_sha256': sha(output / 'manifest.json'), 'n': len(event_ids)})
    return manifest


def calibrate(ident, *, dataset_id, release_id, population, reference, actor, check=None, stage='FINAL'):
    from production import confidence
    from production.qualification import decision_feature
    from training.framework.event_data import load_inputs, load_answers
    reference = reference_time(reference)
    dataset = jobs.member('event-datasets', dataset_id)
    manifest, inputs = load_inputs(dataset, 'CALIBRATION')
    if not inputs: raise ValueError('Calibration inputs required')
    release = jobs.member('releases', release_id); m, _ = releases.verify_seal(release)
    if stage not in ('FINAL','LAYA'):raise ValueError('Unknown calibration stage')
    if stage=='LAYA' and m['spec']['mode']!='LAYA_ONLY':raise ValueError('Specialist routing calibration requires a LAYA_ONLY release')
    from production.cascade_policy import stage_identity
    identity=stage_identity(m) if stage=='LAYA' else m['identity']
    partition='LAYA_STAGE' if stage=='LAYA' else 'CASCADE_FINAL' if m['spec'].get('laya_calibrator_id') else None
    if partition=='CASCADE_FINAL':
        prior=confidence.load(jobs.member('customer-calibrators',m['spec']['laya_calibrator_id']).with_suffix('.json'),stage_identity(m))
        if (prior.get('context') or {}).get('dataset_sha256')!=sha(dataset/'manifest.json'):
            raise ValueError('Cascade stage/final calibration requires disjoint partitions of the same frozen cohort')
    work = jobs.member('customer-calibration-runs', ident)
    from production.qualification import independent_groups
    groups = independent_groups(inputs)
    from production.evaluation import predict
    # Input-only loader; no live event/review capability is used here.
    manifest, inputs, predictions = predict(dataset, 'CALIBRATION', release, work, reference, check, calibration_partition=partition)
    if any(r['meta']['population'] != population for r in predictions): raise ValueError('Calibration population mismatch')
    if partition:
        from training.framework.event_data import load_calibration_answers
        truth=load_calibration_answers(dataset,manifest,partition,inputs)
    else:truth = load_answers(dataset, manifest, 'CALIBRATION', inputs)
    groups=independent_groups(inputs)
    records = []
    for row in predictions:
        key = truth[row['id']]; result = row['result']; meta = row['meta']
        with store.connect() as c:
            verified = c.execute('SELECT i.* FROM client_freezes f JOIN client_review_identity i ON i.review_id=f.review_id WHERE f.event_id=? AND f.dataset_id=?', (row['id'], dataset_id)).fetchone()
        authenticated = bool(verified and verified['expert'] and verified['blind'] and verified['source_kind'] == 'HUMAN')
        if verified and verified['evaluation_time'] != reference: raise ValueError('Calibration labels use a different evaluation time')
        real_source = all(m['payload']['source_type'] == 'USER_PROVIDED' for m in events.get(row['id'])['messages'])
        origin = key['provenance']['origin'] if authenticated and real_source else 'AI_ASSISTED_OR_UNAUTHENTICATED'
        # Split whole generation families; never disperse template variants.
        group = groups[row['id']]
        fold = 'FIT' if int(digest(group)[:8], 16) % 3 else 'EVALUATION'
        for pred in (*PREDICATES, 'final_decision'):
            f = (decision_feature(row['text'], result, meta) if pred == 'final_decision' else
                 confidence.feature_row(row['text'], pred, result['predicates'][pred], language=meta['language'], input_type=meta['input_type'], conflicts=result['reconciliation']['conflicts']))
            if pred == 'final_decision':
                if key.get('expected_final_status') is None: continue
                correct = result['decision']['classification'] == key['expected_final_status']
            else: correct = result['predicates'][pred]['value'] == key['target'][pred]
            records.append({'id': row['id'], 'role': 'CALIBRATION', 'fold': fold, 'group': group, 'predicate': pred,
                            'features': f['features'], 'correct': correct, 'origin': origin})
    out = jobs.WORKSPACE / 'customer-calibrators'; out.mkdir(parents=True, exist_ok=True)
    jobs.member('customer-calibrators', ident)
    payload = confidence.fit(records, identity=identity, population=population, output=out / (ident + '.json'),
                             context={'dataset_sha256':sha(dataset/'manifest.json'),'calibration_partition':partition or 'STANDALONE_FINAL'})
    write(work / 'features.json', records)
    audit(actor, 'CALIBRATOR_FITTED', {'id': ident, 'identity': identity, 'sha256': payload['sha256'],
                                    'stage':stage,'calibration_partition':partition or 'STANDALONE_FINAL'})
    return payload


def promote(ident, actor, expected_previous_id):
    from production.qualification import verify
    plan, receipt = verify(ident)
    if not receipt['customer_gate_passed']: raise ValueError('Customer quality gate not met: ' + ', '.join(receipt['reasons']))
    if actor in receipt['reviewers']: raise ValueError('Promotion requires an administrator independent of the test reviewers')
    with store.connect() as c:
        c.execute('BEGIN IMMEDIATE')
        if c.execute('SELECT 1 FROM client_suspensions WHERE qualification_id=?', (ident,)).fetchone():
            raise ValueError('Qualification suspended after a verified error; new independent qualification required')
        prior = c.execute('SELECT id FROM client_promotions ORDER BY id DESC LIMIT 1').fetchone()
        if (prior[0] if prior else None) != expected_previous_id: raise ValueError('Promotion revision conflict')
        c.execute('INSERT INTO client_promotions VALUES(NULL,?,?,?,?)', (store.now(), ident, expected_previous_id,
                  store.dumps({'actor': actor, 'qualification_sha256': digest(receipt), 'release_identity': plan['release_identity']})))
    audit(actor, 'CUSTOMER_RELEASE_PROMOTED', {'id': ident})
    return {'qualification_id': ident, 'promoted': True, 'automation_enabled': os.environ.get('AUTOMATION_ENABLED', 'false') == 'true'}


def select_operating_point(ident, *, campaign_id, candidate, dataset_id, calibrator_id, population, actor, stage='FINAL'):
    """Use persisted validation predictions only; never run/select on test data."""
    from production import confidence, operating
    from production.cascade_policy import stage_identity
    from training.framework.event_data import load_inputs, load_answers
    campaign=jobs.member('campaigns',campaign_id)
    state=json.loads((campaign/'result.json').read_text())
    if candidate not in state['candidates']:raise ValueError('Unknown validated candidate')
    release_id=state['candidates'][candidate]
    release=jobs.member('releases',release_id);m,_=releases.verify_seal(release)
    if stage not in ('FINAL','LAYA') or stage=='LAYA' and m['spec']['mode']!='LAYA_ONLY':
        raise ValueError('Invalid operating point stage')
    identity=stage_identity(m) if stage=='LAYA' else m['identity']
    cal=confidence.load(jobs.member('customer-calibrators',calibrator_id).with_suffix('.json'),identity)
    if cal['population']!=population:raise ValueError('Calibration population mismatch')
    out=campaign/('validation-'+candidate)
    report=json.loads((out/'evaluation.json').read_text());receipt=json.loads((out/'PREDICTIONS_SAVED.json').read_text())
    if report['role']!='VALIDATION' or report['release_identity']!=m['identity'] or sha(out/'predictions.jsonl')!=receipt['sha256']:
        raise ValueError('Validation prediction identity/integrity mismatch')
    dataset=jobs.member('event-datasets',dataset_id);manifest,inputs=load_inputs(dataset,'VALIDATION')
    if sha(dataset/'manifest.json')!=receipt['dataset_sha256']:raise ValueError('Validation dataset mismatch')
    truth=load_answers(dataset,manifest,'VALIDATION',inputs);members={r['id']:r for r in inputs}
    from production.qualification import assess, independent_groups
    groups=independent_groups(inputs);rows=[]
    predictions=[json.loads(line) for line in (out/'predictions.jsonl').read_text().splitlines()]
    if {r['id'] for r in predictions}!=set(members) or len(predictions)!=len(members):raise ValueError('Validation membership mismatch')
    for row in predictions:
        if row['snapshot_hash']!=members[row['id']]['snapshot_hash'] or row['text']!=members[row['id']]['text']:
            raise ValueError('Validation source mismatch')
        answer=truth[row['id']]
        if answer.get('expected_final_status') is None or answer.get('expected_deadline_status') is None:
            raise ValueError('Complete final/deadline truth needed for operating point selection')
        result=row['result'];a=assess(row['text'],result,row['meta'],cal,identity,.5)
        probs=[p['confidence'] for p in a['predicates'].values()]+[a['final_decision_confidence']]
        p=min(probs) if all(v is not None for v in probs) else None
        reasons=[r for r in a['review_reasons'] if not r.endswith(':LOW_OR_UNSUPPORTED_TRUST') and r!='FINAL_DECISION_TRUST_NOT_ESTABLISHED']
        pred={k:result['predicates'][k]['value'] for k in __import__('semantic_pipeline.schema',fromlist=['PREDICATES']).PREDICATES}
        target={k:answer['target'][k] for k in pred}
        exact=pred==target and result['decision']['classification']==answer['expected_final_status'] and result['deadline']['status']==answer['expected_deadline_status']
        rows.append({'id':row['id'],'role':'VALIDATION','group':groups[row['id']],'confidence':p,'force_review':bool(reasons),
                     'exact_correct':exact,'truth':target,'prediction':pred})
    folder=jobs.WORKSPACE/'customer-operating-points';folder.mkdir(parents=True,exist_ok=True)
    path=jobs.member('customer-operating-points',ident).with_suffix('.json')
    point=operating.select(rows,identity=identity,calibrator_hash=cal['sha256'],output=path)
    audit(actor,'OPERATING_POINT_SELECTED',{'id':ident,'sha256':point['sha256'],'status':point['status']})
    return point
