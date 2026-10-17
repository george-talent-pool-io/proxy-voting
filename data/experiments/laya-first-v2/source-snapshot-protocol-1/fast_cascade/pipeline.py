"""Three independently gated gears, immutable stage outputs, no automation."""
import copy,time
from dataclasses import asdict
from semantic_pipeline.schema import PREDICATES
from semantic_pipeline.decision import decide
from semantic_pipeline.pipeline import resolve_deadline
from semantic_pipeline.reconcile import llm_factors
from semantic_pipeline.evidence import verify_evidence
from qwen_domain.confidence import features,decision_confidence
from fast_cascade.protocol import ROOT,read,sha,digest,now
from fast_cascade.routing import Policy,assess,reconcile

VERSION='three-gear-pipeline-v2'

def confidence_features(text,key,p,*,stage,language='en',input_type='UNSTRUCTURED_NOTICE',conflict=False):
    out=features(text,key,p,language=language,input_type=input_type,deterministic_conflict=conflict)
    from fast_cascade.routing import signal
    s=signal(text,key,p,language);out['features'].update(stage=stage,laya_native_top=s['top_score'] if stage=='LAYA' else None,
        native_margin=s['margin'],supporting_passage_count=s['supporting_passage_count'],contradicting_passage_count=s['contradicting_passage_count'],
        document_absence=p.get('aggregation_reason')=='DOCUMENT_ABSENCE_NOT_EXPLICIT_NEGATION',prediction=p.get('value'))
    if p.get('value') in ('YES','VOTABLE') and not any(e.get('valid') for e in p.get('evidence',[])):
        out['force_review']=True;out['heuristic_band']='LOW'
    return out

def empty_pred(key,reason):return {'value':'UNCERTAIN' if key=='votability' else 'UNKNOWN','source':reason,'scores':{},'evidence':[]}

class Pipeline:
    def __init__(self,policy=None,*,laya=None,qwen=None,preferences=None,calibrator=None,iso=False):
        self.policy=policy or Policy();self.laya=laya;self.qwen=qwen;self.preferences=preferences or {};self.calibrator=calibrator;self.iso=iso
        config=read(ROOT/'data/experiments/cascade-v2/LLM-CONFIGS-v3.json')['QWEN_DIRECT']
        self.identity=digest({'version':VERSION,'policy':asdict(self.policy),'preferences':self.preferences,'iso':iso,'model_config':config,
            'sources':{p:sha(ROOT/p) for p in ['fast_cascade/pipeline.py','fast_cascade/aggregation.py','fast_cascade/routing.py','fast_cascade/laya.py','fast_cascade/models.py','qwen_domain/constrained.py','qwen_domain/confidence.py','cascade/proxy_semantic_common_v1.txt','semantic_pipeline/decision.py']}})
    def analyse(self,text,*,language='en',reference='2026-10-17T12:00:00+00:00',precomputed_laya=None,precomputed_gear2=None,precomputed_full=None,replay=False):
        if not isinstance(text,str) or not text.strip() or len(text)>2_000_000:raise ValueError('Nonempty source within input limit required')
        started=time.perf_counter();parser=None;structured={};kind='UNSTRUCTURED_NOTICE';narrative=text
        if self.iso:
            from iso_adapter.routing import route
            parser=route(text);kind=parser['input_type'];structured=parser.get('structured_facts',{});narrative=parser.get('narrative') or text
        if precomputed_laya is not None and not replay and digest(text)!=precomputed_laya.get('input_hash'):raise ValueError('Batched Laya source hash mismatch')
        laya=copy.deepcopy(precomputed_laya) if precomputed_laya is not None else self.laya.analyse(narrative)
        if narrative!=text:
            for p in laya['predicates'].values():p['evidence']=[verify_evidence(text,e['text']) for e in p.get('evidence',[]) if verify_evidence(text,e['text'])['valid']]
        current=copy.deepcopy(laya['predicates']);origins={k:'LAYA' for k in PREDICATES};trace=[];conflicts=[]
        gate1={k:assess(text,k,current[k],self.policy,language=language) for k in PREDICATES}
        pending=[k for k,g in gate1.items() if not g['accepted_for_research']];gear2=None;gate2={};unresolved=list(pending)
        if pending and self.policy.gear2:
            if replay:
                if precomputed_gear2 is None:raise ValueError('Missing counterfactual Gear 2 output')
                if not set(pending)<=set(precomputed_gear2['predicates']):raise ValueError('Incomplete counterfactual Gear 2 coverage')
                gear2=copy.deepcopy(precomputed_gear2);gear2['actually_requested_by_policy']=pending
            else:gear2=self.qwen.constrained(text,pending,laya=laya,structured=structured)
            unresolved=[]
            for k in pending:
                p=gear2['predicates'][k];g=assess(text,k,p,self.policy,gear=2,language=language);gate2[k]=g
                before=current[k];merged,c,t=reconcile(before,p,k,right_accepted=g['accepted_for_research'],preferences=self.preferences.get('gear2'))
                current[k]=merged;trace.append({'stage':'GEAR2',**t});conflicts+=c
                if merged is p:origins[k]='CONSTRAINED_QWEN'
                if not g['accepted_for_research'] or c or merged['value'] in ('UNKNOWN','UNCERTAIN'):unresolved.append(k)
        full=None;full_gate={}
        if unresolved:
            if replay:
                if precomputed_full is None:raise ValueError('Missing counterfactual full Qwen output')
                full=copy.deepcopy(precomputed_full)
            else:full=self.qwen.full(text,structured)
            new=llm_factors(full)
            for k in unresolved:
                p=new.get(k,empty_pred(k,'FULL_QWEN_UNAVAILABLE'));valid=bool(full.get('valid'))
                ev=any(e.get('valid') for e in p.get('evidence',[]));known=p['value'] not in ('UNKNOWN','UNCERTAIN','NOT_SUPPORTED')
                accepted=valid and known and (ev or p['value'] in ('NO','NOT_VOTABLE') and self.policy.allow_absence) and language=='en'
                full_gate[k]={'accepted_for_research':accepted,'reasons':[] if accepted else ['UNKNOWN_SCHEMA_EVIDENCE_OR_LANGUAGE_NOT_SUPPORTED']}
                before=current[k];merged,c,t=reconcile(before,p,k,right_accepted=accepted,preferences=self.preferences.get('full'))
                current[k]=merged;trace.append({'stage':'GEAR3',**t});conflicts+=c
                if merged is p:origins[k]='FULL_QWEN_DIRECT'
            if not full.get('valid'):conflicts.append('FULL_QWEN_SCHEMA_FAILURE')
            elif full['parsed'].get('ambiguities'):conflicts.extend('FULL_QWEN_AMBIGUITY:'+a for a in full['parsed']['ambiguities'])
        # Authoritative structure is never silently overwritten by semantics.
        for k,p in structured.items():
            if k not in PREDICATES or not isinstance(p,dict) or 'value' not in p:continue
            if current[k]['value'] not in (p['value'],'UNKNOWN','UNCERTAIN'):conflicts.append(k+':STRUCTURE_SEMANTIC_CONFLICT')
            trace.append({'stage':'STRUCTURE','predicate':k,'rule':'AUTHORITATIVE_STRUCTURE_RETAINED','semantic_diagnostic':current[k]});current[k]=p;origins[k]='STRUCTURE'
        deadline=resolve_deadline(text,{'parsed':None,'structured':structured,'narrative':narrative},full,reference)
        if parser and parser.get('parser')=='PROWIDE':
            from iso_adapter.facts import deadline as iso_deadline
            authoritative=iso_deadline(parser['structure'],reference)
            if authoritative['comparisons']:
                if deadline['status']!='UNKNOWN' and authoritative['status']!=deadline['status']:conflicts.append('STRUCTURED_NARRATIVE_DEADLINE_CONFLICT')
                authoritative['narrative_diagnostic']=deadline;deadline=authoritative
        if deadline.get('conflict'):conflicts.append('DETERMINISTIC_DEADLINE_CONFLICT')
        d_evidence=[verify_evidence(text,c['text']) for c in deadline.get('candidates',[]) if 'text' in c]
        all_preds={**current,'deadline_status':{'value':deadline['status'],'source':'DETERMINISTIC_RULES','evidence':[e for e in d_evidence if e['valid']]}}
        confidence={}
        for k,p in all_preds.items():
            f=confidence_features(text,k,p,stage=origins.get(k,'DETERMINISTIC_RULES'),language=language,input_type=kind,conflict=bool(conflicts))
            v=None if f['force_review'] or not self.calibrator else self.calibrator.predict(k,f['features'],self.identity)
            confidence[k]={**f,'value':p['value'],'confidence':v,'confidence_kind':'CALIBRATED_ON_SYNTHETIC_POPULATION_ONLY' if v is not None else 'HEURISTIC / NOT YET CALIBRATED','manual_review_required':True,'automation_enabled':False,'evidence':p.get('evidence',[])}
        decision=decide(current,deadline,sorted(set(conflicts)))
        remaining=[k for k in PREDICATES if current[k]['value'] in ('UNKNOWN','UNCERTAIN','NOT_SUPPORTED') or (k in full_gate and not full_gate[k]['accepted_for_research'])]
        semantic_review=bool(remaining or conflicts or decision['classification']=='UNCERTAIN_MANUAL_REVIEW')
        return {'architecture':'LAYA_FIRST_CASCADE','pipeline_version':VERSION,'model_identity':self.identity,'input_hash':digest(text),'timestamp':now(),
            'calibrator_identity':digest({'model_identity':self.calibrator.model_identity,'reports':self.calibrator.reports}) if self.calibrator else None,
            'raw_source_preserved':True,'input_type':kind,'parser':parser,'structured_facts':structured,'laya':laya,'gear1_gates':gate1,'gear2':gear2,'gear2_gates':gate2,
            'full_qwen':full,'gear3_gates':full_gate,'escalation':{'gear2_requested':pending if self.policy.gear2 else [],'gear3_requested':unresolved,
                'gear2_reasons':{k:g['reasons'] for k,g in gate1.items() if not g['accepted_for_research']},'gear3_reasons':{k:gate2.get(k,gate1[k])['reasons'] for k in unresolved}},
            'reconciliation':{'trace':trace,'conflicts':sorted(set(conflicts))},'predicates':all_preds,'predicate_origins':origins,'deadline':deadline,'decision':decision,
            'semantic_review_required':semantic_review,'semantic_review_predicates':remaining,'manual_review_required':True,'confidence':confidence,
            'decision_confidence':decision_confidence(decision['classification'],confidence),'policy':asdict(self.policy),
            'resolved_by':'REVIEW' if semantic_review else 'FULL_QWEN' if full else 'CONSTRAINED_QWEN' if gear2 else 'LAYA',
            'latency_ms':(time.perf_counter()-started)*1000,'laya_service_ms':laya['latency_ms'],'gear2_ms':gear2['latency_ms'] if gear2 else 0,'full_qwen_ms':full['latency_ms'] if full else 0,
            'latency_scope':'COUNTERFACTUAL_REPLAY_NOT_ACTUAL_PIPELINE' if replay else 'ACTUAL_PIPELINE_WALL_EXCLUDES_MODEL_LOAD_AND_UPSTREAM_BATCH_QUEUE',
            'reference':reference,'language':language,'automation_enabled':False,'customer_accuracy':None}
