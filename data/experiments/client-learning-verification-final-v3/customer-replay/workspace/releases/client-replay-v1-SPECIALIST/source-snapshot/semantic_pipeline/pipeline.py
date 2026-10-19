"""Complete optional-parser → Laya → real local fallback → reconciliation path."""
import hashlib
import time
from hybrid.parser import parse, facts, deadline_status
from classifier.deadlines import extract_deadline
from semantic_pipeline.models import factor
from semantic_pipeline.schema import PREDICATES
from semantic_pipeline.routing import RoutingConfig, escalate
from semantic_pipeline.reconcile import reconcile
from semantic_pipeline.decision import decide
from semantic_pipeline.fallback import DisabledFallback
from semantic_pipeline.evidence import verify_evidence

REFERENCE='2026-10-16T12:00:00+00:00'

def prepare(text, use_parser=False):
    if not isinstance(text,str) or not text.strip(): raise ValueError('Nonempty source text required')
    if len(text)>2_000_000: raise ValueError('Input exceeds 2 million characters')
    parsed=parse(text) if use_parser else None
    structured={};narrative=text;quarantined=False
    if parsed and parsed['kind'] in ('PARTIAL_ISO15022','VALID_ISO15022','ISO15022_LIKE'):
        structured['iso15022_fields']=[f for f in parsed['facts'] if f['name'] not in ('sequence','narrative')]
        fields=facts(parsed,'narrative')
        narrative='\n\n'.join(f['value'] for f in fields) if fields else ''
        offered=[f for f in facts(parsed,'option_code') if f['value'] in {'ABST','AMGT','MNGT','PROX','CONN','CONY','CEXC','CTEN'} and f['path'] and f['path'][-1].startswith('CAOPTN[')]
        if offered and parsed['message_type'] in ('MT564',None):
            structured['votability']=factor('VOTABLE','ISO15022_OPTION',evidence=[{'valid':True,'text':text[f['start']:f['end']],'start':f['start'],'end':f['end'],'field_id':f['field_id']} for f in offered])
        quarantined=bool(parsed['errors']) or any(f['value'] in ('CANC','REPL') for f in facts(parsed,'function'))
    return {'parsed':parsed,'structured':structured,'narrative':narrative,'quarantined':quarantined}

def resolve_deadline(text, prepared, llm=None, reference=REFERENCE):
    p=prepared['parsed']
    if p:
        result=deadline_status(p,reference)
        if result['comparisons']:
            result['source']='ISO15022_DETERMINISTIC'
            narrative_deadline=extract_deadline(prepared['narrative'],reference)
            result['narrative_diagnostic']=narrative_deadline
            if narrative_deadline['status']!='UNKNOWN' and result['status']!='UNKNOWN' and narrative_deadline['status']!=result['status']:
                result['conflict']=True
                result['reason']='Authoritative RDDT retained; conflicting narrative deadline requires review'
            return result
    result=extract_deadline(text,reference)
    result['source']='DETERMINISTIC_NOTICE_EXTRACTION'
    if llm and llm.get('valid'):
        ev=llm['evidence_validation']['deadline']
        if ev and ev['valid']:
            candidate=extract_deadline(ev['text'],reference)
            result['llm_extracted_passage']=ev
            if candidate['status']!='UNKNOWN':
                # A verified passage may resolve historical/multiple unrelated dates.
                # It may NOT contradict a confidently parsed current deadline silently.
                if result['status']!='UNKNOWN' and candidate['status']!=result['status']:
                    return {**result,'status':'UNKNOWN','conflict':True,'reason':'Conflicting current deadline interpretations'}
                result={**candidate,'source':'LLM_EXACT_PASSAGE_DETERMINISTIC_COMPARISON','passage':ev}
    return result

def run(text, architecture, *, laya_model=None, fallback=None, routing=None,
        reconciliation_policy=None, precomputed_laya=None, precomputed_llm=None, reference=REFERENCE):
    if architecture not in 'ABCDE' or len(architecture)!=1: raise ValueError('Invalid architecture')
    started=time.perf_counter();prepared=prepare(text,architecture=='E')
    laya=None
    if architecture!='D':
        if architecture=='E' and not prepared['narrative']:
            laya={'predicates':{k:factor('UNCERTAIN' if k=='votability' else 'UNKNOWN','NO_NARRATIVE') for k in PREDICATES},
                'checkpoint':None,'model_version':None,'latency_ms':0,'truncated':False,'raw':None}
        else:
            laya=precomputed_laya or laya_model.analyse(prepared['narrative'])
        # Evidence from joined ISO narratives must be remapped to exact original source.
        if architecture=='E' and prepared['narrative']!=text:
            for a in laya['predicates'].values():
                a['evidence']=[verify_evidence(text,e['text']) for e in a.get('evidence',[]) if e.get('valid') and verify_evidence(text,e['text'])['valid']]
    gate={'escalated':architecture=='D','reasons':['INDEPENDENT_LLM_BENCHMARK'] if architecture=='D' else []}
    if architecture in ('C','E'):
        gate=escalate(laya,prepared['structured'],text,routing or RoutingConfig())
        if architecture=='E' and not prepared['narrative']:
            gate={'escalated':False,'reasons':['NO_NARRATIVE_HUMAN_REVIEW'],'configuration':gate['configuration']}
    llm=None
    if gate['escalated']:
        if precomputed_llm is not None: llm=precomputed_llm
        else:
            llm=(fallback or DisabledFallback()).analyse(original_text=text,
                narrative_text=prepared['narrative'], structured_facts=prepared['structured'],
                laya_result=diagnostic(laya) if architecture!='D' else None,
                mode='INDEPENDENT' if architecture=='D' else 'FALLBACK')
    merged=reconcile(prepared['structured'],laya,llm,reconciliation_policy)
    deadline=resolve_deadline(text,prepared,llm,reference)
    conflicts=merged['conflicts']+(['Conflicting deadline facts'] if deadline.get('conflict') else [])
    if gate['escalated'] and llm and not llm.get('valid'):
        conflicts.append('Required fallback unavailable: '+llm.get('error','No validated semantic result'))
        merged['conflicts']=conflicts
    decision=decide(merged['predicates'],deadline,conflicts,prepared['quarantined'])
    if architecture in ('A','B'):
        # Historical five-head model's exact decision preserved, clearly labelled.
        decision={**decision,'classification':laya['raw']['classification'],
            'rule':'LEGACY_WHOLE_TEXT_LAYA frozen status policy',
            'rule_version':'legacy-factorised-1'}
        deadline={**deadline,'status':laya['predicates']['deadline_status']['value'],
            'source':'LEGACY_LAYA_TEMPORAL_HEAD','deterministic_diagnostic':deadline}
    return {'architecture':architecture,'input_hash':hashlib.sha256(text.encode()).hexdigest(),
        'parser':prepared['parsed'],'structured_facts':prepared['structured'],
        'narrative_text':prepared['narrative'],'laya':laya,'escalation':gate,'llm':llm,
        'reconciliation':merged,'deadline':deadline,'decision':decision,
        'latencies':{'laya_ms':laya['latency_ms'] if laya else 0,'llm_ms':llm['latency_ms'] if llm else 0,
            'total_ms':(time.perf_counter()-started)*1000},'reference':reference,
        'automation_enabled':False,'pipeline_version':'semantic-pipeline-2'}

def diagnostic(laya):
    if laya is None:return None
    # Bound prompt to auditable semantic outputs, not SDK tensors/usage or repeated chunk data.
    return {'checkpoint':laya['checkpoint'],'model_version':laya['model_version'],
        'predicates':{k:{q:v for q,v in a.items() if q in ('value','scores','confidence','margin','evidence','conflict')}
            for k,a in laya['predicates'].items()},'truncated':laya.get('truncated',False)}
