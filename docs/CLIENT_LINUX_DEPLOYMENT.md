# Client Linux deployment and acceptance

This distribution is a single-tenant training/classification framework. It does not turn an unlabelled corpus into a validated autonomous classifier. AI-authored data can qualify the machinery; customer automation additionally requires independently reviewed representative client data.

## Supported boundary

`deploy/compose.yml` runs a TLS proxy, a narrow authenticated API and one durable model worker. The legacy research API is not mounted. Named ADMIN, TRAINER, REVIEWER and AUDITOR roles are enforced server-side. Only explicitly configured reviewer accounts can attest expertise. An administrator who reviewed the frozen test cannot promote that qualification.

The containers run as UID/GID 10001, with read-only root filesystems, dropped capabilities, no privilege escalation, bounded temporary storage and rotated logs. The API and model worker use only an internal network: runtime model downloads and external inference are unavailable. The TLS proxy also joins an edge network for client ingress; its fixed configuration forwards only to the internal API. Build-time package/Maven downloads are separate from customer processing. Supply local model weights before startup. Never mount a Docker socket.

Use a Linux host sized for the chosen checkpoint and training method. The current Mac's Docker VM has approximately 4 GB and cannot qualify a 27B Qwen GPU deployment. Official Laya training exceeded a 3 GB cgroup cap in qualification, at both 512 and 2048 context settings. The service now rejects training below conservative 8/16 GiB floors, with a higher weight-size floor where needed; these are admission rules, not proven peak-memory estimates. The CPU image explicitly installs hash-pinned PyTorch CPU wheels; a CUDA deployment needs a separately qualified runtime image and GPU. Linux ARM64 container tests and CPU model tests are reported separately from Mac MLX and eventual customer Linux AMD64/CUDA tests. MLX checkpoints are not Transformers checkpoints and must not be relabelled or silently converted.

## Installation

1. Install Docker Engine and Compose. Copy this source distribution to the server. Keep `/srv/voting` container paths fixed across releases/restores; registered training plans pin absolute paths.
2. Create identities using the interactive CLI, which writes salted scrypt hashes, never plaintext passwords:

   ```sh
   python -m production.security deploy/secrets/users.json administrator --roles ADMIN TRAINER AUDITOR
   python -m production.security deploy/secrets/users.json domain-reviewer --roles REVIEWER --expert-attested
   ```

   The customer must verify the reviewer's expertise and independence. The software records this attestation; it cannot confer expertise. Use a separate ADMIN identity for promotion. Create a new versioned secret for rotation/revocation and restart the API. Do not put credentials in Git, browser storage or command-line arguments.
3. Supply `server.crt` and `server.key` in a private TLS directory. On Linux, make the users secret and TLS private key readable by container GID 10001 (for example root:10001, mode 0640). Docker Compose file-backed secrets retain host file permissions. Certs must cover the configured hostname. Only use self-signed certificates for isolated tests.
4. Set environment variables in a private deployment configuration:

   ```sh
   export VOTING_USERS_SECRET=/absolute/private/users.json
   export VOTING_TLS_DIRECTORY=/absolute/private/tls
   export VOTING_MODEL_DIRECTORY=/absolute/private/models
   export VOTING_PUBLIC_ORIGIN=https://voting.client.example:8443
   export VOTING_BIND_ADDRESS=127.0.0.1
   export VOTING_MEMORY_LIMIT=32g
   export SOURCE_REVISION=$(git rev-parse HEAD)
   docker compose -f deploy/compose.yml up --build -d
   ```

   Default exposure is loopback. Set an approved server interface explicitly for customer network access, with the client's firewall/access controls. TLS terminates at the included proxy. There is no public HTTP listener. Bind no direct API port in production.

5. Open the configured HTTPS origin. Check `/api/client/ready` using a named identity. Verify database, JVM, Prowide helper, workspace permissions and audit integrity. Readiness does not mean the selected model is qualified.
6. After model prerequisites are checked, explicitly set `TRAINING_EXECUTION_ENABLED=true` and recreate the API/worker. Preparation does not start training. The Compose automation switch remains false. A customer-approved deployment override can enable it only after a valid promotion; per-event gates still apply.

## Corpus and review contract

Import JSONL in batches of at most 1,000 rows / 16 MiB. The browser accepts JSONL or a JSON array. The API uses an explicit batch idempotency ID. Each source row declares `raw`, `sender`, `source_type`, `source_reference`, `group_id`, `family`, `split`, `language`, `population`, and optionally `country`, `market`, `declared`. `declared` supplies CORP/SEME/function/PREV only for non-authoritative excerpts. Genuine FIN identities come from Prowide. A disagreement is rejected.

```json
{"raw":"Shareholders may vote ...","sender":"CLIENT-CUSTODIAN","source_type":"USER_PROVIDED","source_reference":"customer-delivery-001/message-42","group_id":"event-42","family":"notice-family-7","split":"TRAIN","language":"en","population":"client-custodian-v1","declared":{"corp":"EVENT42","seme":"MESSAGE42","function":"NEWM"}}
```

Source bytes represented by the UTF-8 JSON string are preserved, including whitespace and line endings. Binary encoding conversion must occur in a documented import preparation step; do not guess an encoding. Every batch reports accepted/rejected rows and quarantined lifecycle states. Row commits are resumable, not an all-or-nothing transaction. Retry the same batch ID only with identical content.

Partition complete events, replacements, duplicates and generation/linguistic families before labelling. Freeze checks exact/lexical duplicate and family leakage. Semantic paraphrases still need curator scrutiny; lexical grouping cannot prove their absence. Dataset freeze requires a current review of every explicit member and locks source snapshots and labels. Changes require a new corpus/event version.

CALIBRATION and FROZEN_TEST reviews are blind: the HTTP source view hides prior labels and predictions. A named reviewer supplies complete factors, exact source quotations and an explicit timezone-aware evaluation time for deadline/final-status truth. All positive labels require source evidence. Final-status truth must match the factor/deadline rule table. The API supplies the identity/provenance; the request cannot impersonate another human. AI labels use a separate route and always remain AI_AUTHORED.

## Learning, confidence and promotion

1. Export TRAIN/VALIDATION only. Prepare a campaign with the exact local base model path/revision, backend, seed, context, optimizer/LoRA configuration and candidate routing policy. Linux accepts official Laya SDK or Transformers PEFT; arbitrary Python executable paths are rejected. Exact-model compatibility needs a real save/reload/serve test.
2. Start the campaign explicitly. Worker logs/checkpoints/validation results persist. Validate/select without frozen answers. Cancellation is cooperative; failed/interrupted attempts are not silently resumed. Create a new attempt to restart from the base.
3. Queue a CALIBRATION task with a release, frozen dataset, population and evaluation reference. All inputs are processed and fsynced before that role's answer file is opened. Fit and evaluation folds are separated by connected family/group/lexical-duplicate components. Portable JSON logistic calibrators use no pickle. Report Brier/ECE and support. Missing support returns null numerical confidence.
4. Freeze a qualification plan **before** test execution. It pins release, calibrator, source code, dataset, population, evaluation time, thresholds and group membership. Do not try alternate thresholds on the frozen test. A revised policy needs new independent test data.
5. Queue QUALIFICATION. Full raw model/evidence stages are saved before any review/key query. Gates include complete-output auto precision, critical-positive recall for voting/blocking/POA/registration, independent group support and measured review rate. One-sided exact lower bounds use the worst outcome per connected group; Bonferroni allocation covers five statistical claims. Default thresholds are conservative engineering assumptions, not regulatory requirements. They are configurable **before** evaluation.
6. Synthetic, unauthenticated, nonexpert or non-client-source labels cannot pass customer qualification. Calibration must also use authenticated blind expert labels from the declared real client population. Qualification expires after the predeclared period; artifact/source changes invalidate it. An independent administrator may explicitly promote only a passed qualification.
7. Per-event routing also requires supported predicate and final-decision calibration, exact evidence, resolved deadlines where relevant, no UNKNOWN/conflict, supported language/format and an active qualification/promotion. Population mismatch fails closed. A verified error on an automatically processed event suspends that qualification pending new independent qualification.

Numerical predicate confidence estimates predicate correctness in its calibration population. Final-decision confidence has its **own correctness calibrator**; a minimum of predicate probabilities is not presented as a joint probability. Exact quote matching verifies provenance, not entailment. No language outside the initial English confidence population is auto-accepted. Human review remains available at every stage.

## Queue, monitoring and recovery

One model worker processes bounded tasks. It loads a release once per batch, not once per notice. The cross-process model lease serializes managed training/inference. Model calls outside this service are not governed by that lease. SIGTERM finishes the current notice, then stops. SIGKILL/container failure retains completed predictions and marks the task INTERRUPTED at restart; an operator submits a new explicit task for remaining events. Nothing automatically re-trains or re-scores frozen data on startup.

The operational console exposes persisted tasks, errors, model traces, label origins, measured review rate and qualification failures. `/api/client/ready` checks dependencies and, in the Docker profile, a measured model-worker heartbeat (stale after 30 seconds); `/health/live` exposes no customer data. Monitor authenticated readiness externally with the client's alerting system. Export the hash-chained audit head to customer-controlled immutable storage. A local database administrator can rewrite an entire database; the hash chain alone is not external tamper proofing.

Stop accepting imports/reviews and stop both API and worker for backup. Take an encrypted/customer-access-controlled snapshot using `python -m training.framework.operations backup /srv/voting/state/backups/VERSION` in a one-off container with the same mounts. This includes an SQLite online backup and file checksums, and lists pinned external model prerequisites. Restore into empty destinations at the same container paths; verify hashes and SQLite integrity before explicit startup. Never overwrite a live database. The deployment must qualify backup/restore, key rotation, storage capacity, load limits and recovery objectives against the client's own operating requirements.

## What can be sold and what remains an acceptance condition

The deliverable is the controlled, auditable training and classification platform, with a contract for qualifying each customer model. It is not a guarantee that a customer corpus yields a particular accuracy or a very low review fraction. Those must be measured with representative independently expert-labelled data. The exact customer GPU/checkpoint, ISO message profile, throughput, failure recovery and security/operational requirements need installation acceptance before live financial operations.

Technical references: [Compose services and isolation controls](https://docs.docker.com/reference/compose-file/services/), [file-backed secret limitations](https://docs.docker.com/reference/compose-file/secrets/), [PEFT checkpoint/base relationship](https://huggingface.co/docs/peft/developer_guides/checkpoint). Prowide is pinned in `tools/prowide/pom.xml`; parse success is deliberately not represented as full SWIFT standards validation.
