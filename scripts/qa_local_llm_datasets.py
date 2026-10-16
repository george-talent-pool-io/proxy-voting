"""Source-only overlap audit. Never opens an answer key or changes a split."""
import hashlib,json,re
from collections import Counter
from pathlib import Path
from training.synthetic_protocol import rows
from classifier.preprocessing import normalise
from semantic_pipeline.experiment import ROOT,read,write,now


def hash_text(s):return hashlib.sha256(normalise(s).encode()).hexdigest()
def shingles(s):
    tokens=re.findall(r'\w+',normalise(s).casefold());return {tuple(tokens[i:i+5]) for i in range(max(0,len(tokens)-4))}

if __name__=='__main__':
    old={s:rows(s) for s in ('train','validation','blind')};new=read(ROOT/'complete-benchmark.json');challenge=read(ROOT/'challenge.json');validation=read(ROOT/'validation.json')
    hashes={s:{hash_text(r['text']) for r in data} for s,data in old.items()}
    collisions={name:[r['id'] for r in new if hash_text(r['text']) in values] for name,values in hashes.items()}
    collisions['challenge']=[r['id'] for r in new if hash_text(r['text']) in {hash_text(q['text']) for q in challenge}]
    comparisons=[('old-'+split,r) for split,rr in old.items() for r in rr]+[('challenge',r) for r in challenge]
    reference=[(group,r['id'],shingles(r['text'])) for group,r in comparisons]
    near=[];maximum=0
    for r in new:
        a=shingles(r['text'])
        for group,identifier,b in reference:
            score=len(a&b)/len(a|b) if a|b else 0
            maximum=max(maximum,score)
            if score>=.85:near.append({'complete_id':r['id'],'reference_set':group,'reference_id':identifier,'word_5gram_jaccard':score})
    out={'created_at':now(),'source_only':True,'answer_key_opened':False,
        'historical_unique_normalised_texts':{s:len(v) for s,v in hashes.items()},
        'historical_test_rows_seen_in_train_or_validation':sum(hash_text(r['text']) in hashes['train']|hashes['validation'] for r in old['blind']),
        'selected_validation_n':len(validation),'selected_validation_unique':len({hash_text(r['text']) for r in validation}),
        'selected_validation_rows_seen_in_historical_training':sum(hash_text(r['text']) in hashes['train'] for r in validation),
        'complete_n':len(new),'complete_unique':len({hash_text(r['text']) for r in new}),
        'complete_exact_overlap_ids':collisions,'complete_near_overlap_85':near,
        'maximum_complete_reference_word5_jaccard':maximum,
        'new_training':'NONE; benchmark labels never enter supervised training',
        'limits':'Exact/lexical overlap checks do not prove absence of semantic paraphrases or pretraining exposure. The supplied old split remains leaky; it was not silently repartitioned.'}
    assert not any(collisions.values());assert not near
    write(ROOT/'DATASET-QA.json',out);print(json.dumps(out,indent=2))
