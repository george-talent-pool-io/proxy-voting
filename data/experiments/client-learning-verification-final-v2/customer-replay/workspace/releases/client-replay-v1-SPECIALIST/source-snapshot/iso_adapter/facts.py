"""Business projection of Prowide's typed components, not another FIN parser."""
from datetime import datetime,timezone,timedelta

VERSION='prowide-fact-projection-v1'

def project(parsed):
    out=[]
    for index,field in enumerate(parsed.get('fields',[])):
        c=field.get('components',[]);tag=field['tag'];q=field.get('qualifier');name=None;value=None
        if tag=='20C' and len(c)>=2:name=q.lower() if q else None;value=c[1]
        elif tag=='23G' and c:name='function';value=c[0]
        elif tag=='22F' and q in ('CAEV','CAOP','CAMV') and len(c)>=3 and c[1] is None:name=q.lower();value=c[2]
        elif tag=='13A' and q=='CAON' and len(c)>=2:name='option_number';value=c[1]
        elif tag=='35B' and len(c)>=2 and c[0]=='ISIN':name='security';value={'isin':c[1],'description':'\n'.join(x for x in c[2:] if x)}
        elif tag in ('98A','98C','98E') and c:
            try:
                dt=datetime.strptime(c[1],'%Y%m%d')
                if tag!='98A':dt=datetime.strptime(c[1]+c[2],'%Y%m%d%H%M%S')
                if tag=='98E':
                    if len(c)>3 and c[3]:dt=dt.replace(microsecond=int(c[3].ljust(3,'0')))
                    if len(c)>5 and c[5]:
                        offset=c[5];hours=int(offset[:2]);minutes=int(offset[2:] or 0)
                        if hours>23 or minutes>59:raise ValueError('Invalid UTC offset')
                        dt=dt.replace(tzinfo=timezone(timedelta(hours=hours,minutes=minutes)*(-1 if c[4]=='N' else 1)))
                name=q.lower() if q else None;value={'iso':dt.date().isoformat() if tag=='98A' else dt.isoformat(),'offset_known':dt.tzinfo is not None,'precision':'DATE' if tag=='98A' else 'SECOND'}
            except (ValueError,IndexError,TypeError):
                out.append({'name':'unresolved_date','value':None,'warning':'Typed components contain an invalid or unsupported date; no date invented','source':'PROWIDE','field':field});continue
        if name and value is not None:
            out.append({'name':name,'value':value,'source':'PROWIDE','field_id':f'prowide:{index}','tag':tag,'qualifier':q,'sequence_path':field.get('sequence_instance_path',field['sequence_path']),
                'start':field.get('start'),'end':field.get('end'),'field':field})
    return out

def deadline(parsed,reference):
    ref=datetime.fromisoformat(reference.replace('Z','+00:00'))
    if ref.tzinfo is None:raise ValueError('Evaluation time must have a timezone')
    facts=project(parsed);comparisons=[]
    for fact in facts:
        if fact['name']!='rddt':continue
        d=fact['value'];state='UNKNOWN'
        if d['offset_known']:state='PASSED' if datetime.fromisoformat(d['iso'])<ref else 'OPEN'
        comparisons.append({'source':'PROWIDE','field_id':fact['field_id'],'path':fact['sequence_path'],'deadline':d,'status':state,'field':fact['field']})
    states={f['status'] for f in comparisons}
    return {'status':next(iter(states)) if len(states)==1 else 'UNKNOWN','comparisons':comparisons,'conflict':len(states)>1,
        'source':'PROWIDE_COMPONENTS_DETERMINISTIC_COMPARISON','reason':'Only RDDT is controlling. Bare local/date-only values require an agreed timezone profile; no UTC assumption.'}

def semantic_facts(parsed):
    from semantic_pipeline.models import factor
    facts=project(parsed);out={'iso15022_fields':facts}
    # Preserve the existing conservative option rule; CAEV alone does not establish entitlement.
    options=[f for f in facts if f['name']=='caop' and f['value'] in {'ABST','AMGT','MNGT','PROX','CONN','CONY','CEXC','CTEN'} and any(p.startswith('CAOPTN[') for p in f['sequence_path'])]
    if options and parsed['message_type']=='MT564':
        ev=[{'valid':True,'text':f['field']['source_text'],'start':f['start'],'end':f['end'],'source':'PROWIDE','tag':f['tag'],'qualifier':f['qualifier']} for f in options if f['start'] is not None]
        out['votability']=factor('VOTABLE','PROWIDE_OPTION',evidence=ev)
    return out
