"""One owned Ollama/Qwen process shared by constrained and full inference."""
import copy,threading,time
import psutil
from cascade.fallback import CommonFallback
from qwen_domain.constrained import ConstrainedQwen,ANCHORS
from qwen_domain.runtime import request
from semantic_pipeline.evidence import verify_evidence
from semantic_pipeline.schema import PREDICATES
from fast_cascade.protocol import ROOT,STUDY,read,append,now

class SharedQwen:
    def __init__(self):
        self.config=read(ROOT/'data/experiments/cascade-v2/LLM-CONFIGS-v3.json')['QWEN_DIRECT'];self.full_model=None;self.tokens=None;self.lock=threading.RLock();self.runtime=None
    def ensure(self):
        from scripts.start_cascade_runtime import ensure
        ensure();started=time.perf_counter()
        request(self.config['base_url'],'/api/generate',{'model':self.config['model'],'keep_alive':'30m'})
        for p in psutil.process_iter(['pid','ppid','cmdline']):
            try:
                c=p.info['cmdline'] or []
                if not c or 'llama-server' not in c[0] or '--model' not in c:continue
                if psutil.Process(p.ppid()).environ().get('OLLAMA_HOST')!='127.0.0.1:11435':continue
                if c[c.index('--model')+1].split('/')[-1]!='sha256-f5f1dd8920d417aac2718b0bda3403da274301efdd6760b4f0f4b864ff2ad57d':raise RuntimeError('Shared runner checkpoint mismatch')
                base='http://127.0.0.1:'+c[c.index('--port')+1]
                request(base,'/health')
                previous=(self.runtime or {}).get('pid');self.runtime={'pid':p.pid,'parent_pid':p.ppid(),'native_base':base,'command':c,'same_process_for_both_gears':True,'load_or_lease_ms':(time.perf_counter()-started)*1000}
                if previous!=p.pid:
                    self.tokens=ConstrainedQwen(base_url=base)
                    append(STUDY/'RUNTIME-EVENTS.jsonl',{'timestamp':now(),**self.runtime,'compatibility':'Pinned Ollama internal llama-server API; changes require compatibility re-verification'})
                return
            except (psutil.NoSuchProcess,psutil.AccessDenied):continue
        raise RuntimeError('Cannot verify the owned local native runtime; no alternate model substituted')
    def full(self,text,structured=None):
        with self.lock:
            self.ensure()
            if self.full_model is None:self.full_model=CommonFallback(self.config)
            result=self.full_model.analyse(original_text=text,narrative_text=text,structured_facts=structured or {},mode='INDEPENDENT')
            result['shared_runtime']=self.runtime
            return result
    def constrained(self,text,requested,*,laya=None,structured=None,cache=True,evidence_strategy='PASSAGE_SCORING'):
        import re
        if not set(requested)<=set(PREDICATES):raise ValueError('Unknown predicate')
        with self.lock:
            self.ensure();started=time.perf_counter();preds={};calls=0
            for key in requested:
                calls+=1;call_started=time.perf_counter()
                try:p=self.tokens.classify(text,key,structured=structured,cache=cache)
                except ValueError as e:
                    # Missing/invalid class probabilities are unavailable, never zeros.
                    # Checkpoint/tokenizer identity errors remain fatal configuration failures.
                    if 'differs from frozen' in str(e) or 'tokenizer' in str(e):raise
                    preds[key]={'value':'UNCERTAIN' if key=='votability' else 'UNKNOWN','valid':False,'source':'QWEN_CONSTRAINED_FAILURE','error':str(e),'raw_model_probability':None,'confidence':None,'evidence':[],'latency_ms':(time.perf_counter()-call_started)*1000}
                    continue
                p.setdefault('latency_ms',(time.perf_counter()-call_started)*1000)
                p['source']='QWEN_CONSTRAINED'
                existing=(laya or {}).get('predicates',{}).get(key,{})
                supporting=[e for e in existing.get('evidence',[]) if e.get('valid') and existing.get('value')==p['value']]
                if supporting:
                    p['evidence']=[verify_evidence(text,e['text']) for e in supporting];p['evidence_method']='NATIVE_LAYA_PASSAGE_AND_QWEN_DOCUMENT_AGREE'
                else:
                    candidates=[m.group().strip() for m in re.finditer(r'[^.!?\n]+(?:[.!?]|$)',text) if re.search(ANCHORS[key],m.group(),re.I)]
                    p['deterministic_evidence_candidates']=[verify_evidence(text,s) for s in candidates[:3]]
                    if candidates and p['value'] not in ('UNKNOWN','UNCERTAIN') and evidence_strategy=='PASSAGE_SCORING':
                        # One targeted evidence call, then abstain/escalate if it cannot support the result.
                        candidate=candidates[0];calls+=1
                        try:passage=self.tokens.classify(text,key,passage=candidate,structured=structured,cache=cache)
                        except ValueError as e:
                            if 'differs from frozen' in str(e):raise
                            p.setdefault('evidence_errors',[]).append(str(e));preds[key]=p;continue
                        p['passage_scores']=[{'source':candidate,'result':passage}]
                        if passage['value']==p['value']:
                            ev=verify_evidence(text,candidate)
                            if ev['valid']:p['evidence']=[{**ev,'relevance':'MODEL_ASSESSED_NOT_EXPERT_VERIFIED'}];p['evidence_method']='CONTEXTUAL_PASSAGE_SCORING'
                if not p.get('evidence'):p['evidence_method']='EVIDENCE_UNAVAILABLE'
                preds[key]=p
            return {'predicates':preds,'requested_predicates':list(requested),'native_model_calls':calls,'notice_invoked':bool(requested),'latency_ms':(time.perf_counter()-started)*1000,'runtime':self.runtime,'raw_model_probability_is_calibrated':False,'evidence_strategy':evidence_strategy}
