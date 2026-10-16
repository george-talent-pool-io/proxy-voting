# Laya + local LLM architecture evaluation

**Research outcome: C improves agreement on the authored challenge, but has no LLM-call savings. D is competitive on the complete synthetic benchmark and better on its positive restrictions, despite weak votability on the challenge. E is faster on many notices but accepts numerous wrong specialist cases. No architecture is qualified for unattended customer decisions.**

Automation remains disabled. Production/customer accuracy is UNKNOWN / NOT YET ESTABLISHED. This is not a production-readiness claim.

## 1. Exact local model and selection

`zai-org/GLM-4.7-Flash`, local tag `glm-4.7-flash:latest`, full digest `d1a8a26252f18b34301218d22abd2620a65b85ba4b78987842eb157e01321222`. 29,943,393,920 stored parameters, Q4_K_M GGUF, MIT. One existing model selected; no multiple-weight download. GLM had a working mature local runtime, commercial-PoC-compatible licence, multilingual capability and room for a 16k context on this Mac. The three-candidate decision and limitations are in [LOCAL_LLM_SELECTION.md](LOCAL_LLM_SELECTION.md). This experiment does not establish it as the best local LLM. Thinking was explicitly disabled.

## 2–4. Runtime, hardware and locality

Ollama 0.34.3, literal loopback HTTP, Apple M3 Max (16 CPU cores), 64 GiB unified memory, Metal local weights. Actual local model manifest and three blob hashes were checked. No notice was sent to a cloud inference API. The adapter rejects remote endpoints, DNS aliases, proxies and redirects and checks the installed digest/runtime before requests. Laya uses installed official 0.4.8 SDK/checkpoints on MPS with network downloads disabled.

## 5. Exact prompt, schema and generation

Prompt text: `semantic_pipeline/prompt.txt`; typed schema: `semantic_pipeline/schema.py`; immutable prompt+schema SHA256/version `264e2fc98de4a1f9a1dfe98daed9f42bc0da0e4822fac3b43f79ab97e104b4e4`. Runtime request format is the generated JSON schema, with strict Pydantic validation afterwards. Configured context 16,384, max generation 2,048, temperature 0, seed 42, think=false. Raw messages, output, token counts and timings are persisted per inference. No model confidence is requested or treated as calibrated. Native Laya choice probabilities and margins are uncalibrated decision scores.

Independent D receives source and empty structured context, with no Laya prediction, score or evidence. C/E fallback receives the same source plus bounded specialist diagnostics and deterministic facts where parsed. Exact threshold reasons are persisted outside the prompt; stable generic escalation context makes validation counterfactual routing comparisons meaningful.

The schema covers votability plus eight YES/NO/UNKNOWN restrictions: blocking, POA, registration, beneficial-owner disclosure, holding confirmation, split-voting restriction, lending recall and residual other restriction. It also returns source-exact deadline text, evidence per predicate and ambiguities. Temporal comparison is deterministic.

## 6. Reproducibility

- raw_text_stable: 17/20 cases stable across three identical generations (60 actual local generations total).
- parsed_result_stable: 17/20 cases stable across three identical generations (60 actual local generations total).
- semantic_labels_stable: 20/20 cases stable across three identical generations (60 actual local generations total).
- final_decision_stable: 20/20 cases stable across three identical generations (60 actual local generations total).

The probes use deterministic length-diverse validation selection and are not prompt/routing tuning. Parsed-result variability includes evidence/ambiguity wording even when labels stay stable. Earlier explicit reload probes reproduced native Laya scores/evidence and LLM parsed results for 3/3 validation notices. Fixed seed/temperature on a device runtime is not proof of universal bitwise determinism. Full outputs: `REPEATABILITY-60-CALLS.jsonl`, reload checks and resource summary.

## 7–8. Data, blindness and denominators

| Dataset | Notices | Labelled assertions | Final-status labels | Status |
|---|---:|---:|---:|---|
| Authored semantic challenge | 57 | 95 | 4 | Frozen original partial assertions; repeatedly observed historical challenge, never trained on |
| Old synthetic development test | 100 | 600 | 100 | NOT BLIND / DEVELOPMENT ONLY; key previously exposed and train/test duplicates present |
| SYNTHETIC_COMPLETE_BENCHMARK | 48 | 528 | 48 | New separate authored truth; 9 semantic fields + deadline + final derived status for every case |

The 48 examples include eight standards-derived partial ISO fixtures, not real SWIFT production messages. They are separate from training/tuning; exact-hash and lexical near-duplicate checks found zero overlap with prior training/validation/test/challenge, but cannot prove semantic independence from all prior task knowledge. Challenge text/expected assertions are unchanged. No new fine-tuning or expert labels were created. The earlier requested 3,000-example training phase was superseded by this architecture experiment and was not silently performed.

Routing selection used only 40 unique supplied validation notices with 200 labelled assertions. Eleven validation texts exactly repeat historical training: this limits their reliability. The six expanded semantic attributes lack validation truth. Old synthetic source has only 328 unique texts across 500 rows. See `DATASET-QA.json`; the 7,683 public excerpts remain unlabelled, not verified accuracy observations.

1,025 timed persisted A–E predictions = 205 identical applicable notices × five arms. 497 actual timed local LLM invocations; no model-row failures. Blind-shaped old test predictions were committed before scoring reopened its already-exposed answer key. A commit cannot restore blindness.

### Disclosed evaluator correction

The frozen v1 scorer accidentally used C’s preserved legacy broad auxiliary head rather than the reconciled named restriction union for an old broad assertion. SCORER-v2 changes this projection only, moving C challenge case agreement from 45/57 to 47/57. Raw predictions, model, prompt, thresholds, preprocessing, decision rules and expected answers were unchanged. V1 code/report/summary remain preserved, every projection is listed, and a validation-only check confirms original gate selection is unchanged. `CORRECTED-SUMMARY.json` is the reported analysis; `SUMMARY.json` and `FROZEN-SCORER-V1.md` are the original.

## 9. Controlled A–E results

A: base whole-text Laya. B: existing fine-tuned whole-text Laya. C: B + local fallback/reconciliation/date rules. D: independent local LLM + date/decision rules. E: optional parser + narrow fine-tuned Laya + escalation/local fallback + reconciliation/rules. A/B preserve legacy status precedence; common-policy sensitivity is separately provided. A/B cannot emit six individual expanded attributes: NOT_SUPPORTED counts as wrong on complete truth.

### challenge

| Arm | Correct assertions | Cases satisfying supplied assertions | Mean field balanced accuracy | Blocking YES recall | POA YES recall | LLM calls | Review policy | Median / p95 ms | Sequential notices/s |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| A | 59/95 | 30/57 | 57.8% | 100.0% (n=3) | 66.7% (n=3) | 0/57 | 100% | 42 / 49 | 22.32 |
| B | 73/95 | 37/57 | 57.2% | 66.7% (n=3) | 66.7% (n=3) | 0/57 | 100% | 42 / 52 | 21.40 |
| C | 85/95 | 47/57 | 83.5% | 66.7% (n=3) | 66.7% (n=3) | 57/57 | 100% | 6092 / 7620 | 0.16 |
| D | 58/95 | 22/57 | 82.3% | 100.0% (n=3) | 100.0% (n=3) | 57/57 | 100% | 4779 / 5870 | 0.21 |
| E | 71/95 | 36/57 | 65.1% | 100.0% (n=3) | 66.7% (n=3) | 15/57 | 100% | 153 / 7684 | 0.51 |

Mean field balanced accuracy is the unweighted mean over the supplied fields (including status/deadline where labelled); it is not a universal cross-task score. Per-field balanced accuracy is the interpretable result. Case conjunctions on partial truth are not final-status accuracy. No unlabelled predicate counts as correct.

### synthetic-development

| Arm | Correct assertions | Cases satisfying supplied assertions | Mean field balanced accuracy | Blocking YES recall | POA YES recall | LLM calls | Review policy | Median / p95 ms | Sequential notices/s |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| A | 316/600 | 6/100 | 48.8% | 100.0% (n=11) | 90.9% (n=11) | 0/100 | 100% | 52 / 63 | 18.65 |
| B | 600/600 | 100/100 | 100.0% | 100.0% (n=11) | 100.0% (n=11) | 0/100 | 100% | 47 / 56 | 20.95 |
| C | 456/600 | 19/100 | 78.9% | 90.9% (n=11) | 100.0% (n=11) | 100/100 | 100% | 6417 / 7473 | 0.16 |
| D | 364/600 | 15/100 | 61.8% | 90.9% (n=11) | 90.9% (n=11) | 100/100 | 100% | 5006 / 5684 | 0.20 |
| E | 390/600 | 13/100 | 57.6% | 100.0% (n=11) | 100.0% (n=11) | 36/100 | 100% | 190 / 8281 | 0.36 |

Mean field balanced accuracy is the unweighted mean over the supplied fields (including status/deadline where labelled); it is not a universal cross-task score. Per-field balanced accuracy is the interpretable result. Case conjunctions on partial truth are not final-status accuracy. No unlabelled predicate counts as correct.

### complete

| Arm | Correct assertions | Cases satisfying supplied assertions | Mean field balanced accuracy | Blocking YES recall | POA YES recall | LLM calls | Review policy | Median / p95 ms | Sequential notices/s |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| A | 90/528 | 0/48 | 19.7% | 100.0% (n=3) | 66.7% (n=3) | 0/48 | 100% | 54 / 93 | 16.83 |
| B | 199/528 | 0/48 | 23.6% | 0.0% (n=3) | 66.7% (n=3) | 0/48 | 100% | 54 / 94 | 17.02 |
| C | 484/528 | 29/48 | 81.0% | 0.0% (n=3) | 66.7% (n=3) | 48/48 | 100% | 6835 / 8068 | 0.14 |
| D | 485/528 | 28/48 | 84.5% | 100.0% (n=3) | 100.0% (n=3) | 48/48 | 100% | 5530 / 6037 | 0.18 |
| E | 410/528 | 9/48 | 60.0% | 100.0% (n=3) | 100.0% (n=3) | 36/48 | 100% | 7202 / 8841 | 0.17 |

Mean field balanced accuracy is the unweighted mean over the supplied fields (including status/deadline where labelled); it is not a universal cross-task score. Per-field balanced accuracy is the interpretable result. Case conjunctions on partial truth are not final-status accuracy. No unlabelled predicate counts as correct.

| Arm | Exact match: 9 semantic fields + deadline | Final derived status agreement |
|---|---:|---:|
| A | 0/48 | 8/48 |
| B | 0/48 | 24/48 |
| C | 29/48 | 38/48 |
| D | 28/48 | 36/48 |
| E | 9/48 | 12/48 |

## 10–12. Positive restrictions and votability

All supports and positive precision/recall, specificity, F1, balanced accuracy and confusion matrices follow below. Positive support on the challenge is only three for blocking and three for POA; 100% there is not a reliable production-risk estimate. On the complete benchmark B and C miss all three blocking positives, while D and E detect 3/3. C reconciliation can turn a true affirmative LLM answer into UNKNOWN when a concrete contrary Laya answer lacks a validated precedence rule. This is visible abstention and still a failed labelled assertion.

Independent D has strong restriction detection but severely over-abstains on votability: 40/57 challenge outputs are UNCERTAIN, with no NOT_VOTABLE outputs. Its full prompt was verified to reach the runtime by a real system-role canary. This is an observed limitation of this pinned model/prompt/thinking configuration, not proof against all local LLMs.

## 13–15. Invocation, repairs and damage

| Dataset | Arm | Calls | Semantic wrong→correct | Semantic correct→wrong | Correct→correct | Wrong→wrong |
|---|---|---:|---:|---:|---:|
| challenge | C | 57/57 | 5 | 2 | 63 | 7 |
| challenge | E | 15/57 | 4 | 0 | 6 | 10 |
| synthetic-development | C | 100/100 | 0 | 19 | 381 | 0 |
| synthetic-development | E | 36/100 | 27 | 0 | 93 | 24 |
| complete | C | 48/48 | 275 | 3 | 131 | 23 |
| complete | E | 36/48 | 33 | 0 | 220 | 71 |

These transition denominators contain only labelled semantic assertions on actually invoked cases; date/status changes are excluded. Raw LLM and reconciled transitions are both retained. E’s specialist before fallback already includes deterministic dates/rules, whereas C’s historical comparator is B.

### Date-only attribution

Keeping B’s recorded factors/status policy and changing only its temporal head to the frozen deterministic date rules moves challenge agreement 37→44/57; complete C is 47/57. Thus much of the headline B→C gain is date software, not generative repair. On the old leaky synthetic test the same ablation reduces 100→17/100: 75 OPEN labels lack a deterministically extracted dated deadline, and eight PASSED labels use an unsupported “required no later than” cue. Those failures are preserved, not patched after test inspection. See `DATE-RULE-ABLATION.json`.

## 16. ORACLE_ROUTING — analytical, not deployable

| Dataset | Arm | Labelled assertions | Specialist correct | Errors | LLM correct on errors / maximum repairs | LLM still wrong | Maximum combined correct |
|---|---|---:|---:|---:|---:|---:|---:|
| challenge | C | 95 | 73 | 22 | 15 | 7 | 88 |
| challenge | E | 95 | 67 | 28 | 7 | 21 | 74 |
| synthetic-development | C | 600 | 600 | 0 | 0 | 0 | 600 |
| synthetic-development | E | 600 | 356 | 244 | 58 | 186 | 414 |
| complete | C | 528 | 199 | 329 | 302 | 27 | 501 |
| complete | E | 528 | 370 | 158 | 50 | 108 | 420 |

This optimistic per-assertion bound can keep every correct specialist field and select a fallback field only when truth says it repairs an error. It uses evidence-validated fallback facts with deterministic dates/status derivation. Per-predicate bounds are in EXTENDED-ASSERTION-DIAGNOSTICS.json, with separate case-switching bounds in ORACLE-FALLBACK-ANALYSIS.json. Seventy-eight extra E fallback-context calls were generated only after the timed study for missing specialist-wrong cases; truth was never sent to the model. They are excluded from main call rates/latencies and cannot tune routing. The independent-D oracle is a separate mode, not a universal ceiling on fallback-context generation.

## 17–19. Scores, disagreement and validation routing

Native score/margin versus correctness AUC is reported per predicate, only where both correctness classes occur; unavailable/abstaining scores are excluded with explicit n. Small authored/development samples and saturated native scores do not establish calibrated error detection. Confident errors and accepted specialist failures remain. The original 32 score/margin settings per C/E were selected before evaluation; neither numerical cutoff improved the chosen validation trade-off, so min_score/min_margin are null. UNKNOWN/conflict/unsupported/size triggers remain active. No post-test threshold change occurred.

Disagreement bins are supplied per labelled field for independent D versus the specialist on every input, and separately for observed/oracle fallback-context pairs. The latter E sample is truth-selected and cannot estimate production error prevalence. “Both uncertain” is an additional diagnostic flag, not a disjoint partition. On challenge votability, B and independent D disagree in 37/54 labelled cases; B is correct in 31, D in three, neither in three. Choosing the larger model whenever models disagree would damage many correct specialist answers. Agreement itself is also not proof of truth.

Validation-only strategy diagnostics cover UNKNOWN, score grids, margin grids, UNKNOWN/low-margin/missing-evidence, critical-positive-or-uncertain and always-independent-LLM. Detailed quality, calls, false negatives, repairs/damage, review and recomposed component-time estimates are in VALIDATION-STRATEGY-COMPARISON-v2.json. These additional diagnostics were added after the main freeze, did not change its operating point, and never use challenge scores for selection. Critical predicates are votability, blocking and POA because they establish action or required restrictions/documents; no invented financial costs are applied.

- C: validation-only best `SCORE` threshold 0.5: 167/200 assertions, 0/40 model calls, 0 repairs / 0 damage.
- E: validation-only best `CRITICAL_POSITIVE_OR_UNKNOWN` threshold None: 142/200 assertions, 40/40 model calls, 28 repairs / 0 damage.

The zero-call C diagnostic scores only the five old labelled fields, leaving expanded predicates NOT_SUPPORTED. It cannot justify avoiding the LLM when the full schema is required. The E critical strategy invokes on all 40 validation cases; this is not a useful call-saving gate. Always-LLM uses exactly the independent D records. Strategy latencies are sums of recorded component times, explicitly not new timed end-to-end measurements.

## 20. Review policy

Manual-review requirement is 100% for all architectures because the quality gate is disabled. Separately, uncertain final-status counts are in CORRECTED-SUMMARY.json. UNKNOWN critical facts, invalid evidence, runtime/schema failure, unresolved model/structured conflicts and unlinked replacement/cancellation messages remain review outcomes. No forced definitive classification.

## 21–22. Latency, resources, schema and robustness

After explicit unload, the separate cold call took 8.178 seconds including 2.077 seconds runtime model load; the comparable warm study values are labelled separately. On the challenge, generation rates were approximately 48–49 generated tokens/s; C used 76,453 prompt / 13,856 generated tokens, D 40,926 / 12,658, and E 21,541 / 3,972. Main tables contain actual warmed sequential notice latency, not cached or cold-start comparisons. LATENCY-RESOURCES.json records all arms’ median/p95/throughput, prompt/generated tokens, generation tokens/s and runtime load time. Nonstreaming time-to-first-token is unavailable, not estimated. Cold generation after explicit unload is recorded in RELOAD-REPRODUCIBILITY.json; warm main timings exclude model construction.

Resource supplement on one validation notice per arm: peak Python process RSS 4.00 GB; local llama-server RSS 20.52 GB. Runtime model/context allocation was approximately 20.0 GB at 16k context. This is Apple unified memory, not discrete GPU VRAM. Processes share mapped pages; their RSS must not be summed as distinct physical memory. Sampling at 50ms may miss shorter peaks. These feasibility probes are separate from the timed benchmark.

All 497 timed LLM calls returned schema-valid JSON on the first pass; 67 raw evidence/deadline quote claims failed exact matching and were quarantined. Exact quotation only proves provenance, not correct interpretation. The optional bounded repair wrapper is a later application-only condition, disabled by default and never used to change A–E results. It permits one retry after a completed malformed response, preserves both raw attempts/version hashes, and routes final failure to review. Runtime/timeouts/truncation/context overflow are not retried. The repair prompt is separately stored/versioned.

Real-model integration tests include independent and fallback modes, parser→real Laya→real local LLM→decision, exact evidence, role delivery, eight prompt-injection forms and a real repair generation after an explicitly simulated malformed first response. Ordinary tests use doubles for controlled failures and persistence; real-model tests are marked local_llm. No claim of complete adversarial robustness follows from eight cases.

## 23–25. Does Laya justify the front end?

C handles 0% of complete-schema notices without the LLM and invokes on 100% in all three sets. Therefore this C configuration demonstrates no LLM-call saving; it is slower than D. On the challenge it preserves useful specialist votability and beats D, but the date-only ablation explains much of B→C gain. C repairs five and damages two labelled semantic assertions on the challenge. On the complete synthetic benchmark C and D are almost tied at assertion level (484/528 vs 485/528), while C has 29 vs D 28 all-factor exact matches and 38 vs 36 status agreements. These small, correlated authored differences cannot establish superiority. C misses blocking positives which D detects.

E avoids 42/57 LLM calls on the challenge but 13 of those accepted cases fail supplied assertions. It avoids 12/48 calls on the complete benchmark and nine accepted cases fail. Thus its fast-path savings currently sacrifice quality. D is a simpler candidate for expanded predicates; B is much faster and better on challenge votability. Neither eliminates the need for stronger real labels and validated abstention.

## 26. Parser contribution

Historical detector scan of all 7,683 public filing excerpts recognised zero usable ISO15022 messages. The parser contributes no extracted ISO facts on that corpus. It remains available and optional for future actual SWIFT data; the eight complete-benchmark ISO fixtures exercise controlled structure only. No new broad parser expansion was done.

## 27–29. Best-supported architecture, remaining errors and claim limits

There is no defensible universal winner. B remains the strongest inexpensive specialist-only challenge comparator. C gives the best challenge partial-assertion result but no cost saving and meaningful damage. D nearly matches complete-schema C with lower latency and better affirmative restrictions, but its independent votability is poor. E’s current aggregation/gate is not reliable enough for accepted cases. Keep the default conservative; all arms remain experimental, swappable and auditable.

Major errors: absence-of-mention versus explicit negation in chunk aggregation; whole-notice training versus sentence inference; untrained expanded Laya predicates; LLM over-abstention on votability; specialist/LLM conflicts resolved to UNKNOWN; insufficient evidence; English temporal cue coverage; source-label conventions and synthetic duplicate leakage. False negatives including abstention, explicit YES→NO and false positives are separated for every predicate in EXTENDED-ASSERTION-DIAGNOSTICS.json. Every missed assertion is in [ARCHITECTURE_COMPARISON_ERRORS.md](ARCHITECTURE_COMPARISON_ERRORS.md), with full source, A–E outputs, native scores, LLM output, evidence and reconciliation.

The original 0/11 blocking failure is explained in [BLOCKING_FALSE_NEGATIVE_ANALYSIS.md](BLOCKING_FALSE_NEGATIVE_ANALYSIS.md): all 11 fine-tuned positive passages and whole documents are recognised, then the sentence reducer suppresses them as conflicts. No frozen policy was changed after discovering this.

Not established: representative customer accuracy, safe automation thresholds, regulatory suitability, all-language coverage, robustness on complete custodian notices, external generalisation, or production readiness. No expert-labelled real production test set exists. Synthetic benchmark performance, authored challenge agreement and customer accuracy remain separate in the GUI.

## 30. Single highest-value next experiment

Create a small independent expert-labelled real-notice benchmark rich in positive restrictions, explicit waivers and supersession, split by event/near-duplicate group. Predeclare a scope-aware aggregation candidate that distinguishes absence from negation and compare unchanged B/D plus revised E on that new held-out material. This directly tests the discovered implementation defect and whether specialist-first routing can save calls without hiding missed restrictions. Do not retune on these 57 cases.

## Application, verification and reproducibility

Set CLASSIFICATION_ARCHITECTURE to LEGACY_LAYA (default), FT_LAYA, LAYA_LLM, LLM_ONLY or FULL_HYBRID. LLM_ENABLED=false remains the default. Notice Detail’s explicit configured-analysis action uses the selected real pipeline, saves a new append-only execution associated with the notice, and shows its persisted expandable Decision Trace. Historical batch results/review labels are preserved. Model Lab is internal and compares all five saved study runs on identical cases, with evidence, disagreements, LLM usage and semantic repairs/damage. Normal baseline batch execution remains its historical benchmark; the configured architecture currently applies to the explicit per-notice analysis action, not silently to that old batch endpoint.

Per-arm/dataset manifests are in `manifests/`; their posthoc creation is explicit, while the original model/prompt/threshold FREEZE preceded every evaluation row. Source/runtime/weight hashes and raw results support reproduction. Supplemental oracle/repeatability/resource/live-UI/test calls are excluded from the 497 timed calls. The complete source archive is regenerated at completion; weights are referenced by hashes, not duplicated.

Software/browser/real-model result counts and persistence restart checks are recorded in FINAL-VERIFICATION.json. Existing authored model-quality tests still have 27 base and 20 fine-tuned failures under their unchanged original expectations; these are reported quality failures, not deleted or weakened tests. All previous passing software/parser/property tests and browser tests are retained.

## Per-predicate results and confusion matrices

Rows are truth, columns prediction, with explicit labels/support. Macro F1 uses truth-supported classes. NOT_SUPPORTED remains an error. Positive = VOTABLE for votability and YES for restriction fields. Positive metrics for date/status are not meaningful and are omitted.

### challenge / A

| Field | Correct/n | Positive / negative support | Precision+ | Recall+ | Specificity | F1+ | Macro F1 | Balanced accuracy |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| classification | 2/4 | N/A / N/A | N/A | N/A | N/A | N/A | 0.417 | 50.0% |
| votability | 34/54 | 36 / 15 | 85.2% | 63.9% | 66.7% | 73.0% | 0.535 | 54.6% |
| share_blocking | 8/11 | 3 / 8 | 50.0% | 100.0% | 62.5% | 66.7% | 0.718 | 81.2% |
| poa_required | 7/8 | 3 / 5 | 100.0% | 66.7% | 100.0% | 80.0% | 0.900 | 83.3% |
| deadline_status | 7/14 | N/A / N/A | N/A | N/A | N/A | N/A | 0.497 | 52.8% |
| other_restriction | 1/4 | 4 / 0 | 100.0% | 25.0% | N/A | 40.0% | 0.400 | 25.0% |

```json
{
  "classification": {
    "labels": [
      "NOT_VOTABLE",
      "UNCERTAIN_MANUAL_REVIEW",
      "VOTABLE",
      "VOTABLE_WITH_RESTRICTION"
    ],
    "support": {
      "VOTABLE": 1,
      "NOT_VOTABLE": 1,
      "UNCERTAIN_MANUAL_REVIEW": 1,
      "VOTABLE_WITH_RESTRICTION": 1
    },
    "confusion_matrix": [
      [
        1,
        0,
        0,
        0
      ],
      [
        0,
        1,
        0,
        0
      ],
      [
        0,
        0,
        0,
        1
      ],
      [
        0,
        1,
        0,
        0
      ]
    ]
  },
  "votability": {
    "labels": [
      "NOT_VOTABLE",
      "UNCERTAIN",
      "VOTABLE"
    ],
    "support": {
      "VOTABLE": 36,
      "NOT_VOTABLE": 15,
      "UNCERTAIN": 3
    },
    "confusion_matrix": [
      [
        10,
        3,
        2
      ],
      [
        0,
        1,
        2
      ],
      [
        1,
        12,
        23
      ]
    ]
  },
  "share_blocking": {
    "labels": [
      "NO",
      "YES"
    ],
    "support": {
      "NO": 8,
      "YES": 3
    },
    "confusion_matrix": [
      [
        5,
        3
      ],
      [
        0,
        3
      ]
    ]
  },
  "poa_required": {
    "labels": [
      "NO",
      "UNKNOWN",
      "YES"
    ],
    "support": {
      "NO": 5,
      "YES": 3
    },
    "confusion_matrix": [
      [
        5,
        0,
        0
      ],
      [
        0,
        0,
        0
      ],
      [
        0,
        1,
        2
      ]
    ]
  },
  "deadline_status": {
    "labels": [
      "OPEN",
      "PASSED",
      "UNKNOWN"
    ],
    "support": {
      "OPEN": 4,
      "PASSED": 4,
      "UNKNOWN": 6
    },
    "confusion_matrix": [
      [
        2,
        2,
        0
      ],
      [
        0,
        3,
        1
      ],
      [
        2,
        2,
        2
      ]
    ]
  },
  "other_restriction": {
    "labels": [
      "NO",
      "YES"
    ],
    "support": {
      "YES": 4
    },
    "confusion_matrix": [
      [
        0,
        0
      ],
      [
        3,
        1
      ]
    ]
  }
}
```

### challenge / B

| Field | Correct/n | Positive / negative support | Precision+ | Recall+ | Specificity | F1+ | Macro F1 | Balanced accuracy |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| classification | 3/4 | N/A / N/A | N/A | N/A | N/A | N/A | 0.667 | 75.0% |
| votability | 48/54 | 36 / 15 | 85.7% | 100.0% | 80.0% | 92.3% | 0.604 | 60.0% |
| share_blocking | 10/11 | 3 / 8 | 100.0% | 66.7% | 100.0% | 80.0% | 0.871 | 83.3% |
| poa_required | 7/8 | 3 / 5 | 100.0% | 66.7% | 100.0% | 80.0% | 0.855 | 83.3% |
| deadline_status | 5/14 | N/A / N/A | N/A | N/A | N/A | N/A | 0.290 | 41.7% |
| other_restriction | 0/4 | 4 / 0 | N/A | 0.0% | N/A | 0.0% | 0.000 | 0.0% |

```json
{
  "classification": {
    "labels": [
      "NOT_VOTABLE",
      "UNCERTAIN_MANUAL_REVIEW",
      "VOTABLE",
      "VOTABLE_WITH_RESTRICTION"
    ],
    "support": {
      "VOTABLE": 1,
      "NOT_VOTABLE": 1,
      "UNCERTAIN_MANUAL_REVIEW": 1,
      "VOTABLE_WITH_RESTRICTION": 1
    },
    "confusion_matrix": [
      [
        1,
        0,
        0,
        0
      ],
      [
        0,
        0,
        1,
        0
      ],
      [
        0,
        0,
        1,
        0
      ],
      [
        0,
        0,
        0,
        1
      ]
    ]
  },
  "votability": {
    "labels": [
      "NOT_VOTABLE",
      "UNCERTAIN",
      "VOTABLE"
    ],
    "support": {
      "VOTABLE": 36,
      "NOT_VOTABLE": 15,
      "UNCERTAIN": 3
    },
    "confusion_matrix": [
      [
        12,
        0,
        3
      ],
      [
        0,
        0,
        3
      ],
      [
        0,
        0,
        36
      ]
    ]
  },
  "share_blocking": {
    "labels": [
      "NO",
      "YES"
    ],
    "support": {
      "NO": 8,
      "YES": 3
    },
    "confusion_matrix": [
      [
        8,
        0
      ],
      [
        1,
        2
      ]
    ]
  },
  "poa_required": {
    "labels": [
      "NO",
      "YES"
    ],
    "support": {
      "NO": 5,
      "YES": 3
    },
    "confusion_matrix": [
      [
        5,
        0
      ],
      [
        1,
        2
      ]
    ]
  },
  "deadline_status": {
    "labels": [
      "OPEN",
      "PASSED",
      "UNKNOWN"
    ],
    "support": {
      "OPEN": 4,
      "PASSED": 4,
      "UNKNOWN": 6
    },
    "confusion_matrix": [
      [
        4,
        0,
        0
      ],
      [
        3,
        1,
        0
      ],
      [
        6,
        0,
        0
      ]
    ]
  },
  "other_restriction": {
    "labels": [
      "NO",
      "YES"
    ],
    "support": {
      "YES": 4
    },
    "confusion_matrix": [
      [
        0,
        0
      ],
      [
        4,
        0
      ]
    ]
  }
}
```

### challenge / C

| Field | Correct/n | Positive / negative support | Precision+ | Recall+ | Specificity | F1+ | Macro F1 | Balanced accuracy |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| classification | 4/4 | N/A / N/A | N/A | N/A | N/A | N/A | 1.000 | 100.0% |
| votability | 49/54 | 36 / 15 | 100.0% | 97.2% | 73.3% | 98.6% | 0.793 | 90.2% |
| share_blocking | 10/11 | 3 / 8 | 100.0% | 66.7% | 100.0% | 80.0% | 0.900 | 83.3% |
| poa_required | 7/8 | 3 / 5 | 100.0% | 66.7% | 100.0% | 80.0% | 0.855 | 83.3% |
| deadline_status | 13/14 | N/A / N/A | N/A | N/A | N/A | N/A | 0.933 | 94.4% |
| other_restriction | 2/4 | 4 / 0 | 100.0% | 50.0% | N/A | 66.7% | 0.667 | 50.0% |

```json
{
  "classification": {
    "labels": [
      "NOT_VOTABLE",
      "UNCERTAIN_MANUAL_REVIEW",
      "VOTABLE",
      "VOTABLE_WITH_RESTRICTION"
    ],
    "support": {
      "VOTABLE": 1,
      "NOT_VOTABLE": 1,
      "UNCERTAIN_MANUAL_REVIEW": 1,
      "VOTABLE_WITH_RESTRICTION": 1
    },
    "confusion_matrix": [
      [
        1,
        0,
        0,
        0
      ],
      [
        0,
        1,
        0,
        0
      ],
      [
        0,
        0,
        1,
        0
      ],
      [
        0,
        0,
        0,
        1
      ]
    ]
  },
  "votability": {
    "labels": [
      "NOT_VOTABLE",
      "UNCERTAIN",
      "VOTABLE"
    ],
    "support": {
      "VOTABLE": 36,
      "NOT_VOTABLE": 15,
      "UNCERTAIN": 3
    },
    "confusion_matrix": [
      [
        11,
        4,
        0
      ],
      [
        0,
        3,
        0
      ],
      [
        0,
        1,
        35
      ]
    ]
  },
  "share_blocking": {
    "labels": [
      "NO",
      "UNKNOWN",
      "YES"
    ],
    "support": {
      "NO": 8,
      "YES": 3
    },
    "confusion_matrix": [
      [
        8,
        0,
        0
      ],
      [
        0,
        0,
        0
      ],
      [
        0,
        1,
        2
      ]
    ]
  },
  "poa_required": {
    "labels": [
      "NO",
      "YES"
    ],
    "support": {
      "NO": 5,
      "YES": 3
    },
    "confusion_matrix": [
      [
        5,
        0
      ],
      [
        1,
        2
      ]
    ]
  },
  "deadline_status": {
    "labels": [
      "OPEN",
      "PASSED",
      "UNKNOWN"
    ],
    "support": {
      "OPEN": 4,
      "PASSED": 4,
      "UNKNOWN": 6
    },
    "confusion_matrix": [
      [
        4,
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
        1,
        5
      ]
    ]
  },
  "other_restriction": {
    "labels": [
      "NO",
      "YES"
    ],
    "support": {
      "YES": 4
    },
    "confusion_matrix": [
      [
        0,
        0
      ],
      [
        2,
        2
      ]
    ]
  }
}
```

### challenge / D

| Field | Correct/n | Positive / negative support | Precision+ | Recall+ | Specificity | F1+ | Macro F1 | Balanced accuracy |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| classification | 3/4 | N/A / N/A | N/A | N/A | N/A | N/A | 0.667 | 75.0% |
| votability | 20/54 | 36 / 15 | 100.0% | 47.2% | 0.0% | 64.2% | 0.264 | 49.1% |
| share_blocking | 11/11 | 3 / 8 | 100.0% | 100.0% | 100.0% | 100.0% | 1.000 | 100.0% |
| poa_required | 8/8 | 3 / 5 | 100.0% | 100.0% | 100.0% | 100.0% | 1.000 | 100.0% |
| deadline_status | 13/14 | N/A / N/A | N/A | N/A | N/A | N/A | 0.933 | 94.4% |
| other_restriction | 3/4 | 4 / 0 | 100.0% | 75.0% | N/A | 85.7% | 0.857 | 75.0% |

```json
{
  "classification": {
    "labels": [
      "NOT_VOTABLE",
      "UNCERTAIN_MANUAL_REVIEW",
      "VOTABLE",
      "VOTABLE_WITH_RESTRICTION"
    ],
    "support": {
      "VOTABLE": 1,
      "NOT_VOTABLE": 1,
      "UNCERTAIN_MANUAL_REVIEW": 1,
      "VOTABLE_WITH_RESTRICTION": 1
    },
    "confusion_matrix": [
      [
        0,
        1,
        0,
        0
      ],
      [
        0,
        1,
        0,
        0
      ],
      [
        0,
        0,
        1,
        0
      ],
      [
        0,
        0,
        0,
        1
      ]
    ]
  },
  "votability": {
    "labels": [
      "NOT_VOTABLE",
      "UNCERTAIN",
      "VOTABLE"
    ],
    "support": {
      "VOTABLE": 36,
      "NOT_VOTABLE": 15,
      "UNCERTAIN": 3
    },
    "confusion_matrix": [
      [
        0,
        15,
        0
      ],
      [
        0,
        3,
        0
      ],
      [
        0,
        19,
        17
      ]
    ]
  },
  "share_blocking": {
    "labels": [
      "NO",
      "YES"
    ],
    "support": {
      "NO": 8,
      "YES": 3
    },
    "confusion_matrix": [
      [
        8,
        0
      ],
      [
        0,
        3
      ]
    ]
  },
  "poa_required": {
    "labels": [
      "NO",
      "YES"
    ],
    "support": {
      "NO": 5,
      "YES": 3
    },
    "confusion_matrix": [
      [
        5,
        0
      ],
      [
        0,
        3
      ]
    ]
  },
  "deadline_status": {
    "labels": [
      "OPEN",
      "PASSED",
      "UNKNOWN"
    ],
    "support": {
      "OPEN": 4,
      "PASSED": 4,
      "UNKNOWN": 6
    },
    "confusion_matrix": [
      [
        4,
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
        1,
        5
      ]
    ]
  },
  "other_restriction": {
    "labels": [
      "NO",
      "YES"
    ],
    "support": {
      "YES": 4
    },
    "confusion_matrix": [
      [
        0,
        0
      ],
      [
        1,
        3
      ]
    ]
  }
}
```

### challenge / E

| Field | Correct/n | Positive / negative support | Precision+ | Recall+ | Specificity | F1+ | Macro F1 | Balanced accuracy |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| classification | 3/4 | N/A / N/A | N/A | N/A | N/A | N/A | 0.667 | 75.0% |
| votability | 38/54 | 36 / 15 | 81.4% | 97.2% | 13.3% | 88.6% | 0.429 | 48.0% |
| share_blocking | 11/11 | 3 / 8 | 100.0% | 100.0% | 100.0% | 100.0% | 1.000 | 100.0% |
| poa_required | 6/8 | 3 / 5 | 100.0% | 66.7% | 80.0% | 80.0% | 0.800 | 73.3% |
| deadline_status | 13/14 | N/A / N/A | N/A | N/A | N/A | N/A | 0.933 | 94.4% |
| other_restriction | 0/4 | 4 / 0 | N/A | 0.0% | N/A | 0.0% | 0.000 | 0.0% |

```json
{
  "classification": {
    "labels": [
      "NOT_VOTABLE",
      "UNCERTAIN_MANUAL_REVIEW",
      "VOTABLE",
      "VOTABLE_WITH_RESTRICTION"
    ],
    "support": {
      "VOTABLE": 1,
      "NOT_VOTABLE": 1,
      "UNCERTAIN_MANUAL_REVIEW": 1,
      "VOTABLE_WITH_RESTRICTION": 1
    },
    "confusion_matrix": [
      [
        0,
        1,
        0,
        0
      ],
      [
        0,
        1,
        0,
        0
      ],
      [
        0,
        0,
        1,
        0
      ],
      [
        0,
        0,
        0,
        1
      ]
    ]
  },
  "votability": {
    "labels": [
      "NOT_VOTABLE",
      "UNCERTAIN",
      "VOTABLE"
    ],
    "support": {
      "VOTABLE": 36,
      "NOT_VOTABLE": 15,
      "UNCERTAIN": 3
    },
    "confusion_matrix": [
      [
        2,
        7,
        6
      ],
      [
        0,
        1,
        2
      ],
      [
        0,
        1,
        35
      ]
    ]
  },
  "share_blocking": {
    "labels": [
      "NO",
      "YES"
    ],
    "support": {
      "NO": 8,
      "YES": 3
    },
    "confusion_matrix": [
      [
        8,
        0
      ],
      [
        0,
        3
      ]
    ]
  },
  "poa_required": {
    "labels": [
      "NO",
      "UNKNOWN",
      "YES"
    ],
    "support": {
      "NO": 5,
      "YES": 3
    },
    "confusion_matrix": [
      [
        4,
        1,
        0
      ],
      [
        0,
        0,
        0
      ],
      [
        1,
        0,
        2
      ]
    ]
  },
  "deadline_status": {
    "labels": [
      "OPEN",
      "PASSED",
      "UNKNOWN"
    ],
    "support": {
      "OPEN": 4,
      "PASSED": 4,
      "UNKNOWN": 6
    },
    "confusion_matrix": [
      [
        4,
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
        1,
        5
      ]
    ]
  },
  "other_restriction": {
    "labels": [
      "NO",
      "YES"
    ],
    "support": {
      "YES": 4
    },
    "confusion_matrix": [
      [
        0,
        0
      ],
      [
        4,
        0
      ]
    ]
  }
}
```

### synthetic-development / A

| Field | Correct/n | Positive / negative support | Precision+ | Recall+ | Specificity | F1+ | Macro F1 | Balanced accuracy |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| votability | 67/100 | 78 / 13 | 89.1% | 73.1% | 69.2% | 80.3% | 0.497 | 51.1% |
| share_blocking | 32/100 | 11 / 80 | 15.7% | 100.0% | 25.0% | 27.2% | 0.265 | 45.4% |
| poa_required | 77/100 | 11 / 80 | 41.7% | 90.9% | 82.5% | 57.1% | 0.541 | 61.5% |
| other_restriction | 59/100 | 20 / 71 | 11.1% | 5.0% | 77.5% | 6.9% | 0.366 | 38.6% |
| deadline_status | 57/100 | N/A / N/A | N/A | N/A | N/A | N/A | 0.462 | 66.2% |
| classification | 24/100 | N/A / N/A | N/A | N/A | N/A | N/A | 0.248 | 30.0% |

```json
{
  "votability": {
    "labels": [
      "NOT_VOTABLE",
      "UNCERTAIN",
      "VOTABLE"
    ],
    "support": {
      "VOTABLE": 78,
      "NOT_VOTABLE": 13,
      "UNCERTAIN": 9
    },
    "confusion_matrix": [
      [
        9,
        2,
        2
      ],
      [
        3,
        1,
        5
      ],
      [
        4,
        17,
        57
      ]
    ]
  },
  "share_blocking": {
    "labels": [
      "NO",
      "UNKNOWN",
      "YES"
    ],
    "support": {
      "NO": 80,
      "YES": 11,
      "UNKNOWN": 9
    },
    "confusion_matrix": [
      [
        20,
        4,
        56
      ],
      [
        5,
        1,
        3
      ],
      [
        0,
        0,
        11
      ]
    ]
  },
  "poa_required": {
    "labels": [
      "NO",
      "UNKNOWN",
      "YES"
    ],
    "support": {
      "NO": 80,
      "YES": 11,
      "UNKNOWN": 9
    },
    "confusion_matrix": [
      [
        66,
        0,
        14
      ],
      [
        8,
        1,
        0
      ],
      [
        1,
        0,
        10
      ]
    ]
  },
  "other_restriction": {
    "labels": [
      "NO",
      "UNKNOWN",
      "YES"
    ],
    "support": {
      "NO": 71,
      "YES": 20,
      "UNKNOWN": 9
    },
    "confusion_matrix": [
      [
        55,
        8,
        8
      ],
      [
        6,
        3,
        0
      ],
      [
        19,
        0,
        1
      ]
    ]
  },
  "deadline_status": {
    "labels": [
      "OPEN",
      "PASSED",
      "UNKNOWN"
    ],
    "support": {
      "OPEN": 83,
      "UNKNOWN": 9,
      "PASSED": 8
    },
    "confusion_matrix": [
      [
        45,
        29,
        9
      ],
      [
        0,
        8,
        0
      ],
      [
        0,
        5,
        4
      ]
    ]
  },
  "classification": {
    "labels": [
      "DEADLINE_PASSED",
      "NOT_VOTABLE",
      "UNCERTAIN_MANUAL_REVIEW",
      "VOTABLE",
      "VOTABLE_WITH_RESTRICTION"
    ],
    "support": {
      "VOTABLE": 36,
      "VOTABLE_WITH_RESTRICTION": 34,
      "NOT_VOTABLE": 13,
      "UNCERTAIN_MANUAL_REVIEW": 9,
      "DEADLINE_PASSED": 8
    },
    "confusion_matrix": [
      [
        3,
        0,
        5,
        0,
        0
      ],
      [
        2,
        9,
        2,
        0,
        0
      ],
      [
        5,
        3,
        1,
        0,
        0
      ],
      [
        5,
        0,
        8,
        2,
        21
      ],
      [
        11,
        4,
        10,
        0,
        9
      ]
    ]
  }
}
```

### synthetic-development / B

| Field | Correct/n | Positive / negative support | Precision+ | Recall+ | Specificity | F1+ | Macro F1 | Balanced accuracy |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| votability | 100/100 | 78 / 13 | 100.0% | 100.0% | 100.0% | 100.0% | 1.000 | 100.0% |
| share_blocking | 100/100 | 11 / 80 | 100.0% | 100.0% | 100.0% | 100.0% | 1.000 | 100.0% |
| poa_required | 100/100 | 11 / 80 | 100.0% | 100.0% | 100.0% | 100.0% | 1.000 | 100.0% |
| other_restriction | 100/100 | 20 / 71 | 100.0% | 100.0% | 100.0% | 100.0% | 1.000 | 100.0% |
| deadline_status | 100/100 | N/A / N/A | N/A | N/A | N/A | N/A | 1.000 | 100.0% |
| classification | 100/100 | N/A / N/A | N/A | N/A | N/A | N/A | 1.000 | 100.0% |

```json
{
  "votability": {
    "labels": [
      "NOT_VOTABLE",
      "UNCERTAIN",
      "VOTABLE"
    ],
    "support": {
      "VOTABLE": 78,
      "NOT_VOTABLE": 13,
      "UNCERTAIN": 9
    },
    "confusion_matrix": [
      [
        13,
        0,
        0
      ],
      [
        0,
        9,
        0
      ],
      [
        0,
        0,
        78
      ]
    ]
  },
  "share_blocking": {
    "labels": [
      "NO",
      "UNKNOWN",
      "YES"
    ],
    "support": {
      "NO": 80,
      "YES": 11,
      "UNKNOWN": 9
    },
    "confusion_matrix": [
      [
        80,
        0,
        0
      ],
      [
        0,
        9,
        0
      ],
      [
        0,
        0,
        11
      ]
    ]
  },
  "poa_required": {
    "labels": [
      "NO",
      "UNKNOWN",
      "YES"
    ],
    "support": {
      "NO": 80,
      "YES": 11,
      "UNKNOWN": 9
    },
    "confusion_matrix": [
      [
        80,
        0,
        0
      ],
      [
        0,
        9,
        0
      ],
      [
        0,
        0,
        11
      ]
    ]
  },
  "other_restriction": {
    "labels": [
      "NO",
      "UNKNOWN",
      "YES"
    ],
    "support": {
      "NO": 71,
      "YES": 20,
      "UNKNOWN": 9
    },
    "confusion_matrix": [
      [
        71,
        0,
        0
      ],
      [
        0,
        9,
        0
      ],
      [
        0,
        0,
        20
      ]
    ]
  },
  "deadline_status": {
    "labels": [
      "OPEN",
      "PASSED",
      "UNKNOWN"
    ],
    "support": {
      "OPEN": 83,
      "UNKNOWN": 9,
      "PASSED": 8
    },
    "confusion_matrix": [
      [
        83,
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
        9
      ]
    ]
  },
  "classification": {
    "labels": [
      "DEADLINE_PASSED",
      "NOT_VOTABLE",
      "UNCERTAIN_MANUAL_REVIEW",
      "VOTABLE",
      "VOTABLE_WITH_RESTRICTION"
    ],
    "support": {
      "VOTABLE": 36,
      "VOTABLE_WITH_RESTRICTION": 34,
      "NOT_VOTABLE": 13,
      "UNCERTAIN_MANUAL_REVIEW": 9,
      "DEADLINE_PASSED": 8
    },
    "confusion_matrix": [
      [
        8,
        0,
        0,
        0,
        0
      ],
      [
        0,
        13,
        0,
        0,
        0
      ],
      [
        0,
        0,
        9,
        0,
        0
      ],
      [
        0,
        0,
        0,
        36,
        0
      ],
      [
        0,
        0,
        0,
        0,
        34
      ]
    ]
  }
}
```

### synthetic-development / C

| Field | Correct/n | Positive / negative support | Precision+ | Recall+ | Specificity | F1+ | Macro F1 | Balanced accuracy |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| votability | 93/100 | 78 / 13 | 100.0% | 92.3% | 92.3% | 96.0% | 0.880 | 94.9% |
| share_blocking | 96/100 | 11 / 80 | 100.0% | 90.9% | 96.2% | 95.2% | 0.917 | 95.7% |
| poa_required | 100/100 | 11 / 80 | 100.0% | 100.0% | 100.0% | 100.0% | 1.000 | 100.0% |
| other_restriction | 92/100 | 20 / 71 | 100.0% | 60.0% | 100.0% | 75.0% | 0.883 | 86.7% |
| deadline_status | 19/100 | N/A / N/A | N/A | N/A | N/A | N/A | 0.132 | 37.3% |
| classification | 56/100 | N/A / N/A | N/A | N/A | N/A | N/A | 0.507 | 58.7% |

```json
{
  "votability": {
    "labels": [
      "NOT_VOTABLE",
      "UNCERTAIN",
      "VOTABLE"
    ],
    "support": {
      "VOTABLE": 78,
      "NOT_VOTABLE": 13,
      "UNCERTAIN": 9
    },
    "confusion_matrix": [
      [
        12,
        1,
        0
      ],
      [
        0,
        9,
        0
      ],
      [
        0,
        6,
        72
      ]
    ]
  },
  "share_blocking": {
    "labels": [
      "NO",
      "UNKNOWN",
      "YES"
    ],
    "support": {
      "NO": 80,
      "YES": 11,
      "UNKNOWN": 9
    },
    "confusion_matrix": [
      [
        77,
        3,
        0
      ],
      [
        0,
        9,
        0
      ],
      [
        0,
        1,
        10
      ]
    ]
  },
  "poa_required": {
    "labels": [
      "NO",
      "UNKNOWN",
      "YES"
    ],
    "support": {
      "NO": 80,
      "YES": 11,
      "UNKNOWN": 9
    },
    "confusion_matrix": [
      [
        80,
        0,
        0
      ],
      [
        0,
        9,
        0
      ],
      [
        0,
        0,
        11
      ]
    ]
  },
  "other_restriction": {
    "labels": [
      "NO",
      "UNKNOWN",
      "YES"
    ],
    "support": {
      "NO": 71,
      "YES": 20,
      "UNKNOWN": 9
    },
    "confusion_matrix": [
      [
        71,
        0,
        0
      ],
      [
        0,
        9,
        0
      ],
      [
        7,
        1,
        12
      ]
    ]
  },
  "deadline_status": {
    "labels": [
      "OPEN",
      "PASSED",
      "UNKNOWN"
    ],
    "support": {
      "OPEN": 83,
      "UNKNOWN": 9,
      "PASSED": 8
    },
    "confusion_matrix": [
      [
        10,
        0,
        73
      ],
      [
        0,
        0,
        8
      ],
      [
        0,
        0,
        9
      ]
    ]
  },
  "classification": {
    "labels": [
      "DEADLINE_PASSED",
      "NOT_VOTABLE",
      "UNCERTAIN_MANUAL_REVIEW",
      "VOTABLE",
      "VOTABLE_WITH_RESTRICTION"
    ],
    "support": {
      "VOTABLE": 36,
      "VOTABLE_WITH_RESTRICTION": 34,
      "NOT_VOTABLE": 13,
      "UNCERTAIN_MANUAL_REVIEW": 9,
      "DEADLINE_PASSED": 8
    },
    "confusion_matrix": [
      [
        0,
        0,
        8,
        0,
        0
      ],
      [
        0,
        12,
        1,
        0,
        0
      ],
      [
        0,
        0,
        9,
        0,
        0
      ],
      [
        0,
        0,
        26,
        10,
        0
      ],
      [
        0,
        0,
        9,
        0,
        25
      ]
    ]
  }
}
```

### synthetic-development / D

| Field | Correct/n | Positive / negative support | Precision+ | Recall+ | Specificity | F1+ | Macro F1 | Balanced accuracy |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| votability | 56/100 | 78 / 13 | 100.0% | 60.3% | 0.0% | 75.2% | 0.347 | 53.4% |
| share_blocking | 85/100 | 11 / 80 | 100.0% | 90.9% | 85.0% | 95.2% | 0.781 | 84.6% |
| poa_required | 86/100 | 11 / 80 | 90.9% | 90.9% | 86.2% | 90.9% | 0.776 | 85.0% |
| other_restriction | 78/100 | 20 / 71 | 100.0% | 55.0% | 84.5% | 71.0% | 0.674 | 72.4% |
| deadline_status | 17/100 | N/A / N/A | N/A | N/A | N/A | N/A | 0.118 | 36.5% |
| classification | 42/100 | N/A / N/A | N/A | N/A | N/A | N/A | 0.290 | 39.2% |

```json
{
  "votability": {
    "labels": [
      "NOT_VOTABLE",
      "UNCERTAIN",
      "VOTABLE"
    ],
    "support": {
      "VOTABLE": 78,
      "NOT_VOTABLE": 13,
      "UNCERTAIN": 9
    },
    "confusion_matrix": [
      [
        0,
        13,
        0
      ],
      [
        0,
        9,
        0
      ],
      [
        0,
        31,
        47
      ]
    ]
  },
  "share_blocking": {
    "labels": [
      "NO",
      "UNKNOWN",
      "YES"
    ],
    "support": {
      "NO": 80,
      "YES": 11,
      "UNKNOWN": 9
    },
    "confusion_matrix": [
      [
        68,
        12,
        0
      ],
      [
        2,
        7,
        0
      ],
      [
        0,
        1,
        10
      ]
    ]
  },
  "poa_required": {
    "labels": [
      "NO",
      "UNKNOWN",
      "YES"
    ],
    "support": {
      "NO": 80,
      "YES": 11,
      "UNKNOWN": 9
    },
    "confusion_matrix": [
      [
        69,
        11,
        0
      ],
      [
        1,
        7,
        1
      ],
      [
        0,
        1,
        10
      ]
    ]
  },
  "other_restriction": {
    "labels": [
      "NO",
      "UNKNOWN",
      "YES"
    ],
    "support": {
      "NO": 71,
      "YES": 20,
      "UNKNOWN": 9
    },
    "confusion_matrix": [
      [
        60,
        11,
        0
      ],
      [
        2,
        7,
        0
      ],
      [
        4,
        5,
        11
      ]
    ]
  },
  "deadline_status": {
    "labels": [
      "OPEN",
      "PASSED",
      "UNKNOWN"
    ],
    "support": {
      "OPEN": 83,
      "UNKNOWN": 9,
      "PASSED": 8
    },
    "confusion_matrix": [
      [
        8,
        0,
        75
      ],
      [
        0,
        0,
        8
      ],
      [
        0,
        0,
        9
      ]
    ]
  },
  "classification": {
    "labels": [
      "DEADLINE_PASSED",
      "NOT_VOTABLE",
      "UNCERTAIN_MANUAL_REVIEW",
      "VOTABLE",
      "VOTABLE_WITH_RESTRICTION"
    ],
    "support": {
      "VOTABLE": 36,
      "VOTABLE_WITH_RESTRICTION": 34,
      "NOT_VOTABLE": 13,
      "UNCERTAIN_MANUAL_REVIEW": 9,
      "DEADLINE_PASSED": 8
    },
    "confusion_matrix": [
      [
        0,
        0,
        8,
        0,
        0
      ],
      [
        0,
        0,
        13,
        0,
        0
      ],
      [
        0,
        0,
        9,
        0,
        0
      ],
      [
        0,
        0,
        28,
        8,
        0
      ],
      [
        0,
        0,
        9,
        0,
        25
      ]
    ]
  }
}
```

### synthetic-development / E

| Field | Correct/n | Positive / negative support | Precision+ | Recall+ | Specificity | F1+ | Macro F1 | Balanced accuracy |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| votability | 83/100 | 78 / 13 | 92.8% | 98.7% | 7.7% | 95.7% | 0.500 | 54.0% |
| share_blocking | 94/100 | 11 / 80 | 100.0% | 100.0% | 97.5% | 100.0% | 0.863 | 84.4% |
| poa_required | 96/100 | 11 / 80 | 100.0% | 100.0% | 100.0% | 100.0% | 0.897 | 85.2% |
| other_restriction | 71/100 | 20 / 71 | 80.0% | 20.0% | 87.3% | 32.0% | 0.519 | 54.3% |
| deadline_status | 17/100 | N/A / N/A | N/A | N/A | N/A | N/A | 0.118 | 36.5% |
| classification | 29/100 | N/A / N/A | N/A | N/A | N/A | N/A | 0.218 | 31.5% |

```json
{
  "votability": {
    "labels": [
      "NOT_VOTABLE",
      "UNCERTAIN",
      "VOTABLE"
    ],
    "support": {
      "VOTABLE": 78,
      "NOT_VOTABLE": 13,
      "UNCERTAIN": 9
    },
    "confusion_matrix": [
      [
        1,
        10,
        2
      ],
      [
        0,
        5,
        4
      ],
      [
        0,
        1,
        77
      ]
    ]
  },
  "share_blocking": {
    "labels": [
      "NO",
      "UNKNOWN",
      "YES"
    ],
    "support": {
      "NO": 80,
      "YES": 11,
      "UNKNOWN": 9
    },
    "confusion_matrix": [
      [
        78,
        2,
        0
      ],
      [
        4,
        5,
        0
      ],
      [
        0,
        0,
        11
      ]
    ]
  },
  "poa_required": {
    "labels": [
      "NO",
      "UNKNOWN",
      "YES"
    ],
    "support": {
      "NO": 80,
      "YES": 11,
      "UNKNOWN": 9
    },
    "confusion_matrix": [
      [
        80,
        0,
        0
      ],
      [
        4,
        5,
        0
      ],
      [
        0,
        0,
        11
      ]
    ]
  },
  "other_restriction": {
    "labels": [
      "NO",
      "UNKNOWN",
      "YES"
    ],
    "support": {
      "NO": 71,
      "YES": 20,
      "UNKNOWN": 9
    },
    "confusion_matrix": [
      [
        62,
        8,
        1
      ],
      [
        4,
        5,
        0
      ],
      [
        14,
        2,
        4
      ]
    ]
  },
  "deadline_status": {
    "labels": [
      "OPEN",
      "PASSED",
      "UNKNOWN"
    ],
    "support": {
      "OPEN": 83,
      "UNKNOWN": 9,
      "PASSED": 8
    },
    "confusion_matrix": [
      [
        8,
        0,
        75
      ],
      [
        0,
        0,
        8
      ],
      [
        0,
        0,
        9
      ]
    ]
  },
  "classification": {
    "labels": [
      "DEADLINE_PASSED",
      "NOT_VOTABLE",
      "UNCERTAIN_MANUAL_REVIEW",
      "VOTABLE",
      "VOTABLE_WITH_RESTRICTION"
    ],
    "support": {
      "VOTABLE": 36,
      "VOTABLE_WITH_RESTRICTION": 34,
      "NOT_VOTABLE": 13,
      "UNCERTAIN_MANUAL_REVIEW": 9,
      "DEADLINE_PASSED": 8
    },
    "confusion_matrix": [
      [
        0,
        0,
        8,
        0,
        0
      ],
      [
        0,
        0,
        13,
        0,
        0
      ],
      [
        0,
        0,
        9,
        0,
        0
      ],
      [
        0,
        0,
        28,
        8,
        0
      ],
      [
        0,
        0,
        22,
        0,
        12
      ]
    ]
  }
}
```

### complete / A

| Field | Correct/n | Positive / negative support | Precision+ | Recall+ | Specificity | F1+ | Macro F1 | Balanced accuracy |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| votability | 39/48 | 42 / 4 | 97.2% | 83.3% | 75.0% | 89.7% | 0.616 | 69.4% |
| share_blocking | 7/48 | 3 / 44 | 7.0% | 100.0% | 9.1% | 13.0% | 0.099 | 36.4% |
| poa_required | 31/48 | 3 / 44 | 12.5% | 66.7% | 65.9% | 21.1% | 0.328 | 44.2% |
| registration_required | 0/48 | 3 / 45 | N/A | 0.0% | 0.0% | 0.0% | 0.000 | 0.0% |
| beneficial_owner_disclosure_required | 0/48 | 3 / 45 | N/A | 0.0% | 0.0% | 0.0% | 0.000 | 0.0% |
| holding_confirmation_required | 0/48 | 3 / 45 | N/A | 0.0% | 0.0% | 0.0% | 0.000 | 0.0% |
| split_voting_restricted | 0/48 | 3 / 45 | N/A | 0.0% | 0.0% | 0.0% | 0.000 | 0.0% |
| securities_lending_recall_required | 0/48 | 4 / 44 | N/A | 0.0% | 0.0% | 0.0% | 0.000 | 0.0% |
| other_voting_restriction | 0/48 | 3 / 45 | N/A | 0.0% | 0.0% | 0.0% | 0.000 | 0.0% |
| deadline_status | 5/48 | N/A / N/A | N/A | N/A | N/A | N/A | 0.212 | 29.4% |
| classification | 8/48 | N/A / N/A | N/A | N/A | N/A | N/A | 0.257 | 36.9% |

```json
{
  "votability": {
    "labels": [
      "NOT_VOTABLE",
      "UNCERTAIN",
      "VOTABLE"
    ],
    "support": {
      "VOTABLE": 42,
      "NOT_VOTABLE": 4,
      "UNCERTAIN": 2
    },
    "confusion_matrix": [
      [
        3,
        1,
        0
      ],
      [
        0,
        1,
        1
      ],
      [
        1,
        6,
        35
      ]
    ]
  },
  "share_blocking": {
    "labels": [
      "NO",
      "UNKNOWN",
      "YES"
    ],
    "support": {
      "YES": 3,
      "NO": 44,
      "UNKNOWN": 1
    },
    "confusion_matrix": [
      [
        4,
        1,
        39
      ],
      [
        0,
        0,
        1
      ],
      [
        0,
        0,
        3
      ]
    ]
  },
  "poa_required": {
    "labels": [
      "NO",
      "UNKNOWN",
      "YES"
    ],
    "support": {
      "NO": 44,
      "YES": 3,
      "UNKNOWN": 1
    },
    "confusion_matrix": [
      [
        29,
        1,
        14
      ],
      [
        1,
        0,
        0
      ],
      [
        1,
        0,
        2
      ]
    ]
  },
  "registration_required": {
    "labels": [
      "NO",
      "NOT_SUPPORTED",
      "YES"
    ],
    "support": {
      "NO": 45,
      "YES": 3
    },
    "confusion_matrix": [
      [
        0,
        45,
        0
      ],
      [
        0,
        0,
        0
      ],
      [
        0,
        3,
        0
      ]
    ]
  },
  "beneficial_owner_disclosure_required": {
    "labels": [
      "NO",
      "NOT_SUPPORTED",
      "YES"
    ],
    "support": {
      "NO": 45,
      "YES": 3
    },
    "confusion_matrix": [
      [
        0,
        45,
        0
      ],
      [
        0,
        0,
        0
      ],
      [
        0,
        3,
        0
      ]
    ]
  },
  "holding_confirmation_required": {
    "labels": [
      "NO",
      "NOT_SUPPORTED",
      "YES"
    ],
    "support": {
      "NO": 45,
      "YES": 3
    },
    "confusion_matrix": [
      [
        0,
        45,
        0
      ],
      [
        0,
        0,
        0
      ],
      [
        0,
        3,
        0
      ]
    ]
  },
  "split_voting_restricted": {
    "labels": [
      "NO",
      "NOT_SUPPORTED",
      "YES"
    ],
    "support": {
      "NO": 45,
      "YES": 3
    },
    "confusion_matrix": [
      [
        0,
        45,
        0
      ],
      [
        0,
        0,
        0
      ],
      [
        0,
        3,
        0
      ]
    ]
  },
  "securities_lending_recall_required": {
    "labels": [
      "NO",
      "NOT_SUPPORTED",
      "YES"
    ],
    "support": {
      "NO": 44,
      "YES": 4
    },
    "confusion_matrix": [
      [
        0,
        44,
        0
      ],
      [
        0,
        0,
        0
      ],
      [
        0,
        4,
        0
      ]
    ]
  },
  "other_voting_restriction": {
    "labels": [
      "NO",
      "NOT_SUPPORTED",
      "YES"
    ],
    "support": {
      "NO": 45,
      "YES": 3
    },
    "confusion_matrix": [
      [
        0,
        45,
        0
      ],
      [
        0,
        0,
        0
      ],
      [
        0,
        3,
        0
      ]
    ]
  },
  "deadline_status": {
    "labels": [
      "OPEN",
      "PASSED",
      "UNKNOWN"
    ],
    "support": {
      "OPEN": 40,
      "UNKNOWN": 6,
      "PASSED": 2
    },
    "confusion_matrix": [
      [
        2,
        38,
        0
      ],
      [
        1,
        1,
        0
      ],
      [
        1,
        3,
        2
      ]
    ]
  },
  "classification": {
    "labels": [
      "DEADLINE_PASSED",
      "NOT_VOTABLE",
      "UNCERTAIN_MANUAL_REVIEW",
      "VOTABLE",
      "VOTABLE_WITH_RESTRICTION"
    ],
    "support": {
      "VOTABLE_WITH_RESTRICTION": 21,
      "VOTABLE": 17,
      "NOT_VOTABLE": 4,
      "UNCERTAIN_MANUAL_REVIEW": 4,
      "DEADLINE_PASSED": 2
    },
    "confusion_matrix": [
      [
        1,
        0,
        0,
        0,
        1
      ],
      [
        0,
        3,
        1,
        0,
        0
      ],
      [
        2,
        0,
        2,
        0,
        0
      ],
      [
        13,
        1,
        3,
        0,
        0
      ],
      [
        16,
        0,
        3,
        0,
        2
      ]
    ]
  }
}
```

### complete / B

| Field | Correct/n | Positive / negative support | Precision+ | Recall+ | Specificity | F1+ | Macro F1 | Balanced accuracy |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| votability | 47/48 | 42 / 4 | 97.7% | 100.0% | 100.0% | 98.8% | 0.885 | 83.3% |
| share_blocking | 43/48 | 3 / 44 | N/A | 0.0% | 97.7% | 0.0% | 0.315 | 32.6% |
| poa_required | 44/48 | 3 / 44 | 100.0% | 66.7% | 95.5% | 80.0% | 0.585 | 54.0% |
| registration_required | 0/48 | 3 / 45 | N/A | 0.0% | 0.0% | 0.0% | 0.000 | 0.0% |
| beneficial_owner_disclosure_required | 0/48 | 3 / 45 | N/A | 0.0% | 0.0% | 0.0% | 0.000 | 0.0% |
| holding_confirmation_required | 0/48 | 3 / 45 | N/A | 0.0% | 0.0% | 0.0% | 0.000 | 0.0% |
| split_voting_restricted | 0/48 | 3 / 45 | N/A | 0.0% | 0.0% | 0.0% | 0.000 | 0.0% |
| securities_lending_recall_required | 0/48 | 4 / 44 | N/A | 0.0% | 0.0% | 0.0% | 0.000 | 0.0% |
| other_voting_restriction | 0/48 | 3 / 45 | N/A | 0.0% | 0.0% | 0.0% | 0.000 | 0.0% |
| deadline_status | 41/48 | N/A / N/A | N/A | N/A | N/A | N/A | 0.402 | 38.9% |
| classification | 24/48 | N/A / N/A | N/A | N/A | N/A | N/A | 0.482 | 50.7% |

```json
{
  "votability": {
    "labels": [
      "NOT_VOTABLE",
      "UNCERTAIN",
      "VOTABLE"
    ],
    "support": {
      "VOTABLE": 42,
      "NOT_VOTABLE": 4,
      "UNCERTAIN": 2
    },
    "confusion_matrix": [
      [
        4,
        0,
        0
      ],
      [
        0,
        1,
        1
      ],
      [
        0,
        0,
        42
      ]
    ]
  },
  "share_blocking": {
    "labels": [
      "NO",
      "UNKNOWN",
      "YES"
    ],
    "support": {
      "YES": 3,
      "NO": 44,
      "UNKNOWN": 1
    },
    "confusion_matrix": [
      [
        43,
        1,
        0
      ],
      [
        1,
        0,
        0
      ],
      [
        3,
        0,
        0
      ]
    ]
  },
  "poa_required": {
    "labels": [
      "NO",
      "UNKNOWN",
      "YES"
    ],
    "support": {
      "NO": 44,
      "YES": 3,
      "UNKNOWN": 1
    },
    "confusion_matrix": [
      [
        42,
        2,
        0
      ],
      [
        1,
        0,
        0
      ],
      [
        1,
        0,
        2
      ]
    ]
  },
  "registration_required": {
    "labels": [
      "NO",
      "NOT_SUPPORTED",
      "YES"
    ],
    "support": {
      "NO": 45,
      "YES": 3
    },
    "confusion_matrix": [
      [
        0,
        45,
        0
      ],
      [
        0,
        0,
        0
      ],
      [
        0,
        3,
        0
      ]
    ]
  },
  "beneficial_owner_disclosure_required": {
    "labels": [
      "NO",
      "NOT_SUPPORTED",
      "YES"
    ],
    "support": {
      "NO": 45,
      "YES": 3
    },
    "confusion_matrix": [
      [
        0,
        45,
        0
      ],
      [
        0,
        0,
        0
      ],
      [
        0,
        3,
        0
      ]
    ]
  },
  "holding_confirmation_required": {
    "labels": [
      "NO",
      "NOT_SUPPORTED",
      "YES"
    ],
    "support": {
      "NO": 45,
      "YES": 3
    },
    "confusion_matrix": [
      [
        0,
        45,
        0
      ],
      [
        0,
        0,
        0
      ],
      [
        0,
        3,
        0
      ]
    ]
  },
  "split_voting_restricted": {
    "labels": [
      "NO",
      "NOT_SUPPORTED",
      "YES"
    ],
    "support": {
      "NO": 45,
      "YES": 3
    },
    "confusion_matrix": [
      [
        0,
        45,
        0
      ],
      [
        0,
        0,
        0
      ],
      [
        0,
        3,
        0
      ]
    ]
  },
  "securities_lending_recall_required": {
    "labels": [
      "NO",
      "NOT_SUPPORTED",
      "YES"
    ],
    "support": {
      "NO": 44,
      "YES": 4
    },
    "confusion_matrix": [
      [
        0,
        44,
        0
      ],
      [
        0,
        0,
        0
      ],
      [
        0,
        4,
        0
      ]
    ]
  },
  "other_voting_restriction": {
    "labels": [
      "NO",
      "NOT_SUPPORTED",
      "YES"
    ],
    "support": {
      "NO": 45,
      "YES": 3
    },
    "confusion_matrix": [
      [
        0,
        45,
        0
      ],
      [
        0,
        0,
        0
      ],
      [
        0,
        3,
        0
      ]
    ]
  },
  "deadline_status": {
    "labels": [
      "OPEN",
      "PASSED",
      "UNKNOWN"
    ],
    "support": {
      "OPEN": 40,
      "UNKNOWN": 6,
      "PASSED": 2
    },
    "confusion_matrix": [
      [
        40,
        0,
        0
      ],
      [
        2,
        0,
        0
      ],
      [
        5,
        0,
        1
      ]
    ]
  },
  "classification": {
    "labels": [
      "DEADLINE_PASSED",
      "NOT_VOTABLE",
      "UNCERTAIN_MANUAL_REVIEW",
      "VOTABLE",
      "VOTABLE_WITH_RESTRICTION"
    ],
    "support": {
      "VOTABLE_WITH_RESTRICTION": 21,
      "VOTABLE": 17,
      "NOT_VOTABLE": 4,
      "UNCERTAIN_MANUAL_REVIEW": 4,
      "DEADLINE_PASSED": 2
    },
    "confusion_matrix": [
      [
        0,
        0,
        0,
        2,
        0
      ],
      [
        0,
        4,
        0,
        0,
        0
      ],
      [
        0,
        0,
        2,
        1,
        1
      ],
      [
        0,
        0,
        0,
        16,
        1
      ],
      [
        0,
        0,
        0,
        19,
        2
      ]
    ]
  }
}
```

### complete / C

| Field | Correct/n | Positive / negative support | Precision+ | Recall+ | Specificity | F1+ | Macro F1 | Balanced accuracy |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| votability | 48/48 | 42 / 4 | 100.0% | 100.0% | 100.0% | 100.0% | 1.000 | 100.0% |
| share_blocking | 41/48 | 3 / 44 | N/A | 0.0% | 93.2% | 0.0% | 0.314 | 31.1% |
| poa_required | 44/48 | 3 / 44 | 100.0% | 66.7% | 93.2% | 80.0% | 0.718 | 86.6% |
| registration_required | 44/48 | 3 / 45 | 100.0% | 33.3% | 95.6% | 50.0% | 0.728 | 64.4% |
| beneficial_owner_disclosure_required | 47/48 | 3 / 45 | 100.0% | 100.0% | 97.8% | 100.0% | 0.994 | 98.9% |
| holding_confirmation_required | 45/48 | 3 / 45 | 100.0% | 33.3% | 97.8% | 50.0% | 0.734 | 65.6% |
| split_voting_restricted | 47/48 | 3 / 45 | 100.0% | 100.0% | 97.8% | 100.0% | 0.994 | 98.9% |
| securities_lending_recall_required | 47/48 | 4 / 44 | 100.0% | 100.0% | 97.7% | 100.0% | 0.994 | 98.9% |
| other_voting_restriction | 43/48 | 3 / 45 | 100.0% | 33.3% | 93.3% | 50.0% | 0.722 | 63.3% |
| deadline_status | 40/48 | N/A / N/A | N/A | N/A | N/A | N/A | 0.830 | 93.3% |
| classification | 38/48 | N/A / N/A | N/A | N/A | N/A | N/A | 0.831 | 90.0% |

```json
{
  "votability": {
    "labels": [
      "NOT_VOTABLE",
      "UNCERTAIN",
      "VOTABLE"
    ],
    "support": {
      "VOTABLE": 42,
      "NOT_VOTABLE": 4,
      "UNCERTAIN": 2
    },
    "confusion_matrix": [
      [
        4,
        0,
        0
      ],
      [
        0,
        2,
        0
      ],
      [
        0,
        0,
        42
      ]
    ]
  },
  "share_blocking": {
    "labels": [
      "NO",
      "UNKNOWN",
      "YES"
    ],
    "support": {
      "YES": 3,
      "NO": 44,
      "UNKNOWN": 1
    },
    "confusion_matrix": [
      [
        41,
        3,
        0
      ],
      [
        1,
        0,
        0
      ],
      [
        1,
        2,
        0
      ]
    ]
  },
  "poa_required": {
    "labels": [
      "NO",
      "UNKNOWN",
      "YES"
    ],
    "support": {
      "NO": 44,
      "YES": 3,
      "UNKNOWN": 1
    },
    "confusion_matrix": [
      [
        41,
        3,
        0
      ],
      [
        0,
        1,
        0
      ],
      [
        1,
        0,
        2
      ]
    ]
  },
  "registration_required": {
    "labels": [
      "NO",
      "UNKNOWN",
      "YES"
    ],
    "support": {
      "NO": 45,
      "YES": 3
    },
    "confusion_matrix": [
      [
        43,
        2,
        0
      ],
      [
        0,
        0,
        0
      ],
      [
        2,
        0,
        1
      ]
    ]
  },
  "beneficial_owner_disclosure_required": {
    "labels": [
      "NO",
      "UNKNOWN",
      "YES"
    ],
    "support": {
      "NO": 45,
      "YES": 3
    },
    "confusion_matrix": [
      [
        44,
        1,
        0
      ],
      [
        0,
        0,
        0
      ],
      [
        0,
        0,
        3
      ]
    ]
  },
  "holding_confirmation_required": {
    "labels": [
      "NO",
      "UNKNOWN",
      "YES"
    ],
    "support": {
      "NO": 45,
      "YES": 3
    },
    "confusion_matrix": [
      [
        44,
        1,
        0
      ],
      [
        0,
        0,
        0
      ],
      [
        2,
        0,
        1
      ]
    ]
  },
  "split_voting_restricted": {
    "labels": [
      "NO",
      "UNKNOWN",
      "YES"
    ],
    "support": {
      "NO": 45,
      "YES": 3
    },
    "confusion_matrix": [
      [
        44,
        1,
        0
      ],
      [
        0,
        0,
        0
      ],
      [
        0,
        0,
        3
      ]
    ]
  },
  "securities_lending_recall_required": {
    "labels": [
      "NO",
      "UNKNOWN",
      "YES"
    ],
    "support": {
      "NO": 44,
      "YES": 4
    },
    "confusion_matrix": [
      [
        43,
        1,
        0
      ],
      [
        0,
        0,
        0
      ],
      [
        0,
        0,
        4
      ]
    ]
  },
  "other_voting_restriction": {
    "labels": [
      "NO",
      "UNKNOWN",
      "YES"
    ],
    "support": {
      "NO": 45,
      "YES": 3
    },
    "confusion_matrix": [
      [
        42,
        3,
        0
      ],
      [
        0,
        0,
        0
      ],
      [
        2,
        0,
        1
      ]
    ]
  },
  "deadline_status": {
    "labels": [
      "OPEN",
      "PASSED",
      "UNKNOWN"
    ],
    "support": {
      "OPEN": 40,
      "UNKNOWN": 6,
      "PASSED": 2
    },
    "confusion_matrix": [
      [
        32,
        0,
        8
      ],
      [
        0,
        2,
        0
      ],
      [
        0,
        0,
        6
      ]
    ]
  },
  "classification": {
    "labels": [
      "DEADLINE_PASSED",
      "NOT_VOTABLE",
      "UNCERTAIN_MANUAL_REVIEW",
      "VOTABLE",
      "VOTABLE_WITH_RESTRICTION"
    ],
    "support": {
      "VOTABLE_WITH_RESTRICTION": 21,
      "VOTABLE": 17,
      "NOT_VOTABLE": 4,
      "UNCERTAIN_MANUAL_REVIEW": 4,
      "DEADLINE_PASSED": 2
    },
    "confusion_matrix": [
      [
        2,
        0,
        0,
        0,
        0
      ],
      [
        0,
        4,
        0,
        0,
        0
      ],
      [
        0,
        0,
        4,
        0,
        0
      ],
      [
        0,
        0,
        2,
        15,
        0
      ],
      [
        0,
        0,
        5,
        3,
        13
      ]
    ]
  }
}
```

### complete / D

| Field | Correct/n | Positive / negative support | Precision+ | Recall+ | Specificity | F1+ | Macro F1 | Balanced accuracy |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| votability | 37/48 | 42 / 4 | 100.0% | 83.3% | 0.0% | 90.9% | 0.392 | 61.1% |
| share_blocking | 45/48 | 3 / 44 | 60.0% | 100.0% | 95.5% | 75.0% | 0.576 | 65.2% |
| poa_required | 47/48 | 3 / 44 | 100.0% | 100.0% | 97.7% | 100.0% | 0.885 | 99.2% |
| registration_required | 46/48 | 3 / 45 | 100.0% | 66.7% | 97.8% | 80.0% | 0.889 | 82.2% |
| beneficial_owner_disclosure_required | 47/48 | 3 / 45 | 100.0% | 100.0% | 97.8% | 100.0% | 0.994 | 98.9% |
| holding_confirmation_required | 47/48 | 3 / 45 | 100.0% | 100.0% | 97.8% | 100.0% | 0.994 | 98.9% |
| split_voting_restricted | 47/48 | 3 / 45 | 100.0% | 100.0% | 97.8% | 100.0% | 0.994 | 98.9% |
| securities_lending_recall_required | 47/48 | 4 / 44 | 100.0% | 100.0% | 97.7% | 100.0% | 0.994 | 98.9% |
| other_voting_restriction | 46/48 | 3 / 45 | 100.0% | 66.7% | 97.8% | 80.0% | 0.889 | 82.2% |
| deadline_status | 40/48 | N/A / N/A | N/A | N/A | N/A | N/A | 0.830 | 93.3% |
| classification | 36/48 | N/A / N/A | N/A | N/A | N/A | N/A | 0.433 | 50.2% |

```json
{
  "votability": {
    "labels": [
      "NOT_VOTABLE",
      "UNCERTAIN",
      "VOTABLE"
    ],
    "support": {
      "VOTABLE": 42,
      "NOT_VOTABLE": 4,
      "UNCERTAIN": 2
    },
    "confusion_matrix": [
      [
        0,
        4,
        0
      ],
      [
        0,
        2,
        0
      ],
      [
        0,
        7,
        35
      ]
    ]
  },
  "share_blocking": {
    "labels": [
      "NO",
      "UNKNOWN",
      "YES"
    ],
    "support": {
      "YES": 3,
      "NO": 44,
      "UNKNOWN": 1
    },
    "confusion_matrix": [
      [
        42,
        1,
        1
      ],
      [
        0,
        0,
        1
      ],
      [
        0,
        0,
        3
      ]
    ]
  },
  "poa_required": {
    "labels": [
      "NO",
      "UNKNOWN",
      "YES"
    ],
    "support": {
      "NO": 44,
      "YES": 3,
      "UNKNOWN": 1
    },
    "confusion_matrix": [
      [
        43,
        1,
        0
      ],
      [
        0,
        1,
        0
      ],
      [
        0,
        0,
        3
      ]
    ]
  },
  "registration_required": {
    "labels": [
      "NO",
      "UNKNOWN",
      "YES"
    ],
    "support": {
      "NO": 45,
      "YES": 3
    },
    "confusion_matrix": [
      [
        44,
        1,
        0
      ],
      [
        0,
        0,
        0
      ],
      [
        1,
        0,
        2
      ]
    ]
  },
  "beneficial_owner_disclosure_required": {
    "labels": [
      "NO",
      "UNKNOWN",
      "YES"
    ],
    "support": {
      "NO": 45,
      "YES": 3
    },
    "confusion_matrix": [
      [
        44,
        1,
        0
      ],
      [
        0,
        0,
        0
      ],
      [
        0,
        0,
        3
      ]
    ]
  },
  "holding_confirmation_required": {
    "labels": [
      "NO",
      "UNKNOWN",
      "YES"
    ],
    "support": {
      "NO": 45,
      "YES": 3
    },
    "confusion_matrix": [
      [
        44,
        1,
        0
      ],
      [
        0,
        0,
        0
      ],
      [
        0,
        0,
        3
      ]
    ]
  },
  "split_voting_restricted": {
    "labels": [
      "NO",
      "UNKNOWN",
      "YES"
    ],
    "support": {
      "NO": 45,
      "YES": 3
    },
    "confusion_matrix": [
      [
        44,
        1,
        0
      ],
      [
        0,
        0,
        0
      ],
      [
        0,
        0,
        3
      ]
    ]
  },
  "securities_lending_recall_required": {
    "labels": [
      "NO",
      "UNKNOWN",
      "YES"
    ],
    "support": {
      "NO": 44,
      "YES": 4
    },
    "confusion_matrix": [
      [
        43,
        1,
        0
      ],
      [
        0,
        0,
        0
      ],
      [
        0,
        0,
        4
      ]
    ]
  },
  "other_voting_restriction": {
    "labels": [
      "NO",
      "UNKNOWN",
      "YES"
    ],
    "support": {
      "NO": 45,
      "YES": 3
    },
    "confusion_matrix": [
      [
        44,
        1,
        0
      ],
      [
        0,
        0,
        0
      ],
      [
        1,
        0,
        2
      ]
    ]
  },
  "deadline_status": {
    "labels": [
      "OPEN",
      "PASSED",
      "UNKNOWN"
    ],
    "support": {
      "OPEN": 40,
      "UNKNOWN": 6,
      "PASSED": 2
    },
    "confusion_matrix": [
      [
        32,
        0,
        8
      ],
      [
        0,
        2,
        0
      ],
      [
        0,
        0,
        6
      ]
    ]
  },
  "classification": {
    "labels": [
      "DEADLINE_PASSED",
      "NOT_VOTABLE",
      "UNCERTAIN_MANUAL_REVIEW",
      "VOTABLE",
      "VOTABLE_WITH_RESTRICTION"
    ],
    "support": {
      "VOTABLE_WITH_RESTRICTION": 21,
      "VOTABLE": 17,
      "NOT_VOTABLE": 4,
      "UNCERTAIN_MANUAL_REVIEW": 4,
      "DEADLINE_PASSED": 2
    },
    "confusion_matrix": [
      [
        0,
        0,
        2,
        0,
        0
      ],
      [
        0,
        0,
        4,
        0,
        0
      ],
      [
        0,
        0,
        3,
        0,
        1
      ],
      [
        0,
        0,
        0,
        17,
        0
      ],
      [
        0,
        0,
        4,
        1,
        16
      ]
    ]
  }
}
```

### complete / E

| Field | Correct/n | Positive / negative support | Precision+ | Recall+ | Specificity | F1+ | Macro F1 | Balanced accuracy |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| votability | 44/48 | 42 / 4 | 97.7% | 100.0% | 0.0% | 98.8% | 0.520 | 66.7% |
| share_blocking | 45/48 | 3 / 44 | 100.0% | 100.0% | 95.5% | 100.0% | 0.655 | 65.2% |
| poa_required | 46/48 | 3 / 44 | 100.0% | 100.0% | 97.7% | 100.0% | 0.659 | 65.9% |
| registration_required | 24/48 | 3 / 45 | 100.0% | 33.3% | 51.1% | 50.0% | 0.579 | 42.2% |
| beneficial_owner_disclosure_required | 41/48 | 3 / 45 | N/A | 0.0% | 91.1% | 0.0% | 0.466 | 45.6% |
| holding_confirmation_required | 42/48 | 3 / 45 | 100.0% | 66.7% | 88.9% | 80.0% | 0.871 | 77.8% |
| split_voting_restricted | 44/48 | 3 / 45 | 100.0% | 33.3% | 95.6% | 50.0% | 0.733 | 64.4% |
| securities_lending_recall_required | 23/48 | 4 / 44 | 100.0% | 50.0% | 47.7% | 66.7% | 0.647 | 48.9% |
| other_voting_restriction | 41/48 | 3 / 45 | N/A | 0.0% | 91.1% | 0.0% | 0.461 | 45.6% |
| deadline_status | 48/48 | N/A / N/A | N/A | N/A | N/A | N/A | 1.000 | 100.0% |
| classification | 12/48 | N/A / N/A | N/A | N/A | N/A | N/A | 0.342 | 38.1% |

```json
{
  "votability": {
    "labels": [
      "NOT_VOTABLE",
      "UNCERTAIN",
      "VOTABLE"
    ],
    "support": {
      "VOTABLE": 42,
      "NOT_VOTABLE": 4,
      "UNCERTAIN": 2
    },
    "confusion_matrix": [
      [
        0,
        3,
        1
      ],
      [
        0,
        2,
        0
      ],
      [
        0,
        0,
        42
      ]
    ]
  },
  "share_blocking": {
    "labels": [
      "NO",
      "UNKNOWN",
      "YES"
    ],
    "support": {
      "YES": 3,
      "NO": 44,
      "UNKNOWN": 1
    },
    "confusion_matrix": [
      [
        42,
        2,
        0
      ],
      [
        1,
        0,
        0
      ],
      [
        0,
        0,
        3
      ]
    ]
  },
  "poa_required": {
    "labels": [
      "NO",
      "UNKNOWN",
      "YES"
    ],
    "support": {
      "NO": 44,
      "YES": 3,
      "UNKNOWN": 1
    },
    "confusion_matrix": [
      [
        43,
        1,
        0
      ],
      [
        1,
        0,
        0
      ],
      [
        0,
        0,
        3
      ]
    ]
  },
  "registration_required": {
    "labels": [
      "NO",
      "UNKNOWN",
      "YES"
    ],
    "support": {
      "NO": 45,
      "YES": 3
    },
    "confusion_matrix": [
      [
        23,
        22,
        0
      ],
      [
        0,
        0,
        0
      ],
      [
        2,
        0,
        1
      ]
    ]
  },
  "beneficial_owner_disclosure_required": {
    "labels": [
      "NO",
      "UNKNOWN",
      "YES"
    ],
    "support": {
      "NO": 45,
      "YES": 3
    },
    "confusion_matrix": [
      [
        41,
        4,
        0
      ],
      [
        0,
        0,
        0
      ],
      [
        2,
        1,
        0
      ]
    ]
  },
  "holding_confirmation_required": {
    "labels": [
      "NO",
      "UNKNOWN",
      "YES"
    ],
    "support": {
      "NO": 45,
      "YES": 3
    },
    "confusion_matrix": [
      [
        40,
        5,
        0
      ],
      [
        0,
        0,
        0
      ],
      [
        0,
        1,
        2
      ]
    ]
  },
  "split_voting_restricted": {
    "labels": [
      "NO",
      "UNKNOWN",
      "YES"
    ],
    "support": {
      "NO": 45,
      "YES": 3
    },
    "confusion_matrix": [
      [
        43,
        2,
        0
      ],
      [
        0,
        0,
        0
      ],
      [
        1,
        1,
        1
      ]
    ]
  },
  "securities_lending_recall_required": {
    "labels": [
      "NO",
      "UNKNOWN",
      "YES"
    ],
    "support": {
      "NO": 44,
      "YES": 4
    },
    "confusion_matrix": [
      [
        21,
        23,
        0
      ],
      [
        0,
        0,
        0
      ],
      [
        2,
        0,
        2
      ]
    ]
  },
  "other_voting_restriction": {
    "labels": [
      "NO",
      "UNKNOWN",
      "YES"
    ],
    "support": {
      "NO": 45,
      "YES": 3
    },
    "confusion_matrix": [
      [
        41,
        4,
        0
      ],
      [
        0,
        0,
        0
      ],
      [
        3,
        0,
        0
      ]
    ]
  },
  "deadline_status": {
    "labels": [
      "OPEN",
      "PASSED",
      "UNKNOWN"
    ],
    "support": {
      "OPEN": 40,
      "UNKNOWN": 6,
      "PASSED": 2
    },
    "confusion_matrix": [
      [
        40,
        0,
        0
      ],
      [
        0,
        2,
        0
      ],
      [
        0,
        0,
        6
      ]
    ]
  },
  "classification": {
    "labels": [
      "DEADLINE_PASSED",
      "NOT_VOTABLE",
      "UNCERTAIN_MANUAL_REVIEW",
      "VOTABLE",
      "VOTABLE_WITH_RESTRICTION"
    ],
    "support": {
      "VOTABLE_WITH_RESTRICTION": 21,
      "VOTABLE": 17,
      "NOT_VOTABLE": 4,
      "UNCERTAIN_MANUAL_REVIEW": 4,
      "DEADLINE_PASSED": 2
    },
    "confusion_matrix": [
      [
        2,
        0,
        0,
        0,
        0
      ],
      [
        0,
        0,
        4,
        0,
        0
      ],
      [
        0,
        0,
        2,
        2,
        0
      ],
      [
        0,
        0,
        15,
        2,
        0
      ],
      [
        0,
        0,
        9,
        6,
        6
      ]
    ]
  }
}
```
