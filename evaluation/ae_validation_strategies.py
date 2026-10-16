"""Expanded validation-only strategy diagnostic; frozen operating points remain unchanged."""
import copy,statistics
from semantic_pipeline.experiment import ROOT,lines,read,write,now
from semantic_pipeline.schema import PREDICATES
from semantic_pipeline.pipeline import run
from semantic_pipeline.routing import RoutingConfig
from semantic_pipeline.metrics import summarize,observed,truth
from evaluation.ae_scoring import project

def select(predicates,strategy,threshold=None):
    values=[predicates.get(k,{}) for k in PREDICATES]
    unknown=any(a.get('value') in ('UNKNOWN','UNCERTAIN') for a in values)
    if strategy=='UNKNOWN':return unknown
    if strategy=='SCORE':return any(a.get('confidence') is not None and a['confidence']<threshold for a in values)
    if strategy=='MARGIN':return any(a.get('margin') is not None and a['margin']<threshold for a in values)
    if strategy=='UNKNOWN_OR_MARGIN_OR_EVIDENCE':return unknown or any(a.get('margin') is not None and a['margin']<threshold for a in values) or any(a.get('value')=='YES' and not a.get('evidence') for a in values)
    if strategy=='CRITICAL_POSITIVE_OR_UNKNOWN':return any(predicates.get(k,{}).get('value') in ('YES','VOTABLE','UNKNOWN','UNCERTAIN','NOT_SUPPORTED') for k in ('votability','share_blocking','poa_required'))
    raise ValueError('Unknown strategy')

def analyse():
    out={};independent=lines(ROOT/'validation-D.jsonl');selection=read(ROOT/'VALIDATION-SELECTION.json')
    for arm in ('C','E'):
        saved=lines(ROOT/f'validation-{arm}.jsonl');table=[]
        strategies=[('UNKNOWN',None),('CRITICAL_POSITIVE_OR_UNKNOWN',None)]+[(k,t) for k,ts in [('SCORE',[.5,.7,.8,.9,.95,.98,.995]),('MARGIN',[.1,.2,.4]),('UNKNOWN_OR_MARGIN_OR_EVIDENCE',[.1,.2,.4])] for t in ts]+[('ALWAYS_INDEPENDENT_LLM',None)]
        for name,threshold in strategies:
            items=[];repairs=damage=0;calls=0
            for row,d in zip(saved,independent):
                source=row['result'];laya=source['laya'];llm=source.get('validation_counterfactual_llm') or source.get('llm')
                if name=='ALWAYS_INDEPENDENT_LLM':r=copy.deepcopy(d['result']);sent=True
                else:
                    sent=select(laya['predicates'],name,threshold)
                    cfg=RoutingConfig(unknown=False,unsupported=False,conflict=False,max_chars=1 if sent else 2_000_001)
                    r=run(row['text'],arm,precomputed_laya=copy.deepcopy(laya),precomputed_llm=llm,routing=cfg,
                        reconciliation_policy=selection['reconciliation_policies'].get(arm,{}))
                    # Native component durations from original generation; estimates, not fresh timed invocations.
                    r['latencies']['total_ms']=laya['latency_ms']+(llm['latency_ms'] if sent else 0)
                if name!='ALWAYS_INDEPENDENT_LLM':r=project([{'id':row['id'],'result':r}],arm)[0][0]['result']
                calls+=sent;before=observed({**source,'reconciliation':{'predicates':laya['predicates']}});after=observed(r)
                for k,v in truth(row['expected']).items():
                    if k in ('classification','deadline_status'):continue
                    repairs+=int(sent and before.get(k)!=v and after.get(k)==v);damage+=int(sent and before.get(k)==v and after.get(k)!=v)
                items.append({**row,'result':r})
            items=project(items,arm)[0] if name!='ALWAYS_INDEPENDENT_LLM' else items;m=summarize(items)
            table.append({'strategy':name,'threshold':threshold,'correct_assertions':m['correct_assertions'],'labelled_assertions':m['assertions'],
                'assertion_agreement':m['assertion_accuracy'],'llm_invocations':calls,'llm_invocation_rate':calls/len(items),'laya_only_coverage':1-calls/len(items),
                'repairs_semantic_assertions':repairs,'damage_semantic_assertions':damage,'review_rate':m['manual_review_count']/len(items),
                'uncertain_final_status_rate':m['uncertain_final_status_count']/len(items),'median_component_latency_estimate_ms':m['median_latency_ms'],
                'p95_component_latency_estimate_ms':m['p95_latency_ms'],'votability_false_negative_rate':1-m['fields']['votability']['positive_recall']})
        best=max(table,key=lambda r:(r['assertion_agreement'],-r['llm_invocation_rate'],-r['median_component_latency_estimate_ms']))
        out[arm]={'strategies':table,'best_validation_only':best}
    write(ROOT/'VALIDATION-STRATEGY-COMPARISON-v2.json',{'created_at':now(),'datasets':out,'validation_rows':40,'labelled_assertions_per_strategy':200,
        'operating_points_unchanged':True,'limitations':['Expanded six predicates lack validation truth','11 validation texts duplicate historical training','New strategy diagnostics were added after the main freeze; no challenge scores select a gate','Latency is recomposed from recorded component durations, not new warm execution wall times','Reduced triggers deliberately disable unsupported-output escalation; capability gaps still count as errors','Critical predicates selected because missing votability/blocking/POA can change action or required voting documentation; no monetary costs assumed'],
        'always_llm_mode':'Independent D, exactly the saved D records, not Laya-context fallback','automation_enabled':False})
    print({a:m['best_validation_only'] for a,m in out.items()})

if __name__=='__main__':analyse()
