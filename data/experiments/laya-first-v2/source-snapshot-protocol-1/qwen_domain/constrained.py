"""Exactly one generated token, all-alternative native scores, explicit abstention.

Native scores are conditioned on the three fixed class-token alternatives. They
are raw model probabilities, never calibrated correctness probabilities.
"""
import json,math,time,ipaddress,re,hashlib
from pathlib import Path
from urllib.request import Request,build_opener,ProxyHandler
from urllib.parse import urlparse
from semantic_pipeline.fallback import NoRedirect
from semantic_pipeline.schema import PREDICATES
from semantic_pipeline.evidence import verify_evidence
from qwen_domain.protocol import ROOT,digest,sha
MAPPING={'A':'YES','B':'NO','C':'UNKNOWN'}
TOKEN_IDS={'A':32,'B':33,'C':34}
MODEL_BLOB=Path.home()/'.ollama/models/blobs/sha256-f5f1dd8920d417aac2718b0bda3403da274301efdd6760b4f0f4b864ff2ad57d'
VERSION='qwen38-three-token-v2'
QUESTIONS={
 'votability':'Does the source establish a current holder voting opportunity (even if its deadline has elapsed)?',
 'share_blocking':'Does submitting the voting instruction cause the instructed shares to be blocked against transfer?',
 'poa_required':'Is submitting a power-of-attorney document mandatory for this holder to vote?',
 'registration_required':'Is separate registration mandatory for voting, beyond ordinary record-date eligibility?',
 'beneficial_owner_disclosure_required':'Must the beneficial owner identity be disclosed as a condition of voting?',
 'holding_confirmation_required':'Must documentary confirmation of holdings accompany voting instructions?',
 'split_voting_restricted':'Is splitting the account votes between different directions prohibited or restricted?',
 'securities_lending_recall_required':'Must securities on loan be recalled to exercise voting rights?',
 'other_voting_restriction':'Is an additional mandatory voting restriction stated, excluding the named requirements and ordinary dates?'}
ANCHORS={
 'votability':r'vot|abstimm|stem|assembl|junta',
 'share_blocking':r'block|immobili|frozen|transfer|gesperr|bloqu|blocc|geblok',
 'poa_required':r'power.of.attorney|vollmacht|procur|volmacht|\bpoder\b',
 'registration_required':r'registr|anmeld|inscri',
 'beneficial_owner_disclosure_required':r'beneficial|bénéficiaire|wirtschaftlich|beneficiari|belanghebbende',
 'holding_confirmation_required':r'holding|ownership|bestandsnachweis|attestation|partecipazion|tenencia|aandelenbezit',
 'split_voting_restricted':r'split|fractionn|aufteil|divid|verdelen|different.*direction',
 'securities_lending_recall_required':r'loan|lent|lend|recall|verliehen|prêt|prestat|uitgeleen',
 'other_voting_restriction':r'professional|professionnel|professionell|professiona|profesional|restriction|eligib'}

def allowed_probabilities(response):
    probs=(response.get('completion_probabilities') or [{}])[0].get('top_probs',[])
    found={}
    for p in probs:
        if p.get('id') in TOKEN_IDS.values():
            label=next(k for k,v in TOKEN_IDS.items() if v==p['id'])
            if p.get('token')!=label or not math.isfinite(p.get('prob',float('nan'))) or p['prob']<0:raise ValueError('Unreliable native token score')
            found[label]=p['prob']
    if set(found)!=set(MAPPING) or sum(found.values())<=0:raise ValueError('Not all allowed class alternatives have native scores; never impute zero')
    mass=sum(found.values());values={MAPPING[k]:v/mass for k,v in found.items()}
    order=sorted(values,key=values.get,reverse=True)
    return {'predicted_class':order[0],'raw_model_probability':values,'native_token_probability':found,'native_allowed_token_mass':mass,
        'top_probability':values[order[0]],'second_probability':values[order[1]],'probability_margin':values[order[0]]-values[order[1]],
        'entropy':-sum(v*math.log(v) for v in values.values() if v),
        'confidence':None,'confidence_definition':'Native class-token scores renormalised over A/B/C at this prefix; not calibrated correctness probability.'}

class ConstrainedQwen:
    def __init__(self,base_url='http://127.0.0.1:11436',tokenizer=None):
        u=urlparse(base_url)
        if u.scheme!='http' or not ipaddress.ip_address(u.hostname).is_loopback or u.username or u.password:raise ValueError('Loopback runtime only')
        self.base=base_url;self.opener=build_opener(ProxyHandler({}),NoRedirect())
        if tokenizer is None:
            from transformers import AutoTokenizer
            tokenizer=AutoTokenizer.from_pretrained(ROOT/'data/models/qwen38-tokenizer',local_files_only=True)
        self.tokenizer=tokenizer;self.prompt=Path(__file__).with_name('predicate_prompt_v2.txt').read_text()
        self.prompt_version=VERSION+':'+digest(self.prompt)
        for label,tid in TOKEN_IDS.items():
            if tokenizer.encode(label,add_special_tokens=False)!=[tid]:raise ValueError('Exact official tokenizer mapping changed')
            if self.http('/tokenize',{'content':label,'add_special':False})['tokens']!=[tid]:raise ValueError('GGUF tokenizer differs from official class-token mapping')
    def http(self,path,payload=None):
        req=Request(self.base+path,data=json.dumps(payload,ensure_ascii=False).encode() if payload is not None else None,headers={'Content-Type':'application/json'})
        with self.opener.open(req,timeout=600) as r:return json.load(r)
    def classify(self,text,predicate,*,passage=None,structured=None,cache=True):
        if predicate not in PREDICATES:raise ValueError('Unknown semantic predicate')
        context={'notice':text,'authoritative_structured_facts':structured or {}}
        # The entire source/context prefix precedes the varying predicate suffix.
        content=json.dumps(context,ensure_ascii=False)+'\nREQUESTED_PREDICATE: '+predicate
        content+='\nQUESTION: '+QUESTIONS[predicate]
        if passage is not None:content+='\nPASSAGE_TO_ASSESS_IN_CONTEXT: '+json.dumps(passage,ensure_ascii=False)
        prompt=self.tokenizer.apply_chat_template([{'role':'system','content':self.prompt},{'role':'user','content':content}],tokenize=False,add_generation_prompt=True,enable_thinking=False)
        token_count=len(self.tokenizer.encode(prompt,add_special_tokens=False))
        if token_count+1>32768:return {'valid':False,'value':'UNCERTAIN' if predicate=='votability' else 'UNKNOWN','confidence':None,'error':'CONTEXT_LIMIT_NO_TRUNCATION','evidence':[]}
        payload={'prompt':prompt,'n_predict':1,'grammar':'root ::= "A" | "B" | "C"','n_probs':64,'post_sampling_probs':True,
            'temperature':1.,'top_k':0,'top_p':1.,'min_p':0.,'samplers':['temperature'],'seed':42,'cache_prompt':cache,'return_tokens':True}
        started=time.perf_counter();raw=self.http('/completion',payload)
        if Path(raw.get('model','')).resolve()!=MODEL_BLOB.resolve():raise ValueError('Constrained runtime model differs from frozen Qwen language weights')
        if raw.get('tokens_predicted')!=1 or raw.get('tokens',[None])[0] not in TOKEN_IDS.values() or raw.get('truncated'):raise ValueError('Native one-token constraint violated')
        p=allowed_probabilities(raw);value=p['predicted_class']
        if predicate=='votability':value={'YES':'VOTABLE','NO':'NOT_VOTABLE','UNKNOWN':'UNCERTAIN'}[value]
        return {**p,'value':value,'valid':True,'emitted_token':raw['content'],'emitted_token_id':raw['tokens'][0],
            'prediction_rule':'ARGMAX_OF_NATIVE_ALLOWED_CLASS_SCORES; emitted sampled token retained separately',
            'raw_runtime_response':raw,'request':payload,'prompt_version':self.prompt_version,'mapping_version':VERSION,'latency_ms':(time.perf_counter()-started)*1000,'evidence':[]}
    def analyse(self,text,*,structured=None,evidence=True):
        start=time.perf_counter();facts={};calls=0
        for key in PREDICATES:
            try:p=self.classify(text,key,structured=structured);calls+=1
            except Exception as e:p={'valid':False,'value':'UNCERTAIN' if key=='votability' else 'UNKNOWN','error':f'{type(e).__name__}: {e}','confidence':None,'evidence':[]}
            if evidence and p['valid']:
                candidates=[m.group().strip() for m in re.finditer(r'[^.!?\n]+(?:[.!?]|$)',text) if re.search(ANCHORS[key],m.group(),re.I)]
                for source in candidates[:3]:
                    try:
                        passage=self.classify(text,key,passage=source,structured=structured);calls+=1
                        p.setdefault('passage_scores',[]).append({'source':source,'result':passage})
                        if passage['value']==p['value'] and p['value'] not in ('UNKNOWN','UNCERTAIN'):
                            span=verify_evidence(text,source)
                            if span['valid']:p['evidence'].append({**span,'source':'QWEN_CONSTRAINED_PASSAGE_CANDIDATE','relevance':'MODEL_ASSESSED_NOT_EXPERT_VERIFIED'});break
                    except Exception as e:p.setdefault('evidence_errors',[]).append(str(e))
            facts[key]=p
        return {'predicates':facts,'latency_ms':(time.perf_counter()-start)*1000,'native_model_calls':calls,'architecture':'CONSTRAINED_QWEN','confidence':None,'automation_enabled':False,'prompt_version':self.prompt_version}
