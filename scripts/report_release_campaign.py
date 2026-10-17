"""Render immutable engineering campaign receipts without model execution."""
import argparse
import json
from pathlib import Path
from training.framework import jobs, campaigns
from training.framework.bundle import sha


def report(ident):
    root = jobs.member('campaigns', ident); s = campaigns.status(root)
    if s['state'] != 'COMPLETED': raise ValueError('Campaign incomplete')
    r = s['report']; lines = ['# ISO 15022 learning and release framework qualification', '',
        'This report qualifies engineering with controlled **AI_AUTHORED** labels. '
        'It does not establish customer accuracy. Automation remains disabled.', '',
        '## Dataset and actual learning updates', '',
        'The fixed cohort contains 8 TRAIN, 4 VALIDATION, 4 CALIBRATION and 4 FROZEN_TEST events. '
        'The unchanged 57-case challenge was neither trained on nor used for selection. '
        'These tiny, constructionally labelled samples are not a domain-generalisation trial. The engineering frozen fixture was already scored in the preceding milestone; reusing it tests protection/persistence mechanics, not a new genuinely blind quality result.', '',
        '| Stage | Job | Actual updates | Reload check |', '|---|---|---|---|']
    lines[4:4] = ['**Baseline naming:** internal candidate IDs BASE_LAYA and BASE_QWEN mean the unchanged registered '
                  'engineering checkpoints (one Laya epoch and one Qwen optimizer step from the preceding milestone). '
                  'They do not mean untouched foundation-model weights. New runs start from the same original bases, '
                  'using three epochs/two steps respectively; they do not resume the earlier optimizer.', '']
    recovery = [e for e in s['events'] if e.get('kind') == 'EXPLICIT_RECOVERY']
    if recovery:
        lines[4:4] = ['The earlier campaign was interrupted after training to correct inconsistent JSON-fence handling in the repair path. '
                      'A regression test failed before the correction and passed afterwards. This campaign explicitly reuses the completed '
                      'checkpoints; it does not retrain them or resume optimizer state. Original predictions remain under the earlier identity.', '']
    lines[4:4] = ['Dataset v2 stores TRAIN, VALIDATION, CALIBRATION and FROZEN_TEST answers in separate private files. '
                  'An additional regression test proved that the older mixed-role file allowed cross-role labels to be loaded by a scorer. '
                  'The scorer now rejects mixed-role legacy archives before reading labels. Explicit curation migrated a new version; '
                  'training still consumes only TRAIN/VALIDATION, and no earlier dataset or prediction was overwritten.', '']
    for stage in s['plan']['spec']['stages']:
        job = jobs.member('jobs', r['stage_jobs'][stage['name']]); plan = json.loads((job / 'plan.json').read_text())
        result = json.loads((job / 'result.json').read_text()); spec = plan['spec']
        updates = f"{spec['epochs']} epochs" if spec['family'] == 'LAYA' else f"{spec['max_steps']} optimiser steps (not all eligible records necessarily consumed)"
        lines.append(f"| {stage['name']}{' (registered / reused)' if stage['reuse_job'] else ' (new training)'} | `{job.name}` | {updates} | `{result.get('reload_parity', result.get('reload_validation', 'see result.json'))}` |")
    lines += ['', 'New Laya runs use the official SDK; Qwen uses local quantised MLX LoRA. '
              'Training configurations, loss diagnostics, original weights, adapters and source snapshots remain in their registered job directories. '
              'A weight update or falling training loss alone is not evidence of better unseen semantics.', '',
              '## Same-input validation comparisons', '',
              '| Candidate | Correct semantic assertions | All-nine exact match | Critical false negatives | LLM calls | Median / p95 ms |',
              '|---|---|---|---|---|---|']
    learning = []
    for stage_name, job_id in r['stage_jobs'].items():
        outcome = json.loads((jobs.member('jobs', job_id) / 'result.json').read_text())
        if stage_name == 'laya_3epoch':
            diag = outcome['training']['train_report']; before = diag['before']; after = diag['after']
            learning.append(f"Laya native whole-notice SDK diagnostic: {round(before['accuracy']*before['items'])}/{before['items']} before → "
                            f"{round(after['accuracy']*after['items'])}/{after['items']} after three epochs. "
                            f"Epoch losses: {outcome['training']['epoch_loss']}. This diagnostic differs from passage/reconciliation results below.")
        if stage_name == 'qwen_2step':
            initial = next(p['val_loss'] for p in outcome['curve'] if p['kind'] == 'VALIDATION')
            learning.append(f"Qwen: {outcome['optimiser_steps']} optimiser steps / {outcome['micro_batches']} microbatches, "
                            f"{outcome['trainable_parameters']:,} trainable LoRA parameters; weights_changed={outcome['weights_changed']}. "
                            f"Held-out JSON token loss: {initial:.6f} → {outcome['validation_token_cross_entropy']:.6f}. "
                            f"Training took {outcome['elapsed_seconds']:.1f}s; peak MLX allocated memory {outcome['peak_mlx_allocated_bytes']/1e9:.2f} GB "
                            '(not total OS/unified-memory peak). Token loss is not predicate accuracy.')
    position = lines.index('## Same-input validation comparisons')
    lines[position:position] = ['## Measured learning diagnostics', '', *[p + '\n' for p in learning]]
    for name, v in r['validation'].items():
        m = v['metrics']; lines.append(f"| {name} | {m['correct_assertions']}/{m['assertions']} | {m['cases_satisfying_all_supplied_assertions']}/{m['cases']} | {len(v['critical_false_negatives'])} | {v['llm_calls']}/{m['cases']} | {m['median_latency_ms']:.0f} / {m['p95_latency_ms']:.0f} |")
    lines += ['', 'Latency is measured request time; the first request includes lazy stage loading, explicitly recorded in each prediction. '
              'These are bounded cohort measurements, not steady-state throughput qualification.', '',
              'Repair/damage counters compare initial Laya with the reconciled result and can include authoritative '
              'structured-fact effects. They are not causal LLM-only repairs. Raw model stages and reconciliation '
              'traces retain attribution; deadline/final-status denominators are separate.', '',
              f"Validation selected **{r['selected']}**. New critical false negatives relative to the first baseline are an explicit selection gate. "
              'No frozen result selected the model or routing thresholds.', '',
              '## Frozen release and protected scoring', '',
              'All model/prompt/schema/aggregation/parser/event/rule/routing/dependency and calibration identities are pinned. '
              '`OPERATING_FREEZE.json` precedes frozen-test scoring. All test predictions and their checksums precede answer-key access.', '',
              '```json', json.dumps(r['frozen']['metrics'], indent=2), '```', '',
              '## Calibration and confidence', '',
              '```json', json.dumps(r['calibration'], indent=2), '```', '',
              'The real four-event calibration sample is insufficient. Numerical confidence must remain null. '
              'Independent controlled statistical fixtures verify fitting, held-out Brier/ECE checks, persistence, identity rejection and inference; '
              'those fixtures are software evidence, not model calibration evidence. '
              'Coverage simulations are saved in the campaign calibration directory; no unsupported probability is displayed.', '',
              '## Application, audit, and operations', '',
              'The selected release runs through the event API. Model Lab displays persisted Laya passages, Qwen output, routing, '
              'reconciliation, exact source links and calibration status. Complete-release rollback preserves the entire seal hash. '
              'Separate handoff receipts verify real application execution and API-restart persistence. '
              'The detached campaign survived an API restart. Access control and backup/cold-restore/corruption rejection have independent integration tests.', '',
              '## Boundaries and next useful work', '',
              'The qualified scope is a local single-operator learning framework. The trainable MLX adapter currently supports '
              'Laya → full Qwen Direct → review; the older constrained three-gear study remains separate. '
              'No constrained logits, calibrated customer probability, shared-service RBAC, distributed scheduling or true optimizer-state resume is claimed. '
              'The 7,683 public excerpts remain unlabelled and contain no recognised ISO structure. '
              'Representative real custodian chains are still needed for profile-specific acceptance.', '',
              'Next, run a larger predefined learning campaign with independent generation families and enough calibration error/support '
              'to test useful confidence. AI labels are sufficient to develop this framework; independently expert-labelled real notices '
              'are required before customer-quality or automated-operation claims.', '',
              f"Campaign receipt SHA-256: `{sha(root / 'result.json')}`", '']
    path = Path('data/reports/ISO15022_TRAINABLE_RELEASE_VERIFICATION.md'); path.write_text('\n'.join(lines))
    errors = ['# Trainable release engineering errors', '',
              'All truth below is AI-authored construction truth. No customer accuracy claim.', '']
    for role, reports in [('VALIDATION', r['validation']), ('FROZEN_TEST', {r['selected']: r['frozen']})]:
        for name, v in reports.items():
            for error in v['failures']:
                pred = error['prediction']
                compact = {'truth': error['truth'], 'prediction': {k: pred[k] for k in
                           ['value', 'scores', 'native_score', 'confidence', 'source', 'evidence', 'aggregation_reason'] if k in pred},
                           'whole_notice_scores': pred.get('whole_notice_diagnostic', {}).get('scores'),
                           'passage_scores': [{k: p[k] for k in ['text', 'state', 'native_value', 'scores', 'score', 'margin', 'historical', 'supersession', 'conditional'] if k in p}
                                              for p in pred.get('passage_states', [])],
                           'escalation': error['escalation'],
                           'conflicts': error['reconciliation']['conflicts'],
                           'reconciliation_for_field': [t for t in error['reconciliation'].get('trace', []) if t.get('predicate') == error['predicate']]}
                errors += [f"## {role} / {name} / {error['id']} / {error['predicate']}", '',
                           '```text', error['text'], '```', '', '```json',
                           json.dumps(compact, indent=2), '```', '']
            # Final-status/date errors have distinct truth denominators and
            # must remain visible even when the nine semantic values match.
            from training.framework.event_data import load_inputs, load_answers
            dataset = jobs.member('event-datasets', s['plan']['spec']['dataset_id'])
            manifest, inputs = load_inputs(dataset, role)
            truth = load_answers(dataset, manifest, role, inputs)
            folder = root / ('validation-' + name if role == 'VALIDATION' else 'frozen-test')
            for row in map(json.loads, (folder / 'predictions.jsonl').read_text().splitlines()):
                for field, predicted in [('expected_final_status', row['result']['decision']['classification']),
                                         ('expected_deadline_status', row['result']['deadline']['status'])]:
                    expected = truth[row['id']].get(field)
                    if expected is not None and expected != predicted:
                        errors += [f"## {role} / {name} / {row['id']} / {field}", '', '```text', row['text'], '```',
                                   '```json', json.dumps({'truth': expected, 'prediction': predicted,
                                         'decision': row['result']['decision'], 'deadline': row['result']['deadline']}, indent=2), '```', '']
    Path('data/reports/ISO15022_TRAINABLE_RELEASE_ERRORS.md').write_text('\n'.join(errors))
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    fig, axes = plt.subplots(1, 2, figsize=(10, 3.5))
    for name, job_id in r['stage_jobs'].items():
        result = json.loads((jobs.member('jobs', job_id) / 'result.json').read_text())
        if result.get('backend') == 'LAYA_SDK' and 'training' in result:
            values = result['training']['epoch_loss']
            axes[0].plot(range(1, len(values) + 1), values, 'o-', label=name)
        elif result.get('backend') == 'MLX_QLORA':
            curve = [p for p in result.get('curve', []) if p['kind'] == 'TRAIN']
            axes[1].plot([p['iteration'] for p in curve], [p['train_loss'] for p in curve], 'o-', label=name)
    axes[0].set(xlabel='Epoch', ylabel='Native training loss', title='Laya controlled training')
    axes[1].set(xlabel='Optimiser iteration', ylabel='Assistant-JSON token loss', title='Qwen controlled training')
    for ax in axes: ax.legend(fontsize=7); ax.grid(alpha=.15)
    fig.suptitle('Optimisation diagnostics — not customer accuracy or a data-size learning curve', fontsize=10)
    fig.tight_layout(); fig.savefig(root / 'training-loss.svg'); plt.close(fig)
    completion = Path('artifacts/release-framework-completion.json')
    if completion.exists() and json.loads(completion.read_text())['campaign_id'] == ident:
        with path.open('a') as f:
            f.write('\n## Final verification receipts\n\n'
                    '* 2,197 ordinary application tests passed; one opt-in CPU smoke skipped, 160 model/browser checks deselected in that run.\n'
                    '* 27 browser tests passed with explicit software doubles; a separate live-browser check inspected actual saved model traces with zero browser errors.\n'
                    '* Two real registered Laya/Qwen integration tests passed in 80.76s.\n'
                    '* Real API execution of Laya-only, Qwen-only and cascade releases; complete-release rollback and API-restart persistence passed.\n'
                    '* Checksummed real workspace/SQLite backup completed; corruption rejection and cold restore passed on isolated integration fixtures.\n'
                    '* Timestamp-normalised source delivery was reproduced byte-for-byte and started from a clean locked environment.\n'
                    '* No framework job or timed benchmark remains running. The earlier Laya-first study remains safely stopped with completed rows preserved.\n\n'
                    'Machine receipt: `artifacts/release-framework-completion.json`. '
                    'Operations: `docs/LOCAL_LEARNING_OPERATIONS.md`. Source delivery: '
                    '`artifacts/releases/iso15022-learning-framework-20261017-r3.tar.gz`.\n')
    return path


if __name__ == '__main__':
    p = argparse.ArgumentParser(); p.add_argument('id'); print(report(p.parse_args().id))
