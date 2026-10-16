# Controlled local Laya / LLM A–E experiment

**Customer quality gate NOT MET. Automation remains disabled. No customer accuracy is established.**

## Protocol and models

All architectures used the same inputs and supplied truth. A = official base whole-text Laya; B = historical full-encoder fine-tune; C = B plus real local fallback; D = independent local LLM; E = optional ISO parser, fine-tuned narrow Laya, real fallback, reconciliation and rules. No new fine-tuning occurred. Original checkpoints and the 57-case challenge were retained.

Local LLM: `zai-org/GLM-4.7-Flash`, `d1a8a26252f18b34301218d22abd2620a65b85ba4b78987842eb157e01321222`, Q4_K_M, Ollama 0.34.3. Prompt/schema, thresholds and checkpoints were hashed before evaluation; see `FREEZE.json`. Model choice: [LOCAL_LLM_SELECTION.md](LOCAL_LLM_SELECTION.md).

Independent mode never receives Laya predictions. C and E use actual fallback-context generation, not recycled independent answers. LLM confidence is unavailable; native Laya probabilities are not calibrated correctness probabilities. Exact-substring checks quarantine invalid evidence. Structured facts have priority; unresolved disagreements require review. Validation-supported preferences are recorded in VALIDATION-SELECTION.json.

## Data and denominators

The 57 cases contain partial assertions and only four explicit status labels. Historical 30/57 and 37/57 count cases satisfying all supplied assertions; they are not customer accuracy. The old 100-row key is previously exposed and has known train/test duplicate overlap: NOT BLIND / DEVELOPMENT ONLY. The 48-case complete benchmark is separately authored synthetic material, isolated from training/tuning; all nine semantic predicates, deadline status and derived customer status are labelled. Zero expert-labelled production notices were added.

The complete benchmark includes eight standards-derived partial messages, not public production SWIFT data. The existing 7,683 SEC excerpts remain unlabelled; prior scanning found no recognised ISO15022. They do not supply accuracy denominators.

A/B retain frozen legacy five-factor/status behaviour for historical comparability. They cannot independently emit the expanded predicates, which stay NOT_SUPPORTED and count as wrong on complete truth. Status buckets POA_REQUIRED/SHARE_BLOCKING are collapsed to VOTABLE_WITH_RESTRICTION for customer-status comparison, with raw status retained. C/D/E apply the new shared explicit decision policy; policy differences mean improvements are not attributable solely to a generator. A common-policy sensitivity analysis is included below.

## challenge

Scope: Frozen authored partial assertions; repeatedly observed historical benchmark, not a new blind set.

| Architecture | All supplied assertions, cases | Correct assertions | Votability | Blocking YES recall | POA YES recall | Status accuracy (n) | Median / p95 ms | LLM calls |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| A | 30/57 | 59/95 | 34/54 | 100.0% (n=3) | 66.7% (n=3) | 50.0% (4) | 42 / 49 | 0/57 |
| B | 37/57 | 73/95 | 48/54 | 66.7% (n=3) | 66.7% (n=3) | 75.0% (4) | 42 / 52 | 0/57 |
| C | 45/57 | 83/95 | 49/54 | 66.7% (n=3) | 66.7% (n=3) | 100.0% (4) | 6092 / 7620 | 57/57 |
| D | 22/57 | 58/95 | 20/54 | 100.0% (n=3) | 100.0% (n=3) | 75.0% (4) | 4779 / 5870 | 57/57 |
| E | 36/57 | 71/95 | 38/54 | 100.0% (n=3) | 66.7% (n=3) | 75.0% (4) | 153 / 7684 | 15/57 |

Every field's support, positive precision/recall, specificity, F1, balanced accuracy and full confusion matrix is in SUMMARY.json. Every failure, with source text, score/margin where available, conflicts and escalation reasons, is in the corresponding `*-FAILURES.json` and the GUI error explorer.

Common decision-policy status agreement (identical explicit rule table; missing expanded facts remain unresolved): A: 2/4, B: 3/4, C: 4/4, D: 3/4, E: 3/4.

### C: fallback transitions

Final semantic assertion transitions: `{"correct \u2192 correct": 63, "wrong \u2192 correct": 3, "wrong \u2192 wrong": 9, "correct \u2192 wrong": 2}`.

Raw evidence-validated LLM transitions: `{"correct \u2192 correct": 63, "wrong \u2192 correct": 6, "wrong \u2192 wrong": 6, "correct \u2192 wrong": 2}`.

Case transitions: `{"correct \u2192 correct": 35, "wrong \u2192 correct": 10, "wrong \u2192 wrong": 10, "correct \u2192 wrong": 2}`.

Oracle case-switching upper bound: 46/57, with perfect knowledge of 20 failing specialist cases. This is analytical, not deployable routing.

### E: fallback transitions

Final semantic assertion transitions: `{"correct \u2192 correct": 6, "wrong \u2192 correct": 4, "wrong \u2192 wrong": 10}`.

Raw evidence-validated LLM transitions: `{"correct \u2192 correct": 6, "wrong \u2192 correct": 4, "wrong \u2192 wrong": 10}`.

Case transitions: `{"wrong \u2192 correct": 4, "wrong \u2192 wrong": 8, "correct \u2192 correct": 3}`.

Oracle case-switching upper bound: 39/57, with perfect knowledge of 25 failing specialist cases. This is analytical, not deployable routing.

## synthetic-development

Scope: NOT BLIND / DEVELOPMENT ONLY, previously exposed key and duplicate overlap.

| Architecture | All supplied assertions, cases | Correct assertions | Votability | Blocking YES recall | POA YES recall | Status accuracy (n) | Median / p95 ms | LLM calls |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| A | 6/100 | 316/600 | 67/100 | 100.0% (n=11) | 90.9% (n=11) | 24.0% (100) | 52 / 63 | 0/100 |
| B | 100/100 | 600/600 | 100/100 | 100.0% (n=11) | 100.0% (n=11) | 100.0% (100) | 47 / 56 | 0/100 |
| C | 19/100 | 464/600 | 93/100 | 90.9% (n=11) | 100.0% (n=11) | 56.0% (100) | 6417 / 7473 | 100/100 |
| D | 15/100 | 364/600 | 56/100 | 90.9% (n=11) | 90.9% (n=11) | 42.0% (100) | 5006 / 5684 | 100/100 |
| E | 13/100 | 390/600 | 83/100 | 100.0% (n=11) | 100.0% (n=11) | 29.0% (100) | 190 / 8281 | 36/100 |

Every field's support, positive precision/recall, specificity, F1, balanced accuracy and full confusion matrix is in SUMMARY.json. Every failure, with source text, score/margin where available, conflicts and escalation reasons, is in the corresponding `*-FAILURES.json` and the GUI error explorer.

Common decision-policy status agreement (identical explicit rule table; missing expanded facts remain unresolved): A: 22/100, B: 50/100, C: 56/100, D: 42/100, E: 29/100.

### C: fallback transitions

Final semantic assertion transitions: `{"correct \u2192 correct": 389, "correct \u2192 wrong": 11}`.

Raw evidence-validated LLM transitions: `{"correct \u2192 correct": 381, "correct \u2192 wrong": 19}`.

Case transitions: `{"correct \u2192 wrong": 81, "correct \u2192 correct": 19}`.

Oracle case-switching upper bound: 100/100, with perfect knowledge of 0 failing specialist cases. This is analytical, not deployable routing.

### E: fallback transitions

Final semantic assertion transitions: `{"correct \u2192 correct": 93, "wrong \u2192 correct": 27, "wrong \u2192 wrong": 24}`.

Raw evidence-validated LLM transitions: `{"correct \u2192 correct": 93, "wrong \u2192 correct": 29, "wrong \u2192 wrong": 22}`.

Case transitions: `{"wrong \u2192 wrong": 31, "correct \u2192 correct": 5}`.

Oracle case-switching upper bound: 16/100, with perfect knowledge of 87 failing specialist cases. This is analytical, not deployable routing.

## complete

Scope: SYNTHETIC_COMPLETE_BENCHMARK; complete authored truth, not expert/customer accuracy.

| Architecture | All supplied assertions, cases | Correct assertions | Votability | Blocking YES recall | POA YES recall | Status accuracy (n) | Median / p95 ms | LLM calls |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| A | 0/48 | 90/528 | 39/48 | 100.0% (n=3) | 66.7% (n=3) | 16.7% (48) | 54 / 93 | 0/48 |
| B | 0/48 | 199/528 | 47/48 | 0.0% (n=3) | 66.7% (n=3) | 50.0% (48) | 54 / 94 | 0/48 |
| C | 29/48 | 484/528 | 48/48 | 0.0% (n=3) | 66.7% (n=3) | 79.2% (48) | 6835 / 8068 | 48/48 |
| D | 28/48 | 485/528 | 37/48 | 100.0% (n=3) | 100.0% (n=3) | 75.0% (48) | 5530 / 6037 | 48/48 |
| E | 9/48 | 410/528 | 44/48 | 100.0% (n=3) | 100.0% (n=3) | 25.0% (48) | 7202 / 8841 | 36/48 |

Every field's support, positive precision/recall, specificity, F1, balanced accuracy and full confusion matrix is in SUMMARY.json. Every failure, with source text, score/margin where available, conflicts and escalation reasons, is in the corresponding `*-FAILURES.json` and the GUI error explorer.

Common decision-policy status agreement (identical explicit rule table; missing expanded facts remain unresolved): A: 7/48, B: 10/48, C: 38/48, D: 36/48, E: 12/48.

| Architecture | All-factor exact match |
|---|---:|
| A | 0/48 |
| B | 0/48 |
| C | 29/48 |
| D | 28/48 |
| E | 9/48 |

### C: fallback transitions

Final semantic assertion transitions: `{"correct \u2192 correct": 131, "wrong \u2192 wrong": 23, "wrong \u2192 correct": 275, "correct \u2192 wrong": 3}`.

Raw evidence-validated LLM transitions: `{"correct \u2192 correct": 131, "wrong \u2192 correct": 277, "wrong \u2192 wrong": 21, "correct \u2192 wrong": 3}`.

Case transitions: `{"wrong \u2192 wrong": 19, "wrong \u2192 correct": 29}`.

Oracle case-switching upper bound: 28/48, with perfect knowledge of 48 failing specialist cases. This is analytical, not deployable routing.

### E: fallback transitions

Final semantic assertion transitions: `{"correct \u2192 correct": 220, "wrong \u2192 correct": 33, "wrong \u2192 wrong": 71}`.

Raw evidence-validated LLM transitions: `{"correct \u2192 correct": 220, "wrong \u2192 correct": 33, "wrong \u2192 wrong": 71}`.

Case transitions: `{"wrong \u2192 wrong": 30, "wrong \u2192 correct": 6}`.

Oracle case-switching upper bound: 30/48, with perfect knowledge of 45 failing specialist cases. This is analytical, not deployable routing.

## Routing, policy and limitations

Routing was selected on 40 unique, deterministically selected examples from the supplied validation file, never on challenge/test scores. The full threshold sweep records specialist-only coverage, escalation, combined assertion agreement, votability false-negative rate and component latency. Validation is itself AI-synthetic and partly overlaps historical training: any operating point is exploratory. The file lacks truth for the expanded predicates, so it cannot validate their risk.

Whole-text Laya lacks six of the nine individually requested outputs (it supports votability, share blocking and POA; its broad other label is a separate union). Required unsupported fields therefore force fallback in C. This is a measured capability constraint, not a threshold that can be optimised away. E includes a generic holding-confirmation question; only votability, blocking and POA have historical specialist training labels. The other six targets have transfer inference, not dedicated domain supervision.

All manual_review_required flags remain true because the quality gate is disabled. This is distinct from the UNCERTAIN final-status count and from the LLM escalation rate. No synthetic result authorises unattended processing.

Deterministic dates remain a conservative English/current-deadline subset. Unsupported dates, absent timezones and unclear supersession abstain. A source-exact quotation establishes provenance, not that the model interpreted it correctly. ISO lifecycle replacements/cancellations without validated event linkage are quarantined; the previous persistent event ledger is retained, not silently bypassed.

Runtime errors, truncated generations, malformed JSON and invalid evidence are retained and count toward the actual pipeline outcome. Per-notice latency excludes model load; raw generation/load/token timings are saved. Hardware and runtime versions are recorded. GPU temperature-zero repeatability is measured separately, not guaranteed mathematically.

The most valuable next experiment is an independently expert-labelled sample of real custodian notices, including affirmative restrictions and conditional language, held out by event/near-duplicate group. Synthetic success cannot establish production safety. Select between specialist-first and generator-only using the observed error repairs, damage and latency, not a preference for either model.

## Artifacts

Full immutable experiment directory: `data/experiments/local-llm-v1`. `SUMMARY.json`, per-arm JSONL stage traces, `VALIDATION-SELECTION.json`, `PREDICTION-COMMIT.json`, `FREEZE.json` and failure lists provide reproducibility. Model and software checks are in `VERIFICATION.json` when completed.
