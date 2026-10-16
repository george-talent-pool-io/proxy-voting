"""Exact prefix-filter Jaccard join audits all threshold matches, without LSH recall risk."""
import json
from collections import Counter,defaultdict
from pathlib import Path
from classifier.preprocessing import normalise,shingles,source_hash

from training.split import exact_pairs

def audit(file='data/normalised/public.jsonl'):
    records=[json.loads(line) for line in Path(file).read_text().splitlines()]
    unique={}
    for r in records:unique.setdefault(source_hash(normalise(r['text'])),[]).append(r)
    values=list(unique.values());sets=[shingles(rows[0]['text']) for rows in values]
    matches=[];cross=[];ungrouped=[]
    for i,j,similarity in exact_pairs(sets):
        a,b=values[i],values[j]
        item={'left':a[0]['id'],'right':b[0]['id'],'similarity':similarity,'left_split':a[0]['split'],'right_split':b[0]['split']}
        matches.append(item)
        if a[0]['split']!=b[0]['split']:cross.append(item)
        if a[0]['group_id']!=b[0]['group_id']:ungrouped.append(item)
    return {'method':'Exact global-frequency prefix-filter candidate join + exact five-word Jaccard, numeric masking; all pairs at >=0.85, without LSH recall approximation','unique_texts':len(values),'near_pairs':len(matches),'cross_split_pairs':cross,'ungrouped_pairs':ungrouped}
if __name__=='__main__':
    result=audit()
    with open('artifacts/exact-duplicate-audit.json','x') as f:json.dump(result,f,indent=2)
    print(json.dumps({k:len(v) if isinstance(v,list) else v for k,v in result.items()},indent=2))
