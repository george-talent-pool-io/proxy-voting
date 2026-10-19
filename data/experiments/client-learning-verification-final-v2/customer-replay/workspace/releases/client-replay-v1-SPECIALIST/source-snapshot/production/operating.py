"""Validation-selected, independently tested confidence operating points.

An operating point is a review simulation until customer qualification succeeds.
Bounds count a family as wrong if any accepted event in that family is wrong.
"""
from collections import defaultdict
from scipy.stats import beta
from production.storage import digest
from training.framework.bundle import write

VERSION = 'confidence-operating-point-v1'
CRITICAL = ('votability', 'share_blocking', 'poa_required', 'registration_required')


def summarize(rows, threshold, *, alpha=.05):
    accepted = [r for r in rows if not r['force_review'] and r['confidence'] is not None and r['confidence'] >= threshold]
    groups = defaultdict(list)
    for row in accepted: groups[row['group']].append(row)
    good = sum(all(r['exact_correct'] for r in group) for group in groups.values())
    bound = float(beta.ppf(alpha, good, len(groups) - good + 1)) if good else 0.0
    critical = {k: sum(r['truth'][k] == ('VOTABLE' if k == 'votability' else 'YES') and
                       r['prediction'][k] != r['truth'][k] for r in accepted) for k in CRITICAL}
    return {'threshold': threshold, 'n': len(rows), 'accepted': len(accepted),
            'accepted_groups': len(groups), 'coverage': len(accepted) / len(rows) if rows else 0,
            'review_rate': 1 - len(accepted) / len(rows) if rows else 1,
            'correctness': sum(r['exact_correct'] for r in accepted) / len(accepted) if accepted else None,
            'wrong_accepted': sum(not r['exact_correct'] for r in accepted),
            'precision_lower_bound': bound, 'critical_false_negatives_accepted': critical}


def select(rows, *, identity, calibrator_hash, output, min_precision=.98, min_groups=100,
           thresholds=(.70, .80, .90, .95, .98, .99)):
    if not rows or any(r['role'] != 'VALIDATION' for r in rows):
        raise ValueError('Operating point selection uses VALIDATION only')
    if not .9 <= min_precision < 1 or min_groups < 20:
        raise ValueError('Explicit conservative operating requirements needed')
    # Simultaneous bounds protect against selecting the luckiest threshold.
    curve = [summarize(rows, t, alpha=.05 / len(thresholds)) for t in thresholds]
    eligible = [p for p in curve if p['accepted_groups'] >= min_groups and
                p['precision_lower_bound'] >= min_precision and not any(p['critical_false_negatives_accepted'].values())]
    selected = max(eligible, key=lambda p: (p['coverage'], p['threshold'])) if eligible else None
    value = {'version': VERSION, 'identity': identity, 'calibrator_sha256': calibrator_hash,
             'validation_sha256': digest(rows), 'selection': selected, 'curve': curve,
             'status': 'OPERATING_POINT_SUPPORTED' if selected else 'NO_SUPPORTED_OPERATING_POINT',
             'min_precision': min_precision, 'min_groups': min_groups,
             'scope': 'Declared calibration population only; review simulation, not automation authorisation',
             'automation_enabled': False}
    value['sha256'] = digest(value); write(output, value)
    return value


def evaluate(rows, operating_point, *, identity, calibrator_hash):
    if (operating_point['identity'] != identity or operating_point['calibrator_sha256'] != calibrator_hash or
            operating_point['sha256'] != digest({k: v for k, v in operating_point.items() if k != 'sha256'})):
        raise ValueError('Operating point identity/integrity mismatch')
    if not rows or any(r['role'] != 'FROZEN_TEST' for r in rows): raise ValueError('Independent FROZEN_TEST required')
    if operating_point['selection'] is None:
        return {'status': 'NO_SUPPORTED_OPERATING_POINT', 'accepted': 0, 'review_rate': 1.,
                'benchmark_gate_passed':False,'automation_enabled': False}
    measured=summarize(rows, operating_point['selection']['threshold'])
    reasons=[]
    if measured['accepted_groups']<operating_point['min_groups']:reasons.append('INSUFFICIENT_ACCEPTED_TEST_GROUPS')
    if measured['precision_lower_bound']<operating_point['min_precision']:reasons.append('TEST_PRECISION_LOWER_BOUND_NOT_MET')
    if any(measured['critical_false_negatives_accepted'].values()):reasons.append('ACCEPTED_CRITICAL_FALSE_NEGATIVE')
    return {**measured,'status':'FROZEN_BENCHMARK_GATE_PASSED' if not reasons else 'FROZEN_BENCHMARK_GATE_NOT_MET',
            'benchmark_gate_passed':not reasons,'reasons':reasons,
            'threshold_selected_on':'VALIDATION','automation_enabled':False}
