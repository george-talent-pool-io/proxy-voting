"""Plan accepted-group support before an expensive model qualification run.

This is an exact binomial one-sided precision-bound calculation, not an
accuracy prediction. A group fails if any accepted decision in it is wrong.
Exchangeable independent groups and representative labels remain assumptions.
"""
import argparse
import json
import math

from scipy.stats import beta


def required_groups(precision, *, alpha=.05, candidates=1, errors=0, min_groups=100):
    if (not 0 < precision < 1 or not 0 < alpha < 1 or isinstance(candidates,bool) or
            not isinstance(candidates,int) or candidates < 1 or isinstance(errors,bool) or
            not isinstance(errors,int) or errors < 0 or not isinstance(min_groups,int) or min_groups < 1):
        raise ValueError('Finite precision, alpha, candidate count, errors and minimum support required')
    adjusted = alpha/candidates
    def passes(n):
        return n > errors and float(beta.ppf(adjusted,n-errors,errors+1)) >= precision
    if errors == 0:
        n=max(min_groups,math.ceil(math.log(adjusted)/math.log(precision)))
        while not passes(n):n+=1
        return n
    high=max(min_groups,errors+1)
    while not passes(high):
        high*=2
        if high>10_000_000:raise ValueError('Requested support exceeds practical planner limit')
    low=max(min_groups,errors+1)
    while low<high:
        mid=(low+high)//2
        if passes(mid):high=mid
        else:low=mid+1
    return low


def plan(precision=.98, *, alpha=.05, candidates=6, errors=0, min_groups=100,
         validation_groups=None, frozen_groups=None):
    validation=required_groups(precision,alpha=alpha,candidates=candidates,errors=errors,min_groups=min_groups)
    frozen=required_groups(precision,alpha=alpha,candidates=1,errors=errors,min_groups=min_groups)
    return {'version':'qualification-support-planner-v1','precision_lower_bound_target':precision,
        'alpha':alpha,'validation_candidates':candidates,'assumed_wrong_accepted_groups':errors,
        'required_accepted_validation_groups':validation,'required_accepted_frozen_groups':frozen,
        'declared_validation_groups':validation_groups,'declared_frozen_groups':frozen_groups,
        'validation_structurally_sufficient':None if validation_groups is None else validation_groups>=validation,
        'frozen_structurally_sufficient':None if frozen_groups is None else frozen_groups>=frozen,
        'important_limitations':[
            'Counts are ACCEPTED independent groups, not total imported records or correlated variants.',
            'Zero observed errors is a planning assumption, never a promised model result.',
            'Confidence availability, critical-positive support, review limits, calibration and label provenance remain separate gates.',
            'Unknown future coverage prevents converting these into a guaranteed total corpus size.',
            'Representative independently expert-labelled customer evaluation is required for customer automation.'
        ],'automation_enabled':False}


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--precision',type=float,default=.98);p.add_argument('--alpha',type=float,default=.05)
    p.add_argument('--candidates',type=int,default=6);p.add_argument('--errors',type=int,default=0)
    p.add_argument('--min-groups',type=int,default=100)
    p.add_argument('--validation-groups',type=int);p.add_argument('--frozen-groups',type=int)
    a=p.parse_args();print(json.dumps(plan(a.precision,alpha=a.alpha,candidates=a.candidates,errors=a.errors,
        min_groups=a.min_groups,validation_groups=a.validation_groups,frozen_groups=a.frozen_groups),indent=2))
