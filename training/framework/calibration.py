"""One feature contract for release fitting, held-out scoring and serving."""
from qwen_domain.confidence import confidence_output

VERSION = 'registered-release-confidence-v1'


def predicate_confidence(text, key, pred, *, calibrator=None, identity=None, conflict=False):
    value = confidence_output(text, key, pred, deterministic_conflict=conflict)
    scores = pred.get('scores') or {}
    rank = sorted(scores.values(), reverse=True)
    value['features'].update(native_top_score=rank[0] if rank else None,
                             native_margin=rank[0] - rank[1] if len(rank) > 1 else None,
                             prediction=pred['value'], model_source=pred.get('source', 'UNKNOWN'),
                             supporting_passage_count=pred.get('supporting_passage_count', 0),
                             contradicting_passage_count=pred.get('contradicting_passage_count', 0))
    value['version'] = VERSION
    if calibrator and not value['force_review']:
        trust = calibrator.predict(key, value['features'], identity)
        if trust is not None:
            value.update(confidence=trust, confidence_kind='CALIBRATED_ON_SYNTHETIC_POPULATION_ONLY',
                         calibration_scope='Only the AI-authored calibration population; not customer correctness probability')
    return value
