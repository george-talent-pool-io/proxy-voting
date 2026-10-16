# Controlled A–E local-model experiment

**Quality gate NOT MET. Automation disabled. These are synthetic/authored measurements, not customer accuracy.**

## Scoring correction and audit

C retains a legacy broad auxiliary head alongside new named reconciled factors. The frozen v1 scorer incorrectly selected that auxiliary value for the challenge broad union. Derive the union from the new reconciled schema whenever it is available. A/B native broad output remains valid for their legacy schema.

This correction was identified after freeze and is disclosed rather than hidden. It changes only the evaluator projection of the old broad challenge assertion. The original frozen scorer, its numbers, all raw model results and every expected assertion remain intact. No model, prompt, threshold, preprocessing or classification criterion was adjusted. See `SCORER-v2-PROJECTIONS.json` for every projection and the separate validation check confirming routing selection is unchanged. The original report is [preserved here](../experiments/local-llm-v1/FROZEN-SCORER-V1.md).

A: base whole-text Laya. B: historical whole-text fine-tune. C: B plus real local fallback. D: independent local LLM. E: optional parser, narrow fine-tuned Laya, real local fallback, reconciliation and deterministic rules.

Local model: `zai-org/GLM-4.7-Flash`, Q4_K_M, Ollama 0.34.3; exact digest and selection: [LOCAL_LLM_SELECTION.md](LOCAL_LLM_SELECTION.md). 16,384 configured context, temperature 0, seed 42, thinking disabled, native JSON-schema constraints. No cloud API. No generated confidence is treated as a probability.

## challenge

Frozen authored partial assertions; repeatedly observed historical benchmark, not a new blind set.

| Architecture | Cases satisfying all supplied assertions | Frozen scorer v1 | Votability | Blocking YES recall | POA YES recall | Status agreement (labelled n) | LLM calls | Median / p95 ms |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| A | 30/57 | 30/57 | 34/54 | 100.0% (n=3) | 66.7% (n=3) | 50.0% (4) | 0/57 | 42/49 |
| B | 37/57 | 37/57 | 48/54 | 66.7% (n=3) | 66.7% (n=3) | 75.0% (4) | 0/57 | 42/52 |
| C | 47/57 | 45/57 | 49/54 | 66.7% (n=3) | 66.7% (n=3) | 100.0% (4) | 57/57 | 6092/7620 |
| D | 22/57 | 22/57 | 20/54 | 100.0% (n=3) | 100.0% (n=3) | 75.0% (4) | 57/57 | 4779/5870 |
| E | 36/57 | 36/57 | 38/54 | 100.0% (n=3) | 66.7% (n=3) | 75.0% (4) | 15/57 | 153/7684 |

All supplied assertions is a case-level conjunction. On the 57-case challenge it does **not** mean final-status accuracy; only four status labels exist. Unlabelled factors never count as correct. Missing capabilities remain NOT_SUPPORTED and count as wrong. All manual-review flags remain true because the customer gate is disabled.

Labelled-factor exact match (excludes the separately scored status; incomplete truth stays explicitly partial): A: 30/57, B: 37/57, C: 47/57, D: 22/57, E: 36/57.

Common-policy status sensitivity (same new rule table applied to the recorded facts, without inventing missing facts): A: 2/4, B: 3/4, C: 4/4, D: 3/4, E: 3/4.

### Affirmative/negative detection

| Arm | Field | Correct/n | Positive support | Negative support | Positive precision | Positive recall | Specificity | Positive F1 | Balanced accuracy |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| A | votability | 34/54 | 36 | 15 | 85.2% | 63.9% | 66.7% | 73.0% | 54.6% |
| A | share_blocking | 8/11 | 3 | 8 | 50.0% | 100.0% | 62.5% | 66.7% | 81.2% |
| A | poa_required | 7/8 | 3 | 5 | 100.0% | 66.7% | 100.0% | 80.0% | 83.3% |
| A | other_restriction | 1/4 | 4 | 0 | 100.0% | 25.0% | — | 40.0% | 25.0% |
| B | votability | 48/54 | 36 | 15 | 85.7% | 100.0% | 80.0% | 92.3% | 60.0% |
| B | share_blocking | 10/11 | 3 | 8 | 100.0% | 66.7% | 100.0% | 80.0% | 83.3% |
| B | poa_required | 7/8 | 3 | 5 | 100.0% | 66.7% | 100.0% | 80.0% | 83.3% |
| B | other_restriction | 0/4 | 4 | 0 | — | 0.0% | — | 0.0% | 0.0% |
| C | votability | 49/54 | 36 | 15 | 100.0% | 97.2% | 73.3% | 98.6% | 90.2% |
| C | share_blocking | 10/11 | 3 | 8 | 100.0% | 66.7% | 100.0% | 80.0% | 83.3% |
| C | poa_required | 7/8 | 3 | 5 | 100.0% | 66.7% | 100.0% | 80.0% | 83.3% |
| C | other_restriction | 2/4 | 4 | 0 | 100.0% | 50.0% | — | 66.7% | 50.0% |
| D | votability | 20/54 | 36 | 15 | 100.0% | 47.2% | 0.0% | 64.2% | 49.1% |
| D | share_blocking | 11/11 | 3 | 8 | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% |
| D | poa_required | 8/8 | 3 | 5 | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% |
| D | other_restriction | 3/4 | 4 | 0 | 100.0% | 75.0% | — | 85.7% | 75.0% |
| E | votability | 38/54 | 36 | 15 | 81.4% | 97.2% | 13.3% | 88.6% | 48.0% |
| E | share_blocking | 11/11 | 3 | 8 | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% |
| E | poa_required | 6/8 | 3 | 5 | 100.0% | 66.7% | 80.0% | 80.0% | 73.3% |
| E | other_restriction | 0/4 | 4 | 0 | — | 0.0% | — | 0.0% | 0.0% |

### C: fallback repairs and damage

| Semantic assertion transition | LLM answer | Reconciled answer |
|---|---:|---:|
| wrong → correct | 6 | 5 |
| correct → correct | 63 | 63 |
| correct → wrong | 2 | 2 |
| wrong → wrong | 6 | 7 |

Case transition matrix: `{"correct \u2192 correct": 35, "wrong \u2192 correct": 12, "wrong \u2192 wrong": 8, "correct \u2192 wrong": 2}`.

**Oracle fallback upper bound** using independent D: 46/57 cases, invoking a generator only on the 20 specialist failures known perfectly by an oracle. The independent generator is a different mode from the actual context-bearing fallback; this is an analytical independent-mode bound, not measured deployable C/E performance. The per-assertion mixing bound is 73/77; it can mix models within a case and is even more optimistic.


### E: fallback repairs and damage

| Semantic assertion transition | LLM answer | Reconciled answer |
|---|---:|---:|
| wrong → correct | 4 | 4 |
| correct → correct | 6 | 6 |
| correct → wrong | 0 | 0 |
| wrong → wrong | 10 | 10 |

Case transition matrix: `{"wrong \u2192 correct": 4, "wrong \u2192 wrong": 8, "correct \u2192 correct": 3}`.

**Oracle fallback upper bound** using independent D: 39/57 cases, invoking a generator only on the 25 specialist failures known perfectly by an oracle. The independent generator is a different mode from the actual context-bearing fallback; this is an analytical independent-mode bound, not measured deployable C/E performance. The per-assertion mixing bound is 62/77; it can mix models within a case and is even more optimistic.

## synthetic-development

NOT BLIND / DEVELOPMENT ONLY, previously exposed key and duplicate overlap.

| Architecture | Cases satisfying all supplied assertions | Frozen scorer v1 | Votability | Blocking YES recall | POA YES recall | Status agreement (labelled n) | LLM calls | Median / p95 ms |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| A | 6/100 | 6/100 | 67/100 | 100.0% (n=11) | 90.9% (n=11) | 24.0% (100) | 0/100 | 52/63 |
| B | 100/100 | 100/100 | 100/100 | 100.0% (n=11) | 100.0% (n=11) | 100.0% (100) | 0/100 | 47/56 |
| C | 19/100 | 19/100 | 93/100 | 90.9% (n=11) | 100.0% (n=11) | 56.0% (100) | 100/100 | 6417/7473 |
| D | 15/100 | 15/100 | 56/100 | 90.9% (n=11) | 90.9% (n=11) | 42.0% (100) | 100/100 | 5006/5684 |
| E | 13/100 | 13/100 | 83/100 | 100.0% (n=11) | 100.0% (n=11) | 29.0% (100) | 36/100 | 190/8281 |

All supplied assertions is a case-level conjunction. On the 57-case challenge it does **not** mean final-status accuracy; only four status labels exist. Unlabelled factors never count as correct. Missing capabilities remain NOT_SUPPORTED and count as wrong. All manual-review flags remain true because the customer gate is disabled.

Labelled-factor exact match (excludes the separately scored status; incomplete truth stays explicitly partial): A: 6/100, B: 100/100, C: 19/100, D: 15/100, E: 13/100.

Common-policy status sensitivity (same new rule table applied to the recorded facts, without inventing missing facts): A: 22/100, B: 50/100, C: 56/100, D: 42/100, E: 29/100.

### Affirmative/negative detection

| Arm | Field | Correct/n | Positive support | Negative support | Positive precision | Positive recall | Specificity | Positive F1 | Balanced accuracy |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| A | votability | 67/100 | 78 | 13 | 89.1% | 73.1% | 69.2% | 80.3% | 51.1% |
| A | share_blocking | 32/100 | 11 | 80 | 15.7% | 100.0% | 25.0% | 27.2% | 45.4% |
| A | poa_required | 77/100 | 11 | 80 | 41.7% | 90.9% | 82.5% | 57.1% | 61.5% |
| A | other_restriction | 59/100 | 20 | 71 | 11.1% | 5.0% | 77.5% | 6.9% | 38.6% |
| B | votability | 100/100 | 78 | 13 | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% |
| B | share_blocking | 100/100 | 11 | 80 | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% |
| B | poa_required | 100/100 | 11 | 80 | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% |
| B | other_restriction | 100/100 | 20 | 71 | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% |
| C | votability | 93/100 | 78 | 13 | 100.0% | 92.3% | 92.3% | 96.0% | 94.9% |
| C | share_blocking | 96/100 | 11 | 80 | 100.0% | 90.9% | 96.2% | 95.2% | 95.7% |
| C | poa_required | 100/100 | 11 | 80 | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% |
| C | other_restriction | 92/100 | 20 | 71 | 100.0% | 60.0% | 100.0% | 75.0% | 86.7% |
| D | votability | 56/100 | 78 | 13 | 100.0% | 60.3% | 0.0% | 75.2% | 53.4% |
| D | share_blocking | 85/100 | 11 | 80 | 100.0% | 90.9% | 85.0% | 95.2% | 84.6% |
| D | poa_required | 86/100 | 11 | 80 | 90.9% | 90.9% | 86.2% | 90.9% | 85.0% |
| D | other_restriction | 78/100 | 20 | 71 | 100.0% | 55.0% | 84.5% | 71.0% | 72.4% |
| E | votability | 83/100 | 78 | 13 | 92.8% | 98.7% | 7.7% | 95.7% | 54.0% |
| E | share_blocking | 94/100 | 11 | 80 | 100.0% | 100.0% | 97.5% | 100.0% | 84.4% |
| E | poa_required | 96/100 | 11 | 80 | 100.0% | 100.0% | 100.0% | 100.0% | 85.2% |
| E | other_restriction | 71/100 | 20 | 71 | 80.0% | 20.0% | 87.3% | 32.0% | 54.3% |

### C: fallback repairs and damage

| Semantic assertion transition | LLM answer | Reconciled answer |
|---|---:|---:|
| wrong → correct | 0 | 0 |
| correct → correct | 381 | 381 |
| correct → wrong | 19 | 19 |
| wrong → wrong | 0 | 0 |

Case transition matrix: `{"correct \u2192 wrong": 81, "correct \u2192 correct": 19}`.

**Oracle fallback upper bound** using independent D: 100/100 cases, invoking a generator only on the 0 specialist failures known perfectly by an oracle. The independent generator is a different mode from the actual context-bearing fallback; this is an analytical independent-mode bound, not measured deployable C/E performance. The per-assertion mixing bound is 400/400; it can mix models within a case and is even more optimistic.


### E: fallback repairs and damage

| Semantic assertion transition | LLM answer | Reconciled answer |
|---|---:|---:|
| wrong → correct | 29 | 27 |
| correct → correct | 93 | 93 |
| correct → wrong | 0 | 0 |
| wrong → wrong | 22 | 24 |

Case transition matrix: `{"wrong \u2192 wrong": 31, "correct \u2192 correct": 5}`.

**Oracle fallback upper bound** using independent D: 16/100 cases, invoking a generator only on the 87 specialist failures known perfectly by an oracle. The independent generator is a different mode from the actual context-bearing fallback; this is an analytical independent-mode bound, not measured deployable C/E performance. The per-assertion mixing bound is 372/400; it can mix models within a case and is even more optimistic.

## complete

SYNTHETIC_COMPLETE_BENCHMARK; complete authored truth, not expert/customer accuracy.

| Architecture | Cases satisfying all supplied assertions | Frozen scorer v1 | Votability | Blocking YES recall | POA YES recall | Status agreement (labelled n) | LLM calls | Median / p95 ms |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| A | 0/48 | 0/48 | 39/48 | 100.0% (n=3) | 66.7% (n=3) | 16.7% (48) | 0/48 | 54/93 |
| B | 0/48 | 0/48 | 47/48 | 0.0% (n=3) | 66.7% (n=3) | 50.0% (48) | 0/48 | 54/94 |
| C | 29/48 | 29/48 | 48/48 | 0.0% (n=3) | 66.7% (n=3) | 79.2% (48) | 48/48 | 6835/8068 |
| D | 28/48 | 28/48 | 37/48 | 100.0% (n=3) | 100.0% (n=3) | 75.0% (48) | 48/48 | 5530/6037 |
| E | 9/48 | 9/48 | 44/48 | 100.0% (n=3) | 100.0% (n=3) | 25.0% (48) | 36/48 | 7202/8841 |

All supplied assertions is a case-level conjunction. On the 57-case challenge it does **not** mean final-status accuracy; only four status labels exist. Unlabelled factors never count as correct. Missing capabilities remain NOT_SUPPORTED and count as wrong. All manual-review flags remain true because the customer gate is disabled.

Labelled-factor exact match (excludes the separately scored status; incomplete truth stays explicitly partial): A: 0/48, B: 0/48, C: 29/48, D: 28/48, E: 9/48.

All-factor exact match (nine semantic fields plus deadline): A: 0/48, B: 0/48, C: 29/48, D: 28/48, E: 9/48.

Common-policy status sensitivity (same new rule table applied to the recorded facts, without inventing missing facts): A: 7/48, B: 10/48, C: 38/48, D: 36/48, E: 12/48.

### Affirmative/negative detection

| Arm | Field | Correct/n | Positive support | Negative support | Positive precision | Positive recall | Specificity | Positive F1 | Balanced accuracy |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| A | votability | 39/48 | 42 | 4 | 97.2% | 83.3% | 75.0% | 89.7% | 69.4% |
| A | share_blocking | 7/48 | 3 | 44 | 7.0% | 100.0% | 9.1% | 13.0% | 36.4% |
| A | poa_required | 31/48 | 3 | 44 | 12.5% | 66.7% | 65.9% | 21.1% | 44.2% |
| A | registration_required | 0/48 | 3 | 45 | — | 0.0% | 0.0% | 0.0% | 0.0% |
| A | beneficial_owner_disclosure_required | 0/48 | 3 | 45 | — | 0.0% | 0.0% | 0.0% | 0.0% |
| A | holding_confirmation_required | 0/48 | 3 | 45 | — | 0.0% | 0.0% | 0.0% | 0.0% |
| A | split_voting_restricted | 0/48 | 3 | 45 | — | 0.0% | 0.0% | 0.0% | 0.0% |
| A | securities_lending_recall_required | 0/48 | 4 | 44 | — | 0.0% | 0.0% | 0.0% | 0.0% |
| A | other_voting_restriction | 0/48 | 3 | 45 | — | 0.0% | 0.0% | 0.0% | 0.0% |
| B | votability | 47/48 | 42 | 4 | 97.7% | 100.0% | 100.0% | 98.8% | 83.3% |
| B | share_blocking | 43/48 | 3 | 44 | — | 0.0% | 97.7% | 0.0% | 32.6% |
| B | poa_required | 44/48 | 3 | 44 | 100.0% | 66.7% | 95.5% | 80.0% | 54.0% |
| B | registration_required | 0/48 | 3 | 45 | — | 0.0% | 0.0% | 0.0% | 0.0% |
| B | beneficial_owner_disclosure_required | 0/48 | 3 | 45 | — | 0.0% | 0.0% | 0.0% | 0.0% |
| B | holding_confirmation_required | 0/48 | 3 | 45 | — | 0.0% | 0.0% | 0.0% | 0.0% |
| B | split_voting_restricted | 0/48 | 3 | 45 | — | 0.0% | 0.0% | 0.0% | 0.0% |
| B | securities_lending_recall_required | 0/48 | 4 | 44 | — | 0.0% | 0.0% | 0.0% | 0.0% |
| B | other_voting_restriction | 0/48 | 3 | 45 | — | 0.0% | 0.0% | 0.0% | 0.0% |
| C | votability | 48/48 | 42 | 4 | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% |
| C | share_blocking | 41/48 | 3 | 44 | — | 0.0% | 93.2% | 0.0% | 31.1% |
| C | poa_required | 44/48 | 3 | 44 | 100.0% | 66.7% | 93.2% | 80.0% | 86.6% |
| C | registration_required | 44/48 | 3 | 45 | 100.0% | 33.3% | 95.6% | 50.0% | 64.4% |
| C | beneficial_owner_disclosure_required | 47/48 | 3 | 45 | 100.0% | 100.0% | 97.8% | 100.0% | 98.9% |
| C | holding_confirmation_required | 45/48 | 3 | 45 | 100.0% | 33.3% | 97.8% | 50.0% | 65.6% |
| C | split_voting_restricted | 47/48 | 3 | 45 | 100.0% | 100.0% | 97.8% | 100.0% | 98.9% |
| C | securities_lending_recall_required | 47/48 | 4 | 44 | 100.0% | 100.0% | 97.7% | 100.0% | 98.9% |
| C | other_voting_restriction | 43/48 | 3 | 45 | 100.0% | 33.3% | 93.3% | 50.0% | 63.3% |
| D | votability | 37/48 | 42 | 4 | 100.0% | 83.3% | 0.0% | 90.9% | 61.1% |
| D | share_blocking | 45/48 | 3 | 44 | 60.0% | 100.0% | 95.5% | 75.0% | 65.2% |
| D | poa_required | 47/48 | 3 | 44 | 100.0% | 100.0% | 97.7% | 100.0% | 99.2% |
| D | registration_required | 46/48 | 3 | 45 | 100.0% | 66.7% | 97.8% | 80.0% | 82.2% |
| D | beneficial_owner_disclosure_required | 47/48 | 3 | 45 | 100.0% | 100.0% | 97.8% | 100.0% | 98.9% |
| D | holding_confirmation_required | 47/48 | 3 | 45 | 100.0% | 100.0% | 97.8% | 100.0% | 98.9% |
| D | split_voting_restricted | 47/48 | 3 | 45 | 100.0% | 100.0% | 97.8% | 100.0% | 98.9% |
| D | securities_lending_recall_required | 47/48 | 4 | 44 | 100.0% | 100.0% | 97.7% | 100.0% | 98.9% |
| D | other_voting_restriction | 46/48 | 3 | 45 | 100.0% | 66.7% | 97.8% | 80.0% | 82.2% |
| E | votability | 44/48 | 42 | 4 | 97.7% | 100.0% | 0.0% | 98.8% | 66.7% |
| E | share_blocking | 45/48 | 3 | 44 | 100.0% | 100.0% | 95.5% | 100.0% | 65.2% |
| E | poa_required | 46/48 | 3 | 44 | 100.0% | 100.0% | 97.7% | 100.0% | 65.9% |
| E | registration_required | 24/48 | 3 | 45 | 100.0% | 33.3% | 51.1% | 50.0% | 42.2% |
| E | beneficial_owner_disclosure_required | 41/48 | 3 | 45 | — | 0.0% | 91.1% | 0.0% | 45.6% |
| E | holding_confirmation_required | 42/48 | 3 | 45 | 100.0% | 66.7% | 88.9% | 80.0% | 77.8% |
| E | split_voting_restricted | 44/48 | 3 | 45 | 100.0% | 33.3% | 95.6% | 50.0% | 64.4% |
| E | securities_lending_recall_required | 23/48 | 4 | 44 | 100.0% | 50.0% | 47.7% | 66.7% | 48.9% |
| E | other_voting_restriction | 41/48 | 3 | 45 | — | 0.0% | 91.1% | 0.0% | 45.6% |

### C: fallback repairs and damage

| Semantic assertion transition | LLM answer | Reconciled answer |
|---|---:|---:|
| wrong → correct | 277 | 275 |
| correct → correct | 131 | 131 |
| correct → wrong | 3 | 3 |
| wrong → wrong | 21 | 23 |

Case transition matrix: `{"wrong \u2192 wrong": 19, "wrong \u2192 correct": 29}`.

**Oracle fallback upper bound** using independent D: 28/48 cases, invoking a generator only on the 48 specialist failures known perfectly by an oracle. The independent generator is a different mode from the actual context-bearing fallback; this is an analytical independent-mode bound, not measured deployable C/E performance. The per-assertion mixing bound is 422/432; it can mix models within a case and is even more optimistic.


### E: fallback repairs and damage

| Semantic assertion transition | LLM answer | Reconciled answer |
|---|---:|---:|
| wrong → correct | 33 | 33 |
| correct → correct | 220 | 220 |
| correct → wrong | 0 | 0 |
| wrong → wrong | 71 | 71 |

Case transition matrix: `{"wrong \u2192 wrong": 30, "wrong \u2192 correct": 6}`.

**Oracle fallback upper bound** using independent D: 30/48 cases, invoking a generator only on the 45 specialist failures known perfectly by an oracle. The independent generator is a different mode from the actual context-bearing fallback; this is an analytical independent-mode bound, not measured deployable C/E performance. The per-assertion mixing bound is 419/432; it can mix models within a case and is even more optimistic.

## Validation and operating point

Only 40 unique examples selected deterministically from the supplied validation file were used for gate selection. All 32 score/margin combinations are retained. Expanded predicate truth is absent from this file, and it overlaps historical training: the operating point is exploratory.

No numerical cutoff improved the selected trade-off. The frozen gate uses UNKNOWN, unsupported required predicates, conflicts and long/truncated input. Required missing capabilities force C to invoke the LLM on every case. E uses nine narrow questions, but only votability, blocking and POA were domain fine-tuned; six targets are generic transfer inference. Too few direct disagreements supported any model-preference rule, so concrete disagreements remain unresolved/manual review.

| Arm | Score threshold | Laya-only coverage | LLM rate | Labelled-assertion agreement (frozen scorer) | Votability FN rate | Median ms |
|---|---:|---:|---:|---:|---:|---:|
| C | None | 0.0% | 100.0% | 82.5% | 8.0% | 7655 |
| C | 0.5 | 0.0% | 100.0% | 82.5% | 8.0% | 7655 |
| C | 0.7 | 0.0% | 100.0% | 82.5% | 8.0% | 7655 |
| C | 0.8 | 0.0% | 100.0% | 82.5% | 8.0% | 7655 |
| C | 0.9 | 0.0% | 100.0% | 82.5% | 8.0% | 7655 |
| C | 0.95 | 0.0% | 100.0% | 82.5% | 8.0% | 7655 |
| C | 0.98 | 0.0% | 100.0% | 82.5% | 8.0% | 7655 |
| C | 0.995 | 0.0% | 100.0% | 82.5% | 8.0% | 7655 |
| E | None | 32.5% | 67.5% | 70.0% | 0.0% | 7418 |
| E | 0.5 | 32.5% | 67.5% | 70.0% | 0.0% | 7418 |
| E | 0.7 | 32.5% | 67.5% | 70.0% | 0.0% | 7418 |
| E | 0.8 | 30.0% | 70.0% | 70.0% | 0.0% | 7473 |
| E | 0.9 | 30.0% | 70.0% | 70.0% | 0.0% | 7473 |
| E | 0.95 | 30.0% | 70.0% | 70.0% | 0.0% | 7473 |
| E | 0.98 | 30.0% | 70.0% | 70.0% | 0.0% | 7473 |
| E | 0.995 | 27.5% | 72.5% | 70.0% | 0.0% | 7511 |

For C the separately stored corrected projection changes validation agreement but cannot change threshold ranking: every grid point made the same calls. E is unaffected. No test metric selected a threshold.

## Limits, remaining errors and next experiment

No additional Laya training was performed. The historical 300-train/100-validation fine-tunes were reused, with their existing duplicate leakage and synthetic-label limitations disclosed. The 57 challenge texts and assertions were not trained on or edited. The 100-row historical key is NOT BLIND / DEVELOPMENT ONLY; every new A–E prediction was committed before the scoring stage reopened it. The 48 complete cases were separately authored, never training/tuning material; eight are standards-derived partial messages, not real SWIFT messages.

The 7,683 public filing excerpts remain unlabelled. Earlier deterministic scanning found no recognised ISO15022; this experiment does not turn those excerpts into verified data. Parser exact tests remain separate from semantic metrics. Structured RDDT values have precedence, narrative conflicts are visible, and unlinked replacement/cancellation messages are quarantined. Date extraction supports a conservative English subset and abstains on unsupported/ambiguous forms.

All per-field accuracy/F1, supports and confusion matrices are in CORRECTED-SUMMARY.json. Each failure and its available native scores/margins is in that file and in the GUI error explorer, with full raw stage trace available by record. Raw model accuracy, evidence verification and final policy agreement have separate metrics. A source-exact quotation is not a verified interpretation.

Latency is measured per sequential warmed notice, including rules/HTTP/generation; model-load records are separate. The fallback modes use their own actual generation, not recycled independent answers. Hardware is a shared 64 GiB Apple M3 Max; these are not dedicated production load tests.

**The next experiment should use expert-labelled real custodian notices, including affirmative restrictions, with frozen event/near-duplicate groups.** Compare independent generation against specialist-first routing on shared supported predicates and all required factors. Do not infer customer safety or enable automation from synthetic success. The repair/damage matrices and call rates, not architectural preference, should determine whether Laya adds value.

Artifacts: `data/experiments/local-llm-v1`. Frozen inference: FREEZE.json. All raw per-arm JSONL files: PREDICTION-COMMIT.json. Original scorer: SUMMARY.json. Corrected scorer and full failures: CORRECTED-SUMMARY.json. Scorer change audit: SCORER-v2-PROJECTIONS.json. Verification: VERIFICATION.json and model reproducibility artifacts when completed.


## Measured fast-path quality and fact attribution

This separates avoiding an LLM call from safe automation. All records still require human review. A wrong accepted case means one or more supplied assertions failed; it is not necessarily a fully labelled final-status error.

| Dataset | Arm | No-LLM accepted cases | Accepted cases meeting all supplied assertions | Wrong accepted cases | LLM calls | Policy UNCERTAIN |
|---|---|---:|---:|---:|---:|---:|
| challenge | C | 0/57 | 0/0 | 0 | 57/57 | 31 |
| challenge | E | 42/57 | 29/42 | 13 | 15/57 | 43 |
| synthetic-development | C | 0/100 | 0/0 | 0 | 100/100 | 53 |
| synthetic-development | E | 64/100 | 8/64 | 56 | 36/100 | 80 |
| complete | C | 0/48 | 0/0 | 0 | 48/48 | 11 |
| complete | E | 12/48 | 3/12 | 9 | 36/48 | 30 |

Independent D raw votability distribution on the challenge: {"VOTABLE": 17, "UNCERTAIN": 40}. This distinguishes model over-abstention from evidence filtering or decision-rule effects. It describes this pinned model/prompt/reasoning configuration, not local LLMs generally. The system-role canary confirmed the runtime received the system instruction.

`ERROR-COST-ANALYSIS.json` provides every repeated expected→predicted pattern and exclusive attribution of ten decision-fact slots per record. No explanation of why a neural model erred was invented. Fact-source counts and detector coverage are not parser accuracy.


## Date-rule sensitivity: do not attribute all B→C gains to the LLM

A/B retain the historical learned temporal head; C/D/E use deterministic deadline logic. The following post-hoc ablation replaces only B's deadline with the already frozen date code and derives its status with the original legacy policy. It changes no semantic prediction and makes no model call.

| Dataset | B native | B + deterministic dates only | C with actual fallback |
|---|---:|---:|---:|
| challenge | 37/57 | 44/57 | 47/57 |
| synthetic-development | 100/100 | 17/100 | 19/100 |
| complete | 0/48 | 0/48 | 29/48 |

These are cases satisfying supplied assertions, not customer accuracy. Policy/schema differences remain, so even the residual gap is not a clean causal estimate of LLM value. C versus independent D also changes prompt context; a later label-context ablation is needed to distinguish specialist information from generic prompting effects. The selected GLM run disables thinking; it does not establish the best achievable performance of this model or local generators generally.


## Oracle fallback analysis — actual fallback context

Independent D and fallback C/E use different prompts/context, so an independent-mode oracle is not an upper bound on context-bearing fallback. This additional diagnostic reuses actual fallback outputs and generates the missing E outputs only for specialist-wrong cases. Those extra calls occur after the timed experiment and are excluded from its call rates/latency. Expected answers are used to select oracle cases only; they are never sent to the model. These outputs must not tune a deployment gate.

| Dataset | Arm | Specialist cases correct | Perfect-gate calls | Oracle raw-fallback switch correct | Oracle frozen-reconciliation correct |
|---|---|---:|---:|---:|---:|
| challenge | C | 37/57 | 20/57 | 50/57 | 49/57 |
| challenge | E | 32/57 | 25/57 | 39/57 | 38/57 |
| synthetic-development | C | 100/100 | 0/100 | 100/100 | 100/100 |
| synthetic-development | E | 13/100 | 87/100 | 15/100 | 15/100 |
| complete | C | 0/48 | 48/48 | 30/48 | 29/48 |
| complete | E | 3/48 | 45/48 | 13/48 | 10/48 |

This is a mode-specific analytical/diagnostic ceiling under perfect knowledge of specialist errors, not measured attainable coverage. No final-status accuracy is inferred for unlabelled challenge cases. Raw outputs are in ORACLE-COUNTERFACTUALS.jsonl; all oracle case outcomes are retained in ORACLE-FALLBACK-ANALYSIS.json.
