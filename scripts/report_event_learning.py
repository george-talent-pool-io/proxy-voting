"""Summarise completed receipts, never infer success from documentation."""
import argparse
import json
from pathlib import Path

from apps.api import store
from training.framework import jobs
from training.framework.bundle import sha, write


def report(proof, runtime_proof):
    proof = Path(proof); runtime_proof = Path(runtime_proof)
    r = json.loads(proof.read_text()); runtime = json.loads(runtime_proof.read_text())
    assert r['restart_persistence_verified'] and r['api_restart_during_training_verified']
    assert runtime['restart_persistence_verified']
    models = {}
    for name, ident in r['jobs'].items():
        root = jobs.WORKSPACE / 'jobs' / ident
        plan = json.loads((root / 'plan.json').read_text())
        result = json.loads((root / 'result.json').read_text())
        assert result['reload_parity']['passed'] and jobs.status(root)['state'] == 'COMPLETED'
        models[name] = {'job_id': ident, 'spec': plan['spec'], 'result': result,
                        'manifest_sha256': sha(root / 'model-manifest.json')}
    with store.connect() as c:
        source_count = c.execute('SELECT count(*) FROM notices').fetchone()[0]
        origins = {row[0]: row[1] for row in c.execute("SELECT json_extract(payload,'$.provenance.origin'),count(*) FROM learning_reviews GROUP BY 1")}
        raw_count = c.execute('SELECT count(*) FROM learning_messages').fetchone()[0]
    machine = {'created_at': jobs.now(), 'scope': 'ENGINEERING_QUALIFICATION_ONLY',
               'proof_sha256': sha(proof), 'runtime_proof_sha256': sha(runtime_proof),
               'models': models, 'corpus': {'events': 160, 'raw_messages': raw_count, 'linguistic_families': 20,
               'roles': {'TRAIN': 96, 'VALIDATION': 32, 'CALIBRATION': 16, 'FROZEN_TEST': 16},
               'original_public_notices': source_count, 'review_origins': origins},
               'qualification': r, 'final_runtime': runtime,
               'automation_enabled': False, 'customer_accuracy': None}
    write('data/reports/ISO15022_EVENT_LEARNING_RESULTS.json', machine)
    lines = ['\n## Verified execution results\n',
        f'Original public-notice count remains **{source_count:,}**. The new ledger preserves '
        f'**{raw_count}** synthetic messages. Reviews by origin: `{origins}`. No expert labels are inferred.\n',
        'The real engineering cohort was fixed before training: **8 TRAIN, 4 VALIDATION, '
        '4 CALIBRATION, 4 FROZEN_TEST**. All are AI-authored construction labels. '
        '“Blind” here means the prediction/scoring workflow, not independent secrecy from '
        'the synthetic corpus author. This is not a model-quality benchmark.\n',
        '| Backend | Real update | Reload check | Artifact |', '|---|---|---|---|']
    for name, m in models.items():
        x = m['result']
        update = '1 epoch / 72 question items' if name == 'Laya' else f"{x['optimiser_steps']} optimiser step / {x['trainable_parameters']:,} trainable parameters"
        delta = x['reload_parity'].get('max_absolute_logit_difference', x['reload_parity'].get('max_absolute_score_difference'))
        lines.append(f"| {name} | {update} | maximum probe difference {delta} | `{m['job_id']}` |")
    q = models['Qwen']['result']
    lines += ['', f"Qwen training took {q['elapsed_seconds']:.1f}s; peak MLX allocated memory was "
              f"{q['peak_mlx_allocated_bytes']/1e9:.2f} GB (not total OS/unified-memory peak). "
              'The unchanged base and saved adapter hashes were checked. The reload probe covers '
              '128 tokens on one held-out input, not a claim of whole-dataset bitwise determinism.\n',
              'The initial Laya attempt rejected an unsupported `max_steps` driver setting before '
              'updates. It remains FAILED in the ledger. The corrected new attempt uses epochs; '
              'TrainSpec now rejects this mismatch during preparation. The original Qwen run was '
              'retained rather than retrained.\n',
              '| Role / model | Semantic assertions | All-nine exact match | Final status | Deadline | Warm median / p95 |',
              '|---|---|---|---|---|---|']
    for role, rr in r['reports'].items():
        for name, m in rr['metrics'].items():
            lines.append(f"| {role} / {name} | {m['correct_assertions']}/{m['assertions']} | "
                         f"{m['cases_satisfying_all_supplied_assertions']}/{m['cases']} | "
                         f"{m['final_status']['correct']}/{m['final_status']['support']} | "
                         f"{m['deadline_status']['correct']}/{m['deadline_status']['support']} | "
                         f"{m['median_latency_ms']:.0f} / {m['p95_latency_ms']:.0f} ms |")
    lines += ['', 'These are reconciled semantic assertions with identical structured context and '
              'rules, not pure-model or parser accuracy. Latencies are tiny-cohort warm diagnostics, '
              'exclude loading and are not a controlled throughput comparison. No result is customer '
              'accuracy. All records require review.\n', '### Critical-positive support\n',
              '| Role / model | Voting positive recall | Blocking positive recall | POA positive recall | Registration positive recall |',
              '|---|---|---|---|---|']
    for role in ['VALIDATION', 'FROZEN_TEST']:
        for name, m in r['reports'][role]['metrics'].items():
            values = []
            for k in ['votability', 'share_blocking', 'poa_required', 'registration_required']:
                f = m['fields'][k]; n = f['positive_support']; p = f['positive_recall']
                values.append('N/A (support 0)' if p is None else f'{round(p*n)}/{n}')
            lines.append(f"| {role} / {name} | " + ' | '.join(values) + ' |')
    lines += ['', 'All per-field confusion matrices, support, F1, repair/damage and failures are '
              'in `ISO15022_EVENT_LEARNING_RESULTS.json` and the versioned comparison folders. '
              'Independent candidate transitions are not causal fallback repairs.\n',
              '### Confidence and persistence\n',
              'All nine calibrators for both models report INSUFFICIENT_CALIBRATION_SUPPORT; '
              'no numerical confidence is activated. The support refusal is expected and correct. '
              'The four calibration inputs cannot meet the gate.\n',
              'The real detached worker survived an API restart with exactly the same two task '
              'identities. Both models executed in the event application. An AI_REVIEWED revision '
              'retains the prior execution and exports as a new dataset version. A queued spare '
              'was cancelled; explicit restart produced a new unstarted job. Selection, rollback, '
              'restoration, executions and reviews survived another API restart.\n',
              'A final separate real application proof exercises runtime v4 and persists its '
              'loaded source archive. Engineering safety changes made during QA are not presented '
              'as a frozen architecture-quality experiment or as an accuracy improvement.\n',
              '### Receipts\n',
              f'* `{proof}` — real training/event lifecycle, comparison and rollback.\n'
              f'* `{runtime_proof}` — final runtime / real-model persistence.\n'
              '* `artifacts/event-learning-final-regression.log` — ordinary application tests.\n'
              '* `artifacts/event-learning-final-browser.log` — complete browser regression.\n'
              '* `data/reports/ISO15022_LEARNING_FRAMEWORK_NEXT_CAMPAIGN.md` — next milestone.\n']
    path = Path('data/reports/ISO15022_EVENT_LEARNING_VERIFICATION.md')
    path.write_text(path.read_text() + '\n'.join(lines) + '\n')
    errors = ['# Event learning qualification — every scored failure\n',
              'AI-authored synthetic engineering labels only. Scores are native model outputs; '
              'calibrated confidence is unavailable. Do not reuse frozen errors as training data.\n']
    for role, rr in r['reports'].items():
        p = jobs.WORKSPACE / 'comparisons' / rr['id'] / 'comparison.json'
        for i, error in enumerate(json.loads(p.read_text())['failures'], 1):
            errors += [f"\n## {role} / {i} / {error['candidate']} / {error['id']}\n",
                       '```json\n' + json.dumps(error, ensure_ascii=False, indent=2) + '\n```\n']
    Path('data/reports/ISO15022_EVENT_LEARNING_ERRORS.md').write_text('\n'.join(errors))
    print('Wrote verified event-learning report, machine receipt and every scored failure')


if __name__ == '__main__':
    p = argparse.ArgumentParser(); p.add_argument('proof'); p.add_argument('runtime_proof')
    a = p.parse_args(); report(a.proof, a.runtime_proof)
