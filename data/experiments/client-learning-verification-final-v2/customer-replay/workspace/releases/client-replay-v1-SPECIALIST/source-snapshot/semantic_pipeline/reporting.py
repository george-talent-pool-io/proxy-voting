"""Score only after persisted predictions; never consumed by training or routing."""
import copy
import csv
import hashlib
import io
import json
from collections import Counter
from pathlib import Path
from zipfile import ZipFile
from semantic_pipeline.metrics import summarize, observed, truth, field_metrics
from semantic_pipeline.reconcile import reconcile, llm_factors
from semantic_pipeline.pipeline import prepare, resolve_deadline
from semantic_pipeline.decision import decide
from semantic_pipeline.schema import PREDICATES, NOT_SUPPORTED


def component_before(row,arm,base_index):
    if arm=='C':return base_index[row['id']]['result']
    r=copy.deepcopy(row['result']);p=prepare(row['text'],True)
    merged=reconcile(p['structured'],r['laya'],None)
    deadline=resolve_deadline(row['text'],p)
    return {**r,'reconciliation':merged,'deadline':deadline,
        'decision':decide(merged['predicates'],deadline,merged['conflicts'],p['quarantined'])}


def transition_analysis(rows,arm,baseline_rows,independent_rows):
    baseline={r['id']:r for r in baseline_rows};independent={r['id']:r for r in independent_rows}
    raw_matrix=Counter();merged_matrix=Counter();case_matrix=Counter();disagreements=Counter()
    oracle={'cases':len(rows),'baseline_cases_correct':0,'independent_llm_cases_correct':0,
        'oracle_cases_correct':0,'oracle_invocations':0,'baseline_semantic_assertions_correct':0,
        'oracle_per_assertion_correct':0,'semantic_assertions':0,
        'scope':'Analytical upper bound using independent LLM D on the same inputs; perfect error detection is unavailable in deployment. Per-assertion oracle can mix models and is more optimistic than case switching.'}
    for row in rows:
        r=row['result'];pre=component_before(row,arm,baseline)
        a=observed(pre);b=observed(r);d=observed(independent[row['id']]['result']);gold=truth(row['expected'])
        passed_a=all(a.get(k,NOT_SUPPORTED)==v for k,v in gold.items());passed_b=all(b.get(k,NOT_SUPPORTED)==v for k,v in gold.items());passed_d=all(d.get(k,NOT_SUPPORTED)==v for k,v in gold.items())
        oracle['baseline_cases_correct']+=passed_a;oracle['independent_llm_cases_correct']+=passed_d
        oracle['oracle_cases_correct']+=passed_a or passed_d;oracle['oracle_invocations']+=not passed_a
        llm=r.get('llm');lp=llm_factors(llm)
        if llm and llm.get('invoked'):case_matrix[f'{"correct" if passed_a else "wrong"} → {"correct" if passed_b else "wrong"}']+=1
        for key,v in gold.items():
            if key in ('classification','deadline_status'):continue
            aa=a.get(key,NOT_SUPPORTED);bb=b.get(key,NOT_SUPPORTED);dd=d.get(key,NOT_SUPPORTED)
            oracle['semantic_assertions']+=1;oracle['baseline_semantic_assertions_correct']+=aa==v;oracle['oracle_per_assertion_correct']+=(aa==v or dd==v)
            if not (llm and llm.get('invoked')):continue
            if key=='other_restriction':
                vals=[lp.get(k,{}).get('value',NOT_SUPPORTED) for k in PREDICATES if k not in ('votability','share_blocking','poa_required')]
                rr='YES' if 'YES' in vals else 'NO' if all(x=='NO' for x in vals) else 'UNKNOWN'
            else:rr=lp.get(key,{}).get('value',NOT_SUPPORTED)
            raw_matrix[f'{"correct" if aa==v else "wrong"} → {"correct" if rr==v else "wrong"}']+=1
            merged_matrix[f'{"correct" if aa==v else "wrong"} → {"correct" if bb==v else "wrong"}']+=1
            disagreements[key]+=aa!=rr
    return {'semantic_assertion_transition_llm':dict(raw_matrix),
        'semantic_assertion_transition_reconciled':dict(merged_matrix),
        'case_transition_reconciled':dict(case_matrix),'labelled_predicate_disagreements':dict(disagreements),
        'oracle':oracle,'definitions':'Raw LLM transition uses evidence-validated generative facts; reconciled transition uses actual final semantic facts. NOT_SUPPORTED counts as wrong, not omitted.'}


def report(root, report_path=None):
    from semantic_pipeline.experiment import verify,read,write,lines,sha,now
    verify();commit=read(root/'PREDICTION-COMMIT.json')
    for p,h in commit['files'].items():
        if sha(p)!=h:raise ValueError('Persisted predictions changed before scoring')
    # This file has already been exposed in the historical experiment. Still enforce commit-first access.
    with ZipFile('data/training/laya_voting_synthetic_500.zip') as z:
        key=list(csv.DictReader(io.StringIO(z.read('synthetic_frozen_test_100_ANSWER_KEY.csv').decode('utf-8-sig'))))
    test_truth={r['id']:{'votability':r['votability'],**{k:r[k] for k in ('share_blocking','poa_required','other_restriction','deadline_status')},
        'classification':r['expected_customer_status']} for r in key}
    if not (root/'synthetic-development-truth.json').exists():write(root/'synthetic-development-truth.json',test_truth)
    all_rows={};datasets={};fallback={};layer_metrics={}
    for dataset in ('challenge','synthetic-development','complete'):
        arms={arm:lines(root/f'{dataset}-{arm}.jsonl') for arm in 'ABCDE'}
        expected_ids=[r['id'] for r in arms['A']]
        for arm,rows in arms.items():
            if [r['id'] for r in rows]!=expected_ids:raise ValueError('Architectures used different examples')
            for r in rows:
                if hashlib.sha256(r['text'].encode()).hexdigest()!=r['input_hash']:raise ValueError('Input hash mismatch')
                if dataset=='synthetic-development':r['expected']=test_truth[r['id']]
        all_rows[dataset]=arms;datasets[dataset]={};fallback[dataset]={};layer_metrics[dataset]={}
        for arm,rows in arms.items():
            m=summarize(rows)
            factor_cases=[r for r in rows if set(PREDICATES)|{'deadline_status'}<=set(truth(r['expected']))]
            m['fully_labelled_factor_cases']=len(factor_cases)
            m['all_factor_exact_match_accuracy']=sum(all(observed(r['result']).get(k,NOT_SUPPORTED)==v for k,v in truth(r['expected']).items() if k!='classification') for r in factor_cases)/len(factor_cases) if factor_cases else None
            m['all_factor_exact_match_correct']=round(m['all_factor_exact_match_accuracy']*len(factor_cases)) if factor_cases else None
            common_truth=[];common_predictions=[]
            for rr in rows:
                gg=truth(rr['expected'])
                if 'classification' not in gg:continue
                xx=rr['result']
                dd=decide(xx['reconciliation']['predicates'],xx['deadline'],xx['reconciliation']['conflicts'])
                common_truth.append(gg['classification']);common_predictions.append(dd['classification'])
            m['common_policy_status_metrics']=field_metrics(common_truth,common_predictions) if common_truth else None
            m['customer_status_policy']='Canonical VOTABLE_WITH_RESTRICTION collapses SHARE_BLOCKING/POA_REQUIRED; raw native status retained. A/B use frozen legacy precedence; C/D/E shared deterministic policy. Supplied synthetic source uses blocking-priority buckets.'
            # Explain which errors belong to modelling vs exact quote filtering vs policy.
            native={};quote_totals=Counter()
            for r in rows:
                gold=truth(r['expected']);llm=r['result'].get('llm')
                if llm and llm.get('valid'):
                    for k in PREDICATES:
                        if k in gold:
                            native.setdefault(k,([],[]));native[k][0].append(gold[k]);native[k][1].append(llm['parsed'][k])
                    for qs in llm['evidence_validation']['predicates'].values():
                        for q in qs:quote_totals['total']+=1;quote_totals['valid']+=q['valid']
                    quote_totals['invalid']+=llm['evidence_validation']['invalid_count']
            layer_metrics[dataset][arm]={'raw_llm_predicate_metrics':{k:field_metrics(y,p,'VOTABLE' if k=='votability' else 'YES') for k,(y,p) in native.items()},'exact_evidence_checks':dict(quote_totals),
                'parser_accuracy':'No production labels; controlled fixture assertions reported separately',
                'semantic_accuracy':m['fields'],'end_to_end_status_accuracy':m['customer_status_accuracy'],'end_to_end_status_n':m['final_status_labelled_cases']}
            datasets[dataset][arm]=m
        for arm in ('C','E'):
            fallback[dataset][arm]=transition_analysis(arms[arm],arm,arms['B'],arms['D'])
    result={'created_at':now(),'frozen_manifest_sha256':sha(root/'FREEZE.json'),
        'model':read(Path('semantic_pipeline/llm-config.json')),'datasets':datasets,
        'fallback_analysis':fallback,'layer_metrics':layer_metrics,
        'automation_enabled':False,'customer_accuracy':None,
        'denominator_note':'Only labelled assertions enter per-field metrics. Missing capability NOT_SUPPORTED is an error. Case pass on partial labels is not whole-record final-status accuracy.',
        'quality_gate':{'passed':False,'reasons':['Zero independently expert-labelled real notices','All evaluation sources synthetic or authored','Old synthetic test exposed and duplicate-contaminated','Expanded predicates have no independent validation']},
        'timing_scope':'Actual sequential per-notice wall time, warmed local models, includes rules/HTTP/model generation. Model load is outside per-notice latency; no inference cache between arms.',
        'test_status':{'challenge':'Frozen authored partial assertions; repeatedly observed historical benchmark, not a new blind set',
            'synthetic-development':'NOT BLIND / DEVELOPMENT ONLY, previously exposed key and duplicate overlap',
            'complete':'SYNTHETIC_COMPLETE_BENCHMARK; complete authored truth, not expert/customer accuracy'}}
    write(root/'SUMMARY.json',result)
    for dataset,arms in datasets.items():
        write(root/f'{dataset}-FAILURES.json',{arm:m['failures'] for arm,m in arms.items()})
    md=['# Controlled local Laya / LLM A–E experiment','',
        '**Customer quality gate NOT MET. Automation remains disabled. No customer accuracy is established.**','',
        '## Protocol and models','',
        'All architectures used the same inputs and supplied truth. A = official base whole-text Laya; B = historical full-encoder fine-tune; C = B plus real local fallback; D = independent local LLM; E = optional ISO parser, fine-tuned narrow Laya, real fallback, reconciliation and rules. No new fine-tuning occurred. Original checkpoints and the 57-case challenge were retained.',
        '',f'Local LLM: `{result["model"]["checkpoint"]}`, `{result["model"]["model_digest"]}`, {result["model"]["quantisation"]}, Ollama {result["model"]["runtime_version"]}. Prompt/schema, thresholds and checkpoints were hashed before evaluation; see `FREEZE.json`. Model choice: [LOCAL_LLM_SELECTION.md](LOCAL_LLM_SELECTION.md).',
        '', 'Independent mode never receives Laya predictions. C and E use actual fallback-context generation, not recycled independent answers. LLM confidence is unavailable; native Laya probabilities are not calibrated correctness probabilities. Exact-substring checks quarantine invalid evidence. Structured facts have priority; unresolved disagreements require review. Validation-supported preferences are recorded in VALIDATION-SELECTION.json.',
        '', '## Data and denominators','',
        'The 57 cases contain partial assertions and only four explicit status labels. Historical 30/57 and 37/57 count cases satisfying all supplied assertions; they are not customer accuracy. The old 100-row key is previously exposed and has known train/test duplicate overlap: NOT BLIND / DEVELOPMENT ONLY. The 48-case complete benchmark is separately authored synthetic material, isolated from training/tuning; all nine semantic predicates, deadline status and derived customer status are labelled. Zero expert-labelled production notices were added.',
        '', 'The complete benchmark includes eight standards-derived partial messages, not public production SWIFT data. The existing 7,683 SEC excerpts remain unlabelled; prior scanning found no recognised ISO15022. They do not supply accuracy denominators.',
        '', 'A/B retain frozen legacy five-factor/status behaviour for historical comparability. They cannot independently emit the expanded predicates, which stay NOT_SUPPORTED and count as wrong on complete truth. Status buckets POA_REQUIRED/SHARE_BLOCKING are collapsed to VOTABLE_WITH_RESTRICTION for customer-status comparison, with raw status retained. C/D/E apply the new shared explicit decision policy; policy differences mean improvements are not attributable solely to a generator. A common-policy sensitivity analysis is included below.', '']
    for dataset,arms in datasets.items():
        md += [f'## {dataset}', '', f'Scope: {result["test_status"][dataset]}.', '',
            '| Architecture | All supplied assertions, cases | Correct assertions | Votability | Blocking YES recall | POA YES recall | Status accuracy (n) | Median / p95 ms | LLM calls |',
            '|---|---:|---:|---:|---:|---:|---:|---:|---:|']
        for arm,m in arms.items():
            fmt=lambda v:'unavailable' if v is None else f'{v:.1%}'
            vf=m['fields'].get('votability',{});bf=m['fields'].get('share_blocking',{});pf=m['fields'].get('poa_required',{})
            md.append(f'| {arm} | {m["cases_satisfying_all_supplied_assertions"]}/{m["cases"]} | {m["correct_assertions"]}/{m["assertions"]} | {vf.get("correct",0)}/{vf.get("n",0)} | {fmt(bf.get("positive_recall"))} (n={bf.get("positive_support",0)}) | {fmt(pf.get("positive_recall"))} (n={pf.get("positive_support",0)}) | {fmt(m["customer_status_accuracy"])} ({m["final_status_labelled_cases"]}) | {m["median_latency_ms"]:.0f} / {m["p95_latency_ms"]:.0f} | {m["llm_invocations"]}/{m["cases"]} |')
        md += ['', 'Every field\'s support, positive precision/recall, specificity, F1, balanced accuracy and full confusion matrix is in SUMMARY.json. Every failure, with source text, score/margin where available, conflicts and escalation reasons, is in the corresponding `*-FAILURES.json` and the GUI error explorer.', '']
        md += ['Common decision-policy status agreement (identical explicit rule table; missing expanded facts remain unresolved): '+', '.join(f'{a}: {m["common_policy_status_metrics"]["correct"]}/{m["common_policy_status_metrics"]["n"]}' for a,m in arms.items() if m['common_policy_status_metrics'])+'.', '']
        if dataset=='complete':
            md += ['| Architecture | All-factor exact match |', '|---|---:|']+[f'| {arm} | {m["all_factor_exact_match_correct"]}/{m["fully_labelled_factor_cases"]} |' for arm,m in arms.items()]+['']
        for arm in ('C','E'):
            t=fallback[dataset][arm]
            md += [f'### {arm}: fallback transitions','',f'Final semantic assertion transitions: `{json.dumps(t["semantic_assertion_transition_reconciled"])}`.',
                '',f'Raw evidence-validated LLM transitions: `{json.dumps(t["semantic_assertion_transition_llm"])}`.',
                '',f'Case transitions: `{json.dumps(t["case_transition_reconciled"])}`.',
                '',f'Oracle case-switching upper bound: {t["oracle"]["oracle_cases_correct"]}/{t["oracle"]["cases"]}, with perfect knowledge of {t["oracle"]["oracle_invocations"]} failing specialist cases. This is analytical, not deployable routing.', '']
    md += ['## Routing, policy and limitations','',
        'Routing was selected on 40 unique, deterministically selected examples from the supplied validation file, never on challenge/test scores. The full threshold sweep records specialist-only coverage, escalation, combined assertion agreement, votability false-negative rate and component latency. Validation is itself AI-synthetic and partly overlaps historical training: any operating point is exploratory. The file lacks truth for the expanded predicates, so it cannot validate their risk.',
        '', 'Whole-text Laya lacks six of the nine individually requested outputs (it supports votability, share blocking and POA; its broad other label is a separate union). Required unsupported fields therefore force fallback in C. This is a measured capability constraint, not a threshold that can be optimised away. E includes a generic holding-confirmation question; only votability, blocking and POA have historical specialist training labels. The other six targets have transfer inference, not dedicated domain supervision.',
        '', 'All manual_review_required flags remain true because the quality gate is disabled. This is distinct from the UNCERTAIN final-status count and from the LLM escalation rate. No synthetic result authorises unattended processing.',
        '', 'Deterministic dates remain a conservative English/current-deadline subset. Unsupported dates, absent timezones and unclear supersession abstain. A source-exact quotation establishes provenance, not that the model interpreted it correctly. ISO lifecycle replacements/cancellations without validated event linkage are quarantined; the previous persistent event ledger is retained, not silently bypassed.',
        '', 'Runtime errors, truncated generations, malformed JSON and invalid evidence are retained and count toward the actual pipeline outcome. Per-notice latency excludes model load; raw generation/load/token timings are saved. Hardware and runtime versions are recorded. GPU temperature-zero repeatability is measured separately, not guaranteed mathematically.',
        '', 'The most valuable next experiment is an independently expert-labelled sample of real custodian notices, including affirmative restrictions and conditional language, held out by event/near-duplicate group. Synthetic success cannot establish production safety. Select between specialist-first and generator-only using the observed error repairs, damage and latency, not a preference for either model.',
        '', '## Artifacts','',
        f'Full immutable experiment directory: `{root}`. `SUMMARY.json`, per-arm JSONL stage traces, `VALIDATION-SELECTION.json`, `PREDICTION-COMMIT.json`, `FREEZE.json` and failure lists provide reproducibility. Model and software checks are in `VERIFICATION.json` when completed.']
    target=Path(report_path) if report_path else Path('data/reports/LAYA_LOCAL_LLM_AE_EVALUATION.md')
    target.write_text('\n'.join(md)+'\n')
    print('Scored', {d:{a:m['cases_satisfying_all_supplied_assertions'] for a,m in arms.items()} for d,arms in datasets.items()},flush=True)
    return result
