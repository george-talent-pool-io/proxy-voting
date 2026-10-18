"""Render measured receipts; unavailable experiments remain explicitly absent."""
import json
from pathlib import Path


def report(study,output):
    root=Path(study);result=json.loads((root/'result.json').read_text())
    plan=json.loads((root/'EXPERIMENT_PLAN.json').read_text())
    operating=json.loads((root/'OPERATING_POINT.json').read_text())
    corpus=Path('data/qualification-corpora/composition-confidence-v4')
    cm=json.loads((corpus/'manifest.json').read_text())
    training=plan['training_updates']['training']
    rows=['# Frozen-checkpoint learning and calibrated review qualification','',
          'This report concerns the deliverable framework and controlled AI-authored qualification. '
          'The test corpus and test-trained derivatives are not production model/data deliverables. '
          'Automation remains disabled. Customer accuracy is unknown.','',
          '## Laya diagnosis and measured learning','',
          'The earlier eight-event, frozen-encoder trial did not establish Laya\'s learnability. '
          'The new run uses 128 TRAIN notices, 128 separate VALIDATION notices, all nine labels, '
          'four full-encoder epochs, option-order augmentation, soft cross-entropy, effective batch 16, '
          'and 288 optimizer updates. Encoder/head LR were both 0.0001 in this actual experiment. '
          'The separately provided conservative training recipe uses encoder LR 0.000025; it was not the configuration measured here.','',
          f'Official SDK held-out diagnostic: {training["train_report"]["before"]["accuracy"]:.2%} → '
          f'{training["train_report"]["after"]["accuracy"]:.2%} on 1,152 predicate decisions from 128 notices. '
          'This is whole-notice native classification, before application evidence/aggregation rules.','',
          'Epoch mean losses: '+', '.join(f'{x:.6f}' for x in training['epoch_loss'])+'. Reload scores were identical.','',
          'Whole-notice training and passage inference were mismatched in the earlier implementation. '
          'The framework now exposes both matched whole-notice inference with passage evidence and the preserved passage reducer as explicit validation conditions.','',
          '| Validation condition | Correct / assertions | All-nine exact / notices |',
          '|---|---:|---:|']
    for name,m in result['validation'].items():
        rows.append(f'| {name} | {m["correct_assertions"]}/{m["assertions"]} | {m["cases_satisfying_all_supplied_assertions"]}/{m["cases"]} |')
    rows+=['',f'Selected on validation: **{result["selected"]}**. No frozen/challenge result selected the model.','',
           '## Controlled cohort and leakage','',
           f'The cohort contains {sum(c["examples"] for c in cm["counts"].values())} notices across {cm["groups"]} composition groups. '
           'All eight restriction predicates have explicit mandatory, waived, optional and UNKNOWN construction states and exact-source evidence. '
           'The original 57 challenge cases were neither generated from nor trained on.','',
           '| Role | Notices | Groups |','|---|---:|---:|']
    for role,c in cm['counts'].items():rows.append(f'| {role} | {c["examples"]} | {c["groups"]} |')
    rows+=['','The new cohort TRAIN role is not consumed by the Laya run above. '
           'Construction excludes the actual Laya training fact combinations and lexical near-duplicates. '
           'All variants of a full optional/mandatory fact composition share a role. '
           'Calibration FIT and EVALUATION use different whole groups.','',
           '**Limitations:** shared AI-authored sentence atoms occur across roles. This tests new compositions, '
           'not independent unseen linguistic families. The cohort is English and restriction-focused; all events '
           'are votable. It cannot establish non-votable generalisation or representative client precision.','',
           '## Protected test','']
    m=result['frozen']
    rows += [f'Semantic assertions: **{m["correct_assertions"]}/{m["assertions"]}**; '
             f'all-nine exact: **{m["cases_satisfying_all_supplied_assertions"]}/{m["cases"]}**.',
             f'Final status: {m["benchmark_final_status"]["correct"]}/{m["benchmark_final_status"]["n"]}; '
             f'deadline: {m["benchmark_deadline"]["correct"]}/{m["benchmark_deadline"]["n"]}.','',
             '| Predicate | Correct / n | Positive support | Positive recall | Negative specificity | Macro F1 |',
             '|---|---:|---:|---:|---:|---:|']
    def fmt(v):return 'N/A' if v is None else f'{v:.4f}'
    for key,f in m['fields'].items():rows.append(f'| {key} | {f["correct"]}/{f["n"]} | {f["positive_support"]} | {fmt(f["positive_recall"])} | {fmt(f["negative_recall_specificity"])} | {fmt(f["macro_f1"])} |')
    rows+=['','All confusion matrices and every error, including source text/native scores, are in `frozen/metrics.json`. '
           'All raw results and passage distributions are retained in `frozen/predictions.jsonl`.','',
           '## Actual correctness calibration','',
           'Calibration uses actual selected-model predictions, not a known-frequency software fixture. '
           'The default 100 FIT / 50 EVALUATION independent-group support checks remain in force. '
           'A fixed logistic correctness estimator uses FIT-only scaling when both outcomes have support. '
           'Rare-error conditions use an explicitly non-discriminating, Laplace-smoothed constant; '
           'no errors or probabilities are fabricated. Calibration is checked independently and by predicted label.','',
           '| Predicate | Status | Method | Held-out Brier | Held-out ECE |','|---|---|---|---:|---:|']
    for key,c in result['calibration'].items():
        e=c.get('evaluation',{});rows.append(f'| {key} | {c["status"]} | {c.get("method","N/A")} | {fmt(e.get("brier"))} | {fmt(e.get("ece"))} |')
    rows+=['',f'Events with every required confidence available on frozen inputs: {result["confidence_available_events"]}/{m["cases"]}. '
           'Unsupported labels, languages, input types, conflicts, UNKNOWN and insufficient support retain null confidence.','',
           '## Operating coverage and review','',
           'Threshold selection uses validation only, complete-output correctness, critical false negatives and '
           'simultaneous one-sided grouped exact precision bounds. The frozen test only measures the selected point.','',
           '| Threshold | Validation coverage | Observed correctness | Precision lower bound | Accepted groups |',
           '|---|---:|---:|---:|---:|']
    for c in operating['curve']:rows.append(f'| {c["threshold"]:.2f} | {c["coverage"]:.2%} | {fmt(c["correctness"])} | {c["precision_lower_bound"]:.4f} | {c["accepted_groups"]} |')
    rows+=['',f'Operating status: **{operating["status"]}**. Frozen measurement:','',
           '```json',json.dumps(result['operating'],indent=2),'```','',
           'These are review simulations on a controlled AI population. They grant no customer automation permission. '
           'A low review percentage is measured only if the selected point actually supports it.','',
           '## Unchanged challenge','', '| Condition | Correct labelled assertions | Cases satisfying partial assertions |', '|---|---:|---:|']
    for name,c in result['challenge'].items():rows.append(f'| {name} | {c["correct_assertions"]}/{c["assertions"]} | {c["cases_satisfying_all_supplied_assertions"]}/{c["cases"]} |')
    rows+=['','Only four challenge cases have explicit final-status labels. These are partial-assertion results, not customer accuracy.','',
           '## Measured local latency','',
           'All timings are on the development Mac. Request inference excludes explicit initial model loading '
           'and external queue/network delay. First-request lazy kernel work remains included. No AWS extrapolation.','',
           '| Condition | n | Model load s | Median s | Mean s | Min s | Max s | p95 s |',
           '|---|---:|---:|---:|---:|---:|---:|---:|']
    for folder in ['FROZEN_LAYA_WHOLE','TRAINED_LAYA_PASSAGES','TRAINED_LAYA_WHOLE','calibration','frozen']:
        c=json.loads((root/folder/'PREDICTIONS_SAVED.json').read_text());t=c['latency_seconds']
        rows.append(f'| {folder} | {c["count"]} | {c["model_load_seconds"]:.3f} | '+ ' | '.join(f'{t[k]:.3f}' for k in ['median','mean','min','max','p95'])+' |')
    rows+=['','Receipts also report measured throughput including load/persistence, process RSS and after-notice '
           'MPS driver allocation samples. Those samples are not an OS-wide peak unified-memory measurement.','',
           '## Delivery and remaining limits','',
           'The deliverable supports frozen, dataset-free Laya/Qwen starting checkpoints, parent-bound further learning '
           'with new optimizers, validation selection, distinct stage/final calibration, protected test evaluation, '
           'versioned confidence operating points, calibrated cascade routing, review simulation and authenticated review/audit. '
           'The default remains conservative; test-derived weights are excluded from the source/image delivery.','',
           'A frozen foundation identity is not proof of domain excellence. Customer-specific training/calibration '
           'must be independently qualified. The locally tested Qwen MLX conversion is not a qualified Linux CUDA artifact. '
           'No claim is made about client review percentage or production classification accuracy.','']
    Path(output).write_text('\n'.join(rows))
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    fig,axes=plt.subplots(1,2,figsize=(11,4))
    axes[0].plot([0,1],[0,1],'--',color='#999999')
    for key,c in result['calibration'].items():
        bins=c.get('evaluation',{}).get('bins',[])
        if bins:axes[0].plot([b['mean_probability'] for b in bins],[b['observed_correctness'] for b in bins],'.-',label=key)
    axes[0].set(xlabel='Correctness estimate',ylabel='Held-out observed correctness',title='AI population calibration')
    curve=operating['curve'];axes[1].plot([c['threshold'] for c in curve],[c['coverage'] for c in curve],'.-',label='Coverage')
    axes[1].plot([c['threshold'] for c in curve],[c['correctness'] for c in curve],'.-',label='Correctness')
    axes[1].set(xlabel='Threshold',ylabel='Fraction',ylim=(0,1.02),title='Validation review simulation');axes[1].legend()
    fig.tight_layout();fig.savefig(root/'calibration-coverage.svg');plt.close(fig)

if __name__=='__main__':
    import argparse
    p=argparse.ArgumentParser();p.add_argument('study');p.add_argument('output');a=p.parse_args();report(a.study,a.output)
