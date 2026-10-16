"""Nested supplied-training subsets; validation only. Never reads a test answer key."""
import hashlib,json
from collections import defaultdict
from pathlib import Path
from training.synthetic_protocol import ROOT,rows,export,predict,field_metrics,write
from training.train import train
from classifier.laya_classifier import load_config,LayaClassifier

def nested_order(data):
 families=defaultdict(list)
 for r in sorted(data,key=lambda r:hashlib.sha256(('42:'+r['id']).encode()).hexdigest()):families[r['test_family']].append(r)
 out=[]
 while any(families.values()):
  for k in sorted(families):
   if families[k]:out.append(families[k].pop())
 return out

def main(device='mps',candidate='head-4ep'):
 protocol=json.loads((ROOT/'protocol.json').read_text());cfg=load_config();tr=nested_order(rows('train'));val=rows('validation');points=[]
 c=next(c for c in protocol['candidates'] if c['name']==candidate)
 for n in [50,100,200,300]:
  if n==300:m=json.loads((ROOT/(c['name']+'-validation-metrics.json')).read_text())
  else:
   inp=ROOT/f'curve-{n}-input';export({'train':tr[:n],'validation':val},inp,cfg)
   # Same source constraints, but intentional nested subset rather than all 300.
   # The strict trainer still rejects actual overlap, so this experiment uses the official SDK
   # directly through a separately validated subset contract (see train(...)).
   out=Path('data/models')/ROOT.name/f'curve-{n}'
   train(inp,out,epochs=c['epochs'],device=device,freeze_encoder=c['freeze_encoder'],supplied_synthetic_protocol='nested-subset')
   model=LayaClassifier(load_config(out/'voting-config.json'));p=predict(model,val);m=field_metrics(val,p);write(ROOT/f'curve-{n}-validation-predictions.json',p);write(ROOT/f'curve-{n}-validation-metrics.json',m);del model
  pr=m['fields'];restriction=[]
  # Recall over individual positive restriction factors; absent support is not success.
  total=correct=0
  for k in ['share_blocking','poa_required','other_restriction']:
   z=pr[k]['per_class']['YES'];total+=z['support'];correct+=(z['recall'] or 0)*z['support']
  points.append({'n':n,'unique_texts':len({r['text_sha256'] for r in tr[:n]}),'exact_match':m['all_field_exact_match_accuracy'],'macro_f1':m['mean_field_macro_f1'],'votable_recall':pr['votable']['per_class']['YES']['recall'],'restriction_recall':correct/total if total else None,'validation_n':100})
 write(ROOT/'learning-curve.json',{'points':points,'seed':42,'candidate_hyperparameters':c,'split':'supplied validation, known duplicate overlap','unavailable_sizes':[400,800],'reason':'Only 300 supplied training rows exist; no test/validation labels moved to training.'})
if __name__=='__main__':
 import argparse
 p=argparse.ArgumentParser();p.add_argument('--device',default='mps');p.add_argument('--candidate',default='head-4ep');a=p.parse_args();main(a.device,a.candidate)
