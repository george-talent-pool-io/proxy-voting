"""Lossless field-boundary state machine. NEVER standards validation."""
import re
VERSION='lenient-narrative-recovery-v1.1'
NARRATIVE_TAGS={'70E','70F'}
QUALIFIERS={'ADTX','REGI','INCO','COMP','PACO','WEBB','TAXE','DISC','TXNR','CETI','PTNI'}
def scan(text):
    if not isinstance(text,str):raise TypeError('Raw input must be a string')
    marks=[];offset=0
    for line in text.splitlines(keepends=True):
        m=re.match(r':(\d{2}[A-Z]?):',line)
        if m:marks.append((offset,m[1],offset+m.end()))
        offset+=len(line)
    fields=[];narratives=[];stack=[];instances=[];counts={};warnings=[]
    for i,(start,tag,value_start) in enumerate(marks):
        end=marks[i+1][0] if i+1<len(marks) else len(text)
        value=text[value_start:end];clean=value.strip()
        if clean.endswith('-}'):clean=clean[:-2].rstrip()
        if tag=='16R':
            key=(tuple(instances),clean);counts[key]=counts.get(key,0)+1
            stack.append(clean);instances.append(f'{clean}[{counts[key]}]')
        path=list(stack);q=re.match(r':([A-Z0-9]{4})//',value)
        field={'tag':tag,'value':value,'qualifier':q[1] if q else None,'sequence_path':path,'sequence_instance_path':list(instances),'start':start,'end':end,'raw':text[start:end],'source':'LENIENT_RECOVERY'}
        fields.append(field)
        if tag in NARRATIVE_TAGS and q and q[1] in QUALIFIERS:
            if tag=='70F' and q[1]=='PACO':warnings.append({'code':'NONSTANDARD_TAG_QUALIFIER_COMBINATION','tag':tag,'qualifier':q[1],'start':start,'note':'Public MT568 dictionary lists PACO for option E only; payload recovered without validation'})
            content_start=value_start+q.end();content_end=end
            if text[content_start:content_end].rstrip().endswith('-}'):
                content_end=text.rfind('-}',content_start,content_end)
            # Preserve the exact multiline payload, including its line endings.
            narratives.append({**field,'text':text[content_start:content_end],'text_start':content_start,'text_end':content_end})
        if tag=='16S':
            if stack and stack[-1]==clean:stack.pop();instances.pop()
            else:warnings.append({'code':'UNMATCHED_SEQUENCE_END','tag':tag,'value':clean,'start':start})
    if stack:warnings.append({'code':'UNCLOSED_SEQUENCES','sequence_path':list(stack)})
    return {'parser':'LENIENT_RECOVERY','adapter_version':VERSION,'parse_status':'RECOVERED_NOT_VALIDATED','raw_source':text,'fields':fields,'narratives':narratives,
        'unknown_fields':[f for f in fields if f['tag'] not in ('16R','16S') and not (f['tag'] in NARRATIVE_TAGS and f['qualifier'] in QUALIFIERS)], 'unknown_material':text,'warnings':warnings,'standards_validated':False}
