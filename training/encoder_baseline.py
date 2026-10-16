"""Separate local MiniLM mean-pooled encoder + logistic heads benchmark.
Never a fallback/primary app model. Hyperparameters selected on validation only.
"""
import argparse,json,os,time,hashlib,joblib
from pathlib import Path
import numpy as np
from sklearn.linear_model import LogisticRegression
from training.synthetic_protocol import rows,decision,field_metrics,write,sha,FIELDS,ROOT as EXPERIMENT
from classifier.schema import Decision
from apps.api.store import now

ROOT=EXPERIMENT/'encoder-baseline'

def load_encoder():
 os.environ.update(HF_HUB_OFFLINE='1',TRANSFORMERS_OFFLINE='1',USE_TF='0')
 import torch
 from transformers import AutoTokenizer,AutoModel
 torch.set_num_threads(4)
 root=Path('data/models/minilm');manifest=json.loads((root/'baseline-manifest.json').read_text())
 for p,h in manifest['files'].items():
  if sha(root/p)!=h:raise ValueError('Encoder weight checksum mismatch')
 return AutoTokenizer.from_pretrained(root,local_files_only=True),AutoModel.from_pretrained(root,local_files_only=True).eval(),manifest

def embed(texts,encoder):
 import torch
 tok,model,_=encoder;result=[];latencies=[]
 for start in range(0,len(texts),16):
  batch=texts[start:start+16];t=time.perf_counter();tokens=tok(batch,padding=True,truncation=True,max_length=256,return_tensors='pt')
  with torch.inference_mode():
   out=model(**tokens).last_hidden_state;mask=tokens['attention_mask'].unsqueeze(-1);pooled=(out*mask).sum(1)/mask.sum(1).clamp(min=1);out=torch.nn.functional.normalize(pooled,p=2,dim=1)
  result.append(out.numpy());latencies.extend([(time.perf_counter()-t)*1000/len(batch)]*len(batch))
 return np.concatenate(result),latencies

def predictions(data,x,lat,heads):
 scores={k:heads[k].predict_proba(x) for k in FIELDS};out=[]
 for i,r in enumerate(data):
  native={k:{str(label):float(p) for label,p in zip(heads[k].classes_,scores[k][i])} for k in FIELDS};selected={k:max(s,key=s.get) for k,s in native.items()};d=Decision(votable=selected['votable'],deadline_status=selected['deadline_status'],**{k:True if selected[k]=='YES' else False if selected[k]=='NO' else None for k in ['share_blocking','poa_required','other_restriction']})
  out.append({'id':r['id'],'source_hash':r.get('text_sha256',hashlib.sha256(r['text'].encode()).hexdigest()),'result':{'decision':d.model_dump(),'classification':d.status().value,'scores':native,'confidence':min(max(s.values()) for s in native.values()),'raw_answers':{},'processing_time_ms':lat[i],'model_name':'MiniLM-L6-v2 frozen encoder + logistic heads','action':'MANUAL_REVIEW'}})
 return out

def fit():
 ROOT.mkdir(exist_ok=False);encoder=load_encoder();train=rows('train');val=rows('validation');x,_=embed([r['text'] for r in train],encoder);vx,vl=embed([r['text'] for r in val],encoder)
 selections=[]
 for c in [1.,10.,100.]:
  heads={}
  for k in FIELDS:
   y=[getattr(decision(r),k) for r in train];y=['UNKNOWN' if v is None else 'YES' if v is True else 'NO' if v is False else v for v in y]
   heads[k]=LogisticRegression(C=c,max_iter=2000,random_state=42).fit(x,y)
  p=predictions(val,vx,vl,heads);m=field_metrics(val,p);joblib.dump(heads,ROOT/f'heads-C{c}.joblib');write(ROOT/f'validation-C{c}.json',m);selections.append({'C':c,'exact':m['all_field_exact_match_accuracy'],'macro':m['mean_field_macro_f1']})
 chosen=max(selections,key=lambda r:(r['exact'],r['macro']));model=ROOT/f'heads-C{chosen["C"]}.joblib'
 write(ROOT/'FREEZE.json',{'created_at':now(),'selected':chosen,'candidates':selections,'encoder':encoder[2],'head_path':str(model),'head_sha256':sha(model),'code_sha256':sha(__file__),'archive_sha256':sha('data/training/laya_voting_synthetic_500.zip'),'max_tokens':256,'pooling':'masked mean, L2 normalised','train_n':300,'validation_n':100,'automation_enabled':False})

def blind():
 f=json.loads((ROOT/'FREEZE.json').read_text());model=Path(f['head_path'])
 if sha(model)!=f['head_sha256'] or sha(__file__)!=f['code_sha256']:raise ValueError('Frozen encoder candidate changed')
 data=rows('blind');x,lat=embed([r['text'] for r in data],load_encoder());p=predictions(data,x,lat,joblib.load(model));write(ROOT/'BLIND-PREDICTIONS.json',{'created_at':now(),'freeze_sha256':sha(ROOT/'FREEZE.json'),'predictions':p})
 write(ROOT/'BLIND-COMMIT.json',{'created_at':now(),'predictions_sha256':sha(ROOT/'BLIND-PREDICTIONS.json'),'freeze_sha256':sha(ROOT/'FREEZE.json'),'n':len(p)})

def score():
 from zipfile import ZipFile
 import csv,io
 if not (EXPERIMENT/'BLIND-COMMIT.json').exists():raise ValueError('Laya blind predictions must be persisted first')
 c=json.loads((ROOT/'BLIND-COMMIT.json').read_text())
 if sha(ROOT/'BLIND-PREDICTIONS.json')!=c['predictions_sha256'] or sha(ROOT/'FREEZE.json')!=c['freeze_sha256']:raise ValueError('Encoder prediction commitment changed')
 with ZipFile('data/training/laya_voting_synthetic_500.zip') as z:a=list(csv.DictReader(io.StringIO(z.read('synthetic_frozen_test_100_ANSWER_KEY.csv').decode('utf-8-sig'))))
 by={r['id']:r for r in rows('blind')};data=[{**by[r['id']],**r} for r in a];p=json.loads((ROOT/'BLIND-PREDICTIONS.json').read_text())['predictions'];write(ROOT/'TEST-SCORED.json',field_metrics(data,p))

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('stage',choices=['train','blind','score']);a=p.parse_args();{'train':fit,'blind':blind,'score':score}[a.stage]()
