"""Post-freeze diagnostics only; never tune model, calibration or thresholds here."""
import json
from training.synthetic_protocol import ROOT,decision,write,FIELDS
from evaluation.post_synthetic import labelled_data
from evaluation.metrics import factor_calibration

def main():
 data=labelled_data();calibration={};tradeoff={}
 for name in ['base','fine-tuned']:
  predictions=json.loads((ROOT/(name+'-BLIND-PREDICTIONS.json')).read_text())['predictions'];by={r['id']:r['result'] for r in predictions};evaluation=[]
  for r in data:
   a=by[r['id']];evaluation.append({'true_decision':decision(r).model_dump(),'decision':a['decision'],'scores':a['scores'],'confidence':a['confidence']})
  calibration[name]=factor_calibration(evaluation);points=[]
  for threshold in [.5,.7,.8,.9,.95,.98,.99]:
   selected=[r for r in evaluation if r['confidence']>=threshold];positive=[r for r in selected if r['decision']['votable']=='YES'];tp=sum(r['true_decision']['votable']=='YES' for r in positive);support=sum(r['true_decision']['votable']=='YES' for r in evaluation)
   points.append({'threshold':threshold,'notice':'score-only diagnostic, independent of eligibility and always-disabled production automation','coverage':len(selected)/len(evaluation),'votable_precision':tp/len(positive) if positive else None,'votable_recall_of_all_votable':tp/support if support else None})
  tradeoff[name]=points
 if not (ROOT/'native-calibration.json').exists():write(ROOT/'native-calibration.json',calibration)
 write(ROOT/'automation-precision-recall.json',tradeoff)
if __name__=='__main__':main()
