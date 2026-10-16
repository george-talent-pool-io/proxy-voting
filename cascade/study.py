"""Resumable controlled study. Selection is validation-only; no training.
Historical source/predictions are never overwritten. Use the same staged directory.
"""
import copy,gc,hashlib,json,statistics,time,uuid,threading,concurrent.futures
from pathlib import Path
from collections import Counter
from semantic_pipeline.experiment import read,write,append,lines,sha,now
from semantic_pipeline.models import WholeLaya
from semantic_pipeline.pipeline import run,diagnostic
from semantic_pipeline.schema import PREDICATES
from semantic_pipeline.metrics import summarize,observed,truth,field_metrics
from semantic_pipeline.reconcile import llm_factors
from semantic_pipeline.routing import RoutingConfig
from cascade.fallback import CommonFallback
from cascade.aggregation import AggregationConfig
from cascade.models import EvidenceNarrow,CapableSpecialist
from cascade.routing import Policy,features
from cascade.pipeline import execute
from cascade.resources import Sampler
from evaluation.ae_scoring import project
ROOT=Path('data/experiments/cascade-v2');OLD=Path('data/experiments/local-llm-v1')
LOCK=threading.Lock()

def hashtext(s):return hashlib.sha256(s.encode()).hexdigest()
def save_once(path,value):
    if not path.exists():write(path,value)
    return read(path)

def verify_baseline():
    baseline=read(ROOT/'PRE_AGGREGATION_FIX_BASELINE.json')
    for p,h in baseline['files'].items():assert sha(p)==h,p
    return baseline

def freeze_core():
    verify_baseline()
    names=list(Path('cascade').glob('*.py'))+list(Path('cascade').glob('*.txt'))
    names += [ROOT/n for n in ['DESIGN.json','LLM-CONFIGS-v3.json','AGGREGATION-SELECTION-v2.json','routing-validation-80.json','LLM-validation-40.json','RUNTIME-CONDITION.json']]
    return save_once(ROOT/'COMMON-CONDITION-FREEZE.json',{'created_at':now(),'files':{str(p):sha(p) for p in names},'no_challenge_tuning':True,'automation_enabled':False})

def verify_core():
    f=read(ROOT/'COMMON-CONDITION-FREEZE.json')
    for p,h in f['files'].items():assert sha(p)==h,p
    verify_baseline();return f

def unload_other(model,config):
    client=CommonFallback(config)
    for item in client.http('/api/ps')['models']:
        if item['name']!=model:client.http('/api/generate',{'model':item['name'],'keep_alive':0})

def canonical_specialist(p):
    return {k:{q:v for q,v in x.items() if q in ('value','scores','confidence','margin')} for k,x in p['predicates'].items()}

def benchmark_condition(dataset,condition,model_name,items,*,specialist_kind='WHOLE',policy=None,use_parser=False):
    verify_core();cfg=read(ROOT/'LLM-CONFIGS-v3.json')[model_name];unload_other(cfg['model'],cfg)
    fallback=CommonFallback(cfg);path=ROOT/f'{dataset}-{condition}.jsonl';saved={r['id']:r for r in lines(path)}
    for row in items:
        if row['id'] in saved:assert saved[row['id']]['input_hash']==hashtext(row['text'])
    if len(saved)==len(items):return list(saved.values())
    manifest_path=ROOT/f'{dataset}-{condition}-MANIFEST.json'
    manifest=save_once(manifest_path,{'run_id':str(uuid.uuid4()),'created_at':now(),'dataset':dataset,'condition':condition,'model_config':cfg,
        'common_freeze_sha256':sha(ROOT/'COMMON-CONDITION-FREEZE.json'),'input_hash':hashtext(json.dumps([(r['id'],hashtext(r['text'])) for r in items],sort_keys=True)),
        'policy':policy,'specialist_kind':specialist_kind,'use_parser':use_parser,'concurrency':1,'seed':42,'no_training':True})
    warm=fallback.analyse(original_text='Shareholders may vote at the meeting. No power of attorney is required.',narrative_text='Shareholders may vote at the meeting. No power of attorney is required.',structured_facts={},mode='INDEPENDENT')
    append(ROOT/'COLD-WARMUP-CALLS.jsonl',{'dataset':dataset,'condition':condition,'timestamp':now(),'result':warm,'excluded_from_warm_benchmark':True})
    # Whole-notice context is fixed across C1/C2/C3. Fresh inference is timed and
    # checked, then the canonical identical diagnostic is supplied to each LLM.
    base_index={r['id']:r for r in lines(ROOT/'validation-specialists.jsonl')}
    if dataset!='validation':base_index={r['id']:r for r in lines(ROOT/f'{dataset}-SPECIALISTS.jsonl')}
    model=None
    if not condition.startswith('D'):
        model=WholeLaya(fine=True) if specialist_kind=='WHOLE' else CapableSpecialist(AggregationConfig(**read(ROOT/'AGGREGATION-SELECTION-v2.json')['selected']['config'])) if specialist_kind=='CAPABLE' else EvidenceNarrow(AggregationConfig(**read(ROOT/'AGGREGATION-SELECTION-v2.json')['selected']['config']))
    model_load_finished=now()
    def one(row):
        started=time.perf_counter();text=row['text'];laya=None
        if condition.startswith('D'):result=run(text,'D',fallback=fallback)
        else:
            # MPS inference is serialised; native Laya is not invoked concurrently.
            with LOCK:
                if use_parser:
                    from semantic_pipeline.pipeline import prepare
                    import re
                    hint=bool(re.search(r'(?:^|[\r\n]):\d{2}[A-Z]?:',text) or '{2:' in text)
                    narrative=prepare(text,hint)['narrative']
                else:narrative=text
                laya=model.analyse(narrative)
            if specialist_kind=='WHOLE':
                canonical=base_index[row['id']]['whole']
                assert canonical_specialist(laya)==canonical_specialist(canonical),'Native Laya changed; do not compare different specialist diagnostics'
                laya={**copy.deepcopy(canonical),'latency_ms':laya['latency_ms']}
                result=run(text,'C',fallback=fallback,precomputed_laya=laya,routing=RoutingConfig(max_chars=1))
            else:
                result=execute(text,precomputed=laya,fallback=fallback,policy=Policy(**policy),use_parser=use_parser)
        result['latencies']['actual_pipeline_wall_ms']=result['latencies']['total_ms']
        result['latencies']['total_ms']=(time.perf_counter()-started)*1000
        result['latencies']['timing_scope']='Fresh end-to-end warmed wall time; one notice at a time; fresh native Laya inference and local generation'
        result['condition']=condition
        rowout={'id':row['id'],'text':text,'expected':row['expected'],'input_hash':hashtext(text),'result':result,
            'timestamp':now(),'run_id':manifest['run_id'],'condition':condition,'model_config':cfg,
            'common_freeze_sha256':sha(ROOT/'COMMON-CONDITION-FREEZE.json'),'source_type':row.get('source_type',dataset)}
        if laya is not None:rowout['specialist_diagnostic_hash']=hashtext(json.dumps(diagnostic(laya),sort_keys=True))
        return rowout
    pending=[r for r in items if r['id'] not in saved]
    sampler=Sampler().start()
    with concurrent.futures.ThreadPoolExecutor(max_workers=1) as pool:
        jobs={pool.submit(one,row):row for row in pending}
        for job in concurrent.futures.as_completed(jobs):
            row=job.result();append(path,row);saved[row['id']]=row
            llm=row['result'].get('llm')
            print(dataset,condition,row['id'],'LLM',bool(llm and llm.get('invoked')),'valid',llm.get('valid') if llm else None,'ms',round(row['result']['latencies']['total_ms']),flush=True)
    resource=sampler.finish();resource['runtime_model_allocation']=fallback.http('/api/ps')
    append(ROOT/'RESOURCE-MEASUREMENTS.jsonl',{'dataset':dataset,'condition':condition,'timestamp':now(),'resource':resource})
    del model;gc.collect()
    import torch
    if torch.backends.mps.is_available():torch.mps.empty_cache()
    verify_core();return [saved[r['id']] for r in items]

def validation_common():
    items=read(ROOT/'LLM-validation-40.json')
    for model,suffix in [('GLM','1'),('QWEN_DIRECT','2'),('QWEN_THINKING','3')]:
        for prefix in ('D','C'):benchmark_condition('validation',prefix+suffix,model,items)

def model_metrics(rows):
    pairs={};schema=Counter();evidence=Counter();times=[]
    for row in rows:
        r=row['result'];llm=r.get('llm');gold=truth(row['expected']);facts=llm_factors(llm)
        handling=(llm or {}).get('schema_handling',{})
        for k,v in handling.items():schema[k]+=int(v)
        if llm:
            times.append(llm['latency_ms'])
            if llm.get('valid'):
                for k in PREDICATES:
                    qs=llm['evidence_validation']['predicates'][k];evidence['quotes_supplied']+=len(qs);evidence['exact_matches']+=sum(q['valid'] for q in qs)
                    evidence['invalid_quotes']+=sum(not q['valid'] for q in qs)
                    evidence['missing_positive_evidence']+=llm['parsed'][k] in ('YES','VOTABLE','NOT_VOTABLE') and not any(q['valid'] for q in qs)
        for key in PREDICATES:
            if key not in gold:continue
            pairs.setdefault(key,([],[]));pairs[key][0].append(gold[key]);pairs[key][1].append(facts.get(key,{}).get('value','NOT_SUPPORTED'))
    fields={k:field_metrics(y,p,'VOTABLE' if k=='votability' else 'YES') for k,(y,p) in pairs.items()}
    return {'fields':fields,'schema':dict(schema),'evidence':dict(evidence),'assertions':sum(m['n'] for m in fields.values()),'correct':sum(m['correct'] for m in fields.values()),
        'median_llm_ms':statistics.median(times),'schema_success_rate':sum((r['result'].get('llm') or {}).get('valid',False) for r in rows)/len(rows),
        'critical_positive_recall_mean':statistics.mean(fields[k]['positive_recall'] for k in ('votability','share_blocking','poa_required') if fields[k]['positive_recall'] is not None)}

def repeatability():
    cfgs=read(ROOT/'LLM-CONFIGS-v3.json');ids=['CV-001','CV-066','CV-074'];path=ROOT/'MODEL-REPEATABILITY.jsonl';saved={(r['model'],r['id'],r['repeat']):r for r in lines(path)}
    for model,suffix in [('GLM','1'),('QWEN_DIRECT','2'),('QWEN_THINKING','3')]:
        cfg=cfgs[model];unload_other(cfg['model'],cfg);client=CommonFallback(cfg)
        originals={r['id']:r for r in lines(ROOT/f'validation-D{suffix}.jsonl')}
        for ident in ids:
            old=originals[ident]
            for repeat in (1,2):
                if (model,ident,repeat) in saved:continue
                source=old['text'];result=client.analyse(original_text=source,narrative_text=source,structured_facts={},mode='INDEPENDENT')
                labels=lambda r:{k:r['parsed'][k] for k in PREDICATES} if r.get('valid') else None
                entry={'model':model,'id':ident,'repeat':repeat,'result':result,'labels_identical_to_first':bool(result.get('valid') and old['result']['llm'].get('valid') and labels(result)==labels(old['result']['llm'])),
                    'parsed_identical_to_first':result.get('parsed')==old['result']['llm'].get('parsed'),'timestamp':now()}
                append(path,entry);print('Repeatability',model,ident,repeat,result['valid'],entry['labels_identical_to_first'],flush=True)

def select_model():
    report={};reps=lines(ROOT/'MODEL-REPEATABILITY.jsonl')
    for model,suffix in [('GLM','1'),('QWEN_DIRECT','2'),('QWEN_THINKING','3')]:
        rows=lines(ROOT/f'validation-C{suffix}.jsonl')+lines(ROOT/f'validation-D{suffix}.jsonl');metrics=model_metrics(rows)
        relevant=[r for r in reps if r['model']==model];metrics['label_repeatability']=sum(r['labels_identical_to_first'] for r in relevant)/len(relevant)
        report[model]=metrics
    def rank(k):
        m=report[k];ev=m['evidence'];return (m['schema_success_rate'],m['critical_positive_recall_mean'],m['correct']/m['assertions'],ev.get('exact_matches',0)/max(1,ev.get('quotes_supplied',0)),m['label_repeatability'],-m['median_llm_ms'])
    selected=max(report,key=rank)
    write(ROOT/'PRIMARY-MODEL-SELECTION.json',{'created_at':now(),'selected':selected,'validation_only':True,'metrics':report,
        'ranking':'schema success, mean votability/blocking/POA affirmative recall, semantic assertion agreement, exact-evidence ratio, label repeatability, latency; lexicographic predeclared priorities',
        'no_challenge_used':True,'automation_enabled':False})
    print('PRIMARY_MODEL',selected,flush=True);return selected

def routing_validation():
    selected=read(ROOT/'PRIMARY-MODEL-SELECTION.json')['selected'];items=read(ROOT/'routing-validation-80.json')
    benchmark_condition('routing-validation','FALLBACK_ALWAYS',selected,items,specialist_kind='CAPABLE',policy={'name':'ALWAYS'})
    # Never count truth as a routing feature. It exists only in this diagnostic label column.
    existing={(r['id'],r['predicate']) for r in lines(ROOT/'ROUTING-ASSERTION-DATASET.jsonl')}
    for row in lines(ROOT/'routing-validation-FALLBACK_ALWAYS.jsonl'):
        gold=truth(row['expected']);before=row['result']['laya']['predicates']
        for f in features(row['text'],row['result']['laya']):
            if (row['id'],f['predicate']) not in existing:append(ROOT/'ROUTING-ASSERTION-DATASET.jsonl',{'id':row['id'],**f,'LAYA_CORRECT':before[f['predicate']]['value']==gold[f['predicate']],'truth_for_analysis_only':gold[f['predicate']]})

def select_routing():
    data=lines(ROOT/'routing-validation-FALLBACK_ALWAYS.jsonl');policies=[Policy(name='ALWAYS')]
    for name in ('CONSERVATIVE','MODERATE','AGGRESSIVE'):
        for score in (.7,.9,.98,.995):
            for margin in (.1,.4,.8):policies.append(Policy(name=name,min_score=score,min_margin=margin,require_positive_evidence=name!='AGGRESSIVE',escalate_critical_positive=name=='CONSERVATIVE',escalate_unknown=name!='AGGRESSIVE'))
    from dataclasses import asdict
    candidates=[]
    for p in policies:
        rs=[];calls=0;semcorrect=0;misses=Counter();repair=damage=0
        for row in data:
            old=row['result'];r=execute(row['text'],precomputed=old['laya'],policy=p,precomputed_llm=old['llm'])
            r['latencies']['total_ms']=old['laya']['latency_ms']+(old['llm']['latency_ms'] if r['llm'] else 0)
            rs.append({**row,'result':r});calls+=bool(r.get('llm'));a=observed({**old,'reconciliation':{'predicates':old['laya']['predicates']}});b=observed(r)
            for k,v in truth(row['expected']).items():
                if k not in PREDICATES:continue
                semcorrect+=b[k]==v;positive='VOTABLE' if k=='votability' else 'YES'
                misses[k]+=v==positive and b[k]!=positive
                repair+=a.get(k)!=v and b[k]==v;damage+=a.get(k)==v and b[k]!=v
        metrics=summarize(rs)
        candidates.append({'policy':asdict(p),'cases':len(rs),'semantic_assertions':len(rs)*9,'semantic_correct':semcorrect,'semantic_agreement':semcorrect/(len(rs)*9),
            'llm_invocations':calls,'llm_call_rate':calls/len(rs),'laya_only_coverage':1-calls/len(rs),'positive_misses':dict(misses),
            'semantic_repairs':repair,'semantic_damage':damage,'review_rate':1.0,'uncertain_status_count':metrics['uncertain_final_status_count'],
            'median_component_latency_estimate_ms':metrics['median_latency_ms'],'fields':metrics['fields']})
    always=candidates[0]
    eligible=[r for r in candidates if r['semantic_agreement']>=always['semantic_agreement']-.01 and all(r['positive_misses'].get(k,0)<=always['positive_misses'].get(k,0) for k in PREDICATES)]
    chosen=min(eligible,key=lambda m:(m['llm_call_rate'],-m['semantic_agreement'],m['median_component_latency_estimate_ms']))
    write(ROOT/'ROUTING-SELECTION.json',{'created_at':now(),'selected':chosen,'always':always,'candidates':candidates,
        'selection':'Minimum calls within 1 percentage point semantic agreement of always-fallback and no additional affirmative misses for any labelled semantic predicate. Validation only. No target call percentage.',
        'customer_quality_gate':False,'latency_scope':'Validation policy estimates sum recorded fresh component times; final selected cascade is timed with fresh inference.',
        'limitations':'80 AI-authored synthetic examples; no production precision or calibrated risk estimate.'})
    print('ROUTING_SELECTED',chosen['policy'],chosen['llm_call_rate'],chosen['semantic_agreement'],flush=True)

def freeze_final():
    verify_core();write(ROOT/'FINAL-SELECTION-FREEZE.json',{'created_at':now(),'common_freeze_sha256':sha(ROOT/'COMMON-CONDITION-FREEZE.json'),
        'primary_model':read(ROOT/'PRIMARY-MODEL-SELECTION.json'),'routing':read(ROOT/'ROUTING-SELECTION.json')['selected'],
        'selection_files':{str(ROOT/n):sha(ROOT/n) for n in ['PRIMARY-MODEL-SELECTION.json','ROUTING-SELECTION.json']},'no_training':True,'automation_enabled':False})

def evaluation_specialists():
    verify_core();assert (ROOT/'FINAL-SELECTION-FREEZE.json').exists()
    whole=WholeLaya(fine=True);narrow=EvidenceNarrow(AggregationConfig(**read(ROOT/'AGGREGATION-SELECTION-v2.json')['selected']['config']))
    for dataset,name in [('challenge','challenge.json'),('complete','complete-benchmark.json')]:
        path=ROOT/f'{dataset}-SPECIALISTS.jsonl';saved={r['id']:r for r in lines(path)}
        for row in read(OLD/name):
            if row['id'] in saved:continue
            result={**row,'input_hash':hashtext(row['text']),'whole':whole.analyse(row['text']),'narrow':narrow.base.analyse(row['text'])}
            result['fixed_narrow']=EvidenceNarrow.project(row['text'],result['narrow'],narrow.config)
            result['capable']=CapableSpecialist.combine(result['whole'],result['fixed_narrow']);append(path,result)
    del whole,narrow;gc.collect()

def legacy_reruns():
    for fine,arm in [(False,'A'),(True,'B')]:
        model=WholeLaya(fine=fine)
        for dataset,name in [('challenge','challenge.json'),('complete','complete-benchmark.json')]:
            path=ROOT/f'{dataset}-{arm}.jsonl';saved={r['id'] for r in lines(path)}
            manifest=save_once(ROOT/f'{dataset}-{arm}-MANIFEST.json',{'run_id':str(uuid.uuid4()),'created_at':now(),'architecture':arm,'checkpoint':model.checkpoint,'condition':'UNCHANGED_LEGACY_RERUN','common_freeze_sha256':sha(ROOT/'COMMON-CONDITION-FREEZE.json')})
            for row in read(OLD/name):
                if row['id'] in saved:continue
                started=time.perf_counter();r=run(row['text'],arm,laya_model=model)
                r['latencies']['total_ms']=(time.perf_counter()-started)*1000
                append(path,{**row,'input_hash':hashtext(row['text']),'result':r,'run_id':manifest['run_id'],'timestamp':now()})
        del model;gc.collect()
        import torch
        if torch.backends.mps.is_available():torch.mps.empty_cache()

def evaluation_common():
    for model,suffix in [('GLM','1'),('QWEN_DIRECT','2'),('QWEN_THINKING','3')]:
        for dataset,name in [('challenge','challenge.json'),('complete','complete-benchmark.json')]:
            items=read(OLD/name)
            for prefix in ('D','C'):benchmark_condition(dataset,prefix+suffix,model,items)

def evaluation_selected():
    selected=read(ROOT/'PRIMARY-MODEL-SELECTION.json')['selected'];policy=read(ROOT/'ROUTING-SELECTION.json')['selected']['policy']
    for dataset,name in [('challenge','challenge.json'),('complete','complete-benchmark.json')]:
        items=read(OLD/name)
        for condition,use_parser in [('C_SELECTIVE',False),('E_SELECTIVE',True)]:
            benchmark_condition(dataset,condition,selected,items,specialist_kind='CAPABLE',policy=policy,use_parser=use_parser)
        # Aggregation-only narrow E retains its old votability head for isolation.
        benchmark_condition(dataset,'E_AGGREGATION_ONLY',selected,items,specialist_kind='NARROW',policy=policy,use_parser=True)
    # Commit every result before report generation; no historical key is reopened.
    write(ROOT/'PREDICTION-COMMIT.json',{'created_at':now(),'files':{str(p):sha(p) for p in ROOT.glob('*.jsonl')},'automation_enabled':False})

def main():
    import sys
    stages={'freeze':freeze_core,'validate':validation_common,'repeat':repeatability,'select-model':select_model,
        'routing-validation':routing_validation,'select-routing':select_routing,'freeze-final':freeze_final,
        'evaluation-specialists':evaluation_specialists,'legacy':legacy_reruns,'evaluate-common':evaluation_common,'evaluate-selected':evaluation_selected}
    stages[sys.argv[1]]()
if __name__=='__main__':main()
