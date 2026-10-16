"""Lossless ISO15022 subset reader, not a FIN/network conformance validator.

Offsets are Python/Unicode codepoints into unchanged input. Unknown fields and
non-field material remain in raw and segments. Profiles: public ISO dictionary,
retrieved 2026-10-16; unsupported alternatives are preserved, never guessed.
"""
import hashlib
import re
from collections import Counter
from datetime import datetime, timezone, timedelta

VERSION = 'iso-subset-1'
SUPPORTED = {'564', '565', '567', '568'}
MEETINGS = {'MEET','OMET','XMET','BMET','CMET'}
TAG = re.compile(r'(?m)^:([0-9]{2}[A-Z]?):')
QUAL = re.compile(r'^:([A-Z0-9]{4})/([^/\r\n]*)/(.*)', re.S)
DATE_QUALIFIERS = {'MEET','RDDT','MKDT','EARD','RDTE','REGI','BLOK','PREP','DOCD','BORD'}
NARRATIVE_QUALIFIERS = {'ADTX','REGI','INCO','COMP','PACO','TAXE','DISC','BAIN','CETI','PTNI','TXNR','INST','REAS'}


def date_value(tag, value):
    """Decode only A,C,E. Bare date/time has no silently assumed timezone."""
    try:
        if tag == '98A' and re.fullmatch(r'\d{8}', value):
            return {'iso': datetime.strptime(value,'%Y%m%d').date().isoformat(), 'precision':'DATE','offset_known':False}
        if tag == '98C' and re.fullmatch(r'\d{14}', value):
            return {'iso':datetime.strptime(value,'%Y%m%d%H%M%S').isoformat(),'precision':'SECOND','offset_known':False}
        m = re.fullmatch(r'(\d{14})(?:,(\d{1,3}))?(?:/(N?)(\d{2})(\d{2})?)?',value) if tag == '98E' else None
        if m:
            dt=datetime.strptime(m[1],'%Y%m%d%H%M%S')
            if m[2]:dt=dt.replace(microsecond=int(m[2].ljust(3,'0'))*1000)
            if m[4]:
                hours,minutes=int(m[4]),int(m[5] or 0)
                if hours>23 or minutes>59:return None
                delta=timedelta(hours=hours,minutes=minutes)*( -1 if m[3] else 1)
                dt=dt.replace(tzinfo=timezone(delta))
            return {'iso':dt.isoformat(),'precision':'MILLISECOND' if m[2] else 'SECOND','offset_known':bool(m[4])}
    except (ValueError,OverflowError):
        pass
    return None


def parse(raw, message_type=None):
    if not isinstance(raw,str):
        return {'version':VERSION,'raw':raw if raw is None or isinstance(raw,(bool,int,float)) else repr(raw),'source_hash':None,'message_type':None,'kind':'UNRECOGNISED','fields':[],'segments':[],'errors':['Input must be a string'],'facts':[],'routing':[]}
    digest=hashlib.sha256(raw.encode('utf-8',errors='surrogatepass')).hexdigest()
    header=re.search(r'\{2:[IO](\d{3})',raw)
    mt=header[1] if header else (str(message_type).removeprefix('MT') if message_type else None)
    result={'version':VERSION,'raw':raw,'source_hash':digest,'message_type':f'MT{mt}' if mt else None,'kind':'UNRECOGNISED','fields':[],'segments':[],'errors':[],'facts':[],'routing':[]}
    # FIN block 4 is delimited separately so trailer cannot contaminate last field.
    block=re.search(r'\{4:(?:\r\n|\r|\n)?',raw)
    start=block.end() if block else 0
    end=raw.find('-}',start) if block else len(raw)
    if end<0:end=len(raw);result['errors'].append('Unterminated FIN text block')
    body=raw[start:end]
    # Support CRLF, LF and CR without changing source offsets.
    matches=list(re.finditer(r'(?:\A|(?<=[\r\n])):([0-9]{2}[A-Z]?):',body))
    stack=[];counts=Counter();cursor=0
    for i,m in enumerate(matches):
        if m.start()>cursor:result['segments'].append({'kind':'UNKNOWN_MATERIAL','start':start+cursor,'end':start+m.start()})
        stop=matches[i+1].start() if i+1<len(matches) else len(body)
        value_end=stop
        while value_end>m.end() and body[value_end-1] in '\r\n':value_end-=1
        tag=m[1];value=body[m.end():value_end];q=QUAL.fullmatch(value)
        qualifier,dss,decoded=(q[1],q[2],q[3]) if q else (None,None,value)
        field={'id':f'{digest[:16]}:{i}','tag':tag,'qualifier':qualifier,'data_source_scheme':dss,'value':decoded,'raw_value':value,'start':start+m.start(),'end':start+value_end,'value_start':start+m.end()+(q.start(3) if q else 0),'path':list(stack),'occurrence':i}
        if tag=='16R':
            name=value.strip();parent=tuple(stack);counts[(parent,name)]+=1
            stack.append(f'{name}[{counts[(parent,name)]}]');field['path']=list(stack)
            if not re.fullmatch('[A-Z0-9]{1,16}',name):result['errors'].append(f'Invalid sequence name at {i}')
        elif tag=='16S':
            if not stack or stack[-1].split('[')[0]!=value.strip():result['errors'].append(f'Unmatched sequence end at {i}')
            else:stack.pop()
        result['fields'].append(field)
        result['segments'].append({'kind':'FIELD','field_id':field['id'],'start':start+m.start(),'end':start+stop})
        cursor=stop
    if not matches and body:result['segments'].append({'kind':'UNKNOWN_MATERIAL','start':start,'end':end})
    if stack:result['errors'].append('Unclosed sequences: '+','.join(stack))
    for f in result['fields']:
        route='UNKNOWN_FIELDS';name=None;value=None;seq=[p.split('[')[0] for p in f['path']];tag=f['tag'];q=f['qualifier'];v=f['value']
        if tag in {'16R','16S'}:route='STRUCTURED_FACTS';name='sequence';value=v
        elif tag=='23G' and seq==['GENL']:route='STRUCTURED_FACTS';name='function';value=v.split('/')[0]
        elif tag=='20C' and q in {'SEME','CORP','COAF','PREV','RELA'} and seq and seq[0]=='GENL':
            if re.fullmatch('[^\r\n]{1,16}',v) and not f['data_source_scheme']:route='STRUCTURED_FACTS';name=q.lower();value=v
        elif tag=='22F' and q in {'CAEV','CAMV'} and seq==['GENL'] and not f['data_source_scheme']:
            if re.fullmatch('[A-Z0-9]{4}',v):route='STRUCTURED_FACTS';name=q.lower();value=v
        elif tag=='35B' and seq and seq[-1]=='USECU':
            m=re.match(r'ISIN ([A-Z]{2}[A-Z0-9]{9}\d)(?:\r?\n|\r|$)',v)
            if m:
                route='STRUCTURED_FACTS';name='security';value={'isin':m[1],'description':v[m.end():]}
        elif tag in {'98A','98C','98E'} and q in DATE_QUALIFIERS and not f['data_source_scheme'] and seq and seq[-1] in {'GENL','CADETL','CAOPTN'}:
            value=date_value(tag,v)
            if value is not None:route='STRUCTURED_FACTS';name=q.lower()
            else:result['errors'].append(f'Invalid {tag} {q} at {f["occurrence"]}')
        elif tag=='98B' and q in DATE_QUALIFIERS:
            route='SEMISTRUCTURED_FACTS';name='coded_date';value={'qualifier':q,'code':v,'scheme':f['data_source_scheme']}
        elif tag=='22F' and q in {'CETI','OSTA','OPTF'} and seq and seq[-1]=='CAOPTN' and not f['data_source_scheme']:
            if re.fullmatch('[A-Z0-9]{4}',v):route='STRUCTURED_FACTS';name=q.lower();value=v
        elif tag=='13A' and q=='CAON' and seq and seq[-1] in {'CAOPTN','CAINST','CADETL'} and not f['data_source_scheme']:
            if re.fullmatch('[A-Z0-9]{3}',v):route='STRUCTURED_FACTS';name='option_number';value=v
        elif tag=='22F' and q=='CAOP' and seq and seq[-1] in {'CAOPTN','CAINST','CADETL'} and not f['data_source_scheme']:
            if re.fullmatch('[A-Z0-9]{4}',v):route='STRUCTURED_FACTS';name='option_code';value=v
        elif tag in {'70E','70F','70G','70D'} and q in NARRATIVE_QUALIFIERS:
            route='NARRATIVE_TEXT';name='narrative';value=v
        elif tag=='25D' and q in {'IPRC','CPRC','EPRC','PROC'}:
            route='SEMISTRUCTURED_FACTS';name='processing_status';value={'qualifier':q,'value':v}
        trace={'field_id':f['id'],'tag':tag,'qualifier':q,'path':f['path'],'route':route,'consumer':'Laya predicates' if route=='NARRATIVE_TEXT' else 'deterministic rules' if route=='STRUCTURED_FACTS' else 'preserve/review','start':f['start'],'end':f['end']}
        result['routing'].append(trace)
        if name:result['facts'].append({'name':name,'value':value,'field_id':f['id'],'path':f['path'],'start':f['start'],'end':f['end'],'value_start':f['value_start'],'route':route})
    n=len(matches)
    if n:
        result['kind']='PARTIAL_ISO15022' if any(f['tag']=='16R' for f in result['fields']) and n>=3 else 'ISO15022_LIKE'
        # VALID means subset structural validity, explicitly NOT complete network validation.
        names={f['name'] for f in result['facts']}
        required={'seme','function','caev'}
        if mt in SUPPORTED and block and not result['errors'] and required<=names and any(f['tag']=='16R' and f['value']=='GENL' for f in result['fields']):
            result['subset_structure_valid']=True
            # Full mandatory-field/network rules are not implemented: keep PARTIAL.
            result['kind']='PARTIAL_ISO15022'
    elif len(raw.strip())>=20 and sum(c.isalpha() for c in raw)>=10:result['kind']='UNSTRUCTURED_NOTICE'
    return result


def facts(parsed,name):return [f for f in parsed['facts'] if f['name']==name]


def deadline_status(parsed,evaluation_time):
    """RDDT only. Option deadlines retained; conflicting scopes abstain. No UTC guess."""
    ref=datetime.fromisoformat(evaluation_time.replace('Z','+00:00'))
    if ref.tzinfo is None:raise ValueError('Evaluation time must include timezone')
    deadlines=facts(parsed,'rddt')
    comparisons=[]
    for f in deadlines:
        d=f['value'];status='UNKNOWN'
        if d['offset_known']:
            status='PASSED' if datetime.fromisoformat(d['iso'])<ref else 'OPEN'
        comparisons.append({'field_id':f['field_id'],'path':f['path'],'deadline':d,'evaluation_time':ref.isoformat(),'status':status})
    states={c['status'] for c in comparisons}
    return {'status':next(iter(states)) if len(states)==1 else 'UNKNOWN','comparisons':comparisons,'conflict':len(states)>1,'reason':'Date-only and local times require an agreed sender/timezone profile; MKDT/EARD/MEET/RDTE are not substituted for RDDT.'}
