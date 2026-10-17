"""Append-only learning events, projected from Prowide (never the legacy parser).

Policy v1: REPL replaces the complete operative notification. Older supplements
belong to that notification's epoch and are retained in history, not silently
carried into the new one. Missing replacement facts are unresolved. Arrival
order cannot repair a stale PREV reference. Sender is an explicit namespace.
"""
import json
import uuid
import time
from pathlib import Path
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

from apps.api import store
from classifier.preprocessing import source_hash
from semantic_pipeline.schema import PREDICATES, SemanticResult
from training.framework.jobs import now
from training.framework.schema import Provenance

VERSION = 'prowide-event-state-v1'
ROLES = {'TRAIN', 'VALIDATION', 'CALIBRATION', 'FROZEN_TEST'}


def tables(c):
    # Call before opening the write transaction: executescript commits pending work.
    c.executescript('''
    CREATE TABLE IF NOT EXISTS learning_events(
      id TEXT PRIMARY KEY,sender TEXT NOT NULL,corp TEXT NOT NULL,split TEXT NOT NULL,
      group_id TEXT NOT NULL,family TEXT NOT NULL,created_at TEXT NOT NULL,
      UNIQUE(sender,corp));
    CREATE TABLE IF NOT EXISTS learning_messages(
      id INTEGER PRIMARY KEY AUTOINCREMENT,event_id TEXT NOT NULL REFERENCES learning_events(id),
      sender TEXT NOT NULL,seme TEXT NOT NULL,source_hash TEXT NOT NULL,raw_source TEXT NOT NULL,
      created_at TEXT NOT NULL,state TEXT NOT NULL,payload TEXT NOT NULL,UNIQUE(sender,seme));
    CREATE TABLE IF NOT EXISTS learning_executions(
      id TEXT PRIMARY KEY,event_id TEXT NOT NULL REFERENCES learning_events(id),
      snapshot_hash TEXT NOT NULL,created_at TEXT NOT NULL,job_id TEXT NOT NULL,payload TEXT NOT NULL);
    CREATE TABLE IF NOT EXISTS learning_reviews(
      id INTEGER PRIMARY KEY AUTOINCREMENT,event_id TEXT NOT NULL REFERENCES learning_events(id),
      snapshot_hash TEXT NOT NULL,previous_revision INTEGER REFERENCES learning_reviews(id),
      created_at TEXT NOT NULL,payload TEXT NOT NULL);
    ''')
    for table in ('learning_events', 'learning_messages', 'learning_executions', 'learning_reviews'):
        for action in ('UPDATE', 'DELETE'):
            c.execute(f"CREATE TRIGGER IF NOT EXISTS immutable_{table}_{action.lower()} BEFORE {action} ON {table} BEGIN SELECT RAISE(ABORT,'Learning history is immutable'); END")


def initialise(database=None):
    with store.connect(database) as c:
        tables(c)


def decode(row):
    return {**dict(row), 'payload': json.loads(row['payload'])}


def _view(c, event_id):
    meta = c.execute('SELECT * FROM learning_events WHERE id=?', (event_id,)).fetchone()
    if not meta:
        raise ValueError('Learning event not found')
    rows = [decode(r) for r in c.execute('SELECT * FROM learning_messages WHERE event_id=? ORDER BY id', (event_id,))]
    active = None; supplements = {}; cancelled = False; additive_chain = False
    for row in rows:
        p = row['payload']
        if row['state'] != 'APPLIED':
            continue
        if p['message_type'] in ('MT564', 'NOTICE'):
            if p['function'] == 'CANC':
                cancelled = True; supplements = {}
            else:
                active = row; supplements = {}; cancelled = False
        elif p['message_type'] == 'MT568':
            if p['function'] == 'NEWM' and p['previous_message_id'] in supplements:
                additive_chain = True
            if p['function'] in ('REPL', 'CANC') and p['previous_message_id'] in supplements:
                supplements.pop(p['previous_message_id'])
            if p['function'] != 'CANC':
                supplements[row['id']] = row
    operative = [] if cancelled or active is None else [active, *supplements.values()]
    current_ids = {m['id'] for m in operative}
    recovery_only = active is None and not cancelled
    semantic_messages = ([m for m in rows if m['payload']['message_type'] == 'RECOVERED']
                         if recovery_only else operative)
    history = [{**f, 'message_id': m['id'], 'seme': m['seme'], 'source_hash': m['source_hash'],
                'current': m['id'] in current_ids}
               for m in rows for f in m['payload']['facts']]
    pieces = []; spans = []; offset = 0
    for m in semantic_messages:
        prefix = f"[Message {m['seme']} | {m['payload']['message_type']}]\n"
        body = m['raw_source'] if recovery_only else m['payload']['narrative']
        segment = prefix + body
        pieces.append(segment)
        spans.append({'message_id': m['id'], 'seme': m['seme'], 'start': offset + len(prefix),
                      'end': offset + len(segment), 'source_hash': m['source_hash']})
        offset += len(segment) + 2
    text = '\n\n'.join(pieces)
    # New additive-chain resolution invalidates any old review of an affected
    # chain. Unaffected existing event snapshots/labels retain their identity.
    policy = VERSION + '+supplement-additions-v2' if additive_chain else VERSION
    snapshot = source_hash(store.dumps({'policy': policy, 'messages': [(m['id'], m['source_hash'], m['state']) for m in rows]}))
    return {**dict(meta), 'snapshot_hash': snapshot, 'policy': policy, 'cancelled': cancelled,
            'active_notification_id': active['id'] if active else None,
            'operative_message_ids': sorted(current_ids), 'current_text': text,
            'semantic_message_ids': [m['id'] for m in semantic_messages],
            'context_kind': 'RECOVERED_REVIEW_CONTEXT' if recovery_only and semantic_messages else 'OPERATIVE_EVENT',
            'current_text_hash': source_hash(text), 'source_ranges': spans,
            'facts': history, 'messages': rows,
            'warnings': [i for m in rows if m['state'] == 'QUARANTINED' for i in m['payload']['issues']],
            'manual_review_required': True, 'automation_enabled': False, 'customer_accuracy': None}


def get(event_id, database=None):
    initialise(database)
    with store.connect(database) as c:
        value = _view(c, event_id)
        value['executions'] = [decode(r) for r in c.execute('SELECT * FROM learning_executions WHERE event_id=? ORDER BY rowid', (event_id,))]
        value['reviews'] = [decode(r) for r in c.execute('SELECT * FROM learning_reviews WHERE event_id=? ORDER BY id', (event_id,))]
        return value


def listing(database=None):
    initialise(database)
    with store.connect(database) as c:
        return [dict(r) for r in c.execute('SELECT * FROM learning_events ORDER BY created_at DESC,id')]


def ingest(raw, *, sender, source_type, group_id, family, split, source_reference,
           declared=None, database=None):
    if not raw.strip() or len(raw) > 2_000_000 or not sender.strip() or not source_reference:
        raise ValueError('Nonempty bounded source, sender and source provenance required')
    if split not in ROLES or source_type not in {'STANDARDS_DERIVED_SYNTHETIC', 'PUBLIC_EXAMPLE', 'USER_PROVIDED'}:
        raise ValueError('Unknown split or source type')
    from iso_adapter.routing import route
    from iso_adapter.facts import project
    parsed = route(raw)
    facts = project(parsed['structure']) if parsed['parser'] == 'PROWIDE' else []
    def one(key):
        values = [f['value'] for f in facts if f['name'] == key]
        unique = set(store.dumps(v) for v in values)
        if len(unique) > 1:
            raise ValueError('Ambiguous structured identity: ' + key)
        return values[0] if values else None
    if parsed['parser'] == 'PROWIDE':
        identity = {key: one(key) for key in ('seme', 'corp', 'prev', 'function')}
        mt = parsed['structure']['message_type']
        if declared and any(declared.get(k) not in (None, v) for k, v in identity.items()):
            raise ValueError('Declared identity conflicts with Prowide components')
    else:
        if not declared or not declared.get('corp') or not declared.get('seme'):
            raise ValueError('Non-authoritative input needs explicit external CORP/SEME identity')
        identity = {key: declared.get(key) for key in ('seme', 'corp', 'prev', 'function')}
        identity['function'] = identity['function'] or 'NEWM'
        mt = 'NOTICE' if parsed['parser'] == 'NOT_APPLICABLE' else 'RECOVERED'
    if not identity['seme'] or not identity['corp']:
        raise ValueError('Unambiguous CORP and SEME required')
    corp = identity['corp']; seme = identity['seme']; prev = identity['prev']; fn = identity['function']
    eid = source_hash(sender + '\0' + corp)
    initialise(database)
    with store.connect(database) as c:
        c.execute('BEGIN IMMEDIATE')
        existing = c.execute('SELECT * FROM learning_messages WHERE sender=? AND seme=?', (sender, seme)).fetchone()
        if existing:
            if existing['source_hash'] != source_hash(raw):
                raise ValueError('SEME collision; original source retained')
            return decode(existing)
        meta = c.execute('SELECT * FROM learning_events WHERE id=?', (eid,)).fetchone()
        if meta and (meta['split'], meta['group_id'], meta['family']) != (split, group_id, family):
            raise ValueError('Event split/family identity is frozen')
        if not meta:
            # Family/group identities are partition units, even across different CORPs.
            conflict = c.execute('SELECT 1 FROM learning_events WHERE (group_id=? OR family=?) AND split<>?', (group_id, family, split)).fetchone()
            if conflict: raise ValueError('Family/group split leakage')
            c.execute('INSERT INTO learning_events VALUES(?,?,?,?,?,?,?)', (eid, sender, corp, split, group_id, family, now()))
        view = _view(c, eid)
        linked = c.execute('SELECT * FROM learning_messages WHERE sender=? AND seme=?', (sender, prev)).fetchone() if prev else None
        issues = []; previous = linked['id'] if linked else None
        active = view['active_notification_id']
        if mt == 'RECOVERED': issues.append('Recovered identity/context is non-authoritative; lifecycle quarantined')
        if mt in ('MT564', 'NOTICE'):
            if fn == 'NEWM' and active: issues.append('Second NEWM needs explicit replacement linkage')
            elif fn in ('REPL', 'CANC') and (not linked or linked['event_id'] != eid or linked['id'] != active or view['cancelled']):
                issues.append('Replacement/cancellation must reference the active notification')
            elif fn not in ('NEWM', 'REPL', 'CANC'): issues.append('Unsupported notification function')
        elif mt == 'MT568':
            allowed = view['operative_message_ids']
            if not linked or linked['event_id'] != eid or linked['id'] not in allowed or view['cancelled']:
                issues.append('Supplement must reference a current message in this event')
            elif fn in ('REPL', 'CANC') and linked['id'] == active:
                issues.append('Narrative replacement/cancellation cannot replace the notification')
            elif fn not in ('NEWM', 'REPL', 'CANC'): issues.append('Unsupported narrative function')
        state = 'QUARANTINED' if issues else 'APPLIED' if mt in ('MT564', 'MT568', 'NOTICE') else 'OBSERVATION'
        payload = {'parser': parsed['parser'], 'input_type': parsed['input_type'], 'structure': parsed.get('structure'),
                   'message_type': mt, 'function': fn, 'previous_reference': prev, 'previous_message_id': previous,
                   'facts': facts, 'narrative': parsed['narrative'], 'issues': issues, 'warnings': parsed['warnings'],
                   'source_type': source_type, 'source_reference': source_reference, 'adapter_version': VERSION}
        cur = c.execute('INSERT INTO learning_messages(event_id,sender,seme,source_hash,raw_source,created_at,state,payload) VALUES(?,?,?,?,?,?,?,?)',
                        (eid, sender, seme, source_hash(raw), raw, now(), state, store.dumps(payload)))
        return decode(c.execute('SELECT * FROM learning_messages WHERE id=?', (cur.lastrowid,)).fetchone())


def evidence_links(view, quote, *, require_context=True):
    """Evidence must occur in an operative raw message AND the operative context."""
    if not quote or (require_context and quote not in view['current_text']):
        return []
    links = []
    for m in view['messages']:
        if m['id'] not in view.get('semantic_message_ids', view['operative_message_ids']): continue
        start = m['raw_source'].find(quote)
        if start >= 0:
            links.append({'message_id': m['id'], 'seme': m['seme'], 'source_hash': m['source_hash'],
                          'start': start, 'end': start + len(quote), 'text': quote, 'valid': True})
    return links


class Review(BaseModel):
    model_config = ConfigDict(extra='forbid')
    snapshot_hash: str
    expected_revision: int | None = None
    target: SemanticResult
    provenance: Provenance
    notes: str = Field(default='', max_length=10000)
    expected_deadline_status: Literal['OPEN', 'PASSED', 'UNKNOWN'] | None = None
    expected_final_status: Literal['VOTABLE', 'NOT_VOTABLE', 'VOTABLE_WITH_RESTRICTION', 'DEADLINE_PASSED', 'UNCERTAIN_MANUAL_REVIEW'] | None = None


def review(event_id, value, database=None):
    value = Review.model_validate(value)
    initialise(database)
    with store.connect(database) as c:
        c.execute('BEGIN IMMEDIATE')
        view = _view(c, event_id)
        if view['snapshot_hash'] != value.snapshot_hash: raise ValueError('Event changed; reopen current state before review')
        old = c.execute('SELECT id FROM learning_reviews WHERE event_id=? ORDER BY id DESC LIMIT 1', (event_id,)).fetchone()
        if (old['id'] if old else None) != value.expected_revision: raise ValueError('Review revision conflict')
        if view['cancelled'] or not view['current_text']: raise ValueError('No active event to label')
        evidence = {}
        for key in PREDICATES:
            quotes = getattr(value.target.evidence, key)
            if getattr(value.target, key) in ('YES', 'VOTABLE') and not quotes:
                raise ValueError('Positive review requires source evidence: ' + key)
            evidence[key] = []
            for quote in quotes:
                links = evidence_links(view, quote)
                if not links: raise ValueError('Review evidence is not an exact operative raw-source substring')
                evidence[key].extend(links)
        d = value.target.deadline_information.deadline_text
        if d is not None and not evidence_links(view, d): raise ValueError('Invalid deadline evidence')
        prior = c.execute('SELECT * FROM learning_executions WHERE event_id=? AND snapshot_hash=? ORDER BY rowid DESC LIMIT 1', (event_id, value.snapshot_hash)).fetchone()
        previous = decode(prior) if prior else None
        payload = value.model_dump(mode='json')
        payload.update(evidence_links=evidence, previous_prediction=previous,
                       validation_type='AI_ASSISTED_NOT_HUMAN_GOLD' if value.provenance.origin.value.startswith('AI_') else value.provenance.origin.value,
                       ai_exact_match=(all(previous['payload']['result']['predicates'][k]['value'] == getattr(value.target, k) for k in PREDICATES) if previous else None))
        cur = c.execute('INSERT INTO learning_reviews(event_id,snapshot_hash,previous_revision,created_at,payload) VALUES(?,?,?,?,?)',
                        (event_id, value.snapshot_hash, value.expected_revision, now(), store.dumps(payload)))
        return decode(c.execute('SELECT * FROM learning_reviews WHERE id=?', (cur.lastrowid,)).fetchone())


def classify(event_id, job, *, reference, database=None, model=None):
    view = get(event_id, database)
    if view['cancelled'] or not view['current_text']: raise ValueError('Event has no operative classification context')
    from iso_adapter.facts import semantic_facts, deadline
    active = next((m for m in view['messages'] if m['id'] == view['active_notification_id']), None)
    structure = active['payload'].get('structure') if active and active['payload']['parser'] == 'PROWIDE' else None
    structured = semantic_facts(structure) if structure else {}
    explicit = deadline(structure, reference) if structure else None
    if explicit and not explicit['comparisons']: explicit = None
    owns = model is None
    if owns:
        from training.framework.runtime import RegisteredModel
        model = RegisteredModel(job)
    try:
        started = time.perf_counter()
        try:
            result = model.analyse(view['current_text'], reference=reference, use_iso=False,
                                   structured_context=structured, deadline_override=explicit)
        except (ValueError, RuntimeError, OSError) as exc:
            # A failed inference is still an auditable event. Do not fabricate a
            # successful model answer or discard an otherwise valid source.
            from semantic_pipeline.decision import decide
            factors = {k: {'value': 'UNCERTAIN' if k == 'votability' else 'UNKNOWN',
                          'source': 'MODEL_EXECUTION_FAILED', 'confidence': None, 'scores': {}, 'evidence': []} for k in PREDICATES}
            d = explicit or {'status': 'UNKNOWN'}
            result = {'architecture': 'REGISTERED_EXECUTION_FAILED', 'predicates': factors,
                      'reconciliation': {'predicates': factors, 'conflicts': ['MODEL_EXECUTION_FAILED']},
                      'deadline': d, 'decision': decide(factors, d, ['MODEL_EXECUTION_FAILED']),
                      'execution_error': {'type': type(exc).__name__, 'message': str(exc)},
                      'llm': None, 'latencies': {'total_ms': (time.perf_counter() - started) * 1000},
                      'automation_enabled': False, 'customer_accuracy': None}
    finally:
        if owns: model.close()
    for key in PREDICATES:
        pred = result['predicates'][key]
        for ev in pred.get('evidence', []):
            links = evidence_links(view, ev.get('text'), require_context=not pred.get('source', '').startswith('PROWIDE'))
            ev['event_source_links'] = links
            ev['valid'] = bool(links)
            if not links:
                result['reconciliation']['conflicts'].append(key + ':EVENT_EVIDENCE_INVALID')
    if result['reconciliation']['conflicts']:
        from semantic_pipeline.decision import decide
        result['decision'] = decide(result['predicates'], result['deadline'], result['reconciliation']['conflicts'])
    if view['context_kind'] == 'RECOVERED_REVIEW_CONTEXT':
        from semantic_pipeline.decision import decide
        result['reconciliation']['conflicts'].append('RECOVERED_CONTEXT_NOT_AUTHORITATIVE')
        result['decision'] = decide(result['predicates'], result['deadline'], result['reconciliation']['conflicts'], quarantined=True)
    if view['warnings']:
        result['decision']['review_reasons'].extend(view['warnings'])
    result.update(event_id=event_id, event_snapshot_hash=view['snapshot_hash'], event_policy=view['policy'],
                  event_context_kind=view['context_kind'])
    from qwen_domain.confidence import confidence_output, decision_confidence
    result['confidence'] = {k: confidence_output(view['current_text'], k, result['predicates'][k],
                            deterministic_conflict=bool(result['reconciliation']['conflicts'])) for k in PREDICATES}
    result['decision_confidence'] = decision_confidence(result['decision']['classification'], result['confidence'])
    ident = str(uuid.uuid4())
    payload = {'result': result, 'input': view['current_text'], 'source_ranges': view['source_ranges'],
               'operative_message_ids': view['operative_message_ids']}
    with store.connect(database) as c:
        c.execute('INSERT INTO learning_executions VALUES(?,?,?,?,?,?)',
                  (ident, event_id, view['snapshot_hash'], now(), Path(job).name, store.dumps(payload)))
    return {'id': ident, 'payload': payload}
