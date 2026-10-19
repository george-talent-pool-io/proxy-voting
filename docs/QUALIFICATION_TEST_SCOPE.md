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
