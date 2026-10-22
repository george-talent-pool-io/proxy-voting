"""The candidate sampler cannot change split roles or learn from holdouts."""
import pytest
from scripts.upgrade_domain_candidate import diverse_sample
from tests.unit.test_training_framework import example


def test_domain_sampling_is_order_independent_and_preserves_targets():
    rows=[example(str(i)) for i in range(8)]
    for i,r in enumerate(rows):
        r.source_hash=str(i);r.generation_family='family-'+str(i%3)
    rows[-1].target.votability='UNCERTAIN'
    sampled=diverse_sample(rows,4,'TRAIN')
    assert [r.id for r in sampled]==[r.id for r in diverse_sample(list(reversed(rows)),4,'TRAIN')]
    assert len({r.id for r in sampled})==4
    assert len({r.generation_family for r in sampled})==3
    assert any(r.target.votability=='UNCERTAIN' for r in sampled)


@pytest.mark.parametrize('role', ['CALIBRATION','FROZEN_TEST','TRAIN'])
def test_domain_sampling_refuses_protected_or_mixed_roles(role):
    with pytest.raises(ValueError,match='declared'):
        diverse_sample([example('v','VALIDATION')],1,role)


def test_domain_sampling_refuses_insufficient_support():
    with pytest.raises(ValueError,match='support'):
        diverse_sample([example()],2,'TRAIN')
