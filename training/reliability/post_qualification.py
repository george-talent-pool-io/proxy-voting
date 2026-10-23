"""Post-freeze real challenge and direct hybrid parity checks. No tuning."""
import argparse
import copy
import hashlib
import json
import os
import time
from pathlib import Path

from training.framework import releases
from training.framework.bundle import write, sha, jsonl
from training.framework.resources import model_resource
from training.reliability.paired_report import run as report, lines
from scripts.qualify_model_installation import semantic_signature
from semantic_pipeline.metrics import summarize

CHALLENGE_HASH='0e2f5d991a33deed25f8e9a33682185071c5ff35afd2df9179c1f8565dd17649'


def run(path):
    root=Path(path)
    completed=json.loads((root/'RESULT.json').read_text())
    freeze=json.loads((root/'MODEL_FREEZE.json').read_text())
    if freeze['runtime_sources']!=releases.source_files():raise ValueError('Serving condition changed')
    report(root)
    out=root/'post-freeze';out.mkdir(exist_ok=False)
    write(out/'PLAN.json',{'source_sha256':sha(__file__),'releases':completed['releases'],
        'parity_input_selection':'First three persisted development pilot rows; no threshold/model selection',
        'challenge_sha256':CHALLENGE_HASH,'automation_enabled':False,'customer_accuracy':None})
    cache={}
    class NativeReadThrough:
        def __init__(self,*args):pass
        def analyse(self,text,**kwargs):
            if cache['text']!=text or cache['reference']!=kwargs['reference'] or kwargs.get('structured_context'):
                raise ValueError('Native replay input/context mismatch')
            return copy.deepcopy(cache['stage'])
        def close(self):pass
    refs=completed['releases']
    with model_resource('post-frozen-qualification'):
        # Re-execute the actual hybrid with no native-stage cache and compare
        # semantics to the saved paired replay. Includes real Qwen lazy loads.
        original=lines(root/'HYBRID-VALIDATION-PILOT/predictions.jsonl')[:3]
        model=releases.ReleaseModel(refs['HYBRID']['path'])
        parity=[]
        try:
            for row in original:
                before=time.perf_counter()
                result=model.analyse(row['text'],use_iso=False,reference=row['evaluation_time'])
                parity.append({'id':row['id'],'text':row['text'],'result':result,
                    'request_ms':(time.perf_counter()-before)*1000,
                    'same_semantics':semantic_signature(result)==semantic_signature(row['result']),
                    'physical_llm_invoked':bool((result.get('llm') or {}).get('invoked'))})
                print(json.dumps({'phase':'DIRECT_HYBRID_PARITY','done':len(parity)}),flush=True)
        finally:model.close()
        jsonl(out/'direct-hybrid-parity.jsonl',parity)
        write(out/'DIRECT_HYBRID_PARITY.json',{'n':len(parity),'identical':sum(r['same_semantics'] for r in parity),
            'actual_qwen_calls':sum(r['physical_llm_invoked'] for r in parity),
            'request_seconds':[r['request_ms']/1000 for r in parity],
            'scope':'Actual uncached hybrid; three development inputs only, not sustained throughput'})
        source=Path('tests/fixtures/semantic.json')
        if sha(source)!=CHALLENGE_HASH:raise ValueError('Frozen challenge changed')
        challenge=json.loads(source.read_text())
        inputs=[{'id':r['id'],'text':r['text'],'evaluation_time':r['reference_date']+'T12:00:00+00:00'} for r in challenge]
        primary=releases.ReleaseModel(refs['PRIMARY']['path'])
        hybrid=releases.ReleaseModel(refs['HYBRID']['path'],llm_factory=NativeReadThrough)
        outputs={k:[] for k in ('PRIMARY','HYBRID','LAYA')}
        streams={k:(out/(k+'-challenge.jsonl')).open('x') for k in outputs}
        try:
            for row in inputs:
                if freeze['runtime_sources']!=releases.source_files():raise ValueError('Frozen serving condition drift')
                before=time.perf_counter();a=primary.analyse(row['text'],use_iso=False,reference=row['evaluation_time'])
                elapsed=(time.perf_counter()-before)*1000
                cache.update(text=row['text'],reference=row['evaluation_time'],stage=a['llm_stage'])
                before=time.perf_counter();b=hybrid.analyse(row['text'],use_iso=False,reference=row['evaluation_time'])
                replay=(time.perf_counter()-before)*1000
                for name,result,ms in [('PRIMARY',a,elapsed),('HYBRID',b,replay),('LAYA',b['laya'],None)]:
                    record={**row,'result':result,'request_ms':ms}
                    outputs[name].append(record);streams[name].write(json.dumps(record,ensure_ascii=False,allow_nan=False)+'\n')
                    streams[name].flush();os.fsync(streams[name].fileno())
                print(json.dumps({'phase':'FROZEN_CHALLENGE','done':len(outputs['PRIMARY']),
                    'primary_seconds':round(elapsed/1000,3),'hybrid_logical_llm':bool(b['llm'])}),flush=True)
        finally:
            primary.close();hybrid.close()
            for f in streams.values():f.close()
        write(out/'CHALLENGE_PREDICTIONS_SAVED.json',{'streams':{k:{'count':len(v),'sha256':sha(out/(k+'-challenge.jsonl'))} for k,v in outputs.items()},
            'physical_qwen_generations':len(outputs['PRIMARY']),
            'hybrid_latency_scope':'Replay plus actual Laya; excludes Qwen generation; not actual end-to-end hybrid time',
            'expected_assertions_passed_to_models':False,'automation_enabled':False})
        # Partial ground truth is attached only after all three streams persist.
        truth={r['id']:r['expected'] for r in challenge}
        metrics={k:summarize([{**r,'expected':truth[r['id']]} for r in values]) for k,values in outputs.items()}
        if any(m['assertions']!=95 or m['final_status_labelled_cases']!=4 for m in metrics.values()):
            raise ValueError('Authored challenge denominator changed')
        write(out/'CHALLENGE_METRICS.json',metrics)
    write(out/'RESULT.json',{'challenge_metrics':'CHALLENGE_METRICS.json','direct_hybrid_parity':'DIRECT_HYBRID_PARITY.json',
        'automation_enabled':False,'customer_accuracy':None})


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('experiment');a=p.parse_args();run(a.experiment)
