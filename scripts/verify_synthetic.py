"""Verify completeness, hashes, native probabilities, freeze and commitment ordering."""
import json,math
from pathlib import Path
from datetime import datetime
from training.synthetic_protocol import ROOT,rows,sha,verify_freeze,supplied_status
from classifier.schema import ClassificationResult

def main():
 verify_freeze();commit=json.loads((ROOT/'BLIND-COMMIT.json').read_text());scored=json.loads((ROOT/'TEST-SCORED.json').read_text());expected={r['id']:r for r in rows('blind')};reports={}
 assert datetime.fromisoformat(commit['created_at'])<=datetime.fromisoformat(scored['created_at'])
 for name in ['base','fine-tuned']:
  path=ROOT/(name+'-BLIND-PREDICTIONS.json');data=json.loads(path.read_text());p=data['predictions']
  assert sha(path)==commit['prediction_sha256'][name]
  assert len(p)==len(expected)==len({r['id'] for r in p}) and {r['id'] for r in p}==set(expected)
  for r in p:
   assert r['source_hash']==expected[r['id']]['text_sha256']
   result={k:v for k,v in r['result'].items() if k!='supplied_customer_status'}
   ClassificationResult.model_validate(result)
   assert r['result']['supplied_customer_status']==supplied_status(r['result']['decision'])
   assert result['action']!='AUTO_CLASSIFY'
   assert all(math.isfinite(v) and 0<=v<=1 for s in result['scores'].values() for v in s.values())
   assert abs(min(max(s.values()) for s in result['scores'].values())-result['confidence'])<1e-8
  reload=json.loads((ROOT/(name+'-BLIND-RELOAD-CHECK.json')).read_text());assert reload['identical'] and reload['n']==100
  reports[name]={'n':len(p),'source_hashes_valid':True,'probabilities_valid':True,'automation_enabled':False,'all_100_checkpoint_reload_predictions_identical':True,'prediction_sha256':sha(path)}
 output=ROOT/'VERIFICATION.json'
 with output.open('x') as f:json.dump({'kind':'Artifact integrity, not customer accuracy','commit_precedes_scoring':True,'freeze_sha256':sha(ROOT/'FREEZE.json'),'models':reports},f,indent=2)
 print(json.dumps(reports))
if __name__=='__main__':main()
