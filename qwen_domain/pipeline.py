"""Rules + independent Qwen + evidence + correctness-confidence; no Laya dependency."""
import time,copy
from cascade.fallback import CommonFallback
from semantic_pipeline.pipeline import resolve_deadline
from semantic_pipeline.reconcile import llm_factors,reconcile
from semantic_pipeline.decision import decide
from semantic_pipeline.schema import PREDICATES
from semantic_pipeline.evidence import verify_evidence
from qwen_domain.protocol import ROOT,STUDY,read,digest,sha
from qwen_domain.confidence import confidence_output,decision_confidence

class DomainPipeline:
    def __init__(self,architecture='BASE_QWEN_DIRECT',*,calibrator=None,adapter=None):
        if architecture not in ('BASE_QWEN_DIRECT','CONSTRAINED_QWEN'):raise ValueError('Unknown domain architecture')
        self.architecture=architecture;self.calibrator=calibrator
        import os
        self.iso_enabled=os.environ.get('DOMAIN_ISO_ADAPTER','false').lower()=='true'
        config=read(ROOT/'data/experiments/cascade-v2/LLM-CONFIGS-v3.json')['QWEN_DIRECT']
        if adapter is not None:self.model=adapter
        elif architecture=='BASE_QWEN_DIRECT':self.model=CommonFallback(config)
        else:
            from qwen_domain.constrained import ConstrainedQwen
            self.model=ConstrainedQwen()
        self.identity=digest({'architecture':architecture,'model_digest':config['model_digest'],'prompt_version':self.model.prompt_version,
            'feature_code':sha(ROOT/'qwen_domain/confidence.py'),'pipeline_code':sha(__file__),'iso_adapter_enabled':self.iso_enabled})
    def analyse(self,text,*,reference='2026-10-17T12:00:00+00:00',language='en',repeat_agreement=None):
        if not isinstance(text,str) or not text.strip():raise ValueError('Nonempty source required')
        started=time.perf_counter();structured={};input_type='UNSTRUCTURED_NOTICE';narrative=text;parser=None
        # Parser integration is isolated and opt-in until its separate benchmark completes.
        import os
        if self.iso_enabled:
            from iso_adapter.routing import route
            parser=route(text);input_type=parser['input_type'];structured={**parser.get('structured_facts',{}),**parser.get('semantic_context',{})};narrative=parser.get('narrative') or text
        if self.architecture=='BASE_QWEN_DIRECT':
            raw=self.model.analyse(original_text=text,narrative_text=narrative,structured_facts=structured,mode='INDEPENDENT')
            merged=reconcile(structured,None,raw);preds=merged['predicates'];conflicts=merged['conflicts']
            valid=raw['valid'];repairs=(raw.get('schema_handling') or {}).get('repair_attempts',0)
        else:
            raw=self.model.analyse(text,structured=structured,evidence=True);preds=raw['predicates'];valid=all(p['valid'] for p in preds.values());repairs=0
            conflicts=[]
            if preds['votability']['value']=='NOT_VOTABLE' and any(p['value']=='YES' for k,p in preds.items() if k!='votability'):conflicts.append('Non-votable classification conflicts with a current mandatory voting condition')
        prepared={'parsed':None,'structured':structured,'narrative':narrative,'quarantined':False}
        deadline=resolve_deadline(text,prepared,raw if self.architecture=='BASE_QWEN_DIRECT' else None,reference)
        if parser and parser['parser']=='PROWIDE':
            from iso_adapter.facts import deadline as iso_deadline
            authoritative=iso_deadline(parser['structure'],reference)
            if authoritative['comparisons']:
                authoritative['narrative_diagnostic']=deadline
                authoritative['conflict']=authoritative['conflict'] or authoritative['status']!='UNKNOWN' and deadline['status']!='UNKNOWN' and authoritative['status']!=deadline['status']
                deadline=authoritative
        d_ev=[]
        for candidate in deadline.get('candidates',[]):
            span=verify_evidence(text,candidate['text'])
            if span['valid']:d_ev.append(span)
        preds['deadline_status']={'value':deadline['status'],'evidence':d_ev,'source':'DETERMINISTIC_DEADLINE_RULES'}
        confidences={k:confidence_output(text,k,v,calibrator=self.calibrator,identity=self.identity,language=language,input_type=input_type,
            schema_valid=valid if k!='deadline_status' else True,schema_repairs=repairs,repeat_agreement=repeat_agreement,
            deterministic_conflict=deadline.get('conflict',False)) for k,v in preds.items()}
        decision=decide({k:v for k,v in preds.items() if k in PREDICATES},deadline,conflicts+(['Evidence/model schema failure'] if not valid else []))
        return {'architecture':self.architecture,'model_identity':self.identity,'model_digest':read(ROOT/'data/experiments/cascade-v2/LLM-CONFIGS-v3.json')['QWEN_DIRECT']['model_digest'],
            'input_hash':digest(text),'raw_source_preserved':True,'parser':parser,'input_type':input_type,'predicates':preds,'confidence':confidences,
            'raw_model_result':raw,'deadline':deadline,'decision':decision,'decision_confidence':decision_confidence(decision['classification'],confidences),
            'reference':reference,'language':language,'latency_ms':(time.perf_counter()-started)*1000,'automation_enabled':False,'customer_accuracy':None}
