"""Routing is experimental, separate from permission to automate a customer decision."""
from dataclasses import dataclass, asdict
from semantic_pipeline.schema import PREDICATES, NOT_SUPPORTED

@dataclass(frozen=True)
class RoutingConfig:
    min_score: float | None = None
    min_margin: float | None = None
    unknown: bool = True
    unsupported: bool = True
    conflict: bool = True
    max_chars: int = 12000
    require_positive_evidence: bool = False
    def __post_init__(self):
        for value in (self.min_score,self.min_margin):
            if value is not None and not 0<=value<=1: raise ValueError('Invalid routing threshold')
        if self.max_chars < 1: raise ValueError('Invalid input size')

def escalate(laya, structured, text, config):
    reasons = []
    predictions = laya['predicates']
    if config.unsupported and any(predictions.get(k,{}).get('value',NOT_SUPPORTED)==NOT_SUPPORTED for k in PREDICATES):
        reasons.append('UNSUPPORTED_REQUIRED_PREDICATE')
    if config.unknown and any(a['value'] in ('UNKNOWN','UNCERTAIN') for a in predictions.values()): reasons.append('UNKNOWN_LAYA_OUTPUT')
    if config.min_score is not None and any(a.get('confidence') is not None and a['confidence']<config.min_score for a in predictions.values()): reasons.append('LOW_LAYA_SCORE')
    if config.min_margin is not None and any(a.get('margin') is not None and a['margin']<config.min_margin for a in predictions.values()): reasons.append('LOW_LAYA_MARGIN')
    if config.conflict and any(a.get('conflict') for a in predictions.values()): reasons.append('CONFLICTING_PASSAGES')
    if config.conflict and 'votability' in structured and predictions.get('votability',{}).get('value') not in ('UNCERTAIN',NOT_SUPPORTED,structured['votability']['value']): reasons.append('STRUCTURE_SEMANTIC_CONFLICT')
    vote=predictions.get('votability',{}).get('value')
    if config.conflict and vote=='NOT_VOTABLE' and any(a['value']=='YES' for k,a in predictions.items() if k not in ('votability','deadline_status')): reasons.append('VOTABILITY_RESTRICTION_CONFLICT')
    if laya.get('truncated'): reasons.append('LAYA_TRUNCATED')
    if len(text)>config.max_chars: reasons.append('LONG_INPUT')
    if config.require_positive_evidence and any(a['value']=='YES' and not a.get('evidence') for a in predictions.values()): reasons.append('POSITIVE_EVIDENCE_UNAVAILABLE')
    return {'escalated': bool(reasons), 'reasons': reasons, 'configuration':asdict(config)}
