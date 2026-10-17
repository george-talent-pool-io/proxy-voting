# Event-level learning framework verification

This milestone connects the product lifecycle: linked source messages → current
event → model execution → review revisions → dataset version → Laya/Qwen training
→ comparison → experimental selection and rollback. Automation remains disabled.
Customer accuracy remains unknown.

## Data and scope

The fact-first generator creates 160 event chains (640 MT564/MT568 messages), in
20 linguistic generation families. Each chain contains a notification, supplement,
replacement, and supplement belonging to the replacement. Labels and sources are
explicitly STANDARDS_DERIVED_SYNTHETIC / AI_AUTHORED, never public production
messages or independently expert-reviewed labels. This finite grammar qualifies
the engineering workflow; it does not establish linguistic representativeness.

Family/lexical duplicate grouping precedes the 96 TRAIN, 32 VALIDATION,
16 CALIBRATION, 16 FROZEN_TEST assignment. The 57-case challenge is untouched.
The 7,683 existing unlabelled public excerpts remain a separate source corpus.

## Implemented connections

* **Event state:** Prowide typed-component projection, sender/CORP namespace,
  collision-protected SEME, current PREV linkage, stale-message quarantine,
  notification/narrative replacement, cancellation and observation-only
  instruction/status handling. Original messages, hashes, superseded facts and
  per-message evidence offsets remain inspectable. A replacement starts a new
  notification epoch; omitted facts become unresolved and earlier supplements
  remain historical. The legacy custom parser is not used by this ledger.
* **Classification:** current narrative plus relevant current Prowide facts feed
  the registered model; deadlines use the current notification and deterministic
  comparison. Bare local timestamps stay UNKNOWN. Source quotations must match
  an operative raw message. Ordinary notices bypass ISO parsing.
* **Reviews:** complete semantic labels bind to an event snapshot and optimistic
  revision, retaining previous execution, exact evidence links and label origin.
  AI reviews require model identity and cannot attest human expertise. New event
  state requires a new review rather than changing an older label.
* **Dataset versions:** development exports select eligible role IDs before
  reading targets. Protected registry checks cover hashes, renamed content,
  groups, generation families and lexical near-duplicates. Frozen input membership
  and private keys have checksums; neither held-out role is a trainer input.
* **Jobs:** explicit queue/dispatch, detached worker, durable SQLite history,
  cross-process model lease and timed-benchmark deferral. API restart never starts
  training. Cancellation is bounded; interrupted attempts are terminal. Explicit
  restart creates a new job from the base weights, not an implied optimizer resume.
* **Evaluation:** same inputs and truth, all candidates' predictions flushed and
  checksum-receipted before answer keys are read. Per-field positive recall,
  nine-predicate exact match, deadline and final-status denominators are distinct.
  Comparison includes every error and per-predicate repair/damage transitions.
* **Selection:** validation-only, append-only experimental selection/rollback,
  checkpoint/prompt/rule/validation receipt identities, no automatic promotion.
  It changes only the opt-in event workspace, not the default customer path.
* **GUI:** Model Lab event import/history/review, export/freeze, prepare/queue/
  dispatch/cancel, comparison, experimental selection/rollback and persisted model
  trace. Browser execution doubles are clearly separate from real-model receipts.

## Confidence boundary

CALIBRATION is separate from training and model selection. FIT/EVALUATION folds
are family-isolated. Calibrator identity includes checkpoint, prompt, event policy
and runtime source. The current small engineering cohort cannot meet the existing
support gate (100 fit / 50 evaluation examples per predicate, including correct
and incorrect predictions). The correct output is insufficient support and null
numerical confidence. Native Laya scores are not calibrated probabilities. A new
checkpoint does not inherit another model's calibrator.

## Verification

Actual bounded model-training, evaluation, restart and regression results are
recorded below after verification. They qualify software execution, not model
quality on customer data. Failed attempts remain in the job ledger.

## Running the workflow

Use Model Lab → Event learning loop. The normal application remains conservative.
To opt into explicit local execution, start with TRAINING_EXECUTION_ENABLED=true;
keep AUTOMATION_ENABLED=false. Preparing jobs or refreshing pages never trains.

The reproducible real qualification driver is:

```sh
uv run python -m scripts.verify_event_learning_loop --version NEW_VERSION --output artifacts/NEW_RECEIPT.json
```

Run it with no timed model benchmark active. It freezes a small cohort before
model execution, trains/reloads both backends, restarts FastAPI while its separate
worker runs, compares validation/calibration/frozen roles, verifies review/export
and rollback, then checks persistence after another restart. Versions/receipts
are append-only. The explicit --reuse-qwen-job recovery option verifies the same
bundle manifest and preserves the original job instead of retraining it.

## Limits and next step

This is engineering qualification, not a fair architecture-quality trial or proof
that tiny weight updates improve generalisation. The registered whole-notice
Laya head has no quotation extractor; its trace correctly says evidence is
unavailable and requires review. Prowide parse success is not complete SWIFT
standards validation. Operational entitlement/state policies, production security,
load/concurrency hardening and expert-labelled customer performance remain work.

Next: a repeatable experiment campaign over event-level development data, with
predefined learning-curve stages, adequate separately held-out calibration,
evidence-quality evaluation and critical-damage gates before an explicit
experimental release. AI-assisted data can verify that machinery. Representative
independent expert labels are required before customer-quality/automation claims.

## Verified execution results

Original public-notice count remains **7,683**. The new ledger preserves **640** synthetic messages. Reviews by origin: `{'AI_AUTHORED': 160, 'AI_REVIEWED': 1}`. No expert labels are inferred.

The real engineering cohort was fixed before training: **8 TRAIN, 4 VALIDATION, 4 CALIBRATION, 4 FROZEN_TEST**. All are AI-authored construction labels. “Blind” here means the prediction/scoring workflow, not independent secrecy from the synthetic corpus author. This is not a model-quality benchmark.

| Backend | Real update | Reload check | Artifact |
|---|---|---|---|
| Laya | 1 epoch / 72 question items | maximum probe difference 0.0 | `d487b4d6-4177-4072-9d48-24f6a8a32913` |
| Qwen | 1 optimiser step / 94,208 trainable parameters | maximum probe difference 0.0 | `dde8a411-86b7-480b-b034-dcf22e1db0e0` |

Qwen training took 411.2s; peak MLX allocated memory was 27.69 GB (not total OS/unified-memory peak). The unchanged base and saved adapter hashes were checked. The reload probe covers 128 tokens on one held-out input, not a claim of whole-dataset bitwise determinism.

The initial Laya attempt rejected an unsupported `max_steps` driver setting before updates. It remains FAILED in the ledger. The corrected new attempt uses epochs; TrainSpec now rejects this mismatch during preparation. The original Qwen run was retained rather than retrained.

| Role / model | Semantic assertions | All-nine exact match | Final status | Deadline | Warm median / p95 |
|---|---|---|---|---|---|
| VALIDATION / Laya | 22/36 | 0/4 | 1/4 | 4/4 | 112 / 257 ms |
| VALIDATION / Qwen | 29/36 | 3/4 | 3/4 | 4/4 | 52177 / 124200 ms |
| CALIBRATION / Laya | 22/36 | 0/4 | 0/4 | 4/4 | 147 / 198 ms |
| CALIBRATION / Qwen | 36/36 | 4/4 | 4/4 | 4/4 | 49510 / 51012 ms |
| FROZEN_TEST / Laya | 25/36 | 0/4 | 2/4 | 4/4 | 150 / 192 ms |
| FROZEN_TEST / Qwen | 36/36 | 4/4 | 4/4 | 4/4 | 49740 / 51587 ms |

These are reconciled semantic assertions with identical structured context and rules, not pure-model or parser accuracy. Latencies are tiny-cohort warm diagnostics, exclude loading and are not a controlled throughput comparison. No result is customer accuracy. All records require review.

### Critical-positive support

| Role / model | Voting positive recall | Blocking positive recall | POA positive recall | Registration positive recall |
|---|---|---|---|---|
| VALIDATION / Laya | 2/2 | 1/1 | N/A (support 0) | 0/1 |
| VALIDATION / Qwen | 2/2 | 0/1 | N/A (support 0) | 1/1 |
| FROZEN_TEST / Laya | 3/3 | 1/2 | N/A (support 0) | N/A (support 0) |
| FROZEN_TEST / Qwen | 3/3 | 2/2 | N/A (support 0) | N/A (support 0) |

All per-field confusion matrices, support, F1, repair/damage and failures are in `ISO15022_EVENT_LEARNING_RESULTS.json` and the versioned comparison folders. Independent candidate transitions are not causal fallback repairs.

### Confidence and persistence

All nine calibrators for both models report INSUFFICIENT_CALIBRATION_SUPPORT; no numerical confidence is activated. The support refusal is expected and correct. The four calibration inputs cannot meet the gate.

The real detached worker survived an API restart with exactly the same two task identities. Both models executed in the event application. An AI_REVIEWED revision retains the prior execution and exports as a new dataset version. A queued spare was cancelled; explicit restart produced a new unstarted job. Selection, rollback, restoration, executions and reviews survived another API restart.

A final separate real application proof exercises runtime v4 and persists its loaded source archive. Engineering safety changes made during QA are not presented as a frozen architecture-quality experiment or as an accuracy improvement.

### Receipts

* `artifacts/event-learning-real-proof-v2.json` — real training/event lifecycle, comparison and rollback.
* `artifacts/event-learning-runtime-v4-proof.json` — final runtime / real-model persistence.
* `artifacts/event-learning-final-regression.log` — ordinary application tests.
* `artifacts/event-learning-final-browser.log` — complete browser regression.
* `data/reports/ISO15022_LEARNING_FRAMEWORK_NEXT_CAMPAIGN.md` — next milestone.


## Final verification and hand-off

* **2,175 ordinary application tests passed**; one opt-in tiny CPU training smoke
  was skipped and 157 model/browser checks were deselected in this ordinary run.
  This count does not represent real-LLM executions or semantic accuracy.
* **26 browser tests passed**, including the full event lifecycle with explicit
  model doubles. Separate receipts above execute the actual installed Laya and
  Qwen models. No historical semantic expectation was weakened or removed.
* Source audit: **640/640 raw hashes**, **3,640 projected field/source spans** and
  **1,440 latest-review quotations** checked. These are exact provenance checks,
  not semantic entailment accuracy.
* A live-browser smoke check against the restarted main application loaded both
  real saved event traces, displayed AI_REVIEWED provenance, opened exact raw
  source from nine evidence links, and recorded zero browser errors.
* The main service is available at `http://127.0.0.1:8000/#model_lab` with training
  and candidate execution disabled by default, automation disabled, 160 learning
  events preserved and no running framework tasks.
* `event-learning-reviewed-v2` is the portable dataset version, including all
  raw messages and their hashes/provenance inside its input-only archive. Original
  v1 manifests/keys and all older model/benchmark outputs remain unchanged.

Supplement NEWM chains append narrative; only explicit REPL/CANC supersedes the
linked supplement. The affected-chain policy suffix changes the review snapshot
so old labels cannot silently cover changed context. Existing unaffected event
snapshots were verified unchanged. Partial recovery can feed semantic review
without gaining authoritative structure or an established final event decision.

Leakage checks apply to actual operative classifier inputs. Shared superseded
boilerplate is never model training input. A future history-consuming model must
regroup/refreeze complete message histories; lexical grouping alone cannot prove
absence of semantic paraphrases.

The next milestone is the [trainable cascade release campaign](ISO15022_LEARNING_FRAMEWORK_NEXT_CAMPAIGN.md).
Current experimental selection serves one registered candidate; it does not yet
install a trained pair into the separate selective-cascade experiment.

Final runtime v4 was also executed through the **event** API with both real
registered models, not only the ad-hoc notice API. Both persisted new linked-event
traces, exact raw-message evidence links, null calibrated confidence, review
requirements and runtime-source archives; both survived another API restart.
Receipt: `artifacts/event-learning-current-event-proof.json`.

The separate pre-existing Laya-first study was restored after these checks from
its preserved 58/80 validation checkpoint. It is not a running framework training
job. Its protocol/weights and saved prediction prefixes were verified unchanged;
the older user-stopped Qwen-domain study remains stopped. Restoration receipt:
`artifacts/event-learning-benchmark-restored.json`.
