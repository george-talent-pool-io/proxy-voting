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

NOT YET VERIFIED IN THIS RUN.

## Persisted calibrated browser and restart

NOT YET VERIFIED IN THIS RUN.

## Real two-model release integration

NOT YET VERIFIED IN THIS RUN.

## Delivery boundary and remaining qualification

The source archive and Docker image contain no new AI corpus, test-trained weights, optimizer state, customer database, private answer keys or test calibrator. Provision pinned foundation weights separately and create a fresh customer workspace. A frozen foundation identity is not a domain-accuracy certificate.

Linux ARM64 service startup/authentication/read-only execution/restart persistence is verified separately. Apple MLX training is not Linux CUDA qualification. The exact target Linux model/runtime still needs its own resource, learning and inference qualification. This phase does not establish representative client accuracy, a guaranteed low review percentage, multilingual generalisation or customer voting-risk tolerances.

Highest-value next qualification: use representative client MT564/MT568 events with independently expert-reviewed factorised labels; reserve whole events/amendment chains/families for calibration and final test, then run the same frozen-parent learning and confidence protocol.
