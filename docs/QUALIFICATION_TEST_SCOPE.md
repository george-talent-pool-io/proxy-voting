# Qualification test scopes

The workspace suite and clean source installation have different evidence
availability, not different expected model answers.

* Ordinary software tests run without downloaded model weights. Parser fixtures
  are regenerated using the documented deterministic generators. The Apache-2.0
  publisher MT564 example is a small static fixture, with its original provenance.
* `requires_artifact(path)` checks archived experiment results or the separately
  supplied synthetic ZIP. Its assertions are unchanged. It skips only if that
  optional file is absent from the installation and gives the exact path/reason.
  All those checks continue running in the development evidence workspace.
* Model and browser markers remain separate. Real-model success is reported only
  after the opt-in tests actually execute installed Laya/Qwen checkpoints.
* Contract tests with explicit model doubles use a public, pinned research model
  settings fixture if the historical settings file is absent. This creates no
  predictions, labels, trained weights or completed-experiment receipt. The
  temporary settings file is removed after the test session.

The source delivery test verifies all Python packages, build ignore files and
the exclusion of customer workspaces, qualification corpora and test weights.
The leakage-barrier unit test now reads the existing static authored input
fixture instead of requiring a previously executed prediction file. The frozen
57-case expectations and input text have not changed.

No semantic assertion, historical score expectation or quality gate was relaxed.
The clean-install receipt reports pass/skip counts separately from the complete
workspace regression run; unavailable historical checks are not counted as passes.

## Customer workflow coverage

Run all browser workflows using the marker, rather than only `tests/e2e`:

```sh
RUN_E2E=1 .venv/bin/python -m pytest -m e2e -q
```

`tests/production/test_client_browser.py` starts the real authenticated customer
application in a temporary isolated workspace. Only the model training kernel and
inference kernels are doubles; the actual jobs, training manifests, immutable
splits, validation selection, sealed releases, calibration, qualification, worker
tasks, review, audit and database persistence execute. The double's bytes and
receipts explicitly identify it as untrained. It cannot be imported without the
test-only environment guard and cannot enter the source product's application path.

The suite covers a full customer qualification journey with two successive
learning rounds from a frozen registered derivative, raw-source/AI-review
preservation, failed promotion from AI-labelled/tiny cohorts, insufficient-support
calibration, protected-input refusal, queued cancellation, actual process restart,
real Prowide/scanner/bypass paths, malformed import, auditor permissions and
out-of-order event responses. It does **not** exercise real gradient updates or
27B generation in the browser. No screenshot is a pixel-perfect baseline.

Run installed registered models separately, after preparing a release against the
current source using `scripts.verify_current_customer_release`:

```sh
RUN_RELEASE_REAL_MODEL=1 RELEASE_CAMPAIGN=<current-source-campaign> \
  .venv/bin/python -m pytest tests/classifier/test_registered_release_real.py -q
```

The three registered-release real-model checks execute the actual durable customer
worker against an isolated database snapshot: real Laya and Qwen run, the decision
and review/null-confidence state persist, and the audit verifies. No live customer
database is modified.

A real-model learning candidate has its own manifest, actual optimizer results,
save/reload parity and validation predictions. Its metrics must be reported
separately from software-contract tests. Linux image checks, Mac model checks and
customer hardware qualification are distinct; success on one does not certify the others.
