"""Evidence-aware reduction of native Laya passage decisions, without retraining.
A NO caused by absence of mention is not a contradictory negative statement.
Lexical cues scope model evidence; they do not turn a model NO into a semantic YES.
"""
import re
from dataclasses import dataclass,asdict
from hybrid.semantics import passages
VERSION='evidence-aggregation-v2'
ANCHORS={
 'share_blocking':r'block(?:ed|ing)?|immobili[sz]|cannot be (?:sold|transferred)|freeze|frozen|bloqu|gesperr',
 'poa_required':r'power.of.attorney|\bpoa\b|notari[sz]ed (?:mandate|authority)|procuration|vollmacht',
 'registration_required':r'regist(?:er|ration)|enrol|inscri',
 'beneficial_owner_disclosure_required':r'disclos|identity|identification|titulaire|beneficial.owner.{0,30}(?:details|name|identifier)',
 'holding_confirmation_required':r'holding|ownership|custody certificate|proof|confirmation',
 'split_voting_restricted':r'split|divid(?:e|ing).*votes|differ(?:ent|ently).*vot',
 'securities_lending_recall_required':r'lend|loan|recall|borrow|pr[eê]t',
 'other_voting_restriction':r'restrict|eligib|limit|exclud|prohibit|condition|mandatory|require',
}
NEGATIVE=re.compile(r'\b(?:not|no|never|without|neither|waiv\w*|removed|withdrawn|abolished|unnecessary|unrestricted|exempt\w*|aucun\w*|pas|nicht|kein\w*)\b',re.I)
HISTORY=re.compile(r'\b(?:historically|historical|previously|formerly|last year|prior year|preliminary notice (?:stated|said)|earlier (?:notice|terms) (?:stated|said|required)|used to)\b',re.I)
SUPERSEDE=re.compile(r'\b(?:final|amended|revised|replacement|supersed\w*|withdrawn|removed|waived|no longer|abolished|instead|updated terms)\b',re.I)
ROUTES={'PHYSICAL_ATTENDANCE':re.compile(r'physical attendance|in.person attendance|attend(?:ing)? (?:in person|physically)',re.I),
 'ELECTRONIC_PROXY':re.compile(r'electronic proxy|electronic voting|remote proxy|online proxy|online voting',re.I)}
STRATEGIES=('MAX_POSITIVE','MAX_MARGIN','ANY_STRONG_POSITIVE','WEIGHTED_PASSAGE','LAST_RELEVANT_STATEMENT','SUPERSESSION_AWARE')
@dataclass(frozen=True)
class AggregationConfig:
    strategy:str='SUPERSESSION_AWARE'
    min_score:float=.70
    min_margin:float=.20
    voting_route:str|None=None
    def __post_init__(self):
        if self.strategy not in STRATEGIES:raise ValueError('Unknown aggregation strategy')
        if not 0<=self.min_score<=1 or not 0<=self.min_margin<=1:raise ValueError('Invalid aggregation threshold')
        if self.voting_route is not None and self.voting_route not in ROUTES:raise ValueError('Unknown voting route')

def states(text,predicate,native):
    spans=list(passages(text))
    if len(native)!=len(spans):raise ValueError('Native passage/source count mismatch')
    anchor=re.compile(ANCHORS[predicate],re.I);out=[]
    for i,(span,pred) in enumerate(zip(spans,native)):
        words=span['text'];context=text[max(0,span['start']-180):span['end']]
        relevant=bool(anchor.search(words));clauses=re.split(r';|\bbut\b|\bhowever\b|\bwhereas\b',words,flags=re.I)
        negative=any(anchor.search(c) and NEGATIVE.search(c) for c in clauses);historical=bool(HISTORY.search(words))
        background=bool(re.search(r'general market guide|industry guidance|background example|for reference only|general market practice',words,re.I))
        route=next((k for k,r in ROUTES.items() if r.search(words)),None)
        # A bare NO on unrelated prose means absence. A relevant but implicit NO
        # remains uncertain rather than being treated as an explicit negation.
        state='AFFIRMATIVE' if relevant and pred['value']=='YES' else 'NEGATIVE' if relevant and negative and pred['value']=='NO' else 'UNKNOWN'
        reason='SUPPORTED_NATIVE_STATEMENT' if state!='UNKNOWN' else 'ABSENCE_OR_UNRESOLVED_MODEL_INTERPRETATION'
        out.append({'index':i,'predicate':predicate,'state':state,'native_value':pred['value'],'scores':pred['scores'],
            'score':pred['confidence'],'margin':pred.get('margin'),'start':span['start'],'end':span['end'],'text':words,
            'relevant':relevant,'historical':historical,'background':background,'supersession':bool(SUPERSEDE.search(context)),
            'route':route,'conditional':bool(re.search(r'\b(?:only if|may be required|might be|depending on)\b',words,re.I)),
            'explicit_negative_cue':negative,'truncated':pred.get('truncated',False),'reason':reason})
    return out

def reduce_states(items,config=AggregationConfig()):
    active=[p for p in items if p['state']!='UNKNOWN' and not p['truncated'] and p['score']>=config.min_score and (p['margin'] or 0)>=config.min_margin]
    route_excluded=[]
    if config.voting_route:
        route_excluded=[p['index'] for p in active if p['route'] and p['route']!=config.voting_route]
        active=[p for p in active if p['index'] not in route_excluded]
    relevant=[p for p in active if not p['historical'] and not p['background']]
    affirmative=[p for p in relevant if p['state']=='AFFIRMATIVE'];negative=[p for p in relevant if p['state']=='NEGATIVE']
    winner=None;conflict=bool(affirmative and negative);reason='NO_STRONG_CURRENT_RELEVANT_STATEMENT'
    if config.strategy in ('MAX_POSITIVE','ANY_STRONG_POSITIVE'):
        pool=affirmative or negative;winner=max(pool,key=lambda p:p['score']) if pool else None
    elif config.strategy=='MAX_MARGIN':winner=max(relevant,key=lambda p:p['margin']) if relevant else None
    elif config.strategy=='WEIGHTED_PASSAGE':
        weights={s:sum(p['score']*(p['margin'] or 0) for p in relevant if p['state']==s) for s in ('AFFIRMATIVE','NEGATIVE')}
        if weights['AFFIRMATIVE']!=weights['NEGATIVE']:
            s=max(weights,key=weights.get);winner=max((p for p in relevant if p['state']==s),key=lambda p:p['score'])
    elif config.strategy=='LAST_RELEVANT_STATEMENT':winner=relevant[-1] if relevant else None
    else:
        if not relevant and items and all(p['native_value']=='NO' and not p['truncated'] for p in items) and not any(p['historical'] and p['relevant'] for p in items) and not any(p['relevant'] and not p['explicit_negative_cue'] and not p['background'] for p in items):
            # Closed-world document inference: no current requirement is stated.
            # Explicit evidence remains unavailable and routing may reject this fast path.
            winner=max(items,key=lambda p:p['score']);reason='DOCUMENT_ABSENCE_NOT_EXPLICIT_NEGATION'
        elif conflict:
            last=relevant[-1];prior=[p for p in relevant if p['index']<last['index']]
            same_scope=all(p['route']==last['route'] or not p['route'] or not last['route'] for p in prior)
            if last['supersession'] and same_scope:
                winner=last;conflict=False;reason='EXPLICIT_LATER_SUPERSESSION'
            else:reason='CURRENT_PASSAGE_CONFLICT_OR_DISTINCT_VOTING_ROUTES'
        elif relevant:
            winner=max(relevant,key=lambda p:p['score']);reason='STRONG_CURRENT_RELEVANT_EVIDENCE'
        if winner and winner['conditional'] and (not winner['route'] or not config.voting_route):
            winner=None;conflict=True;reason='CONDITION_OR_VOTING_ROUTE_UNRESOLVED'
    if winner:
        if reason=='NO_STRONG_CURRENT_RELEVANT_STATEMENT':reason='COMPARATOR_STRATEGY_'+config.strategy
        value={'AFFIRMATIVE':'YES','NEGATIVE':'NO'}.get(winner['state'],winner['native_value'])
    else:value='UNKNOWN'
    evidence=[]
    if winner and winner['state']!='UNKNOWN':evidence=[{'valid':True,'text':winner['text'],'start':winner['start'],'end':winner['end'],'source':'NATIVE_LAYA_PASSAGE_WITH_DETERMINISTIC_SCOPE'}]
    support=[p for p in relevant if p['native_value']==value];opposition=[p for p in relevant if p['native_value'] not in (value,'UNKNOWN')]
    return {'value':value,'scores':winner['scores'] if winner else {},'confidence':winner['score'] if winner else None,
        'margin':winner['margin'] if winner else None,'evidence':evidence,'conflict':conflict,'aggregation':config.strategy,
        'aggregation_version':VERSION,'aggregation_config':asdict(config),'aggregation_reason':reason,'passage_states':items,
        'supporting_passage_count':len(support),'contradicting_passage_count':len(opposition),'route_excluded_passages':route_excluded,
        'score_definition':'Native selected passage scores; not document or calibrated correctness probability'}

def aggregate(text,predicate,native,config=AggregationConfig()):return reduce_states(states(text,predicate,native),config)
