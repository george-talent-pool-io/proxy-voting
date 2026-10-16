# Fine-tuned Laya: all semantic challenge errors

Base 30/57 → fine-tuned 37/57. Fixed 13, regressed 6, remaining 14. 12 wrong cases have aggregate policy score ≥0.98.

These are unchanged, partial-field authored expectations, not customer labels. No post-test model change is made. Supplied synthetic deadline/status conventions differ from this challenge; that is an evaluation limitation, not permission to change expectations.

## Pattern counts (overlapping)

{'classification': 1, 'votable': 6, 'deadline_status': 9, 'other_restriction': 4, 'share_blocking': 1, 'poa_required': 1}

## Regressions

ambiguous, bank-holiday, issuer-custodian, meeting-only, registration, sell-restricted

## Every failed case

### bank-holiday — REGRESSION

Voting instructions are due 15 October 2026. The meeting is on 30 October 2026 and payment is on 1 November 2026.

Expected: `{"deadline_status": "PASSED"}`

Observed: `{"classification": "VOTABLE", "deadline_status": "OPEN", "manual_review_required": true, "other_restriction": false, "poa_required": false, "share_blocking": false, "votable": "YES"}`

Policy score: 1.0000. Failed assertions: deadline_status.

```json
{
  "deadline_status": {
    "OPEN": 1.0,
    "PASSED": 0.0,
    "UNKNOWN": 0.0
  },
  "other_restriction": {
    "NO": 1.0,
    "UNKNOWN": 0.0,
    "YES": 0.0
  },
  "poa_required": {
    "NO": 1.0,
    "UNKNOWN": 0.0,
    "YES": 0.0
  },
  "share_blocking": {
    "NO": 1.0,
    "UNKNOWN": 0.0,
    "YES": 0.0
  },
  "votable": {
    "NO": 0.0,
    "UNCERTAIN": 0.0,
    "YES": 1.0
  }
}
```

### contradiction — remaining error

Voting instructions are accepted. Voting instructions are not accepted. Both statements apply to the same meeting and no superseding notice is identified.

Expected: `{"votable": "UNCERTAIN"}`

Observed: `{"classification": "VOTABLE", "deadline_status": "OPEN", "manual_review_required": true, "other_restriction": false, "poa_required": false, "share_blocking": false, "votable": "YES"}`

Policy score: 1.0000. Failed assertions: votable.

```json
{
  "deadline_status": {
    "OPEN": 1.0,
    "PASSED": 0.0,
    "UNKNOWN": 0.0
  },
  "other_restriction": {
    "NO": 1.0,
    "UNKNOWN": 0.0,
    "YES": 0.0
  },
  "poa_required": {
    "NO": 1.0,
    "UNKNOWN": 0.0,
    "YES": 0.0
  },
  "share_blocking": {
    "NO": 1.0,
    "UNKNOWN": 0.0,
    "YES": 0.0
  },
  "votable": {
    "NO": 0.0,
    "UNCERTAIN": 0.0,
    "YES": 1.0
  }
}
```

### foreign-restriction — remaining error

Foreign shareholders may vote only after obtaining local regulatory permission; domestic holders may vote freely.

Expected: `{"other_restriction": true, "votable": "YES"}`

Observed: `{"classification": "VOTABLE", "deadline_status": "OPEN", "manual_review_required": true, "other_restriction": false, "poa_required": false, "share_blocking": false, "votable": "YES"}`

Policy score: 1.0000. Failed assertions: other_restriction.

```json
{
  "deadline_status": {
    "OPEN": 1.0,
    "PASSED": 0.0,
    "UNKNOWN": 0.0
  },
  "other_restriction": {
    "NO": 1.0,
    "UNKNOWN": 0.0,
    "YES": 0.0
  },
  "poa_required": {
    "NO": 1.0,
    "UNKNOWN": 0.0,
    "YES": 0.0
  },
  "share_blocking": {
    "NO": 1.0,
    "UNKNOWN": 0.0,
    "YES": 0.0
  },
  "votable": {
    "NO": 0.0,
    "UNCERTAIN": 0.0,
    "YES": 1.0
  }
}
```

### historic-quote-only — remaining error

The archive quotes a 2020 notice: "You may vote by proxy." This page is a historical archive, with no current vote.

Expected: `{"votable": "NO"}`

Observed: `{"classification": "VOTABLE", "deadline_status": "OPEN", "manual_review_required": true, "other_restriction": false, "poa_required": false, "share_blocking": false, "votable": "YES"}`

Policy score: 1.0000. Failed assertions: votable.

```json
{
  "deadline_status": {
    "OPEN": 1.0,
    "PASSED": 0.0,
    "UNKNOWN": 0.0
  },
  "other_restriction": {
    "NO": 1.0,
    "UNKNOWN": 0.0,
    "YES": 0.0
  },
  "poa_required": {
    "NO": 1.0,
    "UNKNOWN": 0.0,
    "YES": 0.0
  },
  "share_blocking": {
    "NO": 1.0,
    "UNKNOWN": 0.0,
    "YES": 0.0
  },
  "votable": {
    "NO": 0.0,
    "UNCERTAIN": 0.0,
    "YES": 1.0
  }
}
```

### issuer-custodian — REGRESSION

You may vote at the meeting. Issuer voting deadline: 30 October 2026. Our earlier custodian deadline for receipt of your instructions: 10 October 2026.

Expected: `{"deadline_status": "PASSED", "votable": "YES"}`

Observed: `{"classification": "VOTABLE", "deadline_status": "OPEN", "manual_review_required": true, "other_restriction": false, "poa_required": false, "share_blocking": false, "votable": "YES"}`

Policy score: 1.0000. Failed assertions: deadline_status.

```json
{
  "deadline_status": {
    "OPEN": 1.0,
    "PASSED": 0.0,
    "UNKNOWN": 0.0
  },
  "other_restriction": {
    "NO": 1.0,
    "UNKNOWN": 0.0,
    "YES": 0.0
  },
  "poa_required": {
    "NO": 1.0,
    "UNKNOWN": 0.0,
    "YES": 0.0
  },
  "share_blocking": {
    "NO": 1.0,
    "UNKNOWN": 0.0,
    "YES": 0.0
  },
  "votable": {
    "NO": 0.0,
    "UNCERTAIN": 0.0,
    "YES": 1.0
  }
}
```

### no-date — remaining error

Shareholders may vote at the forthcoming AGM. Contact the custodian for the voting deadline.

Expected: `{"deadline_status": "UNKNOWN", "votable": "YES"}`

Observed: `{"classification": "VOTABLE", "deadline_status": "OPEN", "manual_review_required": true, "other_restriction": false, "poa_required": false, "share_blocking": false, "votable": "YES"}`

Policy score: 1.0000. Failed assertions: deadline_status.

```json
{
  "deadline_status": {
    "OPEN": 1.0,
    "PASSED": 0.0,
    "UNKNOWN": 0.0
  },
  "other_restriction": {
    "NO": 1.0,
    "UNKNOWN": 0.0,
    "YES": 0.0
  },
  "poa_required": {
    "NO": 1.0,
    "UNKNOWN": 0.0,
    "YES": 0.0
  },
  "share_blocking": {
    "NO": 1.0,
    "UNKNOWN": 0.0,
    "YES": 0.0
  },
  "votable": {
    "NO": 0.0,
    "UNCERTAIN": 0.0,
    "YES": 1.0
  }
}
```

### record-date — remaining error

The voting record date is 1 October 2026. The AGM will be held on 30 November 2026. Shareholders may vote. No instruction deadline is specified.

Expected: `{"deadline_status": "UNKNOWN", "share_blocking": false, "votable": "YES"}`

Observed: `{"classification": "VOTABLE", "deadline_status": "OPEN", "manual_review_required": true, "other_restriction": false, "poa_required": false, "share_blocking": false, "votable": "YES"}`

Policy score: 1.0000. Failed assertions: deadline_status.

```json
{
  "deadline_status": {
    "OPEN": 1.0,
    "PASSED": 0.0,
    "UNKNOWN": 0.0
  },
  "other_restriction": {
    "NO": 1.0,
    "UNKNOWN": 0.0,
    "YES": 0.0
  },
  "poa_required": {
    "NO": 1.0,
    "UNKNOWN": 0.0,
    "YES": 0.0
  },
  "share_blocking": {
    "NO": 1.0,
    "UNKNOWN": 0.0,
    "YES": 0.0
  },
  "votable": {
    "NO": 0.0,
    "UNCERTAIN": 0.0,
    "YES": 1.0
  }
}
```

### today-date — remaining error

Shareholders may vote. Instructions are due on 16 October 2026; no cutoff time is given.

Expected: `{"deadline_status": "UNKNOWN", "votable": "YES"}`

Observed: `{"classification": "VOTABLE", "deadline_status": "OPEN", "manual_review_required": true, "other_restriction": false, "poa_required": false, "share_blocking": false, "votable": "YES"}`

Policy score: 1.0000. Failed assertions: deadline_status.

```json
{
  "deadline_status": {
    "OPEN": 1.0,
    "PASSED": 0.0,
    "UNKNOWN": 0.0
  },
  "other_restriction": {
    "NO": 1.0,
    "UNKNOWN": 0.0,
    "YES": 0.0
  },
  "poa_required": {
    "NO": 1.0,
    "UNKNOWN": 0.0,
    "YES": 0.0
  },
  "share_blocking": {
    "NO": 1.0,
    "UNKNOWN": 0.0,
    "YES": 0.0
  },
  "votable": {
    "NO": 0.0,
    "UNCERTAIN": 0.0,
    "YES": 1.0
  }
}
```

### two-dates — remaining error

Meeting date: 20 November 2026. Your voting instructions must reach our custody desk by 1 October 2026.

Expected: `{"deadline_status": "PASSED", "votable": "YES"}`

Observed: `{"classification": "VOTABLE", "deadline_status": "OPEN", "manual_review_required": true, "other_restriction": false, "poa_required": false, "share_blocking": false, "votable": "YES"}`

Policy score: 1.0000. Failed assertions: deadline_status.

```json
{
  "deadline_status": {
    "OPEN": 1.0,
    "PASSED": 0.0,
    "UNKNOWN": 0.0
  },
  "other_restriction": {
    "NO": 1.0,
    "UNKNOWN": 0.0,
    "YES": 0.0
  },
  "poa_required": {
    "NO": 1.0,
    "UNKNOWN": 0.0,
    "YES": 0.0
  },
  "share_blocking": {
    "NO": 1.0,
    "UNKNOWN": 0.0,
    "YES": 0.0
  },
  "votable": {
    "NO": 0.0,
    "UNCERTAIN": 0.0,
    "YES": 1.0
  }
}
```

### partial — remaining error

Shareholders may vote at the AGM. Split or partial voting is prohibited: all shares in an account must be voted the same way.

Expected: `{"other_restriction": true, "votable": "YES"}`

Observed: `{"classification": "VOTABLE", "deadline_status": "OPEN", "manual_review_required": true, "other_restriction": false, "poa_required": false, "share_blocking": false, "votable": "YES"}`

Policy score: 0.9987. Failed assertions: other_restriction.

```json
{
  "deadline_status": {
    "OPEN": 1.0,
    "PASSED": 0.0,
    "UNKNOWN": 0.0
  },
  "other_restriction": {
    "NO": 0.9987,
    "UNKNOWN": 0.0,
    "YES": 0.0013
  },
  "poa_required": {
    "NO": 1.0,
    "UNKNOWN": 0.0,
    "YES": 0.0
  },
  "share_blocking": {
    "NO": 1.0,
    "UNKNOWN": 0.0,
    "YES": 0.0
  },
  "votable": {
    "NO": 0.0,
    "UNCERTAIN": 0.0,
    "YES": 1.0
  }
}
```

### historical-results — remaining error

At last year’s AGM, 97% voted in favour of the remuneration policy. These are final historical results; no vote is currently open.

Expected: `{"deadline_status": "UNKNOWN", "votable": "NO"}`

Observed: `{"classification": "VOTABLE", "deadline_status": "OPEN", "manual_review_required": true, "other_restriction": false, "poa_required": false, "share_blocking": false, "votable": "YES"}`

Policy score: 0.9978. Failed assertions: deadline_status, votable.

```json
{
  "deadline_status": {
    "OPEN": 1.0,
    "PASSED": 0.0,
    "UNKNOWN": 0.0
  },
  "other_restriction": {
    "NO": 1.0,
    "UNKNOWN": 0.0,
    "YES": 0.0
  },
  "poa_required": {
    "NO": 1.0,
    "UNKNOWN": 0.0,
    "YES": 0.0
  },
  "share_blocking": {
    "NO": 1.0,
    "UNKNOWN": 0.0,
    "YES": 0.0
  },
  "votable": {
    "NO": 0.0021,
    "UNCERTAIN": 0.0001,
    "YES": 0.9978
  }
}
```

### false-urgency — remaining error

URGENT VOTE VOTE VOTE. The word vote appears in this archived marketing example. It offers no voting opportunity.

Expected: `{"votable": "NO"}`

Observed: `{"classification": "VOTABLE", "deadline_status": "OPEN", "manual_review_required": true, "other_restriction": false, "poa_required": false, "share_blocking": false, "votable": "YES"}`

Policy score: 0.9965. Failed assertions: votable.

```json
{
  "deadline_status": {
    "OPEN": 1.0,
    "PASSED": 0.0,
    "UNKNOWN": 0.0
  },
  "other_restriction": {
    "NO": 1.0,
    "UNKNOWN": 0.0,
    "YES": 0.0
  },
  "poa_required": {
    "NO": 0.9965,
    "UNKNOWN": 0.0,
    "YES": 0.0035
  },
  "share_blocking": {
    "NO": 1.0,
    "UNKNOWN": 0.0,
    "YES": 0.0
  },
  "votable": {
    "NO": 0.0,
    "UNCERTAIN": 0.0,
    "YES": 1.0
  }
}
```

### fr-poa — remaining error

Les bénéficiaires souhaitant voter à l’assemblée doivent fournir une procuration notariée obligatoire.

Expected: `{"poa_required": true, "votable": "YES"}`

Observed: `{"classification": "VOTABLE_WITH_RESTRICTION", "deadline_status": "OPEN", "manual_review_required": true, "other_restriction": true, "poa_required": false, "share_blocking": false, "votable": "YES"}`

Policy score: 0.9723. Failed assertions: poa_required.

```json
{
  "deadline_status": {
    "OPEN": 1.0,
    "PASSED": 0.0,
    "UNKNOWN": 0.0
  },
  "other_restriction": {
    "NO": 0.0277,
    "UNKNOWN": 0.0001,
    "YES": 0.9723
  },
  "poa_required": {
    "NO": 1.0,
    "UNKNOWN": 0.0,
    "YES": 0.0
  },
  "share_blocking": {
    "NO": 1.0,
    "UNKNOWN": 0.0,
    "YES": 0.0
  },
  "votable": {
    "NO": 0.0,
    "UNCERTAIN": 0.0,
    "YES": 1.0
  }
}
```

### sell-restricted — REGRESSION

Holders submitting voting instructions may not sell their shares until after the EGM.

Expected: `{"share_blocking": true, "votable": "YES"}`

Observed: `{"classification": "VOTABLE_WITH_RESTRICTION", "deadline_status": "OPEN", "manual_review_required": true, "other_restriction": true, "poa_required": false, "share_blocking": false, "votable": "YES"}`

Policy score: 0.8941. Failed assertions: share_blocking.

```json
{
  "deadline_status": {
    "OPEN": 1.0,
    "PASSED": 0.0,
    "UNKNOWN": 0.0
  },
  "other_restriction": {
    "NO": 0.1054,
    "UNKNOWN": 0.0005,
    "YES": 0.8941
  },
  "poa_required": {
    "NO": 1.0,
    "UNKNOWN": 0.0,
    "YES": 0.0
  },
  "share_blocking": {
    "NO": 1.0,
    "UNKNOWN": 0.0,
    "YES": 0.0
  },
  "votable": {
    "NO": 0.0,
    "UNCERTAIN": 0.0,
    "YES": 1.0
  }
}
```

### blank-like — remaining error

Meeting: TBD. Participation: TBD. Voting: TBD.

Expected: `{"votable": "UNCERTAIN"}`

Observed: `{"classification": "VOTABLE", "deadline_status": "UNKNOWN", "manual_review_required": true, "other_restriction": false, "poa_required": false, "share_blocking": false, "votable": "YES"}`

Policy score: 0.8407. Failed assertions: votable.

```json
{
  "deadline_status": {
    "OPEN": 0.0,
    "PASSED": 0.0,
    "UNKNOWN": 1.0
  },
  "other_restriction": {
    "NO": 0.8407,
    "UNKNOWN": 0.1592,
    "YES": 0.0001
  },
  "poa_required": {
    "NO": 0.9997,
    "UNKNOWN": 0.0003,
    "YES": 0.0
  },
  "share_blocking": {
    "NO": 0.996,
    "UNKNOWN": 0.004,
    "YES": 0.0
  },
  "votable": {
    "NO": 0.0003,
    "UNCERTAIN": 0.0007,
    "YES": 0.999
  }
}
```

### same-day — remaining error

Vote at the AGM. Voting deadline: 16 October 2026, 17:00 Tokyo time. The reference supplies a date but no time.

Expected: `{"deadline_status": "UNKNOWN"}`

Observed: `{"classification": "VOTABLE_WITH_RESTRICTION", "deadline_status": "OPEN", "manual_review_required": true, "other_restriction": true, "poa_required": false, "share_blocking": false, "votable": "YES"}`

Policy score: 0.7832. Failed assertions: deadline_status.

```json
{
  "deadline_status": {
    "OPEN": 1.0,
    "PASSED": 0.0,
    "UNKNOWN": 0.0
  },
  "other_restriction": {
    "NO": 0.2166,
    "UNKNOWN": 0.0001,
    "YES": 0.7832
  },
  "poa_required": {
    "NO": 1.0,
    "UNKNOWN": 0.0,
    "YES": 0.0
  },
  "share_blocking": {
    "NO": 1.0,
    "UNKNOWN": 0.0,
    "YES": 0.0
  },
  "votable": {
    "NO": 0.0,
    "UNCERTAIN": 0.0,
    "YES": 1.0
  }
}
```

### ambiguous — REGRESSION

Please contact your custodian for information regarding possible participation.

Expected: `{"classification": "UNCERTAIN_MANUAL_REVIEW", "votable": "UNCERTAIN"}`

Observed: `{"classification": "VOTABLE", "deadline_status": "OPEN", "manual_review_required": true, "other_restriction": false, "poa_required": false, "share_blocking": false, "votable": "YES"}`

Policy score: 0.7322. Failed assertions: classification, votable.

```json
{
  "deadline_status": {
    "OPEN": 1.0,
    "PASSED": 0.0,
    "UNKNOWN": 0.0
  },
  "other_restriction": {
    "NO": 0.7322,
    "UNKNOWN": 0.0021,
    "YES": 0.2657
  },
  "poa_required": {
    "NO": 0.9999,
    "UNKNOWN": 0.0001,
    "YES": 0.0
  },
  "share_blocking": {
    "NO": 1.0,
    "UNKNOWN": 0.0,
    "YES": 0.0
  },
  "votable": {
    "NO": 0.0,
    "UNCERTAIN": 0.0,
    "YES": 1.0
  }
}
```

### eligibility — remaining error

Only holders of Class A shares may vote on resolution 3 at the EGM. Class B shares have no voting entitlement.

Expected: `{"other_restriction": true, "votable": "YES"}`

Observed: `{"classification": "VOTABLE", "deadline_status": "OPEN", "manual_review_required": true, "other_restriction": false, "poa_required": false, "share_blocking": false, "votable": "YES"}`

Policy score: 0.6632. Failed assertions: other_restriction.

```json
{
  "deadline_status": {
    "OPEN": 1.0,
    "PASSED": 0.0,
    "UNKNOWN": 0.0
  },
  "other_restriction": {
    "NO": 0.6632,
    "UNKNOWN": 0.0001,
    "YES": 0.3367
  },
  "poa_required": {
    "NO": 1.0,
    "UNKNOWN": 0.0,
    "YES": 0.0
  },
  "share_blocking": {
    "NO": 1.0,
    "UNKNOWN": 0.0,
    "YES": 0.0
  },
  "votable": {
    "NO": 0.0,
    "UNCERTAIN": 0.0,
    "YES": 1.0
  }
}
```

### meeting-only — REGRESSION

Meeting date: 1 October 2026. This document provides no voting opportunity or deadline details.

Expected: `{"deadline_status": "UNKNOWN"}`

Observed: `{"classification": "NOT_VOTABLE", "deadline_status": "OPEN", "manual_review_required": true, "other_restriction": false, "poa_required": false, "share_blocking": false, "votable": "NO"}`

Policy score: 0.6334. Failed assertions: deadline_status.

```json
{
  "deadline_status": {
    "OPEN": 1.0,
    "PASSED": 0.0,
    "UNKNOWN": 0.0
  },
  "other_restriction": {
    "NO": 1.0,
    "UNKNOWN": 0.0,
    "YES": 0.0
  },
  "poa_required": {
    "NO": 0.9996,
    "UNKNOWN": 0.0004,
    "YES": 0.0
  },
  "share_blocking": {
    "NO": 1.0,
    "UNKNOWN": 0.0,
    "YES": 0.0
  },
  "votable": {
    "NO": 0.6334,
    "UNCERTAIN": 0.3666,
    "YES": 0.0
  }
}
```

### registration — REGRESSION

Beneficial owners wishing to vote at the AGM must register in advance in the local shareholder register.

Expected: `{"other_restriction": true, "votable": "YES"}`

Observed: `{"classification": "VOTABLE", "deadline_status": "OPEN", "manual_review_required": true, "other_restriction": false, "poa_required": false, "share_blocking": false, "votable": "YES"}`

Policy score: 0.5739. Failed assertions: other_restriction.

```json
{
  "deadline_status": {
    "OPEN": 1.0,
    "PASSED": 0.0,
    "UNKNOWN": 0.0
  },
  "other_restriction": {
    "NO": 0.5739,
    "UNKNOWN": 0.0004,
    "YES": 0.4257
  },
  "poa_required": {
    "NO": 1.0,
    "UNKNOWN": 0.0,
    "YES": 0.0
  },
  "share_blocking": {
    "NO": 1.0,
    "UNKNOWN": 0.0,
    "YES": 0.0
  },
  "votable": {
    "NO": 0.0,
    "UNCERTAIN": 0.0,
    "YES": 1.0
  }
}
```

