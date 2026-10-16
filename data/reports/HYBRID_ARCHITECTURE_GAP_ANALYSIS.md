# Hybrid architecture gap analysis

Audited 16 October 2026, approximately 18:15 UTC. Scope: executable repository code, saved native prediction artifacts, configuration/checkpoint manifests, collected test identities, read-only inspection of the running browser application, and read-only local runtime/hardware discovery. README prose and architecture diagrams were not accepted as evidence of functionality.

**Implementation is stopped. This audit creates only this report. No new corpus, training run, model download, LLM installation, LLM model load or generative inference was performed.** The proposed 3,000-example corpus has not been created. The existing source/checkpoints/challenge expectations remain unchanged.

## Executive finding

**REAL LLM IMPLEMENTED: NO** — no generative fallback model is integrated in this application.  
**REAL LLM ENABLED: NO** — there is no application runtime/client/route to enable.  
**REAL LLM USED IN 57-CASE EVALUATION: NO.**

`hybrid/fallback.py` defines a `SemanticFallback` protocol returning a generic `dict` and a `DisabledFallback` whose method returns UNKNOWN with zero external calls. `hybrid/pipeline.py` imports `DisabledFallback` but never constructs it or calls `analyse()` on any fallback. Instead, the pipeline returns the literal `fallback={'enabled': False, 'external_calls': 0}`. Its escalation metric is also a literal zero. This is an interface/stub, **not an implemented LLM layer and not a functional escalation router**. `LLM_ENABLED` is not read by executable application code; setting it would not activate an LLM.

There **is** local LLM infrastructure elsewhere on the computer: Ollama 0.34.3 is running with generative checkpoints installed, and LM Studio, llama.cpp binaries and bundled MLX backends are present. The Ollama `/api/ps` metadata endpoint reported **no loaded models**. This machine capability is not application integration and was not used by any reported classification run.

All application-selected LLM details are **not applicable**: model/checkpoint, parameter count, quantisation, inference runtime/device, context length, prompt/template, structured-output enforcement, temperature, confidence mechanism and fallback threshold. Neither a local nor a cloud/API generative model made the reported decisions. Local installed candidates are inventoried separately in section 12.

Evidence: [fallback interface](../../hybrid/fallback.py), [pipeline](../../hybrid/pipeline.py), [view metadata](../../apps/api/hybrid_views.py), [application routes](../../apps/api/main.py).

## 1. What is actually running today

The live service at `http://127.0.0.1:8000` is FastAPI plus a browser JS interface and SQLite. Its imported public corpus contains 7,683 filing excerpts. The two complete persisted classification runs use **base whole-text Laya**, checkpoint `convaiinnovations/laya`, multilingual revision `7b928d828b7b0e022f929d9bd2e44165aa270148`, local path `data/models/laya/multilingual`. The latest displayed run is `0bcd399d-4250-4cb3-9171-acb95f24761e`. Each completed run has 7,683 predictions and zero failed rows. An earlier interrupted run is retained. There are **zero human reviews in the live golden ledger**.

The normal GUI displays those persisted whole-text base results. `POST /api/runs` calls `scripts.run_batch.run_batch()`, whose default factory is `LayaClassifier`; it does not call `NarrowLaya`, `EventLedger` or an LLM. The selected legacy fine-tune and narrow fine-tune are offline experiment checkpoints, not the default public-corpus model. Loading a notice reads saved predictions; it does not initiate fresh inference.

A public notice's additional hybrid inspection calls `apps.api.hybrid_views.inspect(raw)`, which calls the service/pipeline with **model=None**. It therefore parses and applies rules but **does not execute narrow Laya**. The UI correctly says narrow Laya was not executed in that inspection. The three ISO demonstration choices can instead load previously saved `demo-*.json` analyses. Their semantic scores are offline results, not proof of a live integrated classifier.

The synthetic event-history view reads a saved JSON snapshot created by `scripts/seed_iso_demo.py`; it is not a live ingestion/state-to-decision API. The standalone SQLite event ledger is functional for its tested subset but is not called from the hybrid classification pipeline.

Evidence: `apps/api/main.py:164` (`detail`), `apps/api/main.py:291` (`start_run`), `apps/api/hybrid_views.py:19` (`inspect`), `apps/api/hybrid_views.py:21` (`example`), `scripts/run_batch.py` and `scripts/seed_iso_demo.py`.

## 2. What “hybrid fine-tuned Laya = 32/57” actually measured

The actual call path in `scripts/hybrid_benchmark.py` is:

```text
raw authored notice
  → hybrid.parser.parse(raw)
  → no ISO fields found; route complete raw notice as narrative
  → split physical lines/sentences; fragment oversize sentences at <=900 characters
  → NarrowLaya using data/models/narrow-v1
      eight native questions per passage
      three targets have domain fine-tuning labels
      aggregate passage answers using conflict_abstain
  → deterministic English deadline extraction/comparison
      reference = 2026-10-16T12:00:00+00:00
  → combine facts/conflict flags
  → hybrid.rules.decide()
  → stored predictions, scores, evidence candidates and partial-expectation checks
```

No shared HTML/Unicode/whitespace normaliser is called on this hybrid route before Laya; the legacy route does normalise. No structured context is supplied to narrow Laya: context only influences which question can be omitted when structure already establishes votability. No LLM runs before, after or alongside Laya. The pipeline does not call the persistent event ledger. The post-benchmark `hybrid/service.py` guard for unknown CAEV is used by service inspection, not by the frozen benchmark.

Counts below are recomputed directly from all saved `base-challenge.jsonl` and `fine-challenge.jsonl` rows:

| Stage / outcome | Hybrid base | Hybrid fine-tuned |
|---|---:|---:|
| Input records / parser calls | 57 | 57 |
| Detected UNSTRUCTURED_NOTICE | 57 | 57 |
| Records with recognised ISO fields | 0 | 0 |
| Records sent to narrow Laya | 57 | 57 |
| Narrative passages scored | 110 | 110 |
| SDK predict_batch calls in challenge pass | 57 | 57 |
| Potential per-passage factor answers (8 × 110) | 880 | 880 |
| Deadline rule evaluations | 57 | 57 |
| Records with extracted deadline candidates | 10 | 10 |
| Final deterministic rule evaluations | 57 | 57 |
| Records marked conflicting | 13 | 15 |
| Records requiring human review (policy flag) | 57 | 57 |
| Final status UNCERTAIN_MANUAL_REVIEW | 25 | 43 |
| Cases passing every supplied assertion | 26 | 32 |
| Real LLM invocations | 0 | 0 |
| Cases where an LLM changed Laya | 0 | 0 |
| LLM changes correct | 0 | 0 |
| LLM changes incorrect | 0 | 0 |

LLM correction/damage **rates** are undefined because there were no invocations; the counts are zero. The SDK call counts above cover the 57-case pass only, excluding validation, minimal pairs and reload probes in the same script.

The fine-tuned final status distribution is: 43 UNCERTAIN_MANUAL_REVIEW, four VOTABLE_WITH_RESTRICTION, five DEADLINE_PASSED, two NOT_VOTABLE and three VOTABLE. All 57 carry `manual_review_required=True` and `automation_enabled=False` regardless of display status.

**32/57 is not 32 correctly classified fully labelled events.** The challenge contains partial assertions: 54 votability labels, 11 blocking labels, eight POA labels, four broad-other-restriction labels, 14 deadline labels and only **four explicit customer-status labels**. A case passes if every expected field present for that case matches. Missing gold attributes are not verified. Broad `other_restriction` is derived as an OR/UNKNOWN combination of five new predicates for compatibility. Deadline agreement is software output, not a narrow Laya predicate score.

The four architectures are separate experiments: legacy base 30/57, legacy five-factor whole-notice fine-tune 37/57, hybrid narrow base 26/57, hybrid narrow fine-tune 32/57. The hybrid comparison changes question set, document unit, normalisation/context, aggregation, deadline handling and final status policy together. It does not isolate parser benefit or measure fallback benefit.

## 3. Component-by-component audit

YES means implemented/functional within the stated scope, not production-ready. PARTIAL means a subset, disconnected integration or incomplete validation. “Used in 57” distinguishes legacy and hybrid runs in notes. Tests may be deterministic doubles, artifact checks or real offline model benchmarks; see section 11.

| Component | Implemented | Functional | Tested | Used in 57 | Notes |
|---|---|---|---|---|---|
| Input normaliser | YES | YES | YES | PARTIAL | `classifier.preprocessing.normalise`: HTML removal, NFC, whitespace; legacy only. Hybrid passes raw narrative. |
| ISO15022 detector | YES | PARTIAL | YES | YES | Heuristic field/envelope detection, not a conformance detector; all 57 unstructured. |
| Lossless ISO15022 reader | YES | PARTIAL | YES | YES | Raw text, hashes, field spans, sequence paths, unknowns retained; no structured challenge fields. |
| Structured fact extractor | YES | PARTIAL | YES | PARTIAL | Runs on all hybrid cases but extracts zero ISO facts there; subset routing only. |
| MT564 support | PARTIAL | PARTIAL | YES | NO | Partial fields/options/dates/narrative, not full mandatory/network/profile validation. |
| MT565 support | PARTIAL | PARTIAL | YES | NO | Partial instruction-field parsing; no live instruction processing service. |
| MT568 support | PARTIAL | PARTIAL | YES | NO | Narrative extraction plus standalone ledger linkage; semantic supersession incomplete. |
| MT567 support | PARTIAL | PARTIAL | YES | NO | Status fields preserved/routed; no complete acknowledgement/status business processing. |
| MT566 support | PARTIAL | PARTIAL | YES | NO | Opaque confirmation history; no full movement decoder or proof of vote execution. |
| Message/event linker | PARTIAL | PARTIAL | YES | NO | Standalone sender+CORP ledger; not in `pipeline.analyse`. |
| Replacement handling | PARTIAL | PARTIAL | YES | NO | Ledger tests PREV/stale replacement; classifier quarantines REPL instead of consuming reconstructed current state. |
| Cancellation handling | PARTIAL | PARTIAL | YES | NO | Ledger distinguishes event vs instruction cancellation; classifier quarantines CANC, not ledger-resolved final cancellation. |
| Deterministic date rules | YES | PARTIAL | YES | YES | Scoped RDDT A/C/E parsing plus conservative English free-text extractor. Unsupported dates/timezones abstain. |
| Whole-text base Laya | YES | YES | YES | YES | Real model; legacy 30/57 and live saved 7,683-row runs. |
| Whole-text fine-tuned Laya | YES | YES | YES | YES | Real selected encoder checkpoint; legacy 37/57; not default GUI corpus model. |
| Narrow base Laya | YES | YES | YES | YES | Eight questions per passage; hybrid 26/57. |
| Narrow fine-tuned Laya | PARTIAL | PARTIAL | YES | YES | Eight questions inferred but only three supervised targets; hybrid 32/57. |
| Confidence gating | PARTIAL | PARTIAL | YES | PARTIAL | Legacy policy thresholds work; hybrid .70 is evidence/conflict threshold, not an LLM routing gate. |
| Conflict detection | PARTIAL | PARTIAL | YES | YES | Passage YES/NO, deadline differences and parse errors; no general structured/narrative reconciliation. |
| Fallback interface / disabled stub | YES | PARTIAL | YES | NO | Protocol and stub unit test only; pipeline imports but never invokes it. |
| Integrated real local LLM runtime | NO | NO | NO | NO | Host Ollama installation is separate. No application client/model load. |
| LLM semantic prompt/template | NO | NO | NO | NO | Laya question instructions are not a generative LLM prompt. |
| LLM constrained-output schema/decoder | NO | NO | NO | NO | No generative response parsing, schema enforcement or bounded retry implementation. |
| LLM evidence verification | NO | NO | NO | NO | Existing substring checks verify Laya candidates, not LLM outputs. |
| Laya → LLM escalation | NO | NO | NO | NO | No call site, trigger policy, timeout/error path or merged result. |
| Parser/rules → LLM conflict escalation | NO | NO | NO | NO | No resolver; conflicts feed manual status only. |
| Final decision engine | YES | PARTIAL | YES | YES | Explicit hybrid rules plus separate legacy policy; disconnected from persistent state and absent LLM. |
| Manual-review routing | PARTIAL | PARTIAL | YES | YES | Legacy persisted queue/reviews work. Hybrid sets review flags, but benchmark outputs do not enter the live review queue. |
| Provenance/audit trail | PARTIAL | PARTIAL | YES | YES | Strong legacy append-only ledger; hybrid mostly files/snapshots, with some provenance indexed post-run. No LLM audit events. |
| Customer GUI provenance view | PARTIAL | PARTIAL | YES | NO | Live browser verified; source links/rules/scores present. Public hybrid inspection has no model; examples are saved analyses. |
| LLM metrics/dashboard | PARTIAL | NO | PARTIAL | NO | Zero/off labels exist; no LLM performance, routing, correction or damage telemetry. |

## 4. Parser audit: corpus absence versus detector failure

The original zero-recognition result alone cannot distinguish absent structure from a weak detector. I independently scanned **all 7,683 unchanged input texts**, not merely the saved parser labels:

| Independent permissive search | Hits |
|---|---:|
| FIN-style opening block markers `{1:`, `{2:`, `{4:` allowing whitespace | 0 |
| ISO field tags anywhere, allowing whitespace: 16R/S, 20C, 22F, 35B, 98 variants, 70 variants | 0 |
| ISO15022 or MT564/565/567/568 textual mentions | 0 |
| Bare CAEV/CAMV/CORP/SEME/sequence words | 281 |

The bare-word hits include ordinary company “Corp” references; they are not qualified ISO fields. A deterministic 25-record sample covered both document types, every supplied language-detection stratum and length quantiles, including the 21,422-character maximum. Manual inspection showed public compensation tables, proxy/governance disclosures, credit/severance/equity contracts and some bilingual employment material, not FIN messages. I separately inspected all nine UNRECOGNISED records: they are mostly numeric/table fragments, **87–770 characters**. Calling all nine “too short” was imprecise: the detector also requires sufficient alphabetic content. Language metadata is heuristic and often wrong on tables; it is not verified multilingual notice coverage.

**Evidence supports A for the supplied excerpt text: no usable ISO15022 syntax was found by either the implemented detector or a more permissive independent scan.** This does not prove the original full filings contained no message attachments, recover structure lost before ingestion, or establish universal detector recall. The parser could miss indented, escaped, damaged or unsupported encodings/profiles in future data. No independent real-production-message recall benchmark exists.

Actual local corpus inventory:

| Source category | Count | Meaning |
|---|---:|---|
| OFFICIAL_EXAMPLE | 1 | Short literal excerpt from Clearstream's illustrative MT564 disclosure example; not a full production message. |
| PUBLIC_REAL_EXAMPLE | 0 | No production messages incorporated. |
| Standards-derived synthetic, non-mutated | 1,100 | Deliberately partial generated fixtures, including 25 four-message synthetic lifecycle scenarios. |
| Synthetic mutations | 500 | Mutated partial fixtures; some remain readable/partial rather than invalid. |
| Total stored corpus items | 1,601 | **Not 1,601 real messages.** |

Public documentation with additional examples was researched, but those examples were not all incorporated. The single incorporated official example is a disclosure event, not a genuine linked meeting/proxy production pair. Its published 17-character SEME exceeds the generic 16-character limit and is preserved as unknown. Generated tests do not establish production quality.

`hybrid/parser.py` supports a field subset, nested/repeated sequence paths and exact source spans. It does not validate full sequence grammar/order, all mandatory fields, complete message-specific qualifier rules, network envelopes, ISIN checksums or complete custodian profiles. Date alternatives F/J/K are not decoded. It deliberately never returns VALID_ISO15022: structured inputs remain PARTIAL or ISO-like. The decoder is mostly tag/qualifier/sequence based, not a complete separate grammar for every MT.

## 5. Laya training audit and lineage

Both reported fine-tunes start from local official base Laya at `data/models/laya/multilingual`, not from the historical smoke model and not from one another. Installed SDK: `laya==0.4.8`; underlying model metadata identifies `jhu-clsp/mmBERT-base` encoder. Both are non-generative decision-model training runs.

| Attribute | Legacy whole-notice selected fine-tune | Hybrid narrow-predicate fine-tune |
|---|---|---|
| Source | Supplied unchanged `laya_voting_synthetic_500.zip` | Same supplied ZIP |
| Training file | `synthetic_train_300.csv` | Same exact 300 memberships |
| Validation file | `synthetic_validation_100.csv` | Same exact 100 memberships |
| Training rows / unique texts | 300 / 214 | 300 / 214 |
| Validation rows / unique texts | 100 / 84 | 100 / 84 |
| Train+validation unique texts | 271 | 271 |
| Supervised targets | votable, share_blocking, poa_required, other_restriction, deadline_status | votable, share_blocking, poa_required |
| Training question-items | 1,500 | 900 |
| Independent expert-labelled test | 0 | 0 |
| Supplied synthetic frozen test | 100 rows, 80 unique texts; previously scored | Not reused/evaluated for this new narrow checkpoint |
| Other diagnostics | Unchanged 57-case challenge | Same 57-case challenge plus 17 new authored minimal-pair cases |
| Epochs | 4 | 4 |
| Encoder / head learning rate | 2.5e-5 / 1e-4 | 2.5e-5 / 1e-4 |
| Minimum LR / weight decay | 1e-6 / .01 | 1e-6 / .01 |
| Seed | 42 | 42 |
| Encoder frozen? | No | No |
| Loss / effective batch | soft CE; micro 1 × accumulation 8 | Same |
| Token budgets | max_len 2048; head_max_len 256 | Same configured budgets |
| Calibration | Validation-only temperatures; no internal calibration split | Same, only three labelled questions |
| Selection | Full encoder vs head-only, validation all-factor exact match first | One predeclared full-encoder four-epoch candidate |
| Local checkpoint | `data/models/supplied-synthetic-v1/encoder-4ep` | `data/models/narrow-v1` |
| Weight SHA-256 | `71f2eebab410793aeddf7475acc82aea27aacc047d1f43980c5dfcfe616982ab` | `e034d36e9ee229f109d88ff06e3365c9e024cccdbfca8429f5d33a4496d7b58b` |

The legacy model reads the complete normalised notice and predicts five factors; its customer status is deterministic. It is **not** a separately trained mutually exclusive seven-class head with auxiliary labels. The narrow model is trained on whole synthetic source states for three questions, but evaluation decomposes notices into sentence/physical-line passages. That train/inference-unit mismatch is a real limitation.

All 500 supplied rows contain 328 unique raw text hashes. The selected legacy candidate reports 100/100 validation all-factor exact match on the supplied synthetic split, versus 37/57 on the regression challenge. The source split is not independent: 27 unique texts are shared by train/validation and 41/100 validation rows duplicate training text. The known exact/near split overlap was retained under the explicit original dataset protocol, not prevented by the generic leakage machinery. Synthetic validation accuracy is consequently optimistic evidence of generalisation. In addition, many supplied OPEN labels lack an explicit deadline; training those conventions conflicts with the stricter challenge's temporal expectations.

### Challenge contamination checks — and the historical exception

For the 400 TRAIN+VALIDATION rows, this audit checked normalised equality, containment of one complete text in another, and numeric-masked five-word-shingle Jaccard similarity against all 57 challenge texts. Results: **zero exact matches, zero whole-text containment matches, zero >=.85 near matches**; maximum Jaccard was approximately **.05714**. Both reported model manifests and training entrypoints use only the supplied train/validation sources. The original challenge file hash is `0e2f5d991a33deed25f8e9a33682185071c5ff35afd2df9179c1f8565dd17649`, still covered by the historical freeze check.

This supports no direct/surface-copy contamination of the two reported fine-tunes. It **cannot prove that an AI-author never derived a semantic paraphrase from a challenge concept**. Their generation lineage is not sufficiently documented to certify that. The challenge has also been inspected repeatedly for error analysis and is not blind to the experiment designer.

There is a separate, historical **`data/models/synthetic-smoke-v1` checkpoint trained using challenge fixtures**. Its manifest allocates the 57 cases as 29 train / 12 validation / 16 test; it labels the source as a mechanics smoke, not golden data. `EXCLUDED_FROM_STUDY.json` explicitly marks it ineligible, contaminated for challenge evaluation and inactive. **It must not be used for any challenge-quality claim.** It is not the parent of either reported fine-tune. Thus a blanket statement that the challenge has “never entered any training anywhere in this repository” would be false, even though the reported 37/57 and 32/57 model lineages exclude it.

The earlier supplied-test protocol also discloses that `synthetic_all_500.jsonl` was read into lines before the strict protocol, with two test rows surfaced. Subsequent training/tuning used the whitelisted CSVs and blind predictions were persisted before the scoring stage opened the answer key. This is not pristine file-access-blind independence; see `EXPOSURE_DISCLOSURE.json`. No new answer-key access occurred in this audit.

Evidence: [legacy training implementation](../../training/train.py), [supplied protocol](../../training/synthetic_protocol.py), [narrow training](../../training/narrow.py), `training-manifest.json`, `narrow-v1/protocol.json`, `training-result.json` and both frozen manifests.

## 6. Exactly which three predicates were trained

They are **votable**, **share_blocking** and **poa_required**. Each has 300 labelled training rows, but only 214 distinct training texts. Counts below are row counts, not independent notices; labels are AI-synthetic, not expert verified.

| Target | Training distribution | Validation base → fine | Challenge base → fine |
|---|---|---|---|
| votable | YES 237, NO 38, UNCERTAIN 25 | 54/100 → 84/100 | 31/54 → 38/54 |
| share_blocking | YES 32, NO 243, UNKNOWN 25 | 11/100 → 80/100 | 3/11 → 8/11 |
| poa_required | YES 36, NO 239, UNKNOWN 25 | 77/100 → 84/100 | 8/8 → 5/8 |

Important class-sensitive results after narrow passage aggregation:

- Fine-tuned blocking validation: **0/11 YES cases recognised as YES**; all 11 become UNKNOWN. The 80% overall agreement is driven by 74 correct NO and six correct UNKNOWN labels. It is not evidence of useful blocking recall.
- Fine-tuned POA validation: three of 13 YES cases recognised, **23.1% positive recall**. Ten become UNKNOWN.
- Fine-tuned challenge: blocking YES recall 2/3; POA YES recall 2/3; votability YES recall 35/36. The samples are small and partial.
- Validation raw aggregation can return UNKNOWN for votability; pipeline status mapping converts that to UNCERTAIN. Raw validation and decision-level challenge denominators/normalisations therefore need to be read explicitly, not casually combined.

Intended restriction predicates with **no domain-trained specialist target in the narrow checkpoint**:

1. `registration_required`
2. `beneficial_owner_disclosure_required`
3. `split_voting_restricted`
4. `securities_lending_recall_required`
5. `other_voting_restriction` — the new residual predicate, not the legacy broad `other_restriction`.

They do receive predictions from the same generic/fine-tuned Laya model, but that is transfer inference, not supervised training for those questions. A shared encoder has changed, so “untrained target” does not mean “untouched base-model weights”. The old broad other-restriction target was trained only in the legacy model; it cannot substitute for five missing independent targets. The 17 authored minimal-pair diagnostics provide tiny checks, not domain validation: base 15/17, narrow fine-tune 13/17.

## 7. What confidence actually means

The SDK computes native option distributions as `softmax(logits / temperature)` and rounds probabilities to four decimals (`laya/agent.py`, `_answers`, around lines 1330–1370). For choice questions its separate `confidence` field is entropy based; `answer_confidence` is another SDK field. Neither should be confused with the app's policy score.

**Legacy policy score:** minimum across the five factors of the winning native option probability. This is a heuristic aggregation of real native probabilities, **not a native final-status probability and not a calibrated probability that the notice decision is correct**. The SDK entropy field remains in raw answers but is not used by the app gate. The app's score is computed, not hard-coded. The SDK also exposes an action-head `act_probability` and base-model metadata contains an escalation cost; neither is wired to a generative model call by this application.

**Narrow passage confidence:** native probability of the selected option for that predicate/passage; margin is largest minus second-largest option probability. With default aggregation, the highest-confidence passage is selected unless a confident YES/NO conflict causes abstention; on that conflict, document `confidence`, `margin` and evidence become None, while the retained scores still describe one selected passage. There is no calibrated document probability or aggregate customer-status probability. Evidence is offered only for YES with native passage confidence >=.70 and no reported truncation. All semantic evidence is a candidate, not independently verified support.

Both fine-tuning pipelines call official validation-only temperature fitting. Actual persisted temperatures are **[1.0, 1.0, 1.0]**, with empty per-option maps: 500 legacy validation question records and 300 narrow records. Thus the fitting step exists but these artifacts apply neutral scaling. No empirical real-notice calibration guarantee follows from it, and minimum/max passage aggregation is not calibrated. Original base config also contains neutral temperatures. High-confidence narrow errors remain: ten challenge cases have a failing directly scored predicate >=.98. There is no LLM confidence mechanism.

### Actual routing conditions

Legacy `Thresholds.action(confidence, blocked)`:

```text
if score is None/nonfinite/out of [0,1], or blocked:
    MANUAL_REVIEW
else if automation_enabled and score >= .98:
    AUTO_CLASSIFY
else if score >= .70:
    CLASSIFY_AND_REVIEW
else:
    MANUAL_REVIEW
```

Blocked is true for any review reason computed before policy evaluation: uncertain vote; any unknown restriction; YES vote with UNKNOWN deadline; truncated context; SDK option-budget warning; or NO vote with an affirmative restriction. Current configured `automation_enabled=False`, so **AUTO ACCEPT LAYA never occurs**. CLASSIFY_AND_REVIEW also requires human review. Legacy challenge action counts: base 53 MANUAL_REVIEW + four CLASSIFY_AND_REVIEW; fine-tuned five + 52 respectively. Neither has auto processing.

Hybrid routing is different:

```text
score >= .70: eligible for conflict detection / YES evidence selection only
confident YES and NO passages for same predicate: UNKNOWN, confidence=None
reported context truncation: that passage's value becomes UNKNOWN
otherwise: highest-confidence passage may still yield a label even below .70
any parse/date/semantic conflict: decision rule R1
all outcomes: manual_review_required=True; automation_enabled=False
LLM escalation condition: NONE — no implemented route or invocation
```

The proposed quality-gate configuration requires at least 200 test records and 200 independent groups, .98 votable recall, .90 macro F1, <=.01 high-confidence error rate and a .98 lower-bound automation-precision target, plus class support and coverage. `assess()` reports pass/fail and always returns automation disabled. **It is not called as a mandatory interlock inside `LayaClassifier`**: manually editing its config to `automation_enabled=True` would invoke the numeric policy without a quality-gate assessment. Current defaults/runs remain false; a production activation interlock is incomplete.

A subtle issue: UNKNOWN truncation passages retain their native winning confidence. They can outrank a useful nontruncated passage and yield an aggregate UNKNOWN with a high numeric confidence. Physical narrative lines are segmented separately, so normal 35-character ISO wrapping can split semantic context. Confident NO in an unrelated sentence can conflict with a genuinely affirmative restriction elsewhere. Explicit supersession is not reliably reconciled. These are implementation limitations, not evidence an LLM handled the cases.

## 8. Actual decision engines and precedence

There are **two separate policies**, not one unified production engine.

### Legacy policy (`classifier.schema.Decision.status`)

```text
if votable == UNCERTAIN: UNCERTAIN_MANUAL_REVIEW
elif votable == NO: NOT_VOTABLE
elif deadline_status == PASSED: DEADLINE_PASSED
elif any of blocking/POA/other is UNKNOWN: UNCERTAIN_MANUAL_REVIEW
elif more than one restriction is YES, or other is YES: VOTABLE_WITH_RESTRICTION
elif POA == YES: POA_REQUIRED
elif blocking == YES: SHARE_BLOCKING
else: VOTABLE
```

UNKNOWN deadline can coexist with display status VOTABLE, while the separate review guard routes it to human review. Default legacy deadline status is itself a Laya question; the optional deterministic-v2 experiment is not the default live corpus configuration.

### Hybrid assembly (`hybrid.pipeline.analyse`)

```text
parse raw input
CAEV -> meeting_event metadata (not itself used to establish votability)
voting-related CAOPTN code -> structured votable=YES
route narrative -> Laya, if a model was passed
if structured votable exists: it takes priority; omit Laya votable question
otherwise use Laya votability (UNKNOWN becomes UNCERTAIN)
RDDT with usable offset -> deterministic comparison
if unstructured and no structured comparisons -> English deadline extractor
restrictions -> Laya predicate values, missing -> UNKNOWN
conflict = parse errors OR conflicting CAEV codes OR deadline conflict
           OR any per-predicate passage YES/NO conflict
REPL or CANC message -> quarantined=True; no event-ledger lookup
then decide(facts)
```

### Hybrid final rules (`hybrid.rules.decide`), exact precedence

```text
R1 conflict OR quarantined                 -> UNCERTAIN_MANUAL_REVIEW
R2 cancelled                              -> NOT_VOTABLE
R3 votable == NO                          -> NOT_VOTABLE
R4 votable != YES                         -> UNCERTAIN_MANUAL_REVIEW
R5 deadline_status == PASSED               -> DEADLINE_PASSED
R6 any of seven restrictions == YES        -> VOTABLE_WITH_RESTRICTION
R7 deadline_status != OPEN
   OR any missing/UNKNOWN restriction     -> UNCERTAIN_MANUAL_REVIEW
R8 otherwise                              -> VOTABLE
Every branch: manual_review_required=True, automation_enabled=False
```

R6 can report a known restriction despite UNKNOWN deadline/other attributes; it still requires review. R1 outranks all otherwise actionable statuses.

**Missing precedence/integration:**

- No LLM enters this function. Its conceptual entry would be after semantic/conflict assessment and before final fact assembly/decision, with explicit provenance and authority checks; that code does not exist.
- No general structured-fact versus narrative conflict resolver exists. A structured YES can suppress the Laya votability question, so disagreement is not actually measured. `meeting_event=NO` is not in `decision_facts`, nor a general semantic conflict check.
- The frozen v1 pipeline treats an unknown CAEV as a negative meeting code. The service-only wrapper corrects this to UNKNOWN; the 57 unstructured cases are unaffected.
- `EventLedger.event()` is not called. Its cancellation/current-state results never populate pipeline facts. R2 is unit tested but unreachable from `analyse()` as currently assembled because it never supplies `cancelled`.
- The event ledger retains history, but its current-value key `(fact name, sequence path)` lacks field occurrence/qualifier. Repeated same-name fields in one sequence can collapse in current-state projection. Option sequence position is not a full stable option identity across replacements. Omitted replacement fields are retained rather than resolved against a full sender profile. Out-of-order recovery and semantic MT568 supersession are incomplete.

## 9. GUI audit — live browser inspected, no data changed

| Display | Status | Observed behaviour |
|---|---|---|
| Raw source | YES | Full public notice and selected raw fixture visible. |
| Parsed structured fields | PARTIAL | Available for supported fixture fields; public excerpts have none. Not full ISO validation. |
| Laya result | YES | Saved whole-text result for public corpus; saved narrow results in selected fixture examples. |
| Laya confidence / score | YES | Legacy minimum-winning-factor policy score; narrow native passage score; labels distinguish scope. |
| LLM result | NO | No model result exists. |
| Whether LLM was invoked | PARTIAL | Performance page shows zero escalation/off metadata; no per-record invocation audit or genuine execution telemetry. |
| LLM model | NO | No selected/integrated LLM identity. |
| Evidence | PARTIAL | Source-field links, model-score/criteria links and source-exact Laya candidate spans; not guaranteed semantic support. No LLM evidence. |
| Deterministic rule results | YES | Hybrid status, rule ID/reason, deadline calculation and field-routing trace shown. |
| Final decision | YES | Legacy and inspection/demo decisions visible, but from separate pipelines. |
| Source/provenance of each fact | PARTIAL | Parser fields source-linked; legacy assessments link to scores; not a unified event/model/fallback fact ledger. |
| Manual-review reason | PARTIAL | Legacy review reasons and hybrid rule reason visible; no complete explanation of each unresolved conflict/unknown. |
| Human correction/history | YES | Existing review workflow and revisions; no expert reviews currently saved in live DB. |
| Event history | PARTIAL | Clearly synthetic saved demonstration with current/superseded deadline sources, not live event ingestion. |

On a live generated MT564 example, the narrow model's votability YES/100% candidate evidence was **“No power of attorney is required.”** That quotation is source exact but does not establish votability. This directly demonstrates the difference between substring validity and semantic support. The UI labels it as an unverified candidate; an exact-substring check alone is insufficient for a production explanation.

The browser connection supplied by the skill could not initialise in this environment; I used the already-installed Playwright/Chrome for read-only live inspection. No reviews, batch jobs or other write actions were submitted.

## 10. Local inference infrastructure and hardware

Read-only discovery, no model selected or loaded:

| Item | Actual finding |
|---|---|
| Machine | Apple M3 Max, arm64; 16 CPU cores; Apple integrated GPU |
| Unified memory | 64 GiB total; approximately 32.1 GiB available at audit time (dynamic) |
| Available disk | Approximately 463 GiB on project volume |
| PyTorch | 2.14.1, MPS built and available; CUDA unavailable |
| Project Transformers | 5.20.0; installed library, not a generative application integration |
| Ollama | Binary installed; service 0.34.3 responds at 127.0.0.1:11434; `/api/ps` returns empty models |
| llama.cpp | `llama-cli` and `llama-server` binaries installed under Homebrew; no application use |
| LM Studio | App running, `lms` CLI installed; default API port 1234 refused connection |
| MLX | Project venv lacks mlx/mlx-lm; LM Studio has bundled MLX and llama.cpp backends installed |
| Other project runtimes | No llama-cpp-python, Ollama Python client, vLLM or Outlines package in the project venv |
| Integration interface | Only `SemanticFallback.analyse(narrative, structured_context, requested_predicates) -> dict`; disabled implementation only; no client or response schema |

Ollama installed model metadata:

| Local tag | Reported parameters | Quantisation | Approx. stored bytes |
|---|---|---|---:|
| qwen3.6:latest | 36.0B | Q4_K_M | 23,938,333,577 |
| glm-4.7-flash:latest | 29.9B | Q4_K_M | 19,019,270,852 |
| gpt-oss:20b | 20.9B | MXFP4 | 13,780,173,724 |
| gemma3:latest | 4.3B | Q4_K_M | 3,338,801,804 |
| gemma3:270m | 268.10M | Q8_0 | 291,554,930 |
| nomic-embed-text:latest | 137M | F16 | 274,302,450 |

Nomic is an embedding model, not a generative fallback. Mutable local tags and runtime-reported parameter counts are inventory, not a verified publisher checkpoint identity. Before any future experiment, pin the full model digest and actual runtime/template. Current relevant installed digests: gpt-oss `aa4295ac10c3afb60e6d711289fc6896f5aef82258997b9efdaed6d0cc4cd8b8`; GLM `d1a8a26252f18b34301218d22abd2620a65b85ba4b78987842eb157e01321222`.

LM Studio also has DeepSeek-Math-7B-Instruct Q4_0 and DeepSeek-R1-Distill-Qwen-7B Q4_K_M files. HF caches include Qwen3.5-9B MLX 4-bit and other models; cache directory presence alone is not proof of complete weights or working serving. None was exercised for this application audit.

**Capacity estimate, not a measured benchmark:** 3–9B four-bit models are a comfortable initial range, with several GB of weights plus runtime/KV overhead. Installed 20–36B quantised models (roughly 13–24 GB stored weights) are plausible serial local candidates on 64 GiB, using a bounded context such as 8k and careful live-memory accounting. Full advertised 200k+ context is not a memory/latency promise. 70B four-bit weights may approach 40–50 GB before working/KV memory and are not a sensible first controlled test with current memory use. No tokens/sec or LLM latency estimate has been measured here.

## 11. Test-coverage audit

The saved application test log reports **1,829 passed**, 126 opt-in checks deselected. I independently collected current test identities without running inference: **1,829/1,955 collected, 126 deselected**, matching that count. The 126 consist of 114 opt-in real-Laya semantic tests and 12 browser tests. These counts are parameterised test instances, not 1,829 distinct semantic scenarios.

Exclusive breakdown of the 1,829:

| Category | Instances | Evidence |
|---|---:|---|
| Generated partial fixtures + one official excerpt | 1,101 | `test_iso_parser::test_standards_derived_exact` |
| Malformed/mutated fixture preservation | 500 | `test_iso_parser::test_malformed_corpus_lossless` |
| Parser deterministic unit/input/date/scope checks | 28 | Remaining non-property parser tests |
| Parser property/fuzz test functions | 4 | Unicode, line endings/envelope, valid dates, segment coverage |
| Hybrid final-rule tests | 15 | `test_hybrid` restriction/rule table/unknown tests |
| Event-state/link/replacement/cancellation tests | 8 | Standalone `EventLedger` tests |
| Disabled fallback stub test | 1 | Asserts zero external calls on `DisabledFallback` |
| Chunking/aggregation/structured routing/unknown-CAEV guard | 4 | Remaining `test_hybrid` tests |
| GUI/API workflow + hybrid read-only API | 21 | `test_workflow` 16; `test_hybrid_api` 5 |
| Training/review protocol/isolation + grouping migration + hybrid artifact integrity | 22 | Research protocol 11; training 4; migration 3; hybrid artifacts 4 |
| Core normalisation/schema/mapping/threshold/native-score contract/grouping | 68 | `test_core`, uses ContractAgent for classifier calls |
| Decision evidence/source links | 7 | `test_decision_evidence` |
| Metrics/calibration/curves/layer separation | 22 | `test_metrics` 8; synthetic metrics 9; layer metrics 5 |
| Deadline research/study immutability/quality gates | 27 | `test_research` |
| Challenge manifest integrity | 1 | Challenge count/IDs/reference date, no inference |
| **Total** | **1,829** | |

The saved parser verification artifact reports 4,402/4,402 core reference assertions: these chiefly check SEME/CORP/CAEV/function across generated items (plus the official excerpt), not 4,402 independently validated production field types. Many fixture tests share the same generator and assertions. Field/date/options unit checks add specific coverage but do not establish full message conformance.

The four Hypothesis functions have configured maxima totalling 525 examples. The quiet historical test log does not establish how many distinct generated examples actually ran; they are four collected tests, not 525 independent test instances. The 500 mutation tests primarily assert no crash/lossless preservation; they do not demand rejection of every mutation or fully validate malformed-field diagnosis.

**Tests executing a real LLM: 0.**  
**Tests executing Parser/Rules → Laya → real LLM → Decision: 0.**  
**Real generative fallback routing tests: 0.**

No live model training or real-Laya inference is performed by the 1,829 selected software checks: classifier-dependent workflow tests inject `ContractAgent`, training integration replaces `finetune/load`, and hybrid artifact tests read saved real-model outputs/reload certificates. That is valid contract testing, but it is not fresh semantic validation.

The **12 browser tests** cover dashboard/source counts, search/filtering/detail, isolated corrections/golden revisions/persistence, metrics/errors/confusion, export/demo, batch/reproduction, restart, research displays, Unicode evidence, parser provenance, hybrid errors and synthetic event history. Their server explicitly replaces batch classification with `ContractAgent` on an isolated SQLite copy. Some views read real pre-existing saved predictions. None calls a real LLM, and fresh batch UI checks do not execute real Laya.

Separate unchanged legacy real-Laya tests were previously rerun: **47 failed, 68 passed** including the one manifest check (30/57 base, 37/57 fine, plus manifest). Their failures remain. Hybrid real model benchmarks are scripts recording **26/57 and 32/57**, not 57 all-passing application tests. Saved reproduction evidence shows identical native outputs for both models on 57 challenge + 100 validation records in a fresh workspace; this does not add any LLM evaluation.

## 12. Candidate models for a later decision — none selected

These are a shortlist for review, not an installation instruction or an assertion they will beat Laya. Public publisher sources were checked on 16 October 2026; local availability comes from metadata discovery above.

| Candidate | Why it is worth testing | Local route / limitation |
|---|---|---|
| **gpt-oss-20b** | Publisher describes an open-weight ~21B model with 3.6B active parameters and configurable reasoning. Useful capable reasoning comparison with a relatively modest local footprint. [Official model documentation](https://developers.openai.com/api/docs/models/gpt-oss-20b) | Already installed in Ollama as `gpt-oss:20b`, MXFP4. Pin digest, Harmony/template and reasoning settings; schema/evidence behaviour untested here. |
| **GLM-4.7-Flash** | Publisher's 30B-A3B MoE provides a different reasoning architecture and useful capability/latency comparison. [Publisher model card](https://huggingface.co/zai-org/GLM-4.7-Flash) | Already installed in Ollama, Q4_K_M, ~19 GB. Larger memory cost; reasoning mode/sampling and JSON compliance need controlled validation. |
| **Qwen3.5-9B** | Smaller 9B multilingual model, useful for testing whether a compact local generator can resolve the specific semantic failures economically. [Publisher model card](https://huggingface.co/Qwen/Qwen3.5-9B) | A community MLX 4-bit cache is present and LM Studio MLX backends exist. Full checkpoint completeness/serving must be verified after selection; this is a conversion, not publisher-original quantised weights. |

No model-specific temperature, context budget, fallback threshold or prompt has been configured for the application. Do not infer task quality from publishers' general benchmarks. The existing machine inventory means a future experiment need not start by arbitrarily installing another model/runtime.

## 13. Actual gap register

### COMPLETE — within the explicitly tested scope

- Local official Laya loading/inference and five-factor whole-notice baseline.
- Saved legacy full-corpus runs, real base/fine challenge runs, native scores and model identities.
- Actual selected five-factor fine-tune and three-target narrow fine-tune, with source memberships, configurations, seeds, losses and checkpoint files.
- Deterministic fixture generation/provenance, bounded lossless parser checks and full public-text detection audit.
- Source-exact span validation and customer navigation links for parsed fields and Laya candidates.
- Existing whole-text append-only prediction/review ledger, golden revision history and group/split guards.
- Explicit conservative policies, disabled automation, software metrics and disclosure of missing expert accuracy.

These completed pieces do not establish complete production architecture or safe autonomous decisions.

### PARTIAL

- Standards parser: limited grammar/profile coverage, no full VALID decision, almost no genuine message coverage.
- Input normalisation: legacy/hybrid paths differ; no common routing-aware normalisation boundary.
- Narrative chunking/evidence: physical-line splitting, weak supersession, conservative but lossy conflict aggregation, exact quote may not support conclusion.
- Semantic specialist coverage: three of eight inferred questions supervised; five intended restriction targets lack compatible labels.
- Confidence: real native scores and calibration machinery, but no demonstrated calibrated decision confidence or functional fallback gate.
- Conflict handling: no comprehensive structured/narrative or cross-predicate reconciliation.
- Event state: standalone ledger and tests; current projection can collapse repeated facts; no integration into final classification, automatic recovery or complete option identity.
- Review/audit integration: full legacy workflow, hybrid file artifacts and demo snapshots, no unified hybrid/LLM persisted review/fact history.
- Benchmark truth: synthetic leakage, tiny partial challenge labels, no independently expert-verified structured events.
- GUI: useful existing provenance screens, but offline examples and rule-only public inspection must not be mistaken for live model/fallback routing.

### MISSING

- Actual generative LLM adapter and model selection/configuration in the application.
- LLM semantic prompt with structured context, requested predicates and source-role/instruction boundaries.
- Constrained generative output schema/decoder, validation, error handling, timeout/context/retry budgets.
- LLM quotation validation and semantic-support policy; authoritative structured-fact protection and visible disagreement handling.
- Laya → LLM escalation triggers and dispatch; parser/narrative conflict escalation.
- Merge/reconciliation logic and final facts carrying both model sources and unresolved conflicts.
- LLM invocation/correction/damage/latency/resource/cost audit records and GUI fields.
- Real-LLM unit/integration/e2e/quality benchmarks; complete intended architecture test.
- A common controlled A–E comparison. The current 32/57 is not that comparison.
- The proposed 3,000-example dataset and its experiment: stopped before creation/training.

### IMPLEMENTED BUT NOT EVALUATED — or not evaluated to the claimed scope

- Host local inference runtimes and installed model files: discovered but never exercised on these notices in this application.
- `SemanticFallback` interface and `DisabledFallback`: implemented placeholder contract, **not an unevaluated real LLM implementation**. No actual LLM layer exists to evaluate.
- Standalone event state and several parser paths: tested on synthetic fixtures, not validated on a representative genuine custodian feed or in the challenge's live pipeline.
- Five new restriction questions: generic/transfer outputs checked on tiny authored minimal pairs, not evaluated on a meaningful domain-labelled test set.
- Production precision/calibration/automation quality: machinery exists, credible independent public-data labels do not.
- Disagreement as a useful review signal, correction-versus-damage benefits and LLM fallback coverage: never measured.

## 14. Next controlled experiment — proposal only, not run

First choose a local LLM after reviewing this audit. Do not resume corpus generation, train another Laya candidate, tune prompts against challenge answers or install models as part of this audit.

Freeze the existing 57 texts/expectations/hash and the selected 37/57 legacy checkpoint. Use separate validation material to settle the LLM template, requested schema, date/reference policy, context/token budgets, trigger thresholds, temperature/reasoning/seed settings, timeout/retries, evidence validation and merge policy. Record all settings/model digests before looking at new 57-case results. The 57 remain a **fixed, repeatedly observed regression challenge**, not a fresh blind independent test. No examples or paraphrased challenge rows enter training, few-shot prompts or validation. A later independent expert-labelled real test is still required.

| Arm | Frozen proposed route | What it isolates |
|---|---|---|
| A | Official base whole-notice Laya → preserved legacy status policy | Reproduce 30/57 baseline. |
| B | Selected legacy five-factor whole-notice fine-tuned Laya → same policy | Reproduce 37/57. Keep this checkpoint fixed for the comparison. |
| C | Exactly B → actual local LLM only on predeclared uncertain/low-score/conflicting inputs → explicit merge → same final policy | Fallback's incremental repair **and damage** compared with B. |
| D | Actual same local LLM on every full notice → same factor schema and final policy | LLM-only capability, latency and failure reference. |
| E | Optional detector/parser + explicit deterministic/date/state rules → same fine-tuned Laya checkpoint as B on narrative → same fallback as C → explicit decision policy | Structural/rule contribution without simultaneously switching to a different narrow checkpoint. |

E must pass unstructured notices to semantics; parser success is not a prerequisite. With zero ISO messages among these 57, E cannot demonstrate ISO parsing benefit. Any C/E difference must be attributed to explicit free-text date/rule/routing differences, not claimed as a structured-feed win. Genuine linked ISO events need a separate independently labelled evaluation later. If the current narrow checkpoint is also tested, label it an additional arm rather than silently substituting it into E.

Suggested fallback-trigger specification to validate and freeze later: low **defined** native Laya score; any UNKNOWN/UNCERTAIN required factor; truncation/context failure; passage/cross-predicate conflict; or authoritative-structured/narrative disagreement. Complex conditional language needs a specified detector or model predicate; it must not be a subjective hindsight trigger. Log trigger reason(s), inputs/context and source spans for every invocation. Avoid trigger choices based on whether a particular challenge prediction is known wrong.

The generative result should carry constrained factor labels, explicit unknowns, source-exact evidence offsets/quotations and contradiction reports. Validate required keys/enums/types and quotations before using it. Keep authoritative structured facts immutable; conflicting semantic claims remain separately sourced and require review. LLM self-reported “0.91” is an unvalidated self-assessment, not a calibrated probability. If no valid probability mechanism exists, report LLM confidence unavailable rather than invent one. Invalid JSON/evidence, runtime failure, unresolved conflict or missing critical facts must produce explicit review outcomes, with no silent correction.

Persist every arm's predictions before scoring. Use **exactly the same available-reference masks**: votability 54 cases; blocking 11; POA eight; broad other four; deadline 14; final customer status only four. A case-correct/57 metric may reproduce the existing all-supplied-assertions convention, but cannot be described as fully labelled event accuracy. Restriction micro accuracy can use the 23 existing blocking/POA/broad-other assertions, with per-field results and denominators alongside it. Do not impute absent labels as NO. To score all seven new predicates, create a separately versioned, expert-adjudicated annotation sidecar or a new test corpus; do not silently change the original 57 expectations.

For every arm, report: cases passing all available assertions /57; per-field accuracy/F1/precision/recall including UNKNOWN outcomes; restriction micro/macro agreement with explicit supports; customer-status agreement /4; policy manual-review rate; separate unresolved-status rate; explicitly defined high-confidence errors; median/p95 end-to-end warm latency; separate cold-load time; failures/timeouts; and source/model/configuration identity.

For C/E additionally report:

- LLM invocation count and fraction of all 57, plus trigger breakdown and subset eligibility.
- **Repairs:** B wrong → final correct, with case IDs, field changes and evidence.
- **Damage:** B correct → final wrong, with case IDs, field changes and evidence.
- Correct → correct changes and wrong → wrong changes separately; abstentions/conflicts visible.
- Net case gain = repairs − damage; rates with both invoked-case and relevant before-state denominators.
- Per-field repairs/damage, since a case can fix one factor and break another.
- Laya/LLM agreement against known truth; disagreement is not proof the LLM is right.
- Added LLM and total latency, invocation volume and peak memory. Use the same hardware, measured budgets, no concurrent training, and bounded/reported repeats.

Keep automation disabled in every arm. Operational manual-review policy therefore remains 100%; separately labelled hypothetical review/automation eligibility may be studied without enabling it. No 57-case or synthetic result is sufficient to assert customer precision or pass the current expert-data quality gates.

## 15. Review decision requested later

The immediate architectural gap is the **absent integrated local LLM fallback and its evaluation**, not a hidden or merely disabled model. Local infrastructure is already available, but choosing a model and wiring it into confidence/conflict routing is new work. This report proposes that work; it does not perform it. The next choice belongs after your review of the gap and model shortlist.
