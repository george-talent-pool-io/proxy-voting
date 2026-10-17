# Next engineering milestone: trainable cascade release campaigns

The event-level review/train/compare/select loop is implemented. The next step
should connect its registered artifacts to the existing selective cascade and
make repeatable learning campaigns a first-class operation. It should not be
another GUI redesign or an unbounded whole-corpus model run.

## Deliver one concrete release lifecycle

1. Import an event chain and append AI_REVIEWED corrections, retaining exact
   operative-message evidence and the earlier predictions. Export a new version.
2. Submit a predefined campaign containing an unchanged baseline, bounded Laya
   stages and bounded Qwen adapter stages. Use TRAIN/VALIDATION only. The existing
   durable worker records dependencies, cancellation and explicit new attempts.
3. Evaluate the same validation inputs, including critical false negatives,
   evidence availability, schema failures, repair/damage and latency. A model
   that damages important answers remains visible; it is not automatically chosen.
4. Bind a **release manifest** to exact Laya artifact, Qwen base/adapter, semantic
   schema/prompt, passage aggregation, parser/event policy, rule version, routing
   configuration and separate model-specific calibrators. Reject identity mismatch.
5. Collect adequate CALIBRATION support in family-isolated fit/evaluation folds.
   Exercise both correct and incorrect predictions; keep confidence null where
   support/reliability is insufficient. Synthetic calibration is scoped to its
   construction population, not customer correctness probability.
6. Freeze release selection before protected scoring. Run the common evaluation
   and per-stage repair/damage on frozen events. Never use these outcomes to tune
   the same release's routing or thresholds. Open a new development campaign if
   further changes are justified.
7. Support Laya-only and Qwen-only releases through the same manifest; do not
   assume the cascade wins. Execute the registered **Laya → selected Qwen → review** release against the
   original event through the application. Persist both model stages, escalation,
   reconciliation, source links and confidence identities. Roll back the complete
   release, including routing/calibration, rather than only switching a checkpoint.

## Why this follows the completed work

Current experimental selection runs a single registered candidate against an
event. The existing three-gear cascade remains a separate experiment using its
own frozen artifacts. They should share a release/configuration boundary before
claiming a trained end-to-end cascade. Laya's registered whole-notice head also
needs evidence-aware passage inference connected to the learned artifact; its
current evidence-unavailable state is correctly visible.

The new small qualification cohort is deliberately too small to establish a
calibrator or model superiority. A one-step adapter update demonstrates backend
execution, not useful domain learning. The next campaign should quantify whether
additional training improves validation/OOD errors, structured output and evidence
without unacceptable critical damage. GLM remains an interchangeable model family
with an unqualified training backend; Qwen is the real generative backend already
qualified on this Mac.

## Acceptance gate

One versioned campaign must produce both registered artifacts, same-input
comparison, an explicit confidence support decision, a frozen release manifest,
an application execution of that release, and complete-release rollback. Provide
small deterministic browser/worker contracts plus separate real-model receipts.
No default automation, customer accuracy claim or mandatory accuracy improvement.

AI-assisted annotations can develop and verify all of this machinery. Real-world
model validation remains a later gate: representative notices, independent domain
experts, and held-out performance on that population.
