# Frozen starting checkpoints, customer learning and confidence qualification

The product is the local learning/inference/review framework. The AI-authored corpus, test-trained weights, test calibrators, customer workspaces and private answers are excluded from the source/image delivery. **Automation is disabled. Customer accuracy and a customer review percentage remain unestablished.**

## What changed

- Dataset-free foundation and derivative manifests pin every weight, prompt, semantic criterion and parent identity. Serving a frozen seed needs no access to its old training corpus. Relocation requires identical bytes.
- Both Laya and Qwen can continue from frozen weights/adapters with a new optimizer; trained AI artifacts retain AI_TEST_DERIVATIVE provenance.
- Full-encoder Laya training exposes separate encoder/head learning rates, option-order augmentation, training budgets, gradient checkpointing and an optional MPS memory cap. Long MLX jobs have an explicit configurable timeout.
- Matched whole-notice inference preserves native document labels; evidence lookup never changes them. Opposing current evidence, conditional terms and missing positive evidence force review.
- Correctness calibration is fitted on actual model predictions, independently checked by group, scoped to a population and available per predicate and final decision. Unsupported conditions keep null confidence.
- Calibrated specialist routing and final-cascade calibration use physically separate groups and answer files. Confidence operating points are selected on validation and evaluated without retuning on frozen tests.
- Source-hashed complete-input negative judgements have a separate calibrated evidence stratum. They are neither invented quotes nor deterministic proofs that a restriction is absent.

## Diagnosis and controlled training

The earlier eight-event, head-only run was not enough to assess Laya learning. A subsequent 128 TRAIN / 128 VALIDATION full-encoder run reached 99.48% in the official SDK diagnostic on that older construction population, yet only 4,099/5,400 assertions on the new 600-notice validation population with whole-notice serving. Its affirmative blocking recall was 56/236. Sentence serving with the same weights was worse overall. This is a real composition/distribution gap; the 99.48% figure is not general domain performance.

The corrective experiment starts from the official frozen Laya foundation, uses 200 new TRAIN notices plus 32 TRAIN-only replay notices, all nine labels, encoder LR 0.000025, head LR 0.0001, option shuffling, soft cross-entropy, seed 42 and effective batch 16. Four epochs permit 524 optimizer updates. A predeclared extension allows four further epochs with a fresh optimizer only when validation macro F1 or critical-positive recall is below 0.98. No challenge/frozen answer selected training, criteria or thresholds.

Training support diagnostics explicitly report absent/rare classes. Additional epochs cannot create missing supervision. This run has these development-data support warnings: votability:UNCERTAIN:FEWER_THAN_FIVE_TRAINING_GROUPS, share_blocking:UNKNOWN:FEWER_THAN_FIVE_TRAINING_GROUPS, poa_required:UNKNOWN:FEWER_THAN_FIVE_TRAINING_GROUPS, registration_required:UNKNOWN:FEWER_THAN_FIVE_TRAINING_GROUPS, beneficial_owner_disclosure_required:UNKNOWN:FEWER_THAN_FIVE_TRAINING_GROUPS, holding_confirmation_required:UNKNOWN:FEWER_THAN_FIVE_TRAINING_GROUPS, securities_lending_recall_required:UNKNOWN:FEWER_THAN_FIVE_TRAINING_GROUPS, other_voting_restriction:UNKNOWN:FEWER_THAN_FIVE_TRAINING_GROUPS. The five-group diagnostic is not a regulatory or automation threshold.

Resource trials v1 and v2 were interrupted and preserved before the first completed epoch. The first reached roughly 50 GB physical footprint. The completed condition uses gradient checkpointing, micro-batch 8 / accumulation 2, a 0.45 MPS memory fraction and separate framework validation instead of duplicated SDK diagnostics. An external model workload also shared the Mac; do not attribute all resource differences to one setting.

| Validation condition | Correct / 5,400 assertions | All-nine exact / 600 notices |
|---|---:|---:|
| FOUNDATION | 2882/5400 | 0/600 |
| ADAPTED_4_EPOCHS | 5335/5400 | 543/600 |
| ADAPTED_8_EPOCHS | 5388/5400 | 588/600 |

Validation-selected condition: **ADAPTED_8_EPOCHS**. Eligible conditions: FOUNDATION, ADAPTED_8_EPOCHS. Selection maximises correct assertions subject to no new missed critical positive compared with the foundation.

| Validation predicate | Foundation positive recall | Four epochs | Eight epochs |
|---|---:|---:|---:|
| votability | 0.6100 | 1.0000 | 1.0000 |
| other_voting_restriction | 0.6742 | 0.9318 | 1.0000 |
| registration_required | 0.6797 | 0.9922 | 1.0000 |
| securities_lending_recall_required | 0.8302 | 1.0000 | 1.0000 |
| share_blocking | 0.9958 | 0.9958 | 1.0000 |
| split_voting_restricted | 0.9028 | 1.0000 | 1.0000 |
| holding_confirmation_required | 0.7462 | 1.0000 | 1.0000 |
| poa_required | 0.5536 | 1.0000 | 1.0000 |
| beneficial_owner_disclosure_required | 0.5000 | 0.9961 | 1.0000 |

## Cohort and isolation

2,000 notices / 1,000 composition groups: TRAIN 200/100, VALIDATION 600/300, CALIBRATION 800/400, FROZEN_TEST 400/200. All eight positive restrictions are represented. Truth is constructed first; lexical variants stay with their full fact-composition group. Exact/normalised hashes, numeric-masked five-word lexical grouping and source family checks prevent known cross-role duplicates. The corpus excludes the earlier 128 TRAIN fact compositions. TRAIN/VALIDATION export cannot read held-out answer paths.

**Scope limitation:** English, restriction-focused and all votable. Shared AI-authored sentence atoms cross roles. These are held-out compositions, not independent real linguistic families, non-votable evaluation or expert-reviewed production data. The first baseline evaluator had already scored this controlled frozen cohort; corrective training was preregistered before its outcomes were inspected. This is not a new double-blind independent external study. The new selected model persisted every test prediction before opening its answer file.

All 400 frozen examples also have VOTABLE_WITH_RESTRICTION as their final-status truth. This cohort tests individual restriction combinations, not discrimination among every final-status class.

## Protected selected-model results

**3591/3600 semantic assertions**; **391/400 all-nine exact match**. Final status 324/400; deadline 400/400.

| Predicate | Correct / n | Positive support | Positive recall | Positive misses | Specificity | Macro F1 |
|---|---:|---:|---:|---:|---:|---:|
| votability | 400/400 | 400 | 1.0000 | 0 | N/A | 1.0000 |
| share_blocking | 394/400 | 154 | 1.0000 | 0 | 0.9752 | 0.9894 |
| beneficial_owner_disclosure_required | 400/400 | 172 | 1.0000 | 0 | 1.0000 | 1.0000 |
| other_voting_restriction | 400/400 | 162 | 1.0000 | 0 | 1.0000 | 1.0000 |
| poa_required | 400/400 | 172 | 1.0000 | 0 | 1.0000 | 1.0000 |
| holding_confirmation_required | 400/400 | 152 | 1.0000 | 0 | 1.0000 | 1.0000 |
| securities_lending_recall_required | 400/400 | 182 | 1.0000 | 0 | 1.0000 | 1.0000 |
| split_voting_restricted | 397/400 | 168 | 1.0000 | 0 | 0.9870 | 0.9949 |
| registration_required | 400/400 | 166 | 1.0000 | 0 | 1.0000 | 1.0000 |

Every confusion matrix and failure (source, native scores, margin and provenance) is retained in `data/experiments/customer-adaptation-uncontended-v1/frozen/metrics.json`; complete raw outputs are in `frozen/predictions.jsonl`. Those artifacts stay outside the product archive.

Final-status confusion and every status failure are additionally retained in `frozen/decision-diagnostics.json` and `frozen/final-status-errors.json`. The status mismatches are review abstentions, not missed positive restrictions. The following is a post-scoring explanation of those outputs, not a criteria change:

```json
{
  "scope": "Post-scoring diagnostic only; no model/criteria/threshold changes",
  "prediction_sha256": "df3fd7d24b31794c14d6f48be0d9cde7b37c354f90f92e5674cc66295b1b7d95",
  "answer_sha256": "a5d510e23d8e3238c1d27303c766d9add1d31a9c5a8735db4c3894626807d5de",
  "expected_status_support": {
    "VOTABLE_WITH_RESTRICTION": 400
  },
  "confusion": [
    {
      "expected": "VOTABLE_WITH_RESTRICTION",
      "predicted": "UNCERTAIN_MANUAL_REVIEW",
      "count": 76
    },
    {
      "expected": "VOTABLE_WITH_RESTRICTION",
      "predicted": "VOTABLE_WITH_RESTRICTION",
      "count": 324
    }
  ],
  "errors": 76,
  "all_status_errors_require_review": true,
  "error_conflict_counts": {
    "holding_confirmation_required:SCOPED_EVIDENCE_CONFLICT_OR_CONDITION": 34,
    "registration_required:SCOPED_EVIDENCE_CONFLICT_OR_CONDITION": 42
  }
}
```

Foundation control on the same frozen inputs and current runtime: 1950/3600 semantic assertions; 0/400 all-nine exact. Both models saved every prediction before either set was scored.

## Actual confidence calibration

CALIBRATION FIT/EVALUATION groups are disjoint. Fixed L2 logistic calibration uses FIT-only scaling when both correct and wrong outcomes have support. Otherwise an explicitly non-discriminating Laplace-smoothed constant is used. No mistakes or probabilities are manufactured. Default support is 100 FIT / 50 EVALUATION groups globally and 20 groups per supported prediction/evidence stratum. Confidence is null for unsupported populations, classes, languages, input types, missing positive evidence, UNKNOWN or conflicts. No calibration claim transfers to a different customer population.

| Predicate | Calibration status | Method | EVALUATION n | Brier | ECE |
|---|---|---|---:|---:|---:|
| beneficial_owner_disclosure_required | VALIDATED_IN_DECLARED_POPULATION | BETA_BINOMIAL_CONSTANT | 266 | 0.0000 | 0.0019 |
| final_decision | VALIDATED_IN_DECLARED_POPULATION | LOGISTIC | 266 | 0.0008 | 0.0156 |
| holding_confirmation_required | VALIDATED_IN_DECLARED_POPULATION | BETA_BINOMIAL_CONSTANT | 266 | 0.0000 | 0.0019 |
| other_voting_restriction | VALIDATED_IN_DECLARED_POPULATION | BETA_BINOMIAL_CONSTANT | 266 | 0.0000 | 0.0037 |
| poa_required | VALIDATED_IN_DECLARED_POPULATION | BETA_BINOMIAL_CONSTANT | 266 | 0.0000 | 0.0019 |
| registration_required | VALIDATED_IN_DECLARED_POPULATION | BETA_BINOMIAL_CONSTANT | 266 | 0.0000 | 0.0019 |
| securities_lending_recall_required | VALIDATED_IN_DECLARED_POPULATION | BETA_BINOMIAL_CONSTANT | 266 | 0.0000 | 0.0019 |
| share_blocking | VALIDATED_IN_DECLARED_POPULATION | BETA_BINOMIAL_CONSTANT | 266 | 0.0185 | 0.0039 |
| split_voting_restricted | VALIDATED_IN_DECLARED_POPULATION | BETA_BINOMIAL_CONSTANT | 266 | 0.0038 | 0.0074 |
| votability | VALIDATED_IN_DECLARED_POPULATION | BETA_BINOMIAL_CONSTANT | 266 | 0.0000 | 0.0019 |

Complete required trust available on 118/400 frozen events. Final-status correctness has a separate calibrator. The minimum across required confidences is a conservative routing score, not a calibrated joint probability.

Calibrated predicate errors at confidence ≥0.98: **0**. Every such example, native score and confidence is retained in `frozen/calibrated-high-confidence-errors.json`. Independent frozen Brier/ECE for the supported-confidence subset follows; unsupported outcomes remain in the overall correctness denominator and go to review:

```json
{
  "votability": {
    "n": 324,
    "brier": 3.4807306749834163e-06,
    "ece": 0.001865671641791411,
    "bins": [
      {
        "lower": 0.9,
        "upper": 1.0,
        "n": 324,
        "mean_probability": 0.9981343283582086,
        "observed_correctness": 1.0
      }
    ],
    "correct": 324,
    "wrong": 0,
    "available": 324,
    "total": 400,
    "scope": "Supported-confidence subset only; unavailable outcomes retain review/null"
  },
  "share_blocking": {
    "n": 266,
    "brier": 0.00022276676319893209,
    "ece": 0.014925373134328512,
    "bins": [
      {
        "lower": 0.9,
        "upper": 1.0,
        "n": 266,
        "mean_probability": 0.9850746268656715,
        "observed_correctness": 1.0
      }
    ],
    "correct": 266,
    "wrong": 0,
    "available": 266,
    "total": 400,
    "scope": "Supported-confidence subset only; unavailable outcomes retain review/null"
  },
  "poa_required": {
    "n": 322,
    "brier": 3.4807306749834168e-06,
    "ece": 0.001865671641791411,
    "bins": [
      {
        "lower": 0.9,
        "upper": 1.0,
        "n": 322,
        "mean_probability": 0.9981343283582086,
        "observed_correctness": 1.0
      }
    ],
    "correct": 322,
    "wrong": 0,
    "available": 322,
    "total": 400,
    "scope": "Supported-confidence subset only; unavailable outcomes retain review/null"
  },
  "registration_required": {
    "n": 282,
    "brier": 3.4807306749834168e-06,
    "ece": 0.0018656716417913,
    "bins": [
      {
        "lower": 0.9,
        "upper": 1.0,
        "n": 282,
        "mean_probability": 0.9981343283582087,
        "observed_correctness": 1.0
      }
    ],
    "correct": 282,
    "wrong": 0,
    "available": 282,
    "total": 400,
    "scope": "Supported-confidence subset only; unavailable outcomes retain review/null"
  },
  "beneficial_owner_disclosure_required": {
    "n": 285,
    "brier": 3.480730674983416e-06,
    "ece": 0.001865671641791411,
    "bins": [
      {
        "lower": 0.9,
        "upper": 1.0,
        "n": 285,
        "mean_probability": 0.9981343283582086,
        "observed_correctness": 1.0
      }
    ],
    "correct": 285,
    "wrong": 0,
    "available": 285,
    "total": 400,
    "scope": "Supported-confidence subset only; unavailable outcomes retain review/null"
  },
  "holding_confirmation_required": {
    "n": 272,
    "brier": 3.4807306749834163e-06,
    "ece": 0.0018656716417913,
    "bins": [
      {
        "lower": 0.9,
        "upper": 1.0,
        "n": 272,
        "mean_probability": 0.9981343283582087,
        "observed_correctness": 1.0
      }
    ],
    "correct": 272,
    "wrong": 0,
    "available": 272,
    "total": 400,
    "scope": "Supported-confidence subset only; unavailable outcomes retain review/null"
  },
  "split_voting_restricted": {
    "n": 319,
    "brier": 0.00012530630429939804,
    "ece": 0.011194029850746134,
    "bins": [
      {
        "lower": 0.9,
        "upper": 1.0,
        "n": 319,
        "mean_probability": 0.9888059701492539,
        "observed_correctness": 1.0
      }
    ],
    "correct": 319,
    "wrong": 0,
    "available": 319,
    "total": 400,
    "scope": "Supported-confidence subset only; unavailable outcomes retain review/null"
  },
  "securities_lending_recall_required": {
    "n": 288,
    "brier": 3.4807306749834168e-06,
    "ece": 0.0018656716417913,
    "bins": [
      {
        "lower": 0.9,
        "upper": 1.0,
        "n": 288,
        "mean_probability": 0.9981343283582087,
        "observed_correctness": 1.0
      }
    ],
    "correct": 288,
    "wrong": 0,
    "available": 288,
    "total": 400,
    "scope": "Supported-confidence subset only; unavailable outcomes retain review/null"
  },
  "other_voting_restriction": {
    "n": 276,
    "brier": 1.3922922699932837e-05,
    "ece": 0.003731343283581934,
    "bins": [
      {
        "lower": 0.9,
        "upper": 1.0,
        "n": 276,
        "mean_probability": 0.9962686567164181,
        "observed_correctness": 1.0
      }
    ],
    "correct": 276,
    "wrong": 0,
    "available": 276,
    "total": 400,
    "scope": "Supported-confidence subset only; unavailable outcomes retain review/null"
  }
}
```

## Coverage and review

| Validation threshold | Coverage | Complete-output correctness | Simultaneous precision lower bound | Accepted groups |
|---|---:|---:|---:|---:|
| 0.70 | 31.17% | 1.0000 | 0.9537 | 101 |
| 0.80 | 31.17% | 1.0000 | 0.9537 | 101 |
| 0.90 | 31.17% | 1.0000 | 0.9537 | 101 |
| 0.95 | 31.17% | 1.0000 | 0.9537 | 101 |
| 0.98 | 30.83% | 1.0000 | 0.9528 | 99 |
| 0.99 | 0.00% | N/A | 0.0000 | 0 |

**NO_SUPPORTED_OPERATING_POINT**. The rule requires a 98% complete-output precision lower bound, at least 100 accepted validation groups and zero accepted critical false negatives. The frozen test evaluates the already-fixed point:

```json
{
  "status": "NO_SUPPORTED_OPERATING_POINT",
  "accepted": 0,
  "review_rate": 1.0,
  "benchmark_gate_passed": false,
  "automation_enabled": false
}
```

If no point is supported, every event remains review/escalation. This is a measured negative result, not a missing confidence estimator. Even a supported synthetic point cannot enable customer automation.

The stress cohort deliberately includes unresolved requirements. Review by truth stratum is reported below as a diagnostic; every such record remains in the overall denominator above:

```json
{
  "FULLY_SPECIFIED": {
    "n": 338,
    "selected_point": {
      "status": "NO_SUPPORTED_OPERATING_POINT",
      "accepted": 0,
      "review_rate": 1.0,
      "benchmark_gate_passed": false,
      "automation_enabled": false
    }
  },
  "TRUTH_CONTAINS_UNKNOWN": {
    "n": 62,
    "selected_point": {
      "status": "NO_SUPPORTED_OPERATING_POINT",
      "accepted": 0,
      "review_rate": 1.0,
      "benchmark_gate_passed": false,
      "automation_enabled": false
    }
  }
}
```

## Unchanged authored challenge

70/95 labelled assertions; 34/57 cases satisfying supplied partial assertions. Only four cases have explicit final-status truth. These are not customer/final-status accuracy denominators.

Current-runtime foundation control: 60/95 assertions; 27/57 partial-assertion cases. This explicit nine-predicate whole-notice condition differs from the historical legacy seven-bucket baseline.

## Development Mac timings

Apple M3 Max, 64 GB unified memory. No EC2 run or extrapolation. Request timing excludes model initialisation, queue and network time; first-request kernel warm-up remains included. Throughput includes loading and durable prediction writes. Resource samples are not a complete OS-wide peak unified-memory trace.

| Condition | n | Load s | Median s | Mean s | Min s | Max s | p95 s | notices/s |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| FOUNDATION | 600 | 4.431 | 0.106 | 0.106 | 0.088 | 0.260 | 0.116 | 7.700 |
| ADAPTED_4_EPOCHS | 600 | 3.475 | 0.105 | 0.106 | 0.088 | 0.162 | 0.115 | 7.846 |
| ADAPTED_8_EPOCHS | 600 | 3.449 | 0.119 | 0.119 | 0.089 | 0.175 | 0.133 | 7.140 |
| calibration | 800 | 2.269 | 0.122 | 0.122 | 0.097 | 0.159 | 0.135 | 7.164 |
| frozen | 400 | 2.356 | 0.125 | 0.126 | 0.106 | 0.178 | 0.138 | 6.808 |

Known external local-model workers are recorded in each timing receipt. Overlapping runs are labelled `CONTENDED_WITH_EXTERNAL_MODEL_WORKLOAD`; these are actual development conditions, not isolated server capacity.

## Frozen continuation mechanics

Receipt: `data/experiments/client-learning-verification-uncontended-v1/continuation/result.json`.

```json
{
  "results": {
    "LAYA": {
      "parent_identity": "535b87afd07909079b28cd70543616ea50784848a9b3ddaa66767f80345f0875",
      "parent_unchanged": true,
      "job": "/Users/georgebilchev/wavionex/proxy-voting/data/training-workspace/jobs/continuation-LAYA",
      "result": {
        "backend": "LAYA_SDK",
        "training": {
          "train_items": 18,
          "calibration_items": 0,
          "eval_items": 0,
          "skipped": {},
          "epoch_loss": [
            2.2517293984947173e-07
          ],
          "temperature": [
            1.0,
            1.0,
            1.0
          ],
          "temperature_by_options": {},
          "n_by_bucket": {},
          "calibration": {
            "choice": {
              "items": 0,
              "temperature": 1.0,
              "issues": []
            },
            "score": {
              "items": 0,
              "temperature": 1.0,
              "issues": []
            },
            "noul": {
              "items": 0,
              "temperature": 1.0,
              "issues": []
            }
          },
          "abstention_thresholds": {},
          "train_report": {
            "eval_source": null,
            "eval_mode": null,
            "is_held_out": false,
            "eval_items": 0,
            "note": "No evaluation performed (0 calibration items and no --eval set was provided).",
            "before": null,
            "after": null,
            "comparison": null,
            "calibration": {
              "choice": {
                "items": 0,
                "temperature": 1.0,
                "issues": []
              },
              "score": {
                "items": 0,
                "temperature": 1.0,
                "issues": []
              },
              "noul": {
                "items": 0,
                "temperature": 1.0,
                "issues": []
              }
            },
            "abstention_thresholds": {},
            "training": {
              "epochs": 1,
              "micro_batch": 2,
              "grad_accum": 1,
              "encoder_lr": 2.5e-05,
              "head_lr": 0.0001,
              "min_lr": 1e-06,
              "weight_decay": 0.01,
              "grad_clip": 1.0,
              "loss": "soft-ce",
              "rl_samples": 4,
              "sigma_start": 0.4,
              "sigma_end": 0.1,
              "w_sph": 0.75,
              "w_rps": 1.0,
              "shuffle_options": [
                "choice"
              ],
              "option_layout": null,
              "freeze_encoder": false,
              "calib_max": 0,
              "calib_frac": 0,
              "calib_seed": 20260922,
              "seed": 42,
              "max_len": 2048,
              "head_max_len": 256,
              "amp": null,
              "gradient_checkpointing": true,
              "log_every": 100,
              "label_smoothing": 0.0,
              "text_column": "text",
              "label_column": "label",
              "question_id": "label",
              "instructions": null,
              "eval_data": null,
              "target_error": 0.1,
              "min_abstain_n": 10
            }
          },
          "output_dir": "/Users/georgebilchev/wavionex/proxy-voting/data/training-workspace/jobs/continuation-LAYA/checkpoint"
        },
        "validation_kind": "SDK duplicate validation disabled; independent framework validation REQUIRED before sealing",
        "reload_parity": {
          "passed": true,
          "max_absolute_score_difference": 0.0,
          "absolute_tolerance": 1e-05,
          "probe": "First validation input, two fresh loads"
        }
      },
      "model_manifest_sha256": "42c873204b6796cd0435c8e60fe2f7f3f04b3a2d28d10555158fe6cee9f5394f"
    },
    "QWEN": {
      "parent_identity": "4edd2bf110127eb154c6c9091eac167ca0a49ac97d67442b01e0102cc1a44a7b",
      "parent_unchanged": true,
      "job": "/Users/georgebilchev/wavionex/proxy-voting/data/training-workspace/jobs/continuation-QWEN",
      "result": {
        "backend": "MLX_QLORA",
        "optimiser_steps": 1,
        "micro_batches": 1,
        "trainable_parameters": 94208,
        "weights_changed": true,
        "curve": [
          {
            "kind": "VALIDATION",
            "iteration": 0,
            "val_loss": 0.1401975452899933,
            "val_time": 25.02092658309266
          },
          {
            "kind": "TRAIN",
            "iteration": 1,
            "train_loss": 0.12451139092445374,
            "learning_rate": 4.999999873689376e-05,
            "iterations_per_second": 0.010082498476750712,
            "tokens_per_second": 2.9239245582577063,
            "trained_tokens": 290,
            "peak_memory": 22.963117922
          }
        ],
        "validation_token_cross_entropy": 0.13902804255485535,
        "model_load_ms": 2631.266792071983,
        "peak_mlx_allocated_bytes": 22963117922,
        "elapsed_seconds": 154.67789979209192,
        "reload_parity": {
          "passed": true,
          "max_absolute_logit_difference": 0.0,
          "absolute_relative_tolerance": 0.005,
          "probe_tokens": 128
        },
        "validation_kind": "Teacher-forced JSON loss; not semantic accuracy",
        "training_mask": "Assistant JSON tokens only; complete source, no truncation"
      },
      "model_manifest_sha256": "9ed425c6de7338edf6bf399fd2f0b7e27117cc13f268d87fee6eb49b80bed4ef"
    }
  },
  "scope": "AI_TEST_CONTINUATION_MECHANICS_ONLY",
  "automation_enabled": false,
  "eligible_training_examples": 2,
  "new_validation_examples": 2,
  "qwen_optimizer_steps": 1,
  "qwen_examples_consumed": 1,
  "test_models_in_production_delivery": false
}
```

## Authenticated customer workflow

Receipt: `data/experiments/client-learning-verification-final-v3/customer-replay/receipt.json`.

```json
{
  "scope": "AI_ENGINEERING_REPLAY_NOT_NEW_BLIND_QUALITY",
  "workspace": "/Users/georgebilchev/wavionex/proxy-voting/data/experiments/client-learning-verification-final-v3/customer-replay/workspace",
  "database": "/Users/georgebilchev/wavionex/proxy-voting/data/experiments/client-learning-verification-final-v3/customer-replay/client.sqlite",
  "population": "AI_CLIENT_ENGINEERING_REPLAY",
  "events": 2000,
  "seed_identity": "535b87afd07909079b28cd70543616ea50784848a9b3ddaa66767f80345f0875",
  "release_id": "client-replay-v1-SPECIALIST",
  "calibrator_sha256": "4a9e8047d9194f81eef8575fe8fa3ca83ac56543c060c4313208a0c7a813ff34",
  "calibration_reports": {
    "beneficial_owner_disclosure_required": {
      "status": "VALIDATED_IN_DECLARED_POPULATION",
      "evaluation": {
        "n": 240,
        "brier": 3.166119983283064e-06,
        "ece": 0.001779359430605143,
        "bins": [
          {
            "lower": 0.9,
            "upper": 1.0,
            "n": 240,
            "mean_probability": 0.9982206405693949,
            "observed_correctness": 1.0
          }
        ],
        "correct": 240,
        "wrong": 0
      },
      "support": {
        "fit_examples": 560,
        "evaluation_examples": 240,
        "fit_groups": 280,
        "evaluation_groups": 120,
        "fit_correct": 560,
        "fit_wrong": 0
      },
      "method": "BETA_BINOMIAL_CONSTANT",
      "by_prediction": {
        "NO": {
          "fit": 318,
          "fit_groups": 159,
          "evaluation_groups": 70,
          "evaluation": {
            "n": 140,
            "brier": 3.1661199832830634e-06,
            "ece": 0.001779359430605032,
            "bins": [
              {
                "lower": 0.9,
                "upper": 1.0,
                "n": 140,
                "mean_probability": 0.998220640569395,
                "observed_correctness": 1.0
              }
            ],
            "correct": 140,
            "wrong": 0
          }
        },
        "UNKNOWN": {
          "fit": 12,
          "fit_groups": 6,
          "evaluation_groups": 2,
          "evaluation": {
            "n": 4,
            "brier": 3.166119983283064e-06,
            "ece": 0.001779359430605032,
            "bins": [
              {
                "lower": 0.9,
                "upper": 1.0,
                "n": 4,
                "mean_probability": 0.998220640569395,
                "observed_correctness": 1.0
              }
            ],
            "correct": 4,
            "wrong": 0
          }
        },
        "YES": {
          "fit": 230,
          "fit_groups": 115,
          "evaluation_groups": 48,
          "evaluation": {
            "n": 96,
            "brier": 3.166119983283064e-06,
            "ece": 0.001779359430605143,
            "bins": [
              {
                "lower": 0.9,
                "upper": 1.0,
                "n": 96,
                "mean_probability": 0.9982206405693949,
                "observed_correctness": 1.0
              }
            ],
            "correct": 96,
            "wrong": 0
          }
        }
      },
      "scope": "CUSTOMER_QUALIFICATION",
      "coverage_curve_diagnostic_only": [
        {
          "threshold": 0.7,
          "support": 240,
          "coverage": 1.0,
          "correctness": 1.0,
          "errors": 0,
          "review_rate": 0.0
        },
        {
          "threshold": 0.8,
          "support": 240,
          "coverage": 1.0,
          "correctness": 1.0,
          "errors": 0,
          "review_rate": 0.0
        },
        {
          "threshold": 0.9,
          "support": 240,
          "coverage": 1.0,
          "correctness": 1.0,
          "errors": 0,
          "review_rate": 0.0
        },
        {
          "threshold": 0.95,
          "support": 240,
          "coverage": 1.0,
          "correctness": 1.0,
          "errors": 0,
          "review_rate": 0.0
        },
        {
          "threshold": 0.98,
          "support": 240,
          "coverage": 1.0,
          "correctness": 1.0,
          "errors": 0,
          "review_rate": 0.0
        },
        {
          "threshold": 0.99,
          "support": 240,
          "coverage": 1.0,
          "correctness": 1.0,
          "errors": 0,
          "review_rate": 0.0
        }
      ],
      "note": "Do not tune the operational threshold on the calibration evaluation fold or frozen test"
    },
    "final_decision": {
      "status": "VALIDATED_IN_DECLARED_POPULATION",
      "evaluation": {
        "n": 240,
        "brier": 0.0006132321651970209,
        "ece": 0.015280411346467918,
        "bins": [
          {
            "lower": 0.0,
            "upper": 0.1,
            "n": 36,
            "mean_probability": 0.04805829001948604,
            "observed_correctness": 0.0
          },
          {
            "lower": 0.1,
            "upper": 0.2,
            "n": 2,
            "mean_probability": 0.11268211650408597,
            "observed_correctness": 0.0
          },
          {
            "lower": 0.9,
            "upper": 1.0,
            "n": 202,
            "mean_probability": 0.9915255641116701,
            "observed_correctness": 1.0
          }
        ],
        "correct": 202,
        "wrong": 38
      },
      "support": {
        "fit_examples": 560,
        "evaluation_examples": 240,
        "fit_groups": 280,
        "evaluation_groups": 120,
        "fit_correct": 462,
        "fit_wrong": 98
      },
      "method": "LOGISTIC",
      "by_prediction": {
        "UNCERTAIN_MANUAL_REVIEW": {
          "fit": 100,
          "fit_groups": 50,
          "evaluation_groups": 19,
          "evaluation": {
            "n": 38,
            "brier": 0.0033293245313999924,
            "ece": 0.0514595440449913,
            "bins": [
              {
                "lower": 0.0,
                "upper": 0.1,
                "n": 36,
                "mean_probability": 0.04805829001948604,
                "observed_correctness": 0.0
              },
              {
                "lower": 0.1,
                "upper": 0.2,
                "n": 2,
                "mean_probability": 0.11268211650408597,
                "observed_correctness": 0.0
              }
            ],
            "correct": 0,
            "wrong": 38
          }
        },
        "VOTABLE_WITH_RESTRICTION": {
          "fit": 460,
          "fit_groups": 230,
          "evaluation_groups": 101,
          "evaluation": {
            "n": 202,
            "brier": 0.000102284096307353,
            "ece": 0.008474435888329857,
            "bins": [
              {
                "lower": 0.9,
                "upper": 1.0,
                "n": 202,
                "mean_probability": 0.9915255641116701,
                "observed_correctness": 1.0
              }
            ],
            "correct": 202,
            "wrong": 0
          }
        }
      },
      "scope": "CUSTOMER_QUALIFICATION",
      "coverage_curve_diagnostic_only": [
        {
          "threshold": 0.7,
          "support": 202,
          "coverage": 0.8416666666666667,
          "correctness": 1.0,
          "errors": 0,
          "review_rate": 0.15833333333333333
        },
        {
          "threshold": 0.8,
          "support": 202,
          "coverage": 0.8416666666666667,
          "correctness": 1.0,
          "errors": 0,
          "review_rate": 0.15833333333333333
        },
        {
          "threshold": 0.9,
          "support": 202,
          "coverage": 0.8416666666666667,
          "correctness": 1.0,
          "errors": 0,
          "review_rate": 0.15833333333333333
        },
        {
          "threshold": 0.95,
          "support": 202,
          "coverage": 0.8416666666666667,
          "correctness": 1.0,
          "errors": 0,
          "review_rate": 0.15833333333333333
        },
        {
          "threshold": 0.98,
          "support": 193,
          "coverage": 0.8041666666666667,
          "correctness": 1.0,
          "errors": 0,
          "review_rate": 0.1958333333333333
        },
        {
          "threshold": 0.99,
          "support": 148,
          "coverage": 0.6166666666666667,
          "correctness": 1.0,
          "errors": 0,
          "review_rate": 0.3833333333333333
        }
      ],
      "note": "Do not tune the operational threshold on the calibration evaluation fold or frozen test"
    },
    "holding_confirmation_required": {
      "status": "VALIDATED_IN_DECLARED_POPULATION",
      "evaluation": {
        "n": 240,
        "brier": 3.166119983283064e-06,
        "ece": 0.001779359430605143,
        "bins": [
          {
            "lower": 0.9,
            "upper": 1.0,
            "n": 240,
            "mean_probability": 0.9982206405693949,
            "observed_correctness": 1.0
          }
        ],
        "correct": 240,
        "wrong": 0
      },
      "support": {
        "fit_examples": 560,
        "evaluation_examples": 240,
        "fit_groups": 280,
        "evaluation_groups": 120,
        "fit_correct": 560,
        "fit_wrong": 0
      },
      "method": "BETA_BINOMIAL_CONSTANT",
      "by_prediction": {
        "NO": {
          "fit": 298,
          "fit_groups": 149,
          "evaluation_groups": 72,
          "evaluation": {
            "n": 144,
            "brier": 3.166119983283064e-06,
            "ece": 0.001779359430605032,
            "bins": [
              {
                "lower": 0.9,
                "upper": 1.0,
                "n": 144,
                "mean_probability": 0.998220640569395,
                "observed_correctness": 1.0
              }
            ],
            "correct": 144,
            "wrong": 0
          }
        },
        "UNKNOWN": {
          "fit": 6,
          "fit_groups": 3,
          "evaluation_groups": 1,
          "evaluation": {
            "n": 2,
            "brier": 3.166119983283064e-06,
            "ece": 0.001779359430605032,
            "bins": [
              {
                "lower": 0.9,
                "upper": 1.0,
                "n": 2,
                "mean_probability": 0.998220640569395,
                "observed_correctness": 1.0
              }
            ],
            "correct": 2,
            "wrong": 0
          }
        },
        "YES": {
          "fit": 256,
          "fit_groups": 128,
          "evaluation_groups": 47,
          "evaluation": {
            "n": 94,
            "brier": 3.166119983283063e-06,
            "ece": 0.00177935943060481,
            "bins": [
              {
                "lower": 0.9,
                "upper": 1.0,
                "n": 94,
                "mean_probability": 0.9982206405693952,
                "observed_correctness": 1.0
              }
            ],
            "correct": 94,
            "wrong": 0
          }
        }
      },
      "scope": "CUSTOMER_QUALIFICATION",
      "coverage_curve_diagnostic_only": [
        {
          "threshold": 0.7,
          "support": 240,
          "coverage": 1.0,
          "correctness": 1.0,
          "errors": 0,
          "review_rate": 0.0
        },
        {
          "threshold": 0.8,
          "support": 240,
          "coverage": 1.0,
          "correctness": 1.0,
          "errors": 0,
          "review_rate": 0.0
        },
        {
          "threshold": 0.9,
          "support": 240,
          "coverage": 1.0,
          "correctness": 1.0,
          "errors": 0,
          "review_rate": 0.0
        },
        {
          "threshold": 0.95,
          "support": 240,
          "coverage": 1.0,
          "correctness": 1.0,
          "errors": 0,
          "review_rate": 0.0
        },
        {
          "threshold": 0.98,
          "support": 240,
          "coverage": 1.0,
          "correctness": 1.0,
          "errors": 0,
          "review_rate": 0.0
        },
        {
          "threshold": 0.99,
          "support": 240,
          "coverage": 1.0,
          "correctness": 1.0,
          "errors": 0,
          "review_rate": 0.0
        }
      ],
      "note": "Do not tune the operational threshold on the calibration evaluation fold or frozen test"
    },
    "other_voting_restriction": {
      "status": "VALIDATED_IN_DECLARED_POPULATION",
      "evaluation": {
        "n": 240,
        "brier": 3.166119983283064e-06,
        "ece": 0.001779359430605143,
        "bins": [
          {
            "lower": 0.9,
            "upper": 1.0,
            "n": 240,
            "mean_probability": 0.9982206405693949,
            "observed_correctness": 1.0
          }
        ],
        "correct": 240,
        "wrong": 0
      },
      "support": {
        "fit_examples": 560,
        "evaluation_examples": 240,
        "fit_groups": 280,
        "evaluation_groups": 120,
        "fit_correct": 560,
        "fit_wrong": 0
      },
      "method": "BETA_BINOMIAL_CONSTANT",
      "by_prediction": {
        "NO": {
          "fit": 328,
          "fit_groups": 164,
          "evaluation_groups": 67,
          "evaluation": {
            "n": 134,
            "brier": 3.1661199832830634e-06,
            "ece": 0.001779359430605032,
            "bins": [
              {
                "lower": 0.9,
                "upper": 1.0,
                "n": 134,
                "mean_probability": 0.998220640569395,
                "observed_correctness": 1.0
              }
            ],
            "correct": 134,
            "wrong": 0
          }
        },
        "UNKNOWN": {
          "fit": 14,
          "fit_groups": 7,
          "evaluation_groups": 2,
          "evaluation": {
            "n": 4,
            "brier": 3.166119983283064e-06,
            "ece": 0.001779359430605032,
            "bins": [
              {
                "lower": 0.9,
                "upper": 1.0,
                "n": 4,
                "mean_probability": 0.998220640569395,
                "observed_correctness": 1.0
              }
            ],
            "correct": 4,
            "wrong": 0
          }
        },
        "YES": {
          "fit": 218,
          "fit_groups": 109,
          "evaluation_groups": 51,
          "evaluation": {
            "n": 102,
            "brier": 3.166119983283063e-06,
            "ece": 0.00177935943060481,
            "bins": [
              {
                "lower": 0.9,
                "upper": 1.0,
                "n": 102,
                "mean_probability": 0.9982206405693952,
                "observed_correctness": 1.0
              }
            ],
            "correct": 102,
            "wrong": 0
          }
        }
      },
      "scope": "CUSTOMER_QUALIFICATION",
      "coverage_curve_diagnostic_only": [
        {
          "threshold": 0.7,
          "support": 240,
          "coverage": 1.0,
          "correctness": 1.0,
          "errors": 0,
          "review_rate": 0.0
        },
        {
          "threshold": 0.8,
          "support": 240,
          "coverage": 1.0,
          "correctness": 1.0,
          "errors": 0,
          "review_rate": 0.0
        },
        {
          "threshold": 0.9,
          "support": 240,
          "coverage": 1.0,
          "correctness": 1.0,
          "errors": 0,
          "review_rate": 0.0
        },
        {
          "threshold": 0.95,
          "support": 240,
          "coverage": 1.0,
          "correctness": 1.0,
          "errors": 0,
          "review_rate": 0.0
        },
        {
          "threshold": 0.98,
          "support": 240,
          "coverage": 1.0,
          "correctness": 1.0,
          "errors": 0,
          "review_rate": 0.0
        },
        {
          "threshold": 0.99,
          "support": 240,
          "coverage": 1.0,
          "correctness": 1.0,
          "errors": 0,
          "review_rate": 0.0
        }
      ],
      "note": "Do not tune the operational threshold on the calibration evaluation fold or frozen test"
    },
    "poa_required": {
      "status": "VALIDATED_IN_DECLARED_POPULATION",
      "evaluation": {
        "n": 240,
        "brier": 3.166119983283064e-06,
        "ece": 0.001779359430605143,
        "bins": [
          {
            "lower": 0.9,
            "upper": 1.0,
            "n": 240,
            "mean_probability": 0.9982206405693949,
            "observed_correctness": 1.0
          }
        ],
        "correct": 240,
        "wrong": 0
      },
      "support": {
        "fit_examples": 560,
        "evaluation_examples": 240,
        "fit_groups": 280,
        "evaluation_groups": 120,
        "fit_correct": 560,
        "fit_wrong": 0
      },
      "method": "BETA_BINOMIAL_CONSTANT",
      "by_prediction": {
        "NO": {
          "fit": 310,
          "fit_groups": 155,
          "evaluation_groups": 71,
          "evaluation": {
            "n": 142,
            "brier": 3.166119983283064e-06,
            "ece": 0.001779359430604921,
            "bins": [
              {
                "lower": 0.9,
                "upper": 1.0,
                "n": 142,
                "mean_probability": 0.9982206405693951,
                "observed_correctness": 1.0
              }
            ],
            "correct": 142,
            "wrong": 0
          }
        },
        "UNKNOWN": {
          "fit": 14,
          "fit_groups": 7,
          "evaluation_groups": 4,
          "evaluation": {
            "n": 8,
            "brier": 3.166119983283064e-06,
            "ece": 0.001779359430605032,
            "bins": [
              {
                "lower": 0.9,
                "upper": 1.0,
                "n": 8,
                "mean_probability": 0.998220640569395,
                "observed_correctness": 1.0
              }
            ],
            "correct": 8,
            "wrong": 0
          }
        },
        "YES": {
          "fit": 236,
          "fit_groups": 118,
          "evaluation_groups": 45,
          "evaluation": {
            "n": 90,
            "brier": 3.1661199832830634e-06,
            "ece": 0.001779359430605032,
            "bins": [
              {
                "lower": 0.9,
                "upper": 1.0,
                "n": 90,
                "mean_probability": 0.998220640569395,
                "observed_correctness": 1.0
              }
            ],
            "correct": 90,
            "wrong": 0
          }
        }
      },
      "scope": "CUSTOMER_QUALIFICATION",
      "coverage_curve_diagnostic_only": [
        {
          "threshold": 0.7,
          "support": 240,
          "coverage": 1.0,
          "correctness": 1.0,
          "errors": 0,
          "review_rate": 0.0
        },
        {
          "threshold": 0.8,
          "support": 240,
          "coverage": 1.0,
          "correctness": 1.0,
          "errors": 0,
          "review_rate": 0.0
        },
        {
          "threshold": 0.9,
          "support": 240,
          "coverage": 1.0,
          "correctness": 1.0,
          "errors": 0,
          "review_rate": 0.0
        },
        {
          "threshold": 0.95,
          "support": 240,
          "coverage": 1.0,
          "correctness": 1.0,
          "errors": 0,
          "review_rate": 0.0
        },
        {
          "threshold": 0.98,
          "support": 240,
          "coverage": 1.0,
          "correctness": 1.0,
          "errors": 0,
          "review_rate": 0.0
        },
        {
          "threshold": 0.99,
          "support": 240,
          "coverage": 1.0,
          "correctness": 1.0,
          "errors": 0,
          "review_rate": 0.0
        }
      ],
      "note": "Do not tune the operational threshold on the calibration evaluation fold or frozen test"
    },
    "registration_required": {
      "status": "VALIDATED_IN_DECLARED_POPULATION",
      "evaluation": {
        "n": 240,
        "brier": 3.166119983283064e-06,
        "ece": 0.001779359430605143,
        "bins": [
          {
            "lower": 0.9,
            "upper": 1.0,
            "n": 240,
            "mean_probability": 0.9982206405693949,
            "observed_correctness": 1.0
          }
        ],
        "correct": 240,
        "wrong": 0
      },
      "support": {
        "fit_examples": 560,
        "evaluation_examples": 240,
        "fit_groups": 280,
        "evaluation_groups": 120,
        "fit_correct": 560,
        "fit_wrong": 0
      },
      "method": "BETA_BINOMIAL_CONSTANT",
      "by_prediction": {
        "NO": {
          "fit": 332,
          "fit_groups": 166,
          "evaluation_groups": 68,
          "evaluation": {
            "n": 136,
            "brier": 3.166119983283064e-06,
            "ece": 0.001779359430605143,
            "bins": [
              {
                "lower": 0.9,
                "upper": 1.0,
                "n": 136,
                "mean_probability": 0.9982206405693949,
                "observed_correctness": 1.0
              }
            ],
            "correct": 136,
            "wrong": 0
          }
        },
        "UNKNOWN": {
          "fit": 16,
          "fit_groups": 8,
          "evaluation_groups": 2,
          "evaluation": {
            "n": 4,
            "brier": 3.166119983283064e-06,
            "ece": 0.001779359430605032,
            "bins": [
              {
                "lower": 0.9,
                "upper": 1.0,
                "n": 4,
                "mean_probability": 0.998220640569395,
                "observed_correctness": 1.0
              }
            ],
            "correct": 4,
            "wrong": 0
          }
        },
        "YES": {
          "fit": 212,
          "fit_groups": 106,
          "evaluation_groups": 50,
          "evaluation": {
            "n": 100,
            "brier": 3.166119983283063e-06,
            "ece": 0.001779359430604921,
            "bins": [
              {
                "lower": 0.9,
                "upper": 1.0,
                "n": 100,
                "mean_probability": 0.9982206405693951,
                "observed_correctness": 1.0
              }
            ],
            "correct": 100,
            "wrong": 0
          }
        }
      },
      "scope": "CUSTOMER_QUALIFICATION",
      "coverage_curve_diagnostic_only": [
        {
          "threshold": 0.7,
          "support": 240,
          "coverage": 1.0,
          "correctness": 1.0,
          "errors": 0,
          "review_rate": 0.0
        },
        {
          "threshold": 0.8,
          "support": 240,
          "coverage": 1.0,
          "correctness": 1.0,
          "errors": 0,
          "review_rate": 0.0
        },
        {
          "threshold": 0.9,
          "support": 240,
          "coverage": 1.0,
          "correctness": 1.0,
          "errors": 0,
          "review_rate": 0.0
        },
        {
          "threshold": 0.95,
          "support": 240,
          "coverage": 1.0,
          "correctness": 1.0,
          "errors": 0,
          "review_rate": 0.0
        },
        {
          "threshold": 0.98,
          "support": 240,
          "coverage": 1.0,
          "correctness": 1.0,
          "errors": 0,
          "review_rate": 0.0
        },
        {
          "threshold": 0.99,
          "support": 240,
          "coverage": 1.0,
          "correctness": 1.0,
          "errors": 0,
          "review_rate": 0.0
        }
      ],
      "note": "Do not tune the operational threshold on the calibration evaluation fold or frozen test"
    },
    "securities_lending_recall_required": {
      "status": "VALIDATED_IN_DECLARED_POPULATION",
      "evaluation": {
        "n": 240,
        "brier": 3.166119983283064e-06,
        "ece": 0.001779359430605143,
        "bins": [
          {
            "lower": 0.9,
            "upper": 1.0,
            "n": 240,
            "mean_probability": 0.9982206405693949,
            "observed_correctness": 1.0
          }
        ],
        "correct": 240,
        "wrong": 0
      },
      "support": {
        "fit_examples": 560,
        "evaluation_examples": 240,
        "fit_groups": 280,
        "evaluation_groups": 120,
        "fit_correct": 560,
        "fit_wrong": 0
      },
      "method": "BETA_BINOMIAL_CONSTANT",
      "by_prediction": {
        "NO": {
          "fit": 336,
          "fit_groups": 168,
          "evaluation_groups": 71,
          "evaluation": {
            "n": 142,
            "brier": 3.166119983283064e-06,
            "ece": 0.001779359430604921,
            "bins": [
              {
                "lower": 0.9,
                "upper": 1.0,
                "n": 142,
                "mean_probability": 0.9982206405693951,
                "observed_correctness": 1.0
              }
            ],
            "correct": 142,
            "wrong": 0
          }
        },
        "UNKNOWN": {
          "fit": 14,
          "fit_groups": 7,
          "evaluation_groups": 2,
          "evaluation": {
            "n": 4,
            "brier": 3.166119983283064e-06,
            "ece": 0.001779359430605032,
            "bins": [
              {
                "lower": 0.9,
                "upper": 1.0,
                "n": 4,
                "mean_probability": 0.998220640569395,
                "observed_correctness": 1.0
              }
            ],
            "correct": 4,
            "wrong": 0
          }
        },
        "YES": {
          "fit": 210,
          "fit_groups": 105,
          "evaluation_groups": 47,
          "evaluation": {
            "n": 94,
            "brier": 3.166119983283063e-06,
            "ece": 0.00177935943060481,
            "bins": [
              {
                "lower": 0.9,
                "upper": 1.0,
                "n": 94,
                "mean_probability": 0.9982206405693952,
                "observed_correctness": 1.0
              }
            ],
            "correct": 94,
            "wrong": 0
          }
        }
      },
      "scope": "CUSTOMER_QUALIFICATION",
      "coverage_curve_diagnostic_only": [
        {
          "threshold": 0.7,
          "support": 240,
          "coverage": 1.0,
          "correctness": 1.0,
          "errors": 0,
          "review_rate": 0.0
        },
        {
          "threshold": 0.8,
          "support": 240,
          "coverage": 1.0,
          "correctness": 1.0,
          "errors": 0,
          "review_rate": 0.0
        },
        {
          "threshold": 0.9,
          "support": 240,
          "coverage": 1.0,
          "correctness": 1.0,
          "errors": 0,
          "review_rate": 0.0
        },
        {
          "threshold": 0.95,
          "support": 240,
          "coverage": 1.0,
          "correctness": 1.0,
          "errors": 0,
          "review_rate": 0.0
        },
        {
          "threshold": 0.98,
          "support": 240,
          "coverage": 1.0,
          "correctness": 1.0,
          "errors": 0,
          "review_rate": 0.0
        },
        {
          "threshold": 0.99,
          "support": 240,
          "coverage": 1.0,
          "correctness": 1.0,
          "errors": 0,
          "review_rate": 0.0
        }
      ],
      "note": "Do not tune the operational threshold on the calibration evaluation fold or frozen test"
    },
    "share_blocking": {
      "status": "VALIDATED_IN_DECLARED_POPULATION",
      "evaluation": {
        "n": 240,
        "brier": 0.0003283270103068724,
        "ece": 0.005164140827636684,
        "bins": [
          {
            "lower": 0.1,
            "upper": 0.2,
            "n": 2,
            "mean_probability": 0.18010704260970256,
            "observed_correctness": 0.0
          },
          {
            "lower": 0.9,
            "upper": 1.0,
            "n": 238,
            "mean_probability": 0.9963059675907,
            "observed_correctness": 1.0
          }
        ],
        "correct": 238,
        "wrong": 2
      },
      "support": {
        "fit_examples": 560,
        "evaluation_examples": 240,
        "fit_groups": 280,
        "evaluation_groups": 120,
        "fit_correct": 546,
        "fit_wrong": 14
      },
      "method": "LOGISTIC",
      "by_prediction": {
        "NO": {
          "fit": 322,
          "fit_groups": 166,
          "evaluation_groups": 61,
          "evaluation": {
            "n": 122,
            "brier": 9.194490132389697e-05,
            "ece": 0.003518602938295201,
            "bins": [
              {
                "lower": 0.9,
                "upper": 1.0,
                "n": 122,
                "mean_probability": 0.9964813970617048,
                "observed_correctness": 1.0
              }
            ],
            "correct": 122,
            "wrong": 0
          }
        },
        "UNKNOWN": {
          "fit": 14,
          "fit_groups": 7,
          "evaluation_groups": 1,
          "evaluation": {
            "n": 2,
            "brier": 0.0006218697186427443,
            "ece": 0.02489688079388863,
            "bins": [
              {
                "lower": 0.9,
                "upper": 1.0,
                "n": 2,
                "mean_probability": 0.9751031192061114,
                "observed_correctness": 1.0
              }
            ],
            "correct": 2,
            "wrong": 0
          }
        },
        "YES": {
          "fit": 224,
          "fit_groups": 117,
          "evaluation_groups": 58,
          "evaluation": {
            "n": 116,
            "brier": 0.0005718746989211076,
            "ece": 0.00655457309114664,
            "bins": [
              {
                "lower": 0.1,
                "upper": 0.2,
                "n": 2,
                "mean_probability": 0.18010704260970256,
                "observed_correctness": 0.0
              },
              {
                "lower": 0.9,
                "upper": 1.0,
                "n": 114,
                "mean_probability": 0.9964902070758456,
                "observed_correctness": 1.0
              }
            ],
            "correct": 114,
            "wrong": 2
          }
        }
      },
      "scope": "CUSTOMER_QUALIFICATION",
      "coverage_curve_diagnostic_only": [
        {
          "threshold": 0.7,
          "support": 238,
          "coverage": 0.9916666666666667,
          "correctness": 1.0,
          "errors": 0,
          "review_rate": 0.008333333333333304
        },
        {
          "threshold": 0.8,
          "support": 238,
          "coverage": 0.9916666666666667,
          "correctness": 1.0,
          "errors": 0,
          "review_rate": 0.008333333333333304
        },
        {
          "threshold": 0.9,
          "support": 238,
          "coverage": 0.9916666666666667,
          "correctness": 1.0,
          "errors": 0,
          "review_rate": 0.008333333333333304
        },
        {
          "threshold": 0.95,
          "support": 237,
          "coverage": 0.9875,
          "correctness": 1.0,
          "errors": 0,
          "review_rate": 0.012499999999999956
        },
        {
          "threshold": 0.98,
          "support": 235,
          "coverage": 0.9791666666666666,
          "correctness": 1.0,
          "errors": 0,
          "review_rate": 0.02083333333333337
        },
        {
          "threshold": 0.99,
          "support": 214,
          "coverage": 0.8916666666666667,
          "correctness": 1.0,
          "errors": 0,
          "review_rate": 0.10833333333333328
        }
      ],
      "note": "Do not tune the operational threshold on the calibration evaluation fold or frozen test"
    },
    "split_voting_restricted": {
      "status": "VALIDATED_IN_DECLARED_POPULATION",
      "evaluation": {
        "n": 240,
        "brier": 0.016449259761147906,
        "ece": 0.007769869513642114,
        "bins": [
          {
            "lower": 0.9,
            "upper": 1.0,
            "n": 240,
            "mean_probability": 0.9911032028469754,
            "observed_correctness": 0.9833333333333333
          }
        ],
        "correct": 236,
        "wrong": 4
      },
      "support": {
        "fit_examples": 560,
        "evaluation_examples": 240,
        "fit_groups": 280,
        "evaluation_groups": 120,
        "fit_correct": 556,
        "fit_wrong": 4
      },
      "method": "BETA_BINOMIAL_CONSTANT",
      "by_prediction": {
        "NO": {
          "fit": 322,
          "fit_groups": 163,
          "evaluation_groups": 78,
          "evaluation": {
            "n": 152,
            "brier": 7.915299958207262e-05,
            "ece": 0.008896797153024716,
            "bins": [
              {
                "lower": 0.9,
                "upper": 1.0,
                "n": 152,
                "mean_probability": 0.9911032028469753,
                "observed_correctness": 1.0
              }
            ],
            "correct": 152,
            "wrong": 0
          }
        },
        "UNKNOWN": {
          "fit": 12,
          "fit_groups": 6,
          "evaluation_groups": 3,
          "evaluation": {
            "n": 6,
            "brier": 7.915299958207264e-05,
            "ece": 0.008896797153024827,
            "bins": [
              {
                "lower": 0.9,
                "upper": 1.0,
                "n": 6,
                "mean_probability": 0.9911032028469752,
                "observed_correctness": 1.0
              }
            ],
            "correct": 6,
            "wrong": 0
          }
        },
        "YES": {
          "fit": 226,
          "fit_groups": 115,
          "evaluation_groups": 43,
          "evaluation": {
            "n": 82,
            "brier": 0.04799166059440891,
            "ece": 0.039883690651853376,
            "bins": [
              {
                "lower": 0.9,
                "upper": 1.0,
                "n": 82,
                "mean_probability": 0.9911032028469753,
                "observed_correctness": 0.9512195121951219
              }
            ],
            "correct": 78,
            "wrong": 4
          }
        }
      },
      "scope": "CUSTOMER_QUALIFICATION",
      "coverage_curve_diagnostic_only": [
        {
          "threshold": 0.7,
          "support": 240,
          "coverage": 1.0,
          "correctness": 0.9833333333333333,
          "errors": 4,
          "review_rate": 0.0
        },
        {
          "threshold": 0.8,
          "support": 240,
          "coverage": 1.0,
          "correctness": 0.9833333333333333,
          "errors": 4,
          "review_rate": 0.0
        },
        {
          "threshold": 0.9,
          "support": 240,
          "coverage": 1.0,
          "correctness": 0.9833333333333333,
          "errors": 4,
          "review_rate": 0.0
        },
        {
          "threshold": 0.95,
          "support": 240,
          "coverage": 1.0,
          "correctness": 0.9833333333333333,
          "errors": 4,
          "review_rate": 0.0
        },
        {
          "threshold": 0.98,
          "support": 240,
          "coverage": 1.0,
          "correctness": 0.9833333333333333,
          "errors": 4,
          "review_rate": 0.0
        },
        {
          "threshold": 0.99,
          "support": 240,
          "coverage": 1.0,
          "correctness": 0.9833333333333333,
          "errors": 4,
          "review_rate": 0.0
        }
      ],
      "note": "Do not tune the operational threshold on the calibration evaluation fold or frozen test"
    },
    "votability": {
      "status": "VALIDATED_IN_DECLARED_POPULATION",
      "evaluation": {
        "n": 240,
        "brier": 3.166119983283064e-06,
        "ece": 0.001779359430605143,
        "bins": [
          {
            "lower": 0.9,
            "upper": 1.0,
            "n": 240,
            "mean_probability": 0.9982206405693949,
            "observed_correctness": 1.0
          }
        ],
        "correct": 240,
        "wrong": 0
      },
      "support": {
        "fit_examples": 560,
        "evaluation_examples": 240,
        "fit_groups": 280,
        "evaluation_groups": 120,
        "fit_correct": 560,
        "fit_wrong": 0
      },
      "method": "BETA_BINOMIAL_CONSTANT",
      "by_prediction": {
        "VOTABLE": {
          "fit": 560,
          "fit_groups": 280,
          "evaluation_groups": 120,
          "evaluation": {
            "n": 240,
            "brier": 3.166119983283064e-06,
            "ece": 0.001779359430605143,
            "bins": [
              {
                "lower": 0.9,
                "upper": 1.0,
                "n": 240,
                "mean_probability": 0.9982206405693949,
                "observed_correctness": 1.0
              }
            ],
            "correct": 240,
            "wrong": 0
          }
        }
      },
      "scope": "CUSTOMER_QUALIFICATION",
      "coverage_curve_diagnostic_only": [
        {
          "threshold": 0.7,
          "support": 240,
          "coverage": 1.0,
          "correctness": 1.0,
          "errors": 0,
          "review_rate": 0.0
        },
        {
          "threshold": 0.8,
          "support": 240,
          "coverage": 1.0,
          "correctness": 1.0,
          "errors": 0,
          "review_rate": 0.0
        },
        {
          "threshold": 0.9,
          "support": 240,
          "coverage": 1.0,
          "correctness": 1.0,
          "errors": 0,
          "review_rate": 0.0
        },
        {
          "threshold": 0.95,
          "support": 240,
          "coverage": 1.0,
          "correctness": 1.0,
          "errors": 0,
          "review_rate": 0.0
        },
        {
          "threshold": 0.98,
          "support": 240,
          "coverage": 1.0,
          "correctness": 1.0,
          "errors": 0,
          "review_rate": 0.0
        },
        {
          "threshold": 0.99,
          "support": 240,
          "coverage": 1.0,
          "correctness": 1.0,
          "errors": 0,
          "review_rate": 0.0
        }
      ],
      "note": "Do not tune the operational threshold on the calibration evaluation fold or frozen test"
    }
  },
  "operating_point": {
    "version": "confidence-operating-point-v1",
    "identity": "c1308ba289aeef568a84a48bc92e37d80aaab4f7ec2b83a130f68480df2772f8",
    "calibrator_sha256": "4a9e8047d9194f81eef8575fe8fa3ca83ac56543c060c4313208a0c7a813ff34",
    "validation_sha256": "c6ce497af22860c90dc87401f79c5999414f9e28fab011393b994d703f66b7fa",
    "selection": null,
    "curve": [
      {
        "threshold": 0.7,
        "n": 600,
        "accepted": 183,
        "accepted_groups": 100,
        "coverage": 0.305,
        "review_rate": 0.6950000000000001,
        "correctness": 1.0,
        "wrong_accepted": 0,
        "precision_lower_bound": 0.9532530149597332,
        "critical_false_negatives_accepted": {
          "votability": 0,
          "share_blocking": 0,
          "poa_required": 0,
          "registration_required": 0
        }
      },
      {
        "threshold": 0.8,
        "n": 600,
        "accepted": 183,
        "accepted_groups": 100,
        "coverage": 0.305,
        "review_rate": 0.6950000000000001,
        "correctness": 1.0,
        "wrong_accepted": 0,
        "precision_lower_bound": 0.9532530149597332,
        "critical_false_negatives_accepted": {
          "votability": 0,
          "share_blocking": 0,
          "poa_required": 0,
          "registration_required": 0
        }
      },
      {
        "threshold": 0.9,
        "n": 600,
        "accepted": 183,
        "accepted_groups": 100,
        "coverage": 0.305,
        "review_rate": 0.6950000000000001,
        "correctness": 1.0,
        "wrong_accepted": 0,
        "precision_lower_bound": 0.9532530149597332,
        "critical_false_negatives_accepted": {
          "votability": 0,
          "share_blocking": 0,
          "poa_required": 0,
          "registration_required": 0
        }
      },
      {
        "threshold": 0.95,
        "n": 600,
        "accepted": 182,
        "accepted_groups": 100,
        "coverage": 0.30333333333333334,
        "review_rate": 0.6966666666666667,
        "correctness": 1.0,
        "wrong_accepted": 0,
        "precision_lower_bound": 0.9532530149597332,
        "critical_false_negatives_accepted": {
          "votability": 0,
          "share_blocking": 0,
          "poa_required": 0,
          "registration_required": 0
        }
      },
      {
        "threshold": 0.98,
        "n": 600,
        "accepted": 180,
        "accepted_groups": 98,
        "coverage": 0.3,
        "review_rate": 0.7,
        "correctness": 1.0,
        "wrong_accepted": 0,
        "precision_lower_bound": 0.9523221043043256,
        "critical_false_negatives_accepted": {
          "votability": 0,
          "share_blocking": 0,
          "poa_required": 0,
          "registration_required": 0
        }
      },
      {
        "threshold": 0.99,
        "n": 600,
        "accepted": 135,
        "accepted_groups": 78,
        "coverage": 0.225,
        "review_rate": 0.775,
        "correctness": 1.0,
        "wrong_accepted": 0,
        "precision_lower_bound": 0.9404675824403299,
        "critical_false_negatives_accepted": {
          "votability": 0,
          "share_blocking": 0,
          "poa_required": 0,
          "registration_required": 0
        }
      }
    ],
    "status": "NO_SUPPORTED_OPERATING_POINT",
    "min_precision": 0.98,
    "min_groups": 100,
    "scope": "Declared calibration population only; review simulation, not automation authorisation",
    "automation_enabled": false,
    "sha256": "d270bccc55b48070888eb681f0ef70d522d68069db117978e6e13417f4865450"
  },
  "saved_decisions": 7,
  "numerical_final_confidences": 5,
  "review_required": 7,
  "qualification": {
    "id": "client-replay-v1",
    "plan_sha256": "489071a107744624404c0e5907574966c12b886ddd28ddb524154b09996143cc",
    "predictions_sha256": "c834a3a7a6215b595ff0ac193d0a5c753cb16405fd5969af50dd0fd6ad08d7b9",
    "release_identity": "c1308ba289aeef568a84a48bc92e37d80aaab4f7ec2b83a130f68480df2772f8",
    "created_at": "2026-10-19T09:59:29.842072+00:00",
    "expires_at": "2027-01-17T09:59:29.842085+00:00",
    "population": "AI_CLIENT_ENGINEERING_REPLAY",
    "metrics": {
      "cases": 400,
      "independent_groups": 200,
      "accepted": 82,
      "per_predicate": {
        "votability": {
          "n": 400,
          "correct": 400,
          "accuracy": 1.0,
          "macro_f1": 1.0,
          "f1_by_class": {
            "VOTABLE": 1.0
          },
          "balanced_accuracy": 1.0,
          "positive_label": "VOTABLE",
          "positive_support": 400,
          "negative_support": 0,
          "positive_precision": 1.0,
          "positive_recall": 1.0,
          "negative_recall_specificity": null,
          "positive_f1": 1.0,
          "support": {
            "VOTABLE": 400
          },
          "predicted_support": {
            "VOTABLE": 400
          },
          "labels": [
            "VOTABLE"
          ],
          "confusion_matrix": [
            [
              400
            ]
          ],
          "not_supported": 0
        },
        "share_blocking": {
          "n": 400,
          "correct": 394,
          "accuracy": 0.985,
          "macro_f1": 0.9894464728299978,
          "f1_by_class": {
            "NO": 0.9874476987447699,
            "YES": 0.9808917197452229,
            "UNKNOWN": 1.0
          },
          "balanced_accuracy": 0.9917355371900826,
          "positive_label": "YES",
          "positive_support": 154,
          "negative_support": 242,
          "positive_precision": 0.9625,
          "positive_recall": 1.0,
          "negative_recall_specificity": 0.9752066115702479,
          "positive_f1": 0.9808917197452229,
          "support": {
            "NO": 242,
            "YES": 154,
            "UNKNOWN": 4
          },
          "predicted_support": {
            "NO": 236,
            "YES": 160,
            "UNKNOWN": 4
          },
          "labels": [
            "NO",
            "UNKNOWN",
            "YES"
          ],
          "confusion_matrix": [
            [
              236,
              0,
              6
            ],
            [
              0,
              4,
              0
            ],
            [
              0,
              0,
              154
            ]
          ],
          "not_supported": 0
        },
        "poa_required": {
          "n": 400,
          "correct": 400,
          "accuracy": 1.0,
          "macro_f1": 1.0,
          "f1_by_class": {
            "NO": 1.0,
            "YES": 1.0,
            "UNKNOWN": 1.0
          },
          "balanced_accuracy": 1.0,
          "positive_label": "YES",
          "positive_support": 172,
          "negative_support": 216,
          "positive_precision": 1.0,
          "positive_recall": 1.0,
          "negative_recall_specificity": 1.0,
          "positive_f1": 1.0,
          "support": {
            "NO": 216,
            "YES": 172,
            "UNKNOWN": 12
          },
          "predicted_support": {
            "NO": 216,
            "YES": 172,
            "UNKNOWN": 12
          },
          "labels": [
            "NO",
            "UNKNOWN",
            "YES"
          ],
          "confusion_matrix": [
            [
              216,
              0,
              0
            ],
            [
              0,
              12,
              0
            ],
            [
              0,
              0,
              172
            ]
          ],
          "not_supported": 0
        },
        "registration_required": {
          "n": 400,
          "correct": 400,
          "accuracy": 1.0,
          "macro_f1": 1.0,
          "f1_by_class": {
            "NO": 1.0,
            "YES": 1.0,
            "UNKNOWN": 1.0
          },
          "balanced_accuracy": 1.0,
          "positive_label": "YES",
          "positive_support": 166,
          "negative_support": 230,
          "positive_precision": 1.0,
          "positive_recall": 1.0,
          "negative_recall_specificity": 1.0,
          "positive_f1": 1.0,
          "support": {
            "NO": 230,
            "YES": 166,
            "UNKNOWN": 4
          },
          "predicted_support": {
            "NO": 230,
            "YES": 166,
            "UNKNOWN": 4
          },
          "labels": [
            "NO",
            "UNKNOWN",
            "YES"
          ],
          "confusion_matrix": [
            [
              230,
              0,
              0
            ],
            [
              0,
              4,
              0
            ],
            [
              0,
              0,
              166
            ]
          ],
          "not_supported": 0
        },
        "beneficial_owner_disclosure_required": {
          "n": 400,
          "correct": 400,
          "accuracy": 1.0,
          "macro_f1": 1.0,
          "f1_by_class": {
            "YES": 1.0,
            "NO": 1.0,
            "UNKNOWN": 1.0
          },
          "balanced_accuracy": 1.0,
          "positive_label": "YES",
          "positive_support": 172,
          "negative_support": 220,
          "positive_precision": 1.0,
          "positive_recall": 1.0,
          "negative_recall_specificity": 1.0,
          "positive_f1": 1.0,
          "support": {
            "YES": 172,
            "NO": 220,
            "UNKNOWN": 8
          },
          "predicted_support": {
            "YES": 172,
            "NO": 220,
            "UNKNOWN": 8
          },
          "labels": [
            "NO",
            "UNKNOWN",
            "YES"
          ],
          "confusion_matrix": [
            [
              220,
              0,
              0
            ],
            [
              0,
              8,
              0
            ],
            [
              0,
              0,
              172
            ]
          ],
          "not_supported": 0
        },
        "holding_confirmation_required": {
          "n": 400,
          "correct": 400,
          "accuracy": 1.0,
          "macro_f1": 1.0,
          "f1_by_class": {
            "NO": 1.0,
            "YES": 1.0,
            "UNKNOWN": 1.0
          },
          "balanced_accuracy": 1.0,
          "positive_label": "YES",
          "positive_support": 152,
          "negative_support": 236,
          "positive_precision": 1.0,
          "positive_recall": 1.0,
          "negative_recall_specificity": 1.0,
          "positive_f1": 1.0,
          "support": {
            "NO": 236,
            "YES": 152,
            "UNKNOWN": 12
          },
          "predicted_support": {
            "NO": 236,
            "YES": 152,
            "UNKNOWN": 12
          },
          "labels": [
            "NO",
            "UNKNOWN",
            "YES"
          ],
          "confusion_matrix": [
            [
              236,
              0,
              0
            ],
            [
              0,
              12,
              0
            ],
            [
              0,
              0,
              152
            ]
          ],
          "not_supported": 0
        },
        "split_voting_restricted": {
          "n": 400,
          "correct": 397,
          "accuracy": 0.9925,
          "macro_f1": 0.9948619636851855,
          "f1_by_class": {
            "NO": 0.9934354485776805,
            "YES": 0.9911504424778761,
            "UNKNOWN": 1.0
          },
          "balanced_accuracy": 0.9956521739130434,
          "positive_label": "YES",
          "positive_support": 168,
          "negative_support": 230,
          "positive_precision": 0.9824561403508771,
          "positive_recall": 1.0,
          "negative_recall_specificity": 0.9869565217391304,
          "positive_f1": 0.9911504424778761,
          "support": {
            "NO": 230,
            "YES": 168,
            "UNKNOWN": 2
          },
          "predicted_support": {
            "NO": 227,
            "YES": 171,
            "UNKNOWN": 2
          },
          "labels": [
            "NO",
            "UNKNOWN",
            "YES"
          ],
          "confusion_matrix": [
            [
              227,
              0,
              3
            ],
            [
              0,
              2,
              0
            ],
            [
              0,
              0,
              168
            ]
          ],
          "not_supported": 0
        },
        "securities_lending_recall_required": {
          "n": 400,
          "correct": 400,
          "accuracy": 1.0,
          "macro_f1": 1.0,
          "f1_by_class": {
            "UNKNOWN": 1.0,
            "YES": 1.0,
            "NO": 1.0
          },
          "balanced_accuracy": 1.0,
          "positive_label": "YES",
          "positive_support": 182,
          "negative_support": 208,
          "positive_precision": 1.0,
          "positive_recall": 1.0,
          "negative_recall_specificity": 1.0,
          "positive_f1": 1.0,
          "support": {
            "UNKNOWN": 10,
            "YES": 182,
            "NO": 208
          },
          "predicted_support": {
            "UNKNOWN": 10,
            "YES": 182,
            "NO": 208
          },
          "labels": [
            "NO",
            "UNKNOWN",
            "YES"
          ],
          "confusion_matrix": [
            [
              208,
              0,
              0
            ],
            [
              0,
              10,
              0
            ],
            [
              0,
              0,
              182
            ]
          ],
          "not_supported": 0
        },
        "other_voting_restriction": {
          "n": 400,
          "correct": 400,
          "accuracy": 1.0,
          "macro_f1": 1.0,
          "f1_by_class": {
            "YES": 1.0,
            "NO": 1.0,
            "UNKNOWN": 1.0
          },
          "balanced_accuracy": 1.0,
          "positive_label": "YES",
          "positive_support": 162,
          "negative_support": 228,
          "positive_precision": 1.0,
          "positive_recall": 1.0,
          "negative_recall_specificity": 1.0,
          "positive_f1": 1.0,
          "support": {
            "YES": 162,
            "NO": 228,
            "UNKNOWN": 10
          },
          "predicted_support": {
            "YES": 162,
            "NO": 228,
            "UNKNOWN": 10
          },
          "labels": [
            "NO",
            "UNKNOWN",
            "YES"
          ],
          "confusion_matrix": [
            [
              228,
              0,
              0
            ],
            [
              0,
              10,
              0
            ],
            [
              0,
              0,
              162
            ]
          ],
          "not_supported": 0
        }
      },
      "all_fields_exact_correct": 316,
      "accepted_groups": 47,
      "wrong_auto_processed": 0,
      "measured_auto_precision": 1.0,
      "auto_precision_lower_bound": 0.9066649113412796,
      "review_rate": 0.795,
      "critical": {
        "votability": {
          "positive_support": 400,
          "positive_groups": 200,
          "true_positives": 400,
          "false_negatives": 0,
          "recall_lower_bound": 0.9772372209558107
        },
        "share_blocking": {
          "positive_support": 154,
          "positive_groups": 77,
          "true_positives": 154,
          "false_negatives": 0,
          "recall_lower_bound": 0.9419459301799861
        },
        "poa_required": {
          "positive_support": 172,
          "positive_groups": 86,
          "true_positives": 172,
          "false_negatives": 0,
          "recall_lower_bound": 0.9478599776522384
        },
        "registration_required": {
          "positive_support": 166,
          "positive_groups": 83,
          "true_positives": 166,
          "false_negatives": 0,
          "recall_lower_bound": 0.946027180659862
        }
      },
      "statistical_gate_passed": false,
      "reasons": [
        "INSUFFICIENT_INDEPENDENT_TEST_GROUPS",
        "INSUFFICIENT_AUTO_ACCEPT_GROUPS",
        "AUTO_PRECISION_LOWER_BOUND_NOT_MET",
        "REVIEW_RATE_TARGET_NOT_MET",
        "votability:INSUFFICIENT_POSITIVE_GROUPS",
        "votability:RECALL_LOWER_BOUND_NOT_MET",
        "share_blocking:INSUFFICIENT_POSITIVE_GROUPS",
        "share_blocking:RECALL_LOWER_BOUND_NOT_MET",
        "poa_required:INSUFFICIENT_POSITIVE_GROUPS",
        "poa_required:RECALL_LOWER_BOUND_NOT_MET",
        "registration_required:INSUFFICIENT_POSITIVE_GROUPS",
        "registration_required:RECALL_LOWER_BOUND_NOT_MET"
      ],
      "bound_method": "One-sided exact binomial bounds on worst-outcome independent groups; Bonferroni over five claims",
      "policy": {
        "threshold": 0.99,
        "min_test_groups": 500,
        "min_auto_groups": 300,
        "min_positive_groups": 300,
        "min_auto_precision_lower_bound": 0.98,
        "min_critical_recall_lower_bound": 0.98,
        "max_review_rate": 0.1,
        "confidence_level": 0.95,
        "validity_days": 90
      }
    },
    "customer_gate_passed": false,
    "reasons": [
      "AUTO_PRECISION_LOWER_BOUND_NOT_MET",
      "EXPERT_CALIBRATION_REQUIRED",
      "INDEPENDENT_AUTHENTICATED_EXPERT_LABELS_REQUIRED",
      "INSUFFICIENT_AUTO_ACCEPT_GROUPS",
      "INSUFFICIENT_INDEPENDENT_TEST_GROUPS",
      "REVIEW_RATE_TARGET_NOT_MET",
      "SYNTHETIC_OR_NONEXPERT_TEST_LABELS",
      "poa_required:INSUFFICIENT_POSITIVE_GROUPS",
      "poa_required:RECALL_LOWER_BOUND_NOT_MET",
      "registration_required:INSUFFICIENT_POSITIVE_GROUPS",
      "registration_required:RECALL_LOWER_BOUND_NOT_MET",
      "share_blocking:INSUFFICIENT_POSITIVE_GROUPS",
      "share_blocking:RECALL_LOWER_BOUND_NOT_MET",
      "votability:INSUFFICIENT_POSITIVE_GROUPS",
      "votability:RECALL_LOWER_BOUND_NOT_MET"
    ],
    "reviewers": [
      "AI framework construction"
    ],
    "automation_enabled": false,
    "customer_accuracy": null,
    "scope": "Measured held-out population only; not a guarantee on arbitrary future notices"
  },
  "audit": {
    "entries": 2017,
    "head": "3aa449ab02338eb47286286f269bf3ac9313c69c49dab364a3703b6c25fd26ae",
    "valid": true,
    "limitation": "Export the head to customer-controlled immutable storage; a database administrator can rewrite an entire local database"
  },
  "automation_enabled": false,
  "test_models_in_product": false,
  "calibrated_cascade_probe": {
    "stage_partition": "LAYA_STAGE",
    "stage_operating_status": "NO_SUPPORTED_OPERATING_POINT",
    "persisted_executions": 2,
    "llm_invocations": 2,
    "final_confidence_not_inherited": true,
    "all_manual_review": true,
    "scope": "Real stage-routing integration, not final-pipeline quality qualification"
  }
}
```

## Persisted calibrated browser and restart

Receipt: `data/experiments/client-learning-verification-final-v3/customer-browser/receipt.json`.

```json
{
  "actual_persisted_decisions": 7,
  "numerical_confidence_decisions": 5,
  "restart_byte_semantic_parity": true,
  "browser_errors": [],
  "screenshot": "calibrated-decision.png",
  "automation_enabled": false,
  "transport": "Loopback only; temporary credential removed",
  "scope": "AI engineering replay, not a new customer quality evaluation"
}
```

## Real two-model release integration

Receipt: `data/experiments/client-learning-verification-final-v3/receipt.json`.

```json
{
  "scope": "AI_ENGINEERING_QUALIFICATION_ONLY",
  "study": "data/experiments/customer-adaptation-uncontended-v1",
  "quality_selected": "ADAPTED_8_EPOCHS",
  "engineering_derivative": "ADAPTED_8_EPOCHS",
  "real_model_tests": 2,
  "campaign": "client-learning-verification-final-v3-integration",
  "continuation_receipt": "data/experiments/client-learning-verification-uncontended-v1/continuation/result.json",
  "client_receipt": "data/experiments/client-learning-verification-final-v3/customer-replay/receipt.json",
  "browser_receipt": "data/experiments/client-learning-verification-final-v3/customer-browser/receipt.json",
  "automation_enabled": false
}
```

## Delivery boundary and remaining qualification

The source archive and Docker image contain no new AI corpus, test-trained weights, optimizer state, customer database, private answer keys or test calibrator. Provision pinned foundation weights separately and create a fresh customer workspace. A frozen foundation identity is not a domain-accuracy certificate.

Linux ARM64 service startup/authentication/read-only execution/restart persistence is verified separately. Apple MLX training is not Linux CUDA qualification. The exact target Linux model/runtime still needs its own resource, learning and inference qualification. This phase does not establish representative client accuracy, a guaranteed low review percentage, multilingual generalisation or customer voting-risk tolerances.

Highest-value next qualification: use representative client MT564/MT568 events with independently expert-reviewed factorised labels; reserve whole events/amendment chains/families for calibration and final test, then run the same frozen-parent learning and confidence protocol.
