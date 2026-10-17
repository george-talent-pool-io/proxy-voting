# Laya-first cascade evaluation


Updated: 2026-10-17T18:57:57.198851+00:00


**State: STOPPED_BY_USER — Completed rows preserved**. Completion gate remains open until all measurements and regressions are recorded.


Automation is disabled. Every result remains subject to human review. Customer accuracy is unknown. Synthetic and authored results below do not estimate customer quality.


The stopped Qwen domain study is preserved. This is a separately versioned experiment in `data/experiments/laya-first-v2`; no model is retrained.


## Historical quality ceiling

| Condition | Labelled assertions correct /95 | Cases satisfying supplied assertions /57 |
|---|---|---|
| Base whole-notice Laya | 59 | 30 |
| Fine-tuned whole-notice Laya | 73 | 37 |
| Independent Qwen Direct | 92 | 54 |


Only four challenge cases have explicit final-status truth. These historical whole-notice Laya outputs are distinct from the corrected narrow-predicate pipeline; reducer repairs do not change a whole-notice head.


## Corrected Laya and specialist coverage


Same native passage inference is reduced before/after, avoiding checkpoint or batching confounds. Three narrow targets were supervised: votability, share blocking, POA. Six other targets are transfer-only, including registration. Whole-notice votability remains its own supervised head.


### VALIDATION-LAYA

| Predicate | Support | Old reducer correct | Lexical-veto reducer correct | Native-positive reducer correct | Old positive recall | Current positive recall |
|---|---|---|---|---|---|---|
| votability | 80 | 78 | 78 | 78 | 100.0% | 100.0% |
| share_blocking | 80 | 63 | 20 | 38 | 0.0% | 100.0% |
| poa_required | 80 | 65 | 40 | 40 | 0.0% | 100.0% |
| registration_required | 80 | 35 | 45 | 42 | 0.0% | 72.2% |
| beneficial_owner_disclosure_required | 80 | 46 | 54 | 53 | 0.0% | 100.0% |
| holding_confirmation_required | 80 | 39 | 54 | 46 | 0.0% | 100.0% |
| split_voting_restricted | 80 | 54 | 47 | 46 | 0.0% | 0.0% |
| securities_lending_recall_required | 80 | 44 | 62 | 55 | 0.0% | 100.0% |
| other_voting_restriction | 80 | 43 | 42 | 41 | 0.0% | 25.0% |


The first Laya-first revision found all12 blocking-positive validation passages scored native YES=1.0 but vetoed by keyword relevance. Revision2 accepts native semantic affirmative evidence without requiring that vocabulary whitelist. History/background/supersession/current conflicts remain explicit. This correction used validation only; no weights changed. The12positives largely share controlled semantic wording, so they are not12independent linguistic tests.


## Trust signals and safe coverage

Raw winning scores/margins are not calibrated confidence. All passage scores, current/historical states, evidence offsets, support/opposition and UNKNOWN outputs are persisted. Acceptance is a research simulation. Known cross-model disagreements require sufficient validation preference or review.


Routing comparison and safe-coverage estimate pending. No coverage percentage is claimed.


## Actual local speed, batching and prefix reuse

| SDK batch | Notices/sec | Seconds | Label changes vs batch1 |
|---|---|---|---|
| 1 | 0.655 | 24.41 | 0 |
| 8 | 0.78 | 20.51 | 0 |
| 16 | 0.705 | 22.68 | 0 |
| 32 | 0.674 | 23.73 | 0 |


Selected batch: 8; batch-amortised latency is explicitly separate from completion latency.


Gear 2 uses the exact same Qwen GGUF/native process as Gear 3, via the pinned Ollama internal native server. Class mapping A=YES(token32), B=NO(33), C=UNKNOWN(34), checked against official and native tokenizers. All three native alternatives are retained, then normalised over allowed token mass; this is `raw_model_probability`, not calibrated correctness.


Automatic longest-prefix KV reuse is supported in one native slot. This is not a multi-branch encode-once API; full-generation calls may evict it. The private native endpoint is version-pinned and requires compatibility checks on upgrades.

| TRAIN case length | Cache enabled | Three-call wall ms | Retained state tokens (not reused prefix) |
|---|---|---|---|
| 474 | False | 9576 | [606, 608, 604] |
| 474 | True | 9693 | [606, 608, 604] |
| 1191 | False | 12219 | [732, 734, 730] |
| 1191 | True | 12493 | [732, 734, 730] |
| 6152 | False | 28783 | [1689, 1691, 1687] |
| 6152 | True | 17531 | [1689, 1691, 1687] |


## Evidence, reconciliation and confidence


Gear 2 reuses an exact native Laya passage when both document predictions agree; otherwise one context-aware passage scoring call is attempted. The literal candidate and offsets are checked. Missing support escalates; unsupported quotations are never shown. Exact matching verifies quotation identity, not semantic entailment. Supersession/route conflicts remain review reasons.


Gear 3 uses the pinned independent common semantic prompt, without Laya answers, preventing anchoring. Its output is schema/evidence-validated. Dates remain deterministic. Structure is optional and authoritative conflicts remain visible. Ordinary notices bypass ISO parsing.


Calibration fitting/evaluation pending. All numeric correctness confidence is null.


## Frozen comparison, critical recall, repair/damage and oracles


SYNTHETIC_FROZEN_TEST: pending.


ADVERSARIAL_TEST: pending.


OOD_TEST: pending.


CHALLENGE: pending.


## Actual 100 / 1,000-notice throughput


100 notices: pending; no extrapolated throughput is presented.


1000 notices: pending; no extrapolated throughput is presented.


## Training priority and remaining limits


No weights are changed in this phase. Training priority requires validation evidence of repeatable specialist errors and a useful routing opportunity. Missing supervised narrow heads are a distinct limitation; a 92/95 authored Qwen ceiling alone does not justify Qwen fine-tuning.


ISO/Prowide remains a separate future-feed adapter. The existing 7,683 public excerpts previously contained zero recognised ISO15022 structure. Public throughput data has no independent expert truth; it establishes speed and persistence only.


No safe customer acceptance coverage, customer error rate or production readiness can be claimed from these synthetic/authored experiments. The next external quality gate requires representative independently expert-labelled real notices.


## Completion gate


Current persisted state: `{"timestamp": "2026-10-17T18:57:57.185605+00:00", "state": "STOPPED_BY_USER", "stage": "Completed rows preserved", "persisted_rows": {"VALIDATION-GEAR2": 73, "VALIDATION-LAYA": 80, "VALIDATION-FULL": 73}, "automation_enabled": false, "customer_accuracy": null}`


Regression/browser results are recorded separately in `REGRESSION-RESULTS.json` when executed. This report is deliberately a live report until every required measurement completes.


<!-- data-only-results-interpretation-v1 -->

## Measurement interpretation and current completion status

Data-only report revision: 2026-10-17T18:58:13.605467+00:00. Inference source, models, predictions and selection criteria are unchanged.

Current stage: `Completed rows preserved`. Persisted rows: `{"VALIDATION-GEAR2": 73, "VALIDATION-LAYA": 80, "VALIDATION-FULL": 73}`.

For actual prefix reuse use `raw_runtime_response.timings.cache_n`; `tokens_cached` is retained state after prompt evaluation. The measured short/medium notices reused zero tokens. The longest TRAIN notice reused663–667tokens per call; three-call wall time fell28.78→17.53seconds. This single sequential probe does not establish a general speedup. See [runtime notes](LAYA_FIRST_CASCADE_RUNTIME_NOTES.md).

Recorded verification: 2109 ordinary tests;23 browser tests;1 real Laya/native-Qwen/full-Qwen integration test (54.72s). Authored model-quality failures are benchmark outcomes, not deleted or counted as software passes.

**Completion gate OPEN.** Remaining artefacts/measurements: SELECTION.json, CALIBRATION.json, CONFIDENCE-COVERAGE.json, OPERATING-CONFIGURATION-FREEZE.json, SYNTHETIC_FROZEN_TEST-METRICS.json, ADVERSARIAL_TEST-METRICS.json, OOD_TEST-METRICS.json, CHALLENGE-METRICS.json, THROUGHPUT_100-MEASUREMENT.json, THROUGHPUT_1000-MEASUREMENT.json, Complete corrected base-Laya challenge inference.

This study does not establish customer accuracy, safe customer auto-acceptance, calibration on real notices, or production readiness. Representative independently expert-labelled customer notices are still required.
