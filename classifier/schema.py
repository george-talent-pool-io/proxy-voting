from enum import StrEnum
from typing import Literal
from pydantic import BaseModel, ConfigDict, Field, model_validator

class Status(StrEnum):
    VOTABLE='VOTABLE'
    NOT_VOTABLE='NOT_VOTABLE'
    VOTABLE_WITH_RESTRICTION='VOTABLE_WITH_RESTRICTION'
    POA_REQUIRED='POA_REQUIRED'
    SHARE_BLOCKING='SHARE_BLOCKING'
    DEADLINE_PASSED='DEADLINE_PASSED'
    UNCERTAIN_MANUAL_REVIEW='UNCERTAIN_MANUAL_REVIEW'

class Decision(BaseModel):
    model_config=ConfigDict(extra='forbid')
    votable: Literal['YES','NO','UNCERTAIN']
    share_blocking: bool | None = False
    poa_required: bool | None = False
    other_restriction: bool | None = False
    deadline_status: Literal['OPEN','PASSED','UNKNOWN']='UNKNOWN'
    manual_review_required: bool=False

    def status(self) -> Status:
        if self.votable=='UNCERTAIN': return Status.UNCERTAIN_MANUAL_REVIEW
        if self.votable=='NO': return Status.NOT_VOTABLE
        if self.deadline_status=='PASSED': return Status.DEADLINE_PASSED
        flags=[self.share_blocking,self.poa_required,self.other_restriction]
        if any(x is None for x in flags): return Status.UNCERTAIN_MANUAL_REVIEW
        if sum(bool(x) for x in flags)>1 or self.other_restriction: return Status.VOTABLE_WITH_RESTRICTION
        if self.poa_required: return Status.POA_REQUIRED
        if self.share_blocking: return Status.SHARE_BLOCKING
        return Status.VOTABLE

class ClassificationResult(BaseModel):
    classification: Status
    decision: Decision
    confidence: float | None = Field(default=None,ge=0,le=1,allow_inf_nan=False)
    confidence_definition: str='Minimum winning option probability across the five factors; not a probability of the derived status'
    scores: dict[str,dict[str,float]]
    raw_answers: dict
    usage: dict
    model_name: str
    model_version: str
    sdk_version: str
    configuration_version: str
    processing_time_ms: float = Field(ge=0,allow_inf_nan=False)
    timing_definition: str='Amortised batch wall time per record'
    action: Literal['AUTO_CLASSIFY','CLASSIFY_AND_REVIEW','MANUAL_REVIEW']
    review_reasons: list[str]
    deadline_evidence: dict | None = None

    @model_validator(mode='after')
    def validate_scores(self):
        import math
        for scores in self.scores.values():
            if not scores or any(not math.isfinite(v) or not 0<=v<=1 for v in scores.values()):
                raise ValueError('Invalid model probability')
            # SDK rounds each option to 4 decimals; do not silently renormalise.
            if abs(sum(scores.values())-1)>0.001:
                raise ValueError('Option probabilities do not sum to one')
        if self.classification != self.decision.status(): raise ValueError('Status does not match factors')
        return self
