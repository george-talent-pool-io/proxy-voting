"""Post-hoc descriptive error/cost analysis, not model selection or explanation generation."""
import json
from collections import Counter
from pathlib import Path
from semantic_pipeline.schema import PREDICATES, NOT_SUPPORTED
from semantic_pipeline.metrics import summarize, truth, observed
from evaluation.ae_scoring import project


def analyse(root, report_path=None):
    from semantic_pipeline.experiment import read,write,lines,sha,verify,now
    verify();summary=read(root/'CORRECTED-SUMMARY.json');data={}
    key=read(root/'synthetic-development-truth.json')
    for dataset in ('challenge','synthetic-development','complete'):
        data[dataset]={}
        for arm in 'ABCDE':
            rows=lines(root/f'{dataset}-{arm}.jsonl')
            if dataset=='synthetic-development':
                for r in rows:r['expected']=key[r['id']]
            rows,_=project(rows,arm);m=summary['datasets'][dataset][arm]
            accepted=[r for r in rows if arm!='D' and not r['result']['escalation']['escalated']]
            accepted_metrics=summarize(accepted)
            sources=Counter();kinds=Counter();raw_llm_votes=Counter();prediction_patterns=Counter()
            invalid_quotes=0;model_calls=0
            for row in rows:
                r=row['result'];kinds[r['parser']['kind'] if r['parser'] else 'DETECTOR_NOT_RUN']+=1
                model_calls+=r.get('laya') is not None and (r['laya'].get('raw') is not None)
                for k in PREDICATES:
                    a=r['reconciliation']['predicates'].get(k,{})
                    value=a.get('value',NOT_SUPPORTED);source=a.get('source','UNAVAILABLE')
                    if value==NOT_SUPPORTED:bucket='NOT_SUPPORTED'
                    elif value in ('UNKNOWN','UNCERTAIN'):bucket='UNRESOLVED'
                    elif source.startswith('ISO'):bucket='AUTHORITATIVE_STRUCTURE'
                    elif source=='LAYA_LLM_AGREEMENT':bucket='BOTH_MODELS_AGREE'
                    elif source=='LOCAL_LLM':bucket='LOCAL_LLM'
                    elif source.startswith('LAYA'):bucket='LAYA'
                    else:bucket=source
                    sources[bucket]+=1
                d=r['deadline']
                if d['status']=='UNKNOWN':sources['UNRESOLVED']+=1
                elif d['source']=='LEGACY_LAYA_TEMPORAL_HEAD':sources['LAYA']+=1
                elif d['source']=='LLM_EXACT_PASSAGE_DETERMINISTIC_COMPARISON':sources['LLM_EXTRACTION_PLUS_DETERMINISTIC_DATE']+=1
                else:sources['DETERMINISTIC_DATE']+=1
                llm=r.get('llm')
                if llm and llm.get('valid'):
                    raw_llm_votes[llm['parsed']['votability']]+=1
                    invalid_quotes+=llm['evidence_validation']['invalid_count']
                for k,v in truth(row['expected']).items():
                    p=observed(r).get(k,NOT_SUPPORTED)
                    if p!=v:prediction_patterns[(k,v,p)]+=1
            assert sum(sources.values())==len(rows)*10
            data[dataset][arm]={'cases':len(rows),'decision_fact_slots':len(rows)*10,
                'fact_resolution_attribution':dict(sources),'detector_kinds':dict(kinds),
                'laya_records_executed':model_calls,'llm_invocations':m['llm_invocations'],
                'llm_invocation_rate':m['llm_invocations']/len(rows),
                'human_review_required':m['manual_review_count'],'policy_uncertain_status':m['uncertain_final_status_count'],
                'laya_accepted_without_llm':len(accepted),
                'accepted_cases_satisfying_all_supplied_assertions':accepted_metrics['cases_satisfying_all_supplied_assertions'],
                'accepted_wrong_cases':len(accepted)-accepted_metrics['cases_satisfying_all_supplied_assertions'],
                'accepted_labelled_assertions':accepted_metrics['assertions'],
                'accepted_correct_assertions':accepted_metrics['correct_assertions'],
                'raw_llm_votability_distribution':dict(raw_llm_votes),
                'invalid_evidence_quotations':invalid_quotes,
                'error_patterns':[{'field':k,'expected':v,'predicted':p,'count':n} for (k,v,p),n in prediction_patterns.most_common()],
                'note':'Accepted means no generator call in this experiment, NOT production auto-processing; every result still requires review.'}
    write(root/'ERROR-COST-ANALYSIS.json',{'created_at':now(),'datasets':data,
        'fact_denominator':'Nine semantic predicates plus deadline for every record, including non-votable notices. Structure/rules do not receive credit for unrelated ISIN/reference fields. LLM date extraction plus deterministic comparison is not counted as purely deterministic.',
        'source':'Attribution of non-UNKNOWN reported values, not certification that model facts are correct. Descriptive counts from actual frozen predictions; no generated causal explanations'})
    target=(Path(report_path) if report_path else Path('data/reports/LAYA_LOCAL_LLM_AE_EVALUATION.md'))
    with target.open('a') as f:
        f.write('\n\n## Measured fast-path quality and fact attribution\n\n')
        f.write('This separates avoiding an LLM call from safe automation. All records still require human review. A wrong accepted case means one or more supplied assertions failed; it is not necessarily a fully labelled final-status error.\n\n')
        f.write('| Dataset | Arm | No-LLM accepted cases | Accepted cases meeting all supplied assertions | Wrong accepted cases | LLM calls | Policy UNCERTAIN |\n|---|---|---:|---:|---:|---:|---:|\n')
        for dataset,arms in data.items():
            for arm in ('C','E'):
                v=arms[arm];f.write(f'| {dataset} | {arm} | {v["laya_accepted_without_llm"]}/{v["cases"]} | {v["accepted_cases_satisfying_all_supplied_assertions"]}/{v["laya_accepted_without_llm"]} | {v["accepted_wrong_cases"]} | {v["llm_invocations"]}/{v["cases"]} | {v["policy_uncertain_status"]} |\n')
        f.write('\nIndependent D raw votability distribution on the challenge: '+json.dumps(data['challenge']['D']['raw_llm_votability_distribution'])+'. This distinguishes model over-abstention from evidence filtering or decision-rule effects. It describes this pinned model/prompt/reasoning configuration, not local LLMs generally. The system-role canary confirmed the runtime received the system instruction.\n\n')
        f.write('`ERROR-COST-ANALYSIS.json` provides every repeated expected→predicted pattern and exclusive attribution of ten decision-fact slots per record. No explanation of why a neural model erred was invented. Fact-source counts and detector coverage are not parser accuracy.\n')
    print('Error/cost analysis persisted',flush=True)
    return data

if __name__=='__main__':
    from semantic_pipeline.experiment import ROOT
    analyse(ROOT)
