"""Post-hoc fixed-output sensitivity: B + date software, without any LLM.
This isolates a confound in B→C gains; it is not an additional tuned model arm.
"""
import copy
from pathlib import Path
from classifier.schema import Decision
from semantic_pipeline.pipeline import prepare,resolve_deadline
from semantic_pipeline.metrics import summarize
from semantic_pipeline.experiment import ROOT,lines,read,write,verify,now


def analyse(root, report_path=None):
    verify();key=read(root/'synthetic-development-truth.json');out={}
    for dataset in ('challenge','synthetic-development','complete'):
        rows=copy.deepcopy(lines(root/f'{dataset}-B.jsonl'))
        if dataset=='synthetic-development':
            for r in rows:r['expected']=key[r['id']]
        for row in rows:
            r=row['result'];deadline=resolve_deadline(row['text'],prepare(row['text'],False))
            original=r['laya']['raw']['decision'];d=Decision(**{**original,'deadline_status':deadline['status']})
            r['deadline']=deadline;r['decision']={**r['decision'],'classification':str(d.status()),
                'rule':'POSTHOC_DATE_ONLY_ABLATION: original B factors/status policy, deterministic dates'}
        out[dataset]=summarize(rows)
    write(root/'DATE-RULE-ABLATION.json',{'created_at':now(),'datasets':out,
        'scope':'Same stored B semantic predictions and legacy bucket policy; replace only its temporal head with frozen deterministic date extraction/comparison. No model calls, no tuning, no new ground truth.'})
    target=(Path(report_path) if report_path else Path('data/reports/LAYA_LOCAL_LLM_AE_EVALUATION.md'))
    primary=read(root/'CORRECTED-SUMMARY.json')
    with target.open('a') as f:
        f.write('\n\n## Date-rule sensitivity: do not attribute all B→C gains to the LLM\n\n')
        f.write('A/B retain the historical learned temporal head; C/D/E use deterministic deadline logic. The following post-hoc ablation replaces only B\'s deadline with the already frozen date code and derives its status with the original legacy policy. It changes no semantic prediction and makes no model call.\n\n| Dataset | B native | B + deterministic dates only | C with actual fallback |\n|---|---:|---:|---:|\n')
        for d,m in out.items():
            a=primary['datasets'][d];f.write(f'| {d} | {a["B"]["cases_satisfying_all_supplied_assertions"]}/{m["cases"]} | {m["cases_satisfying_all_supplied_assertions"]}/{m["cases"]} | {a["C"]["cases_satisfying_all_supplied_assertions"]}/{m["cases"]} |\n')
        f.write('\nThese are cases satisfying supplied assertions, not customer accuracy. Policy/schema differences remain, so even the residual gap is not a clean causal estimate of LLM value. C versus independent D also changes prompt context; a later label-context ablation is needed to distinguish specialist information from generic prompting effects. The selected GLM run disables thinking; it does not establish the best achievable performance of this model or local generators generally.\n')
    return out

if __name__=='__main__':analyse(ROOT)
