"""Render completed model/calibration receipts without advertising synthetic truth.

No source notices are embedded: the report can accompany the dataset-free source
delivery. Full examples, raw scores and every failure remain in the evidence store.
"""
import json
from pathlib import Path


def report(study, output, *, replay=None, continuation=None, browser=None, integration=None):
    root=Path(study);r=json.loads((root/'result.json').read_text())
    # Post-scoring diagnostics do not modify the frozen result, calibrator or
    # operating point. All probabilities come from the persisted confidence rows.
    from training.framework.bundle import write,sha
    from qwen_domain.confidence import calibration_metrics
    from semantic_pipeline.schema import PREDICATES
    risk=[json.loads(line) for line in (root/'frozen/confidence.jsonl').read_text().splitlines()]
    predictions={p['id']:p for p in (json.loads(line) for line in (root/'frozen/predictions.jsonl').read_text().splitlines())}
    diagnostics=root/'frozen/calibrated-diagnostics.json'
    if diagnostics.exists():supplement=json.loads(diagnostics.read_text())
    else:
        fields={};errors=[]
        for key in PREDICATES:
            rows=[x for x in risk if x['predicate_confidence'][key] is not None]
            fields[key]={**calibration_metrics([x['prediction'][key]==x['truth'][key] for x in rows],
                 [x['predicate_confidence'][key] for x in rows]),'available':len(rows),'total':len(risk),
                 'scope':'Supported-confidence subset only; unavailable outcomes retain review/null'}
            for x in rows:
                if x['predicate_confidence'][key]>=.98 and x['prediction'][key]!=x['truth'][key]:
                    p=predictions[x['id']]
                    errors.append({'id':x['id'],'field':key,'expected':x['truth'][key],'prediction':x['prediction'][key],
                        'calibrated_confidence':x['predicate_confidence'][key],
                        'native_scores':p['result']['predicates'][key].get('scores'),'text':p['text']})
        write(root/'frozen/calibrated-high-confidence-errors.json',errors)
        supplement={'frozen_calibration':fields,'calibrated_high_confidence_error_count':len(errors),
                    'prediction_sha256':sha(root/'frozen/predictions.jsonl'),'confidence_sha256':sha(root/'frozen/confidence.jsonl'),
                    'analysis_script_sha256':sha(Path(__file__)),'threshold_diagnostic':.98,
                    'scope':'Post-scoring diagnostic only; no tuning or release changes'}
        write(diagnostics,supplement)
    if (supplement['prediction_sha256']!=sha(root/'frozen/predictions.jsonl') or
        supplement['confidence_sha256']!=sha(root/'frozen/confidence.jsonl')):raise ValueError('Diagnostic source changed')
    r={**r,**supplement}
    selection=json.loads((root/'MODEL_SELECTION.json').read_text())
    freeze=json.loads((root/'OPERATING_FREEZE.json').read_text())
    point=json.loads((root/'OPERATING_POINT.json').read_text())
    plan=json.loads((root/'PLAN.json').read_text())
    corpus=Path('data/qualification-corpora/composition-confidence-v4')
    cm=json.loads((corpus/'manifest.json').read_text())
    # Separate, post-scoring status diagnostics. They cannot select weights,
    # criteria, a calibrator or a threshold and never alter the original run.
    status_path=root/'frozen/decision-diagnostics.json'
    if not status_path.exists():
        from collections import Counter
        entry=cm['files']['FROZEN_TEST'];answer_path=corpus/entry['labels']
        if sha(answer_path)!=entry['labels_sha256'] or not (root/'frozen/metrics.json').exists():
            raise ValueError('Post-scoring status diagnostics require verified, already-scored answers')
        truth={v['id']:v for v in map(json.loads,answer_path.read_text().splitlines())}
        if set(truth)!=set(predictions):raise ValueError('Status diagnostic membership changed')
        matrix=Counter();failures=[];reasons=Counter()
        for ident,prediction in predictions.items():
            result=prediction['result'];expected=truth[ident]['final_status'];actual=result['decision']['classification']
            matrix[(expected,actual)]+=1
            if expected!=actual:
                reasons.update(result['reconciliation']['conflicts'])
                failures.append({'id':ident,'text':prediction['text'],'expected_final_status':expected,
                    'predicted_final_status':actual,'decision':result['decision'],
                    'conflicts':result['reconciliation']['conflicts'],'predicates':result['predicates']})
        write(root/'frozen/final-status-errors.json',failures)
        write(status_path,{'scope':'Post-scoring diagnostic only; no model/criteria/threshold changes',
            'prediction_sha256':sha(root/'frozen/predictions.jsonl'),'answer_sha256':sha(answer_path),
            'expected_status_support':dict(Counter(v['final_status'] for v in truth.values())),
            'confusion':[{'expected':a,'predicted':b,'count':n} for (a,b),n in sorted(matrix.items())],
            'errors':len(failures),'all_status_errors_require_review':all(f['decision']['manual_review_required'] for f in failures),
            'error_conflict_counts':dict(reasons)})
    status_diagnostic=json.loads(status_path.read_text())
    if status_diagnostic['prediction_sha256']!=sha(root/'frozen/predictions.jsonl'):
        raise ValueError('Status diagnostic source changed')
    def fmt(v):return 'N/A' if v is None else f'{v:.4f}'
    rows=['# Frozen starting checkpoints, customer learning and confidence qualification','',
      'The product is the local learning/inference/review framework. The AI-authored corpus, test-trained weights, '
      'test calibrators, customer workspaces and private answers are excluded from the source/image delivery. '
      '**Automation is disabled. Customer accuracy and a customer review percentage remain unestablished.**','',
      '## What changed','',
      '- Dataset-free foundation and derivative manifests pin every weight, prompt, semantic criterion and parent identity. '
      'Serving a frozen seed needs no access to its old training corpus. Relocation requires identical bytes.',
      '- Both Laya and Qwen can continue from frozen weights/adapters with a new optimizer; trained AI artifacts retain AI_TEST_DERIVATIVE provenance.',
      '- Full-encoder Laya training exposes separate encoder/head learning rates, option-order augmentation, training budgets, '
      'gradient checkpointing and an optional MPS memory cap. Long MLX jobs have an explicit configurable timeout.',
      '- Matched whole-notice inference preserves native document labels; evidence lookup never changes them. '
      'Opposing current evidence, conditional terms and missing positive evidence force review.',
      '- Correctness calibration is fitted on actual model predictions, independently checked by group, scoped to a population '
      'and available per predicate and final decision. Unsupported conditions keep null confidence.',
      '- Calibrated specialist routing and final-cascade calibration use physically separate groups and answer files. '
      'Confidence operating points are selected on validation and evaluated without retuning on frozen tests.',
      '- Source-hashed complete-input negative judgements have a separate calibrated evidence stratum. '
      'They are neither invented quotes nor deterministic proofs that a restriction is absent.','',
      '## Diagnosis and controlled training','',
      'The earlier eight-event, head-only run was not enough to assess Laya learning. A subsequent 128 TRAIN / 128 VALIDATION '
      'full-encoder run reached 99.48% in the official SDK diagnostic on that older construction population, yet only '
      '4,099/5,400 assertions on the new 600-notice validation population with whole-notice serving. '
      'Its affirmative blocking recall was 56/236. Sentence serving with the same weights was worse overall. '
      'This is a real composition/distribution gap; the 99.48% figure is not general domain performance.','',
      'The corrective experiment starts from the official frozen Laya foundation, uses 200 new TRAIN notices plus '
      '32 TRAIN-only replay notices, all nine labels, encoder LR 0.000025, head LR 0.0001, option shuffling, '
      'soft cross-entropy, seed 42 and effective batch 16. Four epochs permit 524 optimizer updates. '
      'A predeclared extension allows four further epochs with a fresh optimizer only when validation macro F1 '
      'or critical-positive recall is below 0.98. No challenge/frozen answer selected training, criteria or thresholds.','',
      'Training support diagnostics explicitly report absent/rare classes. Additional epochs cannot create missing '
      'supervision. This run has these development-data support warnings: '+', '.join(plan['training_label_support']['warnings'])+'. '
      'The five-group diagnostic is not a regulatory or automation threshold.','',
      'Resource trials v1 and v2 were interrupted and preserved before the first completed epoch. The first reached '
      'roughly 50 GB physical footprint. The completed condition uses gradient checkpointing, micro-batch 8 / '
      'accumulation 2, a 0.45 MPS memory fraction and separate framework validation instead of duplicated SDK diagnostics. '
      'An external model workload also shared the Mac; do not attribute all resource differences to one setting.','',
      '| Validation condition | Correct / 5,400 assertions | All-nine exact / 600 notices |',
      '|---|---:|---:|']
    for k,v in r['validation'].items():rows.append(f'| {k} | {v["correct_assertions"]}/{v["assertions"]} | {v["cases_satisfying_all_supplied_assertions"]}/{v["cases"]} |')
    rows += ['',f'Validation-selected condition: **{r["selected"]}**. Eligible conditions: '+', '.join(selection['eligible'])+'. '
             'Selection maximises correct assertions subject to no new missed critical positive compared with the foundation.','',
      '| Validation predicate | Foundation positive recall | Four epochs | Eight epochs |', '|---|---:|---:|---:|']
    for k in r['validation']['FOUNDATION']['fields']:
        vals=[r['validation'].get(c,{}).get('fields',{}).get(k,{}).get('positive_recall') for c in ('FOUNDATION','ADAPTED_4_EPOCHS','ADAPTED_8_EPOCHS')]
        rows.append('| '+k+' | '+' | '.join(fmt(v) for v in vals)+' |')
    rows += ['','## Cohort and isolation','',
      '2,000 notices / 1,000 composition groups: TRAIN 200/100, VALIDATION 600/300, CALIBRATION 800/400, '
      'FROZEN_TEST 400/200. All eight positive restrictions are represented. Truth is constructed first; '
      'lexical variants stay with their full fact-composition group. Exact/normalised hashes, numeric-masked '
      'five-word lexical grouping and source family checks prevent known cross-role duplicates. '
      'The corpus excludes the earlier 128 TRAIN fact compositions. TRAIN/VALIDATION export cannot read held-out answer paths.','',
      '**Scope limitation:** English, restriction-focused and all votable. Shared AI-authored sentence atoms cross roles. '
      'These are held-out compositions, not independent real linguistic families, non-votable evaluation or expert-reviewed production data. '
      'The first baseline evaluator had already scored this controlled frozen cohort; corrective training was preregistered '
      'before its outcomes were inspected. This is not a new double-blind independent external study. '
      'The new selected model persisted every test prediction before opening its answer file.','',
      'All 400 frozen examples also have VOTABLE_WITH_RESTRICTION as their final-status truth. '
      'This cohort tests individual restriction combinations, not discrimination among every final-status class.','',
      '## Protected selected-model results','']
    m=r['frozen']
    rows += [f'**{m["correct_assertions"]}/{m["assertions"]} semantic assertions**; '
             f'**{m["cases_satisfying_all_supplied_assertions"]}/{m["cases"]} all-nine exact match**. '
             f'Final status {m["benchmark_final_status"]["correct"]}/{m["benchmark_final_status"]["n"]}; '
             f'deadline {m["benchmark_deadline"]["correct"]}/{m["benchmark_deadline"]["n"]}.','',
      '| Predicate | Correct / n | Positive support | Positive recall | Positive misses | Specificity | Macro F1 |',
      '|---|---:|---:|---:|---:|---:|---:|']
    for k,f in m['fields'].items():
        misses=f['positive_support']-round((f['positive_recall'] or 0)*f['positive_support'])
        rows.append(f'| {k} | {f["correct"]}/{f["n"]} | {f["positive_support"]} | {fmt(f["positive_recall"])} | {misses} | {fmt(f["negative_recall_specificity"])} | {fmt(f["macro_f1"])} |')
    rows += ['','Every confusion matrix and failure (source, native scores, margin and provenance) is retained in '
      '`'+str(root/'frozen/metrics.json')+'`; complete raw outputs are in `frozen/predictions.jsonl`. '
      'Those artifacts stay outside the product archive.','',
      'Final-status confusion and every status failure are additionally retained in '
      '`frozen/decision-diagnostics.json` and `frozen/final-status-errors.json`. '
      'The status mismatches are review abstentions, not missed positive restrictions. '
      'The following is a post-scoring explanation of those outputs, not a criteria change:','',
      '```json',json.dumps(status_diagnostic,indent=2),'```','',
      'Foundation control on the same frozen inputs and current runtime: '
      f'{r["frozen_foundation"]["correct_assertions"]}/{r["frozen_foundation"]["assertions"]} semantic assertions; '
      f'{r["frozen_foundation"]["cases_satisfying_all_supplied_assertions"]}/{r["frozen_foundation"]["cases"]} all-nine exact. '
      'Both models saved every prediction before either set was scored.','',
      '## Actual confidence calibration','',
      'CALIBRATION FIT/EVALUATION groups are disjoint. Fixed L2 logistic calibration uses FIT-only scaling '
      'when both correct and wrong outcomes have support. Otherwise an explicitly non-discriminating '
      'Laplace-smoothed constant is used. No mistakes or probabilities are manufactured. Default support is '
      '100 FIT / 50 EVALUATION groups globally and 20 groups per supported prediction/evidence stratum. '
      'Confidence is null for unsupported populations, classes, languages, input types, missing positive evidence, '
      'UNKNOWN or conflicts. No calibration claim transfers to a different customer population.','',
      '| Predicate | Calibration status | Method | EVALUATION n | Brier | ECE |', '|---|---|---|---:|---:|---:|']
    for k,c in r['calibration'].items():
        e=c.get('evaluation',{});rows.append(f'| {k} | {c["status"]} | {c.get("method","N/A")} | {e.get("n","N/A")} | {fmt(e.get("brier"))} | {fmt(e.get("ece"))} |')
    rows += ['',f'Complete required trust available on {r["confidence_available_events"]}/{m["cases"]} frozen events. '
      'Final-status correctness has a separate calibrator. The minimum across required confidences is a conservative '
      'routing score, not a calibrated joint probability.','',
      f'Calibrated predicate errors at confidence ≥0.98: **{r["calibrated_high_confidence_error_count"]}**. '
      'Every such example, native score and confidence is retained in `frozen/calibrated-high-confidence-errors.json`. '
      'Independent frozen Brier/ECE for the supported-confidence subset follows; unsupported outcomes remain in the '
      'overall correctness denominator and go to review:','',
      '```json',json.dumps(r.get('frozen_calibration',{}),indent=2),'```','',
      '## Coverage and review','',
      '| Validation threshold | Coverage | Complete-output correctness | Simultaneous precision lower bound | Accepted groups |',
      '|---|---:|---:|---:|---:|']
    for p in point['curve']:rows.append(f'| {p["threshold"]:.2f} | {p["coverage"]:.2%} | {fmt(p["correctness"])} | {p["precision_lower_bound"]:.4f} | {p["accepted_groups"]} |')
    rows += ['',f'**{point["status"]}**. The rule requires a 98% complete-output precision lower bound, '
      'at least 100 accepted validation groups and zero accepted critical false negatives. '
      'The frozen test evaluates the already-fixed point:','', '```json',json.dumps(r['operating'],indent=2),'```','',
      'If no point is supported, every event remains review/escalation. This is a measured negative result, '
      'not a missing confidence estimator. Even a supported synthetic point cannot enable customer automation.','',
      'The stress cohort deliberately includes unresolved requirements. Review by truth stratum is reported below '
      'as a diagnostic; every such record remains in the overall denominator above:','',
      '```json',json.dumps(r.get('ambiguity_strata',{}),indent=2),'```','',
      '## Unchanged authored challenge','',
      f'{r["challenge"]["correct_assertions"]}/{r["challenge"]["assertions"]} labelled assertions; '
      f'{r["challenge"]["cases_satisfying_all_supplied_assertions"]}/{r["challenge"]["cases"]} cases satisfying supplied partial assertions. '
      'Only four cases have explicit final-status truth. These are not customer/final-status accuracy denominators.','',
      f'Current-runtime foundation control: {r["challenge_foundation"]["correct_assertions"]}/{r["challenge_foundation"]["assertions"]} assertions; '
      f'{r["challenge_foundation"]["cases_satisfying_all_supplied_assertions"]}/{r["challenge_foundation"]["cases"]} partial-assertion cases. '
      'This explicit nine-predicate whole-notice condition differs from the historical legacy seven-bucket baseline.','',
      '## Development Mac timings','',
      'Apple M3 Max, 64 GB unified memory. No EC2 run or extrapolation. Request timing excludes model initialisation, '
      'queue and network time; first-request kernel warm-up remains included. Throughput includes loading and durable '
      'prediction writes. Resource samples are not a complete OS-wide peak unified-memory trace.','',
      '| Condition | n | Load s | Median s | Mean s | Min s | Max s | p95 s | notices/s |',
      '|---|---:|---:|---:|---:|---:|---:|---:|---:|']
    for d in [*r['validation'],'calibration','frozen']:
        p=root/d/'PREDICTIONS_SAVED.json'
        if not p.exists():continue
        v=json.loads(p.read_text());t=v['latency_seconds']
        rows.append(f'| {d} | {v["count"]} | {v["model_load_seconds"]:.3f} | '+' | '.join(f'{t[k]:.3f}' for k in ('median','mean','min','max','p95'))+f' | {v["notices_per_second_including_load_and_persistence"]:.3f} |')
    rows += ['', 'Known external local-model workers are recorded in each timing receipt. Overlapping runs are labelled '
      '`CONTENDED_WITH_EXTERNAL_MODEL_WORKLOAD`; these are actual development conditions, not isolated server capacity.','']
    for title,path in [('Frozen continuation mechanics',continuation),('Authenticated customer workflow',replay),('Persisted calibrated browser and restart',browser),('Real two-model release integration',integration)]:
        if path and Path(path).exists():
            rows += ['## '+title,'','Receipt: `'+str(path)+'`.','', '```json',json.dumps(json.loads(Path(path).read_text()),indent=2),'```','']
        else:rows += ['## '+title,'','NOT YET VERIFIED IN THIS RUN.','']
    rows += ['## Delivery boundary and remaining qualification','',
      'The source archive and Docker image contain no new AI corpus, test-trained weights, optimizer state, '
      'customer database, private answer keys or test calibrator. Provision pinned foundation weights separately '
      'and create a fresh customer workspace. A frozen foundation identity is not a domain-accuracy certificate.','',
      'Linux ARM64 service startup/authentication/read-only execution/restart persistence is verified separately. '
      'Apple MLX training is not Linux CUDA qualification. The exact target Linux model/runtime still needs its own '
      'resource, learning and inference qualification. This phase does not establish representative client accuracy, '
      'a guaranteed low review percentage, multilingual generalisation or customer voting-risk tolerances.','',
      'Highest-value next qualification: use representative client MT564/MT568 events with independently expert-reviewed '
      'factorised labels; reserve whole events/amendment chains/families for calibration and final test, '
      'then run the same frozen-parent learning and confidence protocol.','']
    Path(output).write_text('\n'.join(rows))
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    fig,axes=plt.subplots(1,2,figsize=(11,4));axes[0].plot([0,1],[0,1],'--',color='gray')
    for k,c in r['calibration'].items():
        bins=c.get('evaluation',{}).get('bins',[])
        if bins:axes[0].plot([b['mean_probability'] for b in bins],[b['observed_correctness'] for b in bins],'.-',label=k)
    axes[0].set(xlabel='Estimated correctness',ylabel='Held-out correctness',title='AI-population reliability')
    curve=point['curve'];axes[1].plot([p['threshold'] for p in curve],[p['coverage'] for p in curve],'.-',label='Coverage')
    axes[1].plot([p['threshold'] for p in curve],[p['correctness'] for p in curve],'.-',label='Correctness')
    axes[1].set(xlabel='Threshold',ylabel='Fraction',ylim=(0,1.02),title='Validation review simulation');axes[1].legend()
    fig.tight_layout();fig.savefig(root/'calibration-coverage.svg');plt.close(fig)


if __name__=='__main__':
    import argparse
    p=argparse.ArgumentParser();p.add_argument('study');p.add_argument('output');p.add_argument('--replay');p.add_argument('--continuation');p.add_argument('--browser');p.add_argument('--integration')
    a=p.parse_args();report(a.study,a.output,replay=a.replay,continuation=a.continuation,browser=a.browser,integration=a.integration)
