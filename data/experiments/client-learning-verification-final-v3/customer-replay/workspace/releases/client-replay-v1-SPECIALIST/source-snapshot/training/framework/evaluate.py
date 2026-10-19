"""Validation-only semantic evaluation of a registered candidate.

This command does not accept arbitrary answer-key paths or touch frozen tests.
The existing protected experiment harness remains the separate test authority.
"""
import json
from collections import Counter
from pathlib import Path

from semantic_pipeline.metrics import summarize
from semantic_pipeline.schema import PREDICATES
from training.framework.bundle import load_bundle, jsonl, write, sha
from training.framework.jobs import active_experiments, verify_plan


def evaluate_validation(job, output, model=None):
    if active_experiments() and model is None:
        raise ValueError('Timed model experiment active; defer candidate inference')
    root, plan = verify_plan(job, check_sources=False)
    _, data = load_bundle(plan['bundle'])
    selected = [e for e in data if e.split == 'VALIDATION']
    output = Path(output); output.mkdir(parents=True, exist_ok=False)
    if model is None:
        from training.framework.runtime import RegisteredModel
        model = RegisteredModel(root)
    # Persist every prediction without truth before scoring any assertion.
    predictions = []
    try:
        with (output / 'predictions.jsonl').open('x') as f:
            for e in selected:
                row = {'id': e.id, 'source_hash': e.source_hash, 'text': e.text, 'result': model.analyse(e.text)}
                f.write(json.dumps(row, ensure_ascii=False, allow_nan=False) + '\n'); f.flush()
                predictions.append(row)
    finally:
        if hasattr(model, 'close'): model.close()
    by = {e.id: e for e in selected}
    scored = [{**p, 'expected': {k: getattr(by[p['id']].target, k) for k in PREDICATES}} for p in predictions]
    metrics = summarize(scored)
    metrics.update(dataset_role='VALIDATION_ONLY', label_origins=dict(Counter(e.provenance.origin.value for e in selected)),
                   training_label_origins=plan['preflight']['label_origins'],
                   job_id=plan['job_id'], automation_enabled=False, customer_accuracy=None,
                   prediction_file_sha256=sha(output / 'predictions.jsonl'))
    write(output / 'metrics.json', metrics)
    from training.framework.jobs import events
    events(root, {'state': 'COMPLETED', 'kind': 'VALIDATION_EVALUATION',
                  'evaluation_path': str(output.resolve()), 'metrics_sha256': sha(output / 'metrics.json')})
    return metrics
