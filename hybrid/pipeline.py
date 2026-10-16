from hybrid.parser import parse,facts,deadline_status,MEETINGS
from hybrid.rules import decide,RESTRICTIONS
from hybrid.fallback import DisabledFallback
from classifier.deadlines import extract_deadline
VERSION='hybrid-pipeline-1'
LEGACY_MODE='LEGACY_WHOLE_TEXT_LAYA'

def analyse(raw,model=None,message_type=None,evaluation_time='2026-10-16T12:00:00+00:00'):
    p=parse(raw,message_type);structured={};reasons=[]
    events=facts(p,'caev')
    if events:
        codes={f['value'] for f in events}
        if len(codes)>1:reasons.append('Conflicting event codes')
        else:structured['meeting_event']='YES' if next(iter(codes)) in MEETINGS else 'NO'
    options=facts(p,'option_code')
    voting_codes={'ABST','AMGT','MNGT','PROX','CONN','CONY','CEXC','CTEN'}
    offered=[f for f in options if f['value'] in voting_codes and f['path'] and f['path'][-1].startswith('CAOPTN[')]
    if offered and p['message_type'] in {'MT564',None}:structured['votable']='YES'
    texts=facts(p,'narrative')
    # Narrative-only routing. Structured fields never become semantic states.
    narrative='\n\n'.join(f['value'] for f in texts) if texts else raw if p['kind']=='UNSTRUCTURED_NOTICE' else ''
    requested=[k for k in model.questions if k not in structured] if model and hasattr(model,'questions') else None
    semantic=model.analyse(narrative,requested_predicates=requested) if model and narrative else {'predicates':{},'llm_escalations':0,'reason':'Not executed' if narrative else 'No narrative'}
    # Map concatenated narrative evidence back to exact original field spans.
    for answer in semantic.get('predicates',{}).values():
        ev=answer.get('evidence')
        if not ev:continue
        if texts:
            cursor=0;found=False
            for f in texts:
                if cursor<=ev['start'] and ev['end']<=cursor+len(f['value']):
                    a=f['value_start']+ev['start']-cursor;b=a+len(ev['text'])
                    if raw[a:b]==ev['text']:ev.update(start=a,end=b,field_id=f['field_id']);found=True
                    break
                cursor+=len(f['value'])+2
            if not found:answer['evidence']=None
        elif raw[ev['start']:ev['end']]!=ev['text']:answer['evidence']=None
    preds=semantic.get('predicates',{})
    value=lambda k:preds.get(k,{}).get('value','UNKNOWN')
    vote=structured.get('votable',value('votable'));vote='UNCERTAIN' if vote=='UNKNOWN' else vote
    # A non-meeting event alone doesn't exclude a scheme/consent vote in narrative.
    # A meeting code alone doesn't establish beneficial-owner eligibility.
    deadline=deadline_status(p,evaluation_time)
    if not deadline['comparisons'] and p['kind']=='UNSTRUCTURED_NOTICE':
        deadline=extract_deadline(raw,evaluation_time)
    conflict=bool(reasons or p['errors'] or deadline.get('conflict') or any(a.get('conflict') for a in preds.values()))
    fs={'votable':vote,**{k:value(k) for k in RESTRICTIONS},'deadline_status':deadline['status'],'conflict':conflict}
    # A lone CANC cannot safely cancel an event without persistent linkage validation.
    functions=facts(p,'function')
    if any(f['value'] in {'CANC','REPL'} for f in functions):fs['quarantined']=True;reasons.append('Lifecycle message requires validated persistent event state')
    decision=decide(fs)
    return {'version':VERSION,'parsed':p,'structured_facts':structured,'semantic_analysis':semantic,'deadline':deadline,'decision_facts':fs,'decision':decision,'routing_trace':p['routing'],'review_reasons':reasons,'fallback':{'enabled':False,'external_calls':0},'narrative_text':narrative,'metrics':{'structured_values':sum(f['route']=='STRUCTURED_FACTS' and f['name']!='sequence' for f in p['facts']),'narrative_passages':len(texts) if texts else int(bool(narrative)),'laya_executed':bool(model and narrative),'llm_escalations':0,'manual_review':True}}
