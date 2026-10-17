# Classification and training framework

The product is the reusable workflow: source → optional ISO adapter → semantic
models → deterministic decision → review → versioned labels → isolated training
→ registered checkpoint → evaluation → calibration → explicit deployment choice.
An independently trained customer model is a later output of this framework.

AI-authored and AI-reviewed development labels are supported. They retain the
author/model/method/source/revision. They are never promoted to human or expert
gold. Synthetic and AI-labelled evaluation demonstrates workflow behaviour and
benchmark performance; customer accuracy remains unknown. Automation stays off.

## Data contract and reviews

`Example` stores untouched text/hash, duplicate group, generation family, split,
nine semantic predicates, exact-source evidence and provenance. Laya gets the
nine choice questions. The LLM gets the same predicates plus evidence and deadline
text in the production `SemanticResult` schema. Deadline comparison is software;
neither trainer learns the `OPEN`/`PASSED` calculation. Confidence percentages are
not training targets. Calibration remains a separate population-specific stage.

The existing complete-schema review endpoint `/api/domain/reviews` accepts
`label_origin`, `reviewer_model`, `evidence`, `deadline_mentioned`, `deadline_text`.
AI origins require a model identity and cannot attest human expertise. Exact
quotation checks happen before saving. Revisions remain append-only. Positive
labels without supporting evidence can be saved for further review but cannot
be exported for training. Correct them by adding a new revision.

```sh
# Only TRAIN and VALIDATION answers are opened. Original corpus is untouched.
.venv/bin/python -m training.framework export-corpus \
  data/domain-corpus/v4/MANIFEST.json \
  data/training-workspace/bundles/domain-development-v1 --language en

# Alternatively export latest complete reviews; test labels are not fetched.
.venv/bin/python -m training.framework export-reviews \
  data/training-workspace/bundles/reviewed-development-v1

.venv/bin/python -m training.framework capabilities
.venv/bin/python -m training.framework prepare \
  data/training-workspace/bundles/domain-development-v1 \
  training/framework/specs/laya.json \
  data/training-workspace/jobs/laya-development-v1

# Explicit execution, after benchmark workers finish. Never runs from GET/UI.
.venv/bin/python -m training.framework execute \
  data/training-workspace/jobs/laya-development-v1

.venv/bin/python -m training.framework evaluate-validation \
  data/training-workspace/jobs/laya-development-v1 \
  data/training-workspace/evaluations/laya-development-v1
```

Exports recompute exact/normalised/lexical near-duplicate isolation and enforce
source-group/family separation. Protected frozen, challenge, calibration and OOD
paths are rejected. Existing corpus semantic grouping is retained; lexical QC
does not independently guarantee semantic paraphrase isolation. The training
bundle contains no frozen/test file. Content is re-rendered and checked against
annotations before execution, in addition to checksums and counts.

## Training backends

* `LAYA_SDK`: official `laya.train.finetune`, explicit held-out validation, no
  internal random question-level calibration. All nine semantic heads are
  exported, so new specialist labels need not hide inside `other_restriction`.
* `TRANSFORMERS_PEFT`: offline causal-LM LoRA; masked assistant-JSON loss, fixed
  seed, validation token loss, loss curve, safetensors adapter, save/reload logit
  check. Qwen and GLM are model identities/configurations, not business logic.
  The exact checkpoint must be supported by the installed Transformers/PEFT and
  its chat template must preserve the masked prefix. Unsupported architectures
  fail explicitly. No `trust_remote_code`, automatic download or cloud API.
* `MLX_QLORA`: isolated Apple-Silicon quantised LoRA using the official MLX-LM
  trainer, exact Direct-prefix masking, adapter save/reload checks and native
  unified-memory allocation measurements. The pinned27B qualification and its
  measured limits are recorded in the checkpoint-qualification report below.

The optional PEFT dependency is separate from ordinary application inference:
install the pinned requirements in `requirements.txt` into a training environment
that also satisfies the project's locked dependencies. Do not mutate a timed
benchmark environment mid-run. Adapt `specs/qwen.json` or `specs/glm.json` to a
locally downloaded, revision-pinned **trainable** checkpoint. The installed Ollama
Q4 GGUF cannot be used directly for PEFT training. A specification is not proof
that a particular checkpoint was trained or is compatible. `preflight.ready`
means prerequisite checks passed; the actual trainer/reload smoke test is next.

Ordinary27B precision weights need more headroom than this Mac comfortably
provides. The MLX backend instead uses the pinned4-bit conversion of the same
model family. It is a different quantisation/runtime from the historical Ollama
benchmark; no historical accuracy is transferred. Use the explicit setup below;
application startup never downloads weights or begins training.

```sh
uv venv artifacts/mlx-training-venv --python .venv/bin/python
uv pip install --python artifacts/mlx-training-venv/bin/python \
  -r training/framework/requirements-mlx.lock.txt
.venv/bin/python -m scripts.setup_trainable_qwen
.venv/bin/python -m scripts.prepare_framework_qualification \
  data/training-workspace/bundles/ai-domain-development-v1 \
  data/training-workspace/bundles/my-qualification-v1
.venv/bin/python -m training.framework prepare \
  data/training-workspace/bundles/my-qualification-v1 \
  training/framework/specs/qwen38-mlx.json \
  data/training-workspace/jobs/my-qwen-qualification-v1
.venv/bin/python -m training.framework execute \
  data/training-workspace/jobs/my-qwen-qualification-v1
```

The example uses two optimizer steps for engineering qualification. It is not a
domain-training recommendation or learning-curve result. See
[exact checkpoint qualification](../../data/reports/QWEN_TRAINABLE_CHECKPOINT_QUALIFICATION.md).

## Reproducibility and deployment boundary

Preparation creates an immutable plan with dataset hash, source hashes, exact
base file hashes when prerequisites are available, model/revision, seed,
hyperparameters, package versions and hardware. Execution refuses active timed
benchmark workers and preserves RUNNING/FAILED/INTERRUPTED/COMPLETED events.
A completed model is registered `EXPERIMENTAL_NOT_PROMOTED` with artifact hashes.
It does not replace the application's model, change routing, enable automation,
or reuse another model's calibrator. Existing trained Laya/Qwen/GLM experiments
are retained.

Validation token loss is not predicate accuracy. Run the existing assertion-level
evaluation and repair/damage analysis with a checkpoint before promoting it;
freeze selection before opening frozen answers. Customer-quality and framework
execution gates are deliberately separate. Real expert labels can later replace
AI development labels without changing the data or job contracts.

`RegisteredModel` verifies the saved artifact/base lineage and reloads either
backend. `evaluate-validation` saves all predictions before scoring the nine
labelled semantic fields with the shared assertion evaluator, including critical
positive support/recall and confusion matrices. It accepts no answer-key path.
The initial trained Laya whole-notice runtime exposes native scores and marks
quotation evidence unavailable; a decision head is not an evidence extractor.
Use the application's separately evaluated passage/evidence layer when promoting
a specialist into the cascade. This CLI does not silently replace that layer.

The CLI executes jobs synchronously and logs its result. HTTP endpoints expose
status and job preparation. `TRAINED_CANDIDATES_ENABLED=true` separately enables
`POST /api/training/jobs/{id}/analyse`, accepting an existing `record_id` or raw
`text`, plus an explicit evaluation timestamp. This runs a registered candidate,
optionally parses ISO structure, persists its complete trace and retains manual
review. It does not replace the default classifier. The endpoint refuses an
active benchmark/training lease. A later review of an existing notice links to
this prediction; export creates a new dataset revision for learning.

Training code is archived with each new job. Training execution requires the
planned current code. Loading a historical checkpoint verifies its archived
lineage/artifacts without requiring the trainer's current source to be identical.
Distributed scheduling, automatic promotion and full optimizer-state resume
remain separate work. Exact GLM training has not been qualified by the Qwen run.

References checked 2026-10-17:
[PEFT LoRA API](https://huggingface.co/docs/peft/main/package_reference/lora),
[PEFT save/load](https://huggingface.co/docs/peft/main/developer_guides/peft_model),
[MLX LoRA/QLoRA](https://github.com/ml-explore/mlx-lm/blob/main/mlx_lm/LORA.md).
