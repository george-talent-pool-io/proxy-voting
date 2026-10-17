"""Audit split identities and challenge-text separation without reading answers."""
from collections import defaultdict
import json
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from qwen_domain.protocol import ROOT,CORPUS,STUDY,load_inputs,read,write,digest,sha,now
from qwen_domain.dataset import qc_text

def run():
    m=read(CORPUS/'MANIFEST.json');data=[];group_roles=defaultdict(set);family_roles=defaultdict(set);hash_roles=defaultdict(set)
    for role,e in m['splits'].items():
        items=load_inputs(CORPUS/'MANIFEST.json',role);assert len(items)==e['n']
        assert {r['id'] for r in items}==set(e['ids'])
        for family in e['families']:family_roles[family].add(role)
        for r in items:
            assert digest(r['text'])==r['source_hash'];group_roles[r['duplicate_group']].add(role);hash_roles[r['source_hash']].add(role);data.append(r)
    assert all(len(v)==1 for v in [*group_roles.values(),*family_roles.values(),*hash_roles.values()])
    # Historical source texts only. No expected assertions are used in this audit.
    challenge=[r['text'] for r in read(ROOT/'data/experiments/local-llm-v1/challenge.json')]
    assert not ({digest(s) for s in challenge}&{r['source_hash'] for r in data})
    vector=TfidfVectorizer(ngram_range=(3,5),min_df=1)
    matrix=vector.fit_transform([qc_text(r['text']) for r in data]+[qc_text(s) for s in challenge]);similarity=(matrix[:len(data)]@matrix[len(data):].T).toarray()
    lexical=float(similarity.max());assert lexical<.85,'Challenge lexical near-copy in generated corpus'
    from training.encoder_baseline import load_encoder,embed
    encoder=load_encoder();chunks=[];owners=[]
    for i,text in enumerate(challenge):
        words=qc_text(text).split()
        for j in range(0,max(1,len(words)),120):chunks.append(' '.join(words[j:j+120]));owners.append(i)
    x,_=embed(chunks,encoder);y=np.zeros((len(challenge),x.shape[1]),dtype=np.float32)
    for value,i in zip(x,owners):y[i]+=value
    y/=np.maximum(np.linalg.norm(y,axis=1,keepdims=True),1e-12)
    embeddings=np.load(CORPUS/'QC-EMBEDDINGS.npy');semantic=float((embeddings@y.T).max());assert semantic<.985,'Challenge semantic near-copy in generated corpus'
    out={'created_at':now(),'manifest_sha256':sha(CORPUS/'MANIFEST.json'),'n':len(data),'unique_source_hashes':len(hash_roles),'duplicate_groups':len(group_roles),'generation_families':len(family_roles),'cross_split_groups':0,'cross_split_families':0,'cross_split_exact_duplicates':0,'challenge_exact_duplicates':0,'maximum_challenge_lexical_tfidf_cosine':lexical,'maximum_challenge_minilm_cosine':semantic,'challenge_labels_used':False,'limitations':'Similarity is a guard, not a proof of no semantic paraphrase. Construction uses domain concepts but no challenge text or answer as a generator input.'}
    write(CORPUS/'RELEASE-AUDIT.json',out);print(json.dumps(out,indent=2))
if __name__=='__main__':run()
