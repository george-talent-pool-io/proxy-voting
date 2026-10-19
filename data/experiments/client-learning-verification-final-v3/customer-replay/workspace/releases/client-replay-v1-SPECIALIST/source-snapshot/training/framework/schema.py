"""Shared annotation and job contracts for Laya and local generative models."""
from enum import Enum
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator

from classifier.preprocessing import source_hash
from semantic_pipeline.schema import SemanticResult, PREDICATES


class Origin(str, Enum):
    AI_AUTHORED = 'AI_AUTHORED'
    AI_REVIEWED = 'AI_REVIEWED'
    HUMAN_REVIEWED = 'HUMAN_REVIEWED'
    EXPERT_REVIEWED = 'EXPERT_REVIEWED'


class Provenance(BaseModel):
    model_config = ConfigDict(extra='forbid')
    origin: Origin
    author: str = Field(min_length=1)
    model_id: str | None = None
    method: str = Field(min_length=1)
    reviewed_at: str | None = None
    expert_attested: bool = False
    source_reference: str = Field(min_length=1)
    revision: str = Field(min_length=1)

    @model_validator(mode='after')
    def honest_origin(self):
        if self.origin in (Origin.AI_AUTHORED, Origin.AI_REVIEWED):
            if not self.model_id:
                raise ValueError('AI labels require generator/reviewer model identity')
            if self.expert_attested:
                raise ValueError('AI labels cannot attest human expertise')
        if self.origin == Origin.EXPERT_REVIEWED and not self.expert_attested:
            raise ValueError('Expert review requires explicit expertise attestation')
        return self


class Example(BaseModel):
    model_config = ConfigDict(extra='forbid')
    id: str = Field(min_length=1)
    text: str = Field(min_length=1, max_length=2_000_000)
    source_hash: str
    group_id: str = Field(min_length=1)
    generation_family: str | None = None
    split: Literal['TRAIN', 'VALIDATION']
    language: str = 'en'
    structured_context: dict = Field(default_factory=dict)
    target: SemanticResult
    provenance: Provenance

    @model_validator(mode='after')
    def check_source(self):
        if not self.text.strip() or source_hash(self.text) != self.source_hash:
            raise ValueError('Empty source or source hash mismatch')
        quotes = [q for k in PREDICATES for q in getattr(self.target.evidence, k)]
        if self.target.deadline_information.deadline_text is not None:
            quotes.append(self.target.deadline_information.deadline_text)
        if any(not q or q not in self.text for q in quotes):
            raise ValueError('Training evidence must be an exact nonempty source substring')
        for key in PREDICATES:
            if getattr(self.target, key) in ('YES', 'VOTABLE') and not getattr(self.target.evidence, key):
                raise ValueError(f'Positive target requires source evidence: {key}')
        return self


class TrainSpec(BaseModel):
    model_config = ConfigDict(extra='forbid')
    backend: Literal['LAYA_SDK', 'TRANSFORMERS_PEFT', 'MLX_QLORA']
    family: Literal['LAYA', 'QWEN', 'GLM', 'OTHER_CAUSAL_LM']
    model_path: str = Field(min_length=1)
    base_model_id: str = Field(min_length=1)
    base_revision: str = Field(min_length=1)
    seed: int = 42
    epochs: int = Field(default=1, ge=1, le=100)
    learning_rate: float = Field(default=0.00002, gt=0, le=0.1)
    batch_size: int = Field(default=1, ge=1, le=128)
    gradient_accumulation: int = Field(default=8, ge=1, le=1024)
    max_length: int = Field(default=4096, ge=128, le=131072)
    lora_rank: int = Field(default=8, ge=1, le=256)
    lora_alpha: int = Field(default=16, ge=1, le=512)
    target_modules: list[str] = Field(default_factory=lambda: ['q_proj', 'v_proj'])
    device: Literal['cpu', 'mps', 'cuda'] = 'cpu'
    dtype: Literal['float32', 'float16', 'bfloat16'] = 'float32'
    max_steps: int | None = Field(default=None, ge=1)
    freeze_encoder: bool = True
    runtime_python: str | None = None
    lora_layers: int = Field(default=1, ge=1)
    generation_tokens: int = Field(default=2048, ge=32, le=8192)
    # A frozen seed binds both initial weights and serving criteria. The parent
    # optimizer is intentionally never resumed across customer corpora.
    parent_seed_path: str | None = None
    initial_adapter_path: str | None = None
    encoder_learning_rate: float | None = Field(default=None, gt=0, le=.01)
    laya_loss: Literal['soft-ce', 'rlcd'] = 'soft-ce'
    laya_gradient_checkpointing: bool | None = None
    laya_sdk_validation: bool = True
    mps_memory_fraction: float | None = Field(default=None,ge=.1,le=.7)
    training_timeout_seconds: int = Field(default=7200,ge=60,le=604800)

    @model_validator(mode='after')
    def compatible_backend(self):
        if (self.backend == 'LAYA_SDK') != (self.family == 'LAYA'):
            raise ValueError('Laya uses its official SDK; generative models use the PEFT backend')
        if self.device == 'cpu' and self.dtype == 'float16':
            raise ValueError('Use float32 or supported bfloat16 on CPU')
        if self.backend == 'LAYA_SDK' and self.max_steps is not None:
            raise ValueError('Laya SDK uses epochs; max_steps is not supported')
        if self.mps_memory_fraction is not None and self.device!='mps':
            raise ValueError('MPS memory fraction applies only to the MPS device')
        return self
