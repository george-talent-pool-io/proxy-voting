"""Ordinary notices bypass Java; damaged text retains its full semantic source."""
import re
from iso_adapter.prowide import Prowide
from iso_adapter.scanner import scan
_REFERENCE=Prowide()
def route(text,reference=None):
    hint=bool(re.search(r'(?:^|[\r\n]):\d{2}[A-Z]?:',text) or re.search(r'\{2:[IO]\d{3}',text))
    if not hint:return {'input_type':'UNSTRUCTURED_NOTICE' if text.strip() else 'UNRECOGNISED','parser':'NOT_APPLICABLE','raw_source':text,'narrative':text,'semantic_context':{},'warnings':[]}
    recovery=scan(text);warnings=[]
    # A FIN envelope embedded inside an ordinary notice is untrusted source text,
    # not permission to promote the embedded fields into authoritative facts.
    if re.match(r'\s*\{1:[^}]+\}\s*\{2:[IO]\d{3}',text):
        try:
            parsed=(reference or _REFERENCE).parse(text)
            if parsed['parse_status']!='FAILED' and not parsed['warnings']:
                context=[{'source':'PROWIDE','message_type':parsed['message_type'],'tag':n['tag'],'qualifier':n['qualifier'],'sequence_path':n['sequence_path']} for n in parsed['narratives']]
                from iso_adapter.facts import semantic_facts
                return {'input_type':'PROWIDE_PARSEABLE','parser':'PROWIDE','raw_source':text,'narrative':'\n\n'.join(n['text'] for n in parsed['narratives']) or text,'semantic_context':{'narrative_fields':context},'structured_facts':semantic_facts(parsed),'structure':parsed,'warnings':['Prowide Core parse success is not full SWIFT standards validation']}
            warnings.append(parsed)
        except Exception as e:warnings.append({'parser':'PROWIDE','error':f'{type(e).__name__}: {e}'})
    context=[{'source':'LENIENT_RECOVERY','tag':n['tag'],'qualifier':n['qualifier'],'sequence_path':n['sequence_path']} for n in recovery['narratives']]
    return {'input_type':'LENIENT_ISO_RECOVERABLE' if recovery['fields'] else 'UNRECOGNISED','parser':'LENIENT_RECOVERY','raw_source':text,
        'narrative':text,'semantic_context':{'recovered_narrative_fields':context},'structure':recovery,'warnings':warnings+recovery['warnings']+['Recovered context is not authoritative standards validation; full source retained']}
