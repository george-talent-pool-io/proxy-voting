"""Stable, append-safe group allocation. No label-driven movement of held-out groups."""
import hashlib
from classifier.preprocessing import shingles, normalise, source_hash

SPLIT_VERSION = 'group-sha256-v1'

def partition(group: str, seed: str = 'laya-voting-2026-v1') -> str:
    value = int(hashlib.sha256(f'{seed}:{group}'.encode()).hexdigest()[:12], 16) / 16**12
    return 'test' if value < .2 else 'validation' if value < .4 else 'train'

def verify_isolation(rows: list[dict]):
    seen = {}
    for r in rows:
        for key in ('group_id', 'source_hash', 'source_file'):
            if not r.get(key): continue
            identity = (key,r[key])
            if identity in seen and seen[identity] != r['split']:
                raise ValueError(f'Leakage across splits: {identity}')
            seen[identity] = r['split']

# v2: exact threshold join replaces approximate LSH candidate recall.
def exact_pairs(sets,numerator=85,denominator=100):
    from collections import Counter,defaultdict
    counts=Counter(token for s in sets for token in s)
    postings=defaultdict(list)
    for i in sorted(range(len(sets)),key=lambda i:(len(sets[i]),i)):
        s=sets[i];n=len(s);bound=(n*numerator+denominator-1)//denominator
        tokens=sorted(s,key=lambda t:(counts[t],t))[:n-bound+1]
        candidates=set(j for t in tokens for j in postings[t] if len(sets[j])>=bound)
        for j in candidates:
            intersection=len(s & sets[j]);union=n+len(sets[j])-intersection
            if denominator*intersection>=numerator*union:yield j,i,intersection/max(1,union)
        for t in tokens:postings[t].append(i)


def duplicate_groups(records: list[dict], threshold: float=.85) -> list[str]:
    """Complete exact Jaccard grouping under the defined numeric-masked shingle metric.
    Global-frequency prefix filtering and integer threshold checks avoid LSH recall risk.
    Text equality and common source filing remain additional union conditions.
    """
    from fractions import Fraction
    fraction=Fraction(str(threshold))
    if not 0<fraction<=1:raise ValueError('Threshold must be in (0,1]')
    parents=list(range(len(records)));exact={};filings={};unique=[];sets=[];hashes=[]
    def find(i):
        while parents[i]!=i:
            parents[i]=parents[parents[i]];i=parents[i]
        return i
    def union(i,j):
        a,b=find(i),find(j);parents[max(a,b)]=min(a,b)
    for i,r in enumerate(records):
        text=normalise(r['text']);h=source_hash(text);hashes.append(h)
        if h in exact:union(i,exact[h])
        else:
            exact[h]=i;unique.append(i);sets.append(shingles(text))
        filing=r.get('source_file')
        if filing:
            if filing in filings:union(i,filings[filing])
            filings[filing]=i
    for a,b,similarity in exact_pairs(sets,fraction.numerator,fraction.denominator):union(unique[a],unique[b])
    names={}
    for i,h in enumerate(hashes):
        root=find(i);names[root]=min(names.get(root,'f'*64),h)
    return [names[find(i)] for i in range(len(records))]
