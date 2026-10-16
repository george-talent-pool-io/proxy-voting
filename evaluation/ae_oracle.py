"""Post-test, truth-selected diagnostic upper bounds, never routing/tuning data.
Independent D is NOT an upper bound on a differently prompted fallback. For E,
generate missing fallback-context responses only for specialist-wrong cases;
keep these calls outside the timed A–E experiment and its invocation rates.
"""
import copy
from pathlib import Path
from semantic_pipeline.fallback import OllamaFallback
from semantic_pipeline.experiment import lines,read,append,write,sha,verify,now
from semantic_pipeline.metrics import observed,truth
from semantic_pipeline.reporting import component_before
from semantic_pipeline.pipeline import prepare,resolve_deadline,diagnostic
from semantic_pipeline.reconcile import reconcile
from semantic_pipeline.decision import decide
from evaluation.ae_scoring import project


def case_ok(result,gold):return all(observed(result).get(k,'NOT_SUPPORTED')==v for k,v in truth(gold).items())

def analyse(root, report_path=None):
    verify();assert (root/'PREDICTION-COMMIT.json').exists()
    model=OllamaFallback();answers=read(root/'synthetic-development-truth.json');out={}
    path=root/'ORACLE-COUNTERFACTUALS.jsonl'
    cache={(r['dataset'],r['id']):r for r in lines(path)}
    for dataset in ('challenge','synthetic-development','complete'):
        b={r['id']:r for r in lines(root/f'{dataset}-B.jsonl')};out[dataset]={}
        if dataset=='synthetic-development':
            for r in b.values():r['expected']=answers[r['id']]
        for arm in ('C','E'):
            rows,_=project(lines(root/f'{dataset}-{arm}.jsonl'),arm)
            n=len(rows);base_correct=raw_oracle_correct=merged_oracle_correct=required=new_calls=0;per_case=[]
            for row in rows:
                if dataset=='synthetic-development':row['expected']=answers[row['id']]
                raw=row['result'];gold=row['expected'];before=component_before(row,arm,b)
                if case_ok(before,gold):
                    base_correct+=1;raw_oracle_correct+=1;merged_oracle_correct+=1;continue
                required+=1;llm=raw.get('llm')
                if not llm:
                    entry=cache.get((dataset,row['id']))
                    if entry:llm=entry['llm']
                    else:
                        llm=model.analyse(original_text=row['text'],narrative_text=raw['narrative_text'],
                            structured_facts=raw['structured_facts'],laya_result=diagnostic(raw['laya']),mode='FALLBACK')
                        entry={'dataset':dataset,'id':row['id'],'input_hash':raw['input_hash'],
                            'purpose':'ORACLE_POST_TEST_DIAGNOSTIC_ONLY_NOT_ROUTING_OR_TUNING',
                            'expected_answer_supplied_to_model':False,'timestamp':now(),'llm':llm}
                        append(path,entry);cache[(dataset,row['id'])]=entry;new_calls+=llm.get('invoked',False)
                        print('Oracle diagnostic',dataset,arm,row['id'],llm['valid'],flush=True)
                p=prepare(row['text'],arm=='E');deadline=resolve_deadline(row['text'],p,llm)
                only=reconcile(p['structured'],None,llm)
                candidate={**raw,'reconciliation':only,'deadline':deadline,
                    'decision':decide(only['predicates'],deadline,only['conflicts'],p['quarantined'])}
                selection=read(root/'VALIDATION-SELECTION.json');merged=reconcile(p['structured'],raw['laya'],llm,selection['reconciliation_policies'].get(arm,{}))
                constrained={**raw,'reconciliation':merged,'deadline':deadline,
                    'decision':decide(merged['predicates'],deadline,merged['conflicts'],p['quarantined'])}
                if deadline.get('conflict'):
                    candidate['decision']=decide(only['predicates'],deadline,only['conflicts']+['Conflicting deadline facts'],p['quarantined'])
                    constrained['decision']=decide(merged['predicates'],deadline,merged['conflicts']+['Conflicting deadline facts'],p['quarantined'])
                if not llm.get('valid'):
                    candidate['decision']=decide(only['predicates'],deadline,['Required fallback unavailable'],p['quarantined'])
                    constrained['decision']=decide(merged['predicates'],deadline,['Required fallback unavailable'],p['quarantined'])
                constrained=project([{'id':row['id'],'result':constrained}],arm)[0][0]['result']
                corrected=case_ok(candidate,gold);reconciled=case_ok(constrained,gold)
                raw_oracle_correct+=corrected;merged_oracle_correct+=reconciled
                per_case.append({'id':row['id'],'baseline_correct':False,'raw_fallback_correct':corrected,
                    'frozen_reconciliation_correct':reconciled,'llm_request_hash':llm['request_hash']})
            out[dataset][arm]={'cases':n,'baseline_cases_correct':base_correct,
                'oracle_invocations':required,'oracle_invocation_rate':required/n,
                'oracle_raw_fallback_switch_cases_correct':raw_oracle_correct,
                'oracle_with_frozen_reconciliation_cases_correct':merged_oracle_correct,
                'additional_diagnostic_invocations_this_process':new_calls,
                'per_failed_specialist_case':per_case,
                'scope':'Perfect truth-selected gate; not deployable; no labels supplied to models. Raw-switch bound assumes knowing when to keep a correct specialist case; within-case field damage can still prevent a case pass.'}
    write(root/'ORACLE-FALLBACK-ANALYSIS.json',{'created_at':now(),'datasets':out,
        'counterfactual_hash':sha(path) if path.exists() else None,
        'counterfactual_invocations_total':sum(r['llm'].get('invoked',False) for r in lines(path)),
        'excluded_from_main_timed_comparison':True,'automation_enabled':False,
        'model_prompt_thresholds_unchanged':True,'must_not_be_used_for_threshold_selection':True})
    report=(Path(report_path) if report_path else Path('data/reports/LAYA_LOCAL_LLM_AE_EVALUATION.md'))
    with report.open('a') as f:
        f.write('\n\n## Oracle fallback analysis — actual fallback context\n\n')
        f.write('Independent D and fallback C/E use different prompts/context, so an independent-mode oracle is not an upper bound on context-bearing fallback. This additional diagnostic reuses actual fallback outputs and generates the missing E outputs only for specialist-wrong cases. Those extra calls occur after the timed experiment and are excluded from its call rates/latency. Expected answers are used to select oracle cases only; they are never sent to the model. These outputs must not tune a deployment gate.\n\n')
        f.write('| Dataset | Arm | Specialist cases correct | Perfect-gate calls | Oracle raw-fallback switch correct | Oracle frozen-reconciliation correct |\n|---|---|---:|---:|---:|---:|\n')
        for d,arms in out.items():
            for a,m in arms.items():f.write(f'| {d} | {a} | {m["baseline_cases_correct"]}/{m["cases"]} | {m["oracle_invocations"]}/{m["cases"]} | {m["oracle_raw_fallback_switch_cases_correct"]}/{m["cases"]} | {m["oracle_with_frozen_reconciliation_cases_correct"]}/{m["cases"]} |\n')
        f.write('\nThis is a mode-specific analytical/diagnostic ceiling under perfect knowledge of specialist errors, not measured attainable coverage. No final-status accuracy is inferred for unlabelled challenge cases. Raw outputs are in ORACLE-COUNTERFACTUALS.jsonl; all oracle case outcomes are retained in ORACLE-FALLBACK-ANALYSIS.json.\n')
    return out

if __name__=='__main__':
    from semantic_pipeline.experiment import ROOT
    analyse(ROOT)
