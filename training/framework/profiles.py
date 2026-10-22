"""Separate execution smoke budgets from domain-training candidates.

A recipe is not a trained model or a customer qualification. These profiles
never start training, change a pinned foundation, or authorise automation.
"""
import json
from pathlib import Path
from training.framework.schema import TrainSpec

ROOT = Path(__file__).with_name('specs')
PROFILES = (
    ('laya-smoke', 'laya.json', 'SMOKE_TEST', 'Checks training mechanics; not a domain-learning recommendation.'),
    ('qwen-mlx-smoke', 'qwen38-mlx.json', 'SMOKE_TEST', 'Two optimizer steps qualify execution only.'),
    ('laya-domain-linux', 'laya-domain-cpu.json', 'DOMAIN_TRAINING_CANDIDATE', 'Full-encoder candidate; select using customer validation.'),
    ('laya-domain-mac', 'laya-domain-mps.json', 'DOMAIN_TRAINING_CANDIDATE', 'Full-encoder development-Mac candidate; independent qualification required.'),
    ('qwen-domain-mac', 'qwen38-domain-mlx.json', 'DOMAIN_TRAINING_CANDIDATE', 'Bounded multi-layer adapter candidate; quality and capacity remain to be measured.'),
)


def listing(*, linux_only=False):
    rows = []
    for ident, filename, purpose, description in PROFILES:
        spec = TrainSpec.model_validate_json((ROOT / filename).read_text())
        if linux_only and (spec.device == 'mps' or spec.backend == 'MLX_QLORA'):
            continue
        rows.append({'id': ident, 'purpose': purpose, 'description': description,
                     'spec': spec.model_dump(), 'spec_file': 'training/framework/specs/' + filename,
                     'requires_validation_selection': True, 'trained_model': False,
                     'customer_accuracy': None, 'automation_enabled': False})
    return rows


def seed_readiness(seed):
    """Origin is not an accuracy certificate; untrusted receipt text cannot promote."""
    origin = seed.get('origin')
    state = {'OFFICIAL_FOUNDATION': 'FOUNDATION_ONLY_NOT_VOTING_DOMAIN_QUALIFIED',
             'AI_TEST_DERIVATIVE': 'AI_TEST_MODEL_NOT_CUSTOMER_QUALIFIED',
             'CUSTOMER_DERIVATIVE': 'CUSTOMER_MODEL_REQUIRES_INDEPENDENT_QUALIFICATION'}.get(origin, 'UNKNOWN_CHECKPOINT_ORIGIN')
    return {'status': state, 'domain_model_qualified': False,
            'quality_receipt_declared': bool(seed.get('quality_receipt_supplied')),
            'explanation': 'Frozen identity and a declared receipt are not a passed deployment qualification.',
            'integrity_scope': 'Metadata listing; weight integrity is verified at execution.',
            'automation_enabled': False}
