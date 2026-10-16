"""After scoring only: operational diagnostics and conservative sensitivity analyses.
No fitting, threshold/model selection or training occurs in this module.
"""
import csv,io,json
from pathlib import Path
from zipfile import ZipFile
from collections import defaultdict
from training.synthetic_protocol import ROOT,ARCHIVE,rows,decision,field_metrics,supplied_status,write,sha,FIELDS
from evaluation.metrics import automation_curve,factor_calibration
from training.split import duplicate_groups

def labelled_data():
 if not (ROOT/'TEST-SCORED.json').exists():raise ValueError('Complete the frozen blind protocol before diagnostics')
 with ZipFile(ARCHIVE) as z:answers=list(csv.DictReader(io.StringIO(z.read('synthetic_frozen_test_100_ANSWER_KEY.csv').decode('utf-8-sig'))))
 by={r['id']:r for r in rows('blind')};return [{**by[r['id']],**r} for r in answers]

def main():
 data=labelled_data();allrows=rows('train')+rows('validation')+rows('blind');groups=duplicate_groups(allrows);gby={r['id']:g for r,g in zip(allrows,groups)}
 non_test={g for r,g in zip(allrows,groups) if r['id'] not in {x['id'] for x in data}}
 clean={r['id'] for r in data if gby[r['id']] not in non_test};curves={};sensitivity={};status_reports={};calibration={}
 from sklearn.metrics import classification_report,confusion_matrix,accuracy_score,balanced_accuracy_score
 for name in ['base','fine-tuned']:
  p=json.loads((ROOT/(name+'-BLIND-PREDICTIONS.json')).read_text())['predictions'];by={r['id']:r['result'] for r in p};evaluation=[]
  for r in data:
   ai=by[r['id']];d=decision(r).model_dump();complete=all(d[k]==ai['decision'][k] for k in FIELDS)
   # Diagnostic threshold sweep allows all non-conflicting semantic outputs; production eligibility
   # remains independently stricter and disabled. Do not call these real auto-processed notices.
   eligible=ai['decision']['votable']!='UNCERTAIN' and all(ai['decision'][k] is not None for k in ['share_blocking','poa_required','other_restriction']) and ai['decision']['deadline_status']!='UNKNOWN' and not ai['usage'].get('truncated',False)
   evaluation.append({'id':r['id'],'group_id':gby[r['id']],'confidence':ai['confidence'],'eligible':eligible,'correct':complete,'true_decision':d,'decision':ai['decision'],'scores':ai['scores']})
  curves[name]=[r for r in automation_curve(evaluation) if r['threshold'] in [0,.5,.6,.7,.8,.9,.95,.98,.99,1]]
  for point in curves[name]:
   selected=[r for r in evaluation if r['eligible'] and r['confidence']>=point['threshold']]
   positives=[r for r in selected if r['decision']['votable']=='YES'];tp=sum(r['true_decision']['votable']=='YES' for r in positives);support=sum(r['true_decision']['votable']=='YES' for r in evaluation)
   point.update(auto_votable_precision=tp/len(positives) if positives else None,auto_votable_recall_of_all_votable=tp/support if support else None)
  calibration[name]=factor_calibration(evaluation)
  subset=[r for r in data if r['id'] in clean];sensitivity[name]=field_metrics(subset,[r for r in p if r['id'] in clean]) if subset else None
  y=[r['expected_customer_status'] for r in data];pred=[supplied_status(by[r['id']]['decision']) for r in data];labels=['VOTABLE','NOT_VOTABLE','VOTABLE_WITH_RESTRICTION','POA_REQUIRED','SHARE_BLOCKING','DEADLINE_PASSED','UNCERTAIN_MANUAL_REVIEW']
  status_reports[name]={'accuracy':float(accuracy_score(y,pred)),'balanced_accuracy':float(balanced_accuracy_score(y,pred)),'report':classification_report(y,pred,labels=labels,output_dict=True,zero_division=0),'labels':labels,'confusion_matrix':confusion_matrix(y,pred,labels=labels).tolist()}
 write(ROOT/'automation-analysis.json',{'kind':'Post-freeze synthetic diagnostic; no policy selected on test; automation OFF','models':curves})
 write(ROOT/'sensitivity-analysis.json',{'test_n':100,'unique_test_texts':len({r['text_sha256'] for r in data}),'near_duplicate_overlap_train_or_validation_n':100-len(clean),'nonoverlapping_n':len(clean),'nonoverlapping_ids':sorted(clean),'models':sensitivity,'limitation':'Nonoverlap at lexical Jaccard .85 does not imply independence of synthetic templates or authoring model.'})
 write(ROOT/'customer-status-reports.json',status_reports)
 write(ROOT/'native-calibration.json',calibration)
 # Publish every failed case, not just interesting examples.
 scored=json.loads((ROOT/'TEST-SCORED.json').read_text())
 lines=['# Supplied synthetic test — every failure','','AI-authored labels, known duplicate overlap, two previously exposed test labels. No customer accuracy claim.']
 for name,m in scored['models'].items():
  lines+=['',f'## {name}: {len(m["failures"])} records with at least one failed field/status','']
  for r in m['failures']:
   lines += [f'### {r["id"]}','',r['text'],'','```json',json.dumps({k:v for k,v in r.items() if k!='text'},ensure_ascii=False,indent=2),'```','']
 (ROOT/'ALL_TEST_FAILURES.md').write_text('\n'.join(lines)+'\n')

if __name__=='__main__':main()
