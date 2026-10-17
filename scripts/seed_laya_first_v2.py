"""Replay unchanged v1 native validation observations with the v3 reducer.

No inference is performed here. Loading pinned Laya verifies model/questions and
computes the exact new identity. Full-Qwen references require identical requests.
"""
import copy,time,shutil
from fast_cascade.protocol import *
from fast_cascade.study import prepare,inputs,cached,save
from fast_cascade.laya import BatchedLaya
from fast_cascade.aggregation import aggregate
from semantic_pipeline.schema import RESTRICTIONS
from cascade.fallback import CommonFallback


def main():
    prepare();old=ROOT/'data/experiments/laya-first-v1';original=read(old/'PROTOCOL.json')
    current=read(STUDY/'PROTOCOL.json')
    if original['weights']!=current['weights']:raise ValueError('Replay cannot use changed model weights')
    for name,h in original['sources'].items():
        if sha(old/'source-snapshot'/name)!=h:raise ValueError('Original source snapshot missing or changed: '+name)
    if inputs('VALIDATION')!=read(old/'inputs/VALIDATION.json'):raise ValueError('Validation sample changed')
    model=BatchedLaya(8);by={r['id']:r for r in inputs('VALIDATION')};done={r['id'] for r in cached('VALIDATION','LAYA')}
    source=old/'predictions/VALIDATION-LAYA.jsonl';observations=rows(source);source_sha=sha(source)
    for row in observations:
        if row['id'] in done:continue
        c=by[row['id']]
        if row['input_hash']!=digest(c['text']):raise ValueError('Replay source differs')
        p=copy.deepcopy(row['result']);start=time.perf_counter();previous=copy.deepcopy(p['predicates'])
        if set(p['passage_predictions'])!=set(model.narrow.model.questions):raise ValueError('Question set differs')
        for key in RESTRICTIONS:p['predicates'][key]={**p['predicates'][key],**aggregate(c['text'],key,p['passage_predictions'][key],model.aggregation)}
        p.update(pre_native_positive_fix_predicates=previous,aggregation_version='native-positive-evidence-aggregation-v3',laya_identity=model.identity,
            native_inference_reused_from=str(source.relative_to(ROOT)),native_source_file_sha256=source_sha,aggregation_replay_ms=(time.perf_counter()-start)*1000,
            latency_scope='Unchanged historical native batch-amortised time; reduction replay separately measured; not fresh pipeline latency')
        save('VALIDATION','LAYA',c,p,reused_from=str(source.relative_to(ROOT)))
    config=current['qwen_model'];adapter=CommonFallback(config);done={r['id'] for r in cached('VALIDATION','FULL')};full=old/'predictions/VALIDATION-FULL.jsonl'
    if full.exists():
        for row in rows(full):
            if row['id'] in done:continue
            c=by[row['id']];raw=row['result']['raw'];expected=adapter.request(c['text'],c['text'],{},None,'INDEPENDENT')
            if digest(raw['request'])!=digest(expected) or raw['model_digest']!=config['model_digest']:raise ValueError('Full-reference request/model differs')
            save('VALIDATION','FULL',c,row['result'],reused_from=str(full.relative_to(ROOT)),original_run_id=row['run_id'])
    reused={}
    for name in ['NATIVE-CACHE-EVIDENCE-BENCHMARK.json','NATIVE-CACHE-INTERPRETATION.json','SHARED-NATIVE-TOKEN-PROBE.json','SHARED-RUNTIME-PROBE.json']:
        src=old/name;dst=STUDY/name
        if not dst.exists():shutil.copyfile(src,dst)
        if sha(src)!=sha(dst):raise ValueError('Reused measurement changed')
        reused[name]={'path':str(src.relative_to(ROOT)),'sha256':sha(src),'scope':'Identical Qwen weights, neutral prompt, input, native runtime and request; no aggregation dependency. Historical measured time, not a new execution.'}
    manifest=STUDY/'REUSED-OBSERVATIONS.json'
    if not manifest.exists():write(manifest,{'created_at':now(),'previous_protocol_sha256':sha(old/'PROTOCOL.json'),'unchanged_weights':current['weights'],'validation_native_sha256':sha(source),'reuse':reused,'seed_script_sha256':sha(__file__),'challenge_or_frozen_labels_used':False})
    status('READY','v2 seeded; native-positive validation reducer fixed without retraining')
    from fast_cascade.reporting import report
    report()
    print('Seeded',len(cached('VALIDATION','LAYA')),'unchanged native validation predictions;',len(cached('VALIDATION','FULL')),'identical full-Qwen references')
if __name__=='__main__':main()
