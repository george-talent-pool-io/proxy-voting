"""New versioned optional-parser path; historical inference code is untouched."""
import time,hashlib,re,copy
from hybrid.parser import parse
from semantic_pipeline.pipeline import prepare,resolve_deadline,diagnostic,REFERENCE
from semantic_pipeline.reconcile import reconcile
from semantic_pipeline.decision import decide
from semantic_pipeline.evidence import verify_evidence
from cascade.routing import gate,Policy

def execute(text,*,specialist=None,precomputed=None,fallback=None,policy=None,use_parser=False,precomputed_llm=None):
    start=time.perf_counter();policy=policy or Policy();input_type='UNSTRUCTURED_NOTICE'
    # Detection is deliberately cheap; complete parsing is only applied to tagged input.
    iso_hint=bool(re.search(r'(?:^|[\r\n]):\d{2}[A-Z]?:',text) or re.search(r'\{2:[IO](?:564|565|567|568)',text))
    prepared=prepare(text,bool(use_parser and iso_hint))
    if iso_hint:input_type=(prepared['parsed'] or parse(text))['kind']
    if not prepared['narrative']:
        from semantic_pipeline.models import factor
        from semantic_pipeline.schema import PREDICATES
        laya={'predicates':{k:factor('UNCERTAIN' if k=='votability' else 'UNKNOWN','NO_NARRATIVE') for k in PREDICATES},'latency_ms':0,'checkpoint':None,'model_version':None,'truncated':False}
    else:laya=copy.deepcopy(precomputed) if precomputed is not None else specialist.analyse(prepared['narrative'])
    if prepared['narrative']!=text:
        for pred in laya['predicates'].values():
            pred['evidence']=[verify_evidence(text,e['text']) for e in pred.get('evidence',[]) if e.get('valid') and verify_evidence(text,e['text'])['valid']]
            for state in pred.get('passage_states',[]):state['original_source_span']=verify_evidence(text,state['text'])
    escalation=gate(text,laya,prepared['structured'],policy)
    if not prepared['narrative']:escalation={**escalation,'escalated':False,'reasons':['NO_NARRATIVE_MANUAL_REVIEW']}
    llm=None
    if escalation['escalated']:
        llm=precomputed_llm if precomputed_llm is not None else fallback.analyse(original_text=text,narrative_text=prepared['narrative'],structured_facts=prepared['structured'],laya_result=diagnostic(laya),mode='FALLBACK')
    merged=reconcile(prepared['structured'],laya,llm);deadline=resolve_deadline(text,prepared,llm)
    conflicts=merged['conflicts']+(['Conflicting deadlines'] if deadline.get('conflict') else [])
    if escalation['escalated'] and (not llm or not llm.get('valid')):conflicts.append('Required local fallback unavailable or invalid')
    return {'architecture':'E' if use_parser else 'C','pipeline_version':'selective-cascade-v1','input_type':input_type,
        'parser_status':'APPLIED' if prepared['parsed'] else 'NOT_APPLICABLE' if not iso_hint else 'NOT_SELECTED',
        'parser':prepared['parsed'],'structured_facts':prepared['structured'],'narrative_text':prepared['narrative'],
        'laya':laya,'escalation':escalation,'llm':llm,'reconciliation':merged,'deadline':deadline,
        'decision':decide(merged['predicates'],deadline,conflicts,prepared['quarantined']),
        'latencies':{'laya_ms':laya['latency_ms'],'llm_ms':llm['latency_ms'] if llm else 0,'total_ms':(time.perf_counter()-start)*1000},
        'input_hash':hashlib.sha256(text.encode()).hexdigest(),'reference':REFERENCE,'automation_enabled':False}
