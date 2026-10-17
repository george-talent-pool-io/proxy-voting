# Interim local Laya / GLM / Qwen results

Snapshot: 2026-10-17T08:38:39.592450+00:00. **The complete study has NOT finished.** These are authored/synthetic benchmarks, not customer accuracy. Automation is disabled. Frozen-test Qwen xhigh, selected C/E cascades, final oracle analysis and final verification remain pending.

## Completed challenge conditions

57 fixed authored cases; 95 supplied assertions; only four explicit final-status labels. Cases satisfying partial assertions are not ordinary final-status accuracy.

| Condition | Correct assertions /95 | Cases satisfying supplied assertions /57 | Median / p95 seconds |
|---|---:|---:|---:|
| A | 59 | 30 | 0.04 / 0.05 |
| B | 73 | 37 | 0.04 / 0.05 |
| D1 | 58 | 22 | 4.06 / 4.71 |
| D2 | 92 | 54 | 21.35 / 25.11 |
| C1 | 85 | 47 | 5.44 / 7.07 |
| C2 | 88 | 50 | 25.99 / 29.80 |

A=base whole Laya, B=fine-tuned whole Laya. D1=independent GLM; D2=independent Qwen Direct; D3=independent Qwen xhigh. C1/C2/C3 use identical whole-notice Laya diagnostics and always invoke the respective LLM. C1/C2 remain the controlled comparison, not the newly selected selective cascade.

### Challenge semantic repairs / damage

| Condition | Wrong/unsupported → correct | Correct → wrong | Semantic transitions scored |
|---|---:|---:|---:|
| C1 | 5 | 2 | 77 |
| C2 | 7 | 1 | 77 |

Repairs/damage are reconciled semantic transitions against pre-fallback Laya; deadline and final status are excluded. NOT_SUPPORTED capability fills count among repairs; these are not all changes to an affirmative/negative specialist error.

### Challenge affirmative recall

| Predicate | Support | A | B | D1 | D2 | C1 | C2 |
|---|---:|---:|---:|---:|---:|---:|---:|
| votability | 36 | 63.9% | 100.0% | 47.2% | 97.2% | 97.2% | 97.2% |
| share_blocking | 3 | 100.0% | 66.7% | 100.0% | 100.0% | 66.7% | 66.7% |
| poa_required | 3 | 66.7% | 66.7% | 100.0% | 100.0% | 66.7% | 66.7% |
| other_restriction | 4 | 25.0% | 0.0% | 75.0% | 100.0% | 50.0% | 100.0% |

## Completed validation: all three LLMs

40 unique synthetic notices, nine semantic fields each = 360 semantic assertions per condition. Raw model semantics below are evidence-validated LLM outputs before reconciliation; they exclude deadlines/final statuses. Independent and fallback modes use the same 40 inputs but different declared context.

| Condition | LLM semantic assertions correct /360 | Reconciled semantic repairs | Reconciled damage | Median / p95 end-to-end seconds |
|---|---:|---:|---:|---:|
| D1 | 324 | N/A | N/A | 4.65 / 5.34 |
| D2 | 352 | N/A | N/A | 28.02 / 32.78 |
| D3 | 357 | N/A | N/A | 242.36 / 612.57 |
| C1 | 331 | 222 | N/A | 6.76 / 10.62 |
| C2 | 358 | 247 | N/A | 33.16 / 39.77 |
| C3 | 354 | 247 | 4 | 348.20 / 558.66 |

Fallback repairs include filling six unsupported legacy fields (up to 240/360 assertions), not only correcting misclassified supported fields. Validation denominators are small, particularly restriction positives.

### Validation affirmative recall: evidence-validated LLM output

| Predicate | Positive support per mode | D1 | D2 | D3 | C1 | C2 | C3 |
|---|---:|---:|---:|---:|---:|---:|---:|
| votability | 30 | 30/30 | 30/30 | 28/30 | 30/30 | 30/30 | 28/30 |
| share_blocking | 3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 2/3 |
| poa_required | 2 | 2/2 | 2/2 | 2/2 | 2/2 | 2/2 | 1/2 |
| registration_required | 2 | 2/2 | 2/2 | 2/2 | 2/2 | 2/2 | 2/2 |
| beneficial_owner_disclosure_required | 3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 2/3 |
| holding_confirmation_required | 3 | 3/3 | 3/3 | 3/3 | 1/3 | 3/3 | 2/3 |
| split_voting_restricted | 3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 |
| securities_lending_recall_required | 2 | 2/2 | 2/2 | 2/2 | 2/2 | 2/2 | 2/2 |
| other_voting_restriction | 2 | 2/2 | 2/2 | 2/2 | 2/2 | 2/2 | 2/2 |

## Post-fix native Laya

The unchanged whole-notice A/B reruns remain 59/95 and 73/95; that route never used the defective reducer. The supplied development-validation blocking result is 0/11 → 11/11. The clean native narrow-reducer comparisons on the frozen benchmarks are below; they are separate from the composite specialist and LLM.

| Dataset | Predicate | Correct before / n | Correct after / n | Positive support | Positive recall before → after |
|---|---|---:|---:|---:|---:|
| challenge | votability | 38/54 | 38/54 | 36 | 97.2% → 97.2% |
| challenge | share_blocking | 8/11 | 8/11 | 3 | 66.7% → 66.7% |
| challenge | poa_required | 5/8 | 5/8 | 3 | 66.7% → 66.7% |
| challenge | other_restriction | 0/4 | 0/4 | 4 | 0.0% → 0.0% |
| complete | votability | 42/48 | 42/48 | 42 | 100.0% → 100.0% |
| complete | share_blocking | 40/48 | 35/48 | 3 | 0.0% → 100.0% |
| complete | poa_required | 35/48 | 38/48 | 3 | 0.0% → 100.0% |
| complete | registration_required | 11/48 | 12/48 | 3 | 0.0% → 0.0% |
| complete | beneficial_owner_disclosure_required | 40/48 | 34/48 | 3 | 0.0% → 33.3% |
| complete | holding_confirmation_required | 33/48 | 34/48 | 3 | 0.0% → 100.0% |
| complete | split_voting_restricted | 42/48 | 36/48 | 3 | 0.0% → 66.7% |
| complete | securities_lending_recall_required | 16/48 | 14/48 | 4 | 0.0% → 50.0% |
| complete | other_voting_restriction | 41/48 | 28/48 | 3 | 0.0% → 0.0% |

On the 48-case complete synthetic set, blocking-positive recall improves 0/3 → 3/3, but total blocking agreement falls 40/48 → 35/48: eight additional expected-NO cases become UNKNOWN. This is increased abstention, not eight false affirmative blocking claims. On the challenge, blocking-positive recall remains 2/3 after reduction. The fix does not establish general semantic quality.

## Validation-only primary and selective routing

Primary selected: **QWEN_DIRECT**, using the predeclared validation ranking. Independent xhigh has higher aggregate semantic agreement than Direct, but fallback xhigh misses some critical positives and takes substantially longer. Model selection pools both modes without counting them as independent notices.

Selected policy: {"name": "MODERATE", "min_score": 0.7, "min_margin": 0.1, "require_positive_evidence": true, "escalate_critical_positive": false, "escalate_unknown": true, "max_chars": 12000}.
LLM calls 57/80; no-LLM coverage 28.7%. Selected and always-fallback both score 672/720 semantic assertions on these validation notices. No added affirmative misses for any semantic predicate. Every record remains subject to the customer review gate. Frozen-test coverage/quality has not yet run.

## Validation-only oracle (not frozen test)

Capable Laya: 526/720 semantic assertions. It misses 194; the selected Qwen Direct fallback can answer 166 of those correctly in the recorded context. Assertion-wise oracle ceiling: 692/720 (96.1%). Actual selected reconciled routing: 672/720. This analytical ceiling ignores the difficulty of identifying errors and is not a deployable architecture. The final frozen-test oracle remains pending.

## Complete synthetic benchmark conditions finished so far

| Condition | Correct labelled assertions /528 | All supplied assertions satisfied /48 | Median / p95 seconds |
|---|---:|---:|---:|
| A | 90 | 0 | 0.05 / 0.08 |
| B | 199 | 0 | 0.05 / 0.08 |
| D1 | 485 | 28 | 4.90 / 5.52 |
| D2 | 491 | 29 | 23.70 / 26.07 |
| C1 | 484 | 29 | 6.03 / 7.16 |

Historical C gain decomposition, schemas, evidence validation, per-field confusion matrices and raw prediction artifacts remain preserved. The adjacent JSON snapshot contains complete per-field metrics for all finished conditions. No final model-quality or customer-accuracy claim follows from this interim snapshot.
