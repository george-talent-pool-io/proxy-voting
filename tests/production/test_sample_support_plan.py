import pytest
from scipy.stats import beta
from scripts.plan_qualification_support import plan,required_groups


def test_precision_plan_matches_operating_gate_and_detects_impossible_small_study():
    p=plan(validation_groups=115,frozen_groups=355)
    assert p['required_accepted_validation_groups']==237
    assert p['required_accepted_frozen_groups']==149
    assert not p['validation_structurally_sufficient'] and p['frozen_structurally_sufficient']
    assert not p['automation_enabled']


@pytest.mark.parametrize('errors',[0,1,5])
def test_exact_bound_and_minimality_with_observed_group_errors(errors):
    n=required_groups(.98,candidates=6,errors=errors)
    assert beta.ppf(.05/6,n-errors,errors+1)>=.98
    assert beta.ppf(.05/6,n-1-errors,errors+1)<.98


@pytest.mark.parametrize('kwargs',[{'precision':1.},{'precision':float('nan')},{'precision':.98,'candidates':0},
                                 {'precision':.98,'errors':-1},{'precision':.98,'candidates':True}])
def test_invalid_or_unprovable_targets_refused(kwargs):
    with pytest.raises(ValueError):required_groups(**kwargs)
