import json
from pathlib import Path
import pytest
from training.framework.profiles import listing, seed_readiness


def test_domain_recipes_are_distinct_from_execution_smokes():
    rows = {r['id']:r for r in listing()}
    assert rows['laya-smoke']['purpose'] == 'SMOKE_TEST'
    assert rows['qwen-mlx-smoke']['spec']['max_steps'] == 2
    domain = rows['laya-domain-linux']['spec']
    assert domain['epochs'] >= 4 and not domain['freeze_encoder']
    assert domain['encoder_learning_rate'] < domain['learning_rate']
    assert domain['laya_gradient_checkpointing']
    assert rows['qwen-domain-mac']['spec']['max_steps'] > 2
    assert rows['qwen-domain-mac']['spec']['lora_layers'] > 1
    assert all(not r['trained_model'] and not r['automation_enabled'] for r in rows.values())


def test_linux_profile_listing_does_not_offer_mlx_or_mps():
    rows = listing(linux_only=True)
    assert rows and all(r['spec']['device'] != 'mps' and r['spec']['backend'] != 'MLX_QLORA' for r in rows)


@pytest.mark.parametrize('origin', ['OFFICIAL_FOUNDATION','AI_TEST_DERIVATIVE','CUSTOMER_DERIVATIVE','UNTRUSTED'])
def test_origin_or_claimed_receipt_cannot_qualify_a_domain_model(origin):
    status = seed_readiness({'origin':origin,'quality_receipt_supplied':True,'quality_receipt':{'accuracy':1.0}})
    assert not status['domain_model_qualified'] and not status['automation_enabled']
    assert 'qualification' in status['explanation']
