# Reliable voting classifier and calibrated hybrid: execution plan

Version: reliability-programme-20261022-v1. Status: execution in progress.

## Product and acceptance boundary

Deliver a locally deployable, single-tenant learning/classification framework:
frozen starting model → customer training → validation-only selection → frozen
model/rules → separate stage and final calibration → independent qualification →
explicit monitored release → random audit and low-confidence review → new learning
round. AI qualification data, test-trained models and test calibrators remain
outside the product. Production customer accuracy remains unestablished until the
installation's independent client qualification passes; a sellable framework is
not a guarantee that arbitrary customer data yields a specified review rate.

Do not weaken existing quality/support gates to obtain percentages. Do not use
the 57 authored cases or old frozen answers to train, choose prompts or thresholds.
Keep automation disabled by default. Execute the following phases continuously;
ordinary experiment choices do not require a phase approval.

## 0. Freeze and verify model availability

Preserve the previous 71/95 candidate, foundation pins, all predictions, criteria,
sources and calibrators. Archive the initial regression status. Query official
Hugging Face model metadata, actual weight files, provenance, licence and local
runtime compatibility before any new model download. A repository name or a
Transformers architecture class is not evidence that weights have been released.

Initial live checks on 22 October 2026 find no official Qwen4 model repository.
The public `qwen4_exp` model is Qwen3.8-Flash-Next, an architecture preview, not a
released Qwen4-27B. Investigate wider Hub results and record unavailable conditions
explicitly. Never call an older or community model Qwen4. The existing pinned Qwen
may remain a separately named reference; the framework must admit a future verified
checkpoint without coupling business rules to its marketing name.

## 1. Diagnose formulation and data, before adding model layers

Measure true train/validation class and length support, unique groups and model
native scores. The previous sample had 138/160 VOTABLE training labels and only
11 NOT_VOTABLE / 11 UNCERTAIN. Votability represented only one of nine questions.
The 57-case finding is a diagnostic, not a source of new training paraphrases.

Add TRAIN-only, explicit task/class balancing where the official SDK supports
it, preserving actual unique-example counts and derived sampling provenance.
Keep the serving questions and label mapping fixed. Dates stay deterministic.

## 2. Build a new, disclosed fact-first qualification cohort

Author independent development material covering YES/NO/UNKNOWN, non-voting
corporate actions, mandatory/optional/waived conditions, negation, history,
supersession, contradictions, multiple conditions and short/medium/long notices.
Include clean narratives, operational messages and ISO adapters. Preserve exact
evidence, generator/version, original facts and source hashes.

Counterbalance label, length, layout and notice context. Deduplicate and group
variants before TRAIN / VALIDATION / STAGE_CALIBRATION / FINAL_CALIBRATION /
FROZEN_TEST assignment. Keep input-only files separate from held-out answers.
Report shared grammar/phrase-bank limitations; synthetic composition groups must
never be described as independently expert-labelled linguistic populations.

## 3. Run bounded specialist learning and freeze selection

Use official local Laya with unchanged criteria, genuine optimizer updates and
save/reload checks. Compare frozen parent with balanced full-encoder candidates.
Select on validation macro/balanced metrics, affirmative recall and new critical
false negatives, not aggregate accuracy alone. Preserve failed/rejected candidates.
Predeclare finite epoch/compute budgets and stop extensions at the validation
plateau/damage condition. Do not select on the authored challenge.

## 4. Implement and fit stage and final correctness calibration

Use actual model predictions. Keep specialist-routing calibration disjoint from
final-hybrid calibration. Fit correctness estimators on FIT groups, assess them
on EVALUATION groups and independently report frozen-test calibration.

Check engine/source, evidence mode, class, language, input type, length/domain and
source/prompt/checkpoint/routing identity. Unsupported conditions return null and
review. Laya native scores and token probabilities are features, not calibrated
confidence. A minimum of predicate probabilities is a trust score; final-decision
correctness requires a separate calibrator. Report Brier/ECE, reliability bins,
class support, false negatives and coverage/quality bounds.

## 5. Execute the selective hybrid comparison

Compare specialist-only, independent pinned LLM and a calibrated selective
specialist→LLM cascade on identical applicable inputs. If Qwen4 weights remain
unavailable, mark QWEN4 NOT_AVAILABLE and do not invent a benchmark. Keep any
existing-Qwen reference explicitly identified.

Choose routing on development/validation only. Persist exact evidence and model
disagreement. Neither model automatically wins. Measure repairs, damage, oracle
ceilings, calls avoided, review rate, end-to-end median/p95, throughput and memory.
Fit final confidence for the frozen cascade itself, not by reusing stage calibration.

## 6. Strengthen release monitoring and customer operation

Add deterministic, policy-versioned random sampling of otherwise accepted
decisions for human audit, with persisted inclusion probability and reason. Keep
audit reviews separate from low-confidence reviews; record observed error/review
rates and source/model/population drift. Verified accepted errors must suspend the
qualification. Reviewed examples may enter a later training round only through
new versioned splits; protected qualification data cannot silently become training.

Make the GUI expose actual confidence scope/support, engine identity, cascade
decisions, model availability and qualification blockers. Preserve the complete
customer workflow and avoid a visual redesign.

## 7. Independent qualification, deployment and regression

Freeze every selected artifact before protected scoring. Persist predictions
before opening keys; list every error. Re-run the unchanged authored challenge
once after selection, explicitly using its 95-assertion/57-case denominators.

Run ordinary, browser, real-local-model and learning/reload tests, including two
customer learning rounds, confidence persistence, audit sampling and failure paths.
Rebuild/test the Linux service, restart/restore, authentication, resource controls
and local-only data path. Record actual deployment/platform limits; Mac MLX is not
Linux CUDA qualification. Verify source delivery excludes data and learned test weights.

## Deliverables and final decision

- `MODEL_AVAILABILITY_QWEN4.md`: live publisher/weight/runtime evidence.
- New versioned corpus, QC, split manifest, training/selection and frozen receipts.
- Model- and cascade-specific calibrated confidence artifacts and curves.
- `RELIABLE_CLASSIFIER_EVALUATION.md`: all measured results, critical errors,
  repair/damage, latency, review/coverage and unpassed gates.
- Executable customer qualification, audited review and learning workflows.
- Regression, browser, real-model and Linux acceptance receipts; clean source handoff.

Completion means engineering evidence and supported qualification, not relabelling
AI results as production customer accuracy. Any unavailable model, failed semantic
gate, unsupported confidence condition or unqualified hardware remains an explicit
release blocker. Negative outcomes are preserved; no automatic production promotion.
