"""Evidence-aware inference using a newly registered Laya checkpoint.

The native document choice remains available. Restrictions use the existing
supersession-aware reducer; all native passage distributions are retained.
Exact quotations are candidate evidence, not a proof of semantic entailment.
"""
import copy
import math
import time

from cascade.aggregation import AggregationConfig
from fast_cascade.aggregation import aggregate
from hybrid.semantics import passages
from semantic_pipeline.schema import PREDICATES, RESTRICTIONS
from semantic_pipeline.evidence import verify_evidence
from semantic_pipeline.decision import decide
from training.framework.runtime import RegisteredModel

VERSION = 'registered-passage-inference-v2'


def document_with_passage_evidence(original, diagnostic):
    """Keep the trained document answer; verify support and expose disagreement.

    Only current, route-applicable passages selected by the semantic reducer can
    support the document. A native NO on unrelated prose is not opposition.
    Neither an exact substring nor a passage score proves correctness.
    """
    chosen = original['value']
    disagreement = (chosen in ('YES', 'NO') and diagnostic['value'] in ('YES', 'NO')
                    and chosen != diagnostic['value'] and bool(diagnostic['evidence']))
    conflict = bool(original.get('conflict') or diagnostic['conflict'] or disagreement)
    evidence = diagnostic['evidence'] if chosen == diagnostic['value'] and not conflict else []
    return {**original, 'evidence': evidence,
            'evidence_status': 'EXACT_NATIVE_PASSAGE_CANDIDATE' if evidence else 'UNAVAILABLE',
            'supporting_passage_count': diagnostic['supporting_passage_count'] if chosen == diagnostic['value'] else 0,
            'contradicting_passage_count': (diagnostic['supporting_passage_count'] if disagreement
                                           else diagnostic['contradicting_passage_count']),
            'conflict': conflict, 'document_passage_disagreement': disagreement,
            'passage_diagnostic': diagnostic,
            'source': 'REGISTERED_LAYA_WHOLE_WITH_PASSAGE_EVIDENCE'}


def decode(answer, choices, truncated=False):
    scores = answer['probabilities']
    if (set(scores) != set(choices) or any(not math.isfinite(v) or not 0 <= v <= 1 for v in scores.values())
            or abs(sum(scores.values()) - 1) > .002 or answer['choice'] not in scores):
        raise ValueError('Invalid native passage distribution')
    rank = sorted(scores.values(), reverse=True)
    if scores[answer['choice']] < rank[0] - .0001:
        raise ValueError('Native passage winner mismatch')
    return {'value': 'UNKNOWN' if truncated else answer['choice'], 'scores': scores,
            'confidence': scores[answer['choice']], 'margin': rank[0] - rank[1], 'truncated': truncated}


class RegisteredPassages:
    def __init__(self, job, *, config=None, model_factory=RegisteredModel, whole_notice=False):
        self.model = model_factory(job)
        if self.model.spec.backend != 'LAYA_SDK':
            self.model.close()
            raise ValueError('Passage inference requires a registered Laya checkpoint')
        self.config = AggregationConfig(**(config or {}))
        self.whole_notice = whole_notice

    def analyse(self, text, **kwargs):
        started = time.perf_counter()
        result = self.model.analyse(text, **kwargs)
        spans = list(passages(text))
        if len(spans) > 10000:
            raise ValueError('Passage limit exceeded; no silent truncation')
        native = {k: [] for k in PREDICATES}
        for offset in range(0, len(spans), 8):
            batch = spans[offset:offset + 8]
            raw = self.model.agent.predict_batch([p['text'] for p in batch], self.model.questions,
                    batch_size=8, max_len=self.model.spec.max_length, head_max_len=256, sort_by_length=True)
            if len(raw) != len(batch): raise ValueError('Native passage count mismatch')
            for row in raw:
                for key in PREDICATES:
                    native[key].append(decode(row['answers'][key], self.model.questions[key]['criteria'],
                                              bool(row.get('usage', {}).get('truncated'))))
        original = copy.deepcopy(result['predicates'])
        for key in RESTRICTIONS:
            pred = aggregate(text, key, native[key], self.config)
            # The reducer exposes a native winning score, not calibrated trust.
            pred['native_score'] = pred.pop('confidence')
            pred.update(confidence=None, source='REGISTERED_LAYA_PASSAGES',
                        whole_notice_diagnostic=original[key], truncated=any(p['truncated'] for p in native[key]))
            if self.whole_notice:
                # Preserve the document result learned during document training.
                # Passage scores locate candidate evidence and contradictions;
                # they never silently replace the matched whole-notice output.
                pred = document_with_passage_evidence(original[key], pred)
            result['predicates'][key] = pred
        vote = result['predicates']['votability']
        support = [(span, p) for span, p in zip(spans, native['votability'])
                   if p['value'] == vote['value'] and p['confidence'] >= self.config.min_score and not p['truncated']]
        from cascade.aggregation import HISTORY
        support = [(s, p) for s, p in support if not HISTORY.search(s['text'])]
        vote['evidence'] = ([{**verify_evidence(text, support[0][0]['text']), 'source': 'MATCHING_NATIVE_PASSAGE'}]
                            if support else [])
        vote['evidence_status'] = 'EXACT_SOURCE_CANDIDATE' if support else 'UNAVAILABLE'
        vote['supporting_passage_count'] = len(support)
        # Preserve a contrary *current* vote assertion as a conflict signal. The
        # older explicit-scope detector expects YES/NO vote choices.
        from fast_cascade.laya import vote_conflicts
        votes = [{**p, 'value': {'VOTABLE': 'YES', 'NOT_VOTABLE': 'NO', 'UNCERTAIN': 'UNKNOWN'}.get(p['value'], p['value'])}
                 for p in native['votability']]
        opposing = vote_conflicts(text, votes, vote['value'])
        vote.update(opposing_passages=opposing, contradicting_passage_count=len(opposing),
                    conflict=bool(vote.get('conflict') or opposing))
        rank = sorted(vote['scores'].values(), reverse=True)
        vote['margin'] = rank[0] - rank[1]
        conflicts = sorted(set(result['reconciliation']['conflicts']) |
                           {k + ':PASSAGE_CONFLICT' for k in PREDICATES if result['predicates'][k].get('conflict')})
        result['reconciliation'] = {'predicates': {k: result['predicates'][k] for k in PREDICATES}, 'conflicts': conflicts}
        result['decision'] = decide(result['predicates'], result['deadline'], conflicts)
        result.update(whole_notice_diagnostic=original, passage_predictions=native, passage_spans=spans,
                      passage_runtime_version=VERSION)
        result['latencies']['total_ms'] = (time.perf_counter() - started) * 1000
        return result

    def close(self):
        self.model.close()
