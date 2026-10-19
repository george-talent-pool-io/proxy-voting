"""Do not equate a larger generator with ground truth. Preserve every stage."""
from semantic_pipeline.schema import PREDICATES, NOT_SUPPORTED
from semantic_pipeline.models import factor

def llm_factors(llm):
    if not llm or not llm.get('valid'): return {}
    parsed=llm['parsed'];validation=llm['evidence_validation']['predicates']
    out={}
    for k in PREDICATES:
        evidence=[e for e in validation[k] if e['valid']]
        bad=any(not e['valid'] for e in validation[k])
        value=parsed[k]
        # An asserted restriction requires a supporting exact quote; invalid quotes quarantine its fact.
        if bad or (value=='YES' and not evidence): value='UNKNOWN'
        if k=='votability' and (bad or (value in ('VOTABLE','NOT_VOTABLE') and not evidence)): value='UNCERTAIN'
        out[k]=factor(value,'LOCAL_LLM',evidence=evidence,
            model_value=parsed[k], evidence_valid=not bad,
            evidence_missing_for_positive=parsed[k]=='YES' and not evidence)
    return out

def reconcile(structured, laya, llm, policy=None):
    policy=policy or {};left=laya.get('predicates',{}) if laya else {};right=llm_factors(llm)
    result={};conflicts=[];trace=[]
    for key in list(PREDICATES)+(['other_restriction'] if 'other_restriction' in left else []):
        a=left.get(key);b=right.get(key);s=structured.get(key)
        if s:
            result[key]=s
            for candidate in (a,b):
                if candidate and candidate['value'] not in (s['value'],'UNKNOWN','UNCERTAIN',NOT_SUPPORTED):
                    conflicts.append(f'{key}: authoritative structure {s["value"]} vs {candidate["source"]} {candidate["value"]}')
            trace.append({'predicate':key,'rule':'AUTHORITATIVE_STRUCTURE','outcome':s})
        elif a is None or a['value'] in ('UNKNOWN','UNCERTAIN',NOT_SUPPORTED):
            # UNKNOWN means abstention, not a contrary semantic claim.
            result[key]=b or a or factor(NOT_SUPPORTED,'UNAVAILABLE')
            trace.append({'predicate':key,'rule':'FILL_ABSTENTION' if b else 'PRESERVE_UNRESOLVED','outcome':result[key]})
        elif b is None:
            result[key]=a
            trace.append({'predicate':key,'rule':'SPECIALIST_ONLY','outcome':a})
        elif a['value']==b['value']:
            result[key]={**a,'evidence':a.get('evidence',[])+b.get('evidence',[]),'source':'LAYA_LLM_AGREEMENT'}
            trace.append({'predicate':key,'rule':'AGREEMENT','outcome':result[key]})
        else:
            learned=policy.get(key,{})
            # Preference must have validation evidence, not an arbitrary model hierarchy.
            preferred=learned.get('prefer')
            chosen=b if preferred=='LLM' else a if preferred=='LAYA' else None
            if chosen is not None and (preferred!='LLM' or chosen.get('evidence')):
                result[key]=chosen
                trace.append({'predicate':key,'rule':'VALIDATION_PREFERENCE','validation':learned,'laya':a,'llm':b,'outcome':chosen})
            else:
                result[key]=factor('UNCERTAIN' if key=='votability' else 'UNKNOWN','UNRESOLVED_DISAGREEMENT')
                conflicts.append(f'{key}: Laya {a["value"]} vs LLM {b["value"]}')
                trace.append({'predicate':key,'rule':'DISAGREEMENT_REVIEW','laya':a,'llm':b,'outcome':result[key]})
    if llm and llm.get('invoked') and not llm.get('valid'): conflicts.append('LLM runtime/schema failure; result unavailable')
    if llm and llm.get('valid') and llm['parsed']['ambiguities']: conflicts.extend('LLM ambiguity: '+x for x in llm['parsed']['ambiguities'])
    return {'predicates':result,'conflicts':conflicts,'trace':trace}
