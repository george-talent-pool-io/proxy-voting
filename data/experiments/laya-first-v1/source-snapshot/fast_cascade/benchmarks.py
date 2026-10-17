"""Measured experiments, with cache/queue/resource scope explicitly retained."""
import time,numpy as np
from fast_cascade.protocol import *
from cascade.resources import Sampler

def batch_benchmark():
    target=STUDY/'LAYA-BATCH-BENCHMARK.json'
    if target.exists():return read(target)
    from fast_cascade.laya import BatchedLaya
    from qwen_domain.protocol import load_inputs
    data=[r for r in load_inputs(CORPUS/'MANIFEST.json','TRAIN') if r['language']=='en']
    # Fixed input-only length quantiles. No validation/frozen labels are consulted.
    order=sorted(data,key=lambda x:(len(x['text']),x['id']));data=[order[int(i*(len(order)-1)/15)] for i in range(16)]
    model=BatchedLaya(8);results=[];baseline=None
    for batch in (1,8,16,32):
        check_stop();model.batch_size=batch;model.analyse(data[0]['text']) # explicit unmeasured warm-up
        sampler=Sampler().start();start=time.perf_counter();out=model.analyse_batch([r['text'] for r in data]);wall=time.perf_counter()-start;resource=sampler.finish()
        labels=[{k:p['value'] for k,p in r['predicates'].items()} for r in out]
        if baseline is None:baseline=labels
        results.append({'sdk_batch_size':batch,'records':len(data),'source_ids':[r['id'] for r in data],'wall_seconds':wall,'notices_per_second':len(data)/wall,
            'median_batch_amortised_ms':float(np.median([r['latency_ms'] for r in out])),'p95_batch_amortised_ms':float(np.percentile([r['latency_ms'] for r in out],95)),
            'label_changes_from_batch1':sum(a[k]!=b[k] for a,b in zip(baseline,labels) for k in a),'predictions':labels,'resources':resource})
    chosen=min(results,key=lambda r:r['wall_seconds'] if r['label_changes_from_batch1']==0 else float('inf'))['sdk_batch_size']
    result={'created_at':now(),'population':'16 TRAIN notices at input-length quantiles; no quality estimate','load_time_ms':model.load_time_ms,'selected_sdk_batch_size':chosen,'results':results,
        'latency_caveat':'Amortised batch service time. Individual completions/queueing are measured separately in the end-to-end workload.'}
    write(target,result);return result

def native_probe(model):
    path=STUDY/'NATIVE-CACHE-EVIDENCE-BENCHMARK.json'
    if path.exists():return read(path)
    from qwen_domain.protocol import load_inputs
    data=[r for r in load_inputs(CORPUS/'MANIFEST.json','TRAIN') if r['language']=='en']
    data=sorted(data,key=lambda r:len(r['text']));sample=[data[0],data[len(data)//2],data[-1]];out=[]
    for c in sample:
        for cache in (False,True):
            # Same notice prefix; three different predicate questions. Explicit no-cache primes cannot be credited as reuse.
            start=time.perf_counter();results=[]
            model.ensure()
            for k in ['share_blocking','poa_required','registration_required']:results.append(model.tokens.classify(c['text'],k,cache=cache))
            out.append({'id':c['id'],'text_chars':len(c['text']),'cache_prompt':cache,'wall_ms':(time.perf_counter()-start)*1000,'calls':results})
    write(path,{'created_at':now(),'measurements':out,'prefix_reuse_supported':True,'limitation':'Automatic longest-prefix reuse in a single native llama-server slot, not an encode-once branched KV API. Different passages/full-generation requests may evict the prefix.',
        'class_tokens':{'A':{'id':32,'value':'YES'},'B':{'id':33,'value':'NO'},'C':{'id':34,'value':'UNKNOWN'}},'raw_probabilities_are_calibrated':False})
