"""Staged supplied synthetic experiment. Answer-key access exists only in score().
Training/tuning can read only the supplied TRAIN/VALIDATION members of the ZIP.
Predictions for BOTH frozen models must be persisted before answer-key access.
"""
import argparse,csv,hashlib,io,json,os,statistics,time
from pathlib import Path
from zipfile import ZipFile
from collections import Counter
from apps.api.store import dumps,now
from classifier.preprocessing import source_hash,normalise
from classifier.laya_classifier import LayaClassifier,load_config,config_version
from classifier.schema import Decision
from training.study import challenge_guard
from training.train import train

ARCHIVE=Path('data/training/laya_voting_synthetic_500.zip')
ROOT=Path(os.environ.get('LAYA_SYNTHETIC_EXPERIMENT','data/experiments/supplied-synthetic-v1'))
ALLOWED={'train':'synthetic_train_300.csv','validation':'synthetic_validation_100.csv','blind':'synthetic_frozen_test_100_BLIND.csv'}
FIELDS=['votable','share_blocking','poa_required','deadline_status','other_restriction']

def write(path,value):
    with Path(path).open('x') as f:
        f.write(dumps(value)+'\n');f.flush();os.fsync(f.fileno())

def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def rows(split):
    with ZipFile(ARCHIVE) as z:
        data=list(csv.DictReader(io.StringIO(z.read(ALLOWED[split]).decode('utf-8-sig'))))
    if len(data)!={'train':300,'validation':100,'blind':100}[split]:raise ValueError('Unexpected supplied row count')
    if len({r['id'] for r in data})!=len(data):raise ValueError('Duplicate IDs')
    for r in data:
        if source_hash(r['text'])!=r['text_sha256']:raise ValueError('Source hash mismatch')
    return data

def decision(row):
    flags={k:True if row[k]=='YES' else False if row[k]=='NO' else None for k in ['share_blocking','poa_required','other_restriction']}
    return Decision(votable={'VOTABLE':'YES','NOT_VOTABLE':'NO','UNCERTAIN':'UNCERTAIN'}[row['votability']],deadline_status=row['deadline_status'],**flags)

def supplied_status(d):
    """Supplied TRAIN/VALIDATION compatibility policy, distinct from app/challenge v1.
    The supplied labels prioritise blocking even when POA/other restrictions also apply.
    This is fixed before any blind test prediction or answer-key access.
    """
    if d['votable']=='UNCERTAIN':return 'UNCERTAIN_MANUAL_REVIEW'
    if d['votable']=='NO':return 'NOT_VOTABLE'
    if d['deadline_status']=='PASSED':return 'DEADLINE_PASSED'
    if any(d[k] is None for k in ['share_blocking','poa_required','other_restriction']):return 'UNCERTAIN_MANUAL_REVIEW'
    if d['share_blocking']:return 'SHARE_BLOCKING'
    if d['poa_required']:return 'POA_REQUIRED'
    if d['other_restriction']:return 'VOTABLE_WITH_RESTRICTION'
    return 'VOTABLE'

def prepare():
    ROOT.mkdir(parents=True,exist_ok=False)
    cfg=load_config();data={s:rows(s) for s in ['train','validation']}
    write(ROOT/'protocol.json',{'created_at':now(),'archive_sha256':sha(ARCHIVE),'allowed_training_members':[ALLOWED['train']],'allowed_tuning_members':[ALLOWED['validation']],'seed':42,'primary_selection':'validation all-field exact-match; then mean per-field macro F1; then smaller/faster candidate','candidates':[{'name':'head-4ep','epochs':4,'freeze_encoder':True},{'name':'encoder-4ep','epochs':4,'freeze_encoder':False}], 'config':cfg,'automation_enabled':False,'previous_exposure':{'ids':['SYN-0001','SYN-0002'],'reason':'First two all_500 JSONL records inspected before explicit protocol instruction; both are test IDs. Do not claim all 100 labels were unseen.'},'limitations':['Supplied split retained exactly; cross-split duplicate leakage disclosed separately.','Synthetic AI-authored labels are not expert golden labels.','Supplied OPEN labels frequently lack explicit cutoff, unlike application deadline semantics.']})
    for split,items in data.items():write(ROOT/f'{split}-source.json',items)
    return data

def export(data,output,cfg):
    output.mkdir(exist_ok=False);manifest=[];hashes={};counts={}
    for split,items in data.items():
        examples=[]
        for r in items:
            d=decision(r).model_dump(exclude={'manual_review_required'})
            manifest.append({'record_id':r['id'],'split':split,'group_id':r['id'],'source_hash':r['text_sha256'],'normalised_hash':source_hash(normalise(r['text'])),'provenance':'SUPPLIED_AI_SYNTHETIC_NOT_HUMAN_VERIFIED'})
            expected={k:'YES' if v is True else 'NO' if v is False else 'UNKNOWN' if v is None else v for k,v in d.items()}
            examples.append({'state':f'Reference date (UTC): {cfg["evaluation_date"]}\n\nNotice:\n{normalise(r["text"])}','questions':cfg['questions'],'expected':expected})
        challenge_guard(manifest)
        # Retain supplied duplicates and split membership as explicitly requested.
        with (output/f'{split}.jsonl').open('x') as f:
            for r in examples:f.write(json.dumps(r,ensure_ascii=False,allow_nan=False)+'\n')
        hashes[f'{split}.jsonl']=sha(output/f'{split}.jsonl');counts[split]=len(items)
    write(output/'manifest.json',{'kind':'supplied AI synthetic experiment; not verified golden data','config':cfg,'label_revisions':manifest,'counts':counts,'file_hashes':hashes,'split_policy':'Exact supplied CSV memberships; ID groups used only to preserve requested split, NOT a leakage-isolation claim'})

def predict(model,data):
    out=[]
    for i in range(0,len(data),model.config['batch_size']):
        batch=data[i:i+model.config['batch_size']];pred=model.classify_batch([r['text'] for r in batch])
        out.extend({'id':r['id'],'source_hash':r['text_sha256'],'result':{**p.model_dump(mode='json'),'supplied_customer_status':supplied_status(p.decision.model_dump())}} for r,p in zip(batch,pred))
    return out

def field_metrics(data,predictions):
    from sklearn.metrics import accuracy_score,f1_score,confusion_matrix,balanced_accuracy_score
    byid={r['id']:r for r in predictions};truth={r['id']:r for r in data}
    if set(truth)!=set(byid):raise ValueError('Prediction IDs differ from evaluated source IDs')
    results={};failures=[];all_correct=[];status=[];app_status=[]
    for field in FIELDS:
        y=[getattr(decision(r),field) for r in data];p=[byid[r['id']]['result']['decision'][field] for r in data]
        y=['UNKNOWN' if v is None else 'YES' if v is True else 'NO' if v is False else v for v in y];p=['UNKNOWN' if v is None else 'YES' if v is True else 'NO' if v is False else v for v in p]
        labels=['YES','NO','UNCERTAIN'] if field=='votable' else ['OPEN','PASSED','UNKNOWN'] if field=='deadline_status' else ['YES','NO','UNKNOWN']
        results[field]={'accuracy':float(accuracy_score(y,p)),'macro_f1':float(f1_score(y,p,labels=labels,average='macro',zero_division=0)),'weighted_f1':float(f1_score(y,p,average='weighted',zero_division=0)),'labels':labels,'confusion_matrix':confusion_matrix(y,p,labels=labels).tolist()}
        if field=='votable':results[field]['balanced_accuracy']=float(balanced_accuracy_score(y,p))
        for label in labels:
            support=sum(v==label for v in y);tp=sum(a==label and b==label for a,b in zip(y,p));pp=sum(v==label for v in p)
            results[field].setdefault('per_class',{})[label]={'support':support,'precision':tp/pp if pp else None,'recall':tp/support if support else None,'f1':2*tp/(pp+support) if pp+support else None}
    for r in data:
        ai=byid[r['id']]['result'];d=decision(r).model_dump();wrong=[k for k in FIELDS if d[k]!=ai['decision'][k]]
        customer=ai.get('supplied_customer_status',supplied_status(ai['decision']))
        okstatus=r['expected_customer_status']==customer;status.append(okstatus);all_correct.append(not wrong);app_status.append(r['expected_customer_status']==ai['classification'])
        if wrong or not okstatus:failures.append({'id':r['id'],'text':r['text'],'expected':d,'expected_customer_status':r['expected_customer_status'],'observed':ai['decision'],'predicted_customer_status':customer,'application_customer_status':ai['classification'],'failed_fields':wrong,'scores':ai['scores'],'confidence':ai['confidence'],'top_two_margins':{k:sorted(s.values(),reverse=True)[0]-sorted(s.values(),reverse=True)[1] for k,s in ai['scores'].items()},'raw_answers':ai['raw_answers']})
    lat=[r['result']['processing_time_ms'] for r in predictions]
    return {'n':len(data),'fields':results,'all_field_exact_match_accuracy':sum(all_correct)/len(data),'customer_status_accuracy':sum(status)/len(data),'application_status_accuracy_against_supplied_buckets':sum(app_status)/len(data),'customer_status_policy':'supplied-v1 blocking > POA > other; application/challenge policy retained separately','mean_field_macro_f1':statistics.mean(v['macro_f1'] for v in results.values()),'failures':failures,'median_latency_ms':statistics.median(lat),'p95_latency_ms':__import__('numpy').percentile(lat,95).item()}

def fit_candidates(device):
    protocol=json.loads((ROOT/'protocol.json').read_text());cfg=load_config()
    if sha(ARCHIVE)!=protocol['archive_sha256']:raise ValueError('Source archive changed')
    data={s:rows(s) for s in ['train','validation']};base=LayaClassifier(cfg)
    if not (ROOT/'base-validation-predictions.json').exists():
        bp=predict(base,data['validation']);write(ROOT/'base-validation-predictions.json',bp);write(ROOT/'base-validation-metrics.json',field_metrics(data['validation'],bp))
    del base
    scores=[]
    for c in protocol['candidates']:
        export_dir=ROOT/(c['name']+'-input')
        if not export_dir.exists():export(data,export_dir,cfg)
        output=Path('data/models')/ROOT.name/c['name']
        result=train(export_dir,output,epochs=c['epochs'],device=device,freeze_encoder=c['freeze_encoder'],supplied_synthetic_protocol=True)
        model=LayaClassifier(load_config(output/'voting-config.json'));vp=predict(model,data['validation']);m=field_metrics(data['validation'],vp)
        write(ROOT/(c['name']+'-validation-predictions.json'),vp);write(ROOT/(c['name']+'-validation-metrics.json'),m)
        # Reload checkpoint and compare probabilities/choices; exclude wall-clock timing.
        probe=predict(model,data['validation'][:4]);del model
        reload_model=LayaClassifier(load_config(output/'voting-config.json'));replay=predict(reload_model,data['validation'][:4])
        keys=['scores','decision','classification','confidence','model_version','configuration_version']
        if any(any(a['result'][k]!=b['result'][k] for k in keys) for a,b in zip(probe,replay)):raise ValueError('Checkpoint reload changed predictions')
        write(ROOT/(c['name']+'-reload-check.json'),{'identical':True,'ids':[r['id'] for r in probe],'fields_checked':keys})
        scores.append({'candidate':c['name'],'model_config':str(output/'voting-config.json'),'exact_match':m['all_field_exact_match_accuracy'],'macro_f1':m['mean_field_macro_f1'],'median_latency_ms':m['median_latency_ms'],'training_result':result});del reload_model
    write(ROOT/'validation-selection.json',{'created_at':now(),'candidates':scores,'selected':max(scores,key=lambda s:(s['exact_match'],s['macro_f1'],-s['median_latency_ms']))})

def freeze():
    s=json.loads((ROOT/'validation-selection.json').read_text());cfgpath=Path(s['selected']['model_config']);cfg=load_config(cfgpath)
    files={str(p):sha(p) for p in cfgpath.parent.rglob('*') if p.is_file()}
    cfgfiles=['classifier/laya_classifier.py','classifier/schema.py','classifier/preprocessing.py','classifier/thresholds.py','classifier/deadlines.py','training/synthetic_protocol.py','training/train.py','training/encoder_baseline.py','classifier/config.json','evaluation/quality_gates.json','tests/fixtures/semantic.json','scripts/semantic_benchmark.py','uv.lock']
    if (ROOT/'encoder-baseline/FREEZE.json').exists():
        e=json.loads((ROOT/'encoder-baseline/FREEZE.json').read_text());files[e['head_path']]=sha(e['head_path']);files[str(ROOT/'encoder-baseline/FREEZE.json')]=sha(ROOT/'encoder-baseline/FREEZE.json')
    files.update({p:sha(p) for p in cfgfiles});files[str(ROOT/'protocol.json')]=sha(ROOT/'protocol.json')
    write(ROOT/'FREEZE.json',{'created_at':now(),'selected':s['selected']['candidate'],'config':cfg,'config_version':config_version(cfg),'base_config':load_config(),'files':files,'archive_sha256':sha(ARCHIVE),'thresholds':{'automation_enabled':False,'high':cfg['high_threshold'],'review':cfg['review_threshold']},'criterion':'All training and model selection finished; no test labels opened by this pipeline'})

def verify_freeze():
    f=json.loads((ROOT/'FREEZE.json').read_text())
    if sha(ARCHIVE)!=f['archive_sha256'] or any(sha(p)!=h for p,h in f['files'].items()):raise ValueError('Frozen model/code/source modified')
    return f

def blind():
    f=verify_freeze();data=rows('blind')
    for name,cfg in [('base',f['base_config']),('fine-tuned',f['config'])]:
        model=LayaClassifier(cfg);p=predict(model,data);write(ROOT/(name+'-BLIND-PREDICTIONS.json'),{'created_at':now(),'freeze_sha256':sha(ROOT/'FREEZE.json'),'config_version':model.configuration_version,'predictions':p});del model
        model=LayaClassifier(cfg);replayed=predict(model,data);del model
        keys=['scores','decision','classification','confidence','model_version','configuration_version','supplied_customer_status']
        if any(any(a['result'][k]!=b['result'][k] for k in keys) for a,b in zip(p,replayed)):raise ValueError('Frozen checkpoint reload changed blind predictions')
        write(ROOT/(name+'-BLIND-RELOAD-CHECK.json'),{'identical':True,'n':len(data),'keys':keys,'prediction_sha256':sha(ROOT/(name+'-BLIND-PREDICTIONS.json'))})
    write(ROOT/'BLIND-COMMIT.json',{'created_at':now(),'freeze_sha256':sha(ROOT/'FREEZE.json'),'prediction_sha256':{name:sha(ROOT/(name+'-BLIND-PREDICTIONS.json')) for name in ['base','fine-tuned']},'n':100,'answer_key_opened_by_pipeline':False})

def score():
    verify_freeze();commit=json.loads((ROOT/'BLIND-COMMIT.json').read_text())
    if commit['freeze_sha256']!=sha(ROOT/'FREEZE.json'):raise ValueError('Freeze changed after prediction')
    preds={}
    for name,h in commit['prediction_sha256'].items():
        p=ROOT/(name+'-BLIND-PREDICTIONS.json')
        if sha(p)!=h:raise ValueError('Persisted blind predictions changed')
        preds[name]=json.loads(p.read_text())['predictions']
        if len(preds[name])!=100:raise ValueError('Incomplete blind predictions')
    # First and ONLY answer-key read: both complete predictions are already immutable files.
    with ZipFile(ARCHIVE) as z:answers=list(csv.DictReader(io.StringIO(z.read('synthetic_frozen_test_100_ANSWER_KEY.csv').decode('utf-8-sig'))))
    blindby={r['id']:r for r in rows('blind')};data=[{**blindby[r['id']],**r} for r in answers]
    if set(blindby)!={r['id'] for r in answers}:raise ValueError('Answer key ID mismatch')
    report={'created_at':now(),'kind':'Supplied AI-authored synthetic test; NOT customer accuracy','blind_commit_sha256':sha(ROOT/'BLIND-COMMIT.json'),'automation_enabled':False,'previously_exposed_test_ids':['SYN-0001','SYN-0002'],'models':{name:field_metrics(data,p) for name,p in preds.items()},'unexposed_98':{name:field_metrics([r for r in data if r['id'] not in ['SYN-0001','SYN-0002']],[r for r in p if r['id'] not in ['SYN-0001','SYN-0002']]) for name,p in preds.items()}}
    write(ROOT/'TEST-SCORED.json',report);print(dumps({name:{k:v for k,v in m.items() if k not in ['fields','failures']} for name,m in report['models'].items()}))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('stage',choices=['prepare','train','freeze','blind','score']);p.add_argument('--device',default='mps');a=p.parse_args()
    os.environ.update(HF_HUB_OFFLINE='1',TRANSFORMERS_OFFLINE='1',USE_TF='0');import torch;torch.set_num_threads(4)
    {'prepare':prepare,'train':lambda:fit_candidates(a.device),'freeze':freeze,'blind':blind,'score':score}[a.stage]()
