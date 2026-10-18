# Client deployment gap assessment and implementation plan

Date: 2026-10-18. Target: single-tenant Linux Docker service. Qualification data in this phase: AI-authored, explicitly not independent expert labels.

## Confirmed starting state

Executable code provides actual official-SDK Laya training, Qwen MLX LoRA training, versioned bundles/jobs, same-input comparison, source-linked evidence, immutable event/review histories, model-specific calibration, frozen predictions before scoring, and experimental release selection/rollback. The latest real-model qualification used eight training and four validation events. All actual model confidence remains null because calibration support is insufficient. Historical challenge results are partial authored assertions, not customer accuracy.

The current application is a loopback single-operator research service. Its Dockerfile has no JVM and its customer-trained Qwen backend is qualified only on Apple Silicon. All final decisions require review. Importing an unlabelled corpus cannot establish supervised targets, reliable confidence, or a low human-review rate.

## Engineering work

| Gap | Implementation | Verification |
|---|---|---|
| Customer trust boundary | Separate production API, mandatory hashed named-user credentials, roles, same-origin writes, bounded requests, local-only dependencies | Authentication/authorization, spoofing, host/origin/body limits; Linux container smoke |
| Corpus onboarding | Bounded resumable bulk JSONL import; exact raw preservation, per-row receipts, provenance and client metadata | Malformed/idempotent import, collisions, split isolation, persistence |
| Independent review | Authenticated identities, blind held-out review, origin-preserving revisions, locked frozen snapshots | Reviewer spoof prevention, AI never expert, stale/frozen review rejection |
| Train/qualify lifecycle | Reuse actual versioned learning campaigns; explicit protected-data freeze, immutable qualification plans and receipts | Training exclusion, frozen immutability, plan/model/data hash binding |
| Customer confidence | Separate fit/evaluation calibration; serialisable model-specific predicate and final-decision correctness models; population/OOD scope | Support failure, known synthetic probabilities, held-out metrics, reload and mismatch rejection |
| Safe review routing | No numeric trust without supported calibration; exact evidence/conflict/unknown/scope gates; qualification required for automation | Fail-closed paths; no synthetic promotion; critical false-negative tests |
| Production acceptance | Predeclared thresholds; independent frozen scoring, group-aware conservative precision/recall bounds, review-rate target; expert/client-source gate | Small/perfect/synthetic samples fail, corrupted/stale certificates fail, controlled large fixtures exercise machinery |
| Operations/deployment | Pinned non-root Linux image with JVM and training dependencies; fixed paths, secrets, offline networking profile, readiness/metrics, backup/runbook | Actual build/container execution, parser and Laya inference, restart/persistence, regression suites |
| Customer workflow | Operational console for import/review/train/status/qualification and actual saved traces | Browser workflow, safe rendering and confidence labels |

## Acceptance limits

This phase can qualify software using controlled AI-labelled examples. Customer automation must remain disabled until a representative customer corpus has independently authenticated expert-labelled calibration and frozen-test support meeting the predeclared policy. A low review percentage is a measured acceptance condition, never a promised property of an architecture. Linux CUDA Qwen training and production-scale capacity require the client's actual GPU/hardware qualification; Mac MLX artifacts are not silently treated as portable Linux checkpoints.

Do not restart stopped studies, alter the frozen 57-case challenge, replace historical receipts, or claim a production classifier from this engineering exercise.
