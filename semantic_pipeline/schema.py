"""Model-neutral factor schema; absence of capability differs from abstention."""
from typing import Literal
from pydantic import BaseModel, ConfigDict

Tri = Literal['YES', 'NO', 'UNKNOWN']
RESTRICTIONS = ('share_blocking', 'poa_required', 'registration_required',
    'beneficial_owner_disclosure_required', 'holding_confirmation_required',
    'split_voting_restricted', 'securities_lending_recall_required', 'other_voting_restriction')
PREDICATES = ('votability',) + RESTRICTIONS
NOT_SUPPORTED = 'NOT_SUPPORTED'

class StrictModel(BaseModel):
    model_config = ConfigDict(extra='forbid', strict=True)

class DeadlineInformation(StrictModel):
    deadline_mentioned: bool
    deadline_text: str | None

class Evidence(StrictModel):
    votability: list[str]
    share_blocking: list[str]
    poa_required: list[str]
    registration_required: list[str]
    beneficial_owner_disclosure_required: list[str]
    holding_confirmation_required: list[str]
    split_voting_restricted: list[str]
    securities_lending_recall_required: list[str]
    other_voting_restriction: list[str]

class SemanticResult(StrictModel):
    votability: Literal['VOTABLE', 'NOT_VOTABLE', 'UNCERTAIN']
    share_blocking: Tri
    poa_required: Tri
    registration_required: Tri
    beneficial_owner_disclosure_required: Tri
    holding_confirmation_required: Tri
    split_voting_restricted: Tri
    securities_lending_recall_required: Tri
    other_voting_restriction: Tri
    deadline_information: DeadlineInformation
    evidence: Evidence
    ambiguities: list[str]
