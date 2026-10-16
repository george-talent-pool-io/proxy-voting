# Supervised research verification

- Application tests: **145 passed**, 123 opt-in model/browser tests deselected; `artifacts/research-tests-final.log`.
- Browser suite: **9 passed**, including the original eight and the experiment/error-explorer flow, corpus/factor/expected-value/high-confidence filters, and quality gate visibility in demo mode; `artifacts/research-e2e-final.log`.
- Real-model semantic pytest: **47 failed, 68 passed** across two models plus one manifest check. Base: 30/57; frozen selected candidate: 37/57. Those failures are deliberately retained (`artifacts/research-semantic-pytest.log`). No expected answer was modified.
- Both Laya 100-row blind files were closed, flushed and SHA-committed before this scoring pipeline read the answer key. Earlier, before the explicit protocol, an inspection script had read the all-500 JSONL and printed two test rows; the remaining text was not inspected or used for fitting/selection. This is not a pristine file-access-blind study. `BLIND-COMMIT.json` precedes `TEST-SCORED.json`.
- Frozen selected model/preprocessing/criterion/threshold/dependency hashes verify. Source archive SHA-256 is unchanged. Both checkpoints reproduced all 100 native blind scores, decisions, statuses and policy scores exactly on reload. `data/experiments/supplied-synthetic-v1/VERIFICATION.json`.
- Native probability checks: finite, in range, valid SDK-rounded sums; 100/100 source hashes and IDs match for both models. No generated seven-class probabilities.
- Public baseline re-audit: 7,683 inputs/outputs, zero failures/invalid probabilities/hash mismatches, no detected split leakage under the exact grouping metric. `artifacts/research-public-run-verification.json`.
- Restarted application: 7,683 source records, 7,683 preserved baseline predictions, **zero human review rows**. Synthetic labels have not entered the golden dataset. Separate 1,000-record public review cohort retained with immutable IDs/hashes and group splits.
- Automation is OFF in base and fine-tuned configurations and every persisted blind prediction. Current quality gate: **NOT MET**.

The perfect supplied synthetic score does not override 20 remaining semantic challenge failures, 12 highly confident mistakes, split overlap, two previously exposed test labels, or missing expert-reviewed operational evidence. See `LAYA_TRAINING_EVALUATION.md` for interpretation.

A new browser test initially ran after the old final persistence test had deliberately shut down the test server. The fixture lifecycle now owns cleanup of the restarted server; the persistence assertions remain intact. The initial failure log is retained as `artifacts/research-e2e-initial-failure.log`.
