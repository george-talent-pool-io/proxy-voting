"""Correctness confidence is null until independent calibration evaluation passes.

Heuristic bands are explanations, never probability estimates. Synthetic
calibration, if valid, applies only to its documented synthetic population.
"""
import re,math,json
from pathlib import Path
from datetime import datetime,timezone
import numpy as np
from sklearn.feature_extraction import DictVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import brier_score_loss
from sklearn.isotonic import IsotonicRegression
import joblib
VERSION='predicate-correctness-features-v1'
CRITICAL=('votability','share_blocking','poa_required','registration_required')

def features(text,predicate,result,*,language='en',input_type='UNSTRUCTURED_NOTICE',schema_valid=True,schema_repairs=0,repeat_agreement=None,deterministic_conflict=False):
    ev=result.get('evidence',[]);valid=[e for e in ev if e.get('valid')]
    probs=result.get('raw_model_probability') or {};ordered=sorted(probs.values(),reverse=True)
    unknown=result.get('value') in ('UNKNOWN','UNCERTAIN','NOT_SUPPORTED')
    conflict=deterministic_conflict or bool(result.get('conflict')) or bool(re.search(r'neither has priority|no priority rule|unresolved conflict|two current instructions conflict',text,re.I))
    ood=[]
    if language!='en':ood.append('LANGUAGE_NOT_IN_INITIAL_ENGLISH_CONFIDENCE_POPULATION')
    if len(text)>60000:ood.append('EXTREME_LENGTH')
    if '\ufffd' in text or '\x00' in text:ood.append('CORRUPTION')
    if result.get('truncated') or result.get('error')=='CONTEXT_LIMIT_NO_TRUNCATION':ood.append('TRUNCATION_OR_CONTEXT_RISK')
    if schema_repairs>1:ood.append('REPEATED_SCHEMA_REPAIR')
    if input_type not in ('UNSTRUCTURED_NOTICE','PROWIDE_PARSEABLE','LENIENT_ISO_RECOVERABLE'):ood.append('UNRECOGNISED_FORMAT')
    data={'predicate':predicate,'language':language,'input_type':input_type,'text_length':len(text),
        'evidence_present':bool(ev),'evidence_exact_count':len(valid),'invalid_evidence_count':sum(not e.get('valid') for e in ev),
        'direct_evidence_candidate':bool(valid),'evidence_entailment_independently_verified':False,
        'supporting_passages':len(valid),'opposing_passages':sum(p.get('result',{}).get('value')!=result.get('value') for p in result.get('passage_scores',[])),
        'contradiction':conflict,'supersession_cue':bool(re.search(r'supersed|replac|final amendment|withdrawn',text,re.I)),
        'schema_valid':schema_valid,'schema_repairs':schema_repairs,'unknown':unknown,'ood':bool(ood),
        'raw_top_probability':ordered[0] if ordered else None,'raw_margin':ordered[0]-ordered[1] if len(ordered)>1 else None,
        'raw_entropy':-sum(v*math.log(v) for v in probs.values() if v) if probs else None,
        'repeat_agreement':repeat_agreement,'unusual_formatting':bool(re.search(r'<system>|:70E:|\x00|role.{0,4}system',text,re.I)),
        'model_self_assessment':None,'token_signal_available':bool(probs)}
    force=unknown or conflict or bool(ood) or not schema_valid or any(not e.get('valid') for e in ev) or data['unusual_formatting']
    positive=result.get('value') in ('YES','VOTABLE')
    band='UNRESOLVED' if unknown else 'LOW' if force or positive and not valid else 'HIGH' if valid and schema_repairs==0 else 'MEDIUM'
    return {'version':VERSION,'features':data,'heuristic_band':band,'force_review':force,'ood_reasons':ood,
        'confidence':None,'confidence_kind':'HEURISTIC / NOT YET CALIBRATED','confidence_explanation':{'exact_evidence':bool(valid),'contradiction':conflict,'schema_valid':schema_valid,'repeat_stability':repeat_agreement,'ood_reasons':ood}}

def numeric_features(data):
    out={}
    for k,v in data.items():
        if v is None:out[k+'_missing']=True
        elif isinstance(v,(str,bool,int,float)):out[k]=v
    return out

def calibration_metrics(y,p,bins=10):
    if not len(y):return {'n':0,'brier':None,'ece':None,'bins':[]}
    y=np.asarray(y);p=np.asarray(p);out=[];ece=0
    for i in range(bins):
        mask=(p>=i/bins)&((p<(i+1)/bins) if i<bins-1 else (p<=1))
        n=int(mask.sum())
        if not n:continue
        confidence=float(p[mask].mean());accuracy=float(y[mask].mean());ece+=n/len(y)*abs(confidence-accuracy)
        out.append({'lower':i/bins,'upper':(i+1)/bins,'n':n,'mean_probability':confidence,'observed_correctness':accuracy})
    return {'n':len(y),'brier':float(brier_score_loss(y,p)),'ece':ece,'bins':out,'correct':int(y.sum()),'wrong':int((1-y).sum())}

class CorrectnessCalibrator:
    def __init__(self,model_identity):self.model_identity=model_identity;self.models={};self.reports={}
    def fit(self,records):
        # Caller supplies group-isolated CALIBRATION folds; disallow any other role.
        if any(r['split']!='CALIBRATION' for r in records):raise ValueError('Calibration may only use CALIBRATION')
        groups={f:{r['duplicate_group'] for r in records if r['calibration_fold']==f} for f in ['FIT','EVALUATION']}
        if groups['FIT']&groups['EVALUATION']:raise ValueError('Calibration fit/evaluation leakage')
        for key in sorted({r['predicate'] for r in records}):
            fit=[r for r in records if r['predicate']==key and r['calibration_fold']=='FIT'];test=[r for r in records if r['predicate']==key and r['calibration_fold']=='EVALUATION']
            counts={str(v):sum(r['correct']==v for r in fit) for v in [False,True]}
            if len(fit)<100 or len(test)<50 or min(counts.values())<10:
                self.reports[key]={'status':'INSUFFICIENT_CALIBRATION_SUPPORT','fit_n':len(fit),'evaluation_n':len(test),'fit_correctness_counts':counts};continue
            vector=DictVectorizer(sparse=True);x=vector.fit_transform([numeric_features(r['features']) for r in fit])
            model=LogisticRegression(C=.1,max_iter=2000,random_state=42).fit(x,[r['correct'] for r in fit])
            p=model.predict_proba(vector.transform([numeric_features(r['features']) for r in test]))[:,list(model.classes_).index(True)]
            m=calibration_metrics([r['correct'] for r in test],p)
            # Research gate, not a regulatory or customer-automation requirement.
            valid=m['ece']<=.10 and m['wrong']>=5 and m['correct']>=20
            self.reports[key]={'status':'SYNTHETIC_POPULATION_CALIBRATION_VALIDATED' if valid else 'CALIBRATION_QUALITY_NOT_ESTABLISHED','method':'L2 logistic correctness calibration; fixed C=.1','evaluation':m,'fit_n':len(fit),'scope':'Only synthetic calibration population; not customer confidence'}
            if all(r['features'].get('raw_top_probability') is not None for r in fit+test) and len({r['features']['raw_top_probability'] for r in fit})>=10:
                iso=IsotonicRegression(out_of_bounds='clip').fit([r['features']['raw_top_probability'] for r in fit],[r['correct'] for r in fit])
                ip=iso.predict([r['features']['raw_top_probability'] for r in test])
                self.reports[key]['isotonic_diagnostic_not_selected']=calibration_metrics([r['correct'] for r in test],ip)
                self.reports[key]['isotonic_note']='Diagnostic comparison only; fixed logistic method remains selected. Do not model-select on these held-out evaluation outcomes.'
            if valid:self.models[key]=(vector,model)
        return self.reports
    def predict(self,key,data,identity):
        if identity!=self.model_identity:raise ValueError('Calibrator belongs to another model/prompt configuration')
        if key not in self.models:return None
        vec,model=self.models[key]
        return float(model.predict_proba(vec.transform([numeric_features(data)]))[0,list(model.classes_).index(True)])
    def save(self,path):
        if Path(path).exists():raise ValueError('Never overwrite a fitted calibrator')
        joblib.dump(self,path)
    @classmethod
    def load(cls,path,identity):
        value=joblib.load(path)
        if value.model_identity!=identity:raise ValueError('Calibrator model identity mismatch')
        return value

def confidence_output(text,key,pred,*,calibrator=None,identity=None,**kwargs):
    result=features(text,key,pred,**kwargs)
    p=None if result['force_review'] or calibrator is None else calibrator.predict(key,result['features'],identity)
    if p is not None:result.update(confidence=p,confidence_kind='CALIBRATED_ON_SYNTHETIC_POPULATION_ONLY',calibration_scope='Does not establish customer correctness probability')
    result.update(value=pred['value'],evidence=pred.get('evidence',[]),manual_review_required=True,automation_enabled=False)
    return result

def decisive_predicates(status,predicates):
    if status=='NOT_VOTABLE':return ['votability']
    if status=='DEADLINE_PASSED':return ['votability','deadline_status']
    if status=='VOTABLE_WITH_RESTRICTION':
        yes=[k for k,v in predicates.items() if k not in ('votability','deadline_status') and v['value']=='YES']
        return ['votability']+(['deadline_status'] if 'deadline_status' in predicates else [])+yes
    if status=='VOTABLE':return list(predicates)
    return [k for k,v in predicates.items() if v['value'] in ('UNKNOWN','UNCERTAIN')]

def decision_confidence(status,predicates):
    keys=decisive_predicates(status,predicates);values=[predicates.get(k,{}).get('confidence') for k in keys]
    trust=min(values) if values and all(v is not None for v in values) else None
    return {'decisive_predicates':keys,'minimum_decisive_trust_score':trust,'calibrated_decision_confidence':None,
        'definition':'Minimum predicate confidence is a derived trust score, not a calibrated joint probability of the final decision.','manual_review_required':True,'automation_enabled':False}
