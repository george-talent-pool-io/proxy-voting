"""Compare reducers on validation only, before opening challenge evaluation inputs."""
import json,gc
from pathlib import Path
from collections import Counter,defaultdict
from dataclasses import asdict
from semantic_pipeline.experiment import lines,append,write,read,sha,now
from semantic_pipeline.models import NarrowAdapter,WholeLaya
from semantic_pipeline.schema import PREDICATES,RESTRICTIONS
from training.synthetic_protocol import rows
from cascade.models import EvidenceNarrow,CapableSpecialist
from cascade.aggregation import AggregationConfig,STRATEGIES
ROOT=Path('data/experiments/cascade-v2')

def collect():
    items=read(ROOT/'routing-validation-80.json');old=rows('validation')
    items += [{'id':r['id'],'text':r['text'],'expected':{'votability':r['votability'],**{k:r[k] for k in ['share_blocking','poa_required']}}} for r in old]
    saved={r['id']:r for r in lines(ROOT/'validation-specialists.jsonl')}
    whole=WholeLaya(fine=True);narrow=NarrowAdapter()
    for row in items:
        if row['id'] in saved:continue
        result={**row,'input_hash':sha_text(row['text']),'timestamp':now(),'whole':whole.analyse(row['text']),'narrow':narrow.analyse(row['text'])}
        append(ROOT/'validation-specialists.jsonl',result)
        print('Validation specialists',row['id'],flush=True)

def sha_text(text):
    import hashlib
    return hashlib.sha256(text.encode()).hexdigest()

def study():
    data=lines(ROOT/'validation-specialists.jsonl');metrics=[]
    for strategy in STRATEGIES:
        for score,margin in [(.7,.2),(.9,.4),(.98,.4)]:
            cfg=AggregationConfig(strategy=strategy,min_score=score,min_margin=margin);correct=total=0;positives=Counter();detected=Counter();fields=defaultdict(Counter)
            for row in data:
                result=EvidenceNarrow.project(row['text'],row['narrow'],cfg)
                for k,v in row['expected'].items():
                    if k not in RESTRICTIONS:continue
                    p=result['predicates'][k]['value'];correct+=p==v;total+=1
                    fields[k]['n']+=1;fields[k]['correct']+=p==v
                    positives[k]+=v=='YES';detected[k]+=v==p=='YES'
                    fields[k]['false_positive']+=v!='YES' and p=='YES'
                    fields[k]['false_negative']+=v=='YES' and p!='YES'
            metrics.append({'requirements_eligible':strategy=='SUPERSESSION_AWARE','eligibility_reason':'Only supersession-aware reducer satisfies all mandated conflict/conditional-route/minimal-pair contracts; other strategies are diagnostic comparators','config':asdict(cfg),'correct':correct,'assertions':total,'agreement':correct/total,
                'positive_support':dict(positives),'positive_detected':dict(detected),'fields':dict(fields)})
    # Safety-aware validation selection: minimise critical positive misses, then
    # total agreement and false positives; ties prefer explicit supersession logic.
    def rank(m):
        critical=sum(m['fields'][k]['false_negative'] for k in ('share_blocking','poa_required'))
        return (-critical,m['correct'],-sum(f['false_positive'] for f in m['fields'].values()),m['config']['strategy']=='SUPERSESSION_AWARE',-m['config']['min_score'])
    best=max((m for m in metrics if m['requirements_eligible']),key=rank)
    write(ROOT/'AGGREGATION-SELECTION-v2.json',{'created_at':now(),'validation_inputs_sha256':sha(ROOT/'validation-specialists.jsonl'),
        'no_training':True,'challenge_used_for_selection':False,'selection_criterion':'Minimise validation blocking/POA positive misses, then assertion agreement, then false positives; supersession-aware tie preference; lower score on remaining ties',
        'selected':best,'candidates':metrics,'limitations':'AI-authored synthetic validation; old supplied validation overlaps training. Native Laya passage scores are not calibrated.'})
    selected=AggregationConfig(**best['config']);out=[]
    for row in data:
        fixed=EvidenceNarrow.project(row['text'],row['narrow'],selected)
        out.append({**row,'fixed_narrow':fixed,'capable':CapableSpecialist.combine(row['whole'],fixed)})
    for row in out:append(ROOT/'validation-fixed-specialists-v2.jsonl',row)
    write(ROOT/'AGGREGATION-BLOCKING-DELTA-v2.json',{'validation_positive_support':11,
        'before_yes':sum(r['narrow']['predicates']['share_blocking']['value']=='YES' for r in out if r['id'].startswith('SYN-') and r['expected']['share_blocking']=='YES'),
        'after_yes':sum(r['fixed_narrow']['predicates']['share_blocking']['value']=='YES' for r in out if r['id'].startswith('SYN-') and r['expected']['share_blocking']=='YES'),
        'same_checkpoint':True,'weights_retrained':False})
    print('Aggregation selected',best,flush=True)
if __name__=='__main__':
    import sys
    collect() if sys.argv[1]=='collect' else study()
