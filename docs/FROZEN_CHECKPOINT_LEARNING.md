# Frozen checkpoints and customer learning

The delivered product is the learning, inference, confidence and review framework.
Customer notices, labels, optimizer state and customer-trained models live in a
separate writable customer workspace. They are not part of the source release or
Docker image. The AI qualification corpus and its trained adapters are also
excluded. The model volume is mounted read-only during service operation.

The current Qwen choice and the distinct optimized serving candidate are
documented in [Local model selection](LOCAL_MODEL_SELECTION.md). A faster
quantisation/runtime/profile does not inherit another release's calibration.

## Installation and starting state

Use `docs/CLIENT_LINUX_DEPLOYMENT.md` for the authenticated single-tenant service.
A prepared foundation release can run with `review_only_unsealed: true` in an
INFERENCE task to bootstrap AI suggestions before customer validation. It always
requires review and cannot attach qualification/calibration. This is distinct
from a sealed operational release.

First install the appropriate revision-pinned model artifacts using the existing
setup scripts. Inference never downloads weights. The Apple Silicon qualification
uses the official Laya SDK and the pinned MLX conversion of Qwen. An MLX artifact
is not a Linux CUDA artifact; qualify the exact Linux/Transformers artifact before
claiming its measured model accuracy, memory use or latency there.

Freeze a dataset-free starting checkpoint:

```sh
.venv/bin/python -m training.framework freeze-starting-checkpoint \
  training/framework/specs/laya.json \
  data/training-workspace/seeds/laya-foundation-v1
.venv/bin/python -m training.framework freeze-starting-checkpoint \
  training/framework/specs/qwen38-mlx.json \
  data/training-workspace/seeds/qwen-foundation-v1
.venv/bin/python -m training.framework verify-starting-checkpoint \
  data/training-workspace/seeds/laya-foundation-v1
```

Each seed includes exact model-file hashes, revision, quantisation/runtime
configuration, generation parameters, semantic prompt and all nine Laya question
definitions. It contains no training dataset, labels or optimizer state. A model
can serve directly from the seed without fabricating a training job. A source
package contains code and installation recipes, not the large model weights.

`training.framework.seeds.bind` explicitly relocates verified model files using
an installation-local binding. Hashes and the frozen semantic identity remain
unchanged. Changing weights, criteria, prompt or generation settings requires a
new seed and release identity. Identity freezing is not an accuracy certificate.

## Customer corpus and further learning

Import the customer's raw messages, construct event state, review the operative
event, then freeze group-isolated TRAIN, VALIDATION, CALIBRATION and FROZEN_TEST
roles through the customer console. Preserve old messages and review revisions.
AI-labelled reviews remain AI-labelled. The roles and expert attestation do not
change when a model performs well on synthetic examples.

Export a TRAIN/VALIDATION bundle. Prepare a new training job from a seed:

```sh
.venv/bin/python -m training.framework prepare-from-checkpoint \
  data/training-workspace/seeds/laya-foundation-v1 \
  data/training-workspace/bundles/customer-v1 \
  customer-laya-overrides.json \
  data/training-workspace/jobs/customer-laya-v1
.venv/bin/python -m training.framework execute \
  data/training-workspace/jobs/customer-laya-v1
```

An example overrides file is:

```json
{"epochs": 4, "learning_rate": 0.0001,
 "encoder_learning_rate": 0.000025, "freeze_encoder": false,
 "batch_size": 2, "gradient_accumulation": 8, "max_length": 2048,
 "laya_gradient_checkpointing": true, "laya_sdk_validation": false,
 "mps_memory_fraction": 0.45}
```

These values define a development candidate, not guaranteed optimal settings.
The MPS-only memory cap is omitted for CPU/CUDA configurations. The smaller
micro-batch and gradient checkpointing limit activation pressure. Disabling the
SDK's duplicate pre/post diagnostic does not waive validation: the customer
campaign independently scores every validation notice before sealing a release.
Use validation-only fixed experiments to compare head-only versus encoder
updates, training budgets, seeds and question formulations. The original
eight-event qualification was not sufficient to conclude that Laya cannot learn.
Preflight now reports per-predicate, per-class example and group support in both
development roles. Absent classes and fewer than five training groups produce
explicit diagnostics; five is a warning threshold, not proof of sufficient
training. More epochs cannot replace missing supervision or linguistic diversity.
The SDK supports separate encoder/head learning rates; the framework now exposes
them separately. Official SDK reference:
https://nandhakishorm.github.io/laya/reference/train/ (retrieved 2026-10-18).

Train Qwen with the same command and its frozen checkpoint. MLX QLoRA and
Transformers PEFT support loading an existing frozen adapter with a **new**
optimizer. Adapter architecture must match for MLX continuation. Laya loads its
full frozen starting weights. Parent identity and bytes are checked again at
execution. Dataset roles, source hashes, revisions and reload checks remain
mandatory. New models do not inherit the parent's calibrator.

The small `qwen38-mlx.json` step count is an integration smoke configuration.
Set `max_steps`, adapter architecture and `training_timeout_seconds` explicitly
for a customer experiment; the default subprocess budget is two hours and the
validated upper limit is seven days. The enclosing campaign's `max_seconds`
must also cover training plus validation. A short smoke run demonstrates
optimizer/checkpoint mechanics; it does not demonstrate a domain-quality gain.

Named candidate recipes now live beside those smoke configurations:

| Recipe | Purpose | Budget |
| --- | --- | --- |
| `laya-domain-cpu.json` | Linux CPU domain candidate | 4 full-encoder epochs, separate head/encoder learning rates |
| `laya-domain-mps.json` | Development Mac domain candidate | 4 full-encoder epochs, MPS activation/memory controls |
| `qwen38-domain-mlx.json` | Development Mac domain candidate | 200 optimizer steps, 4 LoRA layers, rank 8 |

These are bounded experiment recipes, not measured optimal training settings or
pretrained voting models. Adapt batch/context/budget to the installed hardware
and validation results. Keep a frozen parent's identity by supplying only tunable
overrides to `prepare-from-checkpoint`; do not replace parent paths/digests with
the paths from an unrelated profile. Linux customer consoles offer only compatible
Linux recipes. Exact Qwen/GLM Linux GPU checkpoint training remains separately qualified.

The starting-checkpoint API/UI now explicitly reports foundation-only,
AI-test-derivative or customer-derivative readiness. A supplied quality receipt
does not pass the independent deployment gate. ISO15022 structure is parsed by
Prowide; the semantic model learns voting predicates from the routed narrative.
There is currently no broadly independently qualified "ISO15022 voting model".

Use `seeds.export_derivative` to make a new dataset-free starting checkpoint
from a completed registered job. It preserves frozen criteria and hash-only
training lineage. AI-trained test models are `AI_TEST_DERIVATIVE`; they cannot
be relabelled `OFFICIAL_FOUNDATION` or customer-qualified derivatives.

The authenticated customer console also provides **Freeze a completed training
checkpoint for the next learning round** (`POST /api/client/starting-checkpoints/from-job`).
Supply the completed registered job ID and a new immutable seed ID. The server
derives label origin from the job manifest; the caller cannot declare foundation
or expert status. Prepare the next campaign from that seed with a fresh optimizer.
The customer API accepts an initial base in the managed model volume or the
exact checkpoint of a completed managed job whose frozen derivative identity,
weight hashes and lineage match. Arbitrary workspace paths and forged lineage
are refused. The parent bytes stay unchanged. Recalibrate and requalify every
selected derivative before deployment; qualification never transfers from a parent.

## Match training and inference

Whole-notice training can be served using
`WHOLE_NOTICE_WITH_PASSAGE_EVIDENCE` (native sentence scoring) or
`WHOLE_NOTICE_SCOPED_EVIDENCE` (one document inference and deterministic candidate lookup). The document prediction is retained;
sentence scoring locates exact candidate evidence without replacing that
prediction. The historical `PASSAGES` restriction reducer remains available as
a separate condition. Select between them on validation, not challenge answers.

Neither sentence agreement nor an exact quote alone proves semantic entailment.
Contradictions, unknown critical facts, unverified evidence, unsupported input
populations and context truncation still require review.

## Confidence and the operating point

1. Select the model/criteria/routing using VALIDATION.
2. Execute that fixed model on CALIBRATION inputs and persist predictions before
   loading calibration answers.
3. Fit the correctness estimator on whole-group FIT folds; evaluate on disjoint
   whole-group EVALUATION folds. Default support requires at least 100 FIT and
   50 EVALUATION groups per predicate. Report Brier, ECE and class-conditioned
   correctness. Numerical confidence is unavailable for unseen prediction
   classes, input types, languages or insufficient support.
4. Use fixed L2 logistic calibration when correct and wrong outcomes have enough
   support. Otherwise a disclosed Laplace-smoothed constant estimates the
   population rate. It has no per-example discrimination. Do not invent errors
   to fit a classifier. A perfect small sample never becomes confidence 1.0.
5. Select an operating threshold on VALIDATION using confidence coverage,
   complete-output correctness, critical false negatives and simultaneous
   one-sided exact bounds across candidate thresholds. Zero supported operating
   points is a valid result; the review rate is then 100%.
6. Freeze the complete configuration, calibrator and operating threshold before
   evaluating protected FROZEN_TEST. Never select the best threshold on that
   test. Report every error and critical-positive support/recall.

The frozen operating-point receipt separately says whether its independent
benchmark gate passed. A validation-supported point can fail that test. Neither
verdict replaces the customer expert-label/population/promotion gate.

`production.operating` implements this selection/evaluation boundary. Final
decision correctness has its own calibrator. A minimum of predicate confidence
values is a conservative routing score, not a calibrated joint probability.
The client qualification protocol separately verifies all requested fields,
final status, deadlines, evidence and critical recall with grouped exact bounds.

The customer console can display scoped confidence before production promotion:
an INFERENCE task may supply a managed `calibrator_id` and
`simulation_threshold`. It records **would accept / would review**, while the
real decision stays in review. A calibration artifact grants no automation
permission. The GUI identifies the population and exposes calibration reports.

An explicit negative quote and a complete-input negative are different evidence
conditions. For NO predictions, the runtime can retain a source-hashed
`MODEL_NEGATIVE_AFTER_COMPLETE_SOURCE_V1` basis. This is a model judgement after
reading the complete input, not a quotation or a software proof that a requirement
is absent. It cannot be used for YES, truncated input or a different source hash.
Calibration must independently support the prediction/evidence-mode/input-type/
language stratum before that basis can support a confidence decision. Positive
requirements continue to need verified source quotations. This avoids forcing
all unmentioned negative attributes into review while preserving abstention when
that form of negative evidence has not been qualified.

For a calibrated Laya→Qwen cascade, first validate a `LAYA_ONLY` release and run
CALIBRATION with `stage: "LAYA"`. Select its operating point through
`POST /api/client/operating-points/{id}` using that campaign's saved validation
predictions. Prepare the cascade with the same specialist artifact/aggregation/
inference settings, `laya_calibrator_id` and `laya_operating_point_id`. Stage
identity is independent of which LLM is added but changes if specialist weights,
criteria, runtime or aggregation change. No supported operating point means
escalation, even when raw Laya scores are high. The resulting reconciled cascade
still needs its own FINAL calibration and independent customer qualification.

New event-dataset freezes physically partition CALIBRATION into `LAYA_STAGE`
and `CASCADE_FINAL`, preserving connected duplicate/generation groups. Each
partition has a separate private answer file. The stage calibrator reads only
`LAYA_STAGE`; the resulting cascade's FINAL calibrator reads only
`CASCADE_FINAL`. Both partitions separately need enough FIT/EVALUATION support.
The aggregate calibration file is available only to a standalone final model.
Legacy datasets without these partitions need an explicit new curation freeze;
they cannot silently reuse stage evaluation outcomes to validate the cascade.
The stage and final calibrator must identify the same dataset manifest.

Correctness calibration version `customer-correctness-v4` also separates
prediction strata by engine/source. Final-decision strata distinguish a
specialist-only path from a path that invoked an LLM. Earlier calibrators are
rejected: refit after upgrading; changing a version string does not migrate one.
Unsupported source/class/evidence/language strata return null rather than
borrowing confidence from another engine. Complete-source negative evidence
may support `NOT_VOTABLE`, as well as restriction `NO`, only when the original
input hash, complete processing and model identity are verified. It is never
shown as an invented quotation.

Campaign candidates accept `laya_calibrator_id` and `laya_operating_point_id`
alongside `laya_inference`; these immutable artifacts are included in release
identity and checked again at inference. A customer may first run a specialist
campaign, fit its stage calibrator, select a validation operating point, and
then prepare the calibrated cascade campaign. A zero-coverage result remains
usable: it sends all relevant notices to the generative model/review instead of
relaxing the gate silently.

## Production activation and updates

`AUTOMATION_ENABLED=false` remains the shipped default. A customer deployment
can activate operational automation only after its independently reviewed real
population passes the existing predeclared qualification gate and an independent
administrator promotes the release. No AI qualification artifact grants that
permission. Source/model/prompt/calibrator/population mismatches fail closed.

Promote and roll back complete releases, never just weights. Collect later human
corrections as revisioned new labels. Verified auto-processing errors suspend the
qualification. Customer retraining uses a newly frozen corpus/version, repeats
validation/calibration and requires a new independent quality evaluation.

The frozen qualification policy includes `random_audit_rate` (default 2%,
configurable 1–50%). A local secret deterministically samples otherwise accepted
decisions independently of confidence. Selected decisions require human review
with `RANDOM_ACCEPTED_DECISION_AUDIT`; receipts retain the original eligibility,
inclusion probability and version. Sampling neither enables automation nor
removes low-confidence review. The installation key lives in the private
workspace and survives restart. Keep it with protected workspace backups.
The qualification review-rate budget includes the expected audit load:
confidence-review rate + accepted fraction × audit rate. Reports distinguish
that expectation from measured low-confidence and realised audit counts.

An authenticated human correction of a randomly audited error suspends the
qualification exactly as a later error found in an auto-released case would.
Semantic fields are compared against the original snapshot. Deadline/final-status
comparisons additionally require the original evaluation time, so elapsed time
does not falsely become a model error. The review form pre-fills the saved
evaluation time. AI-authored labels cannot trigger an expert verification claim.

## Task balance for specialist training

`TrainSpec.laya_task_multipliers` accepts known predicate names and integer
multipliers 1–8. For example `{"votability":4}` keeps the original nine-question
TRAIN row and adds three single-votability-question rows. This uses the official
Laya SDK without modifying its loss or label mapping. Unique notice counts,
effective question counts, input hashes and the derived TRAIN-only sampling file
are recorded. Validation/calibration/test data is never resampled. Inspect class
and length support before adding epochs; optimizer updates cannot compensate for
missing supervision or prove generalisation to a new customer population.

The official SDK can rewrite tokenizer compatibility metadata during loading.
Training now passes a private `laya-sdk-working-base` copy to the SDK; inference
uses a temporary private model view and removes it on close. Files are copied,
never hard-linked into frozen weights or shared Hugging Face blobs. The outer
base-file hash check remains mandatory. This was verified against the actual
SDK tokenizer rewrite. A failed base-integrity check still quarantines the job;
it is never converted into a successful job by changing a manifest hash.

Customer campaigns enforce both their overall wall-clock budget and each
training stage's `training_timeout_seconds`. Timeout/cancellation interrupts the
owned child process group, preserves the job/log, and leaves partial artifacts
outside serving. The isolated tests exercise this wait with real harmless child
processes. The low-level research CLI should be run under an explicit supervisor
when a wall budget is required.

## Qualification artifacts versus delivery

`scripts/package_learning_source.py` excludes customer/test corpora, model
weights, adapters, private keys, databases and experiment artifacts. Keep the
generated qualification results in a separate evidence archive. The Docker
build has the same data/model exclusion boundary. Installation requires the
explicitly provisioned model volume and a fresh customer workspace.

On a clean source checkout, recreate the deterministic parser-only test fixtures
before running the software suite:

```sh
python -m hybrid.corpus
python -m scripts.expand_iso_fixtures
python -m pytest -m 'not e2e and not model and not local_llm and not qwen_local'
```

These commands generate standards-derived parser fixtures, not semantic training
data. The small Apache-2.0 Prowide reference example is a static test fixture.
Historical experiment-integrity checks skip when their optional evidence store
is absent. No test-trained weights or customer corpus is needed for the ordinary
software suite. Docker creates its own installation source Git snapshot; a
manual source installation should likewise initialise a Git checkout before
preparing registered jobs, so their source revision is recorded.

## Decision uncertainty and repaired output

Rule version `semantic-decision-3` reports whether the semantic decision is
unresolved. It does not invent a synthetic/customer origin and cannot grant
automation. The persisted customer decision separately records review and
release permission; an unqualified deployment stays review-only even when the
semantic status is clear. Earlier blanket-review unit assertions were replaced
with this separation and retained worker-level refusal tests; challenge answers
were unchanged.

A generative schema repair remains review-only in the current production policy.
Its repair count enters both predicate/final features, and repaired paths have a
separate calibration source stratum. Direct-output confidence is never borrowed
for repaired output. Relaxing this rule would require a new qualified condition.

Existing MLX serving requests are compared after typed default normalisation.
Adding an empty Laya-only training field does not invalidate identical effective
LLM settings. Changes to generation settings, checkpoint or unknown fields still
fail closed; the original request file is not rewritten.
