"""Optional one-retry schema recovery. Not used in the frozen A–E study."""
import copy,time
from pathlib import Path
from semantic_pipeline.fallback import OllamaFallback,digest,DisabledFallback
from semantic_pipeline.schema import SemanticResult
from semantic_pipeline.evidence import validate_all

class BoundedRepairFallback(OllamaFallback):
    def analyse(self,**kwargs):
        first=super().analyse(**kwargs)
        first['schema_handling']={'first_pass_success':first['valid'],'repair_attempts':0,'repair_success':False,'final_failure':not first['valid']}
        raw=first.get('raw_response')
        # Retry only a completed generation whose schema is invalid, never a failed runtime,
        # context overflow, timeout or truncated generation. Maximum two model calls total.
        if first['valid'] or not raw or raw.get('done_reason')!='stop':return first
        instruction=Path(__file__).with_name('repair_prompt.txt').read_text()
        request=copy.deepcopy(first['request']);request['messages'] += [raw['message'],{'role':'user','content':instruction}]
        out={**first,'first_attempt':copy.deepcopy(first),'valid':False,'parsed':None,'evidence_validation':None,
            'prompt_version':digest({'initial_prompt_version':first['prompt_version'],'repair_instruction':instruction}),
            'repair_request':request,'repair_request_hash':digest(request)}
        out['schema_handling']={'first_pass_success':False,'repair_attempts':0,'repair_success':False,'final_failure':True}
        budget=self.config['num_ctx']-self.config['num_predict']-256
        if sum(len(m['content'].encode()) for m in request['messages'])>budget:
            out['error']='REPAIR_CONTEXT_BUDGET_EXCEEDED';return out
        started=time.perf_counter();out['schema_handling']['repair_attempts']=1
        try:
            self.check_identity();repaired=self.http('/api/chat',request);out['repair_raw_response']=repaired
            if not repaired.get('done') or repaired.get('done_reason')!='stop':raise ValueError('Incomplete repair generation')
            parsed=SemanticResult.model_validate_json(repaired['message']['content']).model_dump()
            out.update(parsed=parsed,valid=True,evidence_validation=validate_all(kwargs['original_text'],parsed))
            out.pop('error',None);out['schema_handling'].update(repair_success=True,final_failure=False)
        except Exception as exc:out['error']=f'{type(exc).__name__}: {exc}'
        out['latency_ms']+=(time.perf_counter()-started)*1000
        return out

def configured_fallback():
    import os
    if os.environ.get('LLM_ENABLED','false').lower()!='true':return DisabledFallback()
    return BoundedRepairFallback() if os.environ.get('LLM_SCHEMA_REPAIR','false').lower()=='true' else OllamaFallback()
