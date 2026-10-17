# Qwen domain optimisation

State: **STOPPED_BY_USER** — Stopped safely at explicit user request; completed predictions preserved; no automatic restart.

Automation is disabled. Customer/production accuracy is UNKNOWN. This report is updated from persisted artifacts; an unfinished run is not a completed result.

## Corpus and truth

5,760 unique fact-first constructed texts, 2,880 controlled pairs, six languages, 48 generation families. Authored semantic atoms are composed by deterministic software; these are not 5,760 independent frontier-model generations or domain-expert reviews. English is the primary confidence population. Foreign-language writing has not been certified by native domain experts.

| Split | Records | Duplicate/family groups | Languages |
|---|---:|---:|---|
| TRAIN | 3120 | 20 | {'en': 2160, 'fr': 240, 'es': 300, 'nl': 240, 'de': 60, 'it': 120} |
| SYNTHETIC_FROZEN_TEST | 840 | 5 | {'en': 720, 'de': 60, 'fr': 60} |
| CALIBRATION | 660 | 4 | {'en': 480, 'it': 180} |
| VALIDATION | 660 | 3 | {'en': 480, 'de': 180} |
| ADVERSARIAL_TEST | 240 | 4 | {'en': 180, 'fr': 60} |
| OOD_TEST | 240 | 4 | {'en': 180, 'fr': 60} |

Exact hashes, lexical MinHash/Jaccard and full-document chunk-mean local MiniLM checks group notices before splitting. Minimal pairs and generation families stay together. English MiniLM is not a guarantee of multilingual semantic equivalence. Only a few independent held-out families remain; atom reuse limits external validity. Earlier rejected drafts are preserved and were not benchmarked for model selection.

TRAIN and VALIDATION labels have separate loaders. Frozen/OOD/adversarial answer paths are physically separate and rejected by training loaders. Sealed base predictions may be collected before any training, but frozen answer scoring waits for a final model-selection freeze. This resolves the plan’s base-benchmark/model-selection ordering without using test errors to choose training.

## Exact model and baseline

The immutable QWEN_DIRECT_PRE_DOMAIN_TRAINING manifest pins the installed Qwen3.8:27b-q4_K_M digest, upstream Qwen/Qwen3.8-27B lineage, original common prompt, schema, normalization, rules, checkpoints and historical predictions. Historical Direct achieved92/95 labelled assertions and54/57 case conjunctions; only4 cases supplied a final-status label. It is not customer accuracy. No Laya weights were changed.

## Benchmark, training and calibration

Training decision: **PENDING_BASE_AND_CONSTRAINED_VALIDATION**.

Normal Qwen uses independent mode and receives no Laya outputs. Constrained Qwen uses the identical installed language weights through a pinned local llama.cpp runtime. It receives no labels. Both use the same ten-field truth and deterministic deadline reference. All native requests, scores, evidence, latency and schema outcomes are persisted. All-predicate exact match excludes the separately reported derived customer status.

Numerical confidence is null before support and held-out calibration gates pass. HIGH/MEDIUM/LOW/UNRESOLVED are heuristic bands. Correctness calibrators fit only CALIBRATION/FIT and are evaluated on disjoint duplicate groups in CALIBRATION/EVALUATION. Unsupported languages/OOD/conflicts/schema failures force review. Minimum decisive-predicate confidence is a trust score, not a calibrated joint decision probability.

No domain adapter, learning curve, base/domain repair result, completed stability estimate or calibrated performance is claimed unless the corresponding committed artifact exists. If validation establishes a training target, the run stops short of model selection until data and exact-checkpoint trainer compatibility are audited. Full27B bf16 weights alone need approximately54GB; full-precision training is unsuitable for comfortable64GB operation. Quantized LoRA feasibility remains to be demonstrated.

## Current measured artifacts

Persisted benchmark rows: `{'BASE_QWEN_DIRECT-VALIDATION': 55}`.

The complete formal normal-vs-constrained benchmark, consistency study, calibrated coverage curves, final training decision and independent frozen evaluation remain pending; experiments are stopped at the user’s request. Preflight measurements are software/TRAIN probes and do not establish held-out model quality.

## Parser addendum

Prowide is implemented as a local isolated JVM adapter, but disabled in the frozen primary domain experiment. It introduces no new prompt/data condition here. The separate ISO15022_PROWIDE_EVALUATION report records parser/recovery tests and the7,683-record verification. No parser/source transformation is retroactively applied to historical Qwen results.

## What remains unproven

Synthetic and AI-assisted labels do not establish customer accuracy, customer calibration or production readiness. Independently expert-labelled representative real notices remain the highest-value external validation. Automation remains false, even if a synthetic calibration gate passes.

## Explicit user stop

All experiment coordinators and the isolated local-model runtime are stopped. {'BASE_QWEN_DIRECT-VALIDATION': 55} complete predictions remain preserved, with verified input hashes and valid JSONL. No partial results are labelled a completed benchmark. Frozen inputs/code verified unchanged. The browser application remains running. Resume requires a new user instruction; no automatic restart is scheduled. Stop receipt: data/experiments/qwen-domain-v1/operations/STOP-RECEIPT-8156a292-1ee3-4ee1-a1c4-19d84816c2bd.json.
