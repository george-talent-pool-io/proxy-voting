# Laya baseline failure analysis

Preserved baseline: 30/57 authored cases pass; 27 fail. Reference date: 2026-10-16. These are partial-field assertions on authored adversarial examples, not customer accuracy.

## Primary diagnostic categories

| Diagnostic category | Failed cases |
|---|---:|
| Votability under restriction | 4 |
| Historical context | 4 |
| Negation / event confusion | 4 |
| Temporal reasoning | 3 |
| Other restriction omission | 3 |
| Record date / blocking confusion | 2 |
| Deadline without evidence | 2 |
| Multilingual understanding | 2 |
| Unsupported restriction | 1 |
| Conflict handling | 1 |
| Insufficient context | 1 |

Counts assign one primary diagnostic per failed case and sum to 27. They describe observable error patterns; they do not establish neural causes. Several cases have multiple errors.

Failed asserted fields (overlap): `{'classification': 2, 'share_blocking': 3, 'votable': 20, 'deadline_status': 7, 'other_restriction': 3, 'poa_required': 1}`.

## Findings before any new training

The baseline already uses five independent native Laya choice questions. It is not a seven-way softmax. The seven labels are derived display statuses. Factorisation alone therefore cannot be claimed as a new remedy or explain these failures. There are several error families, with recurring failure to retain YES votability when restrictions or historical context appear. Unsupported restrictions and invented deadline states also occur.

The minimum winning probability is a policy score, not a probability that every factor is correct. High-confidence factor errors can hide behind a low aggregate score. Native SDK confidence is retained below separately; it is not the winner–runner-up margin.

No expected answer has been changed. Unasserted factors are shown but are not scored as verified truths. All five factors were evaluated without truncation on these failed examples. Likely reasons below are testable hypotheses inferred from the text and outputs, not model-generated explanations.

Model revision: `7b928d828b7b0e022f929d9bd2e44165aa270148`; config: `5d770dcd5af69e5a404e62553fe4abc2d1a41f79b4b6977a1c6d7eee240e177b`.

## All 27 failures

### agm — Unsupported restriction

**Source text**

> Shareholders may submit voting instructions for the Annual General Meeting. Voting closes on 20 October 2026.

**Expected asserted fields**
```json
{
  "classification": "VOTABLE",
  "deadline_status": "OPEN",
  "poa_required": false,
  "share_blocking": false,
  "votable": "YES"
}
```
**Observed factors and derived status**
```json
{
  "classification": "SHARE_BLOCKING",
  "deadline_status": "OPEN",
  "manual_review_required": true,
  "other_restriction": false,
  "poa_required": false,
  "share_blocking": true,
  "votable": "YES"
}
```
Failed assertions: classification, share_blocking. Aggregate policy score: 0.4104.

| Factor | All native option probabilities | Winner | Top-two margin | SDK confidence |
|---|---|---|---:|---:|
| deadline_status | OPEN=0.6069, PASSED=0.1433, UNKNOWN=0.2499 | OPEN | 0.3570 | 0.1553 |
| other_restriction | NO=0.6171, UNKNOWN=0.3164, YES=0.0665 | NO | 0.3007 | 0.2333 |
| poa_required | NO=0.4104, UNKNOWN=0.3335, YES=0.2561 | NO | 0.0769 | 0.0164 |
| share_blocking | NO=0.0143, UNKNOWN=0.0347, YES=0.9509 | YES | 0.9162 | 0.7949 |
| votable | NO=0.0472, UNCERTAIN=0.0738, YES=0.8791 | YES | 0.8053 | 0.5907 |

**Likely reason / next discriminating check:** Blocking is asserted although no blocking language appears; the error is in a factor, not status precedence. Compare against independently reviewed examples in this pattern after supervised training; prompt/schema ablations alone cannot establish the cause.

### blocking — Votability under restriction

**Source text**

> Shareholders may vote at the AGM. Shares will be blocked from the date voting instructions are submitted until completion of the meeting.

**Expected asserted fields**
```json
{
  "share_blocking": true,
  "votable": "YES"
}
```
**Observed factors and derived status**
```json
{
  "classification": "UNCERTAIN_MANUAL_REVIEW",
  "deadline_status": "OPEN",
  "manual_review_required": true,
  "other_restriction": null,
  "poa_required": false,
  "share_blocking": true,
  "votable": "UNCERTAIN"
}
```
Failed assertions: votable. Aggregate policy score: 0.4921.

| Factor | All native option probabilities | Winner | Top-two margin | SDK confidence |
|---|---|---|---:|---:|
| deadline_status | OPEN=0.6763, PASSED=0.1276, UNKNOWN=0.1961 | OPEN | 0.4802 | 0.2293 |
| other_restriction | NO=0.3382, UNKNOWN=0.4921, YES=0.1697 | UNKNOWN | 0.1539 | 0.0747 |
| poa_required | NO=0.5497, UNKNOWN=0.0620, YES=0.3883 | NO | 0.1614 | 0.2094 |
| share_blocking | NO=0.1562, UNKNOWN=0.1877, YES=0.6561 | YES | 0.4684 | 0.1985 |
| votable | NO=0.2007, UNCERTAIN=0.4967, YES=0.3026 | UNCERTAIN | 0.1941 | 0.0610 |

**Likely reason / next discriminating check:** Blocking is detected, but the explicit permission to vote is classified UNCERTAIN. A restriction appears to compete with the voting-opportunity decision. Compare against independently reviewed examples in this pattern after supervised training; prompt/schema ablations alone cannot establish the cause.

### poa — Votability under restriction

**Source text**

> Beneficial owners wishing to vote must submit a valid power of attorney.

**Expected asserted fields**
```json
{
  "poa_required": true,
  "votable": "YES"
}
```
**Observed factors and derived status**
```json
{
  "classification": "UNCERTAIN_MANUAL_REVIEW",
  "deadline_status": "UNKNOWN",
  "manual_review_required": true,
  "other_restriction": null,
  "poa_required": true,
  "share_blocking": true,
  "votable": "UNCERTAIN"
}
```
Failed assertions: votable. Aggregate policy score: 0.4355.

| Factor | All native option probabilities | Winner | Top-two margin | SDK confidence |
|---|---|---|---:|---:|
| deadline_status | OPEN=0.2278, PASSED=0.0717, UNKNOWN=0.7005 | UNKNOWN | 0.4727 | 0.2943 |
| other_restriction | NO=0.3143, UNKNOWN=0.4355, YES=0.2502 | UNKNOWN | 0.1212 | 0.0238 |
| poa_required | NO=0.0645, UNKNOWN=0.0197, YES=0.9158 | YES | 0.8513 | 0.6953 |
| share_blocking | NO=0.0217, UNKNOWN=0.0343, YES=0.9439 | YES | 0.9096 | 0.7693 |
| votable | NO=0.1686, UNCERTAIN=0.5714, YES=0.2601 | UNCERTAIN | 0.3113 | 0.1169 |

**Likely reason / next discriminating check:** Required POA is detected; conditional permission to vote is missed. An additional blocking assertion has no textual support. Compare against independently reviewed examples in this pattern after supervised training; prompt/schema ablations alone cannot establish the cause.

### past-deadline — Temporal reasoning

**Source text**

> Voting instructions for the current AGM were required by 10 October 2025.

**Expected asserted fields**
```json
{
  "deadline_status": "PASSED",
  "votable": "YES"
}
```
**Observed factors and derived status**
```json
{
  "classification": "UNCERTAIN_MANUAL_REVIEW",
  "deadline_status": "UNKNOWN",
  "manual_review_required": true,
  "other_restriction": false,
  "poa_required": null,
  "share_blocking": null,
  "votable": "UNCERTAIN"
}
```
Failed assertions: deadline_status, votable. Aggregate policy score: 0.5181.

| Factor | All native option probabilities | Winner | Top-two margin | SDK confidence |
|---|---|---|---:|---:|
| deadline_status | OPEN=0.1955, PASSED=0.2532, UNKNOWN=0.5512 | UNKNOWN | 0.2980 | 0.0941 |
| other_restriction | NO=0.5181, UNKNOWN=0.4510, YES=0.0310 | NO | 0.0671 | 0.2650 |
| poa_required | NO=0.4484, UNKNOWN=0.5186, YES=0.0330 | UNKNOWN | 0.0702 | 0.2602 |
| share_blocking | NO=0.0842, UNKNOWN=0.8252, YES=0.0905 | UNKNOWN | 0.7347 | 0.4681 |
| votable | NO=0.0970, UNCERTAIN=0.7752, YES=0.1278 | UNCERTAIN | 0.6474 | 0.3750 |

**Likely reason / next discriminating check:** An explicit dated instruction deadline is not resolved; votability is also lost. Calendar comparison and opportunity semantics are conflated. Compare against independently reviewed examples in this pattern after supervised training; prompt/schema ablations alone cannot establish the cause.

### blocked-and-poa — Votability under restriction

**Source text**

> To vote at the EGM, beneficial owners must provide a notarised power of attorney and block their shares until the meeting ends.

**Expected asserted fields**
```json
{
  "classification": "VOTABLE_WITH_RESTRICTION",
  "poa_required": true,
  "share_blocking": true,
  "votable": "YES"
}
```
**Observed factors and derived status**
```json
{
  "classification": "UNCERTAIN_MANUAL_REVIEW",
  "deadline_status": "UNKNOWN",
  "manual_review_required": true,
  "other_restriction": true,
  "poa_required": true,
  "share_blocking": true,
  "votable": "UNCERTAIN"
}
```
Failed assertions: classification, votable. Aggregate policy score: 0.4530.

| Factor | All native option probabilities | Winner | Top-two margin | SDK confidence |
|---|---|---|---:|---:|
| deadline_status | OPEN=0.1568, PASSED=0.1095, UNKNOWN=0.7338 | UNKNOWN | 0.5770 | 0.3084 |
| other_restriction | NO=0.0971, UNKNOWN=0.4341, YES=0.4688 | YES | 0.0347 | 0.1409 |
| poa_required | NO=0.2751, UNKNOWN=0.2719, YES=0.4530 | YES | 0.1779 | 0.0280 |
| share_blocking | NO=0.0186, UNKNOWN=0.0406, YES=0.9408 | YES | 0.9002 | 0.7617 |
| votable | NO=0.0730, UNCERTAIN=0.5652, YES=0.3617 | UNCERTAIN | 0.2035 | 0.1977 |

**Likely reason / next discriminating check:** Both named restrictions are detected, but conditional participation becomes UNCERTAIN. The derived status follows that erroneous factor. Compare against independently reviewed examples in this pattern after supervised training; prompt/schema ablations alone cannot establish the cause.

### two-dates — Votability under restriction

**Source text**

> Meeting date: 20 November 2026. Your voting instructions must reach our custody desk by 1 October 2026.

**Expected asserted fields**
```json
{
  "deadline_status": "PASSED",
  "votable": "YES"
}
```
**Observed factors and derived status**
```json
{
  "classification": "UNCERTAIN_MANUAL_REVIEW",
  "deadline_status": "PASSED",
  "manual_review_required": true,
  "other_restriction": true,
  "poa_required": false,
  "share_blocking": true,
  "votable": "UNCERTAIN"
}
```
Failed assertions: votable. Aggregate policy score: 0.4110.

| Factor | All native option probabilities | Winner | Top-two margin | SDK confidence |
|---|---|---|---:|---:|
| deadline_status | OPEN=0.1690, PASSED=0.6199, UNKNOWN=0.2111 | PASSED | 0.4088 | 0.1578 |
| other_restriction | NO=0.3496, UNKNOWN=0.1473, YES=0.5032 | YES | 0.1536 | 0.0942 |
| poa_required | NO=0.4110, UNKNOWN=0.3014, YES=0.2876 | NO | 0.1096 | 0.0121 |
| share_blocking | NO=0.0122, UNKNOWN=0.0262, YES=0.9616 | YES | 0.9354 | 0.8300 |
| votable | NO=0.1175, UNCERTAIN=0.4698, YES=0.4127 | UNCERTAIN | 0.0571 | 0.1154 |

**Likely reason / next discriminating check:** Deadline selection is correct, but a notice requesting instructions becomes UNCERTAIN; unsupported restrictions are also present. Compare against independently reviewed examples in this pattern after supervised training; prompt/schema ablations alone cannot establish the cause.

### record-date — Record date / blocking confusion

**Source text**

> The voting record date is 1 October 2026. The AGM will be held on 30 November 2026. Shareholders may vote. No instruction deadline is specified.

**Expected asserted fields**
```json
{
  "deadline_status": "UNKNOWN",
  "share_blocking": false,
  "votable": "YES"
}
```
**Observed factors and derived status**
```json
{
  "classification": "NOT_VOTABLE",
  "deadline_status": "UNKNOWN",
  "manual_review_required": true,
  "other_restriction": false,
  "poa_required": false,
  "share_blocking": true,
  "votable": "NO"
}
```
Failed assertions: share_blocking, votable. Aggregate policy score: 0.4575.

| Factor | All native option probabilities | Winner | Top-two margin | SDK confidence |
|---|---|---|---:|---:|
| deadline_status | OPEN=0.0260, PASSED=0.4486, UNKNOWN=0.5254 | UNKNOWN | 0.0768 | 0.2786 |
| other_restriction | NO=0.9411, UNKNOWN=0.0329, YES=0.0260 | NO | 0.9082 | 0.7593 |
| poa_required | NO=0.7917, UNKNOWN=0.0248, YES=0.1834 | NO | 0.6083 | 0.4650 |
| share_blocking | NO=0.0401, UNKNOWN=0.0496, YES=0.9103 | YES | 0.8607 | 0.6691 |
| votable | NO=0.4575, UNCERTAIN=0.2740, YES=0.2684 | NO | 0.1835 | 0.0301 |

**Likely reason / next discriminating check:** A record date is treated as blocking and the explicit vote as NO. Record ownership eligibility is different from immobilising shares. Compare against independently reviewed examples in this pattern after supervised training; prompt/schema ablations alone cannot establish the cause.

### quoted-old — Historical context

**Source text**

> The 2025 archive stated: "Votes closed 1 May 2025; blocking required." For the current 2026 AGM, vote by 1 November 2026. No share blocking applies this year.

**Expected asserted fields**
```json
{
  "deadline_status": "OPEN",
  "share_blocking": false,
  "votable": "YES"
}
```
**Observed factors and derived status**
```json
{
  "classification": "UNCERTAIN_MANUAL_REVIEW",
  "deadline_status": "PASSED",
  "manual_review_required": true,
  "other_restriction": false,
  "poa_required": false,
  "share_blocking": false,
  "votable": "UNCERTAIN"
}
```
Failed assertions: deadline_status, votable. Aggregate policy score: 0.6864.

| Factor | All native option probabilities | Winner | Top-two margin | SDK confidence |
|---|---|---|---:|---:|
| deadline_status | OPEN=0.0410, PASSED=0.9066, UNKNOWN=0.0524 | PASSED | 0.8542 | 0.6593 |
| other_restriction | NO=0.9918, UNKNOWN=0.0025, YES=0.0057 | NO | 0.9861 | 0.9524 |
| poa_required | NO=0.9599, UNKNOWN=0.0159, YES=0.0243 | NO | 0.9356 | 0.8223 |
| share_blocking | NO=0.8848, UNKNOWN=0.0161, YES=0.0991 | NO | 0.7857 | 0.6324 |
| votable | NO=0.0426, UNCERTAIN=0.6864, YES=0.2710 | UNCERTAIN | 0.4154 | 0.3205 |

**Likely reason / next discriminating check:** The expired archived deadline overrides the current future deadline despite the explicit current-year distinction; voting opportunity is also missed. Compare against independently reviewed examples in this pattern after supervised training; prompt/schema ablations alone cannot establish the cause.

### voluntary-tender — Negation / event confusion

**Source text**

> Voluntary tender offer: holders may elect cash or retain shares. This election is not a shareholder meeting ballot and no vote is requested.

**Expected asserted fields**
```json
{
  "votable": "NO"
}
```
**Observed factors and derived status**
```json
{
  "classification": "DEADLINE_PASSED",
  "deadline_status": "PASSED",
  "manual_review_required": true,
  "other_restriction": false,
  "poa_required": false,
  "share_blocking": true,
  "votable": "YES"
}
```
Failed assertions: votable. Aggregate policy score: 0.3987.

| Factor | All native option probabilities | Winner | Top-two margin | SDK confidence |
|---|---|---|---:|---:|
| deadline_status | OPEN=0.1236, PASSED=0.5049, UNKNOWN=0.3715 | PASSED | 0.1334 | 0.1159 |
| other_restriction | NO=0.8573, UNKNOWN=0.0285, YES=0.1142 | NO | 0.7431 | 0.5619 |
| poa_required | NO=0.8746, UNKNOWN=0.0357, YES=0.0897 | NO | 0.7849 | 0.5882 |
| share_blocking | NO=0.1236, UNKNOWN=0.0500, YES=0.8264 | YES | 0.7028 | 0.4850 |
| votable | NO=0.2390, UNCERTAIN=0.3623, YES=0.3987 | YES | 0.0364 | 0.0201 |

**Likely reason / next discriminating check:** An explicit exclusion of a ballot is ignored. A voluntary election appears to be mistaken for a shareholder vote. Compare against independently reviewed examples in this pattern after supervised training; prompt/schema ablations alone cannot establish the cause.

### historical-results — Deadline without evidence

**Source text**

> At last year’s AGM, 97% voted in favour of the remuneration policy. These are final historical results; no vote is currently open.

**Expected asserted fields**
```json
{
  "deadline_status": "UNKNOWN",
  "votable": "NO"
}
```
**Observed factors and derived status**
```json
{
  "classification": "NOT_VOTABLE",
  "deadline_status": "PASSED",
  "manual_review_required": true,
  "other_restriction": false,
  "poa_required": false,
  "share_blocking": false,
  "votable": "NO"
}
```
Failed assertions: deadline_status. Aggregate policy score: 0.5688.

| Factor | All native option probabilities | Winner | Top-two margin | SDK confidence |
|---|---|---|---:|---:|
| deadline_status | OPEN=0.0757, PASSED=0.7640, UNKNOWN=0.1603 | PASSED | 0.6037 | 0.3678 |
| other_restriction | NO=0.9908, UNKNOWN=0.0035, YES=0.0057 | NO | 0.9851 | 0.9470 |
| poa_required | NO=0.9552, UNKNOWN=0.0102, YES=0.0346 | NO | 0.9206 | 0.8115 |
| share_blocking | NO=0.9124, UNKNOWN=0.0285, YES=0.0591 | NO | 0.8533 | 0.6794 |
| votable | NO=0.5688, UNCERTAIN=0.2392, YES=0.1920 | NO | 0.3296 | 0.1080 |

**Likely reason / next discriminating check:** Historical results are correctly non-votable but a current passed deadline is asserted without an instruction deadline. Compare against independently reviewed examples in this pattern after supervised training; prompt/schema ablations alone cannot establish the cause.

### eligibility — Other restriction omission

**Source text**

> Only holders of Class A shares may vote on resolution 3 at the EGM. Class B shares have no voting entitlement.

**Expected asserted fields**
```json
{
  "other_restriction": true,
  "votable": "YES"
}
```
**Observed factors and derived status**
```json
{
  "classification": "DEADLINE_PASSED",
  "deadline_status": "PASSED",
  "manual_review_required": true,
  "other_restriction": false,
  "poa_required": false,
  "share_blocking": true,
  "votable": "YES"
}
```
Failed assertions: other_restriction. Aggregate policy score: 0.6012.

| Factor | All native option probabilities | Winner | Top-two margin | SDK confidence |
|---|---|---|---:|---:|
| deadline_status | OPEN=0.2654, PASSED=0.6012, UNKNOWN=0.1334 | PASSED | 0.3358 | 0.1565 |
| other_restriction | NO=0.6074, UNKNOWN=0.0871, YES=0.3055 | NO | 0.3019 | 0.2011 |
| poa_required | NO=0.6086, UNKNOWN=0.0989, YES=0.2925 | NO | 0.3161 | 0.1893 |
| share_blocking | NO=0.1207, UNKNOWN=0.0583, YES=0.8210 | YES | 0.7003 | 0.4695 |
| votable | NO=0.0344, UNCERTAIN=0.1628, YES=0.8028 | YES | 0.6400 | 0.4649 |

**Likely reason / next discriminating check:** Class-specific entitlement is missed. Blocking and a passed deadline are also asserted without supporting language. Compare against independently reviewed examples in this pattern after supervised training; prompt/schema ablations alone cannot establish the cause.

### partial — Other restriction omission

**Source text**

> Shareholders may vote at the AGM. Split or partial voting is prohibited: all shares in an account must be voted the same way.

**Expected asserted fields**
```json
{
  "other_restriction": true,
  "votable": "YES"
}
```
**Observed factors and derived status**
```json
{
  "classification": "UNCERTAIN_MANUAL_REVIEW",
  "deadline_status": "OPEN",
  "manual_review_required": true,
  "other_restriction": false,
  "poa_required": false,
  "share_blocking": false,
  "votable": "UNCERTAIN"
}
```
Failed assertions: other_restriction, votable. Aggregate policy score: 0.4089.

| Factor | All native option probabilities | Winner | Top-two margin | SDK confidence |
|---|---|---|---:|---:|
| deadline_status | OPEN=0.5586, PASSED=0.3473, UNKNOWN=0.0941 | OPEN | 0.2113 | 0.1672 |
| other_restriction | NO=0.8994, UNKNOWN=0.0513, YES=0.0493 | NO | 0.8481 | 0.6395 |
| poa_required | NO=0.7213, UNKNOWN=0.0244, YES=0.2543 | NO | 0.4670 | 0.3860 |
| share_blocking | NO=0.6741, UNKNOWN=0.0310, YES=0.2949 | NO | 0.3792 | 0.3322 |
| votable | NO=0.2816, UNCERTAIN=0.4089, YES=0.3095 | UNCERTAIN | 0.0994 | 0.0119 |

**Likely reason / next discriminating check:** The explicit prohibition on split voting is missed and the accompanying voting permission becomes UNCERTAIN. Compare against independently reviewed examples in this pattern after supervised training; prompt/schema ablations alone cannot establish the cause.

### record-ordinary — Record date / blocking confusion

**Source text**

> Holders on the record date may vote at the annual meeting. The record date does not block trading.

**Expected asserted fields**
```json
{
  "share_blocking": false,
  "votable": "YES"
}
```
**Observed factors and derived status**
```json
{
  "classification": "DEADLINE_PASSED",
  "deadline_status": "PASSED",
  "manual_review_required": true,
  "other_restriction": true,
  "poa_required": null,
  "share_blocking": true,
  "votable": "YES"
}
```
Failed assertions: share_blocking. Aggregate policy score: 0.4536.

| Factor | All native option probabilities | Winner | Top-two margin | SDK confidence |
|---|---|---|---:|---:|
| deadline_status | OPEN=0.1344, PASSED=0.5854, UNKNOWN=0.2802 | PASSED | 0.3052 | 0.1446 |
| other_restriction | NO=0.2034, UNKNOWN=0.0445, YES=0.7521 | YES | 0.5487 | 0.3840 |
| poa_required | NO=0.2380, UNKNOWN=0.4536, YES=0.3084 | UNKNOWN | 0.1452 | 0.0324 |
| share_blocking | NO=0.1299, UNKNOWN=0.0208, YES=0.8492 | YES | 0.7193 | 0.5589 |
| votable | NO=0.0553, UNCERTAIN=0.2004, YES=0.7443 | YES | 0.5439 | 0.3610 |

**Likely reason / next discriminating check:** The model asserts blocking despite an explicit statement that trading is not blocked. Compare against independently reviewed examples in this pattern after supervised training; prompt/schema ablations alone cannot establish the cause.

### contradiction — Conflict handling

**Source text**

> Voting instructions are accepted. Voting instructions are not accepted. Both statements apply to the same meeting and no superseding notice is identified.

**Expected asserted fields**
```json
{
  "votable": "UNCERTAIN"
}
```
**Observed factors and derived status**
```json
{
  "classification": "DEADLINE_PASSED",
  "deadline_status": "PASSED",
  "manual_review_required": true,
  "other_restriction": false,
  "poa_required": false,
  "share_blocking": true,
  "votable": "YES"
}
```
Failed assertions: votable. Aggregate policy score: 0.7335.

| Factor | All native option probabilities | Winner | Top-two margin | SDK confidence |
|---|---|---|---:|---:|
| deadline_status | OPEN=0.1386, PASSED=0.7335, UNKNOWN=0.1278 | PASSED | 0.5949 | 0.3044 |
| other_restriction | NO=0.9171, UNKNOWN=0.0379, YES=0.0450 | NO | 0.8721 | 0.6878 |
| poa_required | NO=0.9641, UNKNOWN=0.0175, YES=0.0184 | NO | 0.9457 | 0.8366 |
| share_blocking | NO=0.0630, UNKNOWN=0.0533, YES=0.8837 | YES | 0.8207 | 0.5997 |
| votable | NO=0.0430, UNCERTAIN=0.1260, YES=0.8310 | YES | 0.7050 | 0.4993 |

**Likely reason / next discriminating check:** The model chooses YES despite equally scoped incompatible statements and no supersession evidence. Compare against independently reviewed examples in this pattern after supervised training; prompt/schema ablations alone cannot establish the cause.

### same-day — Temporal reasoning

**Source text**

> Vote at the AGM. Voting deadline: 16 October 2026, 17:00 Tokyo time. The reference supplies a date but no time.

**Expected asserted fields**
```json
{
  "deadline_status": "UNKNOWN"
}
```
**Observed factors and derived status**
```json
{
  "classification": "UNCERTAIN_MANUAL_REVIEW",
  "deadline_status": "PASSED",
  "manual_review_required": true,
  "other_restriction": true,
  "poa_required": false,
  "share_blocking": true,
  "votable": "UNCERTAIN"
}
```
Failed assertions: deadline_status. Aggregate policy score: 0.4375.

| Factor | All native option probabilities | Winner | Top-two margin | SDK confidence |
|---|---|---|---:|---:|
| deadline_status | OPEN=0.2357, PASSED=0.5464, UNKNOWN=0.2180 | PASSED | 0.3107 | 0.0871 |
| other_restriction | NO=0.2993, UNKNOWN=0.0729, YES=0.6278 | YES | 0.3285 | 0.2315 |
| poa_required | NO=0.4648, UNKNOWN=0.1788, YES=0.3564 | NO | 0.1084 | 0.0610 |
| share_blocking | NO=0.0230, UNKNOWN=0.0722, YES=0.9048 | YES | 0.8326 | 0.6659 |
| votable | NO=0.1343, UNCERTAIN=0.4375, YES=0.4282 | UNCERTAIN | 0.0093 | 0.0947 |

**Likely reason / next discriminating check:** A date-only reference cannot determine whether a timezone-specific same-day cutoff has elapsed. PASSED is unjustified. Compare against independently reviewed examples in this pattern after supervised training; prompt/schema ablations alone cannot establish the cause.

### historic-fiscal — Historical context

**Source text**

> The fiscal year ended 31 December 2025. Vote at the upcoming AGM; instructions must arrive by 2 November 2026.

**Expected asserted fields**
```json
{
  "deadline_status": "OPEN",
  "votable": "YES"
}
```
**Observed factors and derived status**
```json
{
  "classification": "UNCERTAIN_MANUAL_REVIEW",
  "deadline_status": "PASSED",
  "manual_review_required": true,
  "other_restriction": true,
  "poa_required": null,
  "share_blocking": true,
  "votable": "UNCERTAIN"
}
```
Failed assertions: deadline_status, votable. Aggregate policy score: 0.4148.

| Factor | All native option probabilities | Winner | Top-two margin | SDK confidence |
|---|---|---|---:|---:|
| deadline_status | OPEN=0.1283, PASSED=0.6475, UNKNOWN=0.2242 | PASSED | 0.4233 | 0.1989 |
| other_restriction | NO=0.1975, UNKNOWN=0.1837, YES=0.6188 | YES | 0.4213 | 0.1547 |
| poa_required | NO=0.2939, UNKNOWN=0.5317, YES=0.1743 | UNKNOWN | 0.2378 | 0.0895 |
| share_blocking | NO=0.0258, UNKNOWN=0.2316, YES=0.7426 | YES | 0.5110 | 0.4045 |
| votable | NO=0.2472, UNCERTAIN=0.4148, YES=0.3379 | UNCERTAIN | 0.0769 | 0.0196 |

**Likely reason / next discriminating check:** The non-deadline fiscal date appears to distract from the explicit upcoming instruction cutoff; voting opportunity is also missed. Compare against independently reviewed examples in this pattern after supervised training; prompt/schema ablations alone cannot establish the cause.

### non-voting-bond — Negation / event confusion

**Source text**

> Mandatory interest payment to bondholders. No ballot, consent solicitation or shareholder vote.

**Expected asserted fields**
```json
{
  "votable": "NO"
}
```
**Observed factors and derived status**
```json
{
  "classification": "DEADLINE_PASSED",
  "deadline_status": "PASSED",
  "manual_review_required": true,
  "other_restriction": false,
  "poa_required": false,
  "share_blocking": false,
  "votable": "YES"
}
```
Failed assertions: votable. Aggregate policy score: 0.5060.

| Factor | All native option probabilities | Winner | Top-two margin | SDK confidence |
|---|---|---|---:|---:|
| deadline_status | OPEN=0.0943, PASSED=0.6915, UNKNOWN=0.2142 | PASSED | 0.4773 | 0.2647 |
| other_restriction | NO=0.9160, UNKNOWN=0.0238, YES=0.0601 | NO | 0.8559 | 0.6919 |
| poa_required | NO=0.9260, UNKNOWN=0.0237, YES=0.0503 | NO | 0.8757 | 0.7177 |
| share_blocking | NO=0.5060, UNKNOWN=0.0278, YES=0.4662 | NO | 0.0398 | 0.2717 |
| votable | NO=0.2983, UNCERTAIN=0.1561, YES=0.5456 | YES | 0.2473 | 0.1067 |

**Likely reason / next discriminating check:** Mandatory interest payment and explicit denial of any ballot are classified as a voting opportunity. Compare against independently reviewed examples in this pattern after supervised training; prompt/schema ablations alone cannot establish the cause.

### poa-waived — Historical context

**Source text**

> A POA was required last year. This year that requirement has been waived for all beneficial owners voting at the AGM.

**Expected asserted fields**
```json
{
  "poa_required": false,
  "votable": "YES"
}
```
**Observed factors and derived status**
```json
{
  "classification": "UNCERTAIN_MANUAL_REVIEW",
  "deadline_status": "PASSED",
  "manual_review_required": true,
  "other_restriction": false,
  "poa_required": false,
  "share_blocking": false,
  "votable": "UNCERTAIN"
}
```
Failed assertions: votable. Aggregate policy score: 0.7075.

| Factor | All native option probabilities | Winner | Top-two margin | SDK confidence |
|---|---|---|---:|---:|
| deadline_status | OPEN=0.0002, PASSED=0.9994, UNKNOWN=0.0004 | PASSED | 0.9990 | 0.9952 |
| other_restriction | NO=0.9983, UNKNOWN=0.0015, YES=0.0002 | NO | 0.9968 | 0.9881 |
| poa_required | NO=0.9410, UNKNOWN=0.0215, YES=0.0375 | NO | 0.9035 | 0.7606 |
| share_blocking | NO=0.9914, UNKNOWN=0.0015, YES=0.0071 | NO | 0.9843 | 0.9514 |
| votable | NO=0.2420, UNCERTAIN=0.7075, YES=0.0505 | UNCERTAIN | 0.4655 | 0.3274 |

**Likely reason / next discriminating check:** The waiver factor is correct, but the current-year permission to vote is lost amid historical/current contrast. Compare against independently reviewed examples in this pattern after supervised training; prompt/schema ablations alone cannot establish the cause.

### historic-quote-only — Historical context

**Source text**

> The archive quotes a 2020 notice: "You may vote by proxy." This page is a historical archive, with no current vote.

**Expected asserted fields**
```json
{
  "votable": "NO"
}
```
**Observed factors and derived status**
```json
{
  "classification": "UNCERTAIN_MANUAL_REVIEW",
  "deadline_status": "PASSED",
  "manual_review_required": true,
  "other_restriction": false,
  "poa_required": false,
  "share_blocking": false,
  "votable": "UNCERTAIN"
}
```
Failed assertions: votable. Aggregate policy score: 0.5211.

| Factor | All native option probabilities | Winner | Top-two margin | SDK confidence |
|---|---|---|---:|---:|
| deadline_status | OPEN=0.0446, PASSED=0.7496, UNKNOWN=0.2058 | PASSED | 0.5438 | 0.3810 |
| other_restriction | NO=0.9843, UNKNOWN=0.0049, YES=0.0108 | NO | 0.9735 | 0.9176 |
| poa_required | NO=0.9971, UNKNOWN=0.0015, YES=0.0014 | NO | 0.9956 | 0.9799 |
| share_blocking | NO=0.9508, UNKNOWN=0.0103, YES=0.0389 | NO | 0.9119 | 0.7985 |
| votable | NO=0.0849, UNCERTAIN=0.5211, YES=0.3940 | UNCERTAIN | 0.1271 | 0.1662 |

**Likely reason / next discriminating check:** The explicitly archived proxy invitation is not resolved as no current opportunity. Compare against independently reviewed examples in this pattern after supervised training; prompt/schema ablations alone cannot establish the cause.

### false-urgency — Negation / event confusion

**Source text**

> URGENT VOTE VOTE VOTE. The word vote appears in this archived marketing example. It offers no voting opportunity.

**Expected asserted fields**
```json
{
  "votable": "NO"
}
```
**Observed factors and derived status**
```json
{
  "classification": "UNCERTAIN_MANUAL_REVIEW",
  "deadline_status": "OPEN",
  "manual_review_required": true,
  "other_restriction": false,
  "poa_required": true,
  "share_blocking": true,
  "votable": "UNCERTAIN"
}
```
Failed assertions: votable. Aggregate policy score: 0.5015.

| Factor | All native option probabilities | Winner | Top-two margin | SDK confidence |
|---|---|---|---:|---:|
| deadline_status | OPEN=0.5320, PASSED=0.4350, UNKNOWN=0.0329 | OPEN | 0.0970 | 0.2625 |
| other_restriction | NO=0.7308, UNKNOWN=0.0545, YES=0.2147 | NO | 0.5161 | 0.3463 |
| poa_required | NO=0.1293, UNKNOWN=0.0889, YES=0.7818 | YES | 0.6525 | 0.3883 |
| share_blocking | NO=0.0148, UNKNOWN=0.0229, YES=0.9622 | YES | 0.9393 | 0.8306 |
| votable | NO=0.1274, UNCERTAIN=0.5015, YES=0.3711 | UNCERTAIN | 0.1304 | 0.1112 |

**Likely reason / next discriminating check:** Repetition of vote in an explicitly non-actionable marketing archive produces uncertainty and unsupported restrictions. Compare against independently reviewed examples in this pattern after supervised training; prompt/schema ablations alone cannot establish the cause.

### de-vote — Multilingual understanding

**Source text**

> Aktionäre können ihre Stimmrechte auf der Hauptversammlung ausüben und Weisungen zur Stimmabgabe einreichen.

**Expected asserted fields**
```json
{
  "votable": "YES"
}
```
**Observed factors and derived status**
```json
{
  "classification": "UNCERTAIN_MANUAL_REVIEW",
  "deadline_status": "OPEN",
  "manual_review_required": true,
  "other_restriction": null,
  "poa_required": false,
  "share_blocking": true,
  "votable": "UNCERTAIN"
}
```
Failed assertions: votable. Aggregate policy score: 0.3777.

| Factor | All native option probabilities | Winner | Top-two margin | SDK confidence |
|---|---|---|---:|---:|
| deadline_status | OPEN=0.7998, PASSED=0.0361, UNKNOWN=0.1642 | OPEN | 0.6356 | 0.4582 |
| other_restriction | NO=0.3814, UNKNOWN=0.6001, YES=0.0185 | UNKNOWN | 0.2187 | 0.3193 |
| poa_required | NO=0.6529, UNKNOWN=0.2141, YES=0.1330 | NO | 0.4388 | 0.2021 |
| share_blocking | NO=0.3675, UNKNOWN=0.2547, YES=0.3777 | YES | 0.0102 | 0.0133 |
| votable | NO=0.2151, UNCERTAIN=0.5461, YES=0.2387 | UNCERTAIN | 0.3074 | 0.0871 |

**Likely reason / next discriminating check:** The German sentence grants voting/instruction rights; the model misses this. Translation/domain coverage is a hypothesis, not established causation. Compare against independently reviewed examples in this pattern after supervised training; prompt/schema ablations alone cannot establish the cause.

### fr-poa — Multilingual understanding

**Source text**

> Les bénéficiaires souhaitant voter à l’assemblée doivent fournir une procuration notariée obligatoire.

**Expected asserted fields**
```json
{
  "poa_required": true,
  "votable": "YES"
}
```
**Observed factors and derived status**
```json
{
  "classification": "UNCERTAIN_MANUAL_REVIEW",
  "deadline_status": "UNKNOWN",
  "manual_review_required": true,
  "other_restriction": null,
  "poa_required": null,
  "share_blocking": true,
  "votable": "UNCERTAIN"
}
```
Failed assertions: poa_required, votable. Aggregate policy score: 0.4847.

| Factor | All native option probabilities | Winner | Top-two margin | SDK confidence |
|---|---|---|---:|---:|
| deadline_status | OPEN=0.4537, PASSED=0.0431, UNKNOWN=0.5032 | UNKNOWN | 0.0495 | 0.2356 |
| other_restriction | NO=0.1623, UNKNOWN=0.6916, YES=0.1460 | UNKNOWN | 0.5293 | 0.2435 |
| poa_required | NO=0.3425, UNKNOWN=0.4847, YES=0.1728 | UNKNOWN | 0.1422 | 0.0703 |
| share_blocking | NO=0.0214, UNKNOWN=0.0926, YES=0.8861 | YES | 0.7935 | 0.6272 |
| votable | NO=0.2009, UNCERTAIN=0.6984, YES=0.1007 | UNCERTAIN | 0.4975 | 0.2679 |

**Likely reason / next discriminating check:** The French sentence explicitly requires a notarised proxy to vote; both the voting permission and POA factor are missed. Compare against independently reviewed examples in this pattern after supervised training; prompt/schema ablations alone cannot establish the cause.

### no-date — Deadline without evidence

**Source text**

> Shareholders may vote at the forthcoming AGM. Contact the custodian for the voting deadline.

**Expected asserted fields**
```json
{
  "deadline_status": "UNKNOWN",
  "votable": "YES"
}
```
**Observed factors and derived status**
```json
{
  "classification": "UNCERTAIN_MANUAL_REVIEW",
  "deadline_status": "OPEN",
  "manual_review_required": true,
  "other_restriction": null,
  "poa_required": true,
  "share_blocking": true,
  "votable": "YES"
}
```
Failed assertions: deadline_status. Aggregate policy score: 0.4170.

| Factor | All native option probabilities | Winner | Top-two margin | SDK confidence |
|---|---|---|---:|---:|
| deadline_status | OPEN=0.4922, PASSED=0.4053, UNKNOWN=0.1026 | OPEN | 0.0869 | 0.1366 |
| other_restriction | NO=0.3195, UNKNOWN=0.5506, YES=0.1299 | UNKNOWN | 0.2311 | 0.1278 |
| poa_required | NO=0.3767, UNKNOWN=0.2062, YES=0.4170 | YES | 0.0403 | 0.0369 |
| share_blocking | NO=0.1771, UNKNOWN=0.1900, YES=0.6329 | YES | 0.4429 | 0.1702 |
| votable | NO=0.1873, UNCERTAIN=0.3923, YES=0.4204 | YES | 0.0281 | 0.0487 |

**Likely reason / next discriminating check:** A referral to the custodian supplies no actual cutoff. OPEN has no supporting date. Compare against independently reviewed examples in this pattern after supervised training; prompt/schema ablations alone cannot establish the cause.

### today-date — Temporal reasoning

**Source text**

> Shareholders may vote. Instructions are due on 16 October 2026; no cutoff time is given.

**Expected asserted fields**
```json
{
  "deadline_status": "UNKNOWN",
  "votable": "YES"
}
```
**Observed factors and derived status**
```json
{
  "classification": "VOTABLE_WITH_RESTRICTION",
  "deadline_status": "OPEN",
  "manual_review_required": true,
  "other_restriction": true,
  "poa_required": true,
  "share_blocking": true,
  "votable": "YES"
}
```
Failed assertions: deadline_status. Aggregate policy score: 0.5001.

| Factor | All native option probabilities | Winner | Top-two margin | SDK confidence |
|---|---|---|---:|---:|
| deadline_status | OPEN=0.5001, PASSED=0.2853, UNKNOWN=0.2146 | OPEN | 0.2148 | 0.0582 |
| other_restriction | NO=0.2046, UNKNOWN=0.1044, YES=0.6909 | YES | 0.4863 | 0.2572 |
| poa_required | NO=0.0398, UNKNOWN=0.0162, YES=0.9440 | YES | 0.9042 | 0.7729 |
| share_blocking | NO=0.0971, UNKNOWN=0.0614, YES=0.8416 | YES | 0.7445 | 0.5059 |
| votable | NO=0.0130, UNCERTAIN=0.0201, YES=0.9669 | YES | 0.9468 | 0.8474 |

**Likely reason / next discriminating check:** With only a date and no cutoff time on the reference day, OPEN is unjustified. Compare against independently reviewed examples in this pattern after supervised training; prompt/schema ablations alone cannot establish the cause.

### negotiation — Negation / event confusion

**Source text**

> The board has voted to approve a facility agreement. No shareholder vote or action is requested.

**Expected asserted fields**
```json
{
  "votable": "NO"
}
```
**Observed factors and derived status**
```json
{
  "classification": "UNCERTAIN_MANUAL_REVIEW",
  "deadline_status": "PASSED",
  "manual_review_required": true,
  "other_restriction": false,
  "poa_required": false,
  "share_blocking": false,
  "votable": "UNCERTAIN"
}
```
Failed assertions: votable. Aggregate policy score: 0.3849.

| Factor | All native option probabilities | Winner | Top-two margin | SDK confidence |
|---|---|---|---:|---:|
| deadline_status | OPEN=0.0188, PASSED=0.9441, UNKNOWN=0.0371 | PASSED | 0.9070 | 0.7714 |
| other_restriction | NO=0.9945, UNKNOWN=0.0020, YES=0.0035 | NO | 0.9910 | 0.9655 |
| poa_required | NO=0.9961, UNKNOWN=0.0013, YES=0.0026 | NO | 0.9935 | 0.9743 |
| share_blocking | NO=0.9941, UNKNOWN=0.0017, YES=0.0041 | NO | 0.9900 | 0.9639 |
| votable | NO=0.2310, UNCERTAIN=0.3849, YES=0.3841 | UNCERTAIN | 0.0008 | 0.0229 |

**Likely reason / next discriminating check:** A completed board vote is different from a requested shareholder ballot; the explicit exclusion is not resolved to NO. Compare against independently reviewed examples in this pattern after supervised training; prompt/schema ablations alone cannot establish the cause.

### foreign-restriction — Other restriction omission

**Source text**

> Foreign shareholders may vote only after obtaining local regulatory permission; domestic holders may vote freely.

**Expected asserted fields**
```json
{
  "other_restriction": true,
  "votable": "YES"
}
```
**Observed factors and derived status**
```json
{
  "classification": "UNCERTAIN_MANUAL_REVIEW",
  "deadline_status": "UNKNOWN",
  "manual_review_required": true,
  "other_restriction": false,
  "poa_required": false,
  "share_blocking": false,
  "votable": "UNCERTAIN"
}
```
Failed assertions: other_restriction, votable. Aggregate policy score: 0.4983.

| Factor | All native option probabilities | Winner | Top-two margin | SDK confidence |
|---|---|---|---:|---:|
| deadline_status | OPEN=0.2238, PASSED=0.0597, UNKNOWN=0.7165 | UNKNOWN | 0.4927 | 0.3245 |
| other_restriction | NO=0.9660, UNKNOWN=0.0238, YES=0.0102 | NO | 0.9422 | 0.8460 |
| poa_required | NO=0.9621, UNKNOWN=0.0174, YES=0.0204 | NO | 0.9417 | 0.8296 |
| share_blocking | NO=0.8865, UNKNOWN=0.0265, YES=0.0869 | NO | 0.7996 | 0.6219 |
| votable | NO=0.0271, UNCERTAIN=0.4983, YES=0.4746 | UNCERTAIN | 0.0237 | 0.2732 |

**Likely reason / next discriminating check:** Local regulatory permission for foreign holders is an explicit eligibility restriction; it is missed alongside voting permission. Compare against independently reviewed examples in this pattern after supervised training; prompt/schema ablations alone cannot establish the cause.

### blank-like — Insufficient context

**Source text**

> Meeting: TBD. Participation: TBD. Voting: TBD.

**Expected asserted fields**
```json
{
  "votable": "UNCERTAIN"
}
```
**Observed factors and derived status**
```json
{
  "classification": "SHARE_BLOCKING",
  "deadline_status": "UNKNOWN",
  "manual_review_required": true,
  "other_restriction": false,
  "poa_required": false,
  "share_blocking": true,
  "votable": "YES"
}
```
Failed assertions: votable. Aggregate policy score: 0.5575.

| Factor | All native option probabilities | Winner | Top-two margin | SDK confidence |
|---|---|---|---:|---:|
| deadline_status | OPEN=0.0107, PASSED=0.0299, UNKNOWN=0.9593 | UNKNOWN | 0.9294 | 0.8238 |
| other_restriction | NO=0.5575, UNKNOWN=0.4131, YES=0.0295 | NO | 0.1444 | 0.2765 |
| poa_required | NO=0.6761, UNKNOWN=0.2517, YES=0.0722 | NO | 0.4244 | 0.2703 |
| share_blocking | NO=0.0775, UNKNOWN=0.2259, YES=0.6966 | YES | 0.4707 | 0.2845 |
| votable | NO=0.0572, UNCERTAIN=0.1030, YES=0.8398 | YES | 0.7368 | 0.5045 |

**Likely reason / next discriminating check:** TBD fields cannot establish either a voting opportunity or blocking. The model supplies both rather than abstaining. Compare against independently reviewed examples in this pattern after supervised training; prompt/schema ablations alone cannot establish the cause.

## Challenge contamination audit

The earlier `data/models/synthetic-smoke-v1` mechanics checkpoint used challenge fixtures. It is excluded from candidate comparison and must never be reported against the challenge as independent evidence. The official base checkpoint was not changed by that smoke run. No domain fine-tuned candidate exists yet.
