# Aggregation validation — unchanged Laya weights

The historical system is preserved by PRE_AGGREGATION_FIX_BASELINE. This report contains validation-only results, not customer accuracy. No retraining or challenge tuning occurred.

The reducer distinguishes a native NO caused by absence of mention from an explicit negative statement. It retains every passage, native distribution, score/margin, source offsets, route, historical/background scope and supersession cue. Conflicting current terms without clear supersession abstain. A specified electronic-proxy route and a physical-attendance route are tested separately; an unspecified route abstains. Negative source cues only scope a native model decision; regex cannot create a native YES.

## Validation experiment

100 supplied validation notices plus 80 new complete synthetic validation notices yield 840 labelled restriction assertions. The supplied validation overlaps historical training; these figures are development evidence, not an independent accuracy estimate. Six strategies and three score/margin configurations are compared on the same native passage predictions. Contract-violating max/last strategies remain diagnostic comparators; only reducers passing explicit negation/supersession/conflict/route requirements are eligible.

| Strategy | Score / margin | Correct restriction assertions | Blocking positive detected/support | POA positive detected/support | Contract eligible |
|---|---:|---:|---:|---:|---|
| MAX_POSITIVE | 0.7 / 0.2 | 155/840 | 15/15 | 17/17 | False |
| MAX_POSITIVE | 0.9 / 0.4 | 151/840 | 15/15 | 17/17 | False |
| MAX_POSITIVE | 0.98 / 0.4 | 151/840 | 15/15 | 17/17 | False |
| MAX_MARGIN | 0.7 / 0.2 | 154/840 | 15/15 | 17/17 | False |
| MAX_MARGIN | 0.9 / 0.4 | 150/840 | 15/15 | 17/17 | False |
| MAX_MARGIN | 0.98 / 0.4 | 150/840 | 15/15 | 17/17 | False |
| ANY_STRONG_POSITIVE | 0.7 / 0.2 | 155/840 | 15/15 | 17/17 | False |
| ANY_STRONG_POSITIVE | 0.9 / 0.4 | 151/840 | 15/15 | 17/17 | False |
| ANY_STRONG_POSITIVE | 0.98 / 0.4 | 151/840 | 15/15 | 17/17 | False |
| WEIGHTED_PASSAGE | 0.7 / 0.2 | 157/840 | 15/15 | 17/17 | False |
| WEIGHTED_PASSAGE | 0.9 / 0.4 | 153/840 | 15/15 | 17/17 | False |
| WEIGHTED_PASSAGE | 0.98 / 0.4 | 153/840 | 15/15 | 17/17 | False |
| LAST_RELEVANT_STATEMENT | 0.7 / 0.2 | 154/840 | 15/15 | 17/17 | False |
| LAST_RELEVANT_STATEMENT | 0.9 / 0.4 | 150/840 | 15/15 | 17/17 | False |
| LAST_RELEVANT_STATEMENT | 0.98 / 0.4 | 150/840 | 15/15 | 17/17 | False |
| SUPERSESSION_AWARE | 0.7 / 0.2 | 637/840 | 15/15 | 17/17 | True |
| SUPERSESSION_AWARE | 0.9 / 0.4 | 632/840 | 15/15 | 17/17 | True |
| SUPERSESSION_AWARE | 0.98 / 0.4 | 632/840 | 15/15 | 17/17 | True |

Selected: `{"strategy": "SUPERSESSION_AWARE", "min_score": 0.7, "min_margin": 0.2, "voting_route": null}`. The original eleven blocking-positive validation notices improve 0/11 → 11/11 with the exact same checkpoint.

The first validation draft exposed a separate scoping problem: a historical sentence concerning one predicate suppressed unrelated predicates. The v2 reducer scopes history/background to the predicate and treats unexplained relevant native NO conservatively. Original v1 candidate results are retained, and all revisions preceded challenge inference.

Expanded specialist weaknesses remain: beneficial-owner disclosure and split-voting affirmative detection are each 0/4 in this synthetic validation sample after reduction. The reducer cannot manufacture semantic understanding absent from native Laya output. Six expanded predicates have no dedicated domain-supervised labels. These limitations must remain visible in the selective-routing experiment.

A/B are whole-notice classifiers and do not use this reducer. Their unchanged-checkpoint reruns must not be advertised as aggregation improvements. The new capable specialist separately uses whole-notice votability (176/180 validation vs narrow152/180), with fixed narrow restrictions. Both source model views and their checkpoints remain explicit.

Unit/property tests cover positive/negative pairs, unrelated absence, supersession, historical/background references, route conditions, POA/registration/disclosure/recall equivalents, source alignment, arbitrary Unicode and score preservation. Final model/pipeline results will appear only after the controlled run completes. Automation remains disabled; customer accuracy unknown.

## Matched-absence diagnostic control

The original comparator table above includes different document-absence policies: only SUPERSESSION_AWARE implements a conservative native-all-NO absence fallback. Its large total-agreement advantage must therefore **not** be attributed solely to supersession reasoning. This additional validation-only control applies the identical absence fallback to all six reducers, leaving their handling of actual positive/negative/conflicting passages unchanged. No checkpoint, selected strategy, threshold, prompt or routing decision is changed. All predictions come from the same cached native passage outputs; no challenge cases were consulted.

| Strategy | Score / margin | Correct restriction assertions | Affirmative misses (all restriction fields) | False positives |
|---|---:|---:|---:|---:|
| MAX_POSITIVE | 0.7 / 0.2 | 632/840 | 8 | 8 |
| MAX_POSITIVE | 0.9 / 0.4 | 628/840 | 12 | 6 |
| MAX_POSITIVE | 0.98 / 0.4 | 628/840 | 12 | 5 |
| MAX_MARGIN | 0.7 / 0.2 | 631/840 | 9 | 5 |
| MAX_MARGIN | 0.9 / 0.4 | 627/840 | 13 | 4 |
| MAX_MARGIN | 0.98 / 0.4 | 627/840 | 13 | 3 |
| ANY_STRONG_POSITIVE | 0.7 / 0.2 | 632/840 | 8 | 8 |
| ANY_STRONG_POSITIVE | 0.9 / 0.4 | 628/840 | 12 | 6 |
| ANY_STRONG_POSITIVE | 0.98 / 0.4 | 628/840 | 12 | 5 |
| WEIGHTED_PASSAGE | 0.7 / 0.2 | 634/840 | 9 | 2 |
| WEIGHTED_PASSAGE | 0.9 / 0.4 | 630/840 | 13 | 1 |
| WEIGHTED_PASSAGE | 0.98 / 0.4 | 630/840 | 13 | 0 |
| LAST_RELEVANT_STATEMENT | 0.7 / 0.2 | 631/840 | 9 | 2 |
| LAST_RELEVANT_STATEMENT | 0.9 / 0.4 | 627/840 | 13 | 1 |
| LAST_RELEVANT_STATEMENT | 0.98 / 0.4 | 627/840 | 13 | 0 |
| SUPERSESSION_AWARE | 0.7 / 0.2 | 637/840 | 9 | 2 |
| SUPERSESSION_AWARE | 0.9 / 0.4 | 632/840 | 13 | 1 |
| SUPERSESSION_AWARE | 0.98 / 0.4 | 632/840 | 13 | 0 |

Small overall differences on repetitive synthetic validation do not establish superiority on real notices. Contract tests independently require abstention on unresolved contradictions and voting routes; an accurate result on a simple validation sentence does not remove that requirement. Full counts are retained in AGGREGATION-MATCHED-ABSENCE-CONTROL.json.
