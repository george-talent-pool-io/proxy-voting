# Qwen trainable-checkpoint qualification

2026-10-17. This is an engineering qualification, not domain-quality or customer
accuracy evidence. Training, save/reload and semantic validation completed. The real application
persistence check also completed. Engineering qualification: **PASS**.

## Exact model and runtime

* Trainable artifact: `mlx-community/Qwen3.8-27B-4bit`, revision
  `10c35caafbb80f7dc6a7a432cdd11af10a6d4818`, Apache-2.0.
* Published base lineage: `Qwen/Qwen3.8-27B`, a27B model with the Qwen3.5
  architecture. The official repository currently resolves to
  `1d4bf0f2ff6012fd82039f2fa52739d0dd7c60c0`.
* The conversion card declares its base repository but does not pin the original
  conversion's base commit. That relationship is publisher provenance, not a
  byte-level proof of identical weights to the historical Ollama condition.
* Quantisation is the MLX affine4-bit representation from that pinned repository,
  not Ollama's Q4_K_M. The historical GGUF, prompt, scores and experiments remain
  unchanged. No92/95 result is transferred to this new runtime/quantisation.
* Three safetensors shards:16,054,541,349bytes. Complete downloaded repository
  including tokenizer/configuration is approximately16.08GB. No second model was
  downloaded for this qualification.
* Isolated MLX0.32.4, MLX-LM0.32.2, Transformers5.20.1 environment. Application
  inference dependencies were not replaced. Exact environment freeze is retained.
* Hardware: Apple M3Max,64GiB unified memory. All notice inference and training
  remain local. Network use downloaded public weights/packages only.

## Dataset and protocol

`qualification-v1`:12TRAIN and4VALIDATION notices, all AI_AUTHORED, selected from
the existing development bundle. Selection uses development field/class coverage
and shorter complete notices (<=1,600characters). Group/family/duplicate isolation
is retained. No challenge, frozen, calibration, adversarial or OOD answers were
opened. It is deliberately too small for a model-quality conclusion.

All nine semantic predicates are trained. Deadline text/evidence retain the
production schema; elapsed-deadline comparison stays deterministic. No confidence
number or reasoning explanation is trained. The exact current Direct serving
prefix is used. Actual encoded lengths:1,933–2,416tokens for training and
1,940–2,369for validation, below the declared8,192-token limit, without truncation.

Two optimizer updates; micro-batch1; accumulation1; seed42; learning rate5e-5;
LoRA rank4, scale2 (alpha8/rank4); last decoder layer's attention Q/V projections.
The base is frozen. This minimal adapter tests training plumbing, not whether
two steps suffice to adapt this domain.

## Engineering defects found before training

1. **Direct chat-prefix mismatch.** Qwen emits an empty thinking block in the
   generation prefix but not in its complete training-chat rendering. The generic
   trainer rejected the mismatch. A specific renderer now concatenates the exact
   Direct prefix, assistant JSON and EOS, masking the prefix. Unrecognised
   mismatching templates still fail. A regression test protects this behaviour.
2. **Virtual-environment interpreter symlink.** Resolving `venv/bin/python` to its
   filesystem target bypassed the isolated environment. The first versioned
   preflight failed explicitly. The launcher now preserves the venv executable
   path; a new job was prepared and its preflight passed. Failed/prepared artifacts
   were retained instead of overwritten.

The original timed benchmark was checkpointed at a completed-record boundary:
80Laya,19constrained-Qwen and19full-Qwen validation predictions retained. Its
isolated model was unloaded; the normal user Ollama service was untouched.
The common stop handler labels this boundary `STOPPED_BY_USER`; the operation
receipt records that it was a supervisor checkpoint for this authorised task.
The benchmark is to be resumed after exclusive training/application checks.

## Application and learning boundary

Registered checkpoints now load through a common model interface. MLX is isolated
behind a persistent local stdin/stdout JSONL worker. Prowide/recovery feeds useful
facts; ordinary notices bypass Java. Authoritative structure is retained and
semantic conflicts are visible. Deterministic rules derive deadlines/status.

An opt-in candidate endpoint persists complete source/hash, model identity,
parser, semantic results, exact verified evidence, rule result and review state.
Notice Detail can display the saved trace. A subsequent AI/human review links to
that prediction, and existing isolated exports can form a new training version.
Pages do not train a model or automatically promote an adapter. Candidate
execution and automation remain disabled by default; confidence remains null.

## Sources

Retrieved2026-10-17:

* [Official model card](https://huggingface.co/Qwen/Qwen3.8-27B).
* [Pinned MLX conversion](https://huggingface.co/mlx-community/Qwen3.8-27B-4bit/tree/10c35caafbb80f7dc6a7a432cdd11af10a6d4818).
* [MLX-LM LoRA/QLoRA guide](https://github.com/ml-explore/mlx-lm/blob/v0.32.2/mlx_lm/LORA.md).
* [Official MLX-LM trainer implementation](https://github.com/ml-explore/mlx-lm/blob/v0.32.2/mlx_lm/tuner/trainer.py).


## Measured training and semantic results

| Check | Official Laya SDK | Qwen3.8-27B MLX QLoRA |
|---|---:|---:|
| Eligible training notices | 12 | 12 |
| Validation notices | 4 | 4 |
| Actual training budget | 108 question items, one epoch | 2 micro-batches / optimizer updates |
| Adapter/head training | Frozen encoder; official SDK scorer update | 94,208 trainable adapter parameters |
| Save/reload probe maximum delta | 0.0 native-score difference | 0.0 logit difference |
| Semantic assertions correct | 10 / 36 | 36 / 36 |
| All-nine-field exact match | 0 / 4 | 4 / 4 |
| Median warm validation call | 128.6 ms | 27,716.9 ms |
| P95 warm validation call | 199.5 ms | 29,499.0 ms |
| Explicit final-status truth | 0 cases | 0 cases |

Qwen's two updates used two sampled micro-batches, not a full pass through all12
eligible notices. The dataset manifest lists the eligible cohort. The official
trainer and seed determine the sampling order. This is a deliberately small
execution check, not a recommendation for domain-training duration.

Qwen training/save/reload took381.67seconds, including a3.14-second model load,
validation passes and the reload probe. Peak MLX allocation through the training
stage was23,374,963,050bytes (23.37GB decimal). This is model-runtime allocation,
not total Mac unified-memory occupancy. Warm semantic-call times exclude model
load and artifact hashing; four observations do not establish a latency SLA.

Qwen teacher-forced validation JSON-token cross-entropy changed0.156223→0.155460.
Laya SDK validation loss changed2.0040→1.6895 while supplied-assertion correctness
remained10/36. No accuracy-improvement claim follows from either loss change.

### Per-predicate correctness / positive recall

| Predicate | Laya correct /4 | Qwen correct /4 | Positive support | Laya positive recall | Qwen positive recall |
|---|---:|---:|---:|---:|---:|
| Votability | 2 | 4 | 3 | 1/3 | 3/3 |
| Share blocking | 0 | 4 | 0 | N/A | N/A |
| POA | 2 | 4 | 1 | 1/1 | 1/1 |
| Registration | 1 | 4 | 1 | 1/1 | 1/1 |
| Beneficial-owner disclosure | 1 | 4 | 1 | 1/1 | 1/1 |
| Holding confirmation | 1 | 4 | 1 | 1/1 | 1/1 |
| Split-voting restriction | 1 | 4 | 1 | 1/1 | 1/1 |
| Securities-lending recall | 1 | 4 | 1 | 1/1 | 1/1 |
| Other restriction | 1 | 4 | 1 | 1/1 | 1/1 |

Single-positive supports and zero blocking-positive support are deliberately
visible. There is no calibrated confidence or customer-accuracy estimate. Laya's
26 missed assertions remain in the saved validation metrics/failure list. Its
whole-notice runtime does not invent quotation evidence for its decision head.
The model is not promoted. These new nine-predicate candidates are distinct from
historical legacy/challenge architectures and must not replace their results.

Detailed confusion matrices and failures:
[ Laya validation ](../training-workspace/evaluations/laya-qualification-v1/metrics.json),
[ Qwen validation ](../training-workspace/evaluations/qwen38-mlx-qualification-v2/metrics.json).

Both checkpoints are registered EXPERIMENTAL_NOT_PROMOTED, with immutable dataset,
source, base-model and artifact hashes. No frozen/challenge answer was used. No
calibrator was fitted on these four cases or borrowed from another model.


## Real application verification and remaining boundaries

Both registered candidates executed through a temporary local FastAPI instance
on a clearly labelled STANDARDS_DERIVED_SYNTHETIC MT564 fixture. Prowide parsed
its structure; the complete raw source, semantic results, structured facts,
verified evidence, deterministic rules, model hashes and manual-review state
were persisted. The server was restarted and both saved executions were read
back identically. This verifies execution/persistence, not business accuracy.

The initial Qwen application probe returned its JSON inside a Markdown fence.
Strict raw JSON validation failed and the result was retained as manual review;
that original execution remains in the immutable audit table. Runtime revision2
accepts only an exact whole-response JSON fence wrapper, then validates the
unchanged JSON against the same schema. Unrecognised prose is not stripped.
One bounded local format-repair attempt is available if schema validation still
fails; its version/attempt/result are recorded. Repeated failure remains review.

The rerun produced the same raw-output SHA256 as the first probe. Removing its
wrapper made the schema valid; **zero additional repair-model calls were used**.
`first_pass_success` in this runtime means usable schema after the explicitly
recorded wrapper normalisation; it must not be read as native raw-JSON success.
No hidden/unvalidated reasoning text is persisted. The report does not infer
broad reproducibility from one identical-output pair.

The final Qwen decision remained UNCERTAIN_MANUAL_REVIEW for a semantic reason:
the source says the receiving agent has not established whether blocking is
required. The ambiguity is visible. Laya produced VOTABLE_WITH_RESTRICTION;
that is an observed output, not an independently verified final-status score.
Cold API request wall times in the rerun were5.48seconds (Laya) and49.02seconds
(Qwen), including artifact verification, process/model load and parsing. These
must not be compared with the warm semantic-call timings above as if equivalent.

The main application was refreshed with persisted data retained. Registered
candidate execution remains disabled by default; the saved traces remain
inspectable in Model Lab. Existing notices/golden labels/default classification
architecture were not replaced. All automation remains disabled.

Verification: **2,150 ordinary regression tests passed**, one optional real CPU
smoke test skipped and156 model/browser cases deselected in that command;
**25 browser tests passed** separately; **9 focused schema/runtime contracts
passed**. Real27B Qwen and official Laya execution is demonstrated by the
training, reload, semantic-evaluation and API receipts, not by mocks. The earlier
suite failure was a unit test sharing the live resource-lease directory; it now
uses an isolated workspace. No semantic expectation was relaxed.

The original cascade benchmark was resumed from its preserved80/19/19 row
checkpoint after qualification. Frozen protocol/source/weight checks passed.
Its original JSONL prefixes are recorded in the resume receipt. The separate
previously user-stopped Qwen domain study remains stopped.

[Complete machine-readable qualification results](FRAMEWORK_QUALIFICATION_RESULTS.json).

## Next step toward the product

Implement the [event-level ISO15022 learning loop](ISO15022_LEARNING_FRAMEWORK_NEXT_STEP.md):
versioned linked-message ingestion → current event state → registered model →
AI/human review revision → new isolated training version → real jobs → independent
comparison/calibration → explicit experimental selection/rollback. The legacy
event ledger still needs the Prowide adapter boundary; ad-hoc ISO samples need
an event-level annotation/export path. Job launch/resume and candidate selection
remain CLI/experimental operations rather than one complete GUI lifecycle.

AI-labelled controlled fixtures can qualify this workflow. Independent customer
expert labels are a later requirement for customer accuracy, not a blocker to
framework engineering. This task does not establish domain-tuning efficacy,
real-world calibration, safe automation, full SWIFT business validation or
production readiness. GLM's exact trainable checkpoint is not qualified by this
Qwen result.
