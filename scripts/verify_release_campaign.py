"""Real bounded release-campaign acceptance. AI labels, never customer accuracy.

Prepare first, then explicitly dispatch. This script never opens challenge keys.
The completed driver receipt can be inspected without re-running training.
"""
import argparse
import json
from dataclasses import asdict
from pathlib import Path

from fast_cascade.routing import Policy
from training.framework import jobs, campaigns
from training.framework.bundle import write


def prepare(ident, reuse_completed_from=None, dataset_id='event-loop-isolated-v2'):
    source = json.loads(Path('artifacts/event-learning-real-proof-v2.json').read_text())
    laya = json.loads(Path('training/framework/specs/laya.json').read_text())
    laya.update(epochs=3, batch_size=1, gradient_accumulation=1, learning_rate=.0001)
    qwen = json.loads(Path('training/framework/specs/qwen38-mlx.json').read_text())
    qwen.update(max_steps=2, batch_size=1, gradient_accumulation=1)
    spec = {'bundle_id': 'event-loop-v1', 'dataset_id': dataset_id,
            'actor': 'AI engineering acceptance / controlled construction labels', 'max_seconds': 7200,
            'stages': [{'name': 'baseline_laya', 'reuse_job': source['jobs']['Laya']},
                       {'name': 'laya_3epoch', 'training': laya},
                       {'name': 'baseline_qwen', 'reuse_job': source['jobs']['Qwen']},
                       {'name': 'qwen_2step', 'training': qwen}],
            'candidates': [{'name': 'BASE_LAYA', 'mode': 'LAYA_ONLY', 'laya_stage': 'baseline_laya'},
                           {'name': 'TRAINED_LAYA', 'mode': 'LAYA_ONLY', 'laya_stage': 'laya_3epoch'},
                           {'name': 'BASE_QWEN', 'mode': 'QWEN_ONLY', 'llm_stage': 'baseline_qwen'},
                           {'name': 'TRAINED_QWEN', 'mode': 'QWEN_ONLY', 'llm_stage': 'qwen_2step'},
                           {'name': 'CASCADE_CONSERVATIVE', 'mode': 'LAYA_QWEN', 'laya_stage': 'laya_3epoch', 'llm_stage': 'qwen_2step'},
                           {'name': 'CASCADE_MODERATE', 'mode': 'LAYA_QWEN', 'laya_stage': 'laya_3epoch', 'llm_stage': 'qwen_2step',
                            'policy': asdict(Policy('MODERATE', .9, .4, .98, .9, .6, True, False))}]}
    if reuse_completed_from:
        previous = campaigns.status(jobs.member('campaigns', reuse_completed_from))
        if previous['state'] not in ('INTERRUPTED', 'FAILED', 'COMPLETED'):
            raise ValueError('The earlier campaign must be terminal before explicit recovery')
        completed = {s['name']: s['reuse_job'] for s in previous['plan']['spec']['stages'] if s['reuse_job']}
        completed.update({e['stage']: e['job_id'] for e in previous['events'] if e.get('phase') == 'JOB_PREPARED'})
        for name, job_id in completed.items():
            if jobs.status(jobs.member('jobs', job_id))['state'] != 'COMPLETED': raise ValueError('Stage is not reusable: ' + name)
        spec['stages'] = [{'name': s['name'], 'reuse_job': completed[s['name']]} for s in spec['stages']]
    result = campaigns.prepare(spec, jobs.member('campaigns', ident))
    if reuse_completed_from:
        jobs.events(jobs.member('campaigns', ident), {'state': 'PREPARED', 'kind': 'EXPLICIT_RECOVERY',
                    'previous_campaign': reuse_completed_from, 'optimizer_resume': False, 'retraining': False})
    return result


if __name__ == '__main__':
    p = argparse.ArgumentParser(); p.add_argument('id'); p.add_argument('--dispatch', action='store_true')
    p.add_argument('--reuse-completed-from')
    p.add_argument('--dataset-id', default='event-loop-isolated-v2')
    a = p.parse_args()
    if a.dispatch: print(json.dumps(campaigns.spawn(jobs.member('campaigns', a.id))))
    else:
        r = prepare(a.id, a.reuse_completed_from, a.dataset_id); print(json.dumps({'id': r['id'], 'state': r['state']}))
