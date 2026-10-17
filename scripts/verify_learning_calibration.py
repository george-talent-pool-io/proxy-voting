"""Numerical calibration qualification on controlled statistical data.

NOT Laya/Qwen predictions. This tests calibration software with known independent
correctness labels. Its calibrator must never attach to a model release.
"""
import argparse
import json
from pathlib import Path

from semantic_pipeline.schema import PREDICATES
from qwen_domain.confidence import CorrectnessCalibrator, calibration_metrics
from training.framework.bundle import write

IDENTITY = 'SOFTWARE_CONTRACT_FIXTURE_NOT_A_MODEL_RELEASE_V1'


def verify(output):
    root = Path(output); root.mkdir(parents=True, exist_ok=False)
    records = []
    for fold, n in [('FIT', 400), ('EVALUATION', 200)]:
        for i in range(n):
            strong = i % 2 == 0
            # Disjoint groups and fixed conditional frequencies in both folds.
            correct = i % 10 != 0 if strong else i % 10 in (1, 3)
            for key in PREDICATES:
                records.append({'split': 'CALIBRATION', 'predicate': key, 'calibration_fold': fold,
                                'duplicate_group': f'{fold}-{i}', 'correct': correct,
                                'features': {'controlled_reliability_signal': strong}})
    cal = CorrectnessCalibrator(IDENTITY); reports = cal.fit(records)
    assert len(cal.models) == len(PREDICATES)
    cal.save(root / 'calibrator.joblib'); loaded = CorrectnessCalibrator.load(root / 'calibrator.joblib', IDENTITY)
    probe = [loaded.predict('share_blocking', r['features'], IDENTITY) for r in records if r['predicate'] == 'share_blocking' and r['calibration_fold'] == 'EVALUATION']
    truth = [r['correct'] for r in records if r['predicate'] == 'share_blocking' and r['calibration_fold'] == 'EVALUATION']
    metrics = calibration_metrics(truth, probe)
    assert metrics['n'] == 200 and metrics['ece'] < .1
    wrong_identity_rejected = False
    try: loaded.predict('share_blocking', {}, 'ACTUAL_RELEASE')
    except ValueError: wrong_identity_rejected = True
    assert wrong_identity_rejected
    receipt = {'scope': IDENTITY, 'fit_examples_per_predicate': 400, 'held_out_examples_per_predicate': 200,
               'models_fitted': sorted(cal.models), 'reports': reports, 'reload_exact': loaded.predict('share_blocking', {'controlled_reliability_signal': True}, IDENTITY) == cal.predict('share_blocking', {'controlled_reliability_signal': True}, IDENTITY),
               'wrong_identity_rejected': True, 'attached_to_release': False, 'customer_accuracy': None, 'automation_enabled': False}
    write(root / 'receipt.json', receipt)
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots(figsize=(6, 4)); ax.plot([0, 1], [0, 1], '--', color='#999999')
    ax.plot([b['mean_probability'] for b in metrics['bins']], [b['observed_correctness'] for b in metrics['bins']], 'o-', color='#18695f')
    ax.set(xlabel='Calibrated correctness estimate', ylabel='Observed held-out correctness',
           title='Controlled software fixture — NOT model performance', xlim=(0, 1), ylim=(0, 1))
    fig.tight_layout(); fig.savefig(root / 'reliability.svg'); plt.close(fig)
    return receipt


if __name__ == '__main__':
    p = argparse.ArgumentParser(); p.add_argument('output'); a = p.parse_args()
    r = verify(a.output); print(json.dumps({'passed': True, 'scope': r['scope'], 'fitted_predicates': len(r['models_fitted'])}))
