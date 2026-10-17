"""Batch native Laya passage inference; same weights/questions, corrected reducer."""
import copy,math,time,re
from dataclasses import asdict
from classifier.laya_classifier import load_config
from classifier.preprocessing import normalise
from semantic_pipeline.models import NarrowAdapter,WholeLaya,factor
from semantic_pipeline.schema import PREDICATES,RESTRICTIONS
from semantic_pipeline.evidence import verify_evidence
from hybrid.semantics import passages,aggregate as old_aggregate
from cascade.aggregation import AggregationConfig,NEGATIVE,HISTORY
from fast_cascade.aggregation import aggregate,VERSION as AGGREGATION_VERSION
from fast_cascade.protocol import ROOT,read,digest,sha

VERSION='batched-laya-same-weights-v2'

def decode(answer,criteria,truncated=False):
    scores=answer['probabilities'];rank=sorted(scores.values(),reverse=True)
    if set(scores)!=set(criteria) or any(not math.isfinite(v) or not 0<=v<=1 for v in scores.values()) or abs(sum(scores.values())-1)>.002:raise ValueError('Invalid native Laya scores')
    choice=answer['choice']
    if choice not in scores or scores[choice]<rank[0]-.0001:raise ValueError('Laya winning choice mismatch')
    return {'value':'UNKNOWN' if truncated else choice,'scores':scores,'confidence':scores[choice],'margin':rank[0]-rank[1],'truncated':truncated,'sdk_confidence':answer.get('confidence'),'evidence':None}

def vote_evidence(text,native,value):
    """Scope native candidate evidence. Never flip the whole-notice Laya label."""
    choices={'VOTABLE':'YES','NOT_VOTABLE':'NO','UNCERTAIN':'UNCERTAIN'}
    relevant=[]
    for span,pred in zip(passages(text),native):
        if pred['truncated'] or pred['confidence']<.7:continue
        words=span['text']
        if not re.search(r'vot|proxy|ballot|shareholder|meeting|information only|dividend|redemption|tender|automati',words,re.I):continue
        historic=bool(HISTORY.search(words))
        if historic:continue
        if pred['value']==choices.get(value):relevant.append((span,pred))
    if not relevant:return []
    span,pred=max(relevant,key=lambda x:x[1]['confidence'])
    return [{**verify_evidence(text,span['text']),'source':'MATCHING_NATIVE_LAYA_PASSAGE','native_score':pred['confidence'],'relevance':'MODEL_CANDIDATE_NOT_EXPERT_VERIFIED'}]

def vote_conflicts(text,native,value):
    """Require a current, explicit contrary passage, not an unrelated native NO."""
    opposite='NO' if value=='VOTABLE' else 'YES' if value=='NOT_VOTABLE' else None
    result=[]
    for span,p in zip(passages(text),native):
        words=span['text']
        if p['value']!=opposite or p['confidence']<.7 or p.get('truncated') or HISTORY.search(words):continue
        anchor=re.search(r'vot|proxy|ballot|meeting|information only|no shareholder action',words,re.I)
        explicit_no=re.search(r'no (?:shareholder action|vot)|not (?:vot|a vot)|information only|cannot vote',words,re.I)
        if anchor and (opposite=='YES' or explicit_no):result.append(verify_evidence(text,words))
    return result

class BatchedLaya:
    def __init__(self,batch_size=16,*,fine=True,whole=None,narrow=None):
        if batch_size not in (1,8,16,32):raise ValueError('Supported SDK batch sizes:1,8,16,32')
        started=time.perf_counter();self.batch_size=batch_size
        self.whole=whole or WholeLaya(fine=fine)
        if narrow is None:
            if fine:self.narrow=NarrowAdapter()
            else:
                from hybrid.semantics import NarrowLaya
                self.narrow=NarrowAdapter(NarrowLaya())
        else:self.narrow=narrow
        self.aggregation=AggregationConfig(**read(ROOT/'data/experiments/cascade-v2/AGGREGATION-SELECTION-v2.json')['selected']['config'])
        self.identity=digest({'version':VERSION,'whole_checkpoint':self.whole.checkpoint,'narrow_checkpoint':self.narrow.model.model_version,'whole_revision':self.whole.classifier.config['checkpoint_revision'],
            'whole_questions':self.whole.classifier.config['questions'],'narrow_questions':self.narrow.model.questions,'aggregation':asdict(self.aggregation),'source_sha256':sha(__file__),'aggregation_source_sha256':sha(ROOT/'fast_cascade/aggregation.py')})
        self.load_time_ms=(time.perf_counter()-started)*1000
    def analyse(self,text):return self.analyse_batch([text])[0]
    def analyse_batch(self,texts):
        if any(not isinstance(t,str) or not t.strip() or len(t)>2_000_000 for t in texts):raise ValueError('Invalid/empty source or input limit')
        started=time.perf_counter();model=self.narrow.model;chunks=[];owners=[];spans=[]
        for i,text in enumerate(texts):
            current=list(passages(text))
            if len(current)>10000:raise ValueError('Explicit review: too many source passages')
            spans.append(current)
            for span in current:chunks.append(span['text']);owners.append(i)
        per=[{k:[] for k in model.questions} for _ in texts];raw_usage=[]
        for start in range(0,len(chunks),max(32,self.batch_size*4)):
            subset=chunks[start:start+max(32,self.batch_size*4)]
            raw=model.agent.predict_batch(subset,model.questions,batch_size=self.batch_size,max_len=2048,head_max_len=256,sort_by_length=True)
            if len(raw)!=len(subset):raise RuntimeError('SDK count mismatch')
            for off,r in enumerate(raw):
                owner=owners[start+off];raw_usage.append({'owner':owner,'usage':r.get('usage',{})})
                for k,q in model.questions.items():per[owner][k].append(decode(r['answers'][k],q['criteria'],bool(r.get('usage',{}).get('truncated'))))
        narrow_ms=(time.perf_counter()-started)*1000
        cfg=self.whole.classifier.config
        states=[f'Reference date (UTC): {cfg["evaluation_date"]}\n\nNotice:\n{normalise(t)}' for t in texts]
        # Full historical question set retained for parity; temporal answers are audit-only.
        t=time.perf_counter();whole_raw=self.whole.classifier.agent.predict_batch(states,cfg['questions'],batch_size=self.batch_size,max_len=cfg['max_len'],head_max_len=cfg['head_max_len'],sort_by_length=True)
        if len(whole_raw)!=len(texts):raise RuntimeError('Whole-notice SDK count mismatch')
        whole_ms=(time.perf_counter()-t)*1000
        out=[]
        for i,text in enumerate(texts):
            fixed={};legacy={}
            for key in RESTRICTIONS:
                fixed[key]={**aggregate(text,key,per[i][key],self.aggregation),'source':'LAYA_EVIDENCE_AGGREGATION'}
                legacy[key]=old_aggregate(per[i][key])
            a=decode(whole_raw[i]['answers']['votable'],cfg['questions']['votable']['criteria'],bool(whole_raw[i].get('usage',{}).get('truncated')))
            vote={'YES':'VOTABLE','NO':'NOT_VOTABLE','UNCERTAIN':'UNCERTAIN','UNKNOWN':'UNCERTAIN'}[a['value']]
            ev=vote_evidence(text,per[i]['votable'],vote)
            against=vote_conflicts(text,per[i]['votable'],vote)
            fixed['votability']={**a,'value':vote,'source':'LAYA_WHOLE_WITH_NATIVE_PASSAGE_SUPPORT','evidence':ev,'supporting_passage_count':len(ev),'contradicting_passage_count':len(against),'opposing_passages':against,'conflict':bool(against)}
            for key,p in fixed.items():
                natives=per[i]['votable' if key=='votability' else key]
                p['raw_score_definition']='Native winning choice score; not calibrated correctness'
                p['minimum_passage_no_score']=min((n['scores'].get('NO',0) for n in natives),default=0)
                p['minimum_passage_no_margin']=min((n['scores'].get('NO',0)-max(v for k,v in n['scores'].items() if k!='NO') for n in natives),default=0)
            out.append({'predicates':{k:fixed[k] for k in PREDICATES},'legacy_narrow_predicates':legacy,'aggregation_version':AGGREGATION_VERSION,'passage_predictions':per[i],'whole_raw':whole_raw[i],
                'passage_spans':spans[i],'laya_identity':self.identity,'checkpoints':{'whole':self.whole.checkpoint,'narrow':model.model_path},'supervised_narrow_targets':['votable','share_blocking','poa_required'],
                'transfer_only_targets':[k for k in PREDICATES if k not in ('votability','share_blocking','poa_required')],
                'batch_size':self.batch_size,'batch_records':len(texts),'batch_wall_ms':(time.perf_counter()-started)*1000,'narrow_batch_ms':narrow_ms,'whole_batch_ms':whole_ms,
                'latency_ms':(time.perf_counter()-started)*1000/len(texts),'latency_scope':'Batch-amortised service time; not completion/request latency',
                'truncated':bool(whole_raw[i].get('usage',{}).get('truncated')) or any(n['truncated'] for ns in per[i].values() for n in ns),'automation_enabled':False})
        return out
