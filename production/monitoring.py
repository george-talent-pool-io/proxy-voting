"""Reproducible random audits, independent of the model's confidence.

The installation-local secret prevents input authors choosing an event ID to
avoid sampling. Only otherwise releasable decisions enter this sampler.
"""
import fcntl
import hashlib
import hmac
import os
from training.framework import jobs

VERSION = 'accepted-decision-audit-v1'


def installation_key():
    jobs.WORKSPACE.mkdir(parents=True, exist_ok=True)
    path = jobs.WORKSPACE / 'audit-selection.key'
    with path.open('a+b') as f:
        os.fchmod(f.fileno(), 0o600)
        fcntl.flock(f, fcntl.LOCK_EX)
        f.seek(0); key = f.read()
        if not key:
            key = os.urandom(32); f.write(key); f.flush(); os.fsync(f.fileno())
        if len(key) != 32: raise ValueError('Invalid audit selection key; do not silently replace it')
    return key


def select(identity, rate, *, key):
    if not .01 <= rate <= .5: raise ValueError('Audit rate must be between 1% and 50%')
    value = hmac.new(key, (VERSION + '\0' + identity).encode(), hashlib.sha256).digest()
    draw = int.from_bytes(value[:8], 'big') / 2**64
    return {'version': VERSION, 'rate': rate, 'selected': draw < rate,
            'selection_receipt': value.hex(), 'pre_audit_eligible': True,
            'meaning': 'Random audit of an otherwise accepted decision; separate from low-confidence review'}


def apply(decision, identity, rate, *, key=None):
    if decision['review_required'] or not decision.get('automation_enabled'): return decision
    selection = select(identity, rate, key=key if key is not None else installation_key())
    decision['audit_selection'] = selection
    if selection['selected']:
        decision['review_required'] = True
        decision['review_reasons'] = list(decision['review_reasons']) + ['RANDOM_ACCEPTED_DECISION_AUDIT']
    return decision


def verified_errors(prior, source, target, *, reference, expected_deadline=None, expected_final=None):
    """Audit the original semantic decision without treating elapsed time as error."""
    from semantic_pipeline.schema import PREDICATES
    from production.service import reference_time
    d = prior['decision']
    accepted = not d['review_required'] or bool(d.get('audit_selection', {}).get('pre_audit_eligible'))
    if not accepted or not d.get('qualification_id'): return []
    wrong = [k for k in PREDICATES if source['predicates'][k]['value'] != target[k]]
    original_time = source.get('evaluation_time') or d.get('evaluation_time')
    same_time = bool(reference and original_time and reference_time(reference) == reference_time(original_time))
    if same_time:
        if expected_deadline and source['deadline']['status'] != expected_deadline: wrong.append('deadline_status')
        if expected_final and source['decision']['classification'] != expected_final: wrong.append('final_status')
    return wrong
