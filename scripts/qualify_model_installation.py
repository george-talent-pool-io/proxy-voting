"""Explicit, local release execution/reload probe on the installation host.

This measures runtime compatibility, not classification accuracy or customer
automation permission. No downloads, training, prompts or labels are selected.
"""
import argparse
import hashlib
import json
import platform
import statistics
import time
from pathlib import Path

from training.framework import jobs, releases
from training.framework.bundle import write, jsonl, sha
from production.storage import digest

PROBE_VERSION='installation-model-probe-v1'
# Smoke inputs are deliberately separate from all accuracy benchmarks.
NOTICES=(
    'Installation probe. Holders may cast votes on the meeting resolutions. Registration for voting is mandatory.',
    'Installation probe. This automatic cash payment offers no vote to shareholders.',
    'Installation probe. Voting holders must provide a power of attorney. Their securities remain freely transferable.',
    'Installation probe. Participation may be possible; no usable meeting or voting instructions are provided.',
)


def semantic_signature(result):
    from semantic_pipeline.schema import PREDICATES
    return {'predicates':{k:result['predicates'][k]['value'] for k in PREDICATES},
            'deadline_status':result['deadline']['status'], 'decision':result['decision']['classification'],
            'conflicts':result['reconciliation']['conflicts'],
            'llm_schema_valid':(result.get('llm') or {}).get('valid')}


def preflight(root, *, allow_unsealed=False):
    manifest=releases.verify(root) if allow_unsealed else releases.verify_seal(root)[0]
    # Production's Linux admission policy is intentionally reused. A Docker
    # service smoke pass cannot stand in for this model admission/execution.
    if platform.system()=='Linux':
        from production.installation import inference_admission
        admission=inference_admission(root)
    else:
        admission={'scope':'Development-host probe; not Linux/CUDA deployment qualification'}
    return manifest,admission


def probe(release_id, output, *, reference, allow_unsealed=False, model_factory=None):
    from production.service import reference_time
    reference=reference_time(reference)
    out=Path(output);out.mkdir(parents=True,exist_ok=False)
    began=time.perf_counter();root=jobs.member('releases',release_id)
    manifest,admission=preflight(root,allow_unsealed=allow_unsealed)
    condition={'version':PROBE_VERSION,'probe_source_sha256':sha(__file__),
        'release_id':release_id,'release_identity':manifest['identity'],
        'source_hashes':manifest['sources'],'reference':reference,
        'input_hashes':[hashlib.sha256(t.encode()).hexdigest() for t in NOTICES],
        'platform':platform.platform(),'machine':platform.machine(),'python':platform.python_version(),
        'sealed':not allow_unsealed,'admission':admission,'automation_enabled':False,
        'customer_accuracy':None,'scope':'Installation model execution/reload only; not accuracy qualification'}
    write(out/'PLAN.json',condition)
    from training.framework.resources import model_resource
    from semantic_pipeline.evidence import verify_evidence
    import psutil
    predictions=[];loads=[];resources=[]
    with model_resource('installation-model-probe'):
        for repetition in range(2):
            if releases.verify(root)['identity']!=manifest['identity']:raise ValueError('Serving condition drift')
            before=time.perf_counter();model=(model_factory or releases.ReleaseModel)(root,sealed=not allow_unsealed)
            loads.append((time.perf_counter()-before)*1000)
            try:
                for i,text in enumerate(NOTICES):
                    before=time.perf_counter();r=model.analyse(text,use_iso=False,reference=reference)
                    for p in r['predicates'].values():
                        for e in p.get('evidence',[]):
                            if e.get('valid') and not verify_evidence(text,e['text'])['valid']:
                                raise ValueError('Evidence mismatch in actual installation output')
                    if r.get('execution_error') or ((r.get('llm') or {}).get('invoked') and not r['llm'].get('valid')):
                        raise ValueError('Installation neural output failed execution/schema validation')
                    predictions.append({'probe':i,'repetition':repetition,'text':text,'result':r,
                                        'request_ms':(time.perf_counter()-before)*1000})
                    resources.append(psutil.Process().memory_info().rss)
            finally:model.close()
    jsonl(out/'predictions.jsonl',predictions)
    stable=[semantic_signature(predictions[i]['result'])==semantic_signature(predictions[i+len(NOTICES)]['result']) for i in range(len(NOTICES))]
    times=[r['request_ms'] for r in predictions]
    exercised=set()
    for row in predictions:
        if row['result'].get('laya') is not None:exercised.add('laya')
        if (row['result'].get('llm') or {}).get('invoked'):exercised.add('llm')
    missing=set(manifest['models'])-exercised
    # Cold lazy stage loads are included in request times and shown separately.
    receipt={**condition,'semantic_reload_stable':all(stable),'stable_probes':sum(stable),'probes':len(stable),
        'runtime_execution_passed':not missing,'models_exercised':sorted(exercised),'configured_models_not_exercised':sorted(missing),
        'repeatability_passed':all(stable),'predictions_sha256':sha(out/'predictions.jsonl'),
        'elapsed_seconds':time.perf_counter()-began,'requests':len(predictions),
        'wrapper_load_ms':loads,'request_ms':{'median':statistics.median(times),'mean':statistics.mean(times),'min':min(times),'max':max(times)},
        'lazy_stage_loads':[r['result'].get('model_load_times',{}) for r in predictions],
        'sampled_max_process_rss_bytes':max(resources),
        'resources_scope':'After-request parent RSS; excludes child/runtime allocations and is not peak unified/GPU memory',
        'production_or_automation_certified':False}
    receipt['sha256']=digest(receipt);write(out/'receipt.json',receipt)
    return receipt


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--release',required=True);p.add_argument('--output',required=True)
    p.add_argument('--reference',required=True,help='Timezone-aware evaluation instant')
    p.add_argument('--allow-unsealed-research',action='store_true')
    a=p.parse_args()
    r=probe(a.release,a.output,reference=a.reference,allow_unsealed=a.allow_unsealed_research)
    print(json.dumps({'receipt':str(Path(a.output)/'receipt.json'),'runtime_execution_passed':r['runtime_execution_passed'],
                      'repeatability_passed':r['repeatability_passed'],'production_or_automation_certified':False}))
    if not r['runtime_execution_passed'] or not r['repeatability_passed']:raise SystemExit(2)
