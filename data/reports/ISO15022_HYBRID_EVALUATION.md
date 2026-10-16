# ISO15022 hybrid evaluation

Measured 16 October 2026. **Quality gate not met; automation disabled. No customer accuracy claim.**

## 1. Public sources

See [source research](ISO15022_PROXY_RESEARCH.md) and `data/iso15022_corpus/research_sources.json`: public ISO dictionary, Clearstream/LuxCSD service specifications and official example, Euroclear, SIX SIS, DTCC, Euronext and ISO/SMPG context. Direct SMPG document access was blocked; third-party mirrors were excluded. No private MyStandards material was used. Current Clearstream meeting flows use ISO20022 for instructions/status/results; MT564 coexistence is notification/cancellation only. Generic ISO15022 capability is not current sender acceptance.

## 2–3. Genuine examples and generated coverage

1 short official disclosure-message excerpt; **zero public production messages**. Other public documents contain examples not copied into this corpus. 1100 generated partial-message fixtures, including 25 explicit notification/narrative/replacement/cancellation chains; 500 mutations. Every item has source type, URL, organisation, retrieval date, message type, notes and checksums in `sources.jsonl`. These fixtures are excluded from semantic training. They are not a substitute for production data.

## 4–5. Parser support

MT564, MT565, MT567 and MT568 have experimental subset field routing. MT566 can be retained as opaque confirmation history, not a decoded voting confirmation. Supported: nested/repeated 16R/16S, 20C SEME/CORP/COAF/PREV/RELA, 23G function, GENL 22F CAEV/CAMV, USECU 35B ISIN/description, scoped CAON/CAOP and option indicators, 98A/C/E dates with qualifier/precision/offset, coded 98B dates, selected narrative qualifiers, and preserved processing status. Unknown tags/qualifiers/DSS and unsupported date alternatives remain lossless and visible. This is **not complete mandatory-field, network or sender-profile validation**; VALID_ISO15022 is deliberately withheld.

## 6–7. Exact parser and robustness checks

4402 / 4402 reference-value assertions passed across generated partial fixtures and the official excerpt. 28792 field spans checked. No crashes across all 1601 items, including 500 mutations. Property tests exercise 525 generated cases per suite run: arbitrary Unicode, CR/LF/CRLF, envelopes, narrative text, valid calendar dates and lossless segment coverage. This tests bounded inputs, not all possible malformed data, full grammar compliance or production accuracy. See `artifacts/hybrid-app-tests-final.log`.

## 8. Existing public excerpts

All 7683 processed, zero failed rows, 2.711s detector/parser time. Counts: {"UNSTRUCTURED_NOTICE": 7674, "UNRECOGNISED": 9}. Zero recognised tags, zero usable ISO structure. Nine short/unrecognised records are retained for review. Thus the existing corpus primarily tests unstructured semantics, not ISO parsing. Raw source files are unchanged.

## 9–12. Deterministic facts, model routing and escalation

The public routing audit defines nine decision slots per record: vote, seven restrictions and deadline (69147 slots). Deterministic non-unknown outputs: 0 (0.0%). Planned Laya slots: 61392 (88.78%); these are **planned routes**, not completed inference or verified fact resolution. Narrow Laya was not run over all 7,683 rows in this phase. Actual LLM escalations: zero; fallback is disabled and no external dependency exists. Human-review policy: 7683 / 7683 (100%). Full-corpus ML percentages and verified fact accuracy are unmeasured. Parser/rule assertions, semantic scores and final customer decisions remain separate in the GUI.

## 13. Narrow predicate learning and evaluation

A new official-SDK Laya fine-tune used exactly the supplied 300 TRAIN rows and 100 VALIDATION rows, seed 42, four epochs, full encoder, soft CE, option shuffle, no internal calibration split; validation-only temperature fitting. Checkpoint `data/models/narrow-v1`; manifests/config/hashes/losses under `data/experiments/narrow-v1`. All 300 rows train three compatible targets (900 question-items): voting opportunity, share blocking and POA. These are **AI-authored synthetic labels, not expert reviews**. The supplied splits have known duplicate leakage, disclosed in the previous study. No new independent frozen test was available. The previously scored 100-row test was not reused. The original blind-test artifacts and all frozen historical files remain intact. Existing 57 challenge cases and ISO fixtures never train the model.

No compatible labels exist for registration, owner disclosure, split voting, lending recall or the new residual restriction. Their outputs are transfer-only experiments, not domain-trained or validated predicates. Old “other restriction” labels overlap the expanded predicates and were not silently relabelled as residual truth. New review labels are still needed.

Known synthetic validation, same 100 rows (three labelled predicates only):

| Predicate | Narrow base | Narrow fine-tuned |
|---|---:|---:|
| votable | 54.0% | 84.0% |
| share_blocking | 11.0% | 80.0% |
| poa_required | 77.0% | 84.0% |

These are diagnostics after sentence aggregation, not independent test accuracy. Native SDK outputs and per-field confusion matrices are persisted.

New authored minimal-pair diagnostics, never training:

| Predicate | n | Base correct | Fine correct |
|---|---:|---:|---:|
| share_blocking | 4 | 3 | 2 |
| poa_required | 3 | 3 | 2 |
| registration_required | 2 | 1 | 2 |
| beneficial_owner_disclosure_required | 2 | 2 | 2 |
| split_voting_restricted | 2 | 2 | 2 |
| securities_lending_recall_required | 2 | 2 | 2 |
| other_voting_restriction | 2 | 2 | 1 |

Overall: base 15/17; fine 13/17. Tiny authored samples do not establish predicate accuracy. The fine-tune regresses on these diagnostics. Source-exact candidate evidence and all native passage scores remain available.

## 14. Old versus new on the unchanged 57-case challenge

| Architecture | Passed | Failed |
|---|---:|---:|
| legacy_base | 30 | 27 |
| legacy_fine | 37 | 20 |
| hybrid_base | 26 | 31 |
| hybrid_fine | 32 | 25 |

All 57 compatible cases were evaluated using their original partial expected assertions; no expected answers changed. No ISO structure is present. Whole-text fine-tuning beats this narrow pipeline; base hybrid is worse than legacy base. Narrow fine-tuning improves over narrow base but does not outperform the best preserved legacy model. The new pipeline changes semantic framing, chunking and conservative rule policy together; this is not an isolated parser ablation.

Challenge field agreement (denominators differ because expected labels are partial):

| Field | n | Narrow base correct | Narrow fine correct | Base macro F1 | Fine macro F1 |
|---|---:|---:|---:|---:|---:|
| votable | 54 | 31 | 38 | 0.368 | 0.431 |
| share_blocking | 11 | 3 | 8 | 0.154 | 0.552 |
| poa_required | 8 | 8 | 5 | 0.667 | 0.489 |
| other_restriction | 4 | 4 | 0 | 0.333 | 0.000 |
| deadline_status | 14 | 13 | 13 | 0.933 | 0.933 |

`comparison-fixed-labels.json` uses the same three-class vocabulary for both models, unlike the raw exploratory summaries whose observed-label union can differ. Deadline agreement (13/14 for both) is deterministic and **must not be reported as Laya semantic accuracy**. Full confusion matrices and per-class precision/recall/support are in the JSON.

## 15. Failure modes and auditability

[Every hybrid challenge failure](ISO15022_HYBRID_ERRORS.md) includes text, expected/observed assertions, scores, margin/confidence, evidence and deadline calculations. Raw JSONL retains every sentence distribution. Remaining problems include voting/non-voting confusion, missed or contradictory restrictions, negation and supersession. In the narrow fine-tune POA and untrained residual restrictions regress. Opposing confident sentence predictions abstain; this prevents washing away a positive but also treats absent requirements in unrelated passages as conflicting negatives. Sentence segmentation currently treats physical narrative lines as passage boundaries; wrapped ISO text can lose context. Neither sentence scores nor exact quotations guarantee valid supporting evidence. Superseded semantic narrative is not reliably resolved.

The persistent event ledger retains sender+CORP identity, SEME/source hashes, source messages, current and superseded fields, replacements, cancellations, instructions, statuses and opaque confirmations. Unlinked/stale replacements quarantine; instruction cancellation never cancels the event. Omitted replacement fields retain original provenance with review required. Complex option renumbering, semantic MT568 supersession, out-of-order recovery and complete sender-specific account identity remain unsupported; do not treat the ledger as an authoritative custody system.

No automatic LLM disagreement experiment was possible because no local LLM was configured. This is unmeasured, not assumed helpful. DisabledFallback returns UNKNOWN without external calls.

## 16. Did structure improve end-to-end performance?

**Not established.** Deterministic extraction works on the explicitly scoped generated fixtures, but zero existing public rows have ISO fields, one official partial excerpt is insufficient, and no independently expert-labelled structured event test exists. Narrow training learns the synthetic three-target task but transfers inconsistently. This PoC is suitable for an honestly labelled research demonstration, not a customer quality/automation claim. The quality gate remains NOT MET.

Diagnostic confidence coverage on known synthetic validation (three predicates, not complete event decisions):

| Threshold | Fine coverage | Three-predicate exact agreement | Wrong selected |
|---|---:|---:|---:|
| 0.50 | 66.0% | 89.4% | 7 |
| 0.70 | 66.0% | 89.4% | 7 |
| 0.80 | 66.0% | 89.4% | 7 |
| 0.90 | 66.0% | 89.4% | 7 |
| 0.95 | 66.0% | 89.4% | 7 |
| 0.98 | 66.0% | 89.4% | 7 |

No threshold is approved for automation: these labels are synthetic, duplicates cross the supplied splits, validation is not independent test evidence, all predicates lack sufficient verified support, and challenge errors remain. Latencies are persisted per source in JSONL, but runs were not isolated hardware benchmarks (training/other activity overlapped); do not infer a fair throughput win. A new narrow learning curve was not run; the earlier whole-text head-only curve is a different experiment and is not reused as evidence of narrow-task sample efficiency.

## 17. Highest-value next experiment

Obtain a permissioned, sender-profile-specific set of genuine linked meeting notifications/narratives with expert-labelled voting eligibility and all seven predicates. Freeze a duplicate/event-grouped independent test before any tuning. Evaluate deterministic parsing and whole-text versus passage-based narrow Laya on exactly those events, with a validation-only aggregation ablation. This simultaneously addresses corpus validity, missing supervision and the inability of the current unstructured challenge to test structural benefit.

## Reproduction and verification

See README for commands. Historical frozen study hashes are unchanged. Native probability validity, source-exact evidence, fixture provenance, full public-row counts, SQLite event history persistence and checkpoint reload are checked. Both tested checkpoints reload identically on a fixed first-case prediction sequence; this is a narrower check than the previous study’s all-100 reload verification. Application and browser test logs are separate from deliberately failing real-model semantic checks. Automation remains disabled throughout.


### Final verification evidence

A fresh reproduction into `/tmp/laya-hybrid-verified-reproduction` reran both models,
the corpus audits and reports. All 57 challenge and 100 validation native predictions
were identical for each model (`REPRODUCTION.json`). Historical blind-study freeze
verification also passed. The live server restarted with persisted public results and
zero human reviews; no synthetic labels were added to the golden ledger.

The post-benchmark service guard (`hybrid/service.py`) prevents an unrecognised CAEV
from being displayed as a negative meeting fact. It does not alter the preserved
`pipeline.py` benchmark, model, prompts, aggregation or any measured challenge result.
The literal unknown code remains source-linked and reviewed. Neither parser subset
checks nor a source-exact span establish complete FIN validity or semantic support.

Legacy real-model pytest was rerun unchanged: **47 failed, 68 passed** across the two
legacy models and manifest check. New hybrid semantic failures remain 31/57 base and
25/57 fine. These are explicitly excluded from any claim that application checks pass.


Final application checks: **1,829 passed** (126 opt-in checks deselected). Browser acceptance: **12 passed**. Source-span/provenance checks cover all 1,601 corpus items; 4,402 exact reference assertions pass. Source and model-native artifact integrity/reload checks pass. Full real-model semantic specifications still fail as reported above.

High-confidence wrong directly scored predicates (native passage confidence ≥0.98): base 0 challenge cases; fine 10 challenge cases. Derived broad restrictions and deterministic deadlines have no invented joint/model probability.
