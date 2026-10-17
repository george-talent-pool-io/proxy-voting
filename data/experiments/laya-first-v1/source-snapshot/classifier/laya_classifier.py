"""Official Laya SDK boundary. Local checkpoint only; no remote inference/fallback."""
import hashlib
import json
import os
import time
from importlib.metadata import version
from pathlib import Path
from typing import Protocol
from classifier.preprocessing import normalise, VERSION as PREPROCESSING_VERSION
from classifier.schema import ClassificationResult, Decision
from classifier.thresholds import Thresholds

CONFIG_PATH=Path(__file__).with_name('config.json')

def prepare_config(cfg):
    import copy
    cfg=copy.deepcopy(cfg)
    order=cfg.get('question_order')
    if not order or len(order)!=len(set(order)) or set(order)!=set(cfg['questions']):raise ValueError('Explicit question_order must name every question exactly once')
    options=cfg.get('option_order',{})
    questions={}
    for key in order:
        q=cfg['questions'][key];labels=options.get(key,[])
        if len(labels)!=len(set(labels)) or set(labels)!=set(q['criteria']):raise ValueError(f'Explicit option_order required for {key}')
        questions[key]={**q,'criteria':{label:q['criteria'][label] for label in labels}}
    cfg['questions']=questions
    return cfg

def load_config(path=CONFIG_PATH):
    cfg=json.loads(Path(path).read_text())
    from datetime import date
    date.fromisoformat(cfg['evaluation_date'])
    Thresholds(cfg['high_threshold'],cfg['review_threshold'],cfg['automation_enabled'])
    required={'votable','share_blocking','poa_required','other_restriction', 'deadline_present' if cfg.get('deadline_mode')=='deterministic-v1' else 'deadline_status'}
    if set(cfg['questions'])!=required: raise ValueError('Invalid factor schema')
    if not 512<=cfg['max_len']<=8192 or not 1<=cfg['batch_size']<=32: raise ValueError('Invalid model budget')
    return prepare_config(cfg)

def config_version(cfg):
    return hashlib.sha256(json.dumps({'config':cfg,'preprocessing':PREPROCESSING_VERSION},sort_keys=True).encode()).hexdigest()

class VotingClassifier(Protocol):
    def classify(self,text:str)->ClassificationResult: ...
    def classify_batch(self,texts:list[str])->list[ClassificationResult]: ...

class LayaClassifier:
    def __init__(self,config=None,agent=None):
        self.config=prepare_config(config or load_config())
        self.configuration_version=config_version(self.config)
        self.policy=Thresholds(self.config['high_threshold'],self.config['review_threshold'],self.config['automation_enabled'])
        start=time.perf_counter()
        if agent is None:
            # Offline enforcement occurs before SDK/model imports. Missing weights fail clearly.
            os.environ.update(HF_HUB_OFFLINE='1',TRANSFORMERS_OFFLINE='1',HF_HUB_DISABLE_TELEMETRY='1',USE_TF='0')
            path=Path(self.config['model_path']).resolve()
            if not (path/'model.safetensors').is_file(): raise RuntimeError('Local Laya checkpoint missing. Run scripts/download_model.py')
            manifest_path=path/'model-manifest.json'
            if not manifest_path.is_file():raise RuntimeError('Model integrity manifest missing; rerun model setup')
            manifest=json.loads(manifest_path.read_text())
            if manifest['revision']!=self.config['checkpoint_revision']:raise RuntimeError('Configured model revision does not match installed model')
            for name,expected in manifest['files'].items():
                if hashlib.sha256((path/name).read_bytes()).hexdigest()!=expected:raise RuntimeError(f'Model integrity check failed: {name}')
            self.model_manifest=manifest
            import laya
            import torch
            torch.set_num_threads(4)
            device=os.environ.get('LAYA_DEVICE') or ('cuda' if torch.cuda.is_available() else 'mps' if torch.backends.mps.is_available() else 'cpu')
            self.agent=laya.load(str(path),device=device)
        else: self.agent=agent
        self.load_time_ms=(time.perf_counter()-start)*1000

    def classify(self,text): return self.classify_batch([text])[0]

    def classify_batch(self,texts):
        cleaned=[normalise(t) for t in texts]
        if any(not t for t in cleaned): raise ValueError('Empty notice text')
        if any(len(t)>2_000_000 for t in cleaned): raise ValueError('Notice exceeds 2 million character input limit')
        states=[f'Reference date (UTC): {self.config["evaluation_date"]}\n\nNotice:\n{t}' for t in cleaned]
        start=time.perf_counter()
        raw=self.agent.predict_batch(states,self.config['questions'],batch_size=self.config['batch_size'],
            max_len=self.config['max_len'],head_max_len=self.config['head_max_len'],sort_by_length=True)
        elapsed=(time.perf_counter()-start)*1000 / max(1,len(texts))
        if len(raw)!=len(texts): raise RuntimeError('Laya output count mismatch')
        return [self._decode(r,elapsed,text=t) for r,t in zip(raw,cleaned)]

    def _decode(self,raw,elapsed,text=''):
        answers=raw['answers']
        scores={k:answers[k]['probabilities'] for k in self.config['questions']}
        for k,q in self.config['questions'].items():
            if set(scores[k])!=set(q['criteria']): raise ValueError(f'Unexpected score labels for {k}')
            if answers[k]['choice'] not in scores[k]: raise ValueError('Invalid choice')
            if scores[k][answers[k]['choice']] < max(scores[k].values())-0.0001:raise ValueError('Laya choice is not a winning option')
        confidence=min(max(s.values()) for s in scores.values())
        chosen={k:v['choice'] for k,v in answers.items()}
        flag=lambda k: True if chosen[k]=='YES' else False if chosen[k]=='NO' else None
        deadline_evidence=None
        if self.config.get('deadline_mode')=='deterministic-v1':
            from classifier.deadlines import extract_deadline
            deadline_evidence=extract_deadline(text,self.config.get('evaluation_timestamp',self.config['evaluation_date']),chosen['deadline_present'])
            chosen['deadline_status']=deadline_evidence['status']
        decision=Decision(votable=chosen['votable'],share_blocking=flag('share_blocking'),poa_required=flag('poa_required'),
            other_restriction=flag('other_restriction'),deadline_status=chosen['deadline_status'])
        reasons=[]
        if decision.votable=='UNCERTAIN': reasons.append('Ambiguous voting opportunity')
        if any(x is None for x in [decision.share_blocking,decision.poa_required,decision.other_restriction]): reasons.append('Uncertain restriction')
        if decision.votable=='YES' and decision.deadline_status=='UNKNOWN': reasons.append('No verified voting deadline')
        usage=raw.get('usage',{})
        if usage.get('truncated'): reasons.append('Model context truncated; inspect complete source')
        if usage.get('options'): reasons.append('Option token budget warning')
        if decision.votable=='NO' and any([decision.share_blocking,decision.poa_required,decision.other_restriction]): reasons.append('Conflicting voting and restriction decisions')
        action=self.policy.action(confidence,bool(reasons))
        if not self.policy.automation_enabled: reasons.append('Automation disabled pending validation')
        decision.manual_review_required=action!='AUTO_CLASSIFY'
        return ClassificationResult(classification=decision.status(),decision=decision,confidence=confidence,
            scores=scores,raw_answers=answers,usage=usage,model_name=f'{self.config["checkpoint"]}/{self.config["subfolder"]}',
            model_version=self.config['checkpoint_revision'],sdk_version=version('laya'),configuration_version=self.configuration_version,
            processing_time_ms=elapsed,action=action,review_reasons=reasons,deadline_evidence=deadline_evidence,
            confidence_definition='Minimum winning native semantic factor probability; not a probability of the derived status or correctness of date extraction' if deadline_evidence is not None else 'Minimum winning option probability across the five factors; not a probability of the derived status')
