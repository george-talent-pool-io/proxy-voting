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
