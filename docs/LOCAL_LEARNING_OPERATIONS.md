# Local learning workspace operations

The qualified deployment target is one loopback-bound operator on the Mac, with
serial model execution. This is not a multi-tenant hosted service. AI-authored
construction labels can qualify the learning machinery without claiming that a
trained model generalises to customer notices.

## Install and start

Use the checked-in `uv.lock`: `uv sync --frozen`. Build the pinned local Java
helper with `mvn -f tools/prowide/pom.xml package`. The MLX training environment
uses `training/framework/requirements-mlx.lock.txt`; follow the checkpoint setup
in `training/framework/README.md`. Startup does not download weights.

Start the conservative app:

```sh
uv run uvicorn apps.api.main:app --host 127.0.0.1 --port 8000
```

For a protected local operator session, set `LOCAL_OPERATOR_PASSWORD` using your
shell's secure secret configuration before starting. The username is `operator`;
the browser presents its native authentication dialog. Do not place the secret
in a URL, source file or JavaScript storage. All assets and API paths except the
minimal health response require authentication when configured. This boundary
is for loopback use; remote deployment needs HTTPS and a separately reviewed
identity/RBAC setup. Reviewer identities remain annotation provenance, not
independently authenticated human identities in a shared-user service.

Training requires explicit `TRAINING_EXECUTION_ENABLED=true`. Keep
`AUTOMATION_ENABLED=false`. GET, page refresh and API restart never start work.

## Campaign lifecycle

Create a JSON `CampaignSpec` with a versioned development `bundle_id`, a matching
frozen `dataset_id`, fixed training/reused-baseline stages, candidate releases,
operator identity and a maximum runtime. Candidate modes are `LAYA_ONLY`,
`QWEN_ONLY` and `LAYA_QWEN`. The currently qualified trainable MLX adapter exposes
normal Qwen Direct generation, not reliable constrained-token probabilities;
the separate historical three-gear experiment is retained.

```sh
uv run python -m training.framework prepare-campaign campaign-spec.json my-campaign
uv run python -m training.framework run-campaign my-campaign
uv run python -m training.framework campaign-status my-campaign
```

Alternatively use Model Lab → Event learning loop → Learning campaigns. Preparing
is separate from dispatch. The API dispatches a detached worker. Baselines,
stages, validation-based routing candidates and the objective are fixed before
execution. New critical false negatives relative to the first validation
baseline fail the candidate damage gate. Calibration never uses validation or
frozen answers. All frozen predictions are flushed before answers are opened.
The campaign explicitly selects an **experimental** release; it never switches
the default public-notice classifier or enables automation.

A sealed release pins model/base/adapter manifests, prompt, schema, passage
aggregation, parser/event/rule sources, runtime locks, routing, validation and
calibration. A checkpoint cannot inherit another release's calibrator. Drift
fails closed. Source upgrades require a new release. Rolling back an old source
version also requires restoring its compatible application source environment;
the loader will not silently execute new code under an old source identity.

The event-classification endpoint executes the selected complete release unless
a specific checkpoint is requested. Both stages, gates, disagreements, exact
source links and confidence scope remain in the persisted trace. Numerical
confidence stays null when support/quality is inadequate. A minimum of predicate
confidence is a derived trust score, not calibrated joint decision probability.

## Cancellation and recovery

Cancel from the GUI/API. Training stages receive bounded interrupt/kill handling;
evaluation stops at a completed-notice boundary (a model request may run until
its configured timeout). Completed rows and failed attempts remain auditable.
A dead campaign worker becomes INTERRUPTED. There is no automatic restart or
optimizer-state resume. Prepare a **new** campaign and explicitly reuse verified
completed stage jobs. Never remove an execution lock to relabel a partial run.

The shared local model lease prevents overlapping application model calls and
training. Unmanaged third-party runtime processes remain the operator's
responsibility. The older timed study uses its own cooperative STOP protocol;
do not run it concurrently with training/timing qualification.

## Health, backup and restore

```sh
uv run python -m training.framework.operations readiness
uv run python -m training.framework.operations backup /safe/path/snapshot-id
```

Quiesce campaigns/training and application writes before backup. SQLite online
backup provides a consistent database copy; the workspace is checksummed before
and after copy. If it changes, the partial snapshot receives no certification.
Snapshots contain private answer keys/customer source and must be protected as
sensitive local data. They include registered checkpoints, adapters, reviews,
release manifests, calibration and job history. External large base weights are
not duplicated; their exact file hashes are prerequisites for restoration.

Stop the API/workers before restore. Move the damaged deployment aside yourself;
restore refuses to overwrite any existing path. Restore to the **same absolute
configured paths**, because immutable historical plans retain those paths:

```sh
uv run python -m training.framework.operations restore /safe/path/snapshot-id \
  --workspace /original/path/data/training-workspace \
  --database /original/path/data/voting.sqlite
```

Use the original database path from `BACKUP.json` (the example name is not a
default-path claim). Verify readiness and release integrity before explicitly
starting the service. Restore never dispatches work. Corrupt snapshots, changed
base weights and incompatible release sources are rejected. Monitor readiness,
worker/task states and disk capacity; this local product has no managed external
alerting or multi-host scheduler.

## Qualification boundaries

Software contracts use explicitly marked doubles where appropriate; bounded
real-model receipts separately qualify local Laya and Qwen updates/reloads and
serving. Statistical calibration fixtures test the numerical code path; they are
not Qwen/Laya calibration evidence. The reused engineering frozen fixture is not a newly unseen quality benchmark.
Tiny real-model cohorts cannot establish a reliable
calibrator, model superiority or customer accuracy. Real custodian profile
acceptance, expert-labelled real held-out data and deployment-specific security
remain later qualification gates.
