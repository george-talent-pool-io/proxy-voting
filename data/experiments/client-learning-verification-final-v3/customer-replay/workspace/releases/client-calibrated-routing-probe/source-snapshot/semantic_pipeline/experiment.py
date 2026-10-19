"""Staged, resumable A–E experiment. No training and no challenge-driven selection.
Usage: python -m semantic_pipeline.experiment prepare|validate|freeze|evaluate|report|verify
"""
import argparse
import copy
import hashlib
import json
import math
import os
import statistics
import time
import uuid
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from semantic_pipeline.fallback import OllamaFallback, digest
from semantic_pipeline.models import WholeLaya, NarrowAdapter
from semantic_pipeline.pipeline import run, diagnostic
from semantic_pipeline.routing import RoutingConfig, escalate
from semantic_pipeline.metrics import summarize, observed, truth

ROOT=Path(os.environ.get('LAYA_AE_EXPERIMENT','data/experiments/local-llm-v1'))
CHALLENGE=Path('tests/fixtures/semantic.json')
CHALLENGE_SHA='0e2f5d991a33deed25f8e9a33682185071c5ff35afd2df9179c1f8565dd17649'

def now():return datetime.now(timezone.utc).isoformat()
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def write(p,value):
    with Path(p).open('x') as f:json.dump(value,f,ensure_ascii=False,allow_nan=False,indent=2);f.flush();os.fsync(f.fileno())
def read(p):return json.loads(Path(p).read_text())
def lines(p):return [json.loads(s) for s in Path(p).read_text().splitlines()] if Path(p).exists() else []
def append(p,value):
    with Path(p).open('a') as f:f.write(json.dumps(value,ensure_ascii=False,allow_nan=False)+'\n');f.flush();os.fsync(f.fileno())

def prepare():
    from training.synthetic_protocol import rows, verify_freeze
    from semantic_pipeline.benchmark import build
    verify_freeze()
    if sha(CHALLENGE)!=CHALLENGE_SHA:raise ValueError('Challenge set changed')
    ROOT.mkdir(exist_ok=True,parents=True)
    validation=rows('validation')
    # Deterministic rare-label coverage first; no challenge content enters selection.
    selected=[];seen=set();remaining=validation.copy();counts=Counter()
    while len(selected)<40:
        candidates=[r for r in remaining if r['text_sha256'] not in seen]
        def priority(r):
            return sum(1/(1+counts[(k,r[k])]) for k in ('votability','share_blocking','poa_required','deadline_status','other_restriction'))
        r=max(candidates,key=lambda r:(priority(r),r['id']))
        selected.append(r);remaining.remove(r);seen.add(r['text_sha256'])
        for k in ('votability','share_blocking','poa_required','deadline_status','other_restriction'):counts[(k,r[k])]+=1
    def convert(r):return {'id':r['id'],'text':r['text'],'expected':{'votability':r['votability'],**{k:r[k] for k in ('share_blocking','poa_required','deadline_status','other_restriction')}}}
    write(ROOT/'validation.json',[convert(r) for r in selected])
    complete=build();write(ROOT/'complete-benchmark.json',complete)
    # Snapshot challenge truth stays in evaluator; adapters receive only the source/context.
    write(ROOT/'challenge.json',read(CHALLENGE));write(ROOT/'synthetic-test-inputs.json',rows('blind'))
    train=rows('train');train_hashes={r['text_sha256'] for r in train}
    test_hashes={r['text_sha256'] for r in rows('blind')}
    collision=[r['id'] for r in complete if hashlib.sha256(r['text'].encode()).hexdigest() in train_hashes|test_hashes]
    if collision:raise ValueError('Complete benchmark source collision')
    write(ROOT/'PROTOCOL.json',{'created_at':now(),'run_group_id':str(uuid.uuid4()),
        'training':'NONE. Reuse pinned official and historical supervised checkpoints.',
        'challenge_sha256':CHALLENGE_SHA,'validation_source':'Only supplied synthetic_validation_100.csv',
        'validation_selection':'40 unique texts selected deterministically by rare-label coverage; no frozen/challenge tuning',
        'validation_ids':[r['id'] for r in selected],'validation_label_distribution':{str(k):v for k,v in counts.items()},
        'model_selection':'One installed GLM-4.7-Flash Q4_K_M checkpoint; no downloads',
        'synthetic_test_status':'NOT BLIND / DEVELOPMENT ONLY: key previously scored; cross-split duplicates',
        'complete_benchmark_status':'SYNTHETIC_COMPLETE_BENCHMARK, authored after initial prompt, never used for tuning/training; not expert truth',
        'complete_benchmark_rows':len(complete),'automation_enabled':False,
        'threshold_grid':{'score':[None,.5,.7,.8,.9,.95,.98,.995],'margin':[None,.1,.2,.4]},
        'threshold_selection':'Maximise validation assertion accuracy after reconciliation; tie lower invocation rate then lower latency; no automation inferred',
        'preference_rule':'On >=10 known-label disagreements prefer a model only if Wilson 95% lower bound on its win proportion exceeds .5; LLM requires exact evidence at runtime',
        'oracle':'Analytical upper bound from independent LLM D, not a deployable gate',
        'input_files':{str(ROOT/n):sha(ROOT/n) for n in ('validation.json','challenge.json','complete-benchmark.json','synthetic-test-inputs.json')},
        'data_limitations':['AI-authored labels; zero new expert reviews','Supplied validation overlaps historical training','Only legacy fields labelled on old synthetic data; expanded predicate gate not validated','All customer automation disabled']})
    print('Prepared',len(selected),'validation;',len(complete),'complete benchmark',flush=True)

def laya_for(arm):return NarrowAdapter() if arm=='E' else WholeLaya(fine=arm in 'BC') if arm!='D' else None

def stage(dataset,arm,items,selection=None,counterfactual=False):
    target=ROOT/f'{dataset}-{arm}.jsonl';existing=lines(target)
    if [r['id'] for r in existing]!=[r['id'] for r in items[:len(existing)]]:raise ValueError('Invalid resume prefix')
    if len(existing)==len(items):return existing
    load_start=time.perf_counter()
    model=laya_for(arm);fallback=OllamaFallback() if arm in 'CDE' else None
    append(ROOT/'MODEL-LOADS.jsonl',{'dataset':dataset,'architecture':arm,'timestamp':now(),'load_ms':(time.perf_counter()-load_start)*1000})
    selection=selection or {'routing':{},'reconciliation_policy':{}}
    policy=selection.get('reconciliation_policy',{})
    config=RoutingConfig(**selection['routing'].get(arm,{}))
    run_id=existing[0]['run_id'] if existing else str(uuid.uuid4())
    for i,r in enumerate(items[len(existing):],len(existing)):
        start=time.perf_counter()
        result=run(r['text'],arm,laya_model=model,fallback=fallback,routing=config,reconciliation_policy=policy)
        if counterfactual and arm in 'CE' and not result['llm']:
            # Counterfactual responses for every validation row enable threshold sweeps.
            p=result['parser'];structured=result['structured_facts'];narrative=result['narrative_text']
            llm=fallback.analyse(original_text=r['text'],narrative_text=narrative,structured_facts=structured,
                laya_result=diagnostic(result['laya']),mode='FALLBACK')
            result=run(r['text'],arm,laya_model=model,routing=RoutingConfig(),
                precomputed_laya=result['laya'],precomputed_llm=llm,reconciliation_policy=policy)
            result['validation_counterfactual_llm']=llm
        result['latencies']['total_ms']=(time.perf_counter()-start)*1000
        out={'id':r['id'],'text':r['text'],'expected':r.get('expected',{}),'result':result,
            'run_id':run_id,'timestamp':now(),'dataset':dataset,'architecture':arm,
            'input_hash':hashlib.sha256(r['text'].encode()).hexdigest(),
            'frozen_manifest_sha256':sha(ROOT/'FREEZE.json') if (ROOT/'FREEZE.json').exists() else None}
        append(target,out);existing.append(out)
        print(f'{dataset} {arm} {i+1}/{len(items)} validLLM={None if result["llm"] is None else result["llm"]["valid"]} {result["latencies"]["total_ms"]:.0f}ms',flush=True)
    del model;del fallback
    import gc;gc.collect()
    try:
        import torch
        if torch.backends.mps.is_available():torch.mps.empty_cache()
    except ImportError:pass
    return existing

def wilson_lower(wins,n):
    if not n:return 0
    z=1.96;p=wins/n
    return (p+z*z/(2*n)-z*math.sqrt(p*(1-p)/n+z*z/(4*n*n)))/(1+z*z/n)

def validate():
    items=read(ROOT/'validation.json')
    # Full literal fallback context differs from D; actual generation for C and E separately.
    runs={arm:stage('validation',arm,items,counterfactual=True) for arm in ('C','D','E')}
    preferences={};evidence={}
    for arm in ('C','E'):
        votes={}
        for r in runs[arm]:
            result=r['result'];llm=result.get('validation_counterfactual_llm') or result.get('llm')
            if not llm or not llm['valid']:continue
            from semantic_pipeline.reconcile import llm_factors
            a={k:v['value'] for k,v in result['laya']['predicates'].items()};b={k:v['value'] for k,v in llm_factors(llm).items()}
            for k,v in truth(r['expected']).items():
                if k not in a or k not in b or a[k] in ('NOT_SUPPORTED','UNKNOWN','UNCERTAIN') or a[k]==b[k]:continue
                t=votes.setdefault(k,{'disagreements':0,'laya_wins':0,'llm_wins':0})
                t['disagreements']+=1;t['laya_wins']+=a[k]==v;t['llm_wins']+=b[k]==v
        pref={}
        for k,v in votes.items():
            n=v['disagreements'];winner='LLM' if v['llm_wins']>v['laya_wins'] else 'LAYA';wins=v['llm_wins'] if winner=='LLM' else v['laya_wins']
            lower=wilson_lower(wins,n)
            if n>=10 and lower>.5:pref[k]={'prefer':winner,**v,'wilson95_lower':lower,'source':'validation only, known synthetic labels'}
        preferences[arm]=pref;evidence[arm]=votes
    chosen={};sweeps={}
    protocol=read(ROOT/'PROTOCOL.json')
    for arm in ('C','E'):
        sweep=[]
        for score in protocol['threshold_grid']['score']:
            for margin in protocol['threshold_grid']['margin']:
                cfg=RoutingConfig(min_score=score,min_margin=margin);counter=[]
                for r in runs[arm]:
                    result=r['result'];llm=result.get('validation_counterfactual_llm') or result.get('llm')
                    value=run(r['text'],arm,routing=cfg,reconciliation_policy=preferences[arm],
                        precomputed_laya=copy.deepcopy(result['laya']),precomputed_llm=llm)
                    # Component wall time from actual calls; no cache-hit latency claims.
                    value['latencies']['total_ms']=value['latencies']['laya_ms']+value['latencies']['llm_ms']
                    counter.append({**r,'result':value})
                metrics=summarize(counter);invocations=metrics['llm_invocations']
                vm=metrics['fields'].get('votability',{})
                sweep.append({'routing':{'min_score':score,'min_margin':margin},
                    'laya_only_coverage':1-invocations/len(items),'llm_escalation_rate':invocations/len(items),
                    'combined_assertion_accuracy':metrics['assertion_accuracy'],
                    'votability_false_negative_rate':1-vm['positive_recall'] if vm.get('positive_recall') is not None else None,
                    'median_latency_ms':metrics['median_latency_ms'],'p95_latency_ms':metrics['p95_latency_ms'],
                    'labelled_assertions':metrics['assertions'],'unsupported_expanded_truth':'Not labelled in this validation file; no expanded accuracy claim'})
        best=max(sweep,key=lambda x:(x['combined_assertion_accuracy'],-x['llm_escalation_rate'],-x['median_latency_ms']))
        chosen[arm]=best['routing'];sweeps[arm]=sweep
    write(ROOT/'VALIDATION-SELECTION.json',{'created_at':now(),'routing':chosen,
        'reconciliation_policies':preferences,'preference_evidence':evidence,'sweeps':sweeps,
        'validation_dataset_hash':sha(ROOT/'validation.json'),'prompt_hash':OllamaFallback().prompt_version,
        'limitations':protocol['data_limitations']})
    print('Validation selected',chosen,preferences,flush=True)

def freeze():
    from training.synthetic_protocol import verify_freeze
    verify_freeze()
    selection=read(ROOT/'VALIDATION-SELECTION.json')
    targets=list(Path('semantic_pipeline').glob('*.py'))+list(Path('semantic_pipeline').glob('*.json'))+[Path('semantic_pipeline/prompt.txt'),CHALLENGE]
    targets += [ROOT/'installed-runtime-metadata.json']
    targets += [ROOT/n for n in ('PROTOCOL.json','VALIDATION-SELECTION.json','validation.json','challenge.json','complete-benchmark.json','synthetic-test-inputs.json')]
    # Preserve historical checkpoint lineage and code; no new training.
    for directory in ('data/models/laya/multilingual','data/models/supplied-synthetic-v1/encoder-4ep','data/models/narrow-v1'):
        targets += [p for p in Path(directory).rglob('*') if p.is_file() and p.suffix in ('.json','.safetensors')]
    write(ROOT/'FREEZE.json',{'created_at':now(),'files':{str(p):sha(p) for p in targets},
        'reference':'2026-10-16T12:00:00+00:00','automation_enabled':False,
        'selection':selection,'note':'All inference code, prompt, schema, routing, criteria and checkpoint hashes fixed before A–E challenge/test inference'})
    print('Frozen',len(targets),'files',flush=True)

def verify():
    f=read(ROOT/'FREEZE.json')
    for p,h in f['files'].items():
        if sha(p)!=h:raise ValueError(f'Frozen experiment changed: {p}')
    if sha(CHALLENGE)!=CHALLENGE_SHA:raise ValueError('Challenge changed')
    return f

def evaluate():
    f=verify();selected=f['selection']
    for name,filename in [('challenge','challenge.json'),('synthetic-development','synthetic-test-inputs.json'),('complete','complete-benchmark.json')]:
        items=read(ROOT/filename)
        for arm in 'ABCDE':
            config={'routing':selected['routing'],'reconciliation_policy':selected['reconciliation_policies'].get(arm,{})}
            stage(name,arm,items,config)
            verify()
    # Persist the commit BEFORE loading the previously exposed key again.
    write(ROOT/'PREDICTION-COMMIT.json',{'created_at':now(),'files':{str(p):sha(p) for p in ROOT.glob('*.jsonl') if not p.name.startswith('validation-')},'synthetic_key_status':'Previously exposed; NOT BLIND / DEVELOPMENT ONLY'})
    print('All blind-shaped inputs persisted before scoring; key already exposed historically',flush=True)

def report():
    from semantic_pipeline.reporting import report as output
    return output(ROOT)

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('stage',choices=['prepare','validate','freeze','evaluate','report','verify']);args=p.parse_args();globals()[args.stage]()
