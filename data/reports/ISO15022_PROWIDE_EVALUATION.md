# ISO15022 — Prowide + lenient recovery evaluation

Retrieved/tested 2026-10-17T09:43:08.636595+00:00. The Qwen domain study is a separate experimental condition; parser integration does not mutate its datasets, prompt or model weights.

## Version and integration

`com.prowidesoftware:pw-swift-core:SRU2025-10.3.20`, Standards Release2025, Apache-2.0; adapter `prowide-jsonl-v1`. Current Maven metadata was archived. Prowide documents Java11+; the local test JVM was GraalVM Java21.0.1. Gson2.13.2 frames JSON. Exact transitive dependency versions and SHA256s are in `tools/prowide/DEPENDENCIES.lock.json`.

A persistent, local stdin/stdout JSONL helper isolates Java objects from Python/FastAPI. It starts lazily, serializes requests with a lock, caps JVM heap at256MiB, and has a30-second response timeout. There is no listening Java network service and no notice is transmitted externally. First parse includes process/class loading; subsequent calls reuse the helper. Failed parsing preserves raw input/error and falls back to recovery. Missing Java/JAR is an explicit adapter warning, not data loss.

**Core parsing is not full SWIFT network/business-rule validation.** Successful results are `PARSED_NOT_VALIDATED` / `standards_validated=false`; never VALID ISO15022 solely because Core returned an object. Full mandatory-field, market and event-lifecycle conformance remains outside this adapter.

## Public evidence and provenance

| Organisation / document | URL | Relevant finding | Example / use | Licence limitation |
|---|---|---|---|---|
| Prowide Core product documentation | https://www.prowidesoftware.com/products/open-source/core | All MT categories; typed components; Java11+; Apache2 | API architecture | Documentation copyright; summarized |
| Prowide README | https://raw.githubusercontent.com/prowide/prowide-core/main/README.md | Full validation is complementary to Core | Capability boundary | Apache2 repository |
| Maven Central metadata | https://repo.maven.apache.org/maven2/com/prowidesoftware/pw-swift-core/maven-metadata.xml | Exact compatible current release | Dependency pin | Metadata; no notice data |
| ISO dictionary MT568 field70a | https://www.iso20022.org/15022/uhb/mt568-30-field-70a.htm | 70E/F qualifier families and line-boundary semantics | Recovery qualifier tests | Public dictionary; no wholesale redistribution |
| Clearstream disclosure MT564 example | https://www.clearstream.com/resource/blob/2224604/f8aba0b45b2add681902be2bef954314/c20019-c20030-l20022-l20033-d20039-mt564-example-data.pdf | Public field excerpt, not complete FIN envelope | Existing short official corpus excerpt | Clearstream copyright; no production-data claim |
| Prowide MT564ParserTest test564_1 | https://github.com/prowide/prowide-core/blob/34514beab84c9f9fa134c9f9b0e05e340e38de87/src/test/java/com/prowidesoftware/swift/io/parser/MT564ParserTest.java | Publisher FIN message fixture with nested components | Exact Java-string content imported into restart/components test | Apache2, attribution and LICENSE retained |
| OeKB CSD, Using T2S for Transaction Management, v1.4 June2019 | https://www.oekb-csd.at/dam/jcr:586d6dbf-109c-4261-aac7-e4ccca017e0b/Using-T2S-for-Transaction-Management-SWIFT-ISO15022-Examples.pdf | Additional genuine public examples include MT543/548/547/566 | Researched, not copied into scored corpus | Public document; no redistribution licence asserted |

Prowide developer URLs may contain SRU2026 while MT Core’s artifact remains SRU2025; the artifact/SRU pin is authoritative for this experiment. Public examples may predate it and contain unusual source values; no source value is silently corrected.

## Corpus and extraction comparison

Existing corpus:1,100 standards-derived **partial** fixtures +500 deliberately mutated fixtures +1 Clearstream official excerpt. Added:1 Apache-licensed Prowide publisher message example. Total1,602; **not1,602 real production SWIFT messages**. The original source manifest and custom parser are unchanged; the new publisher example has a separate source manifest. Mutations inherited a synthetic source_type, so their directory/original mutation provenance determines the500-mutant count.

Custom subset: 5406/5406 exact supplied field/absence assertions. Prowide projection: 5404/5406. Scanner narrative/absence: 1000/1000.

The1,100 generated partial fixtures were separately wrapped in clearly synthetic FIN envelopes for Prowide component tests. An envelope does not make a partial fixture standards-compliant. The original partial/unwrapped inputs were also run unchanged. No semantic-model training uses any parser fixtures.

The two Prowide misses are CORP and CAEV in the bare Clearstream excerpt: reference parsing has no FIN block2/4, so declines it. The scanner preserves both raw fields and narrative; the custom subset extracts those values. Both behaviours match their claimed role. On existing standards-derived expected values, both full projections agree. The deliberately small expected-field subset does not establish equal full-standard capability.

Original SUMMARY.json mistakenly treated expected narrative=null as an error. SCORING-REVISION.json corrects absence scoring from persisted outputs and separates mutation provenance. Original outputs, timing and initial score are retained. No test expectation or parser was changed to improve the result.

All1,602 inputs completed without a Python parser/scanner crash. Prowide returned explicit FAILED on751 raw inputs lacking usable headers/text block;851 raw inputs were parseable. The production detector deliberately sent651 to Prowide and951 to recovery. This is not a standards-validity denominator. All1,600 synthetic originals/mutations parsed after an experimental FIN envelope was added, demonstrating why parseability alone must not be called validation.

Covered extraction: message type; ordered fields; nested/repeated sequence identity; qualifier; typed component arrays; CORP/SEME/PREV/RELA;35B ISIN/description; CAEV/CAMV;13A CAON;22F CAOP;98A/C/E dates;70E/F narratives with exact offsets and sequence/qualifier provenance. Unsupported fields/components remain present. Date-only or timezone-less RDDT remains UNKNOWN for temporal comparison; no UTC is invented. Invalid date components do not produce a structured date.

MT540–548/564/565/566/568 envelopes execute through real Core tests. Their small synthetic bodies are API/component smoke tests, not complete standards conformance examples. Complete MT message business validation and all market-specific component alternatives are not claimed.

## Routing and retirement

1. Ordinary unstructured notice → no Java/ISO parser; original notice continues to Qwen.
2. FIN-header candidate + Core parse with no sequence warnings → Prowide typed structure/narratives; not a full-validity claim.
3. ISO-like partial/malformed text, Core failure or unmatched sequences → non-validating scanner; full raw source, warnings and recovered context remain.
4. No recoverable fields → UNRECOGNISED or ordinary semantic text as appropriate.

Each fact retains source PROWIDE or LENIENT_RECOVERY, tag, qualifier, sequence instance path and exact source range when matchable. If an offset cannot be verified, it is marked unavailable. Recovery never promotes missing fields into authoritative facts. Structured RDDT/option components feed explicit deterministic rules only in the opt-in new adapter path. Source/narrative conflicts remain review signals.

The custom parser is retained unchanged for historical reproduction, fixtures and the existing event-state benchmark. New Qwen-domain parsing uses the Prowide/scanner boundary when DOMAIN_ISO_ADAPTER=true; the primary frozen domain benchmark keeps that flag false. It is not justified to grow the proprietary standards grammar. Retirement from remaining legacy consumers should be an explicit migration; those old paths have not been silently replaced.

ISO metadata can be passed as a compact narrative-field context. Its semantic benefit has **not** been evaluated; it is not enabled in the main frozen Qwen condition. The opt-in adapter still retains the original raw input for evidence/audit. No claim of improved Qwen accuracy from ISO metadata is made.

## Measured overhead

| Adapter | Warm median ms | Warm p95 ms | Records/sec |
|---|---:|---:|---:|
| PROWIDE | 0.3369 | 0.7328 | 2504.9 |
| CUSTOM | 0.1130 | 0.1277 | 8607.0 |
| SCANNER | 0.0524 | 0.0619 | 18026.7 |

Above:1,000 uncontended repetitions of one exact publisher FIN example. Cold JVM+first-parse median 191.9ms / p95 232.6ms across5 starts. Sampled Java RSS reached 177.2MiB during the heterogeneous corpus, and 132.5MiB in the isolated warm microbenchmark; max heap256MiB does not bound native/JVM total memory. The cold/mixed corpus pass briefly overlapped software tests; warm microbenchmark did not. No Qwen inference overlapped parser timing. These are local microbenchmarks, not production throughput SLAs.

##7,683-record verification

{'UNSTRUCTURED_NOTICE': 7683}. Total routing time 691.9ms. PROWIDE_PARSEABLE=0; LENIENT_ISO_RECOVERABLE=0; UNSTRUCTURED=7,683; UNRECOGNISED=0. All81 forced reference-parser controls, selected across lengths, returned missing FIN block2/4. This supports the earlier detector finding; it cannot prove the absence of every conceivable proprietary/encoded representation. No artificial uncertainty was added because a notice lacked ISO fields.

## Deployment and upgrade

`mvn -f tools/prowide/pom.xml package` builds locally; Java11+ is needed only for the opt-in reference path. Maven/downloads occur at setup, never to process a notice. Build dependencies are pinned and checksummed. The persistent helper is lazy, exits/restarts independently, logs runtime warnings locally and is capped/timeout-bounded. No server port is exposed by it. Upgrades require a new dependency/adapter pin, checksum lock and repeat corpus/regression comparison; prior runs retain old identities. The basic Python-only Docker image does not yet include Java/Maven: use the documented host integration or add a separately versioned Java-capable build before enabling this path in that container.

## Recommendation and remaining limits

Use Prowide for supported FIN structure/components and the scanner for damaged narratives. Retain custom code as a historical benchmark while legacy consumers are migrated. Full network validation, large genuine-production SWIFT evaluation, complete category-specific business profiles and ISO-context semantic-quality evaluation remain unestablished. With zero ISO structure in the7,683 excerpts, stop parser optimisation against that corpus and prioritise the separate Qwen/constrained/calibration study.

## Subsequent detector hardening

Recovery scanner v1.1 adds an explicit warning for70F/PACO (the public MT568 dictionary permits PACO only with optionE). Only a FIN envelope at the start of the input can promote Prowide structure; embedded/quoted FIN specimens remain non-authoritative recovery with the whole notice retained. The40 scanner tests pass, including both new security/qualifier cases. DEPLOYMENT-HARDENING.json records source hashes. Prior corpus/component measurements are preserved under their original implementation; the hardening does not change their supplied extraction assertions. No Qwen frozen source or setting changed. The persisted Qwen Notice Detail view exposes PROWIDE versus LENIENT_RECOVERY fields and source links when such an execution exists; it does not synthesize a parser trace for historical results.

## Line-ending verification

The Python normalizer is now `prowide-jsonl-v1.1` over unchanged JVM helper `prowide-jsonl-v1`. Original LF/CRLF narrative offsets survive Core normalization by comparing an explicit line-ending-only alignment view while retaining original quotations. A direct Core test on lone-CR excerpts failed to recover narrative fields; the failed probe is retained in artifacts/prowide-line-ending-tests.log. Production now detects disagreement between Core and recovery field boundaries and routes that damaged representation to the scanner. The test asserts successful end-to-end recovery rather than claiming Core supports lone-CR FIN. This is a documented parser capability distinction, not an altered semantic truth.
