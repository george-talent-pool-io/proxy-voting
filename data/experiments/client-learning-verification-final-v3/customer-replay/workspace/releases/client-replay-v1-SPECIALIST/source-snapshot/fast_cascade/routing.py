"""Per-predicate interpretable gates. Acceptance is experimental, never automation."""
from dataclasses import dataclass,asdict
from semantic_pipeline.schema import PREDICATES

CRITICAL={'votability','share_blocking','poa_required','registration_required'}
@dataclass(frozen=True)
class Policy:
    name:str='CONSERVATIVE'
    laya_score:float=.98
    laya_margin:float=.6
    critical_score:float=.995
    qwen_score:float=.98
    qwen_margin:float=.8
    allow_absence:bool=False
    gear2:bool=True
    def __post_init__(self):
        if any(not 0<=x<=1 for x in (self.laya_score,self.laya_margin,self.critical_score,self.qwen_score,self.qwen_margin)):raise ValueError('Invalid routing threshold')

def candidates():
    base=[Policy(),Policy('MODERATE',.9,.4,.98,.9,.6,True),Policy('AGGRESSIVE',.7,.2,.9,.8,.3,True)]
    return [Policy(**{**asdict(p),'name':p.name+('-THREE_GEAR' if g else '-TWO_GEAR'),'gear2':g}) for p in base for g in (True,False)]

def signal(text,key,p,language='en'):
    scores=p.get('raw_model_probability') or p.get('scores') or {};rank=sorted(scores.values(),reverse=True)
    state=p.get('value','NOT_SUPPORTED');evidence=[e for e in p.get('evidence',[]) if e.get('valid')]
    return {'predicate':key,'value':state,'top_score':rank[0] if rank else p.get('confidence'),'second_score':rank[1] if len(rank)>1 else None,
        'margin':rank[0]-rank[1] if len(rank)>1 else p.get('margin'),'entropy':p.get('entropy'),'evidence_available':bool(evidence),'evidence':evidence,
        'supporting_passage_count':p.get('supporting_passage_count',len(evidence)),'contradicting_passage_count':p.get('contradicting_passage_count',0),
        'contradiction':bool(p.get('conflict')),'unknown':state in ('UNKNOWN','UNCERTAIN','NOT_SUPPORTED'),'text_length':len(text),'language':language,
        'minimum_passage_no_score':p.get('minimum_passage_no_score'),'minimum_passage_no_margin':p.get('minimum_passage_no_margin'),
        'truncated':bool(p.get('truncated')),'calibrated_confidence':None,'raw_scores_are_calibrated':False}

def assess(text,key,p,policy,*,gear=1,language='en'):
    f=signal(text,key,p,language);why=[]
    if f['unknown']:why.append('UNKNOWN')
    if f['contradiction'] or f['contradicting_passage_count']:why.append('PASSAGE_CONFLICT')
    if f['truncated']:why.append('TRUNCATION')
    if language!='en':why.append('UNVALIDATED_LANGUAGE')
    if '\ufffd' in text or '\x00' in text:why.append('CORRUPT_SOURCE')
    limit=max(policy.laya_score,policy.critical_score) if gear==1 and key in CRITICAL else policy.laya_score if gear==1 else policy.qwen_score
    margin=policy.laya_margin if gear==1 else policy.qwen_margin
    score=f['top_score'];gap=f['margin']
    if gear==1 and p.get('aggregation_reason')=='DOCUMENT_ABSENCE_NOT_EXPLICIT_NEGATION':
        score=f['minimum_passage_no_score'];gap=f['minimum_passage_no_margin']
    if score is None or score<limit:why.append('LOW_RAW_SCORE')
    if gap is None or gap<margin:why.append('LOW_MARGIN')
    if not f['evidence_available']:
        if f['value'] in ('YES','VOTABLE') or not policy.allow_absence:why.append('EVIDENCE_UNAVAILABLE')
        elif gear==1 and p.get('aggregation_reason') not in ('DOCUMENT_ABSENCE_NOT_EXPLICIT_NEGATION',None):why.append('UNSUPPORTED_NEGATIVE')
    return {'accepted_for_research':not why,'reasons':why,'signals':f,'score_basis':'RAW_NATIVE_SIGNALS; not calibrated confidence','policy':asdict(policy)}

def reconcile(left,right,key,*,right_accepted=False,preferences=None):
    """A known disagreement is not resolved just because one model is larger."""
    if not right:return left,[],{'rule':'PRESERVE_PREVIOUS','predicate':key}
    a=left.get('value','NOT_SUPPORTED');b=right.get('value','NOT_SUPPORTED')
    if b in ('UNKNOWN','UNCERTAIN','NOT_SUPPORTED'):return left,[],{'rule':'LATER_ABSTENTION','predicate':key}
    if a in ('UNKNOWN','UNCERTAIN','NOT_SUPPORTED'):
        return (right if right_accepted else left),[],{'rule':'SUPPORTED_FILL_ABSTENTION' if right_accepted else 'LATER_NOT_TRUSTED','predicate':key}
    if a==b:return (right if right_accepted else left),[],{'rule':'AGREEMENT','predicate':key}
    # Absence is weak evidence, but it is still a contrary label. Any preference
    # requires separately persisted validation support and no new critical misses.
    pref=(preferences or {}).get(key,{})
    if right_accepted and pref.get('prefer')=='LATER' and pref.get('support',0)>=10 and pref.get('win_rate',0)>=.9 and pref.get('critical_damage',1)==0:
        return right,[],{'rule':'VALIDATION_SUPPORTED_PREFERENCE','predicate':key,'validation':pref}
    return {**left,'value':'UNCERTAIN' if key=='votability' else 'UNKNOWN','source':'UNRESOLVED_MODEL_DISAGREEMENT','conflict':True},[key+':MODEL_DISAGREEMENT'],{'rule':'DISAGREEMENT_REVIEW','predicate':key,'earlier_value':a,'later_value':b}
