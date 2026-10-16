"""Transparent post-freeze SCORER-v2 correction. NO model/criteria/routing changes.
C's new schema has named restriction facts; the legacy broad auxiliary head is
not its reconciled broad union. Preserve raw artifacts and the frozen v1 score.
"""
import copy
import os
import json
from pathlib import Path
from semantic_pipeline.schema import RESTRICTIONS, NOT_SUPPORTED
from semantic_pipeline.metrics import summarize, truth, observed
from semantic_pipeline.reporting import transition_analysis


def project(rows,arm):
    result=[];changes=[]
    for original in rows:
        row=copy.deepcopy(original);preds=row['result']['reconciliation']['predicates']
        if arm=='C' and 'other_restriction' in preds:
            keys=[k for k in RESTRICTIONS if k not in ('share_blocking','poa_required')]
            values=[preds.get(k,{}).get('value',NOT_SUPPORTED) for k in keys]
            if all(v!=NOT_SUPPORTED for v in values):
                old=preds.pop('other_restriction')
                row['result']['legacy_broad_restriction_diagnostic']=old
                value='YES' if 'YES' in values else 'NO' if all(v=='NO' for v in values) else 'UNKNOWN'
                changes.append({'id':row['id'],'old_broad_value':old['value'],
                    'canonical_broad_value':value,'named_values':dict(zip(keys,values)),
                    'value_changed':old['value']!=value,
                    'reason':'Evaluate the new reconciled schema, not the stale legacy auxiliary head'})
        result.append(row)
    return result,changes


def correct(root, report_path=None):
    from semantic_pipeline.experiment import read,write,lines,sha,verify,now
    verify();commit=read(root/'PREDICTION-COMMIT.json')
    for p,h in commit['files'].items():assert sha(p)==h,p
    original=read(root/'SUMMARY.json');out=copy.deepcopy(original);all_rows={};audit={}
    key=read(root/'synthetic-development-truth.json')
    for dataset in ('challenge','synthetic-development','complete'):
        all_rows[dataset]={};audit[dataset]={}
        for arm in 'ABCDE':
            rows=lines(root/f'{dataset}-{arm}.jsonl')
            if dataset=='synthetic-development':
                for r in rows:r['expected']=key[r['id']]
            rows,changes=project(rows,arm);all_rows[dataset][arm]=rows;audit[dataset][arm]=changes
            fresh=summarize(rows)
            factor_rows=[r for r in rows if any(k!='classification' for k in truth(r['expected']))]
            factor_correct=sum(all(observed(r['result']).get(k,NOT_SUPPORTED)==v for k,v in truth(r['expected']).items() if k!='classification') for r in factor_rows)
            fresh['supplied_factor_exact_match']={'correct':factor_correct,'n':len(factor_rows),'accuracy':factor_correct/len(factor_rows) if factor_rows else None,'scope':'Only factors with supplied truth; full schema only on the complete benchmark'}
            index={rr['id']:rr for rr in rows}
            for error in fresh['failures']:
                rr=index[error['id']]['result']
                error['all_native_laya_scores']={k:a.get('scores',{}) for k,a in (rr.get('laya') or {}).get('predicates',{}).items()}
                if error['confidence'] is None:error['confidence_definition']='Unavailable for this derived/unsupported/model-unscored field; component scores are not a final probability'
            stored=out['datasets'][dataset][arm]
            fresh['high_confidence_wrong_cases']=len({e['id'] for e in fresh['failures'] if e['confidence'] is not None and e['confidence']>=.98})
            stored.update(fresh)
            stored['frozen_scorer_v1_cases_passed']=original['datasets'][dataset][arm]['cases_satisfying_all_supplied_assertions']
            stored['scoring_version']='SCORER-v2: canonical new-schema broad union'
            out['layer_metrics'][dataset][arm]['semantic_accuracy']=fresh['fields']
        for arm in ('C','E'):
            arms=all_rows[dataset]
            out['fallback_analysis'][dataset][arm]=transition_analysis(arms[arm],arm,arms['B'],arms['D'])
    out['scoring_revision']={'version':'SCORER-v2','created_at':now(),'code_sha256':sha(__file__),
        'reason':'C retains a legacy broad auxiliary head alongside new named reconciled factors. The frozen v1 scorer incorrectly selected that auxiliary value for the challenge broad union. Derive the union from the new reconciled schema whenever it is available. A/B native broad output remains valid for their legacy schema.',
        'inference_changed':False,'expected_assertions_changed':False,'thresholds_changed':False,
        'original_summary':'SUMMARY.json','projection_changes':'SCORER-v2-PROJECTIONS.json',
        'warning':'This is a disclosed post-freeze scoring correction, not a fresh blind evaluation. No failed assertions were removed.'}
    write(root/'SCORER-v2-PROJECTIONS.json',audit)
    # All C threshold settings invoked the same full model on every validation row.
    # Reprojection changes scoring but cannot change their tied routing ranking.
    validation,_=project(lines(root/'validation-C.jsonl'),'C');m=summarize(validation)
    selection=read(root/'VALIDATION-SELECTION.json')
    write(root/'SCORER-v2-VALIDATION-CHECK.json',{'C_corrected_assertion_accuracy':m['assertion_accuracy'],
        'C_original_assertion_accuracy':selection['sweeps']['C'][0]['combined_assertion_accuracy'],
        'C_all_routing_settings_escalate_every_case':all(r['llm_escalation_rate']==1 for r in selection['sweeps']['C']),
        'C_selected_threshold_ranking_unchanged':True,'E_projection_unchanged':True,
        'disagreement_preferences':'Unchanged; none selected on direct common predicates',
        'models_prompts_training_criteria_unchanged':True})
    write(root/'CORRECTED-SUMMARY.json',out)
    old=Path(report_path) if report_path else Path('data/reports/LAYA_LOCAL_LLM_AE_EVALUATION.md')
    preserved=root/'FROZEN-SCORER-V1.md'
    with preserved.open('x') as f:f.write(old.read_text())
    fmt=lambda x:'—' if x is None else f'{x:.1%}'
    doc=['# Controlled A–E local-model experiment','',
        '**Quality gate NOT MET. Automation disabled. These are synthetic/authored measurements, not customer accuracy.**','',
        '## Scoring correction and audit','',out['scoring_revision']['reason'],'',
        'This correction was identified after freeze and is disclosed rather than hidden. It changes only the evaluator projection of the old broad challenge assertion. The original frozen scorer, its numbers, all raw model results and every expected assertion remain intact. No model, prompt, threshold, preprocessing or classification criterion was adjusted. See `SCORER-v2-PROJECTIONS.json` for every projection and the separate validation check confirming routing selection is unchanged. The original report is [preserved here]('+os.path.relpath(preserved,old.parent)+').',
        '', 'A: base whole-text Laya. B: historical whole-text fine-tune. C: B plus real local fallback. D: independent local LLM. E: optional parser, narrow fine-tuned Laya, real local fallback, reconciliation and deterministic rules.',
        '', 'Local model: `zai-org/GLM-4.7-Flash`, Q4_K_M, Ollama 0.34.3; exact digest and selection: [LOCAL_LLM_SELECTION.md](LOCAL_LLM_SELECTION.md). 16,384 configured context, temperature 0, seed 42, thinking disabled, native JSON-schema constraints. No cloud API. No generated confidence is treated as a probability.', '']
    for dataset,arms in out['datasets'].items():
        doc += [f'## {dataset}', '',out['test_status'][dataset]+'.','',
            '| Architecture | Cases satisfying all supplied assertions | Frozen scorer v1 | Votability | Blocking YES recall | POA YES recall | Status agreement (labelled n) | LLM calls | Median / p95 ms |',
            '|---|---:|---:|---:|---:|---:|---:|---:|---:|']
        for arm,m in arms.items():
            v=m['fields'].get('votability',{});b=m['fields'].get('share_blocking',{});p=m['fields'].get('poa_required',{})
            doc.append(f'| {arm} | {m["cases_satisfying_all_supplied_assertions"]}/{m["cases"]} | {m["frozen_scorer_v1_cases_passed"]}/{m["cases"]} | {v.get("correct",0)}/{v.get("n",0)} | {fmt(b.get("positive_recall"))} (n={b.get("positive_support",0)}) | {fmt(p.get("positive_recall"))} (n={p.get("positive_support",0)}) | {fmt(m["customer_status_accuracy"])} ({m["final_status_labelled_cases"]}) | {m["llm_invocations"]}/{m["cases"]} | {m["median_latency_ms"]:.0f}/{m["p95_latency_ms"]:.0f} |')
        doc+=['','All supplied assertions is a case-level conjunction. On the 57-case challenge it does **not** mean final-status accuracy; only four status labels exist. Unlabelled factors never count as correct. Missing capabilities remain NOT_SUPPORTED and count as wrong. All manual-review flags remain true because the customer gate is disabled.', '']
        doc+=['Labelled-factor exact match (excludes the separately scored status; incomplete truth stays explicitly partial): '+', '.join(f'{a}: {m["supplied_factor_exact_match"]["correct"]}/{m["supplied_factor_exact_match"]["n"]}' for a,m in arms.items())+'.','']
        if dataset=='complete':
            doc+=['All-factor exact match (nine semantic fields plus deadline): '+', '.join(f'{a}: {m["all_factor_exact_match_correct"]}/{m["fully_labelled_factor_cases"]}' for a,m in arms.items())+'.', '']
        doc+=['Common-policy status sensitivity (same new rule table applied to the recorded facts, without inventing missing facts): '+', '.join(f'{a}: {m["common_policy_status_metrics"]["correct"]}/{m["common_policy_status_metrics"]["n"]}' for a,m in arms.items() if m['common_policy_status_metrics'])+'.','']
        doc+=['### Affirmative/negative detection','',
            '| Arm | Field | Correct/n | Positive support | Negative support | Positive precision | Positive recall | Specificity | Positive F1 | Balanced accuracy |',
            '|---|---|---:|---:|---:|---:|---:|---:|---:|---:|']
        for arm,m in arms.items():
            for field,f in m['fields'].items():
                if field in ('deadline_status','classification'):continue
                doc.append(f'| {arm} | {field} | {f["correct"]}/{f["n"]} | {f["positive_support"]} | {f["negative_support"]} | {fmt(f["positive_precision"])} | {fmt(f["positive_recall"])} | {fmt(f["negative_recall_specificity"])} | {fmt(f["positive_f1"])} | {fmt(f["balanced_accuracy"])} |')
        for arm in ('C','E'):
            t=out['fallback_analysis'][dataset][arm]
            doc += ['',f'### {arm}: fallback repairs and damage','',
                '| Semantic assertion transition | LLM answer | Reconciled answer |','|---|---:|---:|']
            for transition in ('wrong → correct','correct → correct','correct → wrong','wrong → wrong'):
                doc.append(f'| {transition} | {t["semantic_assertion_transition_llm"].get(transition,0)} | {t["semantic_assertion_transition_reconciled"].get(transition,0)} |')
            o=t['oracle'];doc+=['',f'Case transition matrix: `{json.dumps(t["case_transition_reconciled"])}`.',
                '',f'**Oracle fallback upper bound** using independent D: {o["oracle_cases_correct"]}/{o["cases"]} cases, invoking a generator only on the {o["oracle_invocations"]} specialist failures known perfectly by an oracle. The independent generator is a different mode from the actual context-bearing fallback; this is an analytical independent-mode bound, not measured deployable C/E performance. The per-assertion mixing bound is {o["oracle_per_assertion_correct"]}/{o["semantic_assertions"]}; it can mix models within a case and is even more optimistic.', '']
    doc+=['## Validation and operating point','',
        'Only 40 unique examples selected deterministically from the supplied validation file were used for gate selection. All 32 score/margin combinations are retained. Expanded predicate truth is absent from this file, and it overlaps historical training: the operating point is exploratory.',
        '', 'No numerical cutoff improved the selected trade-off. The frozen gate uses UNKNOWN, unsupported required predicates, conflicts and long/truncated input. Required missing capabilities force C to invoke the LLM on every case. E uses nine narrow questions, but only votability, blocking and POA were domain fine-tuned; six targets are generic transfer inference. Too few direct disagreements supported any model-preference rule, so concrete disagreements remain unresolved/manual review.',
        '', '| Arm | Score threshold | Laya-only coverage | LLM rate | Labelled-assertion agreement (frozen scorer) | Votability FN rate | Median ms |',
        '|---|---:|---:|---:|---:|---:|---:|']
    for arm,rows in selection['sweeps'].items():
        for r in rows:
            if r['routing']['min_margin'] is not None:continue
            doc.append(f'| {arm} | {r["routing"]["min_score"]} | {fmt(r["laya_only_coverage"])} | {fmt(r["llm_escalation_rate"])} | {fmt(r["combined_assertion_accuracy"])} | {fmt(r["votability_false_negative_rate"])} | {r["median_latency_ms"]:.0f} |')
    doc+=['','For C the separately stored corrected projection changes validation agreement but cannot change threshold ranking: every grid point made the same calls. E is unaffected. No test metric selected a threshold.',
        '', '## Limits, remaining errors and next experiment','',
        'No additional Laya training was performed. The historical 300-train/100-validation fine-tunes were reused, with their existing duplicate leakage and synthetic-label limitations disclosed. The 57 challenge texts and assertions were not trained on or edited. The 100-row historical key is NOT BLIND / DEVELOPMENT ONLY; every new A–E prediction was committed before the scoring stage reopened it. The 48 complete cases were separately authored, never training/tuning material; eight are standards-derived partial messages, not real SWIFT messages.',
        '', 'The 7,683 public filing excerpts remain unlabelled. Earlier deterministic scanning found no recognised ISO15022; this experiment does not turn those excerpts into verified data. Parser exact tests remain separate from semantic metrics. Structured RDDT values have precedence, narrative conflicts are visible, and unlinked replacement/cancellation messages are quarantined. Date extraction supports a conservative English subset and abstains on unsupported/ambiguous forms.',
        '', 'All per-field accuracy/F1, supports and confusion matrices are in CORRECTED-SUMMARY.json. Each failure and its available native scores/margins is in that file and in the GUI error explorer, with full raw stage trace available by record. Raw model accuracy, evidence verification and final policy agreement have separate metrics. A source-exact quotation is not a verified interpretation.',
        '', 'Latency is measured per sequential warmed notice, including rules/HTTP/generation; model-load records are separate. The fallback modes use their own actual generation, not recycled independent answers. Hardware is a shared 64 GiB Apple M3 Max; these are not dedicated production load tests.',
        '', '**The next experiment should use expert-labelled real custodian notices, including affirmative restrictions, with frozen event/near-duplicate groups.** Compare independent generation against specialist-first routing on shared supported predicates and all required factors. Do not infer customer safety or enable automation from synthetic success. The repair/damage matrices and call rates, not architectural preference, should determine whether Laya adds value.',
        '', f'Artifacts: `{root}`. Frozen inference: FREEZE.json. All raw per-arm JSONL files: PREDICTION-COMMIT.json. Original scorer: SUMMARY.json. Corrected scorer and full failures: CORRECTED-SUMMARY.json. Scorer change audit: SCORER-v2-PROJECTIONS.json. Verification: VERIFICATION.json and model reproducibility artifacts when completed.']
    old.write_text('\n'.join(doc)+'\n')
    print('Corrected projection counts:',{d:{a:m['cases_satisfying_all_supplied_assertions'] for a,m in arms.items()} for d,arms in out['datasets'].items()})
    return out

if __name__=='__main__':
    from semantic_pipeline.experiment import ROOT
    correct(ROOT)
