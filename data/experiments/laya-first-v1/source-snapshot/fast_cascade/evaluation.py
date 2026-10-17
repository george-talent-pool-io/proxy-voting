"""Explicit denominators, asymmetric errors, transition and oracle accounting."""
from collections import Counter
import numpy as np
from semantic_pipeline.schema import PREDICATES
from qwen_domain.metrics import metrics
from fast_cascade.routing import CRITICAL

def values(result):
    out={**{k:v['value'] for k,v in result['predicates'].items()},'classification':result['decision']['classification']}
    broad=[out.get(k,'NOT_SUPPORTED') for k in PREDICATES if k not in ('votability','share_blocking','poa_required')]
    out['other_restriction']='YES' if 'YES' in broad else 'NO' if all(v=='NO' for v in broad) else 'UNKNOWN'
    return out

def summary(cases,predictions):
    by={r['id']:r for r in predictions};fields={};correct=total=case_ok=exact=0
    for key in list(PREDICATES)+['other_restriction','deadline_status','classification']:
        pairs=[(c['expected'][key],values(by[c['id']]['result']).get(key,'NOT_SUPPORTED')) for c in cases if key in c['expected']]
        if pairs:fields[key]=metrics([p[0] for p in pairs],[p[1] for p in pairs],key)
    for c in cases:
        p=values(by[c['id']]['result']);checks=[p.get(k,'NOT_SUPPORTED')==v for k,v in c['expected'].items()];total+=len(checks);correct+=sum(checks);case_ok+=all(checks)
        if all(k in c['expected'] for k in PREDICATES):exact+=all(p[k]==c['expected'][k] for k in PREDICATES)
    rs=[r['result'] for r in predictions];lat=[r['latency_ms'] for r in rs];n=len(rs)
    return {'cases':n,'assertions':total,'correct_assertions':correct,'assertion_correctness':correct/total if total else None,'cases_satisfying_supplied_assertions':case_ok,
        'all_nine_predicates_exact_match':exact,'fully_labelled_semantic_cases':sum(all(k in c['expected'] for k in PREDICATES) for c in cases),'fields':fields,
        'gear2_notice_rate':sum(bool(r.get('gear2')) for r in rs)/n if n else None,'gear3_notice_rate':sum(bool(r.get('full_qwen')) for r in rs)/n if n else None,
        'semantic_review_rate':sum(r.get('semantic_review_required',True) for r in rs)/n if n else None,'actual_manual_review_rate':1.,'resolved_by':dict(Counter(r.get('resolved_by','REFERENCE') for r in rs)),
        'median_latency_ms':float(np.median(lat)) if lat else None,'p95_latency_ms':float(np.percentile(lat,95)) if lat else None,
        'latency_scope':list({r.get('latency_scope','REFERENCE_SERVICE') for r in rs}),'automation_enabled':False,'customer_accuracy':None}

def transition(truth,earlier,later):
    out={'earlier_wrong_later_correct':0,'earlier_correct_later_wrong':0,'both_correct':0,'both_wrong':0}
    for y,a,b in zip(truth,earlier,later):out[('both_correct' if b==y else 'earlier_correct_later_wrong') if a==y else ('earlier_wrong_later_correct' if b==y else 'both_wrong')]+=1
    return out

def oracles(cases,laya,gear2,full):
    b={r['id']:r for r in laya};q={r['id']:r for r in gear2};f={r['id']:r for r in full};out={}
    for key in PREDICATES:
        y=[];a=[];g=[];z=[]
        for c in cases:
            if key not in c['expected']:continue
            ident=c['id'];y.append(c['expected'][key]);a.append(b[ident]['result']['predicates'][key]['value']);g.append(q[ident]['result']['predicates'][key]['value']);z.append(f[ident]['result']['predicates'].get(key,{}).get('value','NOT_SUPPORTED'))
        tr=transition(y,a,z);tr2=transition(y,a,g)
        out[key]={'support':len(y),'laya_correct':sum(v==p for v,p in zip(y,a)),'laya_to_full_oracle_correct':sum(t in (x,zv) for t,x,zv in zip(y,a,z)),
            'three_gear_oracle_correct':sum(t in (x,gx,zv) for t,x,gx,zv in zip(y,a,g,z)),'laya_to_full_transition':tr,'laya_to_constrained_transition':tr2,'constrained_to_full_transition':transition(y,g,z)}
    return {'per_predicate':out,'total':{k:sum(v[k] for v in out.values()) for k in ['support','laya_correct','laya_to_full_oracle_correct','three_gear_oracle_correct']},'deployable':False,'scope':'Labelled semantic assertions only; per-assertion perfect router, not a notice-level executable architecture'}

def preferences(cases,left,right):
    out={};a={r['id']:r['result']['predicates'] for r in left};b={r['id']:r['result']['predicates'] for r in right}
    for k in PREDICATES:
        tr=[]
        for c in cases:
            x=a[c['id']][k]['value'];z=b[c['id']].get(k,{}).get('value','NOT_SUPPORTED');y=c['expected'].get(k)
            if y is not None and x not in ('UNKNOWN','UNCERTAIN') and z not in ('UNKNOWN','UNCERTAIN','NOT_SUPPORTED') and x!=z:tr.append((y,x,z))
        damage=sum(y==x and y!=z and (k in CRITICAL) for y,x,z in tr);win=sum(y==z for y,x,z in tr)
        out[k]={'prefer':'LATER','support':len(tr),'win_rate':win/len(tr) if tr else 0,'critical_damage':damage,'scope':'VALIDATION only; support>=10 and win>=.9 and critical_damage=0 required at runtime'}
    return out

def actual_transitions(cases,predictions):
    truth={c['id']:c['expected'] for c in cases};groups={s:[] for s in ['LAYA_TO_GEAR2_RAW','PRE_GEAR3_TO_FULL_RAW','LAYA_TO_FINAL_RECONCILED']}
    from semantic_pipeline.reconcile import llm_factors
    for row in predictions:
        r=row['result'];y=truth[row['id']]
        for k in PREDICATES:
            if k not in y:continue
            first=r['laya']['predicates'][k]['value']
            if k in r['escalation']['gear2_requested']:groups['LAYA_TO_GEAR2_RAW'].append((y[k],first,r['gear2']['predicates'][k]['value']))
            if k in r['escalation']['gear3_requested']:
                # Keep raw stage transition distinct from the reconciled decision.
                before=r['gear2']['predicates'][k]['value'] if r['gear2'] and k in r['gear2']['predicates'] else first
                groups['PRE_GEAR3_TO_FULL_RAW'].append((y[k],before,llm_factors(r['full_qwen']).get(k,{}).get('value','NOT_SUPPORTED')))
            groups['LAYA_TO_FINAL_RECONCILED'].append((y[k],first,r['predicates'][k]['value']))
    return {s:{'assertions':len(v),'transition':transition(*zip(*v)) if v else transition([],[],[])} for s,v in groups.items()}
