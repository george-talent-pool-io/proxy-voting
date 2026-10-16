# Laya training and evaluation

## Decision

Laya was actually fine-tuned locally on the supplied AI-authored training corpus. The results below measure this synthetic task only. They do not establish customer accuracy, safe automation or production readiness. Automation remains disabled. QUALITY GATE NOT MET: zero expert-reviewed, locked independent public test labels.

## Critical interpretation

The perfect supplied synthetic test is **not** broad semantic success. The unchanged challenge improves only 30/57 → 37/57; 6 previously passing cases regress, and 12 challenge errors have policy score ≥98%. These overconfident mistakes directly contradict any claim of safe confidence-based automation.

Fixed cases: agm, blocked-and-poa, blocking, de-vote, historic-fiscal, negotiation, non-voting-bond, past-deadline, poa, poa-waived, quoted-old, record-ordinary, voluntary-tender. Regressions: ambiguous, bank-holiday, issuer-custodian, meeting-only, registration, sell-restricted.

Remaining failed assertions (overlapping): {'classification': 1, 'votable': 6, 'deadline_status': 9, 'other_restriction': 4, 'share_blocking': 1, 'poa_required': 1}. Nine deadline failures include actual controlling-cutoff errors as well as OPEN/UNKNOWN definition conflicts. Six votability failures include ambiguity, contradictions and historical/non-actionable text. Four other-restriction errors plus blocking/POA misses remain. These cannot all be dismissed as a display-taxonomy issue.

See `LAYA_FINETUNED_CHALLENGE_ERRORS.md` for every failed source, expectation, output and score. The performance page defaults its experiment error explorer to these challenge failures; it does not show an empty test-error screen as if no failures exist.

## Protocol and integrity

- Source: `data/training/laya_voting_synthetic_500.zip`; unchanged SHA-256 `d8d342867115c7cc56d3f011a6bcbb8ba5e96a057d3b80ad66b4c48943b64fbf`.
- Only `synthetic_train_300.csv` entered weight optimisation; only `synthetic_validation_100.csv` entered calibration/model selection.
- No labelled test CSV, answer key, or all-500 file was read by training/tuning code. Both base and selected fine-tuned predictions on `synthetic_frozen_test_100_BLIND.csv` were saved and SHA-committed before the scoring pipeline read the answer key.
- Important prior access: before the explicit blind protocol instruction, an inspection script opened/read the all-500 JSONL to print its first two rows. Only SYN-0001 and SYN-0002 labels appeared in the tool output; both are test examples. Other rows were loaded as text but not inspected or used for fitting/selection. This prevents any claim of a pristine blind protocol from the beginning. The 98-case sensitivity means labels not inspected in tool output, not a file-access guarantee. Training/tuning after the explicit instruction used only the whitelisted CSVs.
- Input-only duplicate audit used blind test text before fitting. Following the explicit protocol instruction, the staged scoring pipeline opened the answer key only after the commitments; earlier file access is disclosed above.
- Supplied split preserved exactly, on explicit instruction, despite known duplicate leakage. It is **not an independent frozen test** in the statistical sense.
- 500 rows contain 328 unique texts and 322 lexical groups; 37 exact and 40 near groups span splits. Test: 100 rows / 80 unique texts; 37 test rows overlap training groups, 42 overlap train or validation; 41 validation rows overlap training groups.
- No substantially identical challenge notice was found at the configured Jaccard ≥0.85 threshold. This cannot exclude conceptual/template overlap.
- Existing 57-case expectations were unchanged and never trained on by the new experiment. Historical challenge-trained synthetic-smoke-v1 is explicitly excluded.

## Exact supplied-test comparison

All-field exact match is the primary metric. Macro F1 below is the mean of five field macro F1 scores, with all three configured options included per field. Customer status uses the supplied compatibility precedence. App/challenge precedence is also retained separately.

| Metric | Base Laya | Fine-tuned Laya |
|---|---:|---:|
| All-field exact match | 6.0% | 100.0% |
| Supplied customer-status accuracy | 19.0% | 100.0% |
| Application status vs supplied buckets | 15.0% | 94.0% |
| Mean field macro F1 | 42.6% | 100.0% |
| Status balanced accuracy | 22.8% | 100.0% |
| Status macro F1 | 16.5% | 100.0% |
| Votable precision | 89.1% | 100.0% |
| Votable recall | 73.1% | 100.0% |
| Share-blocking recall | 100.0% | 100.0% |
| POA recall | 90.9% | 100.0% |
| Existing semantic challenge | 30 / 57 | 37 / 57 |
| Median amortised latency | 37.20 ms | 36.44 ms |
| P95 amortised latency | 45.75 ms | 38.82 ms |

Short synthetic notices, batch size 2, same local MPS device. These timings exclude model load and are not the earlier long-filing benchmark. Both timing measurements were made after training stopped.

### Per-field accuracy and F1

| Field | Base accuracy | Tuned accuracy | Base macro F1 | Tuned macro F1 |
|---|---:|---:|---:|---:|
| deadline_status | 57.0% | 100.0% | 0.4623 | 1.0000 |
| other_restriction | 59.0% | 100.0% | 0.3658 | 1.0000 |
| poa_required | 77.0% | 100.0% | 0.5410 | 1.0000 |
| share_blocking | 32.0% | 100.0% | 0.2651 | 1.0000 |
| votable | 67.0% | 100.0% | 0.4975 | 1.0000 |

Every confusion matrix, support, per-class precision/recall/F1, native score distribution, top-two margin and failed source example is retained in `data/experiments/supplied-synthetic-v1/TEST-SCORED.json` and `ALL_TEST_FAILURES.md`. Customer-status matrices are in `customer-status-reports.json`. The GUI exposes every model failure.

### Sensitivity analyses

| Cohort | n | Base exact match | Tuned exact match |
|---|---:|---:|---:|
| Previously uninspected labels | 98 | 6.1% | 100.0% |
| No ≥0.85 duplicate-group overlap with train/validation | 58 | 8.6% | 100.0% |

These sensitivity cohorts are disclosed diagnostics, not substitutes for the requested 100-row score. Removing lexical matches does not establish template or generator independence.

## Answers to the research questions

### 1. Why did baseline fail 27/57?

See `LAYA_BASELINE_FAILURE_ANALYSIS.md`: 20 votability, seven deadline, three blocking, three other-restriction and one POA failed assertions (overlapping). Eleven primary diagnostic patterns cover all 27 failed cases. Votability under conditions, historical scope, negation, unsupported restrictions and temporal handling recur. Neural causal attribution is not established.

### 2. Was the original taxonomy part of the problem?

The baseline already predicted five independent factors; it was never trained as a seven-way classifier. A flat label cannot retain all combinations. The supplied compatibility policy differs from the app policy: blocking overrides POA/other, while the app combines multiple restrictions. This mismatch affects 17 training and six validation rows even with perfect factors. Both mappings are explicit; no expected answer was changed. Supplied OPEN also often means no expired window stated, whereas the app requires an explicit future cutoff. This label-definition mismatch can harm the original challenge.

### 3. Does factorisation improve results?

The controlled zero-shot ablation matched 2/4 flat explicit-status cases and 2/4 factorised cases. That tiny common subset cannot establish superiority. Factorisation preserves required business information. Separating deadline presence from deterministic date comparison changed the 57-case result from 30 to 34; this challenge-informed ablation is not the selected synthetic-trained model or independent validation.

Deterministic v2 extracts only supported English explicit dates, compares injected date/time with explicit offsets, and abstains on ambiguity/unsupported formats. Selection of current/controlling deadline remains a semantic problem. Hashing, HTML removal, duplicate grouping, split assignment, status precedence and calendar arithmetic belong to deterministic software. The supplied-label experiment retains native deadline-status supervision rather than silently relabelling supplied OPEN values.

### 4. How much labelled data was created?

No new expert golden labels were created. The user supplied 500 AI-authored synthetic labels: 300 train, 100 validation, 100 test; 328 distinct texts overall. The separate real public review cohort has 1,000 selected records (600/200/200), one per filing/duplicate group, and zero human reviews. Synthetic labels were never inserted as human golden reviews.

### 5. How was leakage prevented?

For the public study, immutable split membership covers all 7,683 IDs/source hashes and duplicate/filing groups. Frozen-test labels require a later explicit review-revision lock. For the supplied experiment, leakage was detected, not eliminated: exact requested splits were retained on instruction. Normal training remains strict; the synthetic exception verifies exact allowed source IDs, hashes, text and targets. Challenge IDs/text hashes are blocked from training. This synthetic result cannot satisfy an independent-test quality gate.

### 6. How much does fine-tuning improve Laya?

On the exact supplied 100 rows, all-field exact match changed 6.0% → 100.0%. On the preserved 57-case challenge, 30 → 37. These measure different label definitions and must not be combined into one accuracy claim.

Selected candidate: `encoder-4ep`, from decision-head-only and full-encoder, each four epochs, seed 42, official SDK soft cross entropy, option shuffling, internal calibration disabled, validation-only temperature fitting. All training losses/hyperparameters/ID hashes are checkpointed; both candidate reload checks reproduced native scores and decisions on four validation probes exactly. Reload evidence is scoped to those probes and this runtime, not every future device.

### 7. What does the learning curve look like?

The learning curve is specifically for the four-epoch **decision-head-only** variant, not an inferred curve for the selected full-encoder model. Nested source-train subsets are balanced across supplied authoring families, seed 42, same MPS device and fixed 100-row validation set. Duplicate overlap remains.

| Labelled source rows | Distinct texts | Validation exact match | Mean field macro F1 | Votable recall | Restriction recall |
|---:|---:|---:|---:|---:|---:|
| 50 | 45 | 12.0% | 0.5092 | 64.1% | 48.8% |
| 100 | 83 | 20.0% | 0.5379 | 66.7% | 41.9% |
| 200 | 153 | 35.0% | 0.5401 | 74.4% | 34.9% |
| 300 | 214 | 48.0% | 0.5782 | 91.0% | 41.9% |

Sizes 400/800 are unavailable: only the supplied 300 training rows may enter training. No test/validation labels were moved. Figures: `learning-curve.png`, `automation-curve.png`, `training-loss.png` in the experiment directory.

### 8. Is performance still improving?

The table shows measured changes at the available sizes. A single seed, duplicate-heavy synthetic validation set and a head-only curve cannot establish asymptotic sample efficiency or predict performance at 800 real examples. More independent labels are needed.

### 9. Conventional encoder comparison

A separate local MiniLM-L6-v2 frozen mean-pooled encoder with five logistic heads used exactly the supplied 300/100 split. C∈{1,10,100} was selected on validation only; no LLM API was used. Selected test exact match: 97.0%; customer-status accuracy: 97.0%; mean factor macro F1: 0.9808. Its separate challenge result is 24/57. This is a lightweight frozen-encoder baseline, not a fully fine-tuned ModernBERT comparison. Frozen checkpoint, model revision, source hashes and blind commitment are retained under `encoder-baseline/`. [Official encoder model and pooling documentation](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2).

### 10. What can safely be automated?

No threshold is approved. The table below is an exploratory synthetic diagnostic after model freeze; it did not select a policy. Accuracy here means every factor correct among eligible notices above threshold, not merely a correct display bucket. Production automation remains OFF.

| Model | Threshold | Hypothetical coverage | Exact accuracy | Wrong above threshold |
|---|---:|---:|---:|---:|
| base | 0.50 | 28.0% | 3.6% | 27 |
| base | 0.60 | 3.0% | 33.3% | 2 |
| base | 0.70 | 2.0% | 50.0% | 1 |
| base | 0.80 | 0.0% | Not measured | 0 |
| base | 0.90 | 0.0% | Not measured | 0 |
| base | 0.95 | 0.0% | Not measured | 0 |
| base | 0.98 | 0.0% | Not measured | 0 |
| base | 0.99 | 0.0% | Not measured | 0 |
| base | 1.00 | 0.0% | Not measured | 0 |
| fine-tuned | 0.50 | 91.0% | 100.0% | 0 |
| fine-tuned | 0.60 | 91.0% | 100.0% | 0 |
| fine-tuned | 0.70 | 91.0% | 100.0% | 0 |
| fine-tuned | 0.80 | 91.0% | 100.0% | 0 |
| fine-tuned | 0.90 | 91.0% | 100.0% | 0 |
| fine-tuned | 0.95 | 91.0% | 100.0% | 0 |
| fine-tuned | 0.98 | 91.0% | 100.0% | 0 |
| fine-tuned | 0.99 | 91.0% | 100.0% | 0 |
| fine-tuned | 1.00 | 90.0% | 100.0% | 0 |

Proposed configurable gates in `evaluation/quality_gates.json`: at least 200 independently expert-reviewed locked test groups, votable recall≥98%, status macro F1≥90%, sufficient positive restriction support, high-confidence error rate≤1%, and a validation-qualified automation policy whose test group-level 95% precision lower bound≥98% with useful coverage. These are research criteria, not regulatory rules. Current evidence fails independent expert test support. Passing the report would not activate automation automatically.

### 11. Which errors remain?

Fine-tuned supplied test: 0 records have a field or status error. Original challenge: 20 cases fail at least one retained assertion. Every example and score is retained. Label-definition conflicts, difficult context/negation, and dataset/template limitations must be distinguished from actual model error; no challenge expectation was weakened.

### 12. Is Laya good enough for a customer-facing PoC?

It is suitable for an honest research demonstration of local inference, supervised learning and the remaining errors. It is not yet validated for customer voting operations or an accuracy/automation claim. The synthetic test and small exposed-label sensitivity study cannot replace independently reviewed operational notices. The public corpus remains unlabelled.

### 13. Single most valuable next experiment

Have domain experts blindly label and adjudicate the frozen 200-group public test cohort plus the selected training/validation cohort, with an agreed deadline/status definition. Then train on reviewed training data and compare Laya against MiniLM on that genuinely independent test. Do not optimise against the existing synthetic test after reading its answers.

## Audit artifacts

- `protocol.json`: predeclared candidates, source whitelist, seed, exposure disclosure.
- `FREEZE.json`: exact chosen config, criteria, code/dependency/checkpoint hashes and thresholds.
- `base-BLIND-PREDICTIONS.json`, `fine-tuned-BLIND-PREDICTIONS.json`: complete native outputs, source hashes, fixed model versions.
- `BLIND-COMMIT.json`: both prediction digests before answer-key read.
- `TEST-SCORED.json`: all requested metrics/failures and 98-case sensitivity.
- `base-challenge.json`, `fine-tuned-challenge.json`: unchanged 57-case comparison.
- `data/studies/laya-supervised-v1/`: immutable real-corpus membership and unlabelled review queue.

Application and browser test outcomes are recorded separately in `artifacts/research-tests-final.log` and `artifacts/research-e2e-final.log`. Real-model challenge failures remain visible scientific failures.

## Additional validation details

Both complete 100-row frozen Laya predictions were reproduced after checkpoint reload with identical native scores, decisions, statuses, configuration and version fields. `VERIFICATION.json` confirms counts, source hashes, probability validity, zero auto-classification and commitment ordering.

MiniLM test median/p95 amortised latency: 1.01/1.49 ms. MiniLM uses CPU batches of 16, whereas Laya uses MPS batches of two; these are descriptive timings, not a controlled architecture-speed comparison.

The head-only curve improves exact match 12% → 20% → 35% → 48%, but restriction recall is not monotonic (48.8%, 41.9%, 34.9%, 41.9%). It does not establish that restriction understanding keeps improving with more labels. There is no full-encoder learning curve in this phase.

The selected fine-tuned model remains an experimental checkpoint; the 7,683-row application ledger still shows the preserved base-model run. No synthetic-trained model is silently deployed onto public operational records.

Native per-field Brier/log-loss/ECE are in `native-calibration.json`; score-only votable precision/recall sweeps are in `automation-precision-recall.json`. These are post-freeze diagnostics and never fitted new temperatures or thresholds.
