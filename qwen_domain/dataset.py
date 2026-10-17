"""Group before splitting; private labels never appear in benchmark inputs."""
import re,os,random
from collections import Counter,defaultdict
from pathlib import Path
from datasketch import MinHash,MinHashLSH
from qwen_domain.protocol import CORPUS,ROOT,read,write,append,rows,sha,digest,now
from qwen_domain.material import DISTRACTORS
from classifier.preprocessing import normalise

class Groups:
    def __init__(self,n):self.parent=list(range(n))
    def find(self,x):
        while self.parent[x]!=x:self.parent[x]=self.parent[self.parent[x]];x=self.parent[x]
        return x
    def union(self,a,b):
        a,b=self.find(a),self.find(b)
        if a!=b:self.parent[max(a,b)]=min(a,b)

def qc_text(text):
    for s in DISTRACTORS:text=text.replace(s,'')
    text=re.sub(r'Operations reference[^\n]+','',text)
    return re.sub(r'\d+','#',normalise(text).casefold())

def lexical_groups(data,groups):
    first={};index=MinHashLSH(threshold=.82,num_perm=64);stored={};edges=[]
    for i,r in enumerate(data):
        key=r['generation_family']
        if key in first:groups.union(i,first[key])
        else:first[key]=i
        words=re.findall(r'\w+',qc_text(r['text']));grams={' '.join(words[j:j+5]) for j in range(max(1,len(words)-4))}
        mh=MinHash(num_perm=64,seed=42)
        for s in sorted(grams):mh.update(s.encode())
        for other in index.query(mh):
            j=int(other);previous=stored[j];sim=len(grams&previous)/max(1,len(grams|previous))
            if sim>=.85:groups.union(i,j);edges.append((i,j,float(sim),'LEXICAL_JACCARD'))
        index.insert(str(i),mh);stored[i]=grams
    return edges

def semantic_groups(data,groups):
    """Full QC-view chunk means; existing local English MiniLM, not a multilingual guarantee."""
    import numpy as np
    from sklearn.neighbors import NearestNeighbors
    from training.encoder_baseline import load_encoder,embed
    encoder=load_encoder();texts=[];owners=[]
    for i,r in enumerate(data):
        words=qc_text(r['text']).split()
        for start in range(0,max(1,len(words)),120):texts.append(' '.join(words[start:start+120]));owners.append(i)
    x,_=embed(texts,encoder);sums=np.zeros((len(data),x.shape[1]),dtype=np.float32);counts=np.zeros(len(data))
    for row,i in zip(x,owners):sums[i]+=row;counts[i]+=1
    sums/=counts[:,None];sums/=np.maximum(np.linalg.norm(sums,axis=1,keepdims=True),1e-12)
    np.save(CORPUS/'QC-EMBEDDINGS.npy',sums)
    neighbours=NearestNeighbors(metric='cosine',algorithm='brute',n_jobs=2).fit(sums);edges=[]
    for start in range(0,len(data),128):
        distances,indices=neighbours.radius_neighbors(sums[start:start+128],radius=.015,sort_results=True)
        for local,(ds,ids) in enumerate(zip(distances,indices)):
            i=start+local
            for d,j in zip(ds,ids):
                j=int(j)
                if j<i:groups.union(i,j);edges.append((i,j,float(1-d),'LOCAL_MINILM_COSINE'))
    return edges,encoder[2]

def split(data,groups):
    clusters=defaultdict(list)
    for i,r in enumerate(data):clusters[groups.find(i)].append(r)
    regular=[];assigned={};reserved={'ADVERSARIAL_TEST':[],'OOD_TEST':[]}
    for g,rs in clusters.items():
        roles={r['reserved_split'] for r in rs if r.get('reserved_split')}
        if len(roles)>1:raise ValueError('Duplicate component crosses OOD/adversarial families; improve corpus before freezing')
        if roles:role=next(iter(roles));assigned[g]=role;reserved[role].extend(rs)
        else:regular.append((g,rs))
    n=sum(len(rs) for _,rs in regular)
    if max(len(rs) for _,rs in regular)>n*.4:raise ValueError('One duplicate/family component exceeds 40%; corpus is too repetitive to split defensibly')
    ratios={'TRAIN':.60,'VALIDATION':.12,'CALIBRATION':.12,'SYNTHETIC_FROZEN_TEST':.16};counts=Counter()
    for g,rs in sorted(regular,key=lambda x:(-len(x[1]),digest(str(x[0])))):
        role=max(ratios,key=lambda k:(ratios[k]*n-counts[k])/max(1,ratios[k]*n))
        assigned[g]=role;counts[role]+=len(rs)
    out=defaultdict(list)
    for g,rs in clusters.items():
        for r in rs:out[assigned[g]].append({**r,'split':assigned[g],'duplicate_group':digest('|'.join(sorted(x['id'] for x in rs)))[:20]})
    if any(len(out[k])<100 for k in [*ratios,*reserved]):raise ValueError('A required split has fewer than100 examples')
    # CALIBRATION fit/eval is also group-isolated, never fit and assessed on the same notices.
    cg=defaultdict(list)
    for r in out['CALIBRATION']:cg[r['duplicate_group']].append(r)
    fit=evaln=0
    for _,rs in sorted(cg.items(),key=lambda x:(-len(x[1]),x[0])):
        fold='FIT' if fit/0.7<=evaln/0.3 else 'EVALUATION'
        for r in rs:r['calibration_fold']=fold
        if fold=='FIT':fit+=len(rs)
        else:evaln+=len(rs)
    if not fit or not evaln:raise ValueError('Independent calibration evaluation groups unavailable')
    if any(not any(r['language']=='en' and r['calibration_fold']==fold for r in out['CALIBRATION']) for fold in ('FIT','EVALUATION')):raise ValueError('English calibration must have independent English fit and evaluation groups')
    return out,clusters

def build(semantic=True):
    source=CORPUS/'construction-private/all.jsonl';data=rows(source);g=Groups(len(data));edges=lexical_groups(data,g)
    model=None
    if semantic:
        se,model=semantic_groups(data,g);edges+=se
    else:raise ValueError('Full corpus release requires the semantic duplicate scan')
    outputs,clusters=split(data,g);manifest={'version':'domain-corpus-v4','created_at':now(),'construction_sha256':sha(source),'splits':{},'criteria':read(CORPUS/'CONSTRUCTION-QC.json')['criteria'],
        'duplicate_thresholds':{'lexical_jaccard':.85,'minilm_cosine':.985},'duplicate_edges':len(edges),'duplicate_groups':len(clusters),'semantic_encoder':model,
        'semantic_limitations':'English MiniLM is supplementary evidence for foreign-language similarity, not a multilingual equivalence guarantee. Generation-family grouping is mandatory independently of similarity.',
        'no_cross_split_group_or_family':True,'automation_enabled':False,'customer_accuracy':None,'labels':'Synthetic construction, not expert labels'}
    private=CORPUS/'private';private.mkdir(exist_ok=True);os.chmod(private,0o700)
    family_roles=defaultdict(set);group_roles=defaultdict(set)
    for role,data in outputs.items():
        inputs=Path('inputs')/(role+'.jsonl');labels=Path('development' if role in ('TRAIN','VALIDATION') else 'private')/(role+'.labels.jsonl')
        for r in data:
            append(CORPUS/labels,r)
            fields=['id','text','source_hash','language','evaluation_time','duplicate_group','source_type']
            append(CORPUS/inputs,{k:r[k] for k in fields})
            family_roles[r['generation_family']].add(role);group_roles[r['duplicate_group']].add(role)
        os.chmod(CORPUS/labels,0o600)
        manifest['splits'][role]={'n':len(data),'inputs':str(inputs),'inputs_sha256':sha(CORPUS/inputs),'labels':str(labels),'labels_sha256':sha(CORPUS/labels),'ids':[r['id'] for r in data],
            'groups':len({r['duplicate_group'] for r in data}),'families':sorted({r['generation_family'] for r in data}),'languages':dict(Counter(r['language'] for r in data)),
            'difficulty':dict(Counter(r['difficulty'] for r in data)),'min_chars':min(len(r['text']) for r in data),'max_chars':max(len(r['text']) for r in data),
            'labels_distribution':{k:dict(Counter(r['expected'][k] for r in data)) for k in [*__import__('semantic_pipeline.schema',fromlist=['PREDICATES']).PREDICATES,'deadline_status']},
            'calibration_folds':dict(Counter(r.get('calibration_fold') for r in data)) if role=='CALIBRATION' else None}
    assert all(len(v)==1 for v in [*family_roles.values(),*group_roles.values()])
    write(CORPUS/'MANIFEST.json',manifest)
    write(CORPUS/'FROZEN-LABEL-COMMIT.json',{'created_at':now(),'manifest_sha256':sha(CORPUS/'MANIFEST.json'),'protected_splits':{k:v['labels_sha256'] for k,v in manifest['splits'].items() if k not in ('TRAIN','VALIDATION')},'no_expert_label_claim':True})
    write(CORPUS/'DUPLICATE-EDGES.json',edges)
    return {k:v['n'] for k,v in manifest['splits'].items()}
if __name__=='__main__':print(build())
