"""Resumable, validation-selected experiment. Frozen truth is scoring-only."""
import copy,json,time,uuid,os,subprocess,traceback
from dataclasses import asdict
from collections import defaultdict,Counter
from fast_cascade.protocol import *
from qwen_domain.protocol import load_inputs,load_training,freeze_baseline
from fast_cascade.routing import Policy,candidates,CRITICAL,assess
from semantic_pipeline.schema import PREDICATES
from semantic_pipeline.reconcile import llm_factors
from semantic_pipeline.pipeline import resolve_deadline
from semantic_pipeline.decision import decide
from fast_cascade.pipeline import Pipeline,confidence_features
from fast_cascade.evaluation import summary,preferences,oracles,values,actual_transitions
from qwen_domain.confidence import CorrectnessCalibrator,calibration_metrics
from cascade.resources import Sampler

RUN_ID='laya-first-v1'

def sampled(data,n):
    """Input-only round robin across family/language/length; stable seeded ordering."""
    strata=defaultdict(list)
    for r in data:
        key=(r.get('generation_family',r.get('duplicate_group',r.get('event_type','public'))),r.get('language','en'),min(4,len(r['text'])//2000))
        strata[key].append(r)
    for group in strata.values():group.sort(key=lambda r:digest('laya-first-42:'+r['id']))
    result=[]
    while len(result)<n and any(strata.values()):
        for key in sorted(strata):
            if strata[key] and len(result)<n:result.append(strata[key].pop())
    return result

def calibration_metadata(data):
    """Reproduce the published group-only fold assignment without reading labels."""
    groups=defaultdict(list)
    for r in data:groups[r['duplicate_group']].append(r)
    fit=evaln=0;out=[]
    for _,rs in sorted(groups.items(),key=lambda x:(-len(x[1]),x[0])):
        fold='FIT' if fit/.7<=evaln/.3 else 'EVALUATION'
        out.extend({**r,'calibration_fold':fold} for r in rs)
        if fold=='FIT':fit+=len(rs)
        else:evaln+=len(rs)
    return out

def prepare():
    frozen=STUDY/'PROTOCOL.json'
    if frozen.exists():verify();return read(frozen)
    freeze_baseline();m=read(CORPUS/'MANIFEST.json');selected={}
    for split,n in [('VALIDATION',80),('SYNTHETIC_FROZEN_TEST',80),('ADVERSARIAL_TEST',24),('OOD_TEST',24)]:
        pool=load_inputs(CORPUS/'MANIFEST.json',split)
        if split in ('VALIDATION','SYNTHETIC_FROZEN_TEST'):pool=[r for r in pool if r['language']=='en']
        selected[split]=sampled(pool,n)
    cal=calibration_metadata(load_inputs(CORPUS/'MANIFEST.json','CALIBRATION'))
    selected['CALIBRATION']=sampled([r for r in cal if r['language']=='en' and r['calibration_fold']=='FIT'],100)+sampled([r for r in cal if r['language']=='en' and r['calibration_fold']=='EVALUATION'],60)
    challenge=read(ROOT/'data/experiments/local-llm-v1/challenge.json')
    selected['CHALLENGE']=[{k:r[k] for k in ['id','text','reference_date']} for r in challenge]
    public=rows(ROOT/'data/normalised/public-lsh-v1.jsonl');selected['THROUGHPUT_1000']=sampled(public,1000);selected['THROUGHPUT_100']=selected['THROUGHPUT_1000'][:100]
    for split,data in selected.items():
        for r in data:
            if any(k in r for k in ('expected','fact_specification','evidence_truth')):raise ValueError('Inference sample contains labels')
        target=STUDY/'inputs'/f'{split}.json'
        if target.exists():
            if read(target)!=data:raise ValueError('Existing sample differs; create a new experiment version')
        else:write(target,data)
    source={str(p.relative_to(ROOT)):sha(p) for base in ['fast_cascade'] for p in (ROOT/base).glob('*.py')}
    for p in ['qwen_domain/constrained.py','qwen_domain/confidence.py','cascade/aggregation.py','cascade/proxy_semantic_common_v1.txt','data/experiments/cascade-v2/LLM-CONFIGS-v3.json','data/experiments/local-llm-v1/challenge.json','data/experiments/qwen-domain-v1/QWEN_DIRECT_PRE_DOMAIN_TRAINING.json']:source[p]=sha(ROOT/p)
    for p in ['qwen_domain/predicate_prompt_v2.txt','hybrid/semantics.py','semantic_pipeline/models.py','semantic_pipeline/schema.py','semantic_pipeline/pipeline.py','semantic_pipeline/decision.py','semantic_pipeline/fallback.py','semantic_pipeline/reconcile.py','semantic_pipeline/evidence.py','classifier/laya_classifier.py','classifier/preprocessing.py','classifier/deadlines.py','cascade/fallback.py','data/experiments/cascade-v2/AGGREGATION-SELECTION-v2.json','data/models/supplied-synthetic-v1/encoder-4ep/voting-config.json']:
        source[p]=sha(ROOT/p)
    weights={name:sha(ROOT/name) for name in ['data/models/laya/multilingual/model.safetensors','data/models/supplied-synthetic-v1/encoder-4ep/model.safetensors','data/models/narrow-v1/model.safetensors']}
    protocol={'version':VERSION,'created_at':now(),'seed':42,'sources':source,'weights':weights,'qwen_model':read(ROOT/'data/experiments/cascade-v2/LLM-CONFIGS-v3.json')['QWEN_DIRECT'],'corpus_manifest_sha256':sha(CORPUS/'MANIFEST.json'),'samples':{s:{'n':len(rs),'sha256':sha(STUDY/'inputs'/f'{s}.json'),'ids':[r['id'] for r in rs]} for s,rs in selected.items()},
        'policies':[asdict(p) for p in candidates()],'selection':{'max_assertion_loss_vs_full':.01,'max_additional_critical_false_negatives':0,'prefer':'Passing policies: minimum sum of measured component service times. If none pass, explicitly record NO_VALIDATED_CASCADE; best-quality experimental policy stays review-only.'},
        'calibration':'Fixed logistic C=.1; CALIBRATION FIT100/EVALUATION60, group isolated; min10 fit errors,5 evaluation errors,ECE<=.10; otherwise null. No threshold fit on challenge.',
        'reference':'QWEN_DIRECT_EVERYWHERE; exact historical output reuse allowed only for identical source/reference/model/prompt request. Reuse is never actual pipeline throughput.',
        'disagreement':'No automatic larger-model preference. Validation support>=10,win>=.9,critical damage=0; else review.',
        'training':'NONE; unchanged Laya/Qwen checkpoints','automation_enabled':False,'customer_accuracy':None,'previous_domain_study_state':read(ROOT/'data/experiments/qwen-domain-v1/LIVE-STATUS.json'),
        'benchmark_scope':'Controlled input-stratified subsets of synthetic corpus, unchanged authored challenge; actual public 100/1000 throughput workloads are unlabelled.'}
    write(frozen,protocol);return protocol

def verify():
    p=read(STUDY/'PROTOCOL.json')
    for name,h in p['sources'].items():
        if sha(ROOT/name)!=h:raise ValueError('Frozen experimental source changed: '+name+'; create a new experiment version')
    for name,h in p['weights'].items():
        if sha(ROOT/name)!=h:raise ValueError('Frozen checkpoint changed: '+name)
    if sha(CORPUS/'MANIFEST.json')!=p['corpus_manifest_sha256']:raise ValueError('Corpus manifest changed')
    for s,d in p['samples'].items():
        if sha(STUDY/'inputs'/f'{s}.json')!=d['sha256']:raise ValueError('Sample changed '+s)

def inputs(split):return read(STUDY/'inputs'/f'{split}.json')
def label_cases(split):
    if split=='CHALLENGE':
        if not (STUDY/'SELECTION.json').exists():raise ValueError('Frozen challenge truth cannot enter routing selection')
        from semantic_pipeline.metrics import truth
        return [{**r,'expected':truth(r['expected'])} for r in read(ROOT/'data/experiments/local-llm-v1/challenge.json')]
    if split not in ('VALIDATION','CALIBRATION') and not (STUDY/'SELECTION.json').exists():raise ValueError('Protected truth is scoring-only after selection freeze')
    m=read(CORPUS/'MANIFEST.json');entry=m['splits'][split];p=CORPUS/entry['labels']
    if sha(p)!=entry['labels_sha256']:raise ValueError('Protected label hash changed')
    ids={r['id'] for r in inputs(split)}
    return [r for r in rows(p) if r['id'] in ids]

def path(split,model):return STUDY/'predictions'/f'{split}-{model}.jsonl'
def cached(split,model):return rows(path(split,model)) if path(split,model).exists() else []
def save(split,model,c,result,**extra):
    append(path(split,model),{'run_id':RUN_ID,'id':c['id'],'input_hash':digest(c['text']),'split':split,'model':model,'timestamp':now(),'result':result,**extra})

def collect_laya(split,model,*,base=False):
    name='BASE_LAYA' if base else 'LAYA';done={r['id'] for r in cached(split,name)};pending=[r for r in inputs(split) if r['id'] not in done]
    for start in range(0,len(pending),8):
        check_stop();batch=pending[start:start+8];status('RUNNING',split+'_'+name,next_id=batch[0]['id'])
        out=model.analyse_batch([r['text'] for r in batch])
        for c,result in zip(batch,out):result['input_hash']=digest(c['text']);save(split,name,c,result)
    return cached(split,name)

def reference_result(c,raw):
    text=c['text'];preds=llm_factors(raw);preds={k:preds.get(k,{'value':'UNCERTAIN' if k=='votability' else 'UNKNOWN','evidence':[],'source':'INVALID_LLM_SCHEMA'}) for k in PREDICATES}
    ref=c.get('evaluation_time') or (c.get('reference_date','2026-10-17')+'T12:00:00+00:00')
    deadline=resolve_deadline(text,{'parsed':None,'narrative':text},raw,ref)
    conflicts=['LLM_SCHEMA_FAILURE'] if not raw.get('valid') else list(raw['parsed'].get('ambiguities',[]))
    if deadline.get('conflict'):conflicts.append('DEADLINE_CONFLICT')
    decision=decide(preds,deadline,conflicts)
    return {'predicates':{**preds,'deadline_status':{'value':deadline['status'],'source':'DETERMINISTIC_RULES','evidence':[]}},'deadline':deadline,'decision':decision,'raw':raw,
        'latency_ms':raw['latency_ms'],'latency_scope':'MEASURED_FULL_QWEN_SERVICE; warm/cold request metadata retained','semantic_review_required':decision['classification']=='UNCERTAIN_MANUAL_REVIEW','full_qwen':raw,'automation_enabled':False}

def semantic_reference(c,raw,stage):
    deadline=resolve_deadline(c['text'],{'parsed':None,'narrative':c['text']},None,c.get('evaluation_time') or c.get('reference_date','2026-10-17')+'T12:00:00+00:00')
    preds=raw['predicates'];decision=decide(preds,deadline,['PASSAGE_CONFLICT'] if any(p.get('conflict') for p in preds.values()) else [])
    return {'predicates':{**preds,'deadline_status':{'value':deadline['status']}},'deadline':deadline,'decision':decision,'latency_ms':raw['latency_ms'],
        'semantic_review_required':decision['classification']=='UNCERTAIN_MANUAL_REVIEW','latency_scope':'MEASURED_'+stage+'_COMPONENT_NOT_PIPELINE','automation_enabled':False}

def old_reference(c):
    # Trust exact request/source identity, never just a matching record ID.
    from cascade.fallback import CommonFallback
    config=read(ROOT/'data/experiments/cascade-v2/LLM-CONFIGS-v3.json')['QWEN_DIRECT'];adapter=CommonFallback(config)
    pool=ROOT/'data/experiments/qwen-domain-v1/predictions/BASE_QWEN_DIRECT-VALIDATION.jsonl'
    options=[]
    if pool.exists():
        for r in rows(pool):
            if r['id']==c['id'] and r['input_hash']==digest(c['text']):options.append((r['result']['raw_model_result'],str(pool.relative_to(ROOT))))
    old=ROOT/'data/experiments/cascade-v2/challenge-D2.jsonl'
    if old.exists():
        for r in rows(old):
            if r['id']==c['id'] and r['text']==c['text']:options.append((r['result']['llm'],str(old.relative_to(ROOT))))
    for raw,origin in options:
        request=raw.get('request',{})
        if raw.get('model_digest')!=config['model_digest'] or raw.get('prompt_version')!=adapter.prompt_version:continue
        if request.get('model')!=config['model'] or request.get('think') is not False:continue
        # Exact request fingerprint verified by generating payload using the adapter's prompt helper.
        expected=adapter.request(c['text'],c['text'],{},None,'INDEPENDENT')
        if digest(request)!=digest(expected):continue
        return raw,origin
    return None,None

def collect_models(split,qwen):
    laya={r['id']:r['result'] for r in cached(split,'LAYA')};gdone={r['id'] for r in cached(split,'GEAR2')};fdone={r['id'] for r in cached(split,'FULL')}
    for c in inputs(split):
        check_stop()
        sampler=Sampler().start()
        try:
            collect_one(split,c,qwen,laya,gdone,fdone)
        finally:append(STUDY/'MODEL-RESOURCE-MEASUREMENTS.jsonl',{'split':split,'id':c['id'],'timestamp':now(),'resources':sampler.finish()})

def collect_one(split,c,qwen,laya,gdone,fdone):
        if c['id'] not in gdone:
            status('RUNNING',split+'_CONSTRAINED',next_id=c['id']);r=qwen.constrained(c['text'],list(PREDICATES),laya=laya[c['id']]);save(split,'GEAR2',c,r)
        if c['id'] not in fdone:
            status('RUNNING',split+'_QWEN_REFERENCE',next_id=c['id']);raw,origin=old_reference(c)
            if raw is None:raw=qwen.full(c['text'])
            save(split,'FULL',c,reference_result(c,raw),reused_from=origin)

def replay(split,policy,prefs=None,calibrator=None):
    l={r['id']:r['result'] for r in cached(split,'LAYA')};g={r['id']:r['result'] for r in cached(split,'GEAR2')};f={r['id']:r['result']['raw'] for r in cached(split,'FULL')}
    pipe=Pipeline(policy,preferences=prefs,calibrator=calibrator);out=[]
    for c in inputs(split):
        r=pipe.analyse(c['text'],language=c.get('language','en'),reference=c.get('evaluation_time') or c.get('reference_date','2026-10-17')+'T12:00:00+00:00',precomputed_laya=l[c['id']],precomputed_gear2=g[c['id']],precomputed_full=f[c['id']],replay=True)
        # Only selected predicates' measured service times are summed. This is a counterfactual estimate, not actual latency.
        r['latency_ms']=r['laya_service_ms']+sum(g[c['id']]['predicates'][k]['latency_ms']+sum(x['result']['latency_ms'] for x in g[c['id']]['predicates'][k].get('passage_scores',[])) for k in r['escalation']['gear2_requested'])+r['full_qwen_ms']
        out.append({'id':c['id'],'result':r})
    return out

def select():
    dest=STUDY/'SELECTION.json'
    if dest.exists():return read(dest)
    cases=label_cases('VALIDATION');full=cached('VALIDATION','FULL');l=cached('VALIDATION','LAYA');g=cached('VALIDATION','GEAR2')
    prefs={'gear2':preferences(cases,l,g),'full':preferences(cases,l,full)};baseline=summary(cases,full);tables=[]
    for p in candidates():
        rs=replay('VALIDATION',p,prefs);m=summary(cases,rs)
        m['passed_reference_gate']=m['assertion_correctness']>=baseline['assertion_correctness']-.01 and all(m['fields'][k]['positive_false_negatives']<=baseline['fields'][k]['positive_false_negatives'] for k in CRITICAL)
        tables.append({'policy':asdict(p),'metrics':m})
        for c,r in zip(inputs('VALIDATION'),rs):save('VALIDATION',p.name,c,r['result'])
    passed=[r for r in tables if r['metrics']['passed_reference_gate']]
    chosen=min(passed,key=lambda r:r['metrics']['median_latency_ms']) if passed else max(tables,key=lambda r:(r['metrics']['correct_assertions'],-r['metrics']['median_latency_ms']))
    by={c['id']:c for c in inputs('VALIDATION')}
    specialist=summary(cases,[{'id':r['id'],'result':semantic_reference(by[r['id']],r['result'],'LAYA')} for r in l])
    constrained=summary(cases,[{'id':r['id'],'result':semantic_reference(by[r['id']],r['result'],'CONSTRAINED')} for r in g])
    result={'created_at':now(),'selected_policy':chosen['policy'],'status':'VALIDATION_REFERENCE_GATE_PASSED_RESEARCH_ONLY' if passed else 'NO_VALIDATED_CASCADE','preferences':prefs,'model_identity':Pipeline(Policy(**chosen['policy']),preferences=prefs).identity,'laya':specialist,'constrained':constrained,
        'reference':baseline,'policies':tables,'scope':'VALIDATION only. Research policy does not authorize automation. No challenge/frozen truth used.'}
    write(dest,result);return result

def calibration(laya,qwen):
    selection=read(STUDY/'SELECTION.json');pipe=Pipeline(Policy(**selection['selected_policy']),laya=laya,qwen=qwen,preferences=selection['preferences'])
    done={r['id'] for r in cached('CALIBRATION','CASCADE')};ls={r['id']:r['result'] for r in collect_laya('CALIBRATION',laya)}
    for c in inputs('CALIBRATION'):
        if c['id'] in done:continue
        check_stop();status('RUNNING','CALIBRATION_CASCADE',next_id=c['id']);r=pipe.analyse(c['text'],language=c['language'],reference=c['evaluation_time'],precomputed_laya=ls[c['id']]);save('CALIBRATION','CASCADE',c,r)
    p=STUDY/'calibrator.joblib'
    if p.exists():return CorrectnessCalibrator.load(p,pipe.identity)
    truth={c['id']:c for c in label_cases('CALIBRATION')};records=[]
    for r in cached('CALIBRATION','CASCADE'):
        c=truth[r['id']]
        for k,co in r['result']['confidence'].items():records.append({'id':r['id'],'predicate':k,'split':'CALIBRATION','duplicate_group':c['duplicate_group'],'calibration_fold':c['calibration_fold'],'features':co['features'],'force_review':co['force_review'],'expected':c['expected'][k],'predicted':co['value'],'correct':co['value']==c['expected'][k]})
    cal=CorrectnessCalibrator(pipe.identity);report=cal.fit(records);cal.save(p);write(STUDY/'CALIBRATION.json',report)
    evaluated=[]
    for r in records:
        if r['calibration_fold']!='EVALUATION':continue
        probability=None if r['force_review'] else cal.predict(r['predicate'],r['features'],pipe.identity)
        evaluated.append({**r,'confidence':probability})
    coverage=[]
    for t in [.7,.8,.9,.95,.98]:
        accepted=[r for r in evaluated if r['confidence'] is not None and r['confidence']>=t]
        coverage.append({'threshold':t,'assertions':len(evaluated),'accepted':len(accepted),'coverage':len(accepted)/len(evaluated),'measured_correctness':sum(r['correct'] for r in accepted)/len(accepted) if accepted else None,'review_rate':1-len(accepted)/len(evaluated),'accepted_critical_false_negatives':sum(r['predicate'] in CRITICAL and r['expected'] in ('YES','VOTABLE') and not r['correct'] for r in accepted)})
    write(STUDY/'CONFIDENCE-COVERAGE.json',{'scope':'CALIBRATION EVALUATION only; threshold simulation, automation disabled','coverage':coverage,'records':evaluated})
    return cal

def evaluate(split,laya,qwen,calibrator):
    collect_laya(split,laya);collect_models(split,qwen)
    sel=read(STUDY/'SELECTION.json');rs=replay(split,Policy(**sel['selected_policy']),sel['preferences'],calibrator)
    # Persist every final blind prediction before opening protected answer rows.
    done={r['id'] for r in cached(split,'SELECTED_CASCADE')}
    for c,r in zip(inputs(split),rs):
        if c['id'] not in done:save(split,'SELECTED_CASCADE',c,r['result'])
    cases=label_cases(split)
    if not (STUDY/f'{split}-METRICS.json').exists():
        by={c['id']:c for c in inputs(split)}
        write(STUDY/f'{split}-METRICS.json',{'cascade':summary(cases,rs),'full_qwen':summary(cases,cached(split,'FULL')),
            'laya':summary(cases,[{'id':r['id'],'result':semantic_reference(by[r['id']],r['result'],'LAYA')} for r in cached(split,'LAYA')]),
            'constrained':summary(cases,[{'id':r['id'],'result':semantic_reference(by[r['id']],r['result'],'CONSTRAINED')} for r in cached(split,'GEAR2')]),
            'oracle':oracles(cases,cached(split,'LAYA'),cached(split,'GEAR2'),cached(split,'FULL')),
            'stage_transitions':actual_transitions(cases,rs)})
        errors=[];by_prediction={r['id']:r['result'] for r in rs}
        for c in cases:
            r=by_prediction[c['id']];observed=values(r)
            for k,v in c['expected'].items():
                if observed.get(k,'NOT_SUPPORTED')!=v:errors.append({'id':c['id'],'text':c['text'],'field':k,'truth':v,'predicted':observed.get(k,'NOT_SUPPORTED'),'native_laya':r['laya']['predicates'].get(k),'gear2':(r['gear2'] or {}).get('predicates',{}).get(k),'full_qwen_parsed':(r['full_qwen'] or {}).get('parsed'),'reconciliation':r['reconciliation'],'confidence':r['confidence'].get(k)})
        write(STUDY/f'{split}-ERRORS.json',errors)

def throughput(n,laya,qwen,calibrator):
    split=f'THROUGHPUT_{n}';selection=read(STUDY/'SELECTION.json');pipe=Pipeline(Policy(**selection['selected_policy']),laya=laya,qwen=qwen,preferences=selection['preferences'],calibrator=calibrator)
    target=STUDY/f'{split}-MEASUREMENT.json'
    if target.exists():return read(target)
    done={r['id'] for r in cached(split,'ACTUAL')};pending=[c for c in inputs(split) if c['id'] not in done];sampler=Sampler().start();start=time.perf_counter()
    segments=STUDY/f'{split}-SEGMENTS.jsonl'
    try:
        for off in range(0,len(pending),8):
            check_stop();batch=pending[off:off+8];batch_start=time.perf_counter();native=laya.analyse_batch([r['text'] for r in batch])
            for c,pred in zip(batch,native):
                check_stop();status('RUNNING',split,next_id=c['id']);pred['input_hash']=digest(c['text']);r=pipe.analyse(c['text'],language=c.get('language','en'),precomputed_laya=pred)
                r['completion_latency_from_batch_start_ms']=(time.perf_counter()-batch_start)*1000
                save(split,'ACTUAL',c,r)
                if n==100:
                    # Real public-notice traces become reviewable in the application,
                    # without changing its default architecture or old predictions.
                    from apps.api import store
                    from apps.api.fast_cascade_views import persist
                    with store.connect() as conn:
                        source=conn.execute('SELECT text FROM notices WHERE id=?',(c['id'],)).fetchone()
                    if source and source['text']==c['text']:persist(c['id'],c['text'],r)
    finally:append(segments,{'started_at':now(),'seconds':time.perf_counter()-start,'completed_new':len(cached(split,'ACTUAL'))-len(done),'resources':sampler.finish()})
    all_rows=cached(split,'ACTUAL');dur=sum(r['seconds'] for r in rows(segments));import numpy as np
    lat=[r['result']['laya_service_ms']+r['result']['latency_ms'] for r in all_rows];completion=[r['result']['completion_latency_from_batch_start_ms'] for r in all_rows]
    result={'n':len(all_rows),'total_measured_active_seconds':dur,'notices_per_second':len(all_rows)/dur,'notices_per_hour':len(all_rows)*3600/dur,'median_service_latency_ms':float(np.median(lat)),'p95_service_latency_ms':float(np.percentile(lat,95)),
        'median_completion_from_batch_start_ms':float(np.median(completion)),'p95_completion_from_batch_start_ms':float(np.percentile(completion,95)),
        'laya_notice_calls':len(all_rows),'constrained_notice_calls':sum(bool(r['result']['gear2']) for r in all_rows),'native_one_token_calls':sum(r['result']['gear2']['native_model_calls'] if r['result']['gear2'] else 0 for r in all_rows),
        'full_qwen_calls':sum(bool(r['result']['full_qwen']) for r in all_rows),'semantic_review_count':sum(r['result']['semantic_review_required'] for r in all_rows),'actual_manual_review_count':len(all_rows),
        'actual_full_qwen_model_invocations':sum(bool((r['result']['full_qwen'] or {}).get('invoked')) for r in all_rows),
        'any_qwen_notice_calls':sum(bool(r['result']['gear2'] or r['result']['full_qwen']) for r in all_rows),
        'laya_only_notice_count':sum(not r['result']['gear2'] and not r['result']['full_qwen'] for r in all_rows),
        'resolved_by':dict(Counter(r['result']['resolved_by'] for r in all_rows)),'population':'Unlabelled public filing excerpts; actual inference with no answer cache. Automatic prefix KV reuse permitted. No accuracy measured.','automation_enabled':False}
    write(target,result);return result

def run():
    from fast_cascade.laya import BatchedLaya
    from fast_cascade.models import SharedQwen
    from fast_cascade.benchmarks import batch_benchmark,native_probe
    from fast_cascade.reporting import report
    caffeinate=None
    try:
        prepare();verify();caffeinate=subprocess.Popen(['caffeinate','-i','-w',str(os.getpid())],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
        batch=batch_benchmark();laya=BatchedLaya(batch['selected_sdk_batch_size']);qwen=SharedQwen();status('RUNNING','TRAIN_NATIVE_CACHE_BENCHMARK');native_probe(qwen)
        collect_laya('VALIDATION',laya);report();collect_models('VALIDATION',qwen);select();report()
        cal=calibration(laya,qwen);report()
        operating=STUDY/'OPERATING-CONFIGURATION-FREEZE.json'
        if not operating.exists():write(operating,{'created_at':now(),'protocol_sha256':sha(STUDY/'PROTOCOL.json'),'selection_sha256':sha(STUDY/'SELECTION.json'),'calibrator_sha256':sha(STUDY/'calibrator.joblib'),'calibration_report_sha256':sha(STUDY/'CALIBRATION.json'),'model_identity':read(STUDY/'SELECTION.json')['model_identity'],'scope':'Frozen before protected evaluation; no challenge/test answers used for policy or calibration'})
        for split in ['SYNTHETIC_FROZEN_TEST','ADVERSARIAL_TEST','OOD_TEST','CHALLENGE']:evaluate(split,laya,qwen,cal);report()
        base=BatchedLaya(batch['selected_sdk_batch_size'],fine=False);collect_laya('CHALLENGE',base,base=True);del base
        for n in [100,1000]:throughput(n,laya,qwen,cal);report()
        status('COMPLETED','All measurements persisted');report()
    except (KeyboardInterrupt,InterruptedError):status('STOPPED_BY_USER','Completed rows preserved');report()
    except Exception as e:status('FAILED',type(e).__name__,error=str(e),traceback=traceback.format_exc());report();raise
    finally:
        if caffeinate is not None and caffeinate.poll() is None:caffeinate.terminate()
