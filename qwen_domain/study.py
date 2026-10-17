"""Versioned staged experiment; development never reads frozen answer keys."""
import json,uuid,time,copy
from pathlib import Path
from collections import Counter,defaultdict
from qwen_domain.protocol import ROOT,STUDY,CORPUS,read,write,append,rows,sha,now,digest,load_inputs,load_training,freeze_baseline
from qwen_domain.pipeline import DomainPipeline
from qwen_domain.confidence import CorrectnessCalibrator,calibration_metrics
from qwen_domain.runtime import select
from semantic_pipeline.schema import PREDICATES
from qwen_domain.metrics import metrics as domain_metrics

ARCHITECTURES=('BASE_QWEN_DIRECT','CONSTRAINED_QWEN')
def freeze():
    freeze_baseline();manifest=CORPUS/'MANIFEST.json'
    release=read(CORPUS/'RELEASE-AUDIT.json');assert release['manifest_sha256']==sha(manifest)
    names=list((ROOT/'qwen_domain').glob('*.py'))+list((ROOT/'qwen_domain').glob('*.txt'))+[ROOT/'scripts/run_qwen_domain.py',ROOT/'scripts/audit_domain_release.py',ROOT/'data/experiments/local-llm-v1/challenge.json']+list((ROOT/'data/models/qwen38-tokenizer').glob('*.json'))+list((ROOT/'data/models/qwen38-tokenizer').glob('*.jinja'))
    value={'created_at':now(),'files':{str(p.relative_to(ROOT)):sha(p) for p in names},'corpus_manifest':str(manifest.relative_to(ROOT)),'corpus_sha256':sha(manifest),
        'model_config':read(STUDY/'QWEN_DIRECT_PRE_DOMAIN_TRAINING.json')['model_config'],'release_audit_sha256':sha(CORPUS/'RELEASE-AUDIT.json'),
        'public_explicit_manifest_sha256':sha(ROOT/'data/public-real-explicit/v1/MANIFEST.json'),
        'mapping':{'A':{'token':32,'class':'YES'},'B':{'token':33,'class':'NO'},'C':{'token':34,'class':'UNKNOWN'}},
        'constrained_runtime':'llama.cpp10210 (000547513), identical Q4_K_M GGUF language weights,32768 context, one request at a time',
        'probabilities':'Native all-alternative scores normalised over fixed A/B/C; not calibrated correctness',
        'calibration_method':'Fixed logistic correctness calibration C=.1; FIT/EVALUATION duplicate-group disjoint; null unless held-out quality/support gate passes',
        'thresholds':[.7,.8,.9,.95,.98],'frozen_labels':'Never used for formulation, calibration, thresholds or training decision',
        'training_gate':'English validation only: minimum3 missed critical positives across2 generation families, or >=20 supported semantic errors across2 families. Data must be audited before an adapter trains.',
        'hardware':{'platform':__import__('platform').platform(),'unified_memory_bytes':__import__('psutil').virtual_memory().total,'processor':__import__('subprocess').check_output(['sysctl','-n','machdep.cpu.brand_string'],text=True).strip()},
        'automation_enabled':False,'customer_accuracy':None}
    candidates=load_inputs(manifest,'VALIDATION');buckets=defaultdict(list)
    for r in sorted(candidates,key=lambda r:digest('consistency42:'+r['id'])):buckets[(r['language'],r['duplicate_group'],len(r['text'])//3000)].append(r['id'])
    chosen=[]
    while len(chosen)<min(200,len(candidates)):
        for key in sorted(buckets):
            if buckets[key] and len(chosen)<200:chosen.append(buckets[key].pop())
    value['consistency_ids']=chosen;value['consistency_repeats']=3
    write(STUDY/'FORMULATION-FREEZE.json',value)
def verify():
    f=read(STUDY/'FORMULATION-FREEZE.json')
    for p,h in f['files'].items():assert sha(ROOT/p)==h,p
    assert sha(ROOT/f['corpus_manifest'])==f['corpus_sha256']
    assert sha(CORPUS/'RELEASE-AUDIT.json')==f['release_audit_sha256']
    assert sha(ROOT/'data/public-real-explicit/v1/MANIFEST.json')==f['public_explicit_manifest_sha256']
    freeze_baseline()
    return f
def benchmark(architecture,split):
    verify();manifest=CORPUS/'MANIFEST.json';items=load_inputs(manifest,split)
    import os
    os.environ['DOMAIN_ISO_ADAPTER']='false' # Parser addendum is a separate experimental condition.
    path=STUDY/'predictions'/f'{architecture}-{split}.jsonl';saved={r['id']:r for r in rows(path)} if path.exists() else {}
    if len(saved)==len(items):
        commit=STUDY/'predictions'/f'{architecture}-{split}-COMMIT.json'
        if not commit.exists():write(commit,{'created_at':now(),'predictions_sha256':sha(path),'n':len(items),'inputs_sha256':sha(CORPUS/read(manifest)['splits'][split]['inputs'])})
        return
    switched=time.perf_counter();select(architecture);runtime_switch_ms=(time.perf_counter()-switched)*1000
    initialized=time.perf_counter();model=DomainPipeline(architecture);adapter_init_ms=(time.perf_counter()-initialized)*1000
    calpath=STUDY/f'{architecture}-calibrator.joblib'
    if split not in ('VALIDATION','CALIBRATION') and calpath.exists():model.calibrator=CorrectnessCalibrator.load(calpath,model.identity)
    info=STUDY/'predictions'/f'{architecture}-{split}-MANIFEST.json'
    if not info.exists():write(info,{'run_id':str(uuid.uuid4()),'created_at':now(),'architecture':architecture,'split':split,'inputs_sha256':sha(CORPUS/read(manifest)['splits'][split]['inputs']),
        'formulation_sha256':sha(STUDY/'FORMULATION-FREEZE.json'),'model_identity':model.identity,'prompt_version':model.model.prompt_version,'concurrency':1,'generation_seed':42,'ground_truth_supplied_to_model':False,
        'runtime_switch_wall_ms':runtime_switch_ms,'adapter_initialization_ms':adapter_init_ms,'cold_start_note':'Native server load is included in switch time when newly started; normal Ollama raw load_duration is retained per call. These are separate from warm notice latency.'})
    run=read(info)
    from cascade.resources import Sampler
    sampler=Sampler().start()
    for row in items:
        if row['id'] in saved:
            assert saved[row['id']]['input_hash']==row['source_hash'];continue
        value=model.analyse(row['text'],reference=row['evaluation_time'],language=row['language'])
        serial=json.dumps(value['raw_model_result'])
        if any(s in serial for s in ['Connection refused','Connection reset','RemoteDisconnected']):
            append(STUDY/'INFRASTRUCTURE-FAILURES.jsonl',{'timestamp':now(),'id':row['id'],'architecture':architecture,'split':split,'result':value})
            raise RuntimeError('Local inference infrastructure failed; attempt preserved separately, no fake successful prediction recorded')
        record={'id':row['id'],'input_hash':row['source_hash'],'run_id':run['run_id'],'split':split,'architecture':architecture,'timestamp':now(),'result':value}
        native=value['raw_model_result'];valid=native.get('valid',all(p.get('valid',True) for p in value['predicates'].values()))
        append(path,record);print(split,architecture,row['id'],'schema_valid',valid,'ms',round(value['latency_ms']),flush=True)
    append(STUDY/'resources.jsonl',{'split':split,'architecture':architecture,'timestamp':now(),'resource':sampler.finish()})
    write(STUDY/'predictions'/f'{architecture}-{split}-COMMIT.json',{'created_at':now(),'predictions_sha256':sha(path),'n':len(items),'inputs_sha256':run['inputs_sha256']})

def observations(result):return {**{k:v['value'] for k,v in result['predicates'].items()},'classification':result['decision']['classification']}
def score(architecture,split,*,allow_frozen=False):
    if split not in ('VALIDATION','CALIBRATION') and not allow_frozen:raise ValueError('Frozen scoring requires selected-model freeze and all predictions committed')
    e=read(CORPUS/'MANIFEST.json')['splits'][split]
    if sha(CORPUS/e['labels'])!=e['labels_sha256']:raise ValueError('Frozen labels changed')
    actual={r['id']:r for r in rows(STUDY/'predictions'/f'{architecture}-{split}.jsonl')};data=rows(CORPUS/e['labels']);pairs=defaultdict(lambda:([],[]));errors=[];exact=0
    for row in data:
        a=observations(actual[row['id']]['result']);exact+=all(a.get(k)==v for k,v in row['expected'].items() if k!='classification')
        for k,y in row['expected'].items():
            pairs[k][0].append(y);pairs[k][1].append(a.get(k,'NOT_SUPPORTED'))
            if a.get(k)!=y:errors.append({'id':row['id'],'field':k,'expected':y,'predicted':a.get(k),'language':row['language'],'generation_family':row['generation_family'],'features':row['generation_features'],'text':row['text'],'confidence':actual[row['id']]['result']['confidence'].get(k),'prediction_artifact':str(STUDY/'predictions'/f'{architecture}-{split}.jsonl')})
    fields={k:domain_metrics(y,p,k) for k,(y,p) in pairs.items()};times=sorted(r['result']['latency_ms'] for r in actual.values())
    return {'architecture':architecture,'split':split,'n':len(data),'correct_assertions':sum(f['correct'] for f in fields.values()),'assertions':sum(f['n'] for f in fields.values()),
        'fields':fields,'ALL_PREDICATES_EXACT_MATCH':exact,'exact_match_denominator':len(data),'errors':errors,
        'median_latency_ms':__import__('statistics').median(times),'p95_latency_ms':times[min(len(times)-1,int(.95*len(times)))],
        'records_per_second':len(times)/(sum(times)/1000),'automation_enabled':False,'customer_accuracy':None}

def training_decision():
    metrics={a:score(a,'VALIDATION') for a in ARCHITECTURES};base=metrics['BASE_QWEN_DIRECT']
    critical={'votability','share_blocking','poa_required','registration_required'}
    misses=[e for e in base['errors'] if e['language']=='en' and e['field'] in critical and e['expected'] in ('YES','VOTABLE')]
    semantic=[e for e in base['errors'] if e['language']=='en' and e['field'] in PREDICATES]
    target=misses if len(misses)>=3 else semantic if len(semantic)>=20 else []
    justified=bool(target and len({e['generation_family'] for e in target})>=2)
    decision={'created_at':now(),'status':'TRAINING_CANDIDATE_REQUIRES_DATA_AND_TRAINER_AUDIT' if justified else 'NO_FINE_TUNING_CURRENTLY_JUSTIFIED',
        'reason':'Concrete English validation errors across independent generation families require audit before training' if justified else 'The predeclared validation error/support gate did not establish a convincing domain-training target; do not train merely because possible.',
        'english_critical_false_negatives':misses,'english_semantic_errors':semantic,'validation':metrics,'frozen_answers_opened':False,
        'constrained_experiment_completed_before_decision':True,'local_training':'No adapter trained. Installed GGUF is not a verified trainable MLX/PEFT checkpoint; exact-checkpoint trainer feasibility remains separate.',
        'automation_enabled':False}
    write(STUDY/'TRAINING-DECISION.json',decision)
    md=['# Domain training decision','',decision['status'],'',decision['reason'],'',f'English validation critical misses: {len(misses)}; semantic errors: {len(semantic)}. No frozen/challenge labels informed this decision.','',
        'Both normal and constrained base Qwen were run on the same validation inputs. Detailed per-field support/confusion matrices and every validation error are in TRAINING-DECISION.json.','',
        'The Mac has64GB unified memory. Full27B bf16 weights alone are about54GB before gradients/activations; full-precision training is not a comfortable configuration. MLX-LM documents quantised LoRA, but it is not installed here and compatibility with this exact hybrid Qwen checkpoint has not been demonstrated. No unverified adapter or benchmark is claimed. A training candidate must pass a real trainer smoke/reload check; frozen tests remain sealed until model selection is final.','',
        'The corpus is AI-authored deterministic construction, not expert-labelled production data. A negative training decision does not establish customer readiness.']
    (ROOT/'data/reports/DOMAIN_TRAINING_DECISION.md').write_text('\n'.join(md)+'\n')
    return decision

def calibrate(architecture):
    verify();e=read(CORPUS/'MANIFEST.json')['splits']['CALIBRATION'];truths={r['id']:r for r in rows(CORPUS/e['labels'])};records=[]
    predictions=rows(STUDY/'predictions'/f'{architecture}-CALIBRATION.jsonl')
    commit=read(STUDY/'predictions'/f'{architecture}-CALIBRATION-COMMIT.json');assert commit['predictions_sha256']==sha(STUDY/'predictions'/f'{architecture}-CALIBRATION.jsonl')
    identity=predictions[0]['result']['model_identity']
    for row in predictions:
        t=truths[row['id']]
        for k,c in row['result']['confidence'].items():
            if k not in t['expected']:continue
            records.append({'id':row['id'],'predicate':k,'split':'CALIBRATION','calibration_fold':t['calibration_fold'],'duplicate_group':t['duplicate_group'],
                'features':c['features'],'correct':c['value']==t['expected'][k]})
    for r in records:append(STUDY/f'{architecture}-CONFIDENCE-FEATURES.jsonl',r)
    cal=CorrectnessCalibrator(identity);reports=cal.fit([r for r in records if r['features']['language']=='en']);cal.save(STUDY/f'{architecture}-calibrator.joblib')
    write(STUDY/f'{architecture}-CALIBRATION.json',{'created_at':now(),'identity':identity,'reports':reports,'prediction_commit_sha256':sha(STUDY/'predictions'/f'{architecture}-CALIBRATION-COMMIT.json'),'population':'English synthetic only; other languages force review','automation_enabled':False})

def selection_freeze():
    d=read(STUDY/'TRAINING-DECISION.json')
    if d['status']!='NO_FINE_TUNING_CURRENTLY_JUSTIFIED':raise RuntimeError('Training target needs an actual data/trainer audit; cannot declare a completed base/domain experiment')
    write(STUDY/'SELECTED-MODEL-FREEZE.json',{'created_at':now(),'preferred':'BASE_QWEN_DIRECT','domain_adapter':None,'training_decision_sha256':sha(STUDY/'TRAINING-DECISION.json'),
        'formulation_sha256':sha(STUDY/'FORMULATION-FREEZE.json'),'calibrators':{a:sha(STUDY/f'{a}-calibrator.joblib') for a in ARCHITECTURES},'automation_enabled':False})

def final_score():
    verify();assert (STUDY/'SELECTED-MODEL-FREEZE.json').exists()
    labels=['SYNTHETIC_FROZEN_TEST','ADVERSARIAL_TEST','OOD_TEST']
    for a in ARCHITECTURES:
        for split in labels:
            c=read(STUDY/'predictions'/f'{a}-{split}-COMMIT.json');assert sha(STUDY/'predictions'/f'{a}-{split}.jsonl')==c['predictions_sha256']
    write(STUDY/'FROZEN-PREDICTION-COMMIT.json',{'created_at':now(),'files':{str(p):sha(p) for p in (STUDY/'predictions').glob('*.jsonl')},'answer_keys_not_opened_by_benchmark':True})
    write(STUDY/'SCORED.json',{split:{a:score(a,split,allow_frozen=True) for a in ARCHITECTURES} for split in labels})

def consistency(architecture):
    f=verify();select(architecture);model=DomainPipeline(architecture)
    originals={r['id']:r for r in rows(STUDY/'predictions'/f'{architecture}-VALIDATION.jsonl')}
    inputs={r['id']:r for r in load_inputs(CORPUS/'MANIFEST.json','VALIDATION')}
    path=STUDY/f'{architecture}-REPEATABILITY.jsonl';saved={(r['id'],r['repeat']) for r in rows(path)} if path.exists() else set()
    for ident in f['consistency_ids']:
        row=inputs[ident];original=originals[ident]['result']
        for repeat in (1,2):
            if (ident,repeat) in saved:continue
            result=model.analyse(row['text'],reference=row['evaluation_time'],language=row['language'])
            same={k:original['predicates'][k]['value']==result['predicates'][k]['value'] for k in original['predicates']}
            evidence=lambda r:{k:[e['text'] for e in p.get('evidence',[])] for k,p in r['predicates'].items()}
            append(path,{'id':ident,'repeat':repeat,'result':result,'predicate_agreement':same,'exact_label_agreement':all(same.values()),'evidence_identical':evidence(original)==evidence(result),'timestamp':now()})
            print('Repeat',architecture,ident,repeat,all(same.values()),flush=True)

def challenge(architecture):
    verify();assert (STUDY/'SELECTED-MODEL-FREEZE.json').exists()
    # Challenge truth is not provided to inference; no prompt or threshold changes.
    source=read(ROOT/'data/experiments/local-llm-v1/challenge.json');select(architecture);model=DomainPipeline(architecture)
    p=STUDY/'predictions'/f'{architecture}-SEMANTIC_CHALLENGE.jsonl';saved={r['id'] for r in rows(p)} if p.exists() else set()
    for item in source:
        if item['id'] in saved:continue
        result=model.analyse(item['text'],reference='2026-10-16T12:00:00+00:00')
        append(p,{'id':item['id'],'input_hash':digest(item['text']),'result':result,'timestamp':now(),'scope':'Historical exposed authored challenge, never train/validation'})
        print('Challenge',architecture,item['id'],flush=True)
    c=STUDY/'predictions'/f'{architecture}-SEMANTIC_CHALLENGE-COMMIT.json'
    if not c.exists():write(c,{'created_at':now(),'n':57,'prediction_sha256':sha(p)})

def score_challenge():
    from semantic_pipeline.metrics import truth
    original=read(ROOT/'data/experiments/local-llm-v1/challenge.json');result={}
    for a in ARCHITECTURES:
        p=STUDY/'predictions'/f'{a}-SEMANTIC_CHALLENGE.jsonl';commit=read(p.with_name(f'{a}-SEMANTIC_CHALLENGE-COMMIT.json'));assert sha(p)==commit['prediction_sha256']
        predictions={r['id']:r for r in rows(p)};fields=defaultdict(lambda:([],[]));cases=0;misses=[]
        for r in original:
            y=truth(r['expected']);p=observations(predictions[r['id']]['result'])
            vals=[p.get(x) for x in PREDICATES if x not in ('votability','share_blocking','poa_required')]
            p['other_restriction']='YES' if 'YES' in vals else 'NO' if all(x=='NO' for x in vals) else 'UNKNOWN'
            cases+=all(p.get(k)==v for k,v in y.items())
            for k,v in y.items():
                if k=='other_restriction':
                    vals=[p.get(x) for x in PREDICATES if x not in ('votability','share_blocking','poa_required')]
                    p[k]='YES' if 'YES' in vals else 'NO' if all(x=='NO' for x in vals) else 'UNKNOWN'
                fields[k][0].append(v);fields[k][1].append(p.get(k,'NOT_SUPPORTED'))
                if p.get(k)!=v:misses.append({'id':r['id'],'field':k,'truth':v,'predicted':p.get(k)})
        fm={k:domain_metrics(y,p,k) for k,(y,p) in fields.items()}
        result[a]={'cases_satisfying_supplied_assertions':cases,'cases':57,'correct_assertions':sum(x['correct'] for x in fm.values()),'assertions':sum(x['n'] for x in fm.values()),'fields':fm,'failures':misses,'final_status_truth_count':4}
    write(STUDY/'SEMANTIC-CHALLENGE-SCORED.json',result)

def public_explicit(architecture):
    verify();assert (STUDY/'SELECTED-MODEL-FREEZE.json').exists()
    base=ROOT/'data/public-real-explicit/v1';m=read(base/'MANIFEST.json');assert sha(base/'inputs.jsonl')==m['inputs_sha256']
    path=STUDY/'predictions'/f'{architecture}-PUBLIC_REAL_EXPLICIT.jsonl';saved={r['id'] for r in rows(path)} if path.exists() else set()
    select(architecture);model=DomainPipeline(architecture)
    for row in rows(base/'inputs.jsonl'):
        if row['id'] in saved:continue
        append(path,{'id':row['id'],'input_hash':row['source_hash'],'result':model.analyse(row['text'],reference=row['evaluation_time'],language=row['language']),'timestamp':now()})
    commit=path.with_name(f'{architecture}-PUBLIC_REAL_EXPLICIT-COMMIT.json')
    if not commit.exists():write(commit,{'timestamp':now(),'n':3,'predictions_sha256':sha(path),'inputs_sha256':m['inputs_sha256']})

def main():
    import argparse
    p=argparse.ArgumentParser();p.add_argument('stage',choices=['freeze','benchmark','decision','calibrate','select','score','consistency','challenge','score-challenge']);p.add_argument('--architecture',choices=ARCHITECTURES);p.add_argument('--split');args=p.parse_args()
    {'freeze':freeze,'benchmark':lambda:benchmark(args.architecture,args.split),'decision':training_decision,'calibrate':lambda:calibrate(args.architecture),'select':selection_freeze,'score':final_score,'consistency':lambda:consistency(args.architecture),'challenge':lambda:challenge(args.architecture),'score-challenge':score_challenge}[args.stage]()
if __name__=='__main__':main()
