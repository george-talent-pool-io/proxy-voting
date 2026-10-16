"""Separate unchanged 57-case adversarial regression evaluation; no fitting."""
import json,hashlib,joblib
from pathlib import Path
from training.encoder_baseline import ROOT,load_encoder,embed,predictions
from training.synthetic_protocol import write,sha,FIELDS

def main():
 f=json.loads((ROOT/'FREEZE.json').read_text())
 if sha(f['head_path'])!=f['head_sha256']:raise ValueError('Encoder checkpoint changed')
 data=json.loads(Path('tests/fixtures/semantic.json').read_text());data=[{**r,'text_sha256':hashlib.sha256(r['text'].encode()).hexdigest()} for r in data]
 x,lat=embed([r['text'] for r in data],load_encoder());p=predictions(data,x,lat,joblib.load(f['head_path']));examples=[]
 for r,a in zip(data,p):
  observed={**a['result']['decision'],'classification':a['result']['classification']};checks={k:observed[k]==v for k,v in r['expected'].items()}
  examples.append({'id':r['id'],'text':r['text'],'expected':r['expected'],'observed':observed,'checks':checks,'passed':all(checks.values()),'result':a['result']})
 write(ROOT/'challenge.json',{'kind':'unchanged 57-case authored regression; not independent customer data','passed':sum(r['passed'] for r in examples),'failed':sum(not r['passed'] for r in examples),'cases':57,'examples':examples})
if __name__=='__main__':main()
