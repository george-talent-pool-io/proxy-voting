# Verification — 16 October 2026

The local application runs and preserves auditable decisions. **The zero-shot model does not yet pass the semantic quality gate.** No independently verified customer accuracy or safe automation coverage has been established.

## Corpus and real inference

The replacement public corpus contains 7,683 SEC excerpt rows, not the originally described 15,022 customer notices. There are 1,897 proxy excerpt rows, 5,786 contract distractor rows and 2,931 distinct normalised texts. The source has no verified voting labels. Country, market, ISIN and meeting dates are not guessed. Missing company displays were completed for 1,193 rows only when other publisher metadata for the exact same source filing supplied a single consistent company; each completion retains its reference record ID.

Final ordered run: `0bcd399d-4250-4cb3-9171-acb95f24761e`.

| Check | Actual result |
|---|---:|
| Valid source rows | 7,683 |
| Persisted outputs | 7,683 |
| Failed rows | 0 |
| Invalid probability distributions / NaNs | 0 |
| Source hash mismatches | 0 |
| Distinct model inferences | 2,931 |
| Rows reusing an identical normalised input | 4,752 |
| Inputs with reported context truncation | 562 |
| Human golden reviews in the demo database | 0 |
| Enabled automatic decisions | 0 |

Truncated records retain complete source text and require review. No seven-way class probabilities were fabricated: the system preserves native probabilities for five factor questions. Its policy score is the minimum winning factor probability, explicitly not a calibrated joint-status probability.

## Measured execution

Apple M3 Max, 64 GB host RAM, PyTorch MPS; official Laya SDK 0.4.8 and pinned multilingual weights.

| Measurement | Actual result |
|---|---:|
| Total run wall time | 1,234.52 s (20.58 minutes) |
| Model load | 4.32 s |
| Distinct text throughput | 2.374 texts/s |
| Source row throughput, including duplicate reuse | 6.223 rows/s |
| Median amortised inference | 428.79 ms/text |
| p95 amortised inference | 777.55 ms/text |
| p95 batch wall time | 1,558.15 ms |
| Peak sampled process RSS | 3,634.28 MiB |

These are exploratory measurements from the development host with interface/test activity, not a dedicated hardware benchmark. Per-text latency is amortised batch wall time, not online endpoint latency. RSS excludes device allocations. See [the native benchmark](baseline-benchmark.json) and [run manifest](final-run-manifest.json).

## Application, browser and training checks

- **100 application tests pass**, covering preprocessing, Unicode/HTML, malformed/empty/long inputs, status mapping, thresholds, real SDK score contracts, serialization, configuration/order hashes, grouping, manually calculated metrics, persistence, reviews, golden revision conflicts, exports, date context, training isolation and migration.
- **Eight browser tests pass** against an isolated database: startup, exact source count, search, filters, opening a notice, complete long text, real persisted predictions/scores, invalid input, correction/revision history, golden export, updated metrics, errors, confusion matrix, result downloads, demo settings, batch/reproduction controls and process restart persistence. Browser batch controls use an explicitly named test double in the isolated test server; the full-corpus run and separate reproduction check use real Laya.
- The documented `./scripts/start.sh` command was exercised directly. The final local service runs on port 8000 after restart and dataset activation.
- A **real official Laya training smoke** passed on authored synthetic cases: 29 training, 12 validation and 16 held-out test cases. One CPU epoch made six optimiser updates over 44 labelled training questions. The wrapper fitted validation calibration, exported the checkpoint, reloaded it with integrity checks and produced a valid structured inference. Test examples were not passed into training/calibration. This proves mechanics only; it is not a customer-trained model or evidence of generalisation. See [the smoke record](synthetic-training-smoke.json).
- Docker Compose configuration validates. Builds failed while fetching registry metadata, including a retry using only the Python base image. Container startup remains unverified; native startup is verified.

Full local logs and screenshots are in `artifacts/`. Browser screenshots are smoke artifacts, not cross-platform pixel regression baselines. The in-app browser connector failed before navigation; standalone Playwright supplied the browser verification.

## Actual model-quality gate

Real Laya matched **30 of 57 authored semantic cases** and failed 27. These are hand-authored regression expectations, often labelling only specified factors, not independent customer data or a complete-vector accuracy estimate. The opt-in semantic pytest run reports 27 failures and 31 passes, including its fixture-manifest test. Failures remain visible; they are not xfailed, re-labelled or replaced by rule predictions.

[Every expectation, observation and native score](semantic-challenge.json) is retained. No domain fine-tuned model has been claimed. Human expert labels, adjudication and independent evaluation remain necessary. Automatic processing is disabled; verified accuracy and empirical precision-target coverage remain unknown.

## Reproducibility and duplicate-isolation findings

The first real reproduction check caught a JSON serialization bug: sorted object keys reordered Laya choice options, changing decisions while the original configuration hash stayed equal. Question order and every option order are now explicit versioned arrays, preserved through inference, storage, replay and training exports. Regression tests cover sorted JSON round trips, changed order fingerprints and refusal to replay legacy unordered runs. A fresh real-model four-row run and its reproduction produced **identical factors and native scores**; [the check](reproduction-check.json) records both IDs. Original failed reproduction evidence remains in `artifacts/real-reproduction.json`.

An independent complete exact Jaccard audit found **two cross-split near-duplicate pairs** missed by the original LSH protocol, plus 17 pairs not united into a group. The primary grouper now uses an exact global-frequency prefix-filter join with integer threshold comparisons, tested against exhaustive pairwise joins. The corrected grouping has 1,066 groups; [the exact audit](exact-duplicate-audit.json) finds all 194 near-pairs and **zero ungrouped or cross-split pairs** at the configured 0.85 numeric-masked five-word-shingle threshold. This does not prove absence of all semantic paraphrases below that metric.

Before any review or domain training existed, a versioned database migration corrected 66 group memberships and 16 split assignments. Source text/hashes, every run input and every prediction byte were preserved because split assignment is not a classifier input. The original database and profile are retained. The active database has an immutable dataset-revision record; [migration provenance](grouping-migration.json) includes the backup hash. Final split counts are train 4,427 / validation 1,580 / test 1,676. The final verification recomputed exact grouping from persisted source records.

[Final integrity verification](run-verification.json) checks counts, all structured results and native score distributions, source hashes, model/configuration versions, explicit order fingerprints and exact split isolation. No labels were invented to fill the golden set or produce an accuracy figure.
