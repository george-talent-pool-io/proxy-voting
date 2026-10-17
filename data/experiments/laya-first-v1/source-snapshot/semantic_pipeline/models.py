"""Adapters preserve native output and declare each model's actual capabilities."""
import time
from pathlib import Path
from classifier.laya_classifier import LayaClassifier, load_config
from hybrid.semantics import NarrowLaya
from semantic_pipeline.schema import PREDICATES, RESTRICTIONS, NOT_SUPPORTED
from semantic_pipeline.fallback import digest
from semantic_pipeline.evidence import verify_evidence

FINE_CONFIG = 'data/models/supplied-synthetic-v1/encoder-4ep/voting-config.json'
NARROW_PATH = 'data/models/narrow-v1'

def factor(value, source, scores=None, evidence=None, **extra):
    scores = scores or {}
    rank = sorted(scores.values(), reverse=True)
    return {'value': value, 'source': source, 'scores': scores,
        'confidence': max(rank) if rank else None,
        'margin': rank[0]-rank[1] if len(rank)>1 else None,
        'evidence': evidence or [], **extra}

class WholeLaya:
    def __init__(self, fine=False, classifier=None):
        self.classifier = classifier or LayaClassifier(load_config(FINE_CONFIG) if fine else None)
        self.checkpoint = self.classifier.config['model_path']
    def analyse(self, text):
        raw = self.classifier.classify(text).model_dump(mode='json')
        out = {k: factor(NOT_SUPPORTED, 'LAYA_WHOLE_TEXT_UNSUPPORTED') for k in PREDICATES}
        for key in ('votable','share_blocking','poa_required','other_restriction','deadline_status'):
            a = raw['raw_answers'][key]
            target = 'votability' if key == 'votable' else key
            value = {'YES':'VOTABLE','NO':'NOT_VOTABLE'}.get(a['choice'],a['choice']) if key=='votable' else a['choice']
            out[target] = factor(value,'LAYA_WHOLE_TEXT',a['probabilities'])
        return {'predicates': out, 'raw': raw, 'checkpoint': self.checkpoint,
            'model_version': raw['model_version'], 'configuration_version': raw['configuration_version'],
            'supervised_targets':['votable','share_blocking','poa_required','other_restriction','deadline_status'],
            'latency_ms': raw['processing_time_ms'], 'truncated': bool(raw['usage'].get('truncated'))}

class NarrowAdapter:
    def __init__(self, model=None):
        self.model = model or NarrowLaya(NARROW_PATH)
        # Generic Laya choice inference, NOT supervised holding-confirmation training.
        self.model.questions['holding_confirmation_required'] = {
            'type':'choice', 'instructions':'Does this passage require a holdings certificate or proof/confirmation of ownership as a condition for exercising the current vote? Respect negation, optionality and current superseding terms. Ordinary record-date eligibility alone is not a certificate requirement.',
            'criteria': {'YES':'A current mandatory holdings certificate/proof is required to vote',
                'NO':'No such proof requirement is stated or it is explicitly waived',
                'UNKNOWN':'The requirement is contradictory or genuinely unclear'}}
        self.configuration_version = digest({'historical_config':self.model.config_hash,
            'questions':self.model.questions, 'version':'narrow-adapter-2'})
    def analyse(self, text):
        raw = self.model.analyse(text)
        out = {}
        for key,a in raw['predicates'].items():
            target = 'votability' if key=='votable' else key
            value = {'YES':'VOTABLE','NO':'NOT_VOTABLE','UNKNOWN':'UNCERTAIN'}.get(a['value'],a['value']) if key=='votable' else a['value']
            ev = a.get('evidence')
            out[target] = {**a, 'value':value, 'source':'LAYA_NARROW',
                'evidence':[verify_evidence(text,ev['text'])] if ev else []}
        return {'predicates':out, 'raw':raw, 'checkpoint':self.model.model_path,
            'model_version':self.model.model_version, 'configuration_version':self.configuration_version,
            'supervised_targets':['votable','share_blocking','poa_required'],
            'transfer_only_targets':[k for k in self.model.questions if k not in ('votable','share_blocking','poa_required')],
            'latency_ms':raw['processing_time_ms'],
            'truncated':any(a.get('truncated') for rows in raw['passage_predictions'].values() for a in rows)}
