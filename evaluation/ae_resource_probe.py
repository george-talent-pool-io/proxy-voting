"""Warm resource sampling supplement, includes llama-server child and device allocation."""
import psutil,time,threading,gc
from semantic_pipeline.experiment import ROOT,read,write,append,now,laya_for
from semantic_pipeline.pipeline import run
from semantic_pipeline.routing import RoutingConfig
from semantic_pipeline.fallback import OllamaFallback

def probe():
    peak={};stop=threading.Event();llm=OllamaFallback();stages=[]
    def sample():
        while not stop.is_set():
            for p in psutil.process_iter(['pid','name','memory_info']):
                try:
                    if any(k in p.info['name'].lower() for k in ('ollama','llama-server')) or p.pid==psutil.Process().pid:
                        key=f"{p.pid}:{p.info['name']}";peak[key]=max(peak.get(key,0),p.info['memory_info'].rss)
                except (psutil.NoSuchProcess,psutil.AccessDenied):pass
            stop.wait(.05)
    t=threading.Thread(target=sample,daemon=True);t.start()
    selection=read(ROOT/'VALIDATION-SELECTION.json');row=read(ROOT/'validation.json')[0]
    try:
        for arm in 'ABCDE':
            start=time.perf_counter();model=laya_for(arm);load_ms=(time.perf_counter()-start)*1000
            result=run(row['text'],arm,laya_model=model,fallback=llm,routing=RoutingConfig(**selection['routing'].get(arm,{})),reconciliation_policy=selection['reconciliation_policies'].get(arm,{}))
            stages.append({'arm':arm,'laya_load_ms':load_ms,'python_rss_bytes':psutil.Process().memory_info().rss,
                'llm_model_allocation':llm.http('/api/ps'),'result':result})
            del model;gc.collect()
            import torch
            if torch.backends.mps.is_available():torch.mps.empty_cache()
    finally:stop.set();t.join()
    write(ROOT/'RESOURCE-SUPPLEMENT.json',{'created_at':now(),'hardware_memory':'64 GiB Apple unified memory',
        'sample_period_seconds':.05,'peak_process_rss_bytes':peak,'stages':stages,'source_id':row['id'],
        'excluded_from_timed_AE_comparison':True,'scope':'One existing validation record per architecture, warm Ollama; separate component feasibility probe. Laya load includes reading/hash/checkpoint construction. RSS can include shared mappings; do not sum processes as distinct physical allocation. Model runtime allocation is not discrete VRAM.'})
    print(peak,flush=True)
if __name__=='__main__':probe()
