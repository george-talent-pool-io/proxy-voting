# Laya training diagnosis — validation evidence only

No frozen-test errors or challenge examples informed this diagnosis or the new training recipe.

## Observed results

| Condition | Correct assertions | Exact all-nine notices | Blocking YES recall | POA YES recall | Registration YES recall |
|---|---:|---:|---:|---:|---:|
| FROZEN_LAYA_WHOLE | 2882/5400 | 0/600 | 99.58% | 55.36% | 67.97% |
| TRAINED_LAYA_PASSAGES | 3496/5400 | 6/600 | 25.42% | 50.00% | 28.52% |
| TRAINED_LAYA_WHOLE | 4099/5400 | 53/600 | 23.73% | 89.73% | 61.72% |

The official SDK diagnostic on the older 128-example validation population improved 25.17% → 99.48% after full-encoder training. The new 600-example validation population exposes a substantial generalisation gap. The two results must not be mixed.

## Measured distribution shift

| Population | Notices | Mean simultaneous positive restrictions | Count histogram (0–8 positives) |
|---|---:|---:|---|
| Earlier TRAIN | 128 | 1.516 | {0: 30, 1: 35, 2: 40, 3: 15, 4: 6, 5: 2} |
| Customer-style TRAIN + replay | 232 | 3.078 | {0: 13, 1: 17, 2: 39, 3: 75, 4: 56, 5: 22, 6: 10} |
| Customer-style VALIDATION | 600 | 3.213 | {0: 2, 1: 50, 2: 136, 3: 168, 4: 142, 5: 78, 6: 24} |

## Interpretation and corrective experiment

The original eight-event, head-only trial was insufficient to judge learnability. Full-encoder training on 128 examples learned the old construction population well, but did not generalise to denser combinations of independent conditions. Whole-notice inference performs better than applying a whole-notice-trained model independently to sentences. These are measured findings.

High encoder learning rate, limited positive examples, shared training/validation language atoms and sparse co-occurrence patterns are plausible contributors. This experiment does not isolate their causal contributions. Additional epochs alone cannot be assumed to fix distribution mismatch.

The next fixed experiment starts from the frozen official foundation, trains on the new corpus TRAIN role (200 notices) plus 32 TRAIN-only replay examples, uses encoder LR 0.000025 / head LR 0.0001 and four full-encoder epochs. A predeclared four-epoch continuation is permitted only if validation macro F1 or a critical-positive recall is below 0.98. Validation alone controls this decision. Models, calibrators and thresholds must then be frozen before final scoring.

Calibration is not a repair for poor semantics: an unsupported high-trust operating point must yield review, not an invented acceptance percentage. No automation is enabled, and no test-trained weights or corpus form part of the production delivery.


## Completed corrective experiment — 2026-10-19 follow-up

This section records outcomes after the above recipe was fixed; it did not
inform that recipe or any new tuning. Validation improved from 2,882/5,400
foundation assertions to 5,335/5,400 after four epochs and 5,388/5,400 after the
predeclared eight-epoch total. All-nine exact matches were 0/600, 543/600 and
588/600 respectively. Eight epochs were selected using validation only.

The selected checkpoint scored 3,591/3,600 assertions and 391/400 all-nine
matches on the controlled held-out composition cohort. Every positive
restriction in that cohort was detected. Nine errors were false positives.
The unchanged authored challenge was 70/95 assertions and 34/57 partial-case
passes; the corresponding current-runtime foundation was 60/95 and 27/57.
These nine-predicate conditions differ from the historical legacy classifier.

This demonstrates learnability on the declared synthetic construction
population. It does not demonstrate broad language generalisation: the cohort
shares sentence atoms across roles, is English, and all test notices are
votable with at least one restriction. Further epochs cannot establish
performance outside that scope. Calibrators were fitted, but no operating
point met the predeclared 98% lower-bound precision gate. Do not lower the gate
or reinterpret raw scores to conceal that outcome.

See [the full frozen-checkpoint evaluation](FROZEN_CHECKPOINT_LEARNING_EVALUATION.md)
for calibration support, every error, abstentions, timing and application proofs.
