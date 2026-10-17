# ISO 15022 learning and release framework qualification

This report qualifies engineering with controlled **AI_AUTHORED** labels. It does not establish customer accuracy. Automation remains disabled.

Dataset v2 stores TRAIN, VALIDATION, CALIBRATION and FROZEN_TEST answers in separate private files. An additional regression test proved that the older mixed-role file allowed cross-role labels to be loaded by a scorer. The scorer now rejects mixed-role legacy archives before reading labels. Explicit curation migrated a new version; training still consumes only TRAIN/VALIDATION, and no earlier dataset or prediction was overwritten.

The earlier campaign was interrupted after training to correct inconsistent JSON-fence handling in the repair path. A regression test failed before the correction and passed afterwards. This campaign explicitly reuses the completed checkpoints; it does not retrain them or resume optimizer state. Original predictions remain under the earlier identity.

**Baseline naming:** internal candidate IDs BASE_LAYA and BASE_QWEN mean the unchanged registered engineering checkpoints (one Laya epoch and one Qwen optimizer step from the preceding milestone). They do not mean untouched foundation-model weights. New runs start from the same original bases, using three epochs/two steps respectively; they do not resume the earlier optimizer.

## Dataset and actual learning updates

The fixed cohort contains 8 TRAIN, 4 VALIDATION, 4 CALIBRATION and 4 FROZEN_TEST events. The unchanged 57-case challenge was neither trained on nor used for selection. These tiny, constructionally labelled samples are not a domain-generalisation trial. The engineering frozen fixture was already scored in the preceding milestone; reusing it tests protection/persistence mechanics, not a new genuinely blind quality result.

| Stage | Job | Actual updates | Reload check |
|---|---|---|---|
| baseline_laya (registered / reused) | `d487b4d6-4177-4072-9d48-24f6a8a32913` | 1 epochs | `{'passed': True, 'max_absolute_score_difference': 0.0, 'absolute_tolerance': 1e-05, 'probe': 'First validation input, two fresh loads'}` |
| laya_3epoch (registered / reused) | `a34a1f9f-94da-4839-84bb-0374de69c855` | 3 epochs | `{'passed': True, 'max_absolute_score_difference': 0.0, 'absolute_tolerance': 1e-05, 'probe': 'First validation input, two fresh loads'}` |
| baseline_qwen (registered / reused) | `dde8a411-86b7-480b-b034-dcf22e1db0e0` | 1 optimiser steps (not all eligible records necessarily consumed) | `{'passed': True, 'max_absolute_logit_difference': 0.0, 'absolute_relative_tolerance': 0.005, 'probe_tokens': 128}` |
| qwen_2step (registered / reused) | `48471af2-1c7e-4ab5-ab51-df5b5109e369` | 2 optimiser steps (not all eligible records necessarily consumed) | `{'passed': True, 'max_absolute_logit_difference': 0.0, 'absolute_relative_tolerance': 0.005, 'probe_tokens': 128}` |

New Laya runs use the official SDK; Qwen uses local quantised MLX LoRA. Training configurations, loss diagnostics, original weights, adapters and source snapshots remain in their registered job directories. A weight update or falling training loss alone is not evidence of better unseen semantics.

## Measured learning diagnostics

Laya native whole-notice SDK diagnostic: 19/36 before → 22/36 after three epochs. Epoch losses: [1.2444707108661532, 1.1428806794703834, 1.102055150601599]. This diagnostic differs from passage/reconciliation results below.

Qwen: 2 optimiser steps / 2 microbatches, 94,208 trainable LoRA parameters; weights_changed=True. Held-out JSON token loss: 0.141013 → 0.140507. Training took 792.4s; peak MLX allocated memory 28.53 GB (not total OS/unified-memory peak). Token loss is not predicate accuracy.

## Same-input validation comparisons

| Candidate | Correct semantic assertions | All-nine exact match | Critical false negatives | LLM calls | Median / p95 ms |
|---|---|---|---|---|---|
| BASE_LAYA | 18/36 | 0/4 | 0 | 0/4 | 772 / 6569 |
| TRAINED_LAYA | 19/36 | 0/4 | 0 | 0/4 | 773 / 3063 |
| BASE_QWEN | 36/36 | 4/4 | 0 | 4/4 | 59033 / 111728 |
| TRAINED_QWEN | 36/36 | 4/4 | 0 | 4/4 | 63037 / 171056 |
| CASCADE_CONSERVATIVE | 23/36 | 0/4 | 0 | 4/4 | 78929 / 165161 |
| CASCADE_MODERATE | 23/36 | 0/4 | 0 | 4/4 | 72037 / 165814 |

Latency is measured request time; the first request includes lazy stage loading, explicitly recorded in each prediction. These are bounded cohort measurements, not steady-state throughput qualification.

Repair/damage counters compare initial Laya with the reconciled result and can include authoritative structured-fact effects. They are not causal LLM-only repairs. Raw model stages and reconciliation traces retain attribution; deadline/final-status denominators are separate.

Validation selected **BASE_QWEN**. New critical false negatives relative to the first baseline are an explicit selection gate. No frozen result selected the model or routing thresholds.

## Frozen release and protected scoring

All model/prompt/schema/aggregation/parser/event/rule/routing/dependency and calibration identities are pinned. `OPERATING_FREEZE.json` precedes frozen-test scoring. All test predictions and their checksums precede answer-key access.

```json
{
  "cases": 4,
  "cases_satisfying_all_supplied_assertions": 4,
  "assertions": 36,
  "correct_assertions": 36,
  "assertion_accuracy": 1.0,
  "case_exact_match_scope": "All supplied assertions only; not all fields unless dataset is completely labelled",
  "fields": {
    "votability": {
      "n": 4,
      "correct": 4,
      "accuracy": 1.0,
      "macro_f1": 1.0,
      "f1_by_class": {
        "VOTABLE": 1.0,
        "NOT_VOTABLE": 1.0
      },
      "balanced_accuracy": 1.0,
      "positive_label": "VOTABLE",
      "positive_support": 3,
      "negative_support": 1,
      "positive_precision": 1.0,
      "positive_recall": 1.0,
      "negative_recall_specificity": 1.0,
      "positive_f1": 1.0,
      "support": {
        "VOTABLE": 3,
        "NOT_VOTABLE": 1
      },
      "predicted_support": {
        "VOTABLE": 3,
        "NOT_VOTABLE": 1
      },
      "labels": [
        "NOT_VOTABLE",
        "VOTABLE"
      ],
      "confusion_matrix": [
        [
          1,
          0
        ],
        [
          0,
          3
        ]
      ],
      "not_supported": 0
    },
    "share_blocking": {
      "n": 4,
      "correct": 4,
      "accuracy": 1.0,
      "macro_f1": 1.0,
      "f1_by_class": {
        "YES": 1.0,
        "NO": 1.0
      },
      "balanced_accuracy": 1.0,
      "positive_label": "YES",
      "positive_support": 2,
      "negative_support": 2,
      "positive_precision": 1.0,
      "positive_recall": 1.0,
      "negative_recall_specificity": 1.0,
      "positive_f1": 1.0,
      "support": {
        "YES": 2,
        "NO": 2
      },
      "predicted_support": {
        "YES": 2,
        "NO": 2
      },
      "labels": [
        "NO",
        "YES"
      ],
      "confusion_matrix": [
        [
          2,
          0
        ],
        [
          0,
          2
        ]
      ],
      "not_supported": 0
    },
    "poa_required": {
      "n": 4,
      "correct": 4,
      "accuracy": 1.0,
      "macro_f1": 1.0,
      "f1_by_class": {
        "NO": 1.0
      },
      "balanced_accuracy": 1.0,
      "positive_label": "YES",
      "positive_support": 0,
      "negative_support": 4,
      "positive_precision": null,
      "positive_recall": null,
      "negative_recall_specificity": 1.0,
      "positive_f1": null,
      "support": {
        "NO": 4
      },
      "predicted_support": {
        "NO": 4
      },
      "labels": [
        "NO"
      ],
      "confusion_matrix": [
        [
          4
        ]
      ],
      "not_supported": 0
    },
    "registration_required": {
      "n": 4,
      "correct": 4,
      "accuracy": 1.0,
      "macro_f1": 1.0,
      "f1_by_class": {
        "NO": 1.0
      },
      "balanced_accuracy": 1.0,
      "positive_label": "YES",
      "positive_support": 0,
      "negative_support": 4,
      "positive_precision": null,
      "positive_recall": null,
      "negative_recall_specificity": 1.0,
      "positive_f1": null,
      "support": {
        "NO": 4
      },
      "predicted_support": {
        "NO": 4
      },
      "labels": [
        "NO"
      ],
      "confusion_matrix": [
        [
          4
        ]
      ],
      "not_supported": 0
    },
    "beneficial_owner_disclosure_required": {
      "n": 4,
      "correct": 4,
      "accuracy": 1.0,
      "macro_f1": 1.0,
      "f1_by_class": {
        "NO": 1.0
      },
      "balanced_accuracy": 1.0,
      "positive_label": "YES",
      "positive_support": 0,
      "negative_support": 4,
      "positive_precision": null,
      "positive_recall": null,
      "negative_recall_specificity": 1.0,
      "positive_f1": null,
      "support": {
        "NO": 4
      },
      "predicted_support": {
        "NO": 4
      },
      "labels": [
        "NO"
      ],
      "confusion_matrix": [
        [
          4
        ]
      ],
      "not_supported": 0
    },
    "holding_confirmation_required": {
      "n": 4,
      "correct": 4,
      "accuracy": 1.0,
      "macro_f1": 1.0,
      "f1_by_class": {
        "YES": 1.0,
        "NO": 1.0
      },
      "balanced_accuracy": 1.0,
      "positive_label": "YES",
      "positive_support": 2,
      "negative_support": 2,
      "positive_precision": 1.0,
      "positive_recall": 1.0,
      "negative_recall_specificity": 1.0,
      "positive_f1": 1.0,
      "support": {
        "YES": 2,
        "NO": 2
      },
      "predicted_support": {
        "YES": 2,
        "NO": 2
      },
      "labels": [
        "NO",
        "YES"
      ],
      "confusion_matrix": [
        [
          2,
          0
        ],
        [
          0,
          2
        ]
      ],
      "not_supported": 0
    },
    "split_voting_restricted": {
      "n": 4,
      "correct": 4,
      "accuracy": 1.0,
      "macro_f1": 1.0,
      "f1_by_class": {
        "NO": 1.0
      },
      "balanced_accuracy": 1.0,
      "positive_label": "YES",
      "positive_support": 0,
      "negative_support": 4,
      "positive_precision": null,
      "positive_recall": null,
      "negative_recall_specificity": 1.0,
      "positive_f1": null,
      "support": {
        "NO": 4
      },
      "predicted_support": {
        "NO": 4
      },
      "labels": [
        "NO"
      ],
      "confusion_matrix": [
        [
          4
        ]
      ],
      "not_supported": 0
    },
    "securities_lending_recall_required": {
      "n": 4,
      "correct": 4,
      "accuracy": 1.0,
      "macro_f1": 1.0,
      "f1_by_class": {
        "NO": 1.0
      },
      "balanced_accuracy": 1.0,
      "positive_label": "YES",
      "positive_support": 0,
      "negative_support": 4,
      "positive_precision": null,
      "positive_recall": null,
      "negative_recall_specificity": 1.0,
      "positive_f1": null,
      "support": {
        "NO": 4
      },
      "predicted_support": {
        "NO": 4
      },
      "labels": [
        "NO"
      ],
      "confusion_matrix": [
        [
          4
        ]
      ],
      "not_supported": 0
    },
    "other_voting_restriction": {
      "n": 4,
      "correct": 4,
      "accuracy": 1.0,
      "macro_f1": 1.0,
      "f1_by_class": {
        "NO": 1.0
      },
      "balanced_accuracy": 1.0,
      "positive_label": "YES",
      "positive_support": 0,
      "negative_support": 4,
      "positive_precision": null,
      "positive_recall": null,
      "negative_recall_specificity": 1.0,
      "positive_f1": null,
      "support": {
        "NO": 4
      },
      "predicted_support": {
        "NO": 4
      },
      "labels": [
        "NO"
      ],
      "confusion_matrix": [
        [
          4
        ]
      ],
      "not_supported": 0
    }
  },
  "final_status_labelled_cases": 0,
  "customer_status_accuracy": null,
  "manual_review_count": 4,
  "uncertain_final_status_count": 0,
  "llm_invocations": 4,
  "llm_invalid_outputs": 0,
  "high_confidence_wrong_assertions": 0,
  "median_latency_ms": 49737.65658296179,
  "p95_latency_ms": 54418.22079196572,
  "failures": [],
  "scope": "Synthetic/authored research only. No customer accuracy or automation claim.",
  "expected_final_status": {
    "support": 4,
    "correct": 4
  },
  "expected_deadline_status": {
    "support": 4,
    "correct": 4
  }
}
```

## Calibration and confidence

```json
{
  "release_identity": "aa711b11b8fc498116e246c9008dda4a65aa36968f38ca9400f99a5ddbaa5319",
  "evaluation_sha256": "c04a00735cf85326f9987f470ddbbd9ab32783d2d2bb5a63a22de6c42053bbf6",
  "prediction_sha256": "76d199aede42a1cd2404df7e784516916027dd60684fc3d7a556a33b6ffc360b",
  "reports": {
    "beneficial_owner_disclosure_required": {
      "status": "INSUFFICIENT_CALIBRATION_SUPPORT",
      "fit_n": 2,
      "evaluation_n": 2,
      "fit_correctness_counts": {
        "False": 0,
        "True": 2
      }
    },
    "holding_confirmation_required": {
      "status": "INSUFFICIENT_CALIBRATION_SUPPORT",
      "fit_n": 2,
      "evaluation_n": 2,
      "fit_correctness_counts": {
        "False": 0,
        "True": 2
      }
    },
    "other_voting_restriction": {
      "status": "INSUFFICIENT_CALIBRATION_SUPPORT",
      "fit_n": 2,
      "evaluation_n": 2,
      "fit_correctness_counts": {
        "False": 0,
        "True": 2
      }
    },
    "poa_required": {
      "status": "INSUFFICIENT_CALIBRATION_SUPPORT",
      "fit_n": 2,
      "evaluation_n": 2,
      "fit_correctness_counts": {
        "False": 0,
        "True": 2
      }
    },
    "registration_required": {
      "status": "INSUFFICIENT_CALIBRATION_SUPPORT",
      "fit_n": 2,
      "evaluation_n": 2,
      "fit_correctness_counts": {
        "False": 0,
        "True": 2
      }
    },
    "securities_lending_recall_required": {
      "status": "INSUFFICIENT_CALIBRATION_SUPPORT",
      "fit_n": 2,
      "evaluation_n": 2,
      "fit_correctness_counts": {
        "False": 0,
        "True": 2
      }
    },
    "share_blocking": {
      "status": "INSUFFICIENT_CALIBRATION_SUPPORT",
      "fit_n": 2,
      "evaluation_n": 2,
      "fit_correctness_counts": {
        "False": 0,
        "True": 2
      }
    },
    "split_voting_restricted": {
      "status": "INSUFFICIENT_CALIBRATION_SUPPORT",
      "fit_n": 2,
      "evaluation_n": 2,
      "fit_correctness_counts": {
        "False": 0,
        "True": 2
      }
    },
    "votability": {
      "status": "INSUFFICIENT_CALIBRATION_SUPPORT",
      "fit_n": 2,
      "evaluation_n": 2,
      "fit_correctness_counts": {
        "False": 0,
        "True": 2
      }
    }
  },
  "valid_predicates": [],
  "support_policy": "100 fit / 50 evaluation per predicate; family-isolated; correctness-class support gates retained",
  "scope": "AI-authored synthetic population only; not customer confidence",
  "automation_enabled": false
}
```

The real four-event calibration sample is insufficient. Numerical confidence must remain null. Independent controlled statistical fixtures verify fitting, held-out Brier/ECE checks, persistence, identity rejection and inference; those fixtures are software evidence, not model calibration evidence. Coverage simulations are saved in the campaign calibration directory; no unsupported probability is displayed.

## Application, audit, and operations

The selected release runs through the event API. Model Lab displays persisted Laya passages, Qwen output, routing, reconciliation, exact source links and calibration status. Complete-release rollback preserves the entire seal hash. Separate handoff receipts verify real application execution and API-restart persistence. The detached campaign survived an API restart. Access control and backup/cold-restore/corruption rejection have independent integration tests.

## Boundaries and next useful work

The qualified scope is a local single-operator learning framework. The trainable MLX adapter currently supports Laya → full Qwen Direct → review; the older constrained three-gear study remains separate. No constrained logits, calibrated customer probability, shared-service RBAC, distributed scheduling or true optimizer-state resume is claimed. The 7,683 public excerpts remain unlabelled and contain no recognised ISO structure. Representative real custodian chains are still needed for profile-specific acceptance.

Next, run a larger predefined learning campaign with independent generation families and enough calibration error/support to test useful confidence. AI labels are sufficient to develop this framework; independently expert-labelled real notices are required before customer-quality or automated-operation claims.

Campaign receipt SHA-256: `998f1a7131a8c88811c127af5f4dafa58bec2e29115805e2e921242d18bbb08e`

## Final verification receipts

* 2,197 ordinary application tests passed; one opt-in CPU smoke skipped, 160 model/browser checks deselected in that run.
* 27 browser tests passed with explicit software doubles; a separate live-browser check inspected actual saved model traces with zero browser errors.
* Two real registered Laya/Qwen integration tests passed in 80.76s.
* Real API execution of Laya-only, Qwen-only and cascade releases; complete-release rollback and API-restart persistence passed.
* Checksummed real workspace/SQLite backup completed; corruption rejection and cold restore passed on isolated integration fixtures.
* Timestamp-normalised source delivery was reproduced byte-for-byte and started from a clean locked environment.
* No framework job or timed benchmark remains running. The earlier Laya-first study remains safely stopped with completed rows preserved.

Machine receipt: `artifacts/release-framework-completion.json`. Operations: `docs/LOCAL_LEARNING_OPERATIONS.md`. Source delivery: `artifacts/releases/iso15022-learning-framework-20261017-r3.tar.gz`.
