"""Protected release scoring, correctness calibration and coverage diagnostics."""
import json
import os
from collections import Counter
from pathlib import Path

from semantic_pipeline.metrics import summarize
from semantic_pipeline.schema import PREDICATES
from training.framework import jobs, releases
from training.framework.event_data import load_inputs
from training.framework.bundle import sha, write


def evaluate(dataset, release, output, *, role='VALIDATION', reference='2026-10-17T12:00:00+00:00',
             model_factory=None, selection_id=None, database=None, check=None):
    if role not in ('VALIDATION', 'CALIBRATION', 'FROZEN_TEST'): raise ValueError('Independent evaluation role required')
    m, rows = load_inputs(dataset, role)
    if not rows: raise ValueError('Evaluation role is empty')
    config = releases.verify(release)
    sealed = role == 'FROZEN_TEST'
    if sealed:
        h = releases.history(database)
        if not h or h[-1]['id'] != selection_id or h[-1]['release_id'] != Path(release).name:
            raise ValueError('Select and freeze the complete release before opening test answers')
        releases.verify_seal(release)
    output = Path(output); output.mkdir(parents=True, exist_ok=False)
    write(output / 'plan.json', {'role': role, 'dataset_sha256': sha(Path(dataset) / 'manifest.json'),
          'release_identity': config['identity'], 'reference': reference, 'selection_id': selection_id,
          'answer_keys_opened': False, 'created_at': jobs.now()})
    model = (model_factory or (lambda p: releases.ReleaseModel(p, sealed=sealed)))(release)
    predictions = []
    try:
        with (output / 'predictions.jsonl').open('x') as f:
            for row in rows:
                if check: check()
                from iso_adapter.facts import semantic_facts, deadline
                struct = row.get('active_structure')
                explicit = deadline(struct, reference) if struct else None
                result = model.analyse(row['text'], use_iso=False, reference=reference,
                            structured_context=semantic_facts(struct) if struct else {},
                            deadline_override=explicit if explicit and explicit['comparisons'] else None)
                if row.get('context_kind') == 'RECOVERED_REVIEW_CONTEXT':
                    from semantic_pipeline.decision import decide
                    result['reconciliation']['conflicts'].append('RECOVERED_CONTEXT_NOT_AUTHORITATIVE')
                    result['decision'] = decide(result['predicates'], result['deadline'], result['reconciliation']['conflicts'], quarantined=True)
                value = {'id': row['id'], 'text': row['text'], 'source_hash': row['source_hash'],
                         'group_id': row['group_id'], 'family': row['generation_family'], 'result': result}
                f.write(json.dumps(value, ensure_ascii=False, allow_nan=False) + '\n'); f.flush(); os.fsync(f.fileno())
                predictions.append(value)
    finally: model.close()
    write(output / 'BLIND_PREDICTIONS_PERSISTED.json', {'prediction_sha256': sha(output / 'predictions.jsonl'),
          'n': len(predictions), 'release_identity': config['identity'], 'persisted_at': jobs.now(), 'keys_opened': False})
    # This is deliberately the first label access, after durable predictions.
    keys = Path(dataset) / 'private/answer_keys.jsonl'
    if m['answer_file'] != 'private/answer_keys.jsonl' or sha(keys) != m['answer_sha256']:
        raise ValueError('Answer key checksum changed')
    truth = {r['id']: r for r in map(json.loads, keys.read_text().splitlines())}
    for row in rows:
        if truth[row['id']]['snapshot_hash'] != row['snapshot_hash']: raise ValueError('Evaluation truth snapshot mismatch')
    scored = [{**r, 'expected': {k: truth[r['id']]['target'][k] for k in PREDICATES}} for r in predictions]
    metrics = summarize(scored); failures = []; transitions = {k: Counter() for k in PREDICATES}
    critical_misses = []
    for row in predictions:
        target = truth[row['id']]['target']; result = row['result']
        for k in PREDICATES:
            before = (result.get('laya') or result)['predicates'][k]['value'] == target[k]
            after = result['predicates'][k]['value'] == target[k]
            transitions[k][('correct' if before else 'wrong') + ' → ' + ('correct' if after else 'wrong')] += 1
            if not after:
                failures.append({'id': row['id'], 'text': row['text'], 'predicate': k, 'truth': target[k],
                                 'prediction': result['predicates'][k], 'escalation': result['escalation'],
                                 'reconciliation': result['reconciliation']})
                if k in ('votability', 'share_blocking', 'poa_required', 'registration_required') and target[k] in ('YES', 'VOTABLE'):
                    critical_misses.append({'id': row['id'], 'predicate': k, 'truth': target[k],
                                            'prediction': result['predicates'][k]['value']})
    for field, actual in [('expected_final_status', lambda r: r['decision']['classification']),
                           ('expected_deadline_status', lambda r: r['deadline']['status'])]:
        labelled = [(r, truth[r['id']][field]) for r in predictions if truth[r['id']].get(field) is not None]
        metrics[field] = {'support': len(labelled), 'correct': sum(actual(r['result']) == t for r, t in labelled)}
    report = {'role': role, 'release_identity': config['identity'], 'metrics': metrics,
              'label_origins': dict(Counter(truth[r['id']]['provenance']['origin'] for r in predictions)),
              'llm_calls': sum(bool(r['result'].get('llm_stage')) for r in predictions),
              'llm_call_rate': sum(bool(r['result'].get('llm_stage')) for r in predictions) / len(predictions),
              'semantic_review_count': sum(r['result'].get('semantic_review_required', True) for r in predictions),
              'critical_false_negatives': critical_misses,
              'repair_damage': {k: dict(v) for k, v in transitions.items()}, 'failures': failures,
              'prediction_receipt_sha256': sha(output / 'BLIND_PREDICTIONS_PERSISTED.json'),
              'automation_enabled': False, 'customer_accuracy': None}
    write(output / 'evaluation.json', report)
    return report


def calibrate(evaluation, output):
    """Never fit on validation/frozen results; evaluate separate family folds."""
    evaluation = Path(evaluation); m = json.loads((evaluation / 'evaluation.json').read_text())
    plan = json.loads((evaluation / 'plan.json').read_text())
    receipt = json.loads((evaluation / 'BLIND_PREDICTIONS_PERSISTED.json').read_text())
    if m['role'] != 'CALIBRATION' or plan['role'] != 'CALIBRATION': raise ValueError('Use CALIBRATION only')
    if sha(evaluation / 'predictions.jsonl') != receipt['prediction_sha256']: raise ValueError('Calibration predictions changed')
    # Correctness labels come from the persisted, already scored CALIBRATION
    # errors, never a second model's invented labels.
    errors = {(f['id'], f['predicate']) for f in m['failures']}
    misses = {(f['id'], f['predicate']) for f in m['critical_false_negatives']}
    from qwen_domain.confidence import CorrectnessCalibrator
    from training.framework.calibration import predicate_confidence
    records = []
    for row in map(json.loads, (evaluation / 'predictions.jsonl').read_text().splitlines()):
        fold = 'FIT' if int(releases.digest(row['family'])[:8], 16) % 2 else 'EVALUATION'
        for k in PREDICATES:
            result = row['result']; p = result['predicates'][k]
            records.append({'split': 'CALIBRATION', 'predicate': k, 'duplicate_group': row['group_id'],
                'calibration_fold': fold, 'correct': (row['id'], k) not in errors,
                'critical_false_negative': (row['id'], k) in misses,
                'features': predicate_confidence(row['text'], k, p, conflict=bool(result['reconciliation']['conflicts']))['features']})
    cal = CorrectnessCalibrator(m['release_identity']); reports = cal.fit(records)
    root = Path(output); root.mkdir(parents=True, exist_ok=False)
    cal.save(root / 'calibrator.joblib')
    write(root / 'features.json', records)
    summary = {'release_identity': m['release_identity'], 'evaluation_sha256': sha(evaluation / 'evaluation.json'),
               'prediction_sha256': receipt['prediction_sha256'], 'reports': reports, 'valid_predicates': sorted(cal.models),
               'support_policy': '100 fit / 50 evaluation per predicate; family-isolated; correctness-class support gates retained',
               'scope': 'AI-authored synthetic population only; not customer confidence', 'automation_enabled': False}
    write(root / 'calibration.json', summary)
    return summary


def coverage(evaluation, calibrator):
    """Held-out calibration EVALUATION only; no fitting/threshold selection here."""
    from qwen_domain.confidence import CorrectnessCalibrator
    root = Path(calibrator); m = json.loads((root / 'calibration.json').read_text())
    cal = CorrectnessCalibrator.load(root / 'calibrator.joblib', m['release_identity'])
    rows = json.loads((root / 'features.json').read_text())
    heldout = [r for r in rows if r['calibration_fold'] == 'EVALUATION']
    tables = []
    for threshold in [.7, .8, .9, .95, .98]:
        accepted = [(r, cal.predict(r['predicate'], r['features'], m['release_identity'])) for r in heldout]
        accepted = [(r, p) for r, p in accepted if p is not None and p >= threshold and not r['features'].get('unknown')
                    and not r['features'].get('contradiction') and not r['features'].get('ood')]
        tables.append({'threshold': threshold, 'support': len(heldout), 'accepted': len(accepted),
                       'coverage': len(accepted) / len(heldout) if heldout else 0,
                       'correct': sum(r['correct'] for r, _ in accepted),
                       'correctness': sum(r['correct'] for r, _ in accepted) / len(accepted) if accepted else None,
                       'critical_false_negatives': sum(r['critical_false_negative'] for r, _ in accepted),
                       'would_review_fraction': 1 - len(accepted) / len(heldout) if heldout else None,
                       'simulation_only': True})
    write(root / 'coverage.json', tables)
    return tables
