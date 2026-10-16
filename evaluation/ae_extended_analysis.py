"""Post-frozen scoring diagnostics. Never imports truth into an inference request."""
import copy,json,statistics,hashlib
from collections import Counter,defaultdict
from pathlib import Path
from sklearn.metrics import roc_auc_score
from semantic_pipeline.experiment import ROOT,read,lines,write,sha,now,verify
from semantic_pipeline.metrics import observed,truth,summarize
from semantic_pipeline.reporting import component_before
from semantic_pipeline.pipeline import prepare,resolve_deadline,run
from semantic_pipeline.reconcile import reconcile
from semantic_pipeline.decision import decide
from semantic_pipeline.schema import PREDICATES
from semantic_pipeline.routing import RoutingConfig
from evaluation.ae_scoring import project

def data(dataset,arm):
    rows=project(lines(ROOT/f'{dataset}-{arm}.jsonl'),arm)[0]
    if dataset=='synthetic-development':
        labels=read(ROOT/'synthetic-development-truth.json')
        for r in rows:r['expected']=labels[r['id']]
    return rows

def llm_candidate(row,llm,arm):
    r=row['result'];p=prepare(row['text'],arm=='E');merged=reconcile(p['structured'],None,llm)
    deadline=resolve_deadline(row['text'],p,llm)
    conflicts=merged['conflicts']+(['Conflicting deadline facts'] if deadline.get('conflict') else [])
    return {**r,'reconciliation':merged,'deadline':deadline,'decision':decide(merged['predicates'],deadline,conflicts,p['quarantined'])}

def disagreement(a,b,gold):
    out=Counter();unc={'UNKNOWN','UNCERTAIN','NOT_SUPPORTED'}
    if a in unc and b in unc:out['both_effectively_uncertain']+=1
    if a==b:out['agree_correct' if a==gold else 'agree_wrong']+=1
    else:
        out['disagree_laya_correct']+=int(a==gold);out['disagree_llm_correct']+=int(b==gold)
        out['disagree_both_wrong']+=int(a!=gold and b!=gold)
        out['disagree_total']+=1;out['disagree_laya_wrong']+=int(a!=gold)
    out['n']+=1;return out

def diagnostics():
    verify();summary=read(ROOT/'CORRECTED-SUMMARY.json');out={};oraclecache={(r['dataset'],r['id']):r['llm'] for r in lines(ROOT/'ORACLE-COUNTERFACTUALS.jsonl')}
    errors=['# Every missed labelled assertion across A–E','','SCORER-v2 evaluation projections; raw native predictions are unchanged. Authored/synthetic data only. No customer accuracy. Invalid evidence quotations remain quarantined in raw audit files and are not reproduced as valid evidence here.']
    for dataset in ('challenge','synthetic-development','complete'):
        arms={a:data(dataset,a) for a in 'ABCDE'};by={a:{r['id']:r for r in rs} for a,rs in arms.items()};out[dataset]={}
        for arm in ('C','E'):
            fields=defaultdict(Counter);agree=defaultdict(Counter);fallback_agree=defaultdict(Counter);trans=defaultdict(Counter)
            for row in arms[arm]:
                gold=truth(row['expected']);r=row['result'];before=observed(component_before(row,arm,by['B']));d=observed(by['D'][row['id']]['result'])
                llm=r.get('llm') or oraclecache.get((dataset,row['id']))
                candidate=observed(llm_candidate(row,llm,arm)) if llm else {}
                after=observed(r)
                for k,v in gold.items():
                    a=before.get(k,'NOT_SUPPORTED');b=candidate.get(k,'NOT_SUPPORTED');c=fields[k];c['labelled_assertions']+=1;c['laya_correct']+=int(a==v)
                    if a!=v:
                        c['laya_errors']+=1
                        if not llm:raise ValueError(f'Missing counterfactual {dataset} {arm} {row["id"]}')
                        c['llm_correct_on_laya_errors']+=int(b==v);c['llm_incorrect_on_laya_errors']+=int(b!=v)
                    agree[k].update(disagreement(a,d.get(k,'NOT_SUPPORTED'),v))
                    if llm:fallback_agree[k].update(disagreement(a,b,v))
                    if r.get('llm',{} ) and r['llm'].get('invoked'):
                        trans[k][f'{"correct" if a==v else "wrong"} -> {"correct" if after.get(k)==v else "wrong"}']+=1
            for c in fields.values():
                c['maximum_theoretical_repairs']=c['llm_correct_on_laya_errors'];c['maximum_combined_correct']=c['laya_correct']+c['maximum_theoretical_repairs']
            totals=Counter()
            for c in fields.values():totals.update(c)
            out[dataset][arm]={'ORACLE_ROUTING':{'deployable':False,'scope':'Assertion-wise oracle can switch per labelled field; candidate uses actual fallback context with exact-evidence validation and deterministic date/status derivation. More optimistic than case-wise switching.','per_field':dict(fields),'all_labelled_assertions':dict(totals)},
                'independent_disagreement':dict(agree),'fallback_context_disagreement_observed_and_oracle':dict(fallback_agree),
                'fallback_disagreement_caveat':'E includes truth-selected oracle cases and is selection-biased. Independent D covers every identical case and is the complete-population diagnostic.',
                'actual_invocation_transitions_per_field':dict(trans)}
        # False-negative abstentions count as missed positives; explicit opposite-class errors are also separated.
        asym={}
        for arm,rs in arms.items():
            fields=defaultdict(Counter)
            for row in rs:
                y=truth(row['expected']);p=observed(row['result'])
                for k in PREDICATES:
                    if k not in y:continue
                    positive='VOTABLE' if k=='votability' else 'YES';negative='NOT_VOTABLE' if k=='votability' else 'NO';c=fields[k]
                    c['positive_support']+=int(y[k]==positive);c['negative_support']+=int(y[k]==negative)
                    c['false_negative_including_abstention']+=int(y[k]==positive and p[k]!=positive)
                    c['explicit_positive_to_negative']+=int(y[k]==positive and p[k]==negative)
                    c['false_positive']+=int(y[k]!=positive and p[k]==positive)
            asym[arm]=dict(fields)
        out[dataset]['critical_asymmetry']=asym
        # Every failure: one section per case, every failed assertion listed together with full A–E machine facts.
        for row in arms['A']:
            ident=row['id'];gold=truth(row['expected']);observations={a:observed(by[a][ident]['result']) for a in 'ABCDE'}
            failed={k:{a:p.get(k,'NOT_SUPPORTED') for a,p in observations.items()} for k,v in gold.items() if any(p.get(k,'NOT_SUPPORTED')!=v for p in observations.values())}
            if not failed:continue
            errors += ['',f'## {dataset} / {ident}','','Source:','','```text',row['text'],'```','','Ground truth and every failed assertion:', '```json',json.dumps({'ground_truth':gold,'missed_assertions_all_architectures':failed},ensure_ascii=False,indent=2),'```']
            for a in 'ABCDE':
                r=by[a][ident]['result'];llm=r.get('llm');detail={'result':observations[a],'laya_scores_evidence':(r.get('laya') or {}).get('predicates'),
                    'llm_invoked':bool(llm and llm.get('invoked')),'llm_raw_output':llm['raw_response']['message']['content'] if llm and llm.get('valid') else None,
                    'llm_evidence_validation':llm.get('evidence_validation') if llm else None,'reconciliation':r['reconciliation'],'escalation':r['escalation'],'decision':r['decision']}
                # Raw output is explicit diagnostic untrusted output, not customer evidence.
                errors += ['',f'### {a} — persisted audit (unverified model quotations are diagnostic only)','', '```json',json.dumps(detail,ensure_ascii=False,indent=2),'```']
        # Score/margin are uncalibrated; AUC is diagnostic on recorded predictions, never a tuned gate.
        score_quality={}
        for arm in ('B','E'):
            vals=defaultdict(lambda: {'score':[],'margin':[],'correct':[]})
            for row in arms[arm]:
                gold=truth(row['expected']);pre=component_before(row,'E',by['B']) if arm=='E' else row['result'];pred=observed(pre)
                for k,v in gold.items():
                    native=(row['result'].get('laya') or {}).get('predicates',{}).get(k,{})
                    if native.get('confidence') is None or native.get('margin') is None:continue
                    z=vals[k];z['score'].append(native['confidence']);z['margin'].append(native['margin']);z['correct'].append(int(pred.get(k)==v))
            score_quality[arm]={k:{'n':len(z['correct']),'correct':sum(z['correct']),**{q+'_correctness_auc':float(roc_auc_score(z['correct'],z[q])) if len(set(z['correct']))==2 else None for q in ('score','margin')}} for k,z in vals.items()}
        out[dataset]['native_score_margin_diagnostics']=score_quality
    write(ROOT/'EXTENDED-ASSERTION-DIAGNOSTICS.json',{'created_at':now(),'datasets':out,'automation_enabled':False,'post_test_diagnostic_not_routing_selection':True})
    Path('data/reports/ARCHITECTURE_COMPARISON_ERRORS.md').write_text('\n'.join(errors)+'\n')
    # Per-arm, per-dataset manifests, referencing raw immutable predictions and original pre-inference freeze.
    folder=ROOT/'manifests';folder.mkdir(exist_ok=True)
    for dataset in out:
        for arm in 'ABCDE':
            rs=data(dataset,arm);r=rs[0]['result'];llm=next((x['result']['llm'] for x in rs if x['result'].get('llm')),None)
            write(folder/f'{dataset}-{arm}.json',{'run_id':rs[0]['run_id'],'architecture':arm,'dataset':dataset,
                'dataset_hash':hashlib.sha256(json.dumps([(x['id'],x['input_hash']) for x in rs],sort_keys=True).encode()).hexdigest(),
                'prediction_file_sha256':sha(ROOT/f'{dataset}-{arm}.jsonl'),'laya_checkpoint':(r.get('laya') or {}).get('checkpoint'),
                'llm_model':llm.get('model') if llm else None,'llm_quantisation':summary['model']['quantisation'] if llm else None,
                'prompt_version':llm.get('prompt_version') if llm else None,'routing_config':r['escalation'].get('configuration'),
                'rule_version':r['decision']['rule_version'],'seed':42,'timestamp':rs[0]['timestamp'],
                'freeze_sha256':sha(ROOT/'FREEZE.json'),'posthoc_manifest_created_at':now(),'runtime_nondeterminism':'Temperature zero / fixed seed; finite reproducibility probes do not guarantee universal device determinism.'})
    print('Extended assertions, manifests, every-error report generated')

if __name__=='__main__':diagnostics()
