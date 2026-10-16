"""Interpretable experimental routing. Gate acceptance never enables automation."""
from dataclasses import dataclass,asdict
from semantic_pipeline.schema import PREDICATES
@dataclass(frozen=True)
class Policy:
    name:str='MODERATE'
    min_score:float=.9
    min_margin:float=.4
    require_positive_evidence:bool=True
    escalate_critical_positive:bool=False
    escalate_unknown:bool=True
    max_chars:int=12000
    def __post_init__(self):
        if self.name not in ('ALWAYS','CONSERVATIVE','MODERATE','AGGRESSIVE'):raise ValueError('Unknown routing policy')
        if not 0<=self.min_score<=1 or not 0<=self.min_margin<=1:raise ValueError('Invalid routing threshold')

def features(text,laya):
    out=[]
    for key in PREDICATES:
        p=laya['predicates'].get(key,{})
        out.append({'predicate':key,'laya_result':p.get('value','NOT_SUPPORTED'),'top_score':p.get('confidence'),'margin':p.get('margin'),
            'supporting_passage_count':p.get('supporting_passage_count',len(p.get('evidence',[]))),
            'contradicting_passage_count':p.get('contradicting_passage_count',int(bool(p.get('conflict')))),
            'evidence_available':any(e.get('valid') for e in p.get('evidence',[])),'conflict':bool(p.get('conflict')),
            'historical_passages':sum(s.get('historical',False) and s.get('relevant',False) for s in p.get('passage_states',[])),
            'conditional_passages':sum(s.get('conditional',False) and s.get('relevant',False) for s in p.get('passage_states',[])),
            'text_length':len(text)})
    return out

def gate(text,laya,structured,policy):
    reasons=[];fs=features(text,laya)
    if policy.name=='ALWAYS':reasons.append('ALWAYS_ESCALATE_CONTROL')
    for f in fs:
        key=f['predicate'];value=f['laya_result']
        if value=='NOT_SUPPORTED':reasons.append(key+':NOT_SUPPORTED')
        if policy.escalate_unknown and value in ('UNKNOWN','UNCERTAIN'):reasons.append(key+':UNKNOWN')
        if f['conflict'] or f['contradicting_passage_count']:reasons.append(key+':PASSAGE_CONFLICT')
        if f['top_score'] is not None and f['top_score']<policy.min_score:reasons.append(key+':LOW_SCORE')
        if f['margin'] is not None and f['margin']<policy.min_margin:reasons.append(key+':LOW_MARGIN')
        if policy.require_positive_evidence and value in ('YES','VOTABLE') and not f['evidence_available']:reasons.append(key+':POSITIVE_EVIDENCE_MISSING')
        if policy.escalate_critical_positive and key in ('votability','share_blocking','poa_required') and value in ('YES','VOTABLE'):reasons.append(key+':CRITICAL_POSITIVE')
        if f['conditional_passages'] and value in ('UNKNOWN','UNCERTAIN'):reasons.append(key+':UNRESOLVED_CONDITION')
        if key in structured and value not in ('UNKNOWN','UNCERTAIN',structured[key]['value']):reasons.append(key+':STRUCTURE_CONFLICT')
    if laya.get('truncated'):reasons.append('TRUNCATED_SPECIALIST_INPUT')
    if len(text)>policy.max_chars:reasons.append('LONG_INPUT')
    return {'escalated':bool(reasons),'reasons':reasons,'configuration':asdict(policy),'features':fs,'version':'selective-routing-v1'}
