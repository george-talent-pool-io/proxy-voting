# Framework E2E and model-readiness review — 22 October 2026

## Verdict

The framework had materially stronger research-interface coverage than customer-workflow coverage. It now exercises the authenticated customer qualification and second-round learning journey. Software workflow checks pass, but this does not certify a broadly accurate pretrained voting model. A newly trained Laya candidate improves the development benchmark; it remains an AI-test derivative outside the shipped product. Customer automation stays disabled.

## Gaps found and fixed

1. **Customer browser coverage:** expanded from one import/review smoke test to six tests, including a complete two-round learning/qualification journey. The primary documented browser command now selects all `e2e` tests, including `tests/production`, instead of silently limiting execution to the research directory.
2. **Successive learning rounds:** the customer API previously rejected a registered derivative outside the foundation model volume. A trainer can now freeze a completed job through `POST /api/client/starting-checkpoints/from-job`. Admission accepts only managed, hash-verified registered lineage; arbitrary paths, altered weights and forged lineage are rejected. Origin is derived by the server and cannot be supplied by the caller. Parent weights remain unchanged.
3. **Misleading training budgets:** the one-epoch/frozen-encoder Laya and two-step Qwen configurations are now explicitly distinguished from bounded full-encoder/multi-layer domain candidate recipes. These recipes are experiments, not trained-model or optimal-hyperparameter claims.
4. **Model identity versus quality:** starting-checkpoint API/UI lists readiness separately from identity. Foundation-only, AI-test and customer derivatives all require independent deployment qualification. A user-supplied receipt is not proof of accuracy.
5. **Out-of-order notice loads:** an older asynchronous response could replace a later selection in the review UI. A request-generation guard prevents stale renders; a browser regression deliberately releases the old response last. Busy state makes action completion observable.

## Verification scopes

| Verification | Result | Actual scope |
| --- | --- | --- |
| Ordinary software regression | 2,266 passed; 1 skipped; 166 deselected | All pre-existing contracts plus new profile/sampling/continuation protections; model/browser markers separate |
| All browser workflows | 33 passed | 27 research + 6 authenticated customer tests |
| Final customer-only rerun | 6 passed | Includes genuine Java parsing and standards-derived ISO meeting input in the full learning journey |
| Actual Laya training | Completed | 160 TRAIN notices, 1,440 question items, 90 optimizer updates, one additional full-encoder epoch |
| Actual checkpoint reload | Passed, maximum native-score delta 0.0 | Two fresh official SDK loads of the new checkpoint on the recorded validation probe |
| Linux service | Passed on linux/arm64 | Rebuilt image, named authentication, non-root/read-only/capability-dropped service, import and real process-restart persistence; no model inference in this check |
| Real Laya + Qwen release | Completed; 3 real-model tests passed in 61.64 s | Current-source customer orchestrator on four development events, plus real durable worker execution/persisted decision/audit in an isolated database |

Browser model kernels are explicitly named doubles. The real customer APIs, reviews, split isolation, export, jobs, manifests, candidate selection, release sealing, calibration, frozen qualification, task queue, refusals and persistence execute unchanged. No fake model is counted as trained or accurate. The fixture refuses non-test environments.

The customer journey checks import → AI-labelled review → immutable TRAIN/VALIDATION/CALIBRATION/FROZEN_TEST roles → TRAIN/VALIDATION-only export → training → validation selection → freeze derivative → second training round → new release → calibration → predeclared independent qualification → refused promotion → reviewed inference → actual process restart. It also verifies blind holdouts, frozen-label protection, protected-input refusal, insufficient-support/null confidence, cancellation, persisted decision trace, exact source, audit integrity, search/filtering, invalid JSON, Prowide/scanner/text bypass and auditor access restrictions.

No test or semantic expectation was removed or weakened. Existing metric warnings remain reported. Authored challenge expectations are unchanged. Screenshot artifacts are smoke evidence, not pixel-perfect cross-platform baselines.

## What starting models actually exist

- **Foundation Laya:** pinned official multilingual checkpoint, revision `7b928d828b7b0e022f929d9bd2e44165aa270148`, SDK 0.4.8. Identity is frozen; general proxy-voting quality is not certified.
- **Previous domain Laya:** eight-epoch AI-authored controlled-composition adaptation. Its earlier 3,591/3,600 semantic assertions and 391/400 complete matches came from an English restriction-focused cohort with shared sentence atoms and one final-status truth. That is not broad notice generalisation.
- **New domain Laya candidate:** one further bounded adaptation using existing TRAIN data plus TRAIN-only replay; see exact comparison below. It is `AI_TEST_DERIVATIVE`, not a shipped foundation or production promotion.
- **Trainable Qwen:** pinned `mlx-community/Qwen3.8-27B-4bit` revision `10c35caafbb80f7dc6a7a432cdd11af10a6d4818`. Existing QLoRA checks establish optimizer/save/reload mechanics, not a domain-trained model-quality gain. The historical 92/95 authored result belongs to another Ollama/GGUF condition and is not inherited by MLX or Linux.
- **ISO15022:** Prowide extracts structured facts; Laya/Qwen classify narrative voting predicates. More ISO tag training is not a substitute for semantic coverage. The 7,683 public filing excerpts previously contained no recognised ISO structure.

## Actual model upgrade, without challenge tuning

`scripts/upgrade_domain_candidate.py` selected 128 TRAIN notices for field/class/family coverage from the existing development corpus and 32 disjoint TRAIN replay notices. Validation uses 120 notices from two held-out generation families. Both roles contain all three labels for every predicate. The replay overlap guard initially refused duplicated IDs before any optimizer execution; the corrected attempt explicitly excludes source-corpus IDs/hashes from replay. No failed attempt was overwritten.

Train: 160 notices / 1,440 predicate questions. Validation: 120 notices / 1,080 assertions. Parent: `customer-adaptation-uncontended-v1-8epoch`. One epoch; head LR 0.00005; encoder LR 0.0000125; micro-batch 8; accumulation 2; max length 2,048; seed 42; gradient checkpointing; MPS cap 0.45. Parent, rendered targets, training source and output hashes are retained. Calibration and test answers never entered training or validation selection.

| Same validation inputs | Correct assertions / 1,080 | Nine-field exact / 120 |
| --- | ---: | ---: |
| Foundation | 308/1080 (28.52%) | 0/120 (0.00%) |
| Previous domain checkpoint | 1025/1080 (94.91%) | 84/120 (70.00%) |
| New broader domain candidate | 1065/1080 (98.61%) | 106/120 (88.33%) |

The candidate repairs **40 validation assertion errors**, damages **0 previously correct assertions**, and leaves **15 errors**. It was selected solely on validation, subject to no new critical positive miss. No selected model was automatically promoted or supplied an old calibrator.

| Predicate | Positive support | Previous positive recall | New positive recall | New correct / 120 |
| --- | ---: | ---: | ---: | ---: |
| votability | 101 | 1.0000 | 1.0000 | 120/120 |
| share_blocking | 24 | 1.0000 | 1.0000 | 114/120 |
| poa_required | 31 | 1.0000 | 1.0000 | 118/120 |
| registration_required | 33 | 0.9697 | 1.0000 | 118/120 |
| beneficial_owner_disclosure_required | 30 | 1.0000 | 1.0000 | 119/120 |
| holding_confirmation_required | 36 | 0.8611 | 1.0000 | 119/120 |
| split_voting_restricted | 29 | 1.0000 | 1.0000 | 117/120 |
| securities_lending_recall_required | 29 | 1.0000 | 1.0000 | 120/120 |
| other_voting_restriction | 36 | 1.0000 | 1.0000 | 120/120 |

All reported positive classes were detected in this validation sample, but 15 non-positive/UNKNOWN errors remain. Full confusion matrices, per-class support, F1, raw scores, evidence and every error are persisted in `data/experiments/framework-domain-upgrade-20261022-v2/*/metrics.json` and predictions.

The selected candidate’s median request inference was **182.5 ms**, mean **208.3 ms**, p95 **522.9 ms**, minimum **94.0 ms**, maximum **585.4 ms** on the development Mac. These are 120 direct specialist requests; model loading/persistence are separately recorded. They are not calibrated-cascade, cloud or production-SLA timings.

**Limits:** validation has only two independent generation families despite 120 rows. This is a small AI-authored English development study, not an independent model qualification. Its apparent accuracy cannot choose an operational confidence threshold. No new confidence calibrator was fitted; numerical confidence for the new model remains unavailable. Parent calibration does not transfer.

## Fixed authored challenge — important generalisation blocker

The candidate and configuration were frozen before the separate post-selection challenge check. Both models saved predictions before scoring. Selection was not changed afterward.

| Same frozen authored challenge | Correct supplied assertions / 95 | Cases satisfying supplied assertions / 57 |
| --- | ---: | ---: |
| Previous domain checkpoint | 70/95 (73.68%) | 34/57 |
| New development-selected candidate | 71/95 (74.74%) | 35/57 |

Native model outputs, not just derived statuses, labelled all 57 notices VOTABLE. Among the 54 cases with votability truth, all 36 positives were recognised, but **0/15 NOT_VOTABLE and 0/3 UNCERTAIN** were recognised. Votability precision was 36/54; balanced accuracy was 1/3. Affirmative blocking and POA recall were each **2/3**, not the 100% observed in the development validation sample. This is an operational release blocker.

The scoring aliases and source-exact evidence wrapper were inspected: the wrapper preserves the native document label; it did not force this result. All underlying challenge votability predictions were VOTABLE. This is evidence of a formulation/data/generalisation weakness, not a newly identified evaluator or label-reduction bug. The development cohort's much longer, repetitive notice construction may be a contributor; no causal ablation was run.

The much larger validation gain therefore **does not establish broad generalisation**. The challenge gain is only one assertion and one case. More repeated epochs on similar templates are not justified as a production-readiness fix. The candidate remains experimental, outside the shipped foundation, and automation stays disabled. The 57 cases contain 95 supplied partial assertions and only four explicit final-status labels. Neither assertion accuracy nor case conjunction is customer accuracy or final-status accuracy over 57.

## Remaining readiness gaps and next work

1. A substantially larger family-held-out semantic qualification cohort, covering non-voting events, every restriction, UNKNOWN, contradictions, supersession, deadlines, languages and long notices. Preserve predictions before opening independent answers. The existing controlled study and this two-family validation pilot do not replace it.
2. Exact deployment-checkpoint qualification on Linux CPU/GPU, including pretrained Qwen training/inference and practical workload/cancellation/recovery tests. The rebuilt Linux service receipt verifies service mechanics only; Mac MLX results do not qualify Linux Transformers/CUDA.
3. New-model calibration with separately supported CALIBRATION groups, then validation-only operating selection and independent held-out qualification. No small-review or 100%-correctness threshold has been established for the new candidate.
4. Representative independently expert-labelled client data before customer automation. Successful promotion/production monitoring under real deployment conditions remains distinct from the tested AI-label refusal path.
5. Automatic random sampling of accepted decisions for review remains future engineering; low-confidence review and audit history already exist. This must not be advertised as delivered.
6. No qualified constrained-Qwen Gear 2 is added by this task; unsupported gears remain refused rather than represented as functioning production layers.

The immediate next model task is broader independent qualification of the frozen candidate, not simply more epochs or another model layer. Keep AI corpora, test-trained checkpoints and test calibrators outside the shipped product. Automation remains disabled until the deployment’s own gate passes.

## Reproducible evidence

- `artifacts/framework-upgrade-regression-2026-10-22.log`
- `artifacts/framework-upgrade-all-browser-2026-10-22.log`
- `artifacts/framework-customer-browser-upgrade-2026-10-22.log`
- `data/experiments/framework-domain-upgrade-20261022-v2/PLAN.json`, `result.json`, `SELECTION_FREEZE.json`, `REPAIR_DAMAGE.json`
- `data/experiments/framework-linux-service-20261022/receipt.json`
- `data/training-workspace/campaigns/framework-real-path-20261022/`
- `artifacts/framework-real-model-tests-2026-10-22.log`
- `docs/QUALIFICATION_TEST_SCOPE.md`, `docs/FROZEN_CHECKPOINT_LEARNING.md`

### Challenge predicate results (only explicitly labelled assertions)

| Predicate | Correct / labelled n | Positive support | Positive recall |
| --- | ---: | ---: | ---: |
| classification | 3/4 | 0 | N/A |
| votability | 36/54 | 36 | 1.0 |
| share_blocking | 10/11 | 3 | 0.6666666666666666 |
| poa_required | 6/8 | 3 | 0.6666666666666666 |
| deadline_status | 13/14 | 0 | N/A |
| other_restriction | 3/4 | 4 | 0.75 |

Challenge transition: 1 repairs, 0 damaged previously correct assertions, 24 wrong in both. Every failure and native score is in `CHALLENGE_SELECTED/metrics.json`; raw outputs and immutable selection are adjacent. No challenge failure was used for a subsequent training or routing change.
