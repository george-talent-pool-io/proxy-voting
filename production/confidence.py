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
from pydantic import BaseModel, ConfigDict, Field

VERSION = 'customer-correctness-v4'


def stratum(features):
    # A specialist calibration stratum cannot silently qualify LLM outcomes.
    return '|'.join(str(features.get(k,'UNSPECIFIED')) for k in
        ('prediction','evidence_mode','input_type','language','supersession_cue','source'))


class SupportPolicy(BaseModel):
    """Predeclared sample requirements; changing them creates a new condition."""
    model_config = ConfigDict(extra='forbid', allow_inf_nan=False)
    min_fit_groups: int = Field(default=100, ge=3)
    min_evaluation_groups: int = Field(default=50, ge=2)
    min_class_examples: int = Field(default=10, ge=5)
    min_stratum_groups: int = Field(default=20,ge=10)
    max_ece: float = Field(default=.1, gt=0, le=.1)
    scope: str = 'CUSTOMER_QUALIFICATION'


def feature_row(text, key, pred, *, language, input_type, conflicts=(), schema_valid=True):
    base = features(text, key, pred, language=language, input_type=input_type,
                    deterministic_conflict=bool(conflicts), schema_valid=schema_valid,supported_languages=None)
    from production.evidence_basis import valid_negative_basis
    basis=valid_negative_basis(text,pred)
    exact=any(e.get('valid') for e in pred.get('evidence',[]))
    base['features'].update(complete_source_negative=basis,
                            evidence_mode='QUOTE' if exact else 'COMPLETE_SOURCE_NEGATIVE' if basis else 'MISSING')
    if pred.get('negative_basis') and not basis:base['force_review']=True
    if pred['value'] in ('YES','VOTABLE') and not exact:base['force_review']=True
    scores = sorted((pred.get('scores') or {}).values(), reverse=True)
    base['features'].update(native_top=scores[0] if scores else None,
                            native_margin=scores[0] - scores[1] if len(scores) > 1 else None,
                            prediction=pred['value'], source=pred.get('source', 'UNKNOWN'),
                            supporting_passages=pred.get('supporting_passage_count', base['features']['supporting_passages']),
                            opposing_passages=pred.get('contradicting_passage_count', base['features']['opposing_passages']),
                            passage_conflict=bool(pred.get('conflict')))
    return base


def fit(records, *, identity, population, output, support_policy=None, context=None):
    policy = SupportPolicy.model_validate(support_policy or {})
    if not records or any(r['role'] != 'CALIBRATION' for r in records): raise ValueError('CALIBRATION records only')
    if any(not isinstance(r['correct'], bool) or not r['group'] or not r['id'] for r in records):
        raise ValueError('Explicit boolean correctness and nonempty identities required')
    groups = {fold: {r['group'] for r in records if r['fold'] == fold} for fold in ('FIT', 'EVALUATION')}
    if groups['FIT'] & groups['EVALUATION'] or any(r['fold'] not in groups for r in records):
        raise ValueError('Calibration fold/group leakage')
    if len({(r['id'], r['predicate']) for r in records}) != len(records): raise ValueError('Duplicate calibration assertion')
    if any(isinstance(v, float) and not math.isfinite(v) for r in records for v in r['features'].values()):
        raise ValueError('Nonfinite calibration feature')
    models = {}; reports = {}
    for key in sorted({r['predicate'] for r in records}):
        a = [r for r in records if r['predicate'] == key and r['fold'] == 'FIT']
        b = [r for r in records if r['predicate'] == key and r['fold'] == 'EVALUATION']
        counts = Counter(bool(r['correct']) for r in a)
        # Group support counts prevent template variants inflating support.
        support = {'fit_examples': len(a), 'evaluation_examples': len(b),
                   'fit_groups': len({r['group'] for r in a}), 'evaluation_groups': len({r['group'] for r in b}),
                   'fit_correct': counts[True], 'fit_wrong': counts[False]}
        if support['fit_groups'] < policy.min_fit_groups or support['evaluation_groups'] < policy.min_evaluation_groups:
            reports[key] = {'status': 'INSUFFICIENT_SUPPORT', 'fit': len(a), 'evaluation': len(b)}; continue
        if min(counts[True], counts[False]) >= policy.min_class_examples:
            v = DictVectorizer(sparse=False)
            x = v.fit_transform([numeric_features(r['features']) for r in a])
            mean=x.mean(axis=0);scale=x.std(axis=0);scale[scale<1e-12]=1.
            m = LogisticRegression(C=.1, random_state=42, max_iter=2000).fit((x-mean)/scale, [r['correct'] for r in a])
            p = m.predict_proba((v.transform([numeric_features(r['features']) for r in b])-mean)/scale)[:, 1]
            # Algebraically fold FIT-only scaling into portable coefficients.
            coefficient=m.coef_[0]/scale
            candidate = {'method': 'LOGISTIC', 'vocabulary': v.vocabulary_, 'coefficients': coefficient.tolist(),
                         'intercept': float(m.intercept_[0]-np.dot(mean,coefficient)), 'scaling':'FIT_ONLY_STANDARDISATION_FOLDED_INTO_COEFFICIENTS'}
        else:
            # No fabricated mistakes to fit a binary estimator. This estimates
            # a constant population correctness rate, with explicit weak support.
            # It cannot distinguish individual easy/hard cases.
            probability = (counts[True] + 1) / (len(a) + 2)
            p = np.full(len(b), probability)
            candidate = {'method': 'BETA_BINOMIAL_CONSTANT', 'probability': probability,
                         'limitation': 'Constant population rate; no per-example discrimination'}
        metrics = calibration_metrics([bool(r['correct']) for r in b], p)
        by_prediction = {}
        supported_predictions = []
        for label in sorted({r['features'].get('prediction') for r in a + b if r['features'].get('prediction') is not None}):
            aa = [r for r in a if r['features'].get('prediction') == label]
            bb = [(r, prob) for r, prob in zip(b, p) if r['features'].get('prediction') == label]
            detail = calibration_metrics([r['correct'] for r, _ in bb], [prob for _, prob in bb])
            fit_groups=len({r['group'] for r in aa});evaluation_groups=len({r['group'] for r,_ in bb})
            by_prediction[label] = {'fit': len(aa), 'fit_groups':fit_groups,'evaluation_groups':evaluation_groups,'evaluation': detail}
            if min(fit_groups,evaluation_groups)>=policy.min_stratum_groups and detail['ece'] <= policy.max_ece:
                supported_predictions.append(label)
        supported_strata=[]
        for label in sorted({stratum(r['features']) for r in a+b}):
            aa=[r for r in a if stratum(r['features'])==label]
            bb=[(r,prob) for r,prob in zip(b,p) if stratum(r['features'])==label]
            detail=calibration_metrics([r['correct'] for r,_ in bb],[prob for _,prob in bb])
            if min(len({r['group'] for r in aa}),len({r['group'] for r,_ in bb}))>=policy.min_stratum_groups and detail['ece']<=policy.max_ece:supported_strata.append(label)
        curve = []
        for threshold in [.70, .80, .90, .95, .98, .99]:
            selected = [r for r, prob in zip(b, p) if prob >= threshold]
            curve.append({'threshold': threshold, 'support': len(selected), 'coverage': len(selected) / len(b),
                          'correctness': sum(r['correct'] for r in selected) / len(selected) if selected else None,
                          'errors': sum(not r['correct'] for r in selected), 'review_rate': 1 - len(selected) / len(b)})
        supported = metrics['ece'] <= policy.max_ece and metrics['correct'] >= 20
        reports[key] = {'status': 'VALIDATED_IN_DECLARED_POPULATION' if supported else 'CALIBRATION_NOT_ESTABLISHED',
                        'evaluation': metrics, 'support': support, 'method': candidate['method'],
                        'by_prediction': by_prediction,
                        'scope': policy.scope, 'coverage_curve_diagnostic_only': curve,
                        'note': 'Do not tune the operational threshold on the calibration evaluation fold or frozen test'}
        if supported:
            models[key] = {**candidate, 'languages': sorted({r['features'].get('language', 'UNKNOWN') for r in a}),
                           'prediction_values': supported_predictions,
                           'supported_strata':supported_strata,
                           'input_types': sorted({r['features']['input_type'] for r in a if 'input_type' in r['features']})}
    payload = {'version': VERSION, 'identity': identity, 'population': population, 'models': models, 'reports': reports,
               'context':context,
               'dataset_hash': digest(records), 'label_origins': dict(Counter(r['origin'] for r in records)),
               'support_policy': policy.model_dump(),
               'method': 'Fixed logistic C=.1 when both outcomes supported; otherwise Laplace-smoothed constant; independent group-isolated evaluation'}
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
    if feature['features'].get('prediction') is not None and feature['features']['prediction'] not in model.get('prediction_values', []): return None
    if feature['features'].get('input_type') is not None and feature['features']['input_type'] not in model.get('input_types', []): return None
    f=feature['features']
    if f.get('evidence_mode') is not None:
        if stratum(f) not in model.get('supported_strata',[]):return None
    if model.get('method') == 'BETA_BINOMIAL_CONSTANT': return model['probability']
    data = numeric_features(feature['features']); vector = np.zeros(len(model['vocabulary']))
    for name, value in data.items():
        label = name + '=' + value if isinstance(value, str) else name
        if label in model['vocabulary']: vector[model['vocabulary'][label]] = 1 if isinstance(value, str) else value
    logit = float(np.dot(vector, model['coefficients']) + model['intercept'])
    return 1 / (1 + math.exp(-max(-700, min(700, logit))))
