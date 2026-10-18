"""Portable JSON correctness calibration, with disjoint group-isolated folds.

Numerical outputs are scoped to the labelled population. This does not estimate
correctness in a different customer population and does not approve automation.
"""
import math
from collections import Counter
from pathlib import Path
import numpy as np
from sklearn.feature_extraction import DictVectorizer
from sklearn.linear_model import LogisticRegression
from qwen_domain.confidence import features, numeric_features, calibration_metrics
from training.framework.bundle import write
from production.storage import digest

VERSION = 'customer-correctness-v1'


def feature_row(text, key, pred, *, language, input_type, conflicts=(), schema_valid=True):
    base = features(text, key, pred, language=language, input_type=input_type,
                    deterministic_conflict=bool(conflicts), schema_valid=schema_valid)
    scores = sorted((pred.get('scores') or {}).values(), reverse=True)
    base['features'].update(native_top=scores[0] if scores else None,
                            native_margin=scores[0] - scores[1] if len(scores) > 1 else None,
                            prediction=pred['value'], source=pred.get('source', 'UNKNOWN'))
    return base


def fit(records, *, identity, population, output):
    if not records or any(r['role'] != 'CALIBRATION' for r in records): raise ValueError('CALIBRATION records only')
    groups = {fold: {r['group'] for r in records if r['fold'] == fold} for fold in ('FIT', 'EVALUATION')}
    if groups['FIT'] & groups['EVALUATION'] or any(r['fold'] not in groups for r in records):
        raise ValueError('Calibration fold/group leakage')
    if len({(r['id'], r['predicate']) for r in records}) != len(records): raise ValueError('Duplicate calibration assertion')
    models = {}; reports = {}
    for key in sorted({r['predicate'] for r in records}):
        a = [r for r in records if r['predicate'] == key and r['fold'] == 'FIT']
        b = [r for r in records if r['predicate'] == key and r['fold'] == 'EVALUATION']
        counts = Counter(bool(r['correct']) for r in a)
        # Group support counts prevent template variants inflating support.
        if len({r['group'] for r in a}) < 100 or len({r['group'] for r in b}) < 50 or min(counts[True], counts[False]) < 10:
            reports[key] = {'status': 'INSUFFICIENT_SUPPORT', 'fit': len(a), 'evaluation': len(b)}; continue
        v = DictVectorizer(sparse=False)
        x = v.fit_transform([numeric_features(r['features']) for r in a])
        m = LogisticRegression(C=.1, random_state=42, max_iter=2000).fit(x, [bool(r['correct']) for r in a])
        p = m.predict_proba(v.transform([numeric_features(r['features']) for r in b]))[:, 1]
        metrics = calibration_metrics([bool(r['correct']) for r in b], p)
        curve = []
        for threshold in [.70, .80, .90, .95, .98, .99]:
            selected = [r for r, prob in zip(b, p) if prob >= threshold]
            curve.append({'threshold': threshold, 'support': len(selected), 'coverage': len(selected) / len(b),
                          'correctness': sum(r['correct'] for r in selected) / len(selected) if selected else None,
                          'errors': sum(not r['correct'] for r in selected), 'review_rate': 1 - len(selected) / len(b)})
        supported = metrics['ece'] <= .1 and metrics['wrong'] >= 5 and metrics['correct'] >= 20
        reports[key] = {'status': 'VALIDATED_IN_DECLARED_POPULATION' if supported else 'CALIBRATION_NOT_ESTABLISHED',
                        'evaluation': metrics, 'coverage_curve_diagnostic_only': curve,
                        'note': 'Do not tune the operational threshold on the calibration evaluation fold or frozen test'}
        if supported:
            models[key] = {'vocabulary': v.vocabulary_, 'coefficients': m.coef_[0].tolist(), 'intercept': float(m.intercept_[0]),
                           'languages': sorted({r['features'].get('language', 'UNKNOWN') for r in a})}
    payload = {'version': VERSION, 'identity': identity, 'population': population, 'models': models, 'reports': reports,
               'dataset_hash': digest(records), 'label_origins': dict(Counter(r['origin'] for r in records)),
               'method': 'Fixed L2 logistic correctness model; C=.1; independent group-isolated evaluation'}
    payload['sha256'] = digest(payload)
    write(output, payload)
    return payload


def load(path, identity):
    import json
    value = json.loads(Path(path).read_text())
    if value['version'] != VERSION or value['identity'] != identity or value['sha256'] != digest({k: v for k, v in value.items() if k != 'sha256'}):
        raise ValueError('Calibrator identity/integrity mismatch')
    return value


def predict(calibrator, key, feature, *, identity, population):
    if calibrator['identity'] != identity or calibrator['population'] != population: raise ValueError('Calibration population/model mismatch')
    model = calibrator['models'].get(key)
    if not model or feature.get('force_review') or feature['features'].get('language') not in model['languages']: return None
    data = numeric_features(feature['features']); vector = np.zeros(len(model['vocabulary']))
    for name, value in data.items():
        label = name + '=' + value if isinstance(value, str) else name
        if label in model['vocabulary']: vector[model['vocabulary'][label]] = 1 if isinstance(value, str) else value
    logit = float(np.dot(vector, model['coefficients']) + model['intercept'])
    return 1 / (1 + math.exp(-max(-700, min(700, logit))))
