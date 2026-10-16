"""Validation-only diagnostic: equalise absence handling across all reducers.

This does not change the selected reducer or any inference configuration. The
original comparator implementations intentionally differ in absence policy;
therefore their total-agreement gap is not a pure supersession-strategy effect.
"""
from collections import Counter,defaultdict
from dataclasses import asdict
from pathlib import Path
from cascade.aggregation import AggregationConfig,STRATEGIES,reduce_states
from cascade.study import ROOT,verify_core
from semantic_pipeline.experiment import lines,read,write,sha,now
from semantic_pipeline.schema import RESTRICTIONS


def matched_reduce(states,config):
    value=reduce_states(states,config)
    control=reduce_states(states,AggregationConfig(strategy='SUPERSESSION_AWARE',min_score=config.min_score,min_margin=config.min_margin,voting_route=config.voting_route))
    if control['aggregation_reason']=='DOCUMENT_ABSENCE_NOT_EXPLICIT_NEGATION':
        value=control
    return value


def main():
    verify_core();source=ROOT/'validation-fixed-specialists-v2.jsonl'
    selection=ROOT/'AGGREGATION-SELECTION-v2.json';before=sha(selection)
    data=lines(source);metrics=[]
    for strategy in STRATEGIES:
        for score,margin in [(.7,.2),(.9,.4),(.98,.4)]:
            cfg=AggregationConfig(strategy=strategy,min_score=score,min_margin=margin)
            fields=defaultdict(Counter)
            for row in data:
                for key,y in row['expected'].items():
                    if key not in RESTRICTIONS:continue
                    states=row['fixed_narrow']['predicates'][key]['passage_states']
                    p=matched_reduce(states,cfg)['value'];m=fields[key]
                    m['assertions']+=1;m['correct']+=p==y
                    m['positive_support']+=y=='YES';m['positive_detected']+=y==p=='YES'
                    m['positive_misses']+=y=='YES' and p!='YES';m['false_positives']+=y!='YES' and p=='YES'
            total=Counter()
            for m in fields.values():total.update(m)
            metrics.append({'config':asdict(cfg),'fields':dict(fields),'totals':dict(total)})
    assert sha(selection)==before
    result={'created_at':now(),'source_sha256':sha(source),'selected_config_sha256_unchanged':before,
        'purpose':'Equal document-absence policy; diagnostic only, no model/routing selection',
        'scope':'Same 180 development validation notices, never challenge data; supplied validation has historical train overlap.',
        'selection_changed':False,'candidates':metrics}
    target=ROOT/'AGGREGATION-MATCHED-ABSENCE-CONTROL.json'
    if target.exists():raise RuntimeError('Diagnostic already persisted; do not overwrite it')
    write(target,result)
    md=['','## Matched-absence diagnostic control','',
        'The original comparator table above includes different document-absence policies: only SUPERSESSION_AWARE implements a conservative native-all-NO absence fallback. Its large total-agreement advantage must therefore **not** be attributed solely to supersession reasoning. This additional validation-only control applies the identical absence fallback to all six reducers, leaving their handling of actual positive/negative/conflicting passages unchanged. No checkpoint, selected strategy, threshold, prompt or routing decision is changed. All predictions come from the same cached native passage outputs; no challenge cases were consulted.','',
        '| Strategy | Score / margin | Correct restriction assertions | Affirmative misses (all restriction fields) | False positives |',
        '|---|---:|---:|---:|---:|']
    for m in metrics:
        c=m['config'];t=m['totals'];md.append(f'| {c["strategy"]} | {c["min_score"]} / {c["min_margin"]} | {t["correct"]}/{t["assertions"]} | {t["positive_misses"]} | {t["false_positives"]} |')
    md += ['', 'Small overall differences on repetitive synthetic validation do not establish superiority on real notices. Contract tests independently require abstention on unresolved contradictions and voting routes; an accurate result on a simple validation sentence does not remove that requirement. Full counts are retained in AGGREGATION-MATCHED-ABSENCE-CONTROL.json.']
    with Path('data/reports/AGGREGATION_VALIDATION.md').open('a') as f:f.write('\n'.join(md)+'\n')
    print('Matched-absence control saved; frozen selection unchanged')

if __name__=='__main__':main()
