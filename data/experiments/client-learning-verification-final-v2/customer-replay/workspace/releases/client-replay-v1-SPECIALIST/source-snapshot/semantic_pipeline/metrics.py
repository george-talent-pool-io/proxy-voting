"""Assertion denominators are explicit; missing capabilities count as failures."""
from collections import Counter
from statistics import median
from sklearn.metrics import accuracy_score, f1_score, confusion_matrix
from semantic_pipeline.schema import RESTRICTIONS, PREDICATES, NOT_SUPPORTED

def observed(result):
    preds=result['reconciliation']['predicates']
    out={k:preds.get(k,{}).get('value',NOT_SUPPORTED) for k in PREDICATES}
    # Historical broad other is evaluated only as a broad union, not residual other.
    if 'other_restriction' in preds:
        out['other_restriction']=preds['other_restriction']['value']
    else:
        vals=[out[k] for k in RESTRICTIONS if k not in ('share_blocking','poa_required')]
        out['other_restriction']='YES' if 'YES' in vals else 'NO' if all(v=='NO' for v in vals) else 'UNKNOWN'
    out['deadline_status']=result['deadline']['status']
    out['classification']=result['decision']['classification']
    # Common collapsed customer status does not discard raw native 7-bucket status.
    if out['classification'] in ('POA_REQUIRED','SHARE_BLOCKING'):out['classification']='VOTABLE_WITH_RESTRICTION'
    return out

def truth(expected):
    result={}
    for key,value in expected.items():
        if key=='votable': key='votability';value={'YES':'VOTABLE','NO':'NOT_VOTABLE','UNCERTAIN':'UNCERTAIN'}[value]
        if isinstance(value,bool): value='YES' if value else 'NO'
        if value is None:value='UNKNOWN'
        if key=='classification' and value in ('POA_REQUIRED','SHARE_BLOCKING'): value='VOTABLE_WITH_RESTRICTION'
        result[key]=value
    return result

def field_metrics(y,p,positive='YES'):
    labels=sorted(set(y+p));support=Counter(y);n=len(y)
    cm=confusion_matrix(y,p,labels=labels).tolist()
    # Support-bearing classes only for balanced accuracy; unsupported guesses remain errors.
    recalls={k:sum(a==b==k for a,b in zip(y,p))/v for k,v in support.items()}
    yes=sum(a==positive for a in y);no=sum(a==('NOT_VOTABLE' if positive=='VOTABLE' else 'NO') for a in y)
    tp=sum(a==b==positive for a,b in zip(y,p));pp=sum(b==positive for b in p)
    neg='NOT_VOTABLE' if positive=='VOTABLE' else 'NO'
    return {'n':n,'correct':sum(a==b for a,b in zip(y,p)),'accuracy':float(accuracy_score(y,p)) if n else None,
        'macro_f1':float(f1_score(y,p,labels=sorted(support),average='macro',zero_division=0)) if n else None,
        'f1_by_class':{k:float(f1_score(y,p,labels=[k],average='macro',zero_division=0)) for k in support},
        'balanced_accuracy':sum(recalls.values())/len(recalls) if recalls else None,
        'positive_label':positive,'positive_support':yes,'negative_support':no,
        'positive_precision':tp/pp if pp else None,'positive_recall':tp/yes if yes else None,
        'negative_recall_specificity':sum(a==b==neg for a,b in zip(y,p))/no if no else None,
        'positive_f1':float(f1_score(y,p,labels=[positive],average='macro',zero_division=0)) if yes else None,
        'support':dict(support),'predicted_support':dict(Counter(p)),'labels':labels,'confusion_matrix':cm,
        'not_supported':p.count(NOT_SUPPORTED)}

def summarize(rows):
    fields={};errors=[];passes=0;total_assertions=0;correct_assertions=0
    for r in rows:
        expected=truth(r['expected']);predicted=observed(r['result']);checks={k:predicted.get(k,NOT_SUPPORTED)==v for k,v in expected.items()}
        passes+=all(checks.values());total_assertions+=len(checks);correct_assertions+=sum(checks.values())
        for key,ok in checks.items():
            if not ok:
                a=r['result']['reconciliation']['predicates'].get(key,{})
                errors.append({'id':r['id'],'text':r['text'],'field':key,'expected':expected[key],
                    'predicted':predicted.get(key,NOT_SUPPORTED),'scores':a.get('scores',{}),
                    'confidence':a.get('confidence'),'margin':a.get('margin'),
                    'source':a.get('source'),'escalation':r['result']['escalation'],
                    'conflicts':r['result']['reconciliation']['conflicts'],'record_id':r['id']})
        for k,v in expected.items():fields.setdefault(k,([],[]));fields[k][0].append(v);fields[k][1].append(predicted.get(k,NOT_SUPPORTED))
    metrics={k:field_metrics(y,p,'VOTABLE' if k=='votability' else 'YES') for k,(y,p) in fields.items()}
    times=sorted(r['result']['latencies']['total_ms'] for r in rows)
    status_n=sum('classification' in r['expected'] for r in rows)
    return {'cases':len(rows),'cases_satisfying_all_supplied_assertions':passes,
        'assertions':total_assertions,'correct_assertions':correct_assertions,
        'assertion_accuracy':correct_assertions/total_assertions if total_assertions else None,
        'case_exact_match_scope':'All supplied assertions only; not all fields unless dataset is completely labelled',
        'fields':metrics,'final_status_labelled_cases':status_n,
        'customer_status_accuracy':metrics.get('classification',{}).get('accuracy'),
        'manual_review_count':sum(r['result']['decision']['manual_review_required'] for r in rows),
        'uncertain_final_status_count':sum(r['result']['decision']['classification']=='UNCERTAIN_MANUAL_REVIEW' for r in rows),
        'llm_invocations':sum(bool((r['result'].get('llm') or {}).get('invoked')) for r in rows),
        'llm_invalid_outputs':sum(bool(r['result'].get('llm')) and not r['result']['llm'].get('valid') for r in rows),
        'high_confidence_wrong_assertions':sum(e['confidence'] is not None and e['confidence']>=.98 for e in errors),
        'median_latency_ms':median(times) if times else None,'p95_latency_ms':times[min(len(times)-1,int(.95*len(times)))] if times else None,
        'failures':errors,'scope':'Synthetic/authored research only. No customer accuracy or automation claim.'}

def transitions(rows):
    matrix=Counter();predicates=Counter();oracle={'assertions':0,'baseline_correct':0,'oracle_correct':0,'oracle_llm_calls':0}
    for r in rows:
        result=r['result'];laya=result.get('laya')
        if not laya:continue
        before={**result,'reconciliation':{'predicates':laya['predicates']}}
        a=observed(before);b=observed(result);expected=truth(r['expected']);wrong=False
        for key,v in expected.items():
            if key in ('classification','deadline_status'):continue  # transition matrix semantic assertions only
            left=a.get(key,NOT_SUPPORTED)==v;right=b.get(key,NOT_SUPPORTED)==v
            if result.get('llm') and result['llm'].get('invoked'):
                matrix[('correct' if left else 'wrong')+' → '+('correct' if right else 'wrong')]+=1
            oracle['assertions']+=1;oracle['baseline_correct']+=left;wrong|=not left
        oracle['oracle_llm_calls']+=wrong
    return {'scope':'Assertion-level, only invoked cases; final reconciled result vs pre-fallback specialist',
        'transition_matrix':dict(matrix),'oracle':oracle}
