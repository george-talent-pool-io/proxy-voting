"""Frozen indexed Qwen qualification, paired with the real Laya stage.

One actual independent Qwen inference per notice is shared across architectures.
Hybrid reconciliation uses that exact persisted native stage via a verified
read-through cache. Logical calls and physical generations are separate. Hybrid
replay service times are not presented as measured end-to-end latency.
"""
import copy
import hashlib
import json
import os
import time
from pathlib import Path
from production import confidence,operating
from production.qualification import predicate_feature,decision_feature
from semantic_pipeline.schema import PREDICATES
from semantic_pipeline.metrics import summarize
from training.framework import jobs,releases
from training.framework.bundle import write,sha,jsonl
from training.framework.resources import model_resource
from scripts.qualify_frozen_learning import lines
from scripts.run_reliability_programme import measure
from training.reliability.production_study import calibrate,risk

ROOT=Path('data/experiments/production-qualification-indexed-20261023')
DEVELOPMENT=Path('data/qualification-corpora/fresh-evidence-v1')
FROZEN=Path('data/qualification-corpora/fresh-evidence-v2-independent')
LOADED_SOURCE=Path(__file__).read_bytes()


def input_rows(role,pilot=False):
    corpus=FROZEN if role=='FROZEN_TEST' else DEVELOPMENT
    m=json.loads((corpus/'manifest.json').read_text());entry=m['files'][role];file=corpus/entry['inputs']
    if sha(file)!=entry['inputs_sha256']:raise ValueError('Input changed')
    rows=lines(file)
    return sorted(rows,key=lambda r:r['source_hash'])[:20] if pilot else rows


def truth(role,receipt):
    if sha(receipt.parent/'predictions.jsonl')!=json.loads(receipt.read_text())['sha256']:raise ValueError('Prediction drift')
    corpus=FROZEN if role=='FROZEN_TEST' else DEVELOPMENT
    m=json.loads((corpus/'manifest.json').read_text());entry=m['files'][role];file=corpus/entry['labels']
    if sha(file)!=entry['labels_sha256']:raise ValueError('Answer drift')
    return {r['id']:r for r in lines(file)}


def run():
    ROOT.mkdir(parents=True,exist_ok=False);(ROOT/'study-source.py').write_bytes(LOADED_SOURCE)
    refs={}
    for name,spec in [('PRIMARY',{'mode':'QWEN_ONLY'}),('HYBRID',{
        'mode':'LAYA_QWEN','laya_job':'reliable-voting-balanced-v1-head-isolated',
        'laya_inference':'WHOLE_NOTICE_WITH_PASSAGE_EVIDENCE','policy':{
            'name':'CONSERVATIVE_SUPPORTED','laya_score':.98,'laya_margin':.6,'critical_score':.995,
            'qwen_score':.98,'qwen_margin':.8,'allow_absence':True,'gear2':False}})]:
        root=jobs.member('releases','indexed-qualification-v1-'+name.lower())
        m=releases.prepare({**spec,'llm_seed':'qwen38-indexed-evidence-foundation-v1'},root)
        refs[name]={'path':str(root),'identity':m['identity']}
    sources=releases.source_files()
    write(ROOT/'MODEL_FREEZE.json',{'releases':refs,'runtime_sources':sources,
        'corpora':{str(p):sha(p/'manifest.json') for p in (DEVELOPMENT,FROZEN)},
        'source_sha256':sha(ROOT/'study-source.py'),'foundation_unchanged':True,
        'training_smoke_model_selected':False,'challenge_used_for_selection':False,
        'model_selection':'Twenty development validation notices: same semantic assertions, reduced generation cost; experimental only',
        'hybrid_native_generation_reused':True,'automation_enabled':False,'customer_accuracy':None})
    cached={}
    class NativeReadThrough:
        def __init__(self,*a):pass
        def analyse(self,text,**kwargs):
            if cached['text']!=text or cached['reference']!=kwargs['reference'] or kwargs.get('structured_context'):
                raise ValueError('Cached independent Qwen context mismatch')
            return copy.deepcopy(cached['stage'])
        def close(self):pass
    calibration={};points={};reports={}
    with model_resource('indexed-paired-qualification'):
        for role,pilot in [('VALIDATION',True),('CALIBRATION',False),('VALIDATION',False),('FROZEN_TEST',False)]:
            label='VALIDATION-PILOT' if pilot else role
            if role=='FROZEN_TEST':
                write(ROOT/'OPERATING_FREEZE.json',{'calibrators':{k:v['sha256'] for k,v in calibration.items()},
                    'points':{k:v['sha256'] for k,v in points.items()},'frozen_answers_opened':False,
                    'runtime_sources':sources,'automation_enabled':False})
            outputs={name:ROOT/(name+'-'+label) for name in refs}
            for out in outputs.values():out.mkdir()
            streams={k:(v/'predictions.jsonl').open('x') for k,v in outputs.items()}
            primary=releases.ReleaseModel(refs['PRIMARY']['path'],sealed=not pilot)
            hybrid=releases.ReleaseModel(refs['HYBRID']['path'],sealed=not pilot,llm_factory=NativeReadThrough)
            saved={k:[] for k in refs};began=time.perf_counter()
            try:
                for index,row in enumerate(input_rows(role,pilot)):
                    if releases.source_files()!=sources:raise ValueError('Frozen serving source changed')
                    before=time.perf_counter();a=primary.analyse(row['text'],use_iso=False,reference=row['evaluation_time'])
                    actual_ms=(time.perf_counter()-before)*1000
                    cached.update(text=row['text'],reference=row['evaluation_time'],stage=a['llm_stage'])
                    before=time.perf_counter();b=hybrid.analyse(row['text'],use_iso=False,reference=row['evaluation_time'])
                    replay_ms=(time.perf_counter()-before)*1000
                    b['native_stage_replay']={'source_architecture':'PRIMARY','stage_sha256':hashlib.sha256(json.dumps(a['llm_stage'],sort_keys=True).encode()).hexdigest(),
                        'physical_generations':0,'same_notice_and_context_verified':True,
                        'latency_scope':'Laya plus deterministic downstream replay; excludes generation time reused from PRIMARY'}
                    for name,r,ms in [('PRIMARY',a,actual_ms),('HYBRID',b,replay_ms)]:
                        item={**row,'result':r,'request_ms':ms};saved[name].append(item)
                        streams[name].write(json.dumps(item,ensure_ascii=False,allow_nan=False)+'\n');streams[name].flush();os.fsync(streams[name].fileno())
                    print(json.dumps({'phase':label,'done':index+1,'primary_seconds':round(actual_ms/1000,3),
                                      'hybrid_logical_llm':bool(b['llm'])}),flush=True)
            finally:
                primary.close();hybrid.close()
                for f in streams.values():f.close()
            # Both complete streams are durably saved before either key opens.
            for name,out in outputs.items():
                write(out/'PREDICTIONS_SAVED.json',{'count':len(saved[name]),'sha256':sha(out/'predictions.jsonl'),
                    'answers_opened':False,'paired_elapsed_seconds':time.perf_counter()-began,
                    'physical_qwen_generations_in_this_stream':len(saved[name]) if name=='PRIMARY' else 0,
                    'latency_scope':'Actual sequential primary requests including lazy cold stage loads' if name=='PRIMARY' else
                                    'Deterministic replay plus actual Laya; not an end-to-end hybrid latency benchmark'})
            t=truth(role,outputs['PRIMARY']/'PREDICTIONS_SAVED.json')
            for name,out in outputs.items():
                m=measure(saved[name],t);write(out/'metrics.json',m);reports[name+'-'+label]=m
                if pilot:
                    write(out/'evaluation.json',{'role':'VALIDATION','release_identity':refs[name]['identity'],'metrics':m,
                        'scope':'Twenty-case development selection/integration receipt; not customer qualification'})
                    releases.seal(refs[name]['path'],out)
                elif role=='CALIBRATION':
                    calibration[name]=calibrate(saved[name],t,refs[name]['identity'],out,
                        'INDEXED_PRIMARY_FINAL' if name=='PRIMARY' else 'INDEXED_ACTUAL_STAGE_HYBRID_FINAL')
                else:
                    rr=risk(saved[name],t,calibration[name],role);jsonl(out/'confidence.jsonl',rr)
                    if role=='VALIDATION':points[name]=operating.select(rr,identity=refs[name]['identity'],
                        calibrator_hash=calibration[name]['sha256'],output=out/'operating-point.json')
                    else:
                        write(out/'operating-evaluation.json',operating.evaluate(rr,points[name],identity=refs[name]['identity'],calibrator_hash=calibration[name]['sha256']))
                        write(out/'coverage-curve.json',[operating.summarize(rr,x) for x in (.7,.8,.9,.95,.98,.99)])
            print('ROLE_COMPLETE',label,flush=True)
    write(ROOT/'RESULT.json',{'releases':refs,'metrics':reports,'calibration_reports':{k:v['reports'] for k,v in calibration.items()},
        'points':points,'automation_enabled':False,'customer_accuracy':None})


if __name__=='__main__':run()
