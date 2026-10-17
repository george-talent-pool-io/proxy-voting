"""Same-input candidate comparison. Persist blind predictions before opening keys.

CALIBRATION is a separate correctness-calibration capability, never a training
bundle. Sparse support produces null confidence, not an invented probability.
"""
import json
import os
from collections import Counter
from pathlib import Path

from semantic_pipeline.metrics import summarize
from semantic_pipeline.schema import PREDICATES
from training.framework.bundle import sha, write
from training.framework.event_data import load_inputs, load_answers
from training.framework import jobs, events


def identity(job):
    _, plan = jobs.verify_plan(job, check_sources=False)
    from training.framework.runtime import RUNTIME_SHA256
    return {'model_manifest_sha256': sha(Path(job) / 'model-manifest.json'),
            'prompt_sha256': sha(Path(plan['bundle']) / 'semantic-prompt.txt'),
            'event_policy': events.VERSION, 'runtime_sha256': RUNTIME_SHA256}


def compare(dataset, candidates, output, *, role='VALIDATION', reference='2026-10-17T12:00:00+00:00',
            selection_id=None, database=None, model_factory=None):
    if not candidates: raise ValueError('No comparison candidates')
    if model_factory is None and jobs.active_experiments(): raise ValueError('Timed benchmark active; comparison deferred')
    manifest, inputs = load_inputs(dataset, role)
    if not inputs: raise ValueError('No inputs for requested role')
    if role == 'TRAIN': raise ValueError('Use independent development/held-out roles for comparison')
    if role == 'FROZEN_TEST':
        from training.framework.selection import history
        h = history(database)
        if not h or h[-1]['id'] != selection_id: raise ValueError('Freeze an explicit experimental selection before test scoring')
    if model_factory is None:
        from training.framework.runtime import RegisteredModel
        model_factory = RegisteredModel
    root = Path(output); root.mkdir(parents=True, exist_ok=False)
    ids = {name: identity(job) for name, job in candidates.items()}
    plan = {'created_at': jobs.now(), 'role': role, 'dataset_sha256': sha(Path(dataset) / 'manifest.json'),
            'input_sha256': manifest['input_sha256'], 'candidates': ids, 'selection_id': selection_id,
            'reference': reference, 'answer_keys_opened': False, 'automation_enabled': False}
    write(root / 'comparison-plan.json', plan)
    outputs = {}
    for name, job in candidates.items():
        if not name.replace('_', '').isalnum(): raise ValueError('Invalid comparison candidate name')
        rows = []; model = model_factory(job)
        try:
            with (root / (name + '-predictions.jsonl')).open('x') as f:
                for r in inputs:
                    from iso_adapter.facts import semantic_facts, deadline
                    struct = r.get('active_structure')
                    kwargs = {'use_iso': False, 'reference': reference,
                              'structured_context': semantic_facts(struct) if struct else {}}
                    explicit = deadline(struct, reference) if struct else None
                    if explicit and explicit['comparisons']: kwargs['deadline_override'] = explicit
                    result = model.analyse(r['text'], **kwargs)
                    if r.get('context_kind') == 'RECOVERED_REVIEW_CONTEXT':
                        from semantic_pipeline.decision import decide
                        result['reconciliation']['conflicts'].append('RECOVERED_CONTEXT_NOT_AUTHORITATIVE')
                        result['decision'] = decide(result['predicates'], result['deadline'], result['reconciliation']['conflicts'], quarantined=True)
                    value = {'id': r['id'], 'source_hash': r['source_hash'], 'text': r['text'], 'result': result}
                    f.write(json.dumps(value, ensure_ascii=False, allow_nan=False) + '\n'); f.flush(); os.fsync(f.fileno())
                    rows.append(value)
        finally: model.close()
        outputs[name] = rows
    receipt = {'persisted_at': jobs.now(), 'prediction_files': {name: sha(root / (name + '-predictions.jsonl')) for name in candidates},
               'rows_per_candidate': len(inputs), 'keys_opened': False}
    write(root / 'BLIND_PREDICTIONS_PERSISTED.json', receipt)
    # First label access in this function happens strictly AFTER every candidate's
    # predictions and their immutable checksum receipt have been flushed to disk.
    dataset = Path(dataset)
    truth = load_answers(dataset, manifest, role, inputs)
    for r in inputs:
        if r['id'] not in truth or truth[r['id']]['snapshot_hash'] != r['snapshot_hash']:
            raise ValueError('Truth/input snapshot mismatch')
    metrics = {}; failures = []; transitions = {}
    baseline = next(iter(outputs))
    for name, rows in outputs.items():
        scored = [{**r, 'expected': {k: truth[r['id']]['target'][k] for k in PREDICATES}} for r in rows]
        m = summarize(scored)
        final = [(r['result']['decision']['classification'], truth[r['id']]['expected_final_status']) for r in rows if truth[r['id']]['expected_final_status'] is not None]
        dates = [(r['result']['deadline']['status'], truth[r['id']]['expected_deadline_status']) for r in rows if truth[r['id']]['expected_deadline_status'] is not None]
        m.update(final_status={'correct': sum(a == b for a, b in final), 'support': len(final)},
                 deadline_status={'correct': sum(a == b for a, b in dates), 'support': len(dates)},
                 model_identity=ids[name], role=role, label_origins=dict(Counter(truth[r['id']]['provenance']['origin'] for r in rows)),
                 customer_accuracy=None, automation_enabled=False)
        metrics[name] = m
        byfield = {k: Counter() for k in PREDICATES}
        for before, after in zip(outputs[baseline], rows):
            if before['id'] != after['id']: raise ValueError('Comparison input order changed')
            t = truth[after['id']]['target']
            for k in PREDICATES:
                a = before['result']['predicates'][k]['value'] == t[k]
                b = after['result']['predicates'][k]['value'] == t[k]
                byfield[k][('correct' if a else 'wrong') + ' → ' + ('correct' if b else 'wrong')] += 1
                if not b:
                    failures.append({'candidate': name, 'id': after['id'], 'text': after['text'], 'predicate': k, 'truth': t[k],
                                     'prediction': after['result']['predicates'][k], 'decision': after['result']['decision']})
            for field, actual in [('expected_deadline_status', after['result']['deadline']['status']),
                                   ('expected_final_status', after['result']['decision']['classification'])]:
                expected = truth[after['id']].get(field)
                if expected is not None and actual != expected:
                    failures.append({'candidate': name, 'id': after['id'], 'text': after['text'], 'field': field,
                                     'truth': expected, 'prediction': actual, 'scores': None, 'confidence': None,
                                     'deadline': after['result']['deadline'], 'decision': after['result']['decision']})
        transitions[name] = {k: dict(v) for k, v in byfield.items()}
        if role == 'CALIBRATION':
            from qwen_domain.confidence import CorrectnessCalibrator, features
            cal = CorrectnessCalibrator(ids[name]); records = []
            for r, inp in zip(rows, inputs):
                for k in PREDICATES:
                    records.append({'split': 'CALIBRATION', 'predicate': k, 'duplicate_group': inp['group_id'],
                                    'calibration_fold': 'FIT' if int(__import__('hashlib').sha256(inp['generation_family'].encode()).hexdigest()[:8], 16) % 2 else 'EVALUATION',
                                    'correct': r['result']['predicates'][k]['value'] == truth[r['id']]['target'][k],
                                    'features': features(r['text'], k, r['result']['predicates'][k])['features']})
            m['calibration'] = cal.fit(records)
            cal.save(root / (name + '-calibrator.joblib'))
            m['calibrator_valid_predicates'] = sorted(cal.models)
    report = {'role': role, 'metrics': metrics, 'baseline_for_transitions': baseline,
              'repair_damage': transitions, 'failures': failures, 'predictions_receipt_sha256': sha(root / 'BLIND_PREDICTIONS_PERSISTED.json'),
              'selection_id': selection_id, 'customer_accuracy': None, 'automation_enabled': False}
    write(root / 'comparison.json', report)
    if role == 'VALIDATION':
        for name, job in candidates.items():
            # A small standalone metric receipt is compatible with model selection.
            _, jobplan = jobs.verify_plan(job, check_sources=False)
            folder = root / name; folder.mkdir()
            write(folder / 'metrics.json', {**metrics[name], 'job_id': jobplan['job_id']})
            jobs.events(job, {'state': 'COMPLETED', 'kind': 'VALIDATION_EVALUATION', 'evaluation_path': str(folder.resolve()),
                              'metrics_sha256': sha(folder / 'metrics.json')})
    return report
