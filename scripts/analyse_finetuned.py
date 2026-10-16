"""Publish all challenge errors/regressions, including highly confident mistakes."""
import json
from collections import Counter
from pathlib import Path
from training.synthetic_protocol import ROOT

def main():
 base=json.loads((ROOT/'base-challenge.json').read_text());tuned=json.loads((ROOT/'fine-tuned-challenge.json').read_text())
 old={r['id'] for r in base['examples'] if not r['passed']};bad=[r for r in tuned['examples'] if not r['passed']];new={r['id'] for r in bad}
 summary={'base_passed':base['passed'],'fine_tuned_passed':tuned['passed'],'n':57,'fixed':sorted(old-new),'regressed':sorted(new-old),'remaining':sorted(new&old),'failed_assertions':dict(Counter(k for r in bad for k,v in r['checks'].items() if not v)),'high_confidence_errors':[r['id'] for r in bad if r['result']['confidence']>=.98]}
 (ROOT/'challenge-error-summary.json').write_text(json.dumps(summary,indent=2)+'\n')
 lines=['# Fine-tuned Laya: all semantic challenge errors','',f"Base {base['passed']}/57 → fine-tuned {tuned['passed']}/57. Fixed {len(old-new)}, regressed {len(new-old)}, remaining {len(new&old)}. {len(summary['high_confidence_errors'])} wrong cases have aggregate policy score ≥0.98.",'','These are unchanged, partial-field authored expectations, not customer labels. No post-test model change is made. Supplied synthetic deadline/status conventions differ from this challenge; that is an evaluation limitation, not permission to change expectations.','', '## Pattern counts (overlapping)','',str(summary['failed_assertions']),'','## Regressions','',', '.join(summary['regressed']),'','## Every failed case','']
 for r in sorted(bad,key=lambda r:(-r['result']['confidence'],r['id'])):
  lines += [f"### {r['id']} — {'REGRESSION' if r['id'] not in old else 'remaining error'}",'',r['text'],'','Expected: `'+json.dumps(r['expected'],ensure_ascii=False)+'`','', 'Observed: `'+json.dumps(r['observed'],ensure_ascii=False)+'`','',f"Policy score: {r['result']['confidence']:.4f}. Failed assertions: {', '.join(k for k,v in r['checks'].items() if not v)}.",'','```json',json.dumps(r['result']['scores'],ensure_ascii=False,indent=2),'```','']
 Path('data/reports/LAYA_FINETUNED_CHALLENGE_ERRORS.md').write_text('\n'.join(lines)+'\n');print(summary)
if __name__=='__main__':main()
