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
    for stage in s['plan']['spec']['stages']:
        job = jobs.member('jobs', r['stage_jobs'][stage['name']]); plan = json.loads((job / 'plan.json').read_text())
        result = json.loads((job / 'result.json').read_text()); spec = plan['spec']
        updates = f"{spec['epochs']} epochs" if spec['family'] == 'LAYA' else f"{spec['max_steps']} optimiser steps (not all eligible records necessarily consumed)"
        lines.append(f"| {stage['name']}{' (unchanged)' if stage['reuse_job'] else ' (new training)'} | `{job.name}` | {updates} | `{result.get('reload_parity', result.get('reload_validation', 'see result.json'))}` |")
    lines += ['', 'New Laya runs use the official SDK; Qwen uses local quantised MLX LoRA. '
              'Training configurations, loss diagnostics, original weights, adapters and source snapshots remain in their registered job directories. '
              'A weight update or falling training loss alone is not evidence of better unseen semantics.', '',
              '## Same-input validation comparisons', '',
              '| Candidate | Correct semantic assertions | All-nine exact match | Critical false negatives | LLM calls | Median / p95 ms |',
              '|---|---|---|---|---|---|']
    for name, v in r['validation'].items():
        m = v['metrics']; lines.append(f"| {name} | {m['correct_assertions']}/{m['assertions']} | {m['cases_satisfying_all_supplied_assertions']}/{m['cases']} | {len(v['critical_false_negatives'])} | {v['llm_calls']}/{m['cases']} | {m['median_latency_ms']:.0f} / {m['p95_latency_ms']:.0f} |")
    lines += ['', 'Latency is measured request time; the first request includes lazy stage loading, explicitly recorded in each prediction. '
              'These are bounded cohort measurements, not steady-state throughput qualification.', '',
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
    return path


if __name__ == '__main__':
    p = argparse.ArgumentParser(); p.add_argument('id'); print(report(p.parse_args().id))
