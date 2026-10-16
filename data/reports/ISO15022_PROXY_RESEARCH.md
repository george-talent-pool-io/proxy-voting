# ISO15022 proxy-voting source research

Retrieved 16 October 2026. This is a public-source, experimental subset implementation, **not FIN conformance certification**. No inaccessible SWIFT MyStandards material was used. Full documents cached during research remain under ignored `artifacts/iso-research`; the distributable corpus contains only one short literal excerpt and locally authored fixtures.

## Findings and version boundaries

The ISO dictionary describes general MT564 notifications, MT565 instructions, MT567 statuses and MT568 supplementary narrative. Current sender acceptance is a separate question. In particular, Clearstream's May 2026 meeting-service specification says instructions, statuses and results migrated to ISO20022/portal in November 2024, retaining MT564 coexistence notifications/cancellations. Older general corporate-action profiles must not be represented as current meeting-instruction acceptance.

Public real-message data is scarce: **zero public production messages were incorporated**. One official illustrative disclosure-message excerpt was incorporated. Other public documents contain examples, but complete examples were not copied without an established redistribution licence. Generated fixtures are explicitly synthetic, partial, and excluded from semantic training. We did not retrieve a genuine public linked MT564/MT568 production pair, or genuine production blocking/POA/registration messages. Generated coverage cannot fill that evidentiary gap.

The official disclosure example itself has a 17-character SEME against the dictionary's 16x. It is preserved as unknown rather than repaired. Its heading uses DISC while its actual CAEV field uses DSCL; the literal field is authoritative for the example. These inconsistencies make provenance and unknown preservation essential.

## Implemented boundary

`hybrid/parser.py` preserves the original source, hash, all fields, nested/repeated sequence paths, unknown material and exact Unicode-codepoint spans. It decodes references, function, event/mode indicators, underlying ISIN/description, scoped options, A/C/E dates, coded B dates and narrative qualifiers. F/J/K date alternatives, complete mandatory-field/order constraints, FIN transport validation, accounts, quantities and full market profiles are **not** implemented. Unsupported material remains visible. Because a full validator is absent, the detector deliberately does **not** grant `VALID_ISO15022`; structured examples remain `PARTIAL_ISO15022`.

RDDT controls the experimental response comparison; MKDT, EARD, MEET and RDTE are never substituted. A/C dates without an agreed timezone/precision remain unknown; E offsets are preserved. Different option deadline outcomes abstain rather than silently selecting one. No local clock enters regression tests.

Meeting CAEV identifies event type, not eligibility. Explicit voting-related CAOPTN options can establish that a voting opportunity is offered, without establishing this holder's entitlement. Restrictions remain independent semantic predicates. REGI narrative presence is not proof of an affirmative requirement. Structured values do not enter Laya states.

## Explicit decision rule table

These are conservative PoC policy choices, not regulatory requirements. Every result remains human-reviewed.

| Priority | Condition | Final status |
|---|---|---|
| R1 | Critical conflicts, quarantined lifecycle or malformed supported facts | UNCERTAIN_MANUAL_REVIEW |
| R2 | Validated current event cancellation | NOT_VOTABLE |
| R3 | No current voting opportunity | NOT_VOTABLE |
| R4 | Voting opportunity unresolved | UNCERTAIN_MANUAL_REVIEW |
| R5 | Established vote and controlling response deadline passed | DEADLINE_PASSED |
| R6 | Established vote and any affirmative restriction | VOTABLE_WITH_RESTRICTION |
| R7 | Deadline not open, or restriction information unknown | UNCERTAIN_MANUAL_REVIEW |
| R8 | Established vote, open deadline, all assessed restrictions negative | VOTABLE |

Restriction status can coexist with an unknown deadline; R6 records the restriction but does not authorise processing. A passed deadline outranks restrictions for actionability. An MT565 cancellation request never cancels the event. Persistent sender+CORP identity and PREV linkage retain superseded values; stale references quarantine updates. Omitted replacement fields retain prior provenance and require review. MT568 semantic supersession is deliberately unresolved; it is not automatically merged as current truth. An MT566 movement confirmation is retained as history, never interpreted as vote execution.

## Source inventory

Each entry below records the requested source metadata. The machine-readable version is `data/iso15022_corpus/research_sources.json`.

### ISO15022 public dictionary — MT564 scope and format

[MT564 scope and format](https://www.iso20022.org/15022/uhb/finmt564.htm) · retrieved 2026-10-16

Message types: MT564. Fields/qualifiers: 16R/16S, 20C SEME/CORP/PREV, 23G, 22F CAEV.

Notification structure and repeated options; preliminary, replacement and cancellation messages are distinct.

Actual example: no / not retrieved. Incorporated into tests: yes. Version: Public version retrieved 2026-10-16; release not certified. Access: Retrieved public source.

Rights: No open redistribution licence established. Link to source; locally authored fixtures are separately labelled. Only a short literal excerpt is included where stated.

### ISO15022 public dictionary — MT565 scope and format

[MT565 scope and format](https://www.iso20022.org/15022/uhb/finmt565.htm) · retrieved 2026-10-16

Message types: MT565. Fields/qualifiers: 16R/16S, 20C SEME/CORP/PREV, 23G, 22F CAEV.

Instruction and instruction-cancellation request, not proof of executed vote. CAINST differs from notification CAOPTN.

Actual example: no / not retrieved. Incorporated into tests: yes. Version: Public version retrieved 2026-10-16; release not certified. Access: Retrieved public source.

Rights: No open redistribution licence established. Link to source; locally authored fixtures are separately labelled. Only a short literal excerpt is included where stated.

### ISO15022 public dictionary — MT567 scope and format

[MT567 scope and format](https://www.iso20022.org/15022/uhb/finmt567.htm) · retrieved 2026-10-16

Message types: MT567. Fields/qualifiers: 16R/16S, 20C SEME/CORP/PREV, 23G, 22F CAEV.

Instruction/event/cancellation status advice; acknowledgement does not establish vote execution.

Actual example: no / not retrieved. Incorporated into tests: yes. Version: Public version retrieved 2026-10-16; release not certified. Access: Retrieved public source.

Rights: No open redistribution licence established. Link to source; locally authored fixtures are separately labelled. Only a short literal excerpt is included where stated.

### ISO15022 public dictionary — MT568 scope and format

[MT568 scope and format](https://www.iso20022.org/15022/uhb/finmt568.htm) · retrieved 2026-10-16

Message types: MT568. Fields/qualifiers: 16R/16S, 20C SEME/CORP/PREV, 23G, 22F CAEV.

Supplementary narrative and linked meeting agenda; not a substitute for structured messages.

Actual example: no / not retrieved. Incorporated into tests: yes. Version: Public version retrieved 2026-10-16; release not certified. Access: Retrieved public source.

Rights: No open redistribution licence established. Link to source; locally authored fixtures are separately labelled. Only a short literal excerpt is included where stated.

### ISO15022 public dictionary — MT566 scope and format

[MT566 scope and format](https://www.iso20022.org/15022/uhb/finmt566.htm) · retrieved 2026-10-16

Message types: MT566. Fields/qualifiers: 16R/16S, 20C SEME/CORP/PREV, 23G, 22F CAEV.

Corporate-action movement confirmation. Retained as confirmation lifecycle history; no inference of executed meeting vote.

Actual example: no / not retrieved. Incorporated into tests: no. Version: Public version retrieved 2026-10-16; release not certified. Access: Retrieved public source.

Rights: No open redistribution licence established. Link to source; locally authored fixtures are separately labelled. Only a short literal excerpt is included where stated.

### ISO15022 public dictionary — MT564 general event indicators

[MT564 general event indicators](https://www.iso20022.org/15022/uhb/mt564-5-field-22f.htm) · retrieved 2026-10-16

Message types: MT564. Fields/qualifiers: CAEV, CAMV.

Meeting identification differs from mandatory/voluntary participation; neither proves holder eligibility.

Actual example: no / not retrieved. Incorporated into tests: yes. Version: Public version retrieved 2026-10-16; release not certified. Access: Retrieved public source.

Rights: No open redistribution licence established. Link to source; locally authored fixtures are separately labelled. Only a short literal excerpt is included where stated.

### ISO15022 public dictionary — MT564 event dates

[MT564 event dates](https://www.iso20022.org/15022/uhb/mt564-47-field-98a.htm) · retrieved 2026-10-16

Message types: MT564. Fields/qualifiers: MEET, RDTE, REGI.

Meeting, record and registration dates are distinct; implemented A/C/E date decoding retains precision and offset.

Actual example: no / not retrieved. Incorporated into tests: yes. Version: Public version retrieved 2026-10-16; release not certified. Access: Retrieved public source.

Rights: No open redistribution licence established. Link to source; locally authored fixtures are separately labelled. Only a short literal excerpt is included where stated.

### ISO15022 public dictionary — MT564 option dates

[MT564 option dates](https://www.iso20022.org/15022/uhb/mt564-66-field-98a.htm) · retrieved 2026-10-16

Message types: MT564. Fields/qualifiers: RDDT, MKDT, EARD, BLOK, BORD, DOCD.

Account-servicer response deadline differs from market and early-incentive dates. Do not choose the earliest arbitrary date.

Actual example: no / not retrieved. Incorporated into tests: yes. Version: Public version retrieved 2026-10-16; release not certified. Access: Retrieved public source.

Rights: No open redistribution licence established. Link to source; locally authored fixtures are separately labelled. Only a short literal excerpt is included where stated.

### ISO15022 public dictionary — MT564 option indicators

[MT564 option indicators](https://www.iso20022.org/15022/uhb/mt564-61-field-22f.htm) · retrieved 2026-10-16

Message types: MT564. Fields/qualifiers: CAOP, CETI, OPTF, OSTA.

ABST/AMGT/MNGT/PROX are voting-related options. NOAC is no action. Option cancellation/inactivity is distinct from event cancellation. FULL identifies owner breakdown in option context.

Actual example: no / not retrieved. Incorporated into tests: yes. Version: Public version retrieved 2026-10-16; release not certified. Access: Retrieved public source.

Rights: No open redistribution licence established. Link to source; locally authored fixtures are separately labelled. Only a short literal excerpt is included where stated.

### ISO15022 public dictionary — MT564 additional narrative

[MT564 additional narrative](https://www.iso20022.org/15022/uhb/mt564-106-field-70e.htm) · retrieved 2026-10-16

Message types: MT564. Fields/qualifiers: ADTX, REGI, COMP, INCO, PACO, DISC, TAXE.

Qualifiers route narrative; REGI presence alone does not prove registration required.

Actual example: no / not retrieved. Incorporated into tests: yes. Version: Public version retrieved 2026-10-16; release not certified. Access: Retrieved public source.

Rights: No open redistribution licence established. Link to source; locally authored fixtures are separately labelled. Only a short literal excerpt is included where stated.

### Clearstream — Xact via Swift User Guide

[Xact via Swift User Guide](https://www.clearstream.com/resource/blob/1288716/9435c2032d2953788b97c7e2dbce2285/swift-ug-data.pdf) · retrieved 2026-10-16

Message types: MT564, MT565, MT567, MT568. Fields/qualifiers: CORP, SEME, PREV, RDDT, MT568 pagination.

Contains CA notification, IPAR and reversal examples and field profiles. Sender-specific reference formats are narrower than generic dictionary formats. Guide describes multiple corporate-action services: do not generalise all instructions to current meeting service.

Actual example: yes. Incorporated into tests: no. Version: 27 March 2026; consulted local PDF/text under artifacts/iso-research, not redistributed in corpus. Access: Retrieved public source.

Rights: No open redistribution licence established. Link to source; locally authored fixtures are separately labelled. Only a short literal excerpt is included where stated.

### Clearstream — SRD II connectivity enhancements — Update IV

[SRD II connectivity enhancements — Update IV](https://clearstream.com/clearstream-en/res-library/asset-services/c20019-1991462) · retrieved 2026-10-16

Message types: MT564. Fields/qualifiers: DSCL, CAMV MAND, 17B SRDC.

Historical 2020–2021 interim disclosure flow; public attachment supplies an actual example. Not a meeting ballot or current universal profile.

Actual example: yes. Incorporated into tests: no. Version: Last updated 2 July 2021. Access: Retrieved public source.

Rights: No open redistribution licence established. Link to source; locally authored fixtures are separately labelled. Only a short literal excerpt is included where stated.

### Clearstream — Disclosure Request MT564 Outbound example

[Disclosure Request MT564 Outbound example](https://www.clearstream.com/caas/v1/media/2224604/data/9829e51a4582a1ade84615ea7d7cb3bf/c20019-c20030-l20022-l20033-d20039-mt564-example.pdf) · retrieved 2026-10-16

Message types: MT564. Fields/qualifiers: CORP, SEME, CAEV DSCL, CAMV MAND, PREP, PROC.

Right-column literal field excerpt retained. Published SEME EBDSCL00120191004 is 17 characters, exceeding generic 16x. Preserve unsupported value; do not silently repair. Document heading DISC differs from field DSCL; field value governs parser test.

Actual example: yes. Incorporated into tests: yes. Version: Attachment dated 18 February 2021. Access: Retrieved public source.

Rights: No open redistribution licence established. Link to source; locally authored fixtures are separately labelled. Only a short literal excerpt is included where stated.

### Clearstream / LuxCSD — General Meeting Service — Detailed Functional Specifications

[General Meeting Service — Detailed Functional Specifications](https://www.luxcsd.com/resource/blob/3857176/e9d61c94261acafd540251b217347187/gms-detailed-functional-specifications-data.pdf) · retrieved 2026-10-16

Message types: MT564+, seev.001–008. Fields/qualifiers: CORP, RDDT, MEET, narrative restriction labels.

Since November 2024 current meeting instructions/status/results use ISO20022 or portal; MT564 coexistence notifications/cancellations remain. Sender-specific labels in narrative are not universal ISO15022 fields. This corrects any assumption that generic MT565 support means current Clearstream meeting acceptance.

Actual example: yes. Incorporated into tests: no. Version: May 2026, document 7631; copyright Clearstream all rights reserved. Access: Retrieved public source.

Rights: No open redistribution licence established. Link to source; locally authored fixtures are separately labelled. Only a short literal excerpt is included where stated.

### Clearstream — OneClearstream asset servicing: CBF-issued securities

[OneClearstream asset servicing: CBF-issued securities](https://www.clearstream.com/resource/blob/1296822/a094c0334b0fc5c77d9001bffc77b805/oneclearstream-asset-servicing-cbf-issued-securities-data.pdf) · retrieved 2026-10-16

Message types: MT565, MT567. Fields/qualifiers: CORP, CAON, CAOP.

Historical profile discusses option instructions and best-efforts cancellation. An instruction-cancellation request must not cancel the underlying event.

Actual example: no / not retrieved. Incorporated into tests: no. Version: August 2017; historical, not current service acceptance. Access: Retrieved public source.

Rights: No open redistribution licence established. Link to source; locally authored fixtures are separately labelled. Only a short literal excerpt is included where stated.

### Clearstream — Corporate Action Harmonisation — KADI DE Migration

[Corporate Action Harmonisation — KADI DE Migration](https://www.clearstream.com/caas/v1/media/3711980/data/afde3407d10dfef2e75d6931b762c2c7/cah-functional-specs.pdf) · retrieved 2026-10-16

Message types: MT564, MT568, MT566. Fields/qualifiers: 23G CANC, ADDB REVR.

Reversal reporting varies by event/service; CANC and reversal must not be conflated. Unsupported movement/reversal semantics remain preserved and reviewed.

Actual example: no / not retrieved. Incorporated into tests: no. Version: March 2024. Access: Retrieved public source.

Rights: No open redistribution licence established. Link to source; locally authored fixtures are separately labelled. Only a short literal excerpt is included where stated.

### SMPG — Public market-practice website

[Public market-practice website](https://www.smpg.info/) · retrieved 2026-10-16

Message types: MT56x. Fields/qualifiers: No parser grammar taken from this source.

Public landing page was discoverable, but direct retrieval returned 403 and no authoritative proxy scenario/template file was retrieved. Third-party Scribd/Studylib mirrors were excluded as parser grammar authority. Obtain public SMPG templates in a follow-up corpus expansion.

Actual example: no / not retrieved. Incorporated into tests: no. Version: Public version retrieved 2026-10-16; release not certified. Access: Landing page visible via search/browser fetch; direct HTTP 403; document unavailable.

Rights: No open redistribution licence established. Link to source; locally authored fixtures are separately labelled. Only a short literal excerpt is included where stated.

### ISO TC68 / SMPG — Reflections following SMPG Fall Meeting 2022

[Reflections following SMPG Fall Meeting 2022](https://committee.iso.org/files/live/sites/tc68/files/article_source/TC68_SMPG_Article_Final_29.November.2022.pdf) · retrieved 2026-10-16

Message types: ISO15022, ISO20022. Fields/qualifiers: No parser grammar taken from this source.

Confirms coexistence and role of securities market practices; not a source of field grammar.

Actual example: no / not retrieved. Incorporated into tests: no. Version: 29 November 2022. Access: Retrieved public source.

Rights: No open redistribution licence established. Link to source; locally authored fixtures are separately labelled. Only a short literal excerpt is included where stated.

### Euroclear — Meeting and proxy voting

[Meeting and proxy voting](https://www.euroclear.com/services/en/corporate-actions/corporate-actions-euroclear-uk-international/meeting-and-proxy-voting.html) · retrieved 2026-10-16

Message types: Meeting services. Fields/qualifiers: No parser grammar taken from this source.

Notifications, agendas, results, proxy appointment and admission requests are separate services; market-specific requirements matter. Detailed operational info links to MyEuroclear and was not accessed.

Actual example: no / not retrieved. Incorporated into tests: no. Version: Public version retrieved 2026-10-16; release not certified. Access: Retrieved public source.

Rights: No open redistribution licence established. Link to source; locally authored fixtures are separately labelled. Only a short literal excerpt is included where stated.

### Euroclear — Corporate actions notifications

[Corporate actions notifications](https://www.euroclear.com/campaigns/en/innovation/data-euroclear-information-solutions/reference_data/corporate-actions-notifications.html) · retrieved 2026-10-16

Message types: MT564, ISO20022 meetings. Fields/qualifiers: No parser grammar taken from this source.

Public service description distinguishes corporate-action MT564 delivery and XML meeting delivery; no actual FIN examples retrieved.

Actual example: no / not retrieved. Incorporated into tests: no. Version: Public version retrieved 2026-10-16; release not certified. Access: Retrieved public source.

Rights: No open redistribution licence established. Link to source; locally authored fixtures are separately labelled. Only a short literal excerpt is included where stated.

### SIX SIS — CAEG meeting minutes

[CAEG meeting minutes](https://www.six-group.com/dam/download/sites/swiss-sptc/caeg-meeting-protokolle/2020/2020-06-08-protokoll-caeg.pdf) · retrieved 2026-10-16

Message types: MT564, MT568. Fields/qualifiers: 70E ADTX, TAXE.

Minutes discuss moving tax information between ADTX and TAXE: narrative qualifier practices can vary. Not a complete message template or a current universal profile.

Actual example: no / not retrieved. Incorporated into tests: no. Version: 8 June 2020 minutes, historical. Access: Retrieved public source.

Rights: No open redistribution licence established. Link to source; locally authored fixtures are separately labelled. Only a short literal excerpt is included where stated.

### DTCC — Proxy Services

[Proxy Services](https://www.dtcc.com/products-and-services/asset-services/issuer-services/proxy-services) · retrieved 2026-10-16

Message types: Proxy service. Fields/qualifiers: record-date entitlement.

Omnibus proxy transfers DTC voting rights to record-date participants. Meeting identification alone cannot establish individual beneficial-owner eligibility.

Actual example: no / not retrieved. Incorporated into tests: no. Version: Public version retrieved 2026-10-16; release not certified. Access: Retrieved public source.

Rights: No open redistribution licence established. Link to source; locally authored fixtures are separately labelled. Only a short literal excerpt is included where stated.

### DTCC — Corporate Actions Technical Documentation Hub

[Corporate Actions Technical Documentation Hub](https://www.dtcc.com/products-and-services/asset-services/corporate-actions-processing/ca-documentation) · retrieved 2026-10-16

Message types: ISO20022 corporate actions and meetings. Fields/qualifiers: No parser grammar taken from this source.

Public documentation hub primarily covers ISO20022. Its material must not be treated as an ISO15022 raw-message corpus.

Actual example: no / not retrieved. Incorporated into tests: no. Version: Public version retrieved 2026-10-16; release not certified. Access: Retrieved public source.

Rights: No open redistribution licence established. Link to source; locally authored fixtures are separately labelled. Only a short literal excerpt is included where stated.

### Euronext Securities — ISO15022 Messages EN v9

[ISO15022 Messages EN v9](https://www.euronext.com/sites/default/files/2026-01/20260126_ISO%2015022%20Messages_EN_v9.pdf) · retrieved 2026-10-16

Message types: MT564. Fields/qualifiers: SEME, CORP, COAF, PREP, CAEV.

Public implementation tables support field/qualifier context and illustrate sender-profile differences. No example copied into this phase.

Actual example: no / not retrieved. Incorporated into tests: no. Version: 26 January 2026 v9. Access: Retrieved public source.

Rights: No open redistribution licence established. Link to source; locally authored fixtures are separately labelled. Only a short literal excerpt is included where stated.

## Evidence and metric separation

Every decoded fact links to its original field range. Semantic candidate evidence comes from sentence-level native Laya scores and must match an exact source substring. A matching quotation is a candidate support passage, not a proven explanation. If no reliable candidate passes the predeclared rule, the UI says **Evidence span unavailable**. Negative absence findings do not invent quotations. Supersession conflicts abstain.

Parser reference assertions, semantic predicate accuracy and final customer-status agreement have distinct denominators. Generated parser fixtures are never combined with public-data or expert-verified accuracy. The existing public corpus has no expert-labelled independent final-event test set. The dashboard retains “Not measured” for those public accuracy layers.
