"""Post-study repeatability/resource probe. Never used for prompt or routing selection."""
import json,time,threading,statistics
from pathlib import Path
import psutil
from semantic_pipeline.experiment import ROOT,read,lines,append,write,now
from semantic_pipeline.fallback import OllamaFallback
from semantic_pipeline.pipeline import run
from semantic_pipeline.schema import PREDICATES

def run_probe(root=ROOT):
    path=root/'REPEATABILITY-60-CALLS.jsonl'
    chosen=read(root/'validation.json')
    # Deterministic diversity: length bins plus rare positive restrictions, validation only.
    ordered=sorted(chosen,key=lambda r:(len(r['text']),r['id']))
    selected=[ordered[round(i*(len(ordered)-1)/19)] for i in range(20)]
    existing={(r['id'],r['repeat']):r for r in lines(path)}
    peak={};stop=threading.Event()
    def sample():
        while not stop.is_set():
            for p in psutil.process_iter(['pid','name','memory_info']):
                try:
                    if 'ollama' in p.info['name'].lower() or p.pid==psutil.Process().pid:
                        key=f"{p.pid}:{p.info['name']}";peak[key]=max(peak.get(key,0),p.info['memory_info'].rss)
                except (psutil.NoSuchProcess,psutil.AccessDenied):pass
            stop.wait(.1)
    thread=threading.Thread(target=sample,daemon=True);thread.start()
    fallback=OllamaFallback();started=time.perf_counter()
    try:
        for row in selected:
            for repeat in range(3):
                if (row['id'],repeat) in existing:continue
                result=run(row['text'],'D',fallback=fallback)
                item={'id':row['id'],'repeat':repeat,'text':row['text'],'timestamp':now(),'result':result,
                    'purpose':'POST_STUDY_REPEATABILITY_ONLY_NO_TUNING'}
                append(path,item);existing[(row['id'],repeat)]=item
                print(row['id'],repeat,result['llm']['valid'],flush=True)
    finally:stop.set();thread.join()
    cases=[]
    for row in selected:
        rs=[existing[row['id'],i]['result'] for i in range(3)]
        raw=[r['llm']['raw_response']['message']['content'] for r in rs]
        parsed=[r['llm']['parsed'] for r in rs]
        labels=[{k:p[k] for k in PREDICATES} for p in parsed]
        cases.append({'id':row['id'],'raw_text_stable':len(set(raw))==1,'parsed_result_stable':all(p==parsed[0] for p in parsed),
            'semantic_labels_stable':all(p==labels[0] for p in labels),'final_decision_stable':len({r['decision']['classification'] for r in rs})==1})
    write(root/'REPEATABILITY-RESOURCE-SUMMARY.json',{'created_at':now(),'cases':cases,'unique_cases':20,'repetitions':3,
        'mode':'INDEPENDENT','calls':60,'wall_seconds_this_process':time.perf_counter()-started,'process_peak_rss_bytes':peak,
        'memory_caveat':'Process RSS sampling, not total Apple unified model allocation; 100ms samples may miss shorter peaks.',
        'runtime_model_allocation':fallback.http('/api/ps'),'time_to_first_token':'NOT_AVAILABLE: nonstreaming runtime requests',
        'model':fallback.config,'settings_identical':True,'scope':'Validation-only post-study diagnostic; finite repeatability is not proof of universal determinism.'})

if __name__=='__main__':run_probe()
