"""Accounting attribution of historical B→C differences; does not tune anything."""
import copy,json
from collections import Counter
from pathlib import Path
from semantic_pipeline.experiment import lines,read,write,now
from semantic_pipeline.metrics import observed,truth
from semantic_pipeline.pipeline import prepare,resolve_deadline
from classifier.schema import Decision
from evaluation.ae_scoring import project
OLD=Path('data/experiments/local-llm-v1');NEW=Path('data/experiments/cascade-v2')

def analyse():
    b={r['id']:r for r in lines(OLD/'challenge-B.jsonl')};c=project(lines(OLD/'challenge-C.jsonl'),'C')[0]
    totals=Counter();details=[]
    for row in c:
        before=b[row['id']]['result'];after=row['result'];left=observed(before);right=observed(after);gold=truth(row['expected'])
        det=resolve_deadline(row['text'],prepare(row['text'],False));date_only=copy.deepcopy(before)
        date_only['deadline']=det
        date_only['decision']['classification']=str(Decision(**{**before['laya']['raw']['decision'],'deadline_status':det['status']}).status())
        d=observed(date_only)
        for key,expected in gold.items():
            a=left.get(key);z=right.get(key)
            if a==z:continue
            gain=int(z==expected)-int(a==expected)
            factor=after['reconciliation']['predicates'].get(key,{})
            if key=='deadline_status' and z==det['status']:category='deterministic_date_repair' if gain>0 else 'rule_damage' if gain<0 else 'other'
            elif key=='classification' and z==d[key] and d[key]!=a:category='deterministic_date_repair' if gain>0 else 'rule_damage' if gain<0 else 'other'
            elif key=='classification':category='reconciliation_repair' if gain>0 else 'rule_damage' if gain<0 else 'other'
            elif key=='other_restriction':category='LLM_semantic_repair' if gain>0 else 'LLM_damage' if gain<0 else 'other'
            elif factor.get('source')=='UNRESOLVED_DISAGREEMENT':category='reconciliation_repair' if gain>0 else 'LLM_damage' if gain<0 else 'other'
            else:category='LLM_semantic_repair' if gain>0 else 'LLM_damage' if gain<0 else 'other'
            totals[category]+=1
            details.append({'case':row['id'],'source':row['text'],'field':key,'truth':expected,'B':a,'C':z,'date_only':d.get(key),
                'B_correct':a==expected,'C_correct':z==expected,'net_assertion_delta':gain,'category':category,
                'C_fact_source':factor.get('source'),'C_deadline_source':after['deadline']['source'],'C_conflicts':after['reconciliation']['conflicts'],
                'LLM_parsed':after['llm']['parsed'],'Laya_native_scores':before['laya']['predicates'].get(key,{}).get('scores',{}),
                'note':'Attribution is a declared accounting rule, not proof of a unique causal explanation.'})
    assert sum(r['net_assertion_delta'] for r in details)==12
    payload={'created_at':now(),'baseline':'PRE_AGGREGATION_FIX_BASELINE','assertions':95,'B_correct':73,'C_correct':85,'net_gain':12,
        'changed_assertions':len(details),'counts_by_category':dict(totals),'net_gain_by_category':{k:sum(r['net_assertion_delta'] for r in details if r['category']==k) for k in totals},
        'aggregation_difference':0,'scope':'Historical C uses whole-text B and has no sentence-aggregation difference. Model, date and policy are confounded; classification attribution prioritises unchanged semantic/date-only counterfactual, then reconciliation/rules.',
        'details':details}
    write(NEW/'C-GAIN-DECOMPOSITION.json',payload)
    md=['# Historical C gain decomposition','','This decomposes the preserved historical B = 73/95 and C = 85/95 authored labelled assertions. It is not customer accuracy or a clean estimate that an LLM adds twelve. Source predictions and expected assertions remain unchanged.','','| Category | Changed assertions | Net correctness delta |','|---|---:|---:|']
    for k,n in totals.items():md.append(f'| {k} | {n} | {payload["net_gain_by_category"][k]:+d} |')
    md += ['| aggregation_difference | 0 | 0 |','',f'Total {len(details)} changed assertions; net +12. A date-only counterfactual retains B’s exact semantic outputs and legacy status policy. A deadline/status change reproduced by that counterfactual is assigned to deterministic dates. Other status changes are assigned to reconciliation/rules; semantic UNKNOWN caused by model disagreement is reconciliation repair when correct and LLM damage when it damages a correct specialist. This is an explicit accounting convention; causal attribution can be order-dependent. Raw evidence is retained below.','',
        'The seven date-only case repairs previously reported are a different denominator from individual assertions. C uses the same whole-notice specialist as B, so aggregation contributes zero to this historical comparison. The disclosed SCORER-v2 broad-restriction union projection is used consistently.','']
    for r in details:
        md += [f'## {r["case"]} / {r["field"]}','','```text',r['source'],'```','','```json',json.dumps({k:v for k,v in r.items() if k!='source'},ensure_ascii=False,indent=2),'```','']
    Path('data/reports/C_GAIN_DECOMPOSITION.md').write_text('\n'.join(md)+'\n')
    print(payload['counts_by_category'],payload['net_gain_by_category'])
if __name__=='__main__':analyse()
