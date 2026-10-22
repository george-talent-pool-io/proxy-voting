"""Predeclared, independently scored customer automation qualification.

Bounds use independent event-family groups, with a group counted as wrong if
any accepted event/positive in that group is wrong. Bonferroni allocation covers
the auto-precision and four critical-recall claims. Thresholds are not fitted on
this test. Statistical bounds do not establish population representativeness.
"""
import json
import math
from collections import Counter
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field
from scipy.stats import beta
from apps.api import store
from production import confidence
from production.storage import digest
from semantic_pipeline.schema import PREDICATES
from training.framework import jobs, releases
from training.framework.bundle import write, sha

CRITICAL = ('votability', 'share_blocking', 'poa_required', 'registration_required')


class Policy(BaseModel):
    model_config = ConfigDict(extra='forbid', allow_inf_nan=False)
    threshold: float = Field(default=.99, ge=.5, le=1)
    min_test_groups: int = Field(default=500, ge=100)
    min_auto_groups: int = Field(default=300, ge=100)
    min_positive_groups: int = Field(default=300, ge=50)
    min_auto_precision_lower_bound: float = Field(default=.98, ge=.9, lt=1)
    min_critical_recall_lower_bound: float = Field(default=.98, ge=.9, lt=1)
    max_review_rate: float = Field(default=.1, ge=0, le=1)
    confidence_level: float = Field(default=.95, ge=.9, lt=1)
    validity_days: int = Field(default=90, ge=1, le=180)
    random_audit_rate: float = Field(default=.02, ge=.01, le=.5)


def lower_bound(correct, total, alpha):
    if not total or not correct: return 0.0
    return float(beta.ppf(alpha, correct, total - correct + 1))


def independent_groups(rows):
    """Connected components of families, declared groups and lexical duplicates."""
    from training.split import duplicate_groups
    from training.framework.event_data import content
    duplicates = duplicate_groups([{'text': content(r['text'])} for r in rows])
    parent = list(range(len(rows))); seen = {}
    def find(i):
        while i != parent[i]: parent[i] = parent[parent[i]]; i = parent[i]
        return i
    for i, (row, duplicate) in enumerate(zip(rows, duplicates)):
        for key in [('family', row['generation_family']), ('group', row['group_id']), ('duplicate', duplicate)]:
            if key in seen: parent[find(i)] = find(seen[key])
            else: seen[key] = i
    return {r['id']: 'group-' + str(find(i)) for i, r in enumerate(rows)}


def repair_count(result):
    return int(((result.get('llm') or {}).get('schema_handling') or {}).get('repair_attempts',0))


def predicate_feature(text,key,result,meta):
    repairs=repair_count(result)
    f=confidence.feature_row(text,key,result['predicates'][key],language=meta['language'],input_type=meta['input_type'],
        conflicts=result['reconciliation']['conflicts'],schema_valid=not bool(result.get('execution_error')),schema_repairs=repairs)
    f['force_review'] |= bool(repairs)
    if repairs:f['features']['source']+=':SCHEMA_REPAIRED'
    f['confidence_explanation']['schema_repairs']=repairs
    return f


def decision_feature(text, result, meta):
    ev = [e for p in result['predicates'].values() for e in p.get('evidence', [])]
    status = result['decision']['classification']
    f = confidence.feature_row(text, 'final_decision', {'value': status, 'evidence': ev, 'source': result.get('architecture', 'UNKNOWN')},
                              language=meta['language'], input_type=meta['input_type'], conflicts=result['reconciliation']['conflicts'],schema_repairs=repair_count(result))
    f['force_review'] |= status == 'UNCERTAIN_MANUAL_REVIEW'
    for key in PREDICATES:
        pred = result['predicates'][key]
        scores = sorted((pred.get('scores') or {}).values(), reverse=True)
        f['features'].update({key + '_value': pred['value'], key + '_margin': scores[0] - scores[1] if len(scores) > 1 else None,
                              key + '_evidence': any(e.get('valid') for e in pred.get('evidence', []))})
    f['features']['deadline_status'] = result['deadline']['status']
    f['features']['source'] += ':LLM_INVOKED' if (result.get('llm') or {}).get('invoked') else ':SPECIALIST_OR_RULES_ONLY'
    if repair_count(result):
        f['features']['source']+=':SCHEMA_REPAIRED';f['force_review']=True
    return f


def assess(text, result, meta, calibrator, identity, threshold):
    out = {}; reasons = []
    scope_ok = calibrator['population'] == meta['population']
    if not scope_ok: reasons.append('POPULATION_NOT_IN_CALIBRATION_SCOPE')
    if repair_count(result):reasons.append('LLM_SCHEMA_REPAIR_REQUIRES_REVIEW')
    for key in PREDICATES:
        pred = result['predicates'][key]
        f = predicate_feature(text,key,result,meta)
        probability = confidence.predict(calibrator, key, f, identity=identity, population=meta['population']) if scope_ok else None
        out[key] = {'value': pred['value'], 'confidence': probability,
                    'kind': 'CALIBRATED_IN_DECLARED_POPULATION' if probability is not None else 'HEURISTIC / NOT YET CALIBRATED',
                    'band': f['heuristic_band'], 'evidence': pred.get('evidence', []), 'explanation': f['confidence_explanation']}
        out[key]['negative_basis']=pred.get('negative_basis') if f['features']['complete_source_negative'] else None
        # For operational processing, all requested fields matter, even when a
        # final-status rule could short circuit a restriction.
        if probability is None or probability < threshold: reasons.append(key + ':LOW_OR_UNSUPPORTED_TRUST')
        if f['force_review']: reasons.append(key + ':UNRESOLVED_OR_OOD')
        if not any(e.get('valid') for e in pred.get('evidence', [])) and not f['features']['complete_source_negative']:
            reasons.append(key + ':EVIDENCE_UNAVAILABLE')
    final_feature = decision_feature(text, result, meta)
    final = confidence.predict(calibrator, 'final_decision', final_feature, identity=identity, population=meta['population']) if scope_ok else None
    if final is None or final < threshold: reasons.append('FINAL_DECISION_TRUST_NOT_ESTABLISHED')
    if result.get('execution_error'): reasons.append('MODEL_EXECUTION_FAILED')
    if result['predicates']['votability']['value'] == 'VOTABLE' and result['deadline']['status'] == 'UNKNOWN':
        reasons.append('VOTING_DEADLINE_UNRESOLVED')
    if result.get('event_context_kind') == 'RECOVERED_REVIEW_CONTEXT': reasons.append('NON_AUTHORITATIVE_RECOVERY')
    return {'predicates': out, 'final_decision_confidence': final, 'eligible': not reasons,
            'review_reasons': sorted(set(reasons)), 'confidence_scope': meta['population']}


def statistics(records, policy):
    p = Policy.model_validate(policy)
    if not records: raise ValueError('No qualification examples')
    if len({r['id'] for r in records}) != len(records): raise ValueError('Duplicate qualification record')
    groups = {r['group'] for r in records}
    accepted = [r for r in records if r['accepted']]
    by_group = {}
    for r in accepted: by_group.setdefault(r['group'], []).append(r)
    # Exact complete-output correctness, not just final-status correctness.
    good = sum(all(r['exact_correct'] for r in values) for values in by_group.values())
    alpha = (1 - p.confidence_level) / (1 + len(CRITICAL))
    precision = lower_bound(good, len(by_group), alpha)
    recall = {}
    for key in CRITICAL:
        positive = 'VOTABLE' if key == 'votability' else 'YES'
        positives = [r for r in records if r['truth'][key] == positive]
        clustered = {}
        for r in positives: clustered.setdefault(r['group'], []).append(r)
        correct_groups = sum(all(r['prediction'][key] == positive for r in v) for v in clustered.values())
        recall[key] = {'positive_support': len(positives), 'positive_groups': len(clustered),
                       'true_positives': sum(r['prediction'][key] == positive for r in positives),
                       'false_negatives': sum(r['prediction'][key] != positive for r in positives),
                       'recall_lower_bound': lower_bound(correct_groups, len(clustered), alpha)}
    reasons = []
    if len(groups) < p.min_test_groups: reasons.append('INSUFFICIENT_INDEPENDENT_TEST_GROUPS')
    if len(by_group) < p.min_auto_groups: reasons.append('INSUFFICIENT_AUTO_ACCEPT_GROUPS')
    if precision < p.min_auto_precision_lower_bound: reasons.append('AUTO_PRECISION_LOWER_BOUND_NOT_MET')
    rate = 1 - len(accepted) / len(records)
    total_review = rate + (1 - rate) * p.random_audit_rate
    if total_review > p.max_review_rate: reasons.append('REVIEW_RATE_TARGET_NOT_MET')
    for key, m in recall.items():
        if m['positive_groups'] < p.min_positive_groups: reasons.append(key + ':INSUFFICIENT_POSITIVE_GROUPS')
        if m['recall_lower_bound'] < p.min_critical_recall_lower_bound: reasons.append(key + ':RECALL_LOWER_BOUND_NOT_MET')
    from semantic_pipeline.metrics import field_metrics
    fields = {k: field_metrics([r['truth'][k] for r in records], [r['prediction'][k] for r in records],
                               'VOTABLE' if k == 'votability' else 'YES') for k in PREDICATES}
    return {'cases': len(records), 'independent_groups': len(groups), 'accepted': len(accepted), 'per_predicate': fields,
            'all_fields_exact_correct': sum(r['exact_correct'] for r in records),
            'accepted_groups': len(by_group), 'wrong_auto_processed': sum(not r['exact_correct'] for r in accepted),
            'measured_auto_precision': sum(r['exact_correct'] for r in accepted) / len(accepted) if accepted else None,
            'auto_precision_lower_bound': precision, 'review_rate': rate,
            'expected_total_review_rate_including_audits': total_review,
            'random_audit_rate_of_otherwise_accepted': p.random_audit_rate,
            'review_rate_scope': 'review_rate is confidence/evidence review before random audits; total is the policy expected rate, not a realised finite-sample guarantee',
            'critical': recall,
            'statistical_gate_passed': not reasons, 'reasons': reasons,
            'bound_method': 'One-sided exact binomial bounds on worst-outcome independent groups; Bonferroni over five claims',
            'policy': p.model_dump()}


def root(ident): return jobs.member('customer-qualifications', ident)


def prepare(ident, *, release_id, dataset_id, calibrator_path, population, policy, reference, actor):
    from training.framework.event_data import load_inputs
    from production.service import reference_time
    reference = reference_time(reference)
    with store.connect() as c:
        if c.execute("SELECT 1 FROM client_qualification_plans WHERE json_extract(payload,'$.dataset_id')=?", (dataset_id,)).fetchone():
            raise ValueError('Frozen dataset already reserved for qualification; do not tune or select on reused test answers')
    release = jobs.member('releases', release_id); m, sealed = releases.verify_seal(release)
    path = Path(calibrator_path).resolve()
    # Only service-created calibrators in a dedicated artifact directory.
    if path.parent != (jobs.WORKSPACE / 'customer-calibrators').resolve(): raise ValueError('Unmanaged calibrator path')
    cal = confidence.load(path, m['identity'])
    if cal['population'] != population: raise ValueError('Population mismatch')
    dataset = jobs.member('event-datasets', dataset_id); manifest, membership = load_inputs(dataset, 'FROZEN_TEST')
    if not membership: raise ValueError('An independent frozen test is required')
    with store.connect() as c:
        locks = {r['event_id']: dict(r) for r in c.execute('SELECT * FROM client_freezes WHERE dataset_id=?', (dataset_id,))}
    if any(r['id'] not in locks or locks[r['id']]['snapshot_hash'] != r['snapshot_hash'] for r in membership):
        raise ValueError('Frozen membership/review locks are required')
    with store.connect() as c:
        for x in membership:
            row = c.execute('SELECT evaluation_time FROM client_review_identity WHERE review_id=?', (locks[x['id']]['review_id'],)).fetchone()
            if not row or row[0] != reference: raise ValueError('Frozen labels use a different evaluation time')
    groups = independent_groups(membership)
    r = root(ident); r.mkdir(parents=True, exist_ok=False)
    (r / 'calibrator.json').write_bytes(path.read_bytes())
    plan = {'version': 'customer-qualification-v1', 'id': ident, 'release_id': release_id, 'release_identity': m['identity'],
            'release_seal_sha256': sha(release / 'SEALED.json'), 'dataset_id': dataset_id, 'dataset_manifest_sha256': sha(dataset / 'manifest.json'),
            'calibrator_sha256': sha(r / 'calibrator.json'), 'population': population, 'policy': Policy.model_validate(policy).model_dump(),
            'actor': actor, 'reference': reference, 'created_at': store.now(), 'source_hashes': source_hashes(),
            'membership': [{'id': x['id'], 'snapshot_hash': x['snapshot_hash'], 'review_id': locks[x['id']]['review_id'], 'independent_group': groups[x['id']]} for x in membership],
            'representativeness': 'Customer operator must attest population sampling; statistics cannot prove representativeness'}
    write(r / 'plan.json', plan)
    with store.connect() as c: c.execute('INSERT INTO client_qualification_plans VALUES(?,?)', (ident, store.dumps(plan)))
    return plan


def source_hashes():
    return {p.name: sha(p) for p in sorted(Path(__file__).parent.glob('*.py'))}


def verify_plan(ident):
    plan = json.loads((root(ident) / 'plan.json').read_text())
    with store.connect() as c: row = c.execute('SELECT payload FROM client_qualification_plans WHERE id=?', (ident,)).fetchone()
    if not row or json.loads(row[0]) != plan or plan['source_hashes'] != source_hashes():
        raise ValueError('Qualification plan/source changed; prepare a new condition')
    return plan


def evaluate(ident, check=None):
    """One explicit run; save every model prediction before opening truth."""
    from training.framework import events
    r = root(ident); plan = verify_plan(ident)
    release = jobs.member('releases', plan['release_id']); m, _ = releases.verify_seal(release)
    dataset = jobs.member('event-datasets', plan['dataset_id'])
    if sha(release / 'SEALED.json') != plan['release_seal_sha256'] or sha(dataset / 'manifest.json') != plan['dataset_manifest_sha256']:
        raise ValueError('Frozen qualification artifacts changed')
    if sha(r / 'calibrator.json') != plan['calibrator_sha256']: raise ValueError('Calibrator changed')
    cal = confidence.load(r / 'calibrator.json', m['identity']); rows = []
    from production.evaluation import predict
    from production.service import metadata
    _, _, predictions = predict(dataset, 'FROZEN_TEST', release, r / 'blind', plan['reference'], check)
    members = {x['id']: x for x in plan['membership']}
    for row in predictions:
        member = members[row['id']]
        if row['snapshot_hash'] != member['snapshot_hash']: raise ValueError('Frozen event changed')
        result = row['result']
        assessment = assess(row['text'], result, row['meta'], cal, m['identity'], plan['policy']['threshold'])
        rows.append({'id': row['id'], 'snapshot_hash': row['snapshot_hash'], 'group': member['independent_group'],
                     'prediction': {k: result['predicates'][k]['value'] for k in PREDICATES},
                     'final': result['decision']['classification'], 'deadline': result['deadline']['status'],
                     'accepted': assessment['eligible'], 'assessment': assessment})
    # The full raw model stages live in blind/predictions.jsonl, durable before truth.
    prediction_path = r / 'blind' / 'predictions.jsonl'
    write(r / 'PREDICTIONS_SAVED.json', {'sha256': sha(prediction_path), 'count': len(rows), 'created_at': store.now(), 'plan_sha256': sha(r / 'plan.json')})
    eligibility = []; reviewers = set()
    with store.connect() as c:
        for pred, member in zip(rows, plan['membership']):
            review = c.execute('SELECT * FROM learning_reviews WHERE id=?', (member['review_id'],)).fetchone()
            attestation = c.execute('SELECT * FROM client_review_identity WHERE review_id=?', (member['review_id'],)).fetchone()
            target = json.loads(review['payload']); truth = target['target']
            if not attestation or not attestation['expert'] or not attestation['blind'] or attestation['source_kind'] != 'HUMAN': eligibility.append('INDEPENDENT_AUTHENTICATED_EXPERT_LABELS_REQUIRED')
            if attestation: reviewers.add(attestation['actor'])
            provenance = target['provenance']
            if provenance['origin'] != 'EXPERT_REVIEWED': eligibility.append('SYNTHETIC_OR_NONEXPERT_TEST_LABELS')
            if target.get('expected_final_status') is None or target.get('expected_deadline_status') is None: eligibility.append('COMPLETE_FINAL_AND_DEADLINE_TRUTH_REQUIRED')
            view = events.get(pred['id'])
            if any(x['payload']['source_type'] != 'USER_PROVIDED' for x in view['messages']): eligibility.append('REPRESENTATIVE_CLIENT_SOURCE_REQUIRED')
            if metadata(view)['population'] != plan['population']: eligibility.append('TEST_POPULATION_MISMATCH')
            pred['truth'] = {k: truth[k] for k in PREDICATES}
            pred['exact_correct'] = (all(pred['prediction'][k] == truth[k] for k in PREDICATES) and pred['final'] == target.get('expected_final_status') and pred['deadline'] == target.get('expected_deadline_status'))
    if set(cal['label_origins']) != {'EXPERT_REVIEWED'}: eligibility.append('EXPERT_CALIBRATION_REQUIRED')
    if cal.get('support_policy', confidence.SupportPolicy().model_dump()) != confidence.SupportPolicy().model_dump():
        eligibility.append('NON_STANDARD_CALIBRATION_SUPPORT_POLICY')
    metrics = statistics(rows, plan['policy'])
    reasons = sorted(set(metrics['reasons'] + eligibility))
    receipt = {'id': ident, 'plan_sha256': sha(r / 'plan.json'), 'predictions_sha256': sha(r / 'blind' / 'predictions.jsonl'),
               'release_identity': m['identity'], 'created_at': store.now(), 'expires_at': (datetime.now(timezone.utc) + timedelta(days=plan['policy']['validity_days'])).isoformat(),
               'population': plan['population'], 'metrics': metrics, 'customer_gate_passed': not reasons, 'reasons': reasons,
               'reviewers': sorted(reviewers), 'automation_enabled': False, 'customer_accuracy': None,
               'scope': 'Measured held-out population only; not a guarantee on arbitrary future notices'}
    write(r / 'qualification.json', receipt)
    write(r / 'scored.json', rows)
    with store.connect() as c: c.execute('INSERT INTO client_qualifications VALUES(?,?,?)', (ident, store.now(), store.dumps(receipt)))
    return receipt


def verify(ident):
    r = root(ident); receipt = json.loads((r / 'qualification.json').read_text()); plan = verify_plan(ident)
    with store.connect() as c: saved = c.execute('SELECT payload FROM client_qualifications WHERE id=?', (ident,)).fetchone()
    if not saved or json.loads(saved[0]) != receipt or sha(r / 'plan.json') != receipt['plan_sha256'] or sha(r / 'blind' / 'predictions.jsonl') != receipt['predictions_sha256']:
        raise ValueError('Qualification integrity mismatch')
    release = jobs.member('releases', plan['release_id']); m, _ = releases.verify_seal(release)
    if m['identity'] != receipt['release_identity'] or sha(release / 'SEALED.json') != plan['release_seal_sha256'] or sha(r / 'calibrator.json') != plan['calibrator_sha256']:
        raise ValueError('Qualified model/calibrator identity changed')
    if sha(jobs.member('event-datasets', plan['dataset_id']) / 'manifest.json') != plan['dataset_manifest_sha256']:
        raise ValueError('Qualified dataset changed')
    if datetime.fromisoformat(receipt['expires_at']) <= datetime.now(timezone.utc): raise ValueError('Qualification expired; requalification required')
    return plan, receipt
