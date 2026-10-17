# Next step: an event-level ISO15022 learning loop

**Implementation:** this acceptance specification is now connected in the
application; see [verification](ISO15022_EVENT_LEARNING_VERIFICATION.md).
The follow-on proposal is [trainable cascade release campaigns](ISO15022_LEARNING_FRAMEWORK_NEXT_CAMPAIGN.md).

The next product milestone is **one reproducible application workflow from a
versioned ISO event through review, training, comparison and reversible model
selection**. It can be developed with AI-authored/AI-reviewed data. Human expert
labels are not a prerequisite for this engineering milestone.

## Concrete acceptance scenario

1. Import a versioned, provenance-labelled synthetic event containing MT564 plus
   linked MT568, then a replacement notification. Preserve every raw message.
2. Prowide/scanner produces normalised facts. An event-state adapter resolves
   sender/CORP/SEME/PREV relationships and retains superseded values. The current
   classification uses the current deadline and operative narrative, with links
   back to the individual source messages.
3. Classify with a registered Laya/Qwen configuration. Inspect parser, model,
   evidence, deterministic rules, final decision and review reasons in the GUI.
4. Save an explicit AI_REVIEWED correction with model identity, source evidence,
   reviewer notes, previous prediction and revision history. Human/expert origins
   remain available but are never inferred from an AI review.
5. Export a new training version. Keep every message in an event, near duplicate,
   minimal-pair family and generation family in a single split. Frozen and
   calibration labels cannot enter the training/model-selection worker.
6. Launch a bounded Laya job and a bounded Qwen job from a durable job interface.
   Resource ownership serialises local training/inference. Restarting the API
   preserves the job ledger and cannot silently restart or duplicate a job.
7. Reload both artifacts. Compare per-predicate assertion results, positive
   recall, exact match, evidence, latency and repair/damage on the same inputs.
   Freeze model selection before the independent synthetic test is scored.
8. Fit/evaluate a separate model-specific calibrator where support permits;
   otherwise confidence remains unavailable. Do not inherit another checkpoint's
   calibrator.
9. Select a candidate explicitly in the experimental application, rerun the
   original event, then roll back to the previous artifact. All results, reviews,
   datasets and checkpoints remain inspectable. Automation stays disabled.

The acceptance criterion is that the lifecycle is correct and auditable. It
does not require a predetermined accuracy improvement or perfect synthetic
classification. If a tune damages an answer, the comparison must show that.

## Focused implementation work

| Area | Existing foundation | Next connection |
|---|---|---|
| Parser | Prowide + lenient scanner, source ranges | Versioned event importer with explicit source type |
| Event history | Legacy append-only EventLedger | Accept Prowide-normalised facts instead of reusing the custom parser in the new route |
| Candidate inference | Registered Laya/PEFT/MLX model interface and persisted traces | Classify current linked event context; evidence keyed by message ID |
| Reviews | Complete-schema AI/human review revisions | Event-level annotations and reviewed ad-hoc ISO samples |
| Training data | Checked train/validation bundles | Versioned event-level datasets, protected split registry and frozen-input hash checks |
| Training | Real backend runners, plans, leases and artifact registration | Durable GUI job launch/status/cancel; explicit restart/resume semantics |
| Evaluation | Shared assertion metrics and validation predictions | Common comparison, repair/damage and frozen blind-scoring workflow |
| Calibration | Separate population-specific calibration components | Bind calibrator and routing configuration to the exact artifact identity |
| Deployment | Opt-in experimental candidate analysis | Explicit experimental selection and rollback; no automatic promotion |

## Development corpus

Start with approximately100–200 small event families. Generate facts first, then
message chains and narrative wording. Mark all items
`STANDARDS_DERIVED_SYNTHETIC` / `AI_AUTHORED` or `AI_REVIEWED`; none are presented
as real production SWIFT traffic. Reuse authoritative public field specifications
and the existing parser fixtures, keeping parser fuzz fixtures separate from
semantic training. The existing57-case authored challenge remains untouched.

Cover notification/additional narrative, replacements/cancellations, changed
deadlines, multiple options, explicit mandatory/optional restrictions, negation,
conflicting terms, missing timezone, non-voting corporate actions and ordinary
unstructured notices. Keep genuinely ambiguous facts UNKNOWN. Split whole
families before training; reserve separate validation/calibration/frozen families.

## Required deliverables

* Event-level dataset manifest and provenance; immutable raw input and labels.
* Prowide-to-event-state adapter with tested replacement/cancellation semantics.
* End-to-end browser test for the complete review → train → reload → compare →
  select/rollback lifecycle, using small jobs and clearly labelled fixtures.
* Two real-model acceptance receipts: official Laya and the qualified Qwen backend.
* A framework verification report separating parser assertions, semantic
  assertions, final-status truth and training execution checks.

This is the next step toward the product. Representative independently
expert-labelled customer data remains a later model-quality validation stage.
