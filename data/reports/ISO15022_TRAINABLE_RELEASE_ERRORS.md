# Trainable release engineering errors

All truth below is AI-authored construction truth. No customer accuracy claim.

## VALIDATION / BASE_LAYA / 192427e9aa3ca6f904eb505ac724d3c90e8eba48b9c676788a55d6e407fcb195 / share_blocking

```text
[Message EL0206C | MT564]
Broker service update: the institutional ballot channel is now available for this agenda.
This is solely a cash-distribution advice; it offers no meeting ballot and no shareholder vote.
No requirement for a voting lock on the position applies.
No requirement for a compulsory attorney mandate applies.
No requirement for mandatory meeting registration applies.
No requirement for identification of the underlying owner applies.
No requirement for a custodial holding statement applies.
No requirement for a requirement to cast all votes identically applies.
No requirement for recall of lent securities applies.
No requirement for an in-person-only voting condition applies.


[Message EL0206D | MT568]
Please retain the replacement edition for operational reconciliation. Earlier notification conditions are superseded.

```

```json
{
  "truth": "NO",
  "prediction": {
    "value": "YES",
    "scores": {
      "YES": 0.9813,
      "NO": 0.006,
      "UNKNOWN": 0.0127
    },
    "native_score": 0.9813,
    "confidence": null,
    "source": "REGISTERED_LAYA_PASSAGES",
    "evidence": [
      {
        "valid": true,
        "text": "Earlier notification conditions are superseded.",
        "start": 799,
        "end": 846,
        "source": "NATIVE_LAYA_PASSAGE_WITH_DETERMINISTIC_SCOPE"
      }
    ],
    "aggregation_reason": "STRONG_CURRENT_RELEVANT_EVIDENCE"
  },
  "whole_notice_scores": {
    "YES": 0.9242,
    "NO": 0.0505,
    "UNKNOWN": 0.0253
  },
  "passage_scores": [
    {
      "text": "[Message EL0206C | MT564]",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.9634,
        "NO": 0.0132,
        "UNKNOWN": 0.0234
      },
      "score": 0.9634,
      "margin": 0.9400000000000001,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "Broker service update: the institutional ballot channel is now available for this agenda.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.9233,
        "NO": 0.0399,
        "UNKNOWN": 0.0368
      },
      "score": 0.9233,
      "margin": 0.8834,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "This is solely a cash-distribution advice; it offers no meeting ballot and no shareholder vote.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.9739,
        "NO": 0.0137,
        "UNKNOWN": 0.0124
      },
      "score": 0.9739,
      "margin": 0.9601999999999999,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for a voting lock on the position applies.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.9194,
        "NO": 0.055,
        "UNKNOWN": 0.0257
      },
      "score": 0.9194,
      "margin": 0.8644,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for a compulsory attorney mandate applies.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.971,
        "NO": 0.0181,
        "UNKNOWN": 0.0109
      },
      "score": 0.971,
      "margin": 0.9529,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for mandatory meeting registration applies.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.9611,
        "NO": 0.019,
        "UNKNOWN": 0.0199
      },
      "score": 0.9611,
      "margin": 0.9411999999999999,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for identification of the underlying owner applies.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.9639,
        "NO": 0.0177,
        "UNKNOWN": 0.0184
      },
      "score": 0.9639,
      "margin": 0.9455,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for a custodial holding statement applies.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.9504,
        "NO": 0.0281,
        "UNKNOWN": 0.0215
      },
      "score": 0.9504,
      "margin": 0.9223,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for a requirement to cast all votes identically applies.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.9324,
        "NO": 0.0361,
        "UNKNOWN": 0.0315
      },
      "score": 0.9324,
      "margin": 0.8963,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for recall of lent securities applies.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.9627,
        "NO": 0.0206,
        "UNKNOWN": 0.0167
      },
      "score": 0.9627,
      "margin": 0.9421,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for an in-person-only voting condition applies.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.5791,
        "NO": 0.2824,
        "UNKNOWN": 0.1386
      },
      "score": 0.5791,
      "margin": 0.29669999999999996,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "[Message EL0206D | MT568]",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.9641,
        "NO": 0.0134,
        "UNKNOWN": 0.0225
      },
      "score": 0.9641,
      "margin": 0.9416,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "Please retain the replacement edition for operational reconciliation.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.9526,
        "NO": 0.0272,
        "UNKNOWN": 0.0201
      },
      "score": 0.9526,
      "margin": 0.9254,
      "historical": false,
      "supersession": true,
      "conditional": false
    },
    {
      "text": "Earlier notification conditions are superseded.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.9813,
        "NO": 0.006,
        "UNKNOWN": 0.0127
      },
      "score": 0.9813,
      "margin": 0.9685999999999999,
      "historical": false,
      "supersession": true,
      "conditional": false
    }
  ],
  "escalation": {
    "escalated": false,
    "requested_predicates": [
      "votability",
      "share_blocking",
      "poa_required",
      "registration_required",
      "beneficial_owner_disclosure_required",
      "holding_confirmation_required",
      "split_voting_restricted",
      "securities_lending_recall_required",
      "other_voting_restriction"
    ],
    "reasons": {
      "votability": [
        "LOW_RAW_SCORE",
        "LOW_MARGIN"
      ],
      "share_blocking": [
        "LOW_RAW_SCORE"
      ],
      "poa_required": [
        "LOW_RAW_SCORE",
        "LOW_MARGIN",
        "EVIDENCE_UNAVAILABLE"
      ],
      "registration_required": [
        "LOW_RAW_SCORE"
      ],
      "beneficial_owner_disclosure_required": [
        "LOW_RAW_SCORE"
      ],
      "holding_confirmation_required": [
        "UNKNOWN",
        "LOW_RAW_SCORE",
        "LOW_MARGIN",
        "EVIDENCE_UNAVAILABLE"
      ],
      "split_voting_restricted": [
        "LOW_RAW_SCORE",
        "LOW_MARGIN"
      ],
      "securities_lending_recall_required": [
        "LOW_RAW_SCORE"
      ],
      "other_voting_restriction": [
        "UNKNOWN",
        "PASSAGE_CONFLICT",
        "LOW_RAW_SCORE",
        "LOW_MARGIN",
        "EVIDENCE_UNAVAILABLE"
      ]
    }
  },
  "conflicts": [
    "other_voting_restriction:PASSAGE_CONFLICT"
  ],
  "reconciliation_for_field": []
}
```

## VALIDATION / BASE_LAYA / 192427e9aa3ca6f904eb505ac724d3c90e8eba48b9c676788a55d6e407fcb195 / registration_required

```text
[Message EL0206C | MT564]
Broker service update: the institutional ballot channel is now available for this agenda.
This is solely a cash-distribution advice; it offers no meeting ballot and no shareholder vote.
No requirement for a voting lock on the position applies.
No requirement for a compulsory attorney mandate applies.
No requirement for mandatory meeting registration applies.
No requirement for identification of the underlying owner applies.
No requirement for a custodial holding statement applies.
No requirement for a requirement to cast all votes identically applies.
No requirement for recall of lent securities applies.
No requirement for an in-person-only voting condition applies.


[Message EL0206D | MT568]
Please retain the replacement edition for operational reconciliation. Earlier notification conditions are superseded.

```

```json
{
  "truth": "NO",
  "prediction": {
    "value": "YES",
    "scores": {
      "YES": 0.9047,
      "NO": 0.0765,
      "UNKNOWN": 0.0188
    },
    "native_score": 0.9047,
    "confidence": null,
    "source": "REGISTERED_LAYA_PASSAGES",
    "evidence": [
      {
        "valid": true,
        "text": "No requirement for a custodial holding statement applies.",
        "start": 454,
        "end": 511,
        "source": "NATIVE_LAYA_PASSAGE_WITH_DETERMINISTIC_SCOPE"
      }
    ],
    "aggregation_reason": "STRONG_CURRENT_RELEVANT_EVIDENCE"
  },
  "whole_notice_scores": {
    "YES": 0.4292,
    "NO": 0.4262,
    "UNKNOWN": 0.1446
  },
  "passage_scores": [
    {
      "text": "[Message EL0206C | MT564]",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.6133,
        "NO": 0.1853,
        "UNKNOWN": 0.2014
      },
      "score": 0.6133,
      "margin": 0.41189999999999993,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "Broker service update: the institutional ballot channel is now available for this agenda.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.4424,
        "NO": 0.4236,
        "UNKNOWN": 0.134
      },
      "score": 0.4424,
      "margin": 0.01880000000000004,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "This is solely a cash-distribution advice; it offers no meeting ballot and no shareholder vote.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.8686,
        "NO": 0.1138,
        "UNKNOWN": 0.0176
      },
      "score": 0.8686,
      "margin": 0.7548,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for a voting lock on the position applies.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.7796,
        "NO": 0.2015,
        "UNKNOWN": 0.0189
      },
      "score": 0.7796,
      "margin": 0.5781,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for a compulsory attorney mandate applies.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.8924,
        "NO": 0.0953,
        "UNKNOWN": 0.0123
      },
      "score": 0.8924,
      "margin": 0.7970999999999999,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for mandatory meeting registration applies.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.7687,
        "NO": 0.2091,
        "UNKNOWN": 0.0222
      },
      "score": 0.7687,
      "margin": 0.5596000000000001,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for identification of the underlying owner applies.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.7749,
        "NO": 0.1967,
        "UNKNOWN": 0.0284
      },
      "score": 0.7749,
      "margin": 0.5782,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for a custodial holding statement applies.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.9047,
        "NO": 0.0765,
        "UNKNOWN": 0.0188
      },
      "score": 0.9047,
      "margin": 0.8281999999999999,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for a requirement to cast all votes identically applies.",
      "state": "UNKNOWN",
      "native_value": "NO",
      "scores": {
        "YES": 0.3528,
        "NO": 0.5926,
        "UNKNOWN": 0.0546
      },
      "score": 0.5926,
      "margin": 0.2398,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for recall of lent securities applies.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.7747,
        "NO": 0.196,
        "UNKNOWN": 0.0293
      },
      "score": 0.7747,
      "margin": 0.5787,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for an in-person-only voting condition applies.",
      "state": "UNKNOWN",
      "native_value": "NO",
      "scores": {
        "YES": 0.1364,
        "NO": 0.6687,
        "UNKNOWN": 0.1949
      },
      "score": 0.6687,
      "margin": 0.4738,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "[Message EL0206D | MT568]",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.5789,
        "NO": 0.2101,
        "UNKNOWN": 0.211
      },
      "score": 0.5789,
      "margin": 0.3679,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "Please retain the replacement edition for operational reconciliation.",
      "state": "UNKNOWN",
      "native_value": "NO",
      "scores": {
        "YES": 0.4564,
        "NO": 0.4659,
        "UNKNOWN": 0.0777
      },
      "score": 0.4659,
      "margin": 0.009500000000000008,
      "historical": false,
      "supersession": true,
      "conditional": false
    },
    {
      "text": "Earlier notification conditions are superseded.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.7002,
        "NO": 0.2553,
        "UNKNOWN": 0.0446
      },
      "score": 0.7002,
      "margin": 0.4449,
      "historical": false,
      "supersession": true,
      "conditional": false
    }
  ],
  "escalation": {
    "escalated": false,
    "requested_predicates": [
      "votability",
      "share_blocking",
      "poa_required",
      "registration_required",
      "beneficial_owner_disclosure_required",
      "holding_confirmation_required",
      "split_voting_restricted",
      "securities_lending_recall_required",
      "other_voting_restriction"
    ],
    "reasons": {
      "votability": [
        "LOW_RAW_SCORE",
        "LOW_MARGIN"
      ],
      "share_blocking": [
        "LOW_RAW_SCORE"
      ],
      "poa_required": [
        "LOW_RAW_SCORE",
        "LOW_MARGIN",
        "EVIDENCE_UNAVAILABLE"
      ],
      "registration_required": [
        "LOW_RAW_SCORE"
      ],
      "beneficial_owner_disclosure_required": [
        "LOW_RAW_SCORE"
      ],
      "holding_confirmation_required": [
        "UNKNOWN",
        "LOW_RAW_SCORE",
        "LOW_MARGIN",
        "EVIDENCE_UNAVAILABLE"
      ],
      "split_voting_restricted": [
        "LOW_RAW_SCORE",
        "LOW_MARGIN"
      ],
      "securities_lending_recall_required": [
        "LOW_RAW_SCORE"
      ],
      "other_voting_restriction": [
        "UNKNOWN",
        "PASSAGE_CONFLICT",
        "LOW_RAW_SCORE",
        "LOW_MARGIN",
        "EVIDENCE_UNAVAILABLE"
      ]
    }
  },
  "conflicts": [
    "other_voting_restriction:PASSAGE_CONFLICT"
  ],
  "reconciliation_for_field": []
}
```

## VALIDATION / BASE_LAYA / 192427e9aa3ca6f904eb505ac724d3c90e8eba48b9c676788a55d6e407fcb195 / holding_confirmation_required

```text
[Message EL0206C | MT564]
Broker service update: the institutional ballot channel is now available for this agenda.
This is solely a cash-distribution advice; it offers no meeting ballot and no shareholder vote.
No requirement for a voting lock on the position applies.
No requirement for a compulsory attorney mandate applies.
No requirement for mandatory meeting registration applies.
No requirement for identification of the underlying owner applies.
No requirement for a custodial holding statement applies.
No requirement for a requirement to cast all votes identically applies.
No requirement for recall of lent securities applies.
No requirement for an in-person-only voting condition applies.


[Message EL0206D | MT568]
Please retain the replacement edition for operational reconciliation. Earlier notification conditions are superseded.

```

```json
{
  "truth": "NO",
  "prediction": {
    "value": "UNKNOWN",
    "scores": {},
    "native_score": null,
    "confidence": null,
    "source": "REGISTERED_LAYA_PASSAGES",
    "evidence": [],
    "aggregation_reason": "NO_STRONG_CURRENT_RELEVANT_STATEMENT"
  },
  "whole_notice_scores": {
    "YES": 0.5881,
    "NO": 0.2247,
    "UNKNOWN": 0.1872
  },
  "passage_scores": [
    {
      "text": "[Message EL0206C | MT564]",
      "state": "UNKNOWN",
      "native_value": "NO",
      "scores": {
        "YES": 0.0718,
        "NO": 0.6152,
        "UNKNOWN": 0.3129
      },
      "score": 0.6152,
      "margin": 0.30229999999999996,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "Broker service update: the institutional ballot channel is now available for this agenda.",
      "state": "UNKNOWN",
      "native_value": "NO",
      "scores": {
        "YES": 0.2407,
        "NO": 0.4441,
        "UNKNOWN": 0.3152
      },
      "score": 0.4441,
      "margin": 0.12890000000000001,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "This is solely a cash-distribution advice; it offers no meeting ballot and no shareholder vote.",
      "state": "UNKNOWN",
      "native_value": "NO",
      "scores": {
        "YES": 0.1325,
        "NO": 0.7123,
        "UNKNOWN": 0.1551
      },
      "score": 0.7123,
      "margin": 0.5572,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for a voting lock on the position applies.",
      "state": "UNKNOWN",
      "native_value": "NO",
      "scores": {
        "YES": 0.0868,
        "NO": 0.7534,
        "UNKNOWN": 0.1599
      },
      "score": 0.7534,
      "margin": 0.5934999999999999,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for a compulsory attorney mandate applies.",
      "state": "UNKNOWN",
      "native_value": "NO",
      "scores": {
        "YES": 0.1067,
        "NO": 0.7334,
        "UNKNOWN": 0.16
      },
      "score": 0.7334,
      "margin": 0.5734,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for mandatory meeting registration applies.",
      "state": "UNKNOWN",
      "native_value": "NO",
      "scores": {
        "YES": 0.0964,
        "NO": 0.7201,
        "UNKNOWN": 0.1836
      },
      "score": 0.7201,
      "margin": 0.5365,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for identification of the underlying owner applies.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.4708,
        "NO": 0.3903,
        "UNKNOWN": 0.1389
      },
      "score": 0.4708,
      "margin": 0.08050000000000002,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for a custodial holding statement applies.",
      "state": "NEGATIVE",
      "native_value": "NO",
      "scores": {
        "YES": 0.1843,
        "NO": 0.538,
        "UNKNOWN": 0.2777
      },
      "score": 0.538,
      "margin": 0.26030000000000003,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for a requirement to cast all votes identically applies.",
      "state": "UNKNOWN",
      "native_value": "NO",
      "scores": {
        "YES": 0.0727,
        "NO": 0.8431,
        "UNKNOWN": 0.0842
      },
      "score": 0.8431,
      "margin": 0.7588999999999999,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for recall of lent securities applies.",
      "state": "UNKNOWN",
      "native_value": "NO",
      "scores": {
        "YES": 0.0706,
        "NO": 0.8292,
        "UNKNOWN": 0.1002
      },
      "score": 0.8292,
      "margin": 0.7290000000000001,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for an in-person-only voting condition applies.",
      "state": "UNKNOWN",
      "native_value": "NO",
      "scores": {
        "YES": 0.024,
        "NO": 0.7343,
        "UNKNOWN": 0.2417
      },
      "score": 0.7343,
      "margin": 0.4925999999999999,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "[Message EL0206D | MT568]",
      "state": "UNKNOWN",
      "native_value": "NO",
      "scores": {
        "YES": 0.0572,
        "NO": 0.6858,
        "UNKNOWN": 0.257
      },
      "score": 0.6858,
      "margin": 0.42879999999999996,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "Please retain the replacement edition for operational reconciliation.",
      "state": "UNKNOWN",
      "native_value": "NO",
      "scores": {
        "YES": 0.163,
        "NO": 0.6909,
        "UNKNOWN": 0.1461
      },
      "score": 0.6909,
      "margin": 0.5278999999999999,
      "historical": false,
      "supersession": true,
      "conditional": false
    },
    {
      "text": "Earlier notification conditions are superseded.",
      "state": "UNKNOWN",
      "native_value": "UNKNOWN",
      "scores": {
        "YES": 0.2717,
        "NO": 0.2909,
        "UNKNOWN": 0.4374
      },
      "score": 0.4374,
      "margin": 0.14650000000000002,
      "historical": false,
      "supersession": true,
      "conditional": false
    }
  ],
  "escalation": {
    "escalated": false,
    "requested_predicates": [
      "votability",
      "share_blocking",
      "poa_required",
      "registration_required",
      "beneficial_owner_disclosure_required",
      "holding_confirmation_required",
      "split_voting_restricted",
      "securities_lending_recall_required",
      "other_voting_restriction"
    ],
    "reasons": {
      "votability": [
        "LOW_RAW_SCORE",
        "LOW_MARGIN"
      ],
      "share_blocking": [
        "LOW_RAW_SCORE"
      ],
      "poa_required": [
        "LOW_RAW_SCORE",
        "LOW_MARGIN",
        "EVIDENCE_UNAVAILABLE"
      ],
      "registration_required": [
        "LOW_RAW_SCORE"
      ],
      "beneficial_owner_disclosure_required": [
        "LOW_RAW_SCORE"
      ],
      "holding_confirmation_required": [
        "UNKNOWN",
        "LOW_RAW_SCORE",
        "LOW_MARGIN",
        "EVIDENCE_UNAVAILABLE"
      ],
      "split_voting_restricted": [
        "LOW_RAW_SCORE",
        "LOW_MARGIN"
      ],
      "securities_lending_recall_required": [
        "LOW_RAW_SCORE"
      ],
      "other_voting_restriction": [
        "UNKNOWN",
        "PASSAGE_CONFLICT",
        "LOW_RAW_SCORE",
        "LOW_MARGIN",
        "EVIDENCE_UNAVAILABLE"
      ]
    }
  },
  "conflicts": [
    "other_voting_restriction:PASSAGE_CONFLICT"
  ],
  "reconciliation_for_field": []
}
```

## VALIDATION / BASE_LAYA / 192427e9aa3ca6f904eb505ac724d3c90e8eba48b9c676788a55d6e407fcb195 / split_voting_restricted

```text
[Message EL0206C | MT564]
Broker service update: the institutional ballot channel is now available for this agenda.
This is solely a cash-distribution advice; it offers no meeting ballot and no shareholder vote.
No requirement for a voting lock on the position applies.
No requirement for a compulsory attorney mandate applies.
No requirement for mandatory meeting registration applies.
No requirement for identification of the underlying owner applies.
No requirement for a custodial holding statement applies.
No requirement for a requirement to cast all votes identically applies.
No requirement for recall of lent securities applies.
No requirement for an in-person-only voting condition applies.


[Message EL0206D | MT568]
Please retain the replacement edition for operational reconciliation. Earlier notification conditions are superseded.

```

```json
{
  "truth": "NO",
  "prediction": {
    "value": "YES",
    "scores": {
      "YES": 0.7599,
      "NO": 0.1949,
      "UNKNOWN": 0.0453
    },
    "native_score": 0.7599,
    "confidence": null,
    "source": "REGISTERED_LAYA_PASSAGES",
    "evidence": [
      {
        "valid": true,
        "text": "This is solely a cash-distribution advice; it offers no meeting ballot and no shareholder vote.",
        "start": 116,
        "end": 211,
        "source": "NATIVE_LAYA_PASSAGE_WITH_DETERMINISTIC_SCOPE"
      }
    ],
    "aggregation_reason": "STRONG_CURRENT_RELEVANT_EVIDENCE"
  },
  "whole_notice_scores": {
    "YES": 0.3961,
    "NO": 0.5428,
    "UNKNOWN": 0.0611
  },
  "passage_scores": [
    {
      "text": "[Message EL0206C | MT564]",
      "state": "UNKNOWN",
      "native_value": "NO",
      "scores": {
        "YES": 0.3052,
        "NO": 0.37,
        "UNKNOWN": 0.3248
      },
      "score": 0.37,
      "margin": 0.04520000000000002,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "Broker service update: the institutional ballot channel is now available for this agenda.",
      "state": "UNKNOWN",
      "native_value": "NO",
      "scores": {
        "YES": 0.2694,
        "NO": 0.6047,
        "UNKNOWN": 0.1259
      },
      "score": 0.6047,
      "margin": 0.33530000000000004,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "This is solely a cash-distribution advice; it offers no meeting ballot and no shareholder vote.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.7599,
        "NO": 0.1949,
        "UNKNOWN": 0.0453
      },
      "score": 0.7599,
      "margin": 0.5650000000000001,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for a voting lock on the position applies.",
      "state": "UNKNOWN",
      "native_value": "NO",
      "scores": {
        "YES": 0.3324,
        "NO": 0.5808,
        "UNKNOWN": 0.0869
      },
      "score": 0.5808,
      "margin": 0.2484,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for a compulsory attorney mandate applies.",
      "state": "UNKNOWN",
      "native_value": "NO",
      "scores": {
        "YES": 0.3261,
        "NO": 0.5547,
        "UNKNOWN": 0.1191
      },
      "score": 0.5547,
      "margin": 0.22859999999999997,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for mandatory meeting registration applies.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.5754,
        "NO": 0.3946,
        "UNKNOWN": 0.0301
      },
      "score": 0.5754,
      "margin": 0.18080000000000002,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for identification of the underlying owner applies.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.4463,
        "NO": 0.3747,
        "UNKNOWN": 0.179
      },
      "score": 0.4463,
      "margin": 0.0716,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for a custodial holding statement applies.",
      "state": "UNKNOWN",
      "native_value": "NO",
      "scores": {
        "YES": 0.2549,
        "NO": 0.6488,
        "UNKNOWN": 0.0962
      },
      "score": 0.6488,
      "margin": 0.39390000000000003,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for a requirement to cast all votes identically applies.",
      "state": "UNKNOWN",
      "native_value": "NO",
      "scores": {
        "YES": 0.2188,
        "NO": 0.7354,
        "UNKNOWN": 0.0457
      },
      "score": 0.7354,
      "margin": 0.5166000000000001,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for recall of lent securities applies.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.7305,
        "NO": 0.2272,
        "UNKNOWN": 0.0423
      },
      "score": 0.7305,
      "margin": 0.5033000000000001,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for an in-person-only voting condition applies.",
      "state": "UNKNOWN",
      "native_value": "NO",
      "scores": {
        "YES": 0.4082,
        "NO": 0.5024,
        "UNKNOWN": 0.0894
      },
      "score": 0.5024,
      "margin": 0.09419999999999995,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "[Message EL0206D | MT568]",
      "state": "UNKNOWN",
      "native_value": "NO",
      "scores": {
        "YES": 0.2183,
        "NO": 0.4406,
        "UNKNOWN": 0.3412
      },
      "score": 0.4406,
      "margin": 0.09939999999999999,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "Please retain the replacement edition for operational reconciliation.",
      "state": "UNKNOWN",
      "native_value": "NO",
      "scores": {
        "YES": 0.1878,
        "NO": 0.7525,
        "UNKNOWN": 0.0598
      },
      "score": 0.7525,
      "margin": 0.5647,
      "historical": false,
      "supersession": true,
      "conditional": false
    },
    {
      "text": "Earlier notification conditions are superseded.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.5756,
        "NO": 0.3457,
        "UNKNOWN": 0.0786
      },
      "score": 0.5756,
      "margin": 0.2299,
      "historical": false,
      "supersession": true,
      "conditional": false
    }
  ],
  "escalation": {
    "escalated": false,
    "requested_predicates": [
      "votability",
      "share_blocking",
      "poa_required",
      "registration_required",
      "beneficial_owner_disclosure_required",
      "holding_confirmation_required",
      "split_voting_restricted",
      "securities_lending_recall_required",
      "other_voting_restriction"
    ],
    "reasons": {
      "votability": [
        "LOW_RAW_SCORE",
        "LOW_MARGIN"
      ],
      "share_blocking": [
        "LOW_RAW_SCORE"
      ],
      "poa_required": [
        "LOW_RAW_SCORE",
        "LOW_MARGIN",
        "EVIDENCE_UNAVAILABLE"
      ],
      "registration_required": [
        "LOW_RAW_SCORE"
      ],
      "beneficial_owner_disclosure_required": [
        "LOW_RAW_SCORE"
      ],
      "holding_confirmation_required": [
        "UNKNOWN",
        "LOW_RAW_SCORE",
        "LOW_MARGIN",
        "EVIDENCE_UNAVAILABLE"
      ],
      "split_voting_restricted": [
        "LOW_RAW_SCORE",
        "LOW_MARGIN"
      ],
      "securities_lending_recall_required": [
        "LOW_RAW_SCORE"
      ],
      "other_voting_restriction": [
        "UNKNOWN",
        "PASSAGE_CONFLICT",
        "LOW_RAW_SCORE",
        "LOW_MARGIN",
        "EVIDENCE_UNAVAILABLE"
      ]
    }
  },
  "conflicts": [
    "other_voting_restriction:PASSAGE_CONFLICT"
  ],
  "reconciliation_for_field": []
}
```

## VALIDATION / BASE_LAYA / 192427e9aa3ca6f904eb505ac724d3c90e8eba48b9c676788a55d6e407fcb195 / securities_lending_recall_required

```text
[Message EL0206C | MT564]
Broker service update: the institutional ballot channel is now available for this agenda.
This is solely a cash-distribution advice; it offers no meeting ballot and no shareholder vote.
No requirement for a voting lock on the position applies.
No requirement for a compulsory attorney mandate applies.
No requirement for mandatory meeting registration applies.
No requirement for identification of the underlying owner applies.
No requirement for a custodial holding statement applies.
No requirement for a requirement to cast all votes identically applies.
No requirement for recall of lent securities applies.
No requirement for an in-person-only voting condition applies.


[Message EL0206D | MT568]
Please retain the replacement edition for operational reconciliation. Earlier notification conditions are superseded.

```

```json
{
  "truth": "NO",
  "prediction": {
    "value": "YES",
    "scores": {
      "YES": 0.8663,
      "NO": 0.1108,
      "UNKNOWN": 0.0229
    },
    "native_score": 0.8663,
    "confidence": null,
    "source": "REGISTERED_LAYA_PASSAGES",
    "evidence": [
      {
        "valid": true,
        "text": "No requirement for a custodial holding statement applies.",
        "start": 454,
        "end": 511,
        "source": "NATIVE_LAYA_PASSAGE_WITH_DETERMINISTIC_SCOPE"
      }
    ],
    "aggregation_reason": "STRONG_CURRENT_RELEVANT_EVIDENCE"
  },
  "whole_notice_scores": {
    "YES": 0.5857,
    "NO": 0.3415,
    "UNKNOWN": 0.0728
  },
  "passage_scores": [
    {
      "text": "[Message EL0206C | MT564]",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.6409,
        "NO": 0.2363,
        "UNKNOWN": 0.1228
      },
      "score": 0.6409,
      "margin": 0.4046,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "Broker service update: the institutional ballot channel is now available for this agenda.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.6504,
        "NO": 0.2317,
        "UNKNOWN": 0.1179
      },
      "score": 0.6504,
      "margin": 0.41869999999999996,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "This is solely a cash-distribution advice; it offers no meeting ballot and no shareholder vote.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.6909,
        "NO": 0.2685,
        "UNKNOWN": 0.0406
      },
      "score": 0.6909,
      "margin": 0.42239999999999994,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for a voting lock on the position applies.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.7725,
        "NO": 0.19,
        "UNKNOWN": 0.0375
      },
      "score": 0.7725,
      "margin": 0.5825,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for a compulsory attorney mandate applies.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.7769,
        "NO": 0.1866,
        "UNKNOWN": 0.0365
      },
      "score": 0.7769,
      "margin": 0.5903,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for mandatory meeting registration applies.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.7737,
        "NO": 0.1828,
        "UNKNOWN": 0.0436
      },
      "score": 0.7737,
      "margin": 0.5909000000000001,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for identification of the underlying owner applies.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.7506,
        "NO": 0.1963,
        "UNKNOWN": 0.0531
      },
      "score": 0.7506,
      "margin": 0.5543,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for a custodial holding statement applies.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.8663,
        "NO": 0.1108,
        "UNKNOWN": 0.0229
      },
      "score": 0.8663,
      "margin": 0.7555,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for a requirement to cast all votes identically applies.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.536,
        "NO": 0.415,
        "UNKNOWN": 0.049
      },
      "score": 0.536,
      "margin": 0.12100000000000005,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for recall of lent securities applies.",
      "state": "NEGATIVE",
      "native_value": "NO",
      "scores": {
        "YES": 0.3652,
        "NO": 0.6196,
        "UNKNOWN": 0.0152
      },
      "score": 0.6196,
      "margin": 0.2544,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for an in-person-only voting condition applies.",
      "state": "UNKNOWN",
      "native_value": "NO",
      "scores": {
        "YES": 0.2951,
        "NO": 0.5457,
        "UNKNOWN": 0.1592
      },
      "score": 0.5457,
      "margin": 0.2506,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "[Message EL0206D | MT568]",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.6235,
        "NO": 0.2348,
        "UNKNOWN": 0.1418
      },
      "score": 0.6235,
      "margin": 0.38870000000000005,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "Please retain the replacement edition for operational reconciliation.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.5798,
        "NO": 0.335,
        "UNKNOWN": 0.0852
      },
      "score": 0.5798,
      "margin": 0.24479999999999996,
      "historical": false,
      "supersession": true,
      "conditional": false
    },
    {
      "text": "Earlier notification conditions are superseded.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.7353,
        "NO": 0.2046,
        "UNKNOWN": 0.0601
      },
      "score": 0.7353,
      "margin": 0.5307,
      "historical": false,
      "supersession": true,
      "conditional": false
    }
  ],
  "escalation": {
    "escalated": false,
    "requested_predicates": [
      "votability",
      "share_blocking",
      "poa_required",
      "registration_required",
      "beneficial_owner_disclosure_required",
      "holding_confirmation_required",
      "split_voting_restricted",
      "securities_lending_recall_required",
      "other_voting_restriction"
    ],
    "reasons": {
      "votability": [
        "LOW_RAW_SCORE",
        "LOW_MARGIN"
      ],
      "share_blocking": [
        "LOW_RAW_SCORE"
      ],
      "poa_required": [
        "LOW_RAW_SCORE",
        "LOW_MARGIN",
        "EVIDENCE_UNAVAILABLE"
      ],
      "registration_required": [
        "LOW_RAW_SCORE"
      ],
      "beneficial_owner_disclosure_required": [
        "LOW_RAW_SCORE"
      ],
      "holding_confirmation_required": [
        "UNKNOWN",
        "LOW_RAW_SCORE",
        "LOW_MARGIN",
        "EVIDENCE_UNAVAILABLE"
      ],
      "split_voting_restricted": [
        "LOW_RAW_SCORE",
        "LOW_MARGIN"
      ],
      "securities_lending_recall_required": [
        "LOW_RAW_SCORE"
      ],
      "other_voting_restriction": [
        "UNKNOWN",
        "PASSAGE_CONFLICT",
        "LOW_RAW_SCORE",
        "LOW_MARGIN",
        "EVIDENCE_UNAVAILABLE"
      ]
    }
  },
  "conflicts": [
    "other_voting_restriction:PASSAGE_CONFLICT"
  ],
  "reconciliation_for_field": []
}
```

## VALIDATION / BASE_LAYA / 192427e9aa3ca6f904eb505ac724d3c90e8eba48b9c676788a55d6e407fcb195 / other_voting_restriction

```text
[Message EL0206C | MT564]
Broker service update: the institutional ballot channel is now available for this agenda.
This is solely a cash-distribution advice; it offers no meeting ballot and no shareholder vote.
No requirement for a voting lock on the position applies.
No requirement for a compulsory attorney mandate applies.
No requirement for mandatory meeting registration applies.
No requirement for identification of the underlying owner applies.
No requirement for a custodial holding statement applies.
No requirement for a requirement to cast all votes identically applies.
No requirement for recall of lent securities applies.
No requirement for an in-person-only voting condition applies.


[Message EL0206D | MT568]
Please retain the replacement edition for operational reconciliation. Earlier notification conditions are superseded.

```

```json
{
  "truth": "NO",
  "prediction": {
    "value": "UNKNOWN",
    "scores": {},
    "native_score": null,
    "confidence": null,
    "source": "REGISTERED_LAYA_PASSAGES",
    "evidence": [],
    "aggregation_reason": "CURRENT_PASSAGE_CONFLICT_OR_DISTINCT_VOTING_ROUTES"
  },
  "whole_notice_scores": {
    "YES": 0.5337,
    "NO": 0.3905,
    "UNKNOWN": 0.0758
  },
  "passage_scores": [
    {
      "text": "[Message EL0206C | MT564]",
      "state": "UNKNOWN",
      "native_value": "NO",
      "scores": {
        "YES": 0.2881,
        "NO": 0.6638,
        "UNKNOWN": 0.0481
      },
      "score": 0.6638,
      "margin": 0.3756999999999999,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "Broker service update: the institutional ballot channel is now available for this agenda.",
      "state": "UNKNOWN",
      "native_value": "NO",
      "scores": {
        "YES": 0.4571,
        "NO": 0.4996,
        "UNKNOWN": 0.0434
      },
      "score": 0.4996,
      "margin": 0.04249999999999998,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "This is solely a cash-distribution advice; it offers no meeting ballot and no shareholder vote.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.8459,
        "NO": 0.1313,
        "UNKNOWN": 0.0228
      },
      "score": 0.8459,
      "margin": 0.7146,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for a voting lock on the position applies.",
      "state": "NEGATIVE",
      "native_value": "NO",
      "scores": {
        "YES": 0.3816,
        "NO": 0.5904,
        "UNKNOWN": 0.028
      },
      "score": 0.5904,
      "margin": 0.20880000000000004,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for a compulsory attorney mandate applies.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.6467,
        "NO": 0.3146,
        "UNKNOWN": 0.0386
      },
      "score": 0.6467,
      "margin": 0.33210000000000006,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for mandatory meeting registration applies.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.6841,
        "NO": 0.2861,
        "UNKNOWN": 0.0298
      },
      "score": 0.6841,
      "margin": 0.398,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for identification of the underlying owner applies.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.8335,
        "NO": 0.1367,
        "UNKNOWN": 0.0298
      },
      "score": 0.8335,
      "margin": 0.6968000000000001,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for a custodial holding statement applies.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.7577,
        "NO": 0.2088,
        "UNKNOWN": 0.0335
      },
      "score": 0.7577,
      "margin": 0.5489,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for a requirement to cast all votes identically applies.",
      "state": "NEGATIVE",
      "native_value": "NO",
      "scores": {
        "YES": 0.4053,
        "NO": 0.5718,
        "UNKNOWN": 0.023
      },
      "score": 0.5718,
      "margin": 0.16649999999999998,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for recall of lent securities applies.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.7477,
        "NO": 0.2223,
        "UNKNOWN": 0.03
      },
      "score": 0.7477,
      "margin": 0.5254000000000001,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for an in-person-only voting condition applies.",
      "state": "NEGATIVE",
      "native_value": "NO",
      "scores": {
        "YES": 0.1685,
        "NO": 0.7973,
        "UNKNOWN": 0.0342
      },
      "score": 0.7973,
      "margin": 0.6288,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "[Message EL0206D | MT568]",
      "state": "UNKNOWN",
      "native_value": "NO",
      "scores": {
        "YES": 0.2631,
        "NO": 0.6998,
        "UNKNOWN": 0.037
      },
      "score": 0.6998,
      "margin": 0.4367,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "Please retain the replacement edition for operational reconciliation.",
      "state": "UNKNOWN",
      "native_value": "NO",
      "scores": {
        "YES": 0.2943,
        "NO": 0.6395,
        "UNKNOWN": 0.0662
      },
      "score": 0.6395,
      "margin": 0.34519999999999995,
      "historical": false,
      "supersession": true,
      "conditional": false
    },
    {
      "text": "Earlier notification conditions are superseded.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.6745,
        "NO": 0.2787,
        "UNKNOWN": 0.0468
      },
      "score": 0.6745,
      "margin": 0.3958,
      "historical": false,
      "supersession": true,
      "conditional": false
    }
  ],
  "escalation": {
    "escalated": false,
    "requested_predicates": [
      "votability",
      "share_blocking",
      "poa_required",
      "registration_required",
      "beneficial_owner_disclosure_required",
      "holding_confirmation_required",
      "split_voting_restricted",
      "securities_lending_recall_required",
      "other_voting_restriction"
    ],
    "reasons": {
      "votability": [
        "LOW_RAW_SCORE",
        "LOW_MARGIN"
      ],
      "share_blocking": [
        "LOW_RAW_SCORE"
      ],
      "poa_required": [
        "LOW_RAW_SCORE",
        "LOW_MARGIN",
        "EVIDENCE_UNAVAILABLE"
      ],
      "registration_required": [
        "LOW_RAW_SCORE"
      ],
      "beneficial_owner_disclosure_required": [
        "LOW_RAW_SCORE"
      ],
      "holding_confirmation_required": [
        "UNKNOWN",
        "LOW_RAW_SCORE",
        "LOW_MARGIN",
        "EVIDENCE_UNAVAILABLE"
      ],
      "split_voting_restricted": [
        "LOW_RAW_SCORE",
        "LOW_MARGIN"
      ],
      "securities_lending_recall_required": [
        "LOW_RAW_SCORE"
      ],
      "other_voting_restriction": [
        "UNKNOWN",
        "PASSAGE_CONFLICT",
        "LOW_RAW_SCORE",
        "LOW_MARGIN",
        "EVIDENCE_UNAVAILABLE"
      ]
    }
  },
  "conflicts": [
    "other_voting_restriction:PASSAGE_CONFLICT"
  ],
  "reconciliation_for_field": []
}
```

## VALIDATION / BASE_LAYA / 255328bb369bd44fa7cb0a788d797be6085e4bdab88a810f35f8b14469f269d2 / votability

```text
[Message EL0107C | MT564]
Issuer secretariat memorandum concerning arrangements for the forthcoming extraordinary assembly.
Participation may become possible, but the agent has not established whether this holder can vote.
For this vote, voting-related immobilisation is required.
The receiving agent has not resolved whether an obligatory power-of-attorney document is required for this vote.
No requirement for a required voter registration form applies.
No requirement for beneficial-owner disclosure applies.
For this vote, documentary confirmation of ownership is required.
No requirement for a ban on splitting voting instructions applies.
No requirement for retrieval of loaned voting positions applies.
No requirement for a mandatory paper-only ballot applies.


[Message EL0107D | MT568]
Please retain the replacement edition for operational reconciliation. Earlier notification conditions are superseded.

```

```json
{
  "truth": "UNCERTAIN",
  "prediction": {
    "value": "NOT_VOTABLE",
    "scores": {
      "VOTABLE": 0.1924,
      "NOT_VOTABLE": 0.5364,
      "UNCERTAIN": 0.2713
    },
    "native_score": 0.5364,
    "confidence": null,
    "source": "REGISTERED_LAYA_WHOLE_NOTICE",
    "evidence": [
      {
        "valid": true,
        "normalisation": "identity",
        "text": "[Message EL0107C | MT564]",
        "start": 0,
        "end": 25,
        "source": "MATCHING_NATIVE_PASSAGE"
      }
    ]
  },
  "whole_notice_scores": null,
  "passage_scores": [],
  "escalation": {
    "escalated": false,
    "requested_predicates": [
      "votability",
      "share_blocking",
      "poa_required",
      "registration_required",
      "beneficial_owner_disclosure_required",
      "holding_confirmation_required",
      "split_voting_restricted",
      "securities_lending_recall_required",
      "other_voting_restriction"
    ],
    "reasons": {
      "votability": [
        "LOW_RAW_SCORE",
        "LOW_MARGIN"
      ],
      "share_blocking": [
        "LOW_RAW_SCORE"
      ],
      "poa_required": [
        "UNKNOWN",
        "LOW_RAW_SCORE",
        "LOW_MARGIN",
        "EVIDENCE_UNAVAILABLE"
      ],
      "registration_required": [
        "LOW_RAW_SCORE"
      ],
      "beneficial_owner_disclosure_required": [
        "LOW_RAW_SCORE"
      ],
      "holding_confirmation_required": [
        "LOW_RAW_SCORE"
      ],
      "split_voting_restricted": [
        "LOW_RAW_SCORE"
      ],
      "securities_lending_recall_required": [
        "LOW_RAW_SCORE"
      ],
      "other_voting_restriction": [
        "UNKNOWN",
        "PASSAGE_CONFLICT",
        "LOW_RAW_SCORE",
        "LOW_MARGIN",
        "EVIDENCE_UNAVAILABLE"
      ]
    }
  },
  "conflicts": [
    "other_voting_restriction:PASSAGE_CONFLICT"
  ],
  "reconciliation_for_field": []
}
```

## VALIDATION / BASE_LAYA / 255328bb369bd44fa7cb0a788d797be6085e4bdab88a810f35f8b14469f269d2 / registration_required

```text
[Message EL0107C | MT564]
Issuer secretariat memorandum concerning arrangements for the forthcoming extraordinary assembly.
Participation may become possible, but the agent has not established whether this holder can vote.
For this vote, voting-related immobilisation is required.
The receiving agent has not resolved whether an obligatory power-of-attorney document is required for this vote.
No requirement for a required voter registration form applies.
No requirement for beneficial-owner disclosure applies.
For this vote, documentary confirmation of ownership is required.
No requirement for a ban on splitting voting instructions applies.
No requirement for retrieval of loaned voting positions applies.
No requirement for a mandatory paper-only ballot applies.


[Message EL0107D | MT568]
Please retain the replacement edition for operational reconciliation. Earlier notification conditions are superseded.

```

```json
{
  "truth": "NO",
  "prediction": {
    "value": "YES",
    "scores": {
      "YES": 0.9254,
      "NO": 0.037,
      "UNKNOWN": 0.0376
    },
    "native_score": 0.9254,
    "confidence": null,
    "source": "REGISTERED_LAYA_PASSAGES",
    "evidence": [
      {
        "valid": true,
        "text": "The receiving agent has not resolved whether an obligatory power-of-attorney document is required for this vote.",
        "start": 281,
        "end": 393,
        "source": "NATIVE_LAYA_PASSAGE_WITH_DETERMINISTIC_SCOPE"
      }
    ],
    "aggregation_reason": "STRONG_CURRENT_RELEVANT_EVIDENCE"
  },
  "whole_notice_scores": {
    "YES": 0.1415,
    "NO": 0.8369,
    "UNKNOWN": 0.0216
  },
  "passage_scores": [
    {
      "text": "[Message EL0107C | MT564]",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.5917,
        "NO": 0.2325,
        "UNKNOWN": 0.1758
      },
      "score": 0.5917,
      "margin": 0.35919999999999996,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "Issuer secretariat memorandum concerning arrangements for the forthcoming extraordinary assembly.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.7047,
        "NO": 0.2729,
        "UNKNOWN": 0.0224
      },
      "score": 0.7047,
      "margin": 0.4318,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "Participation may become possible, but the agent has not established whether this holder can vote.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.7314,
        "NO": 0.1968,
        "UNKNOWN": 0.0718
      },
      "score": 0.7314,
      "margin": 0.5346000000000001,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "For this vote, voting-related immobilisation is required.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.6795,
        "NO": 0.2706,
        "UNKNOWN": 0.0499
      },
      "score": 0.6795,
      "margin": 0.4089,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "The receiving agent has not resolved whether an obligatory power-of-attorney document is required for this vote.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.9254,
        "NO": 0.037,
        "UNKNOWN": 0.0376
      },
      "score": 0.9254,
      "margin": 0.8878,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for a required voter registration form applies.",
      "state": "NEGATIVE",
      "native_value": "NO",
      "scores": {
        "YES": 0.3569,
        "NO": 0.6154,
        "UNKNOWN": 0.0277
      },
      "score": 0.6154,
      "margin": 0.25849999999999995,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for beneficial-owner disclosure applies.",
      "state": "UNKNOWN",
      "native_value": "NO",
      "scores": {
        "YES": 0.4056,
        "NO": 0.567,
        "UNKNOWN": 0.0274
      },
      "score": 0.567,
      "margin": 0.16139999999999993,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "For this vote, documentary confirmation of ownership is required.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.901,
        "NO": 0.0667,
        "UNKNOWN": 0.0324
      },
      "score": 0.901,
      "margin": 0.8343,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for a ban on splitting voting instructions applies.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.8799,
        "NO": 0.1082,
        "UNKNOWN": 0.0119
      },
      "score": 0.8799,
      "margin": 0.7717,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for retrieval of loaned voting positions applies.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.68,
        "NO": 0.2672,
        "UNKNOWN": 0.0528
      },
      "score": 0.68,
      "margin": 0.41280000000000006,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for a mandatory paper-only ballot applies.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.716,
        "NO": 0.2685,
        "UNKNOWN": 0.0155
      },
      "score": 0.716,
      "margin": 0.44749999999999995,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "[Message EL0107D | MT568]",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.5079,
        "NO": 0.2792,
        "UNKNOWN": 0.2128
      },
      "score": 0.5079,
      "margin": 0.22870000000000001,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "Please retain the replacement edition for operational reconciliation.",
      "state": "UNKNOWN",
      "native_value": "NO",
      "scores": {
        "YES": 0.4564,
        "NO": 0.4659,
        "UNKNOWN": 0.0777
      },
      "score": 0.4659,
      "margin": 0.009500000000000008,
      "historical": false,
      "supersession": true,
      "conditional": false
    },
    {
      "text": "Earlier notification conditions are superseded.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.7002,
        "NO": 0.2553,
        "UNKNOWN": 0.0446
      },
      "score": 0.7002,
      "margin": 0.4449,
      "historical": false,
      "supersession": true,
      "conditional": false
    }
  ],
  "escalation": {
    "escalated": false,
    "requested_predicates": [
      "votability",
      "share_blocking",
      "poa_required",
      "registration_required",
      "beneficial_owner_disclosure_required",
      "holding_confirmation_required",
      "split_voting_restricted",
      "securities_lending_recall_required",
      "other_voting_restriction"
    ],
    "reasons": {
      "votability": [
        "LOW_RAW_SCORE",
        "LOW_MARGIN"
      ],
      "share_blocking": [
        "LOW_RAW_SCORE"
      ],
      "poa_required": [
        "UNKNOWN",
        "LOW_RAW_SCORE",
        "LOW_MARGIN",
        "EVIDENCE_UNAVAILABLE"
      ],
      "registration_required": [
        "LOW_RAW_SCORE"
      ],
      "beneficial_owner_disclosure_required": [
        "LOW_RAW_SCORE"
      ],
      "holding_confirmation_required": [
        "LOW_RAW_SCORE"
      ],
      "split_voting_restricted": [
        "LOW_RAW_SCORE"
      ],
      "securities_lending_recall_required": [
        "LOW_RAW_SCORE"
      ],
      "other_voting_restriction": [
        "UNKNOWN",
        "PASSAGE_CONFLICT",
        "LOW_RAW_SCORE",
        "LOW_MARGIN",
        "EVIDENCE_UNAVAILABLE"
      ]
    }
  },
  "conflicts": [
    "other_voting_restriction:PASSAGE_CONFLICT"
  ],
  "reconciliation_for_field": []
}
```

## VALIDATION / BASE_LAYA / 255328bb369bd44fa7cb0a788d797be6085e4bdab88a810f35f8b14469f269d2 / split_voting_restricted

```text
[Message EL0107C | MT564]
Issuer secretariat memorandum concerning arrangements for the forthcoming extraordinary assembly.
Participation may become possible, but the agent has not established whether this holder can vote.
For this vote, voting-related immobilisation is required.
The receiving agent has not resolved whether an obligatory power-of-attorney document is required for this vote.
No requirement for a required voter registration form applies.
No requirement for beneficial-owner disclosure applies.
For this vote, documentary confirmation of ownership is required.
No requirement for a ban on splitting voting instructions applies.
No requirement for retrieval of loaned voting positions applies.
No requirement for a mandatory paper-only ballot applies.


[Message EL0107D | MT568]
Please retain the replacement edition for operational reconciliation. Earlier notification conditions are superseded.

```

```json
{
  "truth": "NO",
  "prediction": {
    "value": "YES",
    "scores": {
      "YES": 0.9278,
      "NO": 0.0559,
      "UNKNOWN": 0.0163
    },
    "native_score": 0.9278,
    "confidence": null,
    "source": "REGISTERED_LAYA_PASSAGES",
    "evidence": [
      {
        "valid": true,
        "text": "No requirement for a ban on splitting voting instructions applies.",
        "start": 579,
        "end": 645,
        "source": "NATIVE_LAYA_PASSAGE_WITH_DETERMINISTIC_SCOPE"
      }
    ],
    "aggregation_reason": "STRONG_CURRENT_RELEVANT_EVIDENCE"
  },
  "whole_notice_scores": {
    "YES": 0.3089,
    "NO": 0.6656,
    "UNKNOWN": 0.0255
  },
  "passage_scores": [
    {
      "text": "[Message EL0107C | MT564]",
      "state": "UNKNOWN",
      "native_value": "NO",
      "scores": {
        "YES": 0.2137,
        "NO": 0.4505,
        "UNKNOWN": 0.3358
      },
      "score": 0.4505,
      "margin": 0.11470000000000002,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "Issuer secretariat memorandum concerning arrangements for the forthcoming extraordinary assembly.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.7796,
        "NO": 0.2023,
        "UNKNOWN": 0.0182
      },
      "score": 0.7796,
      "margin": 0.5772999999999999,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "Participation may become possible, but the agent has not established whether this holder can vote.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.4703,
        "NO": 0.3441,
        "UNKNOWN": 0.1856
      },
      "score": 0.4703,
      "margin": 0.12619999999999998,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "For this vote, voting-related immobilisation is required.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.8339,
        "NO": 0.1133,
        "UNKNOWN": 0.0528
      },
      "score": 0.8339,
      "margin": 0.7206,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "The receiving agent has not resolved whether an obligatory power-of-attorney document is required for this vote.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.8684,
        "NO": 0.0641,
        "UNKNOWN": 0.0674
      },
      "score": 0.8684,
      "margin": 0.8009999999999999,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for a required voter registration form applies.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.5237,
        "NO": 0.4315,
        "UNKNOWN": 0.0447
      },
      "score": 0.5237,
      "margin": 0.09220000000000006,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for beneficial-owner disclosure applies.",
      "state": "UNKNOWN",
      "native_value": "NO",
      "scores": {
        "YES": 0.135,
        "NO": 0.7396,
        "UNKNOWN": 0.1254
      },
      "score": 0.7396,
      "margin": 0.6046,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "For this vote, documentary confirmation of ownership is required.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.8151,
        "NO": 0.1174,
        "UNKNOWN": 0.0674
      },
      "score": 0.8151,
      "margin": 0.6977,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for a ban on splitting voting instructions applies.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.9278,
        "NO": 0.0559,
        "UNKNOWN": 0.0163
      },
      "score": 0.9278,
      "margin": 0.8719,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for retrieval of loaned voting positions applies.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.6749,
        "NO": 0.2531,
        "UNKNOWN": 0.072
      },
      "score": 0.6749,
      "margin": 0.42180000000000006,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for a mandatory paper-only ballot applies.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.5822,
        "NO": 0.3841,
        "UNKNOWN": 0.0337
      },
      "score": 0.5822,
      "margin": 0.19810000000000005,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "[Message EL0107D | MT568]",
      "state": "UNKNOWN",
      "native_value": "NO",
      "scores": {
        "YES": 0.103,
        "NO": 0.6342,
        "UNKNOWN": 0.2628
      },
      "score": 0.6342,
      "margin": 0.3714,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "Please retain the replacement edition for operational reconciliation.",
      "state": "UNKNOWN",
      "native_value": "NO",
      "scores": {
        "YES": 0.1878,
        "NO": 0.7525,
        "UNKNOWN": 0.0598
      },
      "score": 0.7525,
      "margin": 0.5647,
      "historical": false,
      "supersession": true,
      "conditional": false
    },
    {
      "text": "Earlier notification conditions are superseded.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.5756,
        "NO": 0.3457,
        "UNKNOWN": 0.0786
      },
      "score": 0.5756,
      "margin": 0.2299,
      "historical": false,
      "supersession": true,
      "conditional": false
    }
  ],
  "escalation": {
    "escalated": false,
    "requested_predicates": [
      "votability",
      "share_blocking",
      "poa_required",
      "registration_required",
      "beneficial_owner_disclosure_required",
      "holding_confirmation_required",
      "split_voting_restricted",
      "securities_lending_recall_required",
      "other_voting_restriction"
    ],
    "reasons": {
      "votability": [
        "LOW_RAW_SCORE",
        "LOW_MARGIN"
      ],
      "share_blocking": [
        "LOW_RAW_SCORE"
      ],
      "poa_required": [
        "UNKNOWN",
        "LOW_RAW_SCORE",
        "LOW_MARGIN",
        "EVIDENCE_UNAVAILABLE"
      ],
      "registration_required": [
        "LOW_RAW_SCORE"
      ],
      "beneficial_owner_disclosure_required": [
        "LOW_RAW_SCORE"
      ],
      "holding_confirmation_required": [
        "LOW_RAW_SCORE"
      ],
      "split_voting_restricted": [
        "LOW_RAW_SCORE"
      ],
      "securities_lending_recall_required": [
        "LOW_RAW_SCORE"
      ],
      "other_voting_restriction": [
        "UNKNOWN",
        "PASSAGE_CONFLICT",
        "LOW_RAW_SCORE",
        "LOW_MARGIN",
        "EVIDENCE_UNAVAILABLE"
      ]
    }
  },
  "conflicts": [
    "other_voting_restriction:PASSAGE_CONFLICT"
  ],
  "reconciliation_for_field": []
}
```

## VALIDATION / BASE_LAYA / 255328bb369bd44fa7cb0a788d797be6085e4bdab88a810f35f8b14469f269d2 / securities_lending_recall_required

```text
[Message EL0107C | MT564]
Issuer secretariat memorandum concerning arrangements for the forthcoming extraordinary assembly.
Participation may become possible, but the agent has not established whether this holder can vote.
For this vote, voting-related immobilisation is required.
The receiving agent has not resolved whether an obligatory power-of-attorney document is required for this vote.
No requirement for a required voter registration form applies.
No requirement for beneficial-owner disclosure applies.
For this vote, documentary confirmation of ownership is required.
No requirement for a ban on splitting voting instructions applies.
No requirement for retrieval of loaned voting positions applies.
No requirement for a mandatory paper-only ballot applies.


[Message EL0107D | MT568]
Please retain the replacement edition for operational reconciliation. Earlier notification conditions are superseded.

```

```json
{
  "truth": "NO",
  "prediction": {
    "value": "YES",
    "scores": {
      "YES": 0.8506,
      "NO": 0.1006,
      "UNKNOWN": 0.0489
    },
    "native_score": 0.8506,
    "confidence": null,
    "source": "REGISTERED_LAYA_PASSAGES",
    "evidence": [
      {
        "valid": true,
        "text": "For this vote, voting-related immobilisation is required.",
        "start": 223,
        "end": 280,
        "source": "NATIVE_LAYA_PASSAGE_WITH_DETERMINISTIC_SCOPE"
      }
    ],
    "aggregation_reason": "STRONG_CURRENT_RELEVANT_EVIDENCE"
  },
  "whole_notice_scores": {
    "YES": 0.238,
    "NO": 0.7335,
    "UNKNOWN": 0.0284
  },
  "passage_scores": [
    {
      "text": "[Message EL0107C | MT564]",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.6153,
        "NO": 0.261,
        "UNKNOWN": 0.1237
      },
      "score": 0.6153,
      "margin": 0.35429999999999995,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "Issuer secretariat memorandum concerning arrangements for the forthcoming extraordinary assembly.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.61,
        "NO": 0.3327,
        "UNKNOWN": 0.0574
      },
      "score": 0.61,
      "margin": 0.2773,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "Participation may become possible, but the agent has not established whether this holder can vote.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.6027,
        "NO": 0.2833,
        "UNKNOWN": 0.114
      },
      "score": 0.6027,
      "margin": 0.3194,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "For this vote, voting-related immobilisation is required.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.8506,
        "NO": 0.1006,
        "UNKNOWN": 0.0489
      },
      "score": 0.8506,
      "margin": 0.75,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "The receiving agent has not resolved whether an obligatory power-of-attorney document is required for this vote.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.8437,
        "NO": 0.096,
        "UNKNOWN": 0.0603
      },
      "score": 0.8437,
      "margin": 0.7477,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for a required voter registration form applies.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.5902,
        "NO": 0.3591,
        "UNKNOWN": 0.0506
      },
      "score": 0.5902,
      "margin": 0.23109999999999997,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for beneficial-owner disclosure applies.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.6077,
        "NO": 0.3268,
        "UNKNOWN": 0.0655
      },
      "score": 0.6077,
      "margin": 0.28090000000000004,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "For this vote, documentary confirmation of ownership is required.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.8489,
        "NO": 0.0944,
        "UNKNOWN": 0.0567
      },
      "score": 0.8489,
      "margin": 0.7545,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for a ban on splitting voting instructions applies.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.8503,
        "NO": 0.1283,
        "UNKNOWN": 0.0214
      },
      "score": 0.8503,
      "margin": 0.722,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for retrieval of loaned voting positions applies.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.6994,
        "NO": 0.2438,
        "UNKNOWN": 0.0568
      },
      "score": 0.6994,
      "margin": 0.4556,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for a mandatory paper-only ballot applies.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.8045,
        "NO": 0.1754,
        "UNKNOWN": 0.0201
      },
      "score": 0.8045,
      "margin": 0.6291,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "[Message EL0107D | MT568]",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.5852,
        "NO": 0.283,
        "UNKNOWN": 0.1318
      },
      "score": 0.5852,
      "margin": 0.3022000000000001,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "Please retain the replacement edition for operational reconciliation.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.5798,
        "NO": 0.335,
        "UNKNOWN": 0.0852
      },
      "score": 0.5798,
      "margin": 0.24479999999999996,
      "historical": false,
      "supersession": true,
      "conditional": false
    },
    {
      "text": "Earlier notification conditions are superseded.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.7353,
        "NO": 0.2046,
        "UNKNOWN": 0.0601
      },
      "score": 0.7353,
      "margin": 0.5307,
      "historical": false,
      "supersession": true,
      "conditional": false
    }
  ],
  "escalation": {
    "escalated": false,
    "requested_predicates": [
      "votability",
      "share_blocking",
      "poa_required",
      "registration_required",
      "beneficial_owner_disclosure_required",
      "holding_confirmation_required",
      "split_voting_restricted",
      "securities_lending_recall_required",
      "other_voting_restriction"
    ],
    "reasons": {
      "votability": [
        "LOW_RAW_SCORE",
        "LOW_MARGIN"
      ],
      "share_blocking": [
        "LOW_RAW_SCORE"
      ],
      "poa_required": [
        "UNKNOWN",
        "LOW_RAW_SCORE",
        "LOW_MARGIN",
        "EVIDENCE_UNAVAILABLE"
      ],
      "registration_required": [
        "LOW_RAW_SCORE"
      ],
      "beneficial_owner_disclosure_required": [
        "LOW_RAW_SCORE"
      ],
      "holding_confirmation_required": [
        "LOW_RAW_SCORE"
      ],
      "split_voting_restricted": [
        "LOW_RAW_SCORE"
      ],
      "securities_lending_recall_required": [
        "LOW_RAW_SCORE"
      ],
      "other_voting_restriction": [
        "UNKNOWN",
        "PASSAGE_CONFLICT",
        "LOW_RAW_SCORE",
        "LOW_MARGIN",
        "EVIDENCE_UNAVAILABLE"
      ]
    }
  },
  "conflicts": [
    "other_voting_restriction:PASSAGE_CONFLICT"
  ],
  "reconciliation_for_field": []
}
```

## VALIDATION / BASE_LAYA / 255328bb369bd44fa7cb0a788d797be6085e4bdab88a810f35f8b14469f269d2 / other_voting_restriction

```text
[Message EL0107C | MT564]
Issuer secretariat memorandum concerning arrangements for the forthcoming extraordinary assembly.
Participation may become possible, but the agent has not established whether this holder can vote.
For this vote, voting-related immobilisation is required.
The receiving agent has not resolved whether an obligatory power-of-attorney document is required for this vote.
No requirement for a required voter registration form applies.
No requirement for beneficial-owner disclosure applies.
For this vote, documentary confirmation of ownership is required.
No requirement for a ban on splitting voting instructions applies.
No requirement for retrieval of loaned voting positions applies.
No requirement for a mandatory paper-only ballot applies.


[Message EL0107D | MT568]
Please retain the replacement edition for operational reconciliation. Earlier notification conditions are superseded.

```

```json
{
  "truth": "NO",
  "prediction": {
    "value": "UNKNOWN",
    "scores": {},
    "native_score": null,
    "confidence": null,
    "source": "REGISTERED_LAYA_PASSAGES",
    "evidence": [],
    "aggregation_reason": "CURRENT_PASSAGE_CONFLICT_OR_DISTINCT_VOTING_ROUTES"
  },
  "whole_notice_scores": {
    "YES": 0.263,
    "NO": 0.7061,
    "UNKNOWN": 0.0308
  },
  "passage_scores": [
    {
      "text": "[Message EL0107C | MT564]",
      "state": "UNKNOWN",
      "native_value": "NO",
      "scores": {
        "YES": 0.2388,
        "NO": 0.7214,
        "UNKNOWN": 0.0399
      },
      "score": 0.7214,
      "margin": 0.48260000000000003,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "Issuer secretariat memorandum concerning arrangements for the forthcoming extraordinary assembly.",
      "state": "UNKNOWN",
      "native_value": "NO",
      "scores": {
        "YES": 0.3909,
        "NO": 0.5895,
        "UNKNOWN": 0.0196
      },
      "score": 0.5895,
      "margin": 0.1986,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "Participation may become possible, but the agent has not established whether this holder can vote.",
      "state": "UNKNOWN",
      "native_value": "NO",
      "scores": {
        "YES": 0.4147,
        "NO": 0.482,
        "UNKNOWN": 0.1034
      },
      "score": 0.482,
      "margin": 0.06729999999999997,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "For this vote, voting-related immobilisation is required.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.619,
        "NO": 0.3368,
        "UNKNOWN": 0.0442
      },
      "score": 0.619,
      "margin": 0.2822,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "The receiving agent has not resolved whether an obligatory power-of-attorney document is required for this vote.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.6464,
        "NO": 0.266,
        "UNKNOWN": 0.0876
      },
      "score": 0.6464,
      "margin": 0.38039999999999996,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for a required voter registration form applies.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.5985,
        "NO": 0.3692,
        "UNKNOWN": 0.0322
      },
      "score": 0.5985,
      "margin": 0.22930000000000006,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for beneficial-owner disclosure applies.",
      "state": "NEGATIVE",
      "native_value": "NO",
      "scores": {
        "YES": 0.1173,
        "NO": 0.8542,
        "UNKNOWN": 0.0284
      },
      "score": 0.8542,
      "margin": 0.7369,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "For this vote, documentary confirmation of ownership is required.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.8037,
        "NO": 0.1499,
        "UNKNOWN": 0.0464
      },
      "score": 0.8037,
      "margin": 0.6537999999999999,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for a ban on splitting voting instructions applies.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.7451,
        "NO": 0.2381,
        "UNKNOWN": 0.0168
      },
      "score": 0.7451,
      "margin": 0.507,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for retrieval of loaned voting positions applies.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.6373,
        "NO": 0.3377,
        "UNKNOWN": 0.025
      },
      "score": 0.6373,
      "margin": 0.2996,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for a mandatory paper-only ballot applies.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.5615,
        "NO": 0.4125,
        "UNKNOWN": 0.0259
      },
      "score": 0.5615,
      "margin": 0.14900000000000002,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "[Message EL0107D | MT568]",
      "state": "UNKNOWN",
      "native_value": "NO",
      "scores": {
        "YES": 0.2328,
        "NO": 0.7339,
        "UNKNOWN": 0.0333
      },
      "score": 0.7339,
      "margin": 0.5011,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "Please retain the replacement edition for operational reconciliation.",
      "state": "UNKNOWN",
      "native_value": "NO",
      "scores": {
        "YES": 0.2943,
        "NO": 0.6395,
        "UNKNOWN": 0.0662
      },
      "score": 0.6395,
      "margin": 0.34519999999999995,
      "historical": false,
      "supersession": true,
      "conditional": false
    },
    {
      "text": "Earlier notification conditions are superseded.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.6745,
        "NO": 0.2787,
        "UNKNOWN": 0.0468
      },
      "score": 0.6745,
      "margin": 0.3958,
      "historical": false,
      "supersession": true,
      "conditional": false
    }
  ],
  "escalation": {
    "escalated": false,
    "requested_predicates": [
      "votability",
      "share_blocking",
      "poa_required",
      "registration_required",
      "beneficial_owner_disclosure_required",
      "holding_confirmation_required",
      "split_voting_restricted",
      "securities_lending_recall_required",
      "other_voting_restriction"
    ],
    "reasons": {
      "votability": [
        "LOW_RAW_SCORE",
        "LOW_MARGIN"
      ],
      "share_blocking": [
        "LOW_RAW_SCORE"
      ],
      "poa_required": [
        "UNKNOWN",
        "LOW_RAW_SCORE",
        "LOW_MARGIN",
        "EVIDENCE_UNAVAILABLE"
      ],
      "registration_required": [
        "LOW_RAW_SCORE"
      ],
      "beneficial_owner_disclosure_required": [
        "LOW_RAW_SCORE"
      ],
      "holding_confirmation_required": [
        "LOW_RAW_SCORE"
      ],
      "split_voting_restricted": [
        "LOW_RAW_SCORE"
      ],
      "securities_lending_recall_required": [
        "LOW_RAW_SCORE"
      ],
      "other_voting_restriction": [
        "UNKNOWN",
        "PASSAGE_CONFLICT",
        "LOW_RAW_SCORE",
        "LOW_MARGIN",
        "EVIDENCE_UNAVAILABLE"
      ]
    }
  },
  "conflicts": [
    "other_voting_restriction:PASSAGE_CONFLICT"
  ],
  "reconciliation_for_field": []
}
```

## VALIDATION / BASE_LAYA / 25150120b9a9e92a98ab8b33fb003cab98a2ec6b4230ec908fda5c15d2bbc7d7 / share_blocking

```text
[Message EL0105C | MT564]
Issuer secretariat memorandum concerning arrangements for the forthcoming extraordinary assembly.
The current agenda is open for shareholder voting instructions.
No requirement for voting-related immobilisation applies.
No requirement for an obligatory power-of-attorney document applies.
For this vote, a required voter registration form is required.
No requirement for beneficial-owner disclosure applies.
No requirement for documentary confirmation of ownership applies.
No requirement for a ban on splitting voting instructions applies.
For this vote, retrieval of loaned voting positions is required.
No requirement for a mandatory paper-only ballot applies.


[Message EL0105D | MT568]
Please retain the replacement edition for operational reconciliation. Earlier notification conditions are superseded.

```

```json
{
  "truth": "NO",
  "prediction": {
    "value": "YES",
    "scores": {
      "YES": 0.9813,
      "NO": 0.006,
      "UNKNOWN": 0.0127
    },
    "native_score": 0.9813,
    "confidence": null,
    "source": "REGISTERED_LAYA_PASSAGES",
    "evidence": [
      {
        "valid": true,
        "text": "Earlier notification conditions are superseded.",
        "start": 788,
        "end": 835,
        "source": "NATIVE_LAYA_PASSAGE_WITH_DETERMINISTIC_SCOPE"
      }
    ],
    "aggregation_reason": "STRONG_CURRENT_RELEVANT_EVIDENCE"
  },
  "whole_notice_scores": {
    "YES": 0.6645,
    "NO": 0.2454,
    "UNKNOWN": 0.0901
  },
  "passage_scores": [
    {
      "text": "[Message EL0105C | MT564]",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.9666,
        "NO": 0.0137,
        "UNKNOWN": 0.0197
      },
      "score": 0.9666,
      "margin": 0.9469,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "Issuer secretariat memorandum concerning arrangements for the forthcoming extraordinary assembly.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.9452,
        "NO": 0.0408,
        "UNKNOWN": 0.0141
      },
      "score": 0.9452,
      "margin": 0.9044000000000001,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "The current agenda is open for shareholder voting instructions.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.8826,
        "NO": 0.0712,
        "UNKNOWN": 0.0462
      },
      "score": 0.8826,
      "margin": 0.8114,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for voting-related immobilisation applies.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.9708,
        "NO": 0.0219,
        "UNKNOWN": 0.0072
      },
      "score": 0.9708,
      "margin": 0.9489,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for an obligatory power-of-attorney document applies.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.9399,
        "NO": 0.0382,
        "UNKNOWN": 0.0219
      },
      "score": 0.9399,
      "margin": 0.9017,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "For this vote, a required voter registration form is required.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.9662,
        "NO": 0.0133,
        "UNKNOWN": 0.0205
      },
      "score": 0.9662,
      "margin": 0.9457,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for beneficial-owner disclosure applies.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.9354,
        "NO": 0.0392,
        "UNKNOWN": 0.0254
      },
      "score": 0.9354,
      "margin": 0.8962,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for documentary confirmation of ownership applies.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.9633,
        "NO": 0.0238,
        "UNKNOWN": 0.0129
      },
      "score": 0.9633,
      "margin": 0.9395,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for a ban on splitting voting instructions applies.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.9785,
        "NO": 0.0108,
        "UNKNOWN": 0.0107
      },
      "score": 0.9785,
      "margin": 0.9677,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "For this vote, retrieval of loaned voting positions is required.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.9306,
        "NO": 0.0307,
        "UNKNOWN": 0.0387
      },
      "score": 0.9306,
      "margin": 0.8919,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for a mandatory paper-only ballot applies.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.9294,
        "NO": 0.0456,
        "UNKNOWN": 0.0251
      },
      "score": 0.9294,
      "margin": 0.8838,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "[Message EL0105D | MT568]",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.9674,
        "NO": 0.0142,
        "UNKNOWN": 0.0185
      },
      "score": 0.9674,
      "margin": 0.9489000000000001,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "Please retain the replacement edition for operational reconciliation.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.9526,
        "NO": 0.0272,
        "UNKNOWN": 0.0201
      },
      "score": 0.9526,
      "margin": 0.9254,
      "historical": false,
      "supersession": true,
      "conditional": false
    },
    {
      "text": "Earlier notification conditions are superseded.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.9813,
        "NO": 0.006,
        "UNKNOWN": 0.0127
      },
      "score": 0.9813,
      "margin": 0.9685999999999999,
      "historical": false,
      "supersession": true,
      "conditional": false
    }
  ],
  "escalation": {
    "escalated": false,
    "requested_predicates": [
      "share_blocking",
      "poa_required",
      "registration_required",
      "beneficial_owner_disclosure_required",
      "holding_confirmation_required",
      "split_voting_restricted",
      "securities_lending_recall_required",
      "other_voting_restriction"
    ],
    "reasons": {
      "share_blocking": [
        "LOW_RAW_SCORE"
      ],
      "poa_required": [
        "LOW_RAW_SCORE"
      ],
      "registration_required": [
        "LOW_RAW_SCORE"
      ],
      "beneficial_owner_disclosure_required": [
        "LOW_RAW_SCORE"
      ],
      "holding_confirmation_required": [
        "LOW_RAW_SCORE"
      ],
      "split_voting_restricted": [
        "LOW_RAW_SCORE"
      ],
      "securities_lending_recall_required": [
        "LOW_RAW_SCORE"
      ],
      "other_voting_restriction": [
        "UNKNOWN",
        "PASSAGE_CONFLICT",
        "LOW_RAW_SCORE",
        "LOW_MARGIN",
        "EVIDENCE_UNAVAILABLE"
      ]
    }
  },
  "conflicts": [
    "other_voting_restriction:PASSAGE_CONFLICT",
    "votability:STRUCTURE_SEMANTIC_CONFLICT"
  ],
  "reconciliation_for_field": []
}
```

## VALIDATION / BASE_LAYA / 25150120b9a9e92a98ab8b33fb003cab98a2ec6b4230ec908fda5c15d2bbc7d7 / split_voting_restricted

```text
[Message EL0105C | MT564]
Issuer secretariat memorandum concerning arrangements for the forthcoming extraordinary assembly.
The current agenda is open for shareholder voting instructions.
No requirement for voting-related immobilisation applies.
No requirement for an obligatory power-of-attorney document applies.
For this vote, a required voter registration form is required.
No requirement for beneficial-owner disclosure applies.
No requirement for documentary confirmation of ownership applies.
No requirement for a ban on splitting voting instructions applies.
For this vote, retrieval of loaned voting positions is required.
No requirement for a mandatory paper-only ballot applies.


[Message EL0105D | MT568]
Please retain the replacement edition for operational reconciliation. Earlier notification conditions are superseded.

```

```json
{
  "truth": "NO",
  "prediction": {
    "value": "YES",
    "scores": {
      "YES": 0.9278,
      "NO": 0.0559,
      "UNKNOWN": 0.0163
    },
    "native_score": 0.9278,
    "confidence": null,
    "source": "REGISTERED_LAYA_PASSAGES",
    "evidence": [
      {
        "valid": true,
        "text": "No requirement for a ban on splitting voting instructions applies.",
        "start": 500,
        "end": 566,
        "source": "NATIVE_LAYA_PASSAGE_WITH_DETERMINISTIC_SCOPE"
      }
    ],
    "aggregation_reason": "STRONG_CURRENT_RELEVANT_EVIDENCE"
  },
  "whole_notice_scores": {
    "YES": 0.4644,
    "NO": 0.4786,
    "UNKNOWN": 0.057
  },
  "passage_scores": [
    {
      "text": "[Message EL0105C | MT564]",
      "state": "UNKNOWN",
      "native_value": "NO",
      "scores": {
        "YES": 0.2024,
        "NO": 0.4907,
        "UNKNOWN": 0.3069
      },
      "score": 0.4907,
      "margin": 0.18380000000000002,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "Issuer secretariat memorandum concerning arrangements for the forthcoming extraordinary assembly.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.7796,
        "NO": 0.2023,
        "UNKNOWN": 0.0182
      },
      "score": 0.7796,
      "margin": 0.5772999999999999,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "The current agenda is open for shareholder voting instructions.",
      "state": "UNKNOWN",
      "native_value": "NO",
      "scores": {
        "YES": 0.2095,
        "NO": 0.6811,
        "UNKNOWN": 0.1095
      },
      "score": 0.6811,
      "margin": 0.4716,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for voting-related immobilisation applies.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.6013,
        "NO": 0.3281,
        "UNKNOWN": 0.0706
      },
      "score": 0.6013,
      "margin": 0.27319999999999994,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for an obligatory power-of-attorney document applies.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.6998,
        "NO": 0.249,
        "UNKNOWN": 0.0511
      },
      "score": 0.6998,
      "margin": 0.4508,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "For this vote, a required voter registration form is required.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.8884,
        "NO": 0.0693,
        "UNKNOWN": 0.0423
      },
      "score": 0.8884,
      "margin": 0.8190999999999999,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for beneficial-owner disclosure applies.",
      "state": "UNKNOWN",
      "native_value": "NO",
      "scores": {
        "YES": 0.135,
        "NO": 0.7396,
        "UNKNOWN": 0.1254
      },
      "score": 0.7396,
      "margin": 0.6046,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for documentary confirmation of ownership applies.",
      "state": "UNKNOWN",
      "native_value": "NO",
      "scores": {
        "YES": 0.3997,
        "NO": 0.5398,
        "UNKNOWN": 0.0605
      },
      "score": 0.5398,
      "margin": 0.14009999999999995,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for a ban on splitting voting instructions applies.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.9278,
        "NO": 0.0559,
        "UNKNOWN": 0.0163
      },
      "score": 0.9278,
      "margin": 0.8719,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "For this vote, retrieval of loaned voting positions is required.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.769,
        "NO": 0.1588,
        "UNKNOWN": 0.0723
      },
      "score": 0.769,
      "margin": 0.6102000000000001,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for a mandatory paper-only ballot applies.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.5822,
        "NO": 0.3841,
        "UNKNOWN": 0.0337
      },
      "score": 0.5822,
      "margin": 0.19810000000000005,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "[Message EL0105D | MT568]",
      "state": "UNKNOWN",
      "native_value": "NO",
      "scores": {
        "YES": 0.1502,
        "NO": 0.577,
        "UNKNOWN": 0.2728
      },
      "score": 0.577,
      "margin": 0.30419999999999997,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "Please retain the replacement edition for operational reconciliation.",
      "state": "UNKNOWN",
      "native_value": "NO",
      "scores": {
        "YES": 0.1878,
        "NO": 0.7525,
        "UNKNOWN": 0.0598
      },
      "score": 0.7525,
      "margin": 0.5647,
      "historical": false,
      "supersession": true,
      "conditional": false
    },
    {
      "text": "Earlier notification conditions are superseded.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.5756,
        "NO": 0.3457,
        "UNKNOWN": 0.0786
      },
      "score": 0.5756,
      "margin": 0.2299,
      "historical": false,
      "supersession": true,
      "conditional": false
    }
  ],
  "escalation": {
    "escalated": false,
    "requested_predicates": [
      "share_blocking",
      "poa_required",
      "registration_required",
      "beneficial_owner_disclosure_required",
      "holding_confirmation_required",
      "split_voting_restricted",
      "securities_lending_recall_required",
      "other_voting_restriction"
    ],
    "reasons": {
      "share_blocking": [
        "LOW_RAW_SCORE"
      ],
      "poa_required": [
        "LOW_RAW_SCORE"
      ],
      "registration_required": [
        "LOW_RAW_SCORE"
      ],
      "beneficial_owner_disclosure_required": [
        "LOW_RAW_SCORE"
      ],
      "holding_confirmation_required": [
        "LOW_RAW_SCORE"
      ],
      "split_voting_restricted": [
        "LOW_RAW_SCORE"
      ],
      "securities_lending_recall_required": [
        "LOW_RAW_SCORE"
      ],
      "other_voting_restriction": [
        "UNKNOWN",
        "PASSAGE_CONFLICT",
        "LOW_RAW_SCORE",
        "LOW_MARGIN",
        "EVIDENCE_UNAVAILABLE"
      ]
    }
  },
  "conflicts": [
    "other_voting_restriction:PASSAGE_CONFLICT",
    "votability:STRUCTURE_SEMANTIC_CONFLICT"
  ],
  "reconciliation_for_field": []
}
```

## VALIDATION / BASE_LAYA / 25150120b9a9e92a98ab8b33fb003cab98a2ec6b4230ec908fda5c15d2bbc7d7 / other_voting_restriction

```text
[Message EL0105C | MT564]
Issuer secretariat memorandum concerning arrangements for the forthcoming extraordinary assembly.
The current agenda is open for shareholder voting instructions.
No requirement for voting-related immobilisation applies.
No requirement for an obligatory power-of-attorney document applies.
For this vote, a required voter registration form is required.
No requirement for beneficial-owner disclosure applies.
No requirement for documentary confirmation of ownership applies.
No requirement for a ban on splitting voting instructions applies.
For this vote, retrieval of loaned voting positions is required.
No requirement for a mandatory paper-only ballot applies.


[Message EL0105D | MT568]
Please retain the replacement edition for operational reconciliation. Earlier notification conditions are superseded.

```

```json
{
  "truth": "NO",
  "prediction": {
    "value": "UNKNOWN",
    "scores": {},
    "native_score": null,
    "confidence": null,
    "source": "REGISTERED_LAYA_PASSAGES",
    "evidence": [],
    "aggregation_reason": "CURRENT_PASSAGE_CONFLICT_OR_DISTINCT_VOTING_ROUTES"
  },
  "whole_notice_scores": {
    "YES": 0.3276,
    "NO": 0.5702,
    "UNKNOWN": 0.1023
  },
  "passage_scores": [
    {
      "text": "[Message EL0105C | MT564]",
      "state": "UNKNOWN",
      "native_value": "NO",
      "scores": {
        "YES": 0.1955,
        "NO": 0.7749,
        "UNKNOWN": 0.0296
      },
      "score": 0.7749,
      "margin": 0.5794,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "Issuer secretariat memorandum concerning arrangements for the forthcoming extraordinary assembly.",
      "state": "UNKNOWN",
      "native_value": "NO",
      "scores": {
        "YES": 0.3909,
        "NO": 0.5895,
        "UNKNOWN": 0.0196
      },
      "score": 0.5895,
      "margin": 0.1986,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "The current agenda is open for shareholder voting instructions.",
      "state": "UNKNOWN",
      "native_value": "NO",
      "scores": {
        "YES": 0.2613,
        "NO": 0.6802,
        "UNKNOWN": 0.0585
      },
      "score": 0.6802,
      "margin": 0.41890000000000005,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for voting-related immobilisation applies.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.5303,
        "NO": 0.4382,
        "UNKNOWN": 0.0315
      },
      "score": 0.5303,
      "margin": 0.09210000000000002,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for an obligatory power-of-attorney document applies.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.5774,
        "NO": 0.3804,
        "UNKNOWN": 0.0422
      },
      "score": 0.5774,
      "margin": 0.197,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "For this vote, a required voter registration form is required.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.746,
        "NO": 0.1881,
        "UNKNOWN": 0.0658
      },
      "score": 0.746,
      "margin": 0.5579000000000001,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for beneficial-owner disclosure applies.",
      "state": "NEGATIVE",
      "native_value": "NO",
      "scores": {
        "YES": 0.1173,
        "NO": 0.8542,
        "UNKNOWN": 0.0284
      },
      "score": 0.8542,
      "margin": 0.7369,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for documentary confirmation of ownership applies.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.7244,
        "NO": 0.2371,
        "UNKNOWN": 0.0385
      },
      "score": 0.7244,
      "margin": 0.48730000000000007,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for a ban on splitting voting instructions applies.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.7451,
        "NO": 0.2381,
        "UNKNOWN": 0.0168
      },
      "score": 0.7451,
      "margin": 0.507,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "For this vote, retrieval of loaned voting positions is required.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.6306,
        "NO": 0.3274,
        "UNKNOWN": 0.042
      },
      "score": 0.6306,
      "margin": 0.3032,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for a mandatory paper-only ballot applies.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.5615,
        "NO": 0.4125,
        "UNKNOWN": 0.0259
      },
      "score": 0.5615,
      "margin": 0.14900000000000002,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "[Message EL0105D | MT568]",
      "state": "UNKNOWN",
      "native_value": "NO",
      "scores": {
        "YES": 0.2593,
        "NO": 0.7068,
        "UNKNOWN": 0.0339
      },
      "score": 0.7068,
      "margin": 0.4475,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "Please retain the replacement edition for operational reconciliation.",
      "state": "UNKNOWN",
      "native_value": "NO",
      "scores": {
        "YES": 0.2943,
        "NO": 0.6395,
        "UNKNOWN": 0.0662
      },
      "score": 0.6395,
      "margin": 0.34519999999999995,
      "historical": false,
      "supersession": true,
      "conditional": false
    },
    {
      "text": "Earlier notification conditions are superseded.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.6745,
        "NO": 0.2787,
        "UNKNOWN": 0.0468
      },
      "score": 0.6745,
      "margin": 0.3958,
      "historical": false,
      "supersession": true,
      "conditional": false
    }
  ],
  "escalation": {
    "escalated": false,
    "requested_predicates": [
      "share_blocking",
      "poa_required",
      "registration_required",
      "beneficial_owner_disclosure_required",
      "holding_confirmation_required",
      "split_voting_restricted",
      "securities_lending_recall_required",
      "other_voting_restriction"
    ],
    "reasons": {
      "share_blocking": [
        "LOW_RAW_SCORE"
      ],
      "poa_required": [
        "LOW_RAW_SCORE"
      ],
      "registration_required": [
        "LOW_RAW_SCORE"
      ],
      "beneficial_owner_disclosure_required": [
        "LOW_RAW_SCORE"
      ],
      "holding_confirmation_required": [
        "LOW_RAW_SCORE"
      ],
      "split_voting_restricted": [
        "LOW_RAW_SCORE"
      ],
      "securities_lending_recall_required": [
        "LOW_RAW_SCORE"
      ],
      "other_voting_restriction": [
        "UNKNOWN",
        "PASSAGE_CONFLICT",
        "LOW_RAW_SCORE",
        "LOW_MARGIN",
        "EVIDENCE_UNAVAILABLE"
      ]
    }
  },
  "conflicts": [
    "other_voting_restriction:PASSAGE_CONFLICT",
    "votability:STRUCTURE_SEMANTIC_CONFLICT"
  ],
  "reconciliation_for_field": []
}
```

## VALIDATION / BASE_LAYA / 2414be60f4dff3cc46dcf385c748749f7c7c3dc05ef8f904052ec9797bdc2f19 / share_blocking

```text
[Message EL0104C | MT564]
Issuer secretariat memorandum concerning arrangements for the forthcoming extraordinary assembly.
The current agenda is open for shareholder voting instructions.
No requirement for voting-related immobilisation applies.
No requirement for an obligatory power-of-attorney document applies.
No requirement for a required voter registration form applies.
For this vote, beneficial-owner disclosure is required.
No requirement for documentary confirmation of ownership applies.
No requirement for a ban on splitting voting instructions applies.
No requirement for retrieval of loaned voting positions applies.
For this vote, a mandatory paper-only ballot is required.


[Message EL0104D | MT568]
Please retain the replacement edition for operational reconciliation. Earlier notification conditions are superseded.

```

```json
{
  "truth": "NO",
  "prediction": {
    "value": "YES",
    "scores": {
      "YES": 0.9813,
      "NO": 0.006,
      "UNKNOWN": 0.0127
    },
    "native_score": 0.9813,
    "confidence": null,
    "source": "REGISTERED_LAYA_PASSAGES",
    "evidence": [
      {
        "valid": true,
        "text": "Earlier notification conditions are superseded.",
        "start": 788,
        "end": 835,
        "source": "NATIVE_LAYA_PASSAGE_WITH_DETERMINISTIC_SCOPE"
      }
    ],
    "aggregation_reason": "STRONG_CURRENT_RELEVANT_EVIDENCE"
  },
  "whole_notice_scores": {
    "YES": 0.7381,
    "NO": 0.2015,
    "UNKNOWN": 0.0604
  },
  "passage_scores": [
    {
      "text": "[Message EL0104C | MT564]",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.966,
        "NO": 0.0134,
        "UNKNOWN": 0.0206
      },
      "score": 0.966,
      "margin": 0.9454,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "Issuer secretariat memorandum concerning arrangements for the forthcoming extraordinary assembly.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.9452,
        "NO": 0.0408,
        "UNKNOWN": 0.0141
      },
      "score": 0.9452,
      "margin": 0.9044000000000001,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "The current agenda is open for shareholder voting instructions.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.8826,
        "NO": 0.0712,
        "UNKNOWN": 0.0462
      },
      "score": 0.8826,
      "margin": 0.8114,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for voting-related immobilisation applies.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.9708,
        "NO": 0.0219,
        "UNKNOWN": 0.0072
      },
      "score": 0.9708,
      "margin": 0.9489,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for an obligatory power-of-attorney document applies.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.9399,
        "NO": 0.0382,
        "UNKNOWN": 0.0219
      },
      "score": 0.9399,
      "margin": 0.9017,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for a required voter registration form applies.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.8735,
        "NO": 0.0909,
        "UNKNOWN": 0.0356
      },
      "score": 0.8735,
      "margin": 0.7826000000000001,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "For this vote, beneficial-owner disclosure is required.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.9353,
        "NO": 0.0373,
        "UNKNOWN": 0.0273
      },
      "score": 0.9353,
      "margin": 0.898,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for documentary confirmation of ownership applies.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.9633,
        "NO": 0.0238,
        "UNKNOWN": 0.0129
      },
      "score": 0.9633,
      "margin": 0.9395,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for a ban on splitting voting instructions applies.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.9785,
        "NO": 0.0108,
        "UNKNOWN": 0.0107
      },
      "score": 0.9785,
      "margin": 0.9677,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for retrieval of loaned voting positions applies.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.9032,
        "NO": 0.0694,
        "UNKNOWN": 0.0274
      },
      "score": 0.9032,
      "margin": 0.8338,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "For this vote, a mandatory paper-only ballot is required.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.9736,
        "NO": 0.0124,
        "UNKNOWN": 0.014
      },
      "score": 0.9736,
      "margin": 0.9596,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "[Message EL0104D | MT568]",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.968,
        "NO": 0.0131,
        "UNKNOWN": 0.019
      },
      "score": 0.968,
      "margin": 0.949,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "Please retain the replacement edition for operational reconciliation.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.9526,
        "NO": 0.0272,
        "UNKNOWN": 0.0201
      },
      "score": 0.9526,
      "margin": 0.9254,
      "historical": false,
      "supersession": true,
      "conditional": false
    },
    {
      "text": "Earlier notification conditions are superseded.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.9813,
        "NO": 0.006,
        "UNKNOWN": 0.0127
      },
      "score": 0.9813,
      "margin": 0.9685999999999999,
      "historical": false,
      "supersession": true,
      "conditional": false
    }
  ],
  "escalation": {
    "escalated": false,
    "requested_predicates": [
      "share_blocking",
      "poa_required",
      "registration_required",
      "beneficial_owner_disclosure_required",
      "holding_confirmation_required",
      "split_voting_restricted",
      "securities_lending_recall_required",
      "other_voting_restriction"
    ],
    "reasons": {
      "share_blocking": [
        "LOW_RAW_SCORE"
      ],
      "poa_required": [
        "LOW_RAW_SCORE"
      ],
      "registration_required": [
        "LOW_RAW_SCORE"
      ],
      "beneficial_owner_disclosure_required": [
        "LOW_RAW_SCORE"
      ],
      "holding_confirmation_required": [
        "LOW_RAW_SCORE"
      ],
      "split_voting_restricted": [
        "LOW_RAW_SCORE"
      ],
      "securities_lending_recall_required": [
        "LOW_RAW_SCORE"
      ],
      "other_voting_restriction": [
        "LOW_RAW_SCORE"
      ]
    }
  },
  "conflicts": [
    "votability:STRUCTURE_SEMANTIC_CONFLICT"
  ],
  "reconciliation_for_field": []
}
```

## VALIDATION / BASE_LAYA / 2414be60f4dff3cc46dcf385c748749f7c7c3dc05ef8f904052ec9797bdc2f19 / registration_required

```text
[Message EL0104C | MT564]
Issuer secretariat memorandum concerning arrangements for the forthcoming extraordinary assembly.
The current agenda is open for shareholder voting instructions.
No requirement for voting-related immobilisation applies.
No requirement for an obligatory power-of-attorney document applies.
No requirement for a required voter registration form applies.
For this vote, beneficial-owner disclosure is required.
No requirement for documentary confirmation of ownership applies.
No requirement for a ban on splitting voting instructions applies.
No requirement for retrieval of loaned voting positions applies.
For this vote, a mandatory paper-only ballot is required.


[Message EL0104D | MT568]
Please retain the replacement edition for operational reconciliation. Earlier notification conditions are superseded.

```

```json
{
  "truth": "NO",
  "prediction": {
    "value": "YES",
    "scores": {
      "YES": 0.9309,
      "NO": 0.0578,
      "UNKNOWN": 0.0113
    },
    "native_score": 0.9309,
    "confidence": null,
    "source": "REGISTERED_LAYA_PASSAGES",
    "evidence": [
      {
        "valid": true,
        "text": "For this vote, a mandatory paper-only ballot is required.",
        "start": 632,
        "end": 689,
        "source": "NATIVE_LAYA_PASSAGE_WITH_DETERMINISTIC_SCOPE"
      }
    ],
    "aggregation_reason": "STRONG_CURRENT_RELEVANT_EVIDENCE"
  },
  "whole_notice_scores": {
    "YES": 0.2163,
    "NO": 0.6902,
    "UNKNOWN": 0.0936
  },
  "passage_scores": [
    {
      "text": "[Message EL0104C | MT564]",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.6235,
        "NO": 0.2066,
        "UNKNOWN": 0.1699
      },
      "score": 0.6235,
      "margin": 0.41690000000000005,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "Issuer secretariat memorandum concerning arrangements for the forthcoming extraordinary assembly.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.7047,
        "NO": 0.2729,
        "UNKNOWN": 0.0224
      },
      "score": 0.7047,
      "margin": 0.4318,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "The current agenda is open for shareholder voting instructions.",
      "state": "UNKNOWN",
      "native_value": "NO",
      "scores": {
        "YES": 0.1846,
        "NO": 0.7334,
        "UNKNOWN": 0.0819
      },
      "score": 0.7334,
      "margin": 0.5488000000000001,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for voting-related immobilisation applies.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.8715,
        "NO": 0.1084,
        "UNKNOWN": 0.0201
      },
      "score": 0.8715,
      "margin": 0.7631000000000001,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for an obligatory power-of-attorney document applies.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.8488,
        "NO": 0.1345,
        "UNKNOWN": 0.0167
      },
      "score": 0.8488,
      "margin": 0.7142999999999999,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for a required voter registration form applies.",
      "state": "NEGATIVE",
      "native_value": "NO",
      "scores": {
        "YES": 0.3569,
        "NO": 0.6154,
        "UNKNOWN": 0.0277
      },
      "score": 0.6154,
      "margin": 0.25849999999999995,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "For this vote, beneficial-owner disclosure is required.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.6203,
        "NO": 0.3248,
        "UNKNOWN": 0.0548
      },
      "score": 0.6203,
      "margin": 0.2955,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for documentary confirmation of ownership applies.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.6705,
        "NO": 0.3057,
        "UNKNOWN": 0.0238
      },
      "score": 0.6705,
      "margin": 0.36479999999999996,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for a ban on splitting voting instructions applies.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.8799,
        "NO": 0.1082,
        "UNKNOWN": 0.0119
      },
      "score": 0.8799,
      "margin": 0.7717,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for retrieval of loaned voting positions applies.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.68,
        "NO": 0.2672,
        "UNKNOWN": 0.0528
      },
      "score": 0.68,
      "margin": 0.41280000000000006,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "For this vote, a mandatory paper-only ballot is required.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.9309,
        "NO": 0.0578,
        "UNKNOWN": 0.0113
      },
      "score": 0.9309,
      "margin": 0.8731,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "[Message EL0104D | MT568]",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.5695,
        "NO": 0.2224,
        "UNKNOWN": 0.2081
      },
      "score": 0.5695,
      "margin": 0.3471,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "Please retain the replacement edition for operational reconciliation.",
      "state": "UNKNOWN",
      "native_value": "NO",
      "scores": {
        "YES": 0.4564,
        "NO": 0.4659,
        "UNKNOWN": 0.0777
      },
      "score": 0.4659,
      "margin": 0.009500000000000008,
      "historical": false,
      "supersession": true,
      "conditional": false
    },
    {
      "text": "Earlier notification conditions are superseded.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.7002,
        "NO": 0.2553,
        "UNKNOWN": 0.0446
      },
      "score": 0.7002,
      "margin": 0.4449,
      "historical": false,
      "supersession": true,
      "conditional": false
    }
  ],
  "escalation": {
    "escalated": false,
    "requested_predicates": [
      "share_blocking",
      "poa_required",
      "registration_required",
      "beneficial_owner_disclosure_required",
      "holding_confirmation_required",
      "split_voting_restricted",
      "securities_lending_recall_required",
      "other_voting_restriction"
    ],
    "reasons": {
      "share_blocking": [
        "LOW_RAW_SCORE"
      ],
      "poa_required": [
        "LOW_RAW_SCORE"
      ],
      "registration_required": [
        "LOW_RAW_SCORE"
      ],
      "beneficial_owner_disclosure_required": [
        "LOW_RAW_SCORE"
      ],
      "holding_confirmation_required": [
        "LOW_RAW_SCORE"
      ],
      "split_voting_restricted": [
        "LOW_RAW_SCORE"
      ],
      "securities_lending_recall_required": [
        "LOW_RAW_SCORE"
      ],
      "other_voting_restriction": [
        "LOW_RAW_SCORE"
      ]
    }
  },
  "conflicts": [
    "votability:STRUCTURE_SEMANTIC_CONFLICT"
  ],
  "reconciliation_for_field": []
}
```

## VALIDATION / BASE_LAYA / 2414be60f4dff3cc46dcf385c748749f7c7c3dc05ef8f904052ec9797bdc2f19 / split_voting_restricted

```text
[Message EL0104C | MT564]
Issuer secretariat memorandum concerning arrangements for the forthcoming extraordinary assembly.
The current agenda is open for shareholder voting instructions.
No requirement for voting-related immobilisation applies.
No requirement for an obligatory power-of-attorney document applies.
No requirement for a required voter registration form applies.
For this vote, beneficial-owner disclosure is required.
No requirement for documentary confirmation of ownership applies.
No requirement for a ban on splitting voting instructions applies.
No requirement for retrieval of loaned voting positions applies.
For this vote, a mandatory paper-only ballot is required.


[Message EL0104D | MT568]
Please retain the replacement edition for operational reconciliation. Earlier notification conditions are superseded.

```

```json
{
  "truth": "NO",
  "prediction": {
    "value": "YES",
    "scores": {
      "YES": 0.9278,
      "NO": 0.0559,
      "UNKNOWN": 0.0163
    },
    "native_score": 0.9278,
    "confidence": null,
    "source": "REGISTERED_LAYA_PASSAGES",
    "evidence": [
      {
        "valid": true,
        "text": "No requirement for a ban on splitting voting instructions applies.",
        "start": 500,
        "end": 566,
        "source": "NATIVE_LAYA_PASSAGE_WITH_DETERMINISTIC_SCOPE"
      }
    ],
    "aggregation_reason": "STRONG_CURRENT_RELEVANT_EVIDENCE"
  },
  "whole_notice_scores": {
    "YES": 0.4837,
    "NO": 0.4681,
    "UNKNOWN": 0.0483
  },
  "passage_scores": [
    {
      "text": "[Message EL0104C | MT564]",
      "state": "UNKNOWN",
      "native_value": "NO",
      "scores": {
        "YES": 0.2504,
        "NO": 0.4247,
        "UNKNOWN": 0.3248
      },
      "score": 0.4247,
      "margin": 0.09990000000000004,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "Issuer secretariat memorandum concerning arrangements for the forthcoming extraordinary assembly.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.7796,
        "NO": 0.2023,
        "UNKNOWN": 0.0182
      },
      "score": 0.7796,
      "margin": 0.5772999999999999,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "The current agenda is open for shareholder voting instructions.",
      "state": "UNKNOWN",
      "native_value": "NO",
      "scores": {
        "YES": 0.2095,
        "NO": 0.6811,
        "UNKNOWN": 0.1095
      },
      "score": 0.6811,
      "margin": 0.4716,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for voting-related immobilisation applies.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.6013,
        "NO": 0.3281,
        "UNKNOWN": 0.0706
      },
      "score": 0.6013,
      "margin": 0.27319999999999994,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for an obligatory power-of-attorney document applies.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.6998,
        "NO": 0.249,
        "UNKNOWN": 0.0511
      },
      "score": 0.6998,
      "margin": 0.4508,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for a required voter registration form applies.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.5237,
        "NO": 0.4315,
        "UNKNOWN": 0.0447
      },
      "score": 0.5237,
      "margin": 0.09220000000000006,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "For this vote, beneficial-owner disclosure is required.",
      "state": "UNKNOWN",
      "native_value": "NO",
      "scores": {
        "YES": 0.4312,
        "NO": 0.5082,
        "UNKNOWN": 0.0606
      },
      "score": 0.5082,
      "margin": 0.07699999999999996,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for documentary confirmation of ownership applies.",
      "state": "UNKNOWN",
      "native_value": "NO",
      "scores": {
        "YES": 0.3997,
        "NO": 0.5398,
        "UNKNOWN": 0.0605
      },
      "score": 0.5398,
      "margin": 0.14009999999999995,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for a ban on splitting voting instructions applies.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.9278,
        "NO": 0.0559,
        "UNKNOWN": 0.0163
      },
      "score": 0.9278,
      "margin": 0.8719,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for retrieval of loaned voting positions applies.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.6749,
        "NO": 0.2531,
        "UNKNOWN": 0.072
      },
      "score": 0.6749,
      "margin": 0.42180000000000006,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "For this vote, a mandatory paper-only ballot is required.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.8995,
        "NO": 0.0682,
        "UNKNOWN": 0.0323
      },
      "score": 0.8995,
      "margin": 0.8312999999999999,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "[Message EL0104D | MT568]",
      "state": "UNKNOWN",
      "native_value": "NO",
      "scores": {
        "YES": 0.1791,
        "NO": 0.5177,
        "UNKNOWN": 0.3031
      },
      "score": 0.5177,
      "margin": 0.21460000000000007,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "Please retain the replacement edition for operational reconciliation.",
      "state": "UNKNOWN",
      "native_value": "NO",
      "scores": {
        "YES": 0.1878,
        "NO": 0.7525,
        "UNKNOWN": 0.0598
      },
      "score": 0.7525,
      "margin": 0.5647,
      "historical": false,
      "supersession": true,
      "conditional": false
    },
    {
      "text": "Earlier notification conditions are superseded.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.5756,
        "NO": 0.3457,
        "UNKNOWN": 0.0786
      },
      "score": 0.5756,
      "margin": 0.2299,
      "historical": false,
      "supersession": true,
      "conditional": false
    }
  ],
  "escalation": {
    "escalated": false,
    "requested_predicates": [
      "share_blocking",
      "poa_required",
      "registration_required",
      "beneficial_owner_disclosure_required",
      "holding_confirmation_required",
      "split_voting_restricted",
      "securities_lending_recall_required",
      "other_voting_restriction"
    ],
    "reasons": {
      "share_blocking": [
        "LOW_RAW_SCORE"
      ],
      "poa_required": [
        "LOW_RAW_SCORE"
      ],
      "registration_required": [
        "LOW_RAW_SCORE"
      ],
      "beneficial_owner_disclosure_required": [
        "LOW_RAW_SCORE"
      ],
      "holding_confirmation_required": [
        "LOW_RAW_SCORE"
      ],
      "split_voting_restricted": [
        "LOW_RAW_SCORE"
      ],
      "securities_lending_recall_required": [
        "LOW_RAW_SCORE"
      ],
      "other_voting_restriction": [
        "LOW_RAW_SCORE"
      ]
    }
  },
  "conflicts": [
    "votability:STRUCTURE_SEMANTIC_CONFLICT"
  ],
  "reconciliation_for_field": []
}
```

## VALIDATION / BASE_LAYA / 2414be60f4dff3cc46dcf385c748749f7c7c3dc05ef8f904052ec9797bdc2f19 / securities_lending_recall_required

```text
[Message EL0104C | MT564]
Issuer secretariat memorandum concerning arrangements for the forthcoming extraordinary assembly.
The current agenda is open for shareholder voting instructions.
No requirement for voting-related immobilisation applies.
No requirement for an obligatory power-of-attorney document applies.
No requirement for a required voter registration form applies.
For this vote, beneficial-owner disclosure is required.
No requirement for documentary confirmation of ownership applies.
No requirement for a ban on splitting voting instructions applies.
No requirement for retrieval of loaned voting positions applies.
For this vote, a mandatory paper-only ballot is required.


[Message EL0104D | MT568]
Please retain the replacement edition for operational reconciliation. Earlier notification conditions are superseded.

```

```json
{
  "truth": "NO",
  "prediction": {
    "value": "YES",
    "scores": {
      "YES": 0.9407,
      "NO": 0.0463,
      "UNKNOWN": 0.013
    },
    "native_score": 0.9407,
    "confidence": null,
    "source": "REGISTERED_LAYA_PASSAGES",
    "evidence": [
      {
        "valid": true,
        "text": "For this vote, a mandatory paper-only ballot is required.",
        "start": 632,
        "end": 689,
        "source": "NATIVE_LAYA_PASSAGE_WITH_DETERMINISTIC_SCOPE"
      }
    ],
    "aggregation_reason": "STRONG_CURRENT_RELEVANT_EVIDENCE"
  },
  "whole_notice_scores": {
    "YES": 0.2481,
    "NO": 0.6864,
    "UNKNOWN": 0.0655
  },
  "passage_scores": [
    {
      "text": "[Message EL0104C | MT564]",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.6248,
        "NO": 0.2592,
        "UNKNOWN": 0.116
      },
      "score": 0.6248,
      "margin": 0.36560000000000004,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "Issuer secretariat memorandum concerning arrangements for the forthcoming extraordinary assembly.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.61,
        "NO": 0.3327,
        "UNKNOWN": 0.0574
      },
      "score": 0.61,
      "margin": 0.2773,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "The current agenda is open for shareholder voting instructions.",
      "state": "UNKNOWN",
      "native_value": "NO",
      "scores": {
        "YES": 0.3427,
        "NO": 0.5534,
        "UNKNOWN": 0.1039
      },
      "score": 0.5534,
      "margin": 0.2107,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for voting-related immobilisation applies.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.8341,
        "NO": 0.1352,
        "UNKNOWN": 0.0308
      },
      "score": 0.8341,
      "margin": 0.6989,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for an obligatory power-of-attorney document applies.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.763,
        "NO": 0.1998,
        "UNKNOWN": 0.0372
      },
      "score": 0.763,
      "margin": 0.5632,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for a required voter registration form applies.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.5902,
        "NO": 0.3591,
        "UNKNOWN": 0.0506
      },
      "score": 0.5902,
      "margin": 0.23109999999999997,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "For this vote, beneficial-owner disclosure is required.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.7062,
        "NO": 0.2109,
        "UNKNOWN": 0.0829
      },
      "score": 0.7062,
      "margin": 0.4953000000000001,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for documentary confirmation of ownership applies.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.701,
        "NO": 0.2482,
        "UNKNOWN": 0.0508
      },
      "score": 0.701,
      "margin": 0.4528,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for a ban on splitting voting instructions applies.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.8503,
        "NO": 0.1283,
        "UNKNOWN": 0.0214
      },
      "score": 0.8503,
      "margin": 0.722,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for retrieval of loaned voting positions applies.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.6994,
        "NO": 0.2438,
        "UNKNOWN": 0.0568
      },
      "score": 0.6994,
      "margin": 0.4556,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "For this vote, a mandatory paper-only ballot is required.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.9407,
        "NO": 0.0463,
        "UNKNOWN": 0.013
      },
      "score": 0.9407,
      "margin": 0.8944,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "[Message EL0104D | MT568]",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.5888,
        "NO": 0.2694,
        "UNKNOWN": 0.1418
      },
      "score": 0.5888,
      "margin": 0.3194,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "Please retain the replacement edition for operational reconciliation.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.5798,
        "NO": 0.335,
        "UNKNOWN": 0.0852
      },
      "score": 0.5798,
      "margin": 0.24479999999999996,
      "historical": false,
      "supersession": true,
      "conditional": false
    },
    {
      "text": "Earlier notification conditions are superseded.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.7353,
        "NO": 0.2046,
        "UNKNOWN": 0.0601
      },
      "score": 0.7353,
      "margin": 0.5307,
      "historical": false,
      "supersession": true,
      "conditional": false
    }
  ],
  "escalation": {
    "escalated": false,
    "requested_predicates": [
      "share_blocking",
      "poa_required",
      "registration_required",
      "beneficial_owner_disclosure_required",
      "holding_confirmation_required",
      "split_voting_restricted",
      "securities_lending_recall_required",
      "other_voting_restriction"
    ],
    "reasons": {
      "share_blocking": [
        "LOW_RAW_SCORE"
      ],
      "poa_required": [
        "LOW_RAW_SCORE"
      ],
      "registration_required": [
        "LOW_RAW_SCORE"
      ],
      "beneficial_owner_disclosure_required": [
        "LOW_RAW_SCORE"
      ],
      "holding_confirmation_required": [
        "LOW_RAW_SCORE"
      ],
      "split_voting_restricted": [
        "LOW_RAW_SCORE"
      ],
      "securities_lending_recall_required": [
        "LOW_RAW_SCORE"
      ],
      "other_voting_restriction": [
        "LOW_RAW_SCORE"
      ]
    }
  },
  "conflicts": [
    "votability:STRUCTURE_SEMANTIC_CONFLICT"
  ],
  "reconciliation_for_field": []
}
```

## VALIDATION / BASE_LAYA / 192427e9aa3ca6f904eb505ac724d3c90e8eba48b9c676788a55d6e407fcb195 / expected_final_status

```text
[Message EL0206C | MT564]
Broker service update: the institutional ballot channel is now available for this agenda.
This is solely a cash-distribution advice; it offers no meeting ballot and no shareholder vote.
No requirement for a voting lock on the position applies.
No requirement for a compulsory attorney mandate applies.
No requirement for mandatory meeting registration applies.
No requirement for identification of the underlying owner applies.
No requirement for a custodial holding statement applies.
No requirement for a requirement to cast all votes identically applies.
No requirement for recall of lent securities applies.
No requirement for an in-person-only voting condition applies.


[Message EL0206D | MT568]
Please retain the replacement edition for operational reconciliation. Earlier notification conditions are superseded.

```
```json
{
  "truth": "NOT_VOTABLE",
  "prediction": "UNCERTAIN_MANUAL_REVIEW",
  "decision": {
    "classification": "UNCERTAIN_MANUAL_REVIEW",
    "rule": "R1 unresolved conflicts",
    "rule_version": "semantic-decision-2",
    "manual_review_required": true,
    "automation_enabled": false,
    "review_reasons": [
      "other_voting_restriction:PASSAGE_CONFLICT",
      "Synthetic-only evaluation; customer quality gate not met"
    ]
  },
  "deadline": {
    "status": "OPEN",
    "comparisons": [
      {
        "source": "PROWIDE",
        "field_id": "prowide:9",
        "path": [
          "CAOPTN[1]"
        ],
        "deadline": {
          "iso": "2026-11-24T17:00:00+00:00",
          "offset_known": true,
          "precision": "SECOND"
        },
        "status": "OPEN",
        "field": {
          "components": [
            "RDDT",
            "20261124",
            "170000",
            "000",
            null,
            "00"
          ],
          "end": 226,
          "qualifier": "RDDT",
          "sequence_instance_path": [
            "CAOPTN[1]"
          ],
          "sequence_path": [
            "CAOPTN"
          ],
          "source": "PROWIDE",
          "source_text": ":98E::RDDT//20261124170000,000/00\n",
          "start": 192,
          "tag": "98E",
          "typed_field": "Field98E",
          "value": ":RDDT//20261124170000,000/00"
        }
      }
    ],
    "conflict": false,
    "source": "PROWIDE_COMPONENTS_DETERMINISTIC_COMPARISON",
    "reason": "Only RDDT is controlling. Bare local/date-only values require an agreed timezone profile; no UTC assumption."
  }
}
```

## VALIDATION / BASE_LAYA / 25150120b9a9e92a98ab8b33fb003cab98a2ec6b4230ec908fda5c15d2bbc7d7 / expected_final_status

```text
[Message EL0105C | MT564]
Issuer secretariat memorandum concerning arrangements for the forthcoming extraordinary assembly.
The current agenda is open for shareholder voting instructions.
No requirement for voting-related immobilisation applies.
No requirement for an obligatory power-of-attorney document applies.
For this vote, a required voter registration form is required.
No requirement for beneficial-owner disclosure applies.
No requirement for documentary confirmation of ownership applies.
No requirement for a ban on splitting voting instructions applies.
For this vote, retrieval of loaned voting positions is required.
No requirement for a mandatory paper-only ballot applies.


[Message EL0105D | MT568]
Please retain the replacement edition for operational reconciliation. Earlier notification conditions are superseded.

```
```json
{
  "truth": "VOTABLE_WITH_RESTRICTION",
  "prediction": "UNCERTAIN_MANUAL_REVIEW",
  "decision": {
    "classification": "UNCERTAIN_MANUAL_REVIEW",
    "rule": "R1 unresolved conflicts",
    "rule_version": "semantic-decision-2",
    "manual_review_required": true,
    "automation_enabled": false,
    "review_reasons": [
      "other_voting_restriction:PASSAGE_CONFLICT",
      "votability:STRUCTURE_SEMANTIC_CONFLICT",
      "Synthetic-only evaluation; customer quality gate not met"
    ]
  },
  "deadline": {
    "status": "OPEN",
    "comparisons": [
      {
        "source": "PROWIDE",
        "field_id": "prowide:10",
        "path": [
          "CAOPTN[1]"
        ],
        "deadline": {
          "iso": "2026-11-24T17:00:00+00:00",
          "offset_known": true,
          "precision": "SECOND"
        },
        "status": "OPEN",
        "field": {
          "components": [
            "RDDT",
            "20261124",
            "170000",
            "000",
            null,
            "00"
          ],
          "end": 243,
          "qualifier": "RDDT",
          "sequence_instance_path": [
            "CAOPTN[1]"
          ],
          "sequence_path": [
            "CAOPTN"
          ],
          "source": "PROWIDE",
          "source_text": ":98E::RDDT//20261124170000,000/00\n",
          "start": 209,
          "tag": "98E",
          "typed_field": "Field98E",
          "value": ":RDDT//20261124170000,000/00"
        }
      }
    ],
    "conflict": false,
    "source": "PROWIDE_COMPONENTS_DETERMINISTIC_COMPARISON",
    "reason": "Only RDDT is controlling. Bare local/date-only values require an agreed timezone profile; no UTC assumption."
  }
}
```

## VALIDATION / BASE_LAYA / 2414be60f4dff3cc46dcf385c748749f7c7c3dc05ef8f904052ec9797bdc2f19 / expected_final_status

```text
[Message EL0104C | MT564]
Issuer secretariat memorandum concerning arrangements for the forthcoming extraordinary assembly.
The current agenda is open for shareholder voting instructions.
No requirement for voting-related immobilisation applies.
No requirement for an obligatory power-of-attorney document applies.
No requirement for a required voter registration form applies.
For this vote, beneficial-owner disclosure is required.
No requirement for documentary confirmation of ownership applies.
No requirement for a ban on splitting voting instructions applies.
No requirement for retrieval of loaned voting positions applies.
For this vote, a mandatory paper-only ballot is required.


[Message EL0104D | MT568]
Please retain the replacement edition for operational reconciliation. Earlier notification conditions are superseded.

```
```json
{
  "truth": "DEADLINE_PASSED",
  "prediction": "UNCERTAIN_MANUAL_REVIEW",
  "decision": {
    "classification": "UNCERTAIN_MANUAL_REVIEW",
    "rule": "R1 unresolved conflicts",
    "rule_version": "semantic-decision-2",
    "manual_review_required": true,
    "automation_enabled": false,
    "review_reasons": [
      "votability:STRUCTURE_SEMANTIC_CONFLICT",
      "Synthetic-only evaluation; customer quality gate not met"
    ]
  },
  "deadline": {
    "status": "PASSED",
    "comparisons": [
      {
        "source": "PROWIDE",
        "field_id": "prowide:10",
        "path": [
          "CAOPTN[1]"
        ],
        "deadline": {
          "iso": "2025-09-01T17:00:00+00:00",
          "offset_known": true,
          "precision": "SECOND"
        },
        "status": "PASSED",
        "field": {
          "components": [
            "RDDT",
            "20250901",
            "170000",
            "000",
            null,
            "00"
          ],
          "end": 243,
          "qualifier": "RDDT",
          "sequence_instance_path": [
            "CAOPTN[1]"
          ],
          "sequence_path": [
            "CAOPTN"
          ],
          "source": "PROWIDE",
          "source_text": ":98E::RDDT//20250901170000,000/00\n",
          "start": 209,
          "tag": "98E",
          "typed_field": "Field98E",
          "value": ":RDDT//20250901170000,000/00"
        }
      }
    ],
    "conflict": false,
    "source": "PROWIDE_COMPONENTS_DETERMINISTIC_COMPARISON",
    "reason": "Only RDDT is controlling. Bare local/date-only values require an agreed timezone profile; no UTC assumption."
  }
}
```

## VALIDATION / TRAINED_LAYA / 192427e9aa3ca6f904eb505ac724d3c90e8eba48b9c676788a55d6e407fcb195 / share_blocking

```text
[Message EL0206C | MT564]
Broker service update: the institutional ballot channel is now available for this agenda.
This is solely a cash-distribution advice; it offers no meeting ballot and no shareholder vote.
No requirement for a voting lock on the position applies.
No requirement for a compulsory attorney mandate applies.
No requirement for mandatory meeting registration applies.
No requirement for identification of the underlying owner applies.
No requirement for a custodial holding statement applies.
No requirement for a requirement to cast all votes identically applies.
No requirement for recall of lent securities applies.
No requirement for an in-person-only voting condition applies.


[Message EL0206D | MT568]
Please retain the replacement edition for operational reconciliation. Earlier notification conditions are superseded.

```

```json
{
  "truth": "NO",
  "prediction": {
    "value": "YES",
    "scores": {
      "YES": 0.9632,
      "NO": 0.0123,
      "UNKNOWN": 0.0244
    },
    "native_score": 0.9632,
    "confidence": null,
    "source": "REGISTERED_LAYA_PASSAGES",
    "evidence": [
      {
        "valid": true,
        "text": "Earlier notification conditions are superseded.",
        "start": 799,
        "end": 846,
        "source": "NATIVE_LAYA_PASSAGE_WITH_DETERMINISTIC_SCOPE"
      }
    ],
    "aggregation_reason": "STRONG_CURRENT_RELEVANT_EVIDENCE"
  },
  "whole_notice_scores": {
    "YES": 0.8643,
    "NO": 0.0941,
    "UNKNOWN": 0.0416
  },
  "passage_scores": [
    {
      "text": "[Message EL0206C | MT564]",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.9274,
        "NO": 0.0274,
        "UNKNOWN": 0.0452
      },
      "score": 0.9274,
      "margin": 0.8822,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "Broker service update: the institutional ballot channel is now available for this agenda.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.858,
        "NO": 0.08,
        "UNKNOWN": 0.062
      },
      "score": 0.858,
      "margin": 0.778,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "This is solely a cash-distribution advice; it offers no meeting ballot and no shareholder vote.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.9437,
        "NO": 0.0315,
        "UNKNOWN": 0.0248
      },
      "score": 0.9437,
      "margin": 0.9122,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for a voting lock on the position applies.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.86,
        "NO": 0.0962,
        "UNKNOWN": 0.0438
      },
      "score": 0.86,
      "margin": 0.7638,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for a compulsory attorney mandate applies.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.9405,
        "NO": 0.0385,
        "UNKNOWN": 0.021
      },
      "score": 0.9405,
      "margin": 0.902,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for mandatory meeting registration applies.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.9214,
        "NO": 0.041,
        "UNKNOWN": 0.0376
      },
      "score": 0.9214,
      "margin": 0.8804,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for identification of the underlying owner applies.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.9292,
        "NO": 0.0368,
        "UNKNOWN": 0.0341
      },
      "score": 0.9292,
      "margin": 0.8924000000000001,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for a custodial holding statement applies.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.9021,
        "NO": 0.0575,
        "UNKNOWN": 0.0404
      },
      "score": 0.9021,
      "margin": 0.8446,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for a requirement to cast all votes identically applies.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.8764,
        "NO": 0.0703,
        "UNKNOWN": 0.0533
      },
      "score": 0.8764,
      "margin": 0.8060999999999999,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for recall of lent securities applies.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.9214,
        "NO": 0.0467,
        "UNKNOWN": 0.0319
      },
      "score": 0.9214,
      "margin": 0.8747,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for an in-person-only voting condition applies.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.5156,
        "NO": 0.3209,
        "UNKNOWN": 0.1634
      },
      "score": 0.5156,
      "margin": 0.19469999999999993,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "[Message EL0206D | MT568]",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.9297,
        "NO": 0.0283,
        "UNKNOWN": 0.042
      },
      "score": 0.9297,
      "margin": 0.8876999999999999,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "Please retain the replacement edition for operational reconciliation.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.9104,
        "NO": 0.053,
        "UNKNOWN": 0.0366
      },
      "score": 0.9104,
      "margin": 0.8573999999999999,
      "historical": false,
      "supersession": true,
      "conditional": false
    },
    {
      "text": "Earlier notification conditions are superseded.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.9632,
        "NO": 0.0123,
        "UNKNOWN": 0.0244
      },
      "score": 0.9632,
      "margin": 0.9388,
      "historical": false,
      "supersession": true,
      "conditional": false
    }
  ],
  "escalation": {
    "escalated": false,
    "requested_predicates": [
      "votability",
      "share_blocking",
      "poa_required",
      "registration_required",
      "beneficial_owner_disclosure_required",
      "holding_confirmation_required",
      "split_voting_restricted",
      "securities_lending_recall_required",
      "other_voting_restriction"
    ],
    "reasons": {
      "votability": [
        "LOW_RAW_SCORE",
        "LOW_MARGIN"
      ],
      "share_blocking": [
        "LOW_RAW_SCORE"
      ],
      "poa_required": [
        "LOW_RAW_SCORE",
        "LOW_MARGIN",
        "EVIDENCE_UNAVAILABLE"
      ],
      "registration_required": [
        "LOW_RAW_SCORE"
      ],
      "beneficial_owner_disclosure_required": [
        "LOW_RAW_SCORE"
      ],
      "holding_confirmation_required": [
        "UNKNOWN",
        "LOW_RAW_SCORE",
        "LOW_MARGIN",
        "EVIDENCE_UNAVAILABLE"
      ],
      "split_voting_restricted": [
        "UNKNOWN",
        "LOW_RAW_SCORE",
        "LOW_MARGIN",
        "EVIDENCE_UNAVAILABLE"
      ],
      "securities_lending_recall_required": [
        "LOW_RAW_SCORE"
      ],
      "other_voting_restriction": [
        "UNKNOWN",
        "PASSAGE_CONFLICT",
        "LOW_RAW_SCORE",
        "LOW_MARGIN",
        "EVIDENCE_UNAVAILABLE"
      ]
    }
  },
  "conflicts": [
    "other_voting_restriction:PASSAGE_CONFLICT"
  ],
  "reconciliation_for_field": []
}
```

## VALIDATION / TRAINED_LAYA / 192427e9aa3ca6f904eb505ac724d3c90e8eba48b9c676788a55d6e407fcb195 / registration_required

```text
[Message EL0206C | MT564]
Broker service update: the institutional ballot channel is now available for this agenda.
This is solely a cash-distribution advice; it offers no meeting ballot and no shareholder vote.
No requirement for a voting lock on the position applies.
No requirement for a compulsory attorney mandate applies.
No requirement for mandatory meeting registration applies.
No requirement for identification of the underlying owner applies.
No requirement for a custodial holding statement applies.
No requirement for a requirement to cast all votes identically applies.
No requirement for recall of lent securities applies.
No requirement for an in-person-only voting condition applies.


[Message EL0206D | MT568]
Please retain the replacement edition for operational reconciliation. Earlier notification conditions are superseded.

```

```json
{
  "truth": "NO",
  "prediction": {
    "value": "YES",
    "scores": {
      "YES": 0.8329,
      "NO": 0.1315,
      "UNKNOWN": 0.0356
    },
    "native_score": 0.8329,
    "confidence": null,
    "source": "REGISTERED_LAYA_PASSAGES",
    "evidence": [
      {
        "valid": true,
        "text": "No requirement for a custodial holding statement applies.",
        "start": 454,
        "end": 511,
        "source": "NATIVE_LAYA_PASSAGE_WITH_DETERMINISTIC_SCOPE"
      }
    ],
    "aggregation_reason": "STRONG_CURRENT_RELEVANT_EVIDENCE"
  },
  "whole_notice_scores": {
    "YES": 0.3798,
    "NO": 0.4589,
    "UNKNOWN": 0.1614
  },
  "passage_scores": [
    {
      "text": "[Message EL0206C | MT564]",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.4786,
        "NO": 0.2675,
        "UNKNOWN": 0.2539
      },
      "score": 0.4786,
      "margin": 0.2111,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "Broker service update: the institutional ballot channel is now available for this agenda.",
      "state": "UNKNOWN",
      "native_value": "NO",
      "scores": {
        "YES": 0.3833,
        "NO": 0.4561,
        "UNKNOWN": 0.1606
      },
      "score": 0.4561,
      "margin": 0.07280000000000003,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "This is solely a cash-distribution advice; it offers no meeting ballot and no shareholder vote.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.7642,
        "NO": 0.2014,
        "UNKNOWN": 0.0344
      },
      "score": 0.7642,
      "margin": 0.5628,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for a voting lock on the position applies.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.685,
        "NO": 0.2818,
        "UNKNOWN": 0.0332
      },
      "score": 0.685,
      "margin": 0.40320000000000006,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for a compulsory attorney mandate applies.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.813,
        "NO": 0.1633,
        "UNKNOWN": 0.0237
      },
      "score": 0.813,
      "margin": 0.6496999999999999,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for mandatory meeting registration applies.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.6825,
        "NO": 0.2784,
        "UNKNOWN": 0.0391
      },
      "score": 0.6825,
      "margin": 0.4041,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for identification of the underlying owner applies.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.6885,
        "NO": 0.263,
        "UNKNOWN": 0.0485
      },
      "score": 0.6885,
      "margin": 0.4255,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for a custodial holding statement applies.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.8329,
        "NO": 0.1315,
        "UNKNOWN": 0.0356
      },
      "score": 0.8329,
      "margin": 0.7014,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for a requirement to cast all votes identically applies.",
      "state": "UNKNOWN",
      "native_value": "NO",
      "scores": {
        "YES": 0.3075,
        "NO": 0.6067,
        "UNKNOWN": 0.0858
      },
      "score": 0.6067,
      "margin": 0.2992,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for recall of lent securities applies.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.6795,
        "NO": 0.2704,
        "UNKNOWN": 0.05
      },
      "score": 0.6795,
      "margin": 0.4091,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for an in-person-only voting condition applies.",
      "state": "UNKNOWN",
      "native_value": "NO",
      "scores": {
        "YES": 0.1321,
        "NO": 0.6574,
        "UNKNOWN": 0.2105
      },
      "score": 0.6574,
      "margin": 0.44689999999999996,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "[Message EL0206D | MT568]",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.4527,
        "NO": 0.2911,
        "UNKNOWN": 0.2561
      },
      "score": 0.4527,
      "margin": 0.16159999999999997,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "Please retain the replacement edition for operational reconciliation.",
      "state": "UNKNOWN",
      "native_value": "NO",
      "scores": {
        "YES": 0.3889,
        "NO": 0.5066,
        "UNKNOWN": 0.1045
      },
      "score": 0.5066,
      "margin": 0.11770000000000003,
      "historical": false,
      "supersession": true,
      "conditional": false
    },
    {
      "text": "Earlier notification conditions are superseded.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.597,
        "NO": 0.3291,
        "UNKNOWN": 0.0739
      },
      "score": 0.597,
      "margin": 0.26789999999999997,
      "historical": false,
      "supersession": true,
      "conditional": false
    }
  ],
  "escalation": {
    "escalated": false,
    "requested_predicates": [
      "votability",
      "share_blocking",
      "poa_required",
      "registration_required",
      "beneficial_owner_disclosure_required",
      "holding_confirmation_required",
      "split_voting_restricted",
      "securities_lending_recall_required",
      "other_voting_restriction"
    ],
    "reasons": {
      "votability": [
        "LOW_RAW_SCORE",
        "LOW_MARGIN"
      ],
      "share_blocking": [
        "LOW_RAW_SCORE"
      ],
      "poa_required": [
        "LOW_RAW_SCORE",
        "LOW_MARGIN",
        "EVIDENCE_UNAVAILABLE"
      ],
      "registration_required": [
        "LOW_RAW_SCORE"
      ],
      "beneficial_owner_disclosure_required": [
        "LOW_RAW_SCORE"
      ],
      "holding_confirmation_required": [
        "UNKNOWN",
        "LOW_RAW_SCORE",
        "LOW_MARGIN",
        "EVIDENCE_UNAVAILABLE"
      ],
      "split_voting_restricted": [
        "UNKNOWN",
        "LOW_RAW_SCORE",
        "LOW_MARGIN",
        "EVIDENCE_UNAVAILABLE"
      ],
      "securities_lending_recall_required": [
        "LOW_RAW_SCORE"
      ],
      "other_voting_restriction": [
        "UNKNOWN",
        "PASSAGE_CONFLICT",
        "LOW_RAW_SCORE",
        "LOW_MARGIN",
        "EVIDENCE_UNAVAILABLE"
      ]
    }
  },
  "conflicts": [
    "other_voting_restriction:PASSAGE_CONFLICT"
  ],
  "reconciliation_for_field": []
}
```

## VALIDATION / TRAINED_LAYA / 192427e9aa3ca6f904eb505ac724d3c90e8eba48b9c676788a55d6e407fcb195 / holding_confirmation_required

```text
[Message EL0206C | MT564]
Broker service update: the institutional ballot channel is now available for this agenda.
This is solely a cash-distribution advice; it offers no meeting ballot and no shareholder vote.
No requirement for a voting lock on the position applies.
No requirement for a compulsory attorney mandate applies.
No requirement for mandatory meeting registration applies.
No requirement for identification of the underlying owner applies.
No requirement for a custodial holding statement applies.
No requirement for a requirement to cast all votes identically applies.
No requirement for recall of lent securities applies.
No requirement for an in-person-only voting condition applies.


[Message EL0206D | MT568]
Please retain the replacement edition for operational reconciliation. Earlier notification conditions are superseded.

```

```json
{
  "truth": "NO",
  "prediction": {
    "value": "UNKNOWN",
    "scores": {},
    "native_score": null,
    "confidence": null,
    "source": "REGISTERED_LAYA_PASSAGES",
    "evidence": [],
    "aggregation_reason": "NO_STRONG_CURRENT_RELEVANT_STATEMENT"
  },
  "whole_notice_scores": {
    "YES": 0.4978,
    "NO": 0.276,
    "UNKNOWN": 0.2262
  },
  "passage_scores": [
    {
      "text": "[Message EL0206C | MT564]",
      "state": "UNKNOWN",
      "native_value": "NO",
      "scores": {
        "YES": 0.0848,
        "NO": 0.6041,
        "UNKNOWN": 0.3111
      },
      "score": 0.6041,
      "margin": 0.293,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "Broker service update: the institutional ballot channel is now available for this agenda.",
      "state": "UNKNOWN",
      "native_value": "NO",
      "scores": {
        "YES": 0.2317,
        "NO": 0.455,
        "UNKNOWN": 0.3133
      },
      "score": 0.455,
      "margin": 0.1417,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "This is solely a cash-distribution advice; it offers no meeting ballot and no shareholder vote.",
      "state": "UNKNOWN",
      "native_value": "NO",
      "scores": {
        "YES": 0.134,
        "NO": 0.6982,
        "UNKNOWN": 0.1678
      },
      "score": 0.6982,
      "margin": 0.5304,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for a voting lock on the position applies.",
      "state": "UNKNOWN",
      "native_value": "NO",
      "scores": {
        "YES": 0.0932,
        "NO": 0.7337,
        "UNKNOWN": 0.1731
      },
      "score": 0.7337,
      "margin": 0.5606,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for a compulsory attorney mandate applies.",
      "state": "UNKNOWN",
      "native_value": "NO",
      "scores": {
        "YES": 0.1105,
        "NO": 0.7214,
        "UNKNOWN": 0.1681
      },
      "score": 0.7214,
      "margin": 0.5533,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for mandatory meeting registration applies.",
      "state": "UNKNOWN",
      "native_value": "NO",
      "scores": {
        "YES": 0.1005,
        "NO": 0.7088,
        "UNKNOWN": 0.1907
      },
      "score": 0.7088,
      "margin": 0.5181,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for identification of the underlying owner applies.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.4231,
        "NO": 0.4166,
        "UNKNOWN": 0.1603
      },
      "score": 0.4231,
      "margin": 0.00649999999999995,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for a custodial holding statement applies.",
      "state": "NEGATIVE",
      "native_value": "NO",
      "scores": {
        "YES": 0.1836,
        "NO": 0.5383,
        "UNKNOWN": 0.278
      },
      "score": 0.5383,
      "margin": 0.2603,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for a requirement to cast all votes identically applies.",
      "state": "UNKNOWN",
      "native_value": "NO",
      "scores": {
        "YES": 0.0812,
        "NO": 0.8201,
        "UNKNOWN": 0.0988
      },
      "score": 0.8201,
      "margin": 0.7213,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for recall of lent securities applies.",
      "state": "UNKNOWN",
      "native_value": "NO",
      "scores": {
        "YES": 0.0759,
        "NO": 0.8134,
        "UNKNOWN": 0.1107
      },
      "score": 0.8134,
      "margin": 0.7027,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for an in-person-only voting condition applies.",
      "state": "UNKNOWN",
      "native_value": "NO",
      "scores": {
        "YES": 0.0286,
        "NO": 0.7233,
        "UNKNOWN": 0.248
      },
      "score": 0.7233,
      "margin": 0.47530000000000006,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "[Message EL0206D | MT568]",
      "state": "UNKNOWN",
      "native_value": "NO",
      "scores": {
        "YES": 0.0702,
        "NO": 0.6671,
        "UNKNOWN": 0.2626
      },
      "score": 0.6671,
      "margin": 0.4045,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "Please retain the replacement edition for operational reconciliation.",
      "state": "UNKNOWN",
      "native_value": "NO",
      "scores": {
        "YES": 0.1701,
        "NO": 0.6672,
        "UNKNOWN": 0.1626
      },
      "score": 0.6672,
      "margin": 0.4971,
      "historical": false,
      "supersession": true,
      "conditional": false
    },
    {
      "text": "Earlier notification conditions are superseded.",
      "state": "UNKNOWN",
      "native_value": "UNKNOWN",
      "scores": {
        "YES": 0.2577,
        "NO": 0.3233,
        "UNKNOWN": 0.419
      },
      "score": 0.419,
      "margin": 0.09570000000000001,
      "historical": false,
      "supersession": true,
      "conditional": false
    }
  ],
  "escalation": {
    "escalated": false,
    "requested_predicates": [
      "votability",
      "share_blocking",
      "poa_required",
      "registration_required",
      "beneficial_owner_disclosure_required",
      "holding_confirmation_required",
      "split_voting_restricted",
      "securities_lending_recall_required",
      "other_voting_restriction"
    ],
    "reasons": {
      "votability": [
        "LOW_RAW_SCORE",
        "LOW_MARGIN"
      ],
      "share_blocking": [
        "LOW_RAW_SCORE"
      ],
      "poa_required": [
        "LOW_RAW_SCORE",
        "LOW_MARGIN",
        "EVIDENCE_UNAVAILABLE"
      ],
      "registration_required": [
        "LOW_RAW_SCORE"
      ],
      "beneficial_owner_disclosure_required": [
        "LOW_RAW_SCORE"
      ],
      "holding_confirmation_required": [
        "UNKNOWN",
        "LOW_RAW_SCORE",
        "LOW_MARGIN",
        "EVIDENCE_UNAVAILABLE"
      ],
      "split_voting_restricted": [
        "UNKNOWN",
        "LOW_RAW_SCORE",
        "LOW_MARGIN",
        "EVIDENCE_UNAVAILABLE"
      ],
      "securities_lending_recall_required": [
        "LOW_RAW_SCORE"
      ],
      "other_voting_restriction": [
        "UNKNOWN",
        "PASSAGE_CONFLICT",
        "LOW_RAW_SCORE",
        "LOW_MARGIN",
        "EVIDENCE_UNAVAILABLE"
      ]
    }
  },
  "conflicts": [
    "other_voting_restriction:PASSAGE_CONFLICT"
  ],
  "reconciliation_for_field": []
}
```

## VALIDATION / TRAINED_LAYA / 192427e9aa3ca6f904eb505ac724d3c90e8eba48b9c676788a55d6e407fcb195 / split_voting_restricted

```text
[Message EL0206C | MT564]
Broker service update: the institutional ballot channel is now available for this agenda.
This is solely a cash-distribution advice; it offers no meeting ballot and no shareholder vote.
No requirement for a voting lock on the position applies.
No requirement for a compulsory attorney mandate applies.
No requirement for mandatory meeting registration applies.
No requirement for identification of the underlying owner applies.
No requirement for a custodial holding statement applies.
No requirement for a requirement to cast all votes identically applies.
No requirement for recall of lent securities applies.
No requirement for an in-person-only voting condition applies.


[Message EL0206D | MT568]
Please retain the replacement edition for operational reconciliation. Earlier notification conditions are superseded.

```

```json
{
  "truth": "NO",
  "prediction": {
    "value": "UNKNOWN",
    "scores": {},
    "native_score": null,
    "confidence": null,
    "source": "REGISTERED_LAYA_PASSAGES",
    "evidence": [],
    "aggregation_reason": "NO_STRONG_CURRENT_RELEVANT_STATEMENT"
  },
  "whole_notice_scores": {
    "YES": 0.3607,
    "NO": 0.5605,
    "UNKNOWN": 0.0787
  },
  "passage_scores": [
    {
      "text": "[Message EL0206C | MT564]",
      "state": "UNKNOWN",
      "native_value": "NO",
      "scores": {
        "YES": 0.2755,
        "NO": 0.3989,
        "UNKNOWN": 0.3255
      },
      "score": 0.3989,
      "margin": 0.07339999999999997,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "Broker service update: the institutional ballot channel is now available for this agenda.",
      "state": "UNKNOWN",
      "native_value": "NO",
      "scores": {
        "YES": 0.2557,
        "NO": 0.5983,
        "UNKNOWN": 0.146
      },
      "score": 0.5983,
      "margin": 0.34260000000000007,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "This is solely a cash-distribution advice; it offers no meeting ballot and no shareholder vote.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.6608,
        "NO": 0.267,
        "UNKNOWN": 0.0722
      },
      "score": 0.6608,
      "margin": 0.39380000000000004,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for a voting lock on the position applies.",
      "state": "UNKNOWN",
      "native_value": "NO",
      "scores": {
        "YES": 0.3069,
        "NO": 0.5844,
        "UNKNOWN": 0.1087
      },
      "score": 0.5844,
      "margin": 0.2775,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for a compulsory attorney mandate applies.",
      "state": "UNKNOWN",
      "native_value": "NO",
      "scores": {
        "YES": 0.2958,
        "NO": 0.5613,
        "UNKNOWN": 0.143
      },
      "score": 0.5613,
      "margin": 0.2655,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for mandatory meeting registration applies.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.5105,
        "NO": 0.4416,
        "UNKNOWN": 0.0479
      },
      "score": 0.5105,
      "margin": 0.06889999999999996,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for identification of the underlying owner applies.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.3998,
        "NO": 0.3973,
        "UNKNOWN": 0.2029
      },
      "score": 0.3998,
      "margin": 0.0025000000000000022,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for a custodial holding statement applies.",
      "state": "UNKNOWN",
      "native_value": "NO",
      "scores": {
        "YES": 0.2424,
        "NO": 0.6404,
        "UNKNOWN": 0.1172
      },
      "score": 0.6404,
      "margin": 0.39799999999999996,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for a requirement to cast all votes identically applies.",
      "state": "UNKNOWN",
      "native_value": "NO",
      "scores": {
        "YES": 0.2106,
        "NO": 0.7259,
        "UNKNOWN": 0.0635
      },
      "score": 0.7259,
      "margin": 0.5153,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for recall of lent securities applies.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.6313,
        "NO": 0.3017,
        "UNKNOWN": 0.0671
      },
      "score": 0.6313,
      "margin": 0.32959999999999995,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for an in-person-only voting condition applies.",
      "state": "UNKNOWN",
      "native_value": "NO",
      "scores": {
        "YES": 0.3574,
        "NO": 0.5276,
        "UNKNOWN": 0.115
      },
      "score": 0.5276,
      "margin": 0.17019999999999996,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "[Message EL0206D | MT568]",
      "state": "UNKNOWN",
      "native_value": "NO",
      "scores": {
        "YES": 0.205,
        "NO": 0.4557,
        "UNKNOWN": 0.3393
      },
      "score": 0.4557,
      "margin": 0.1164,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "Please retain the replacement edition for operational reconciliation.",
      "state": "UNKNOWN",
      "native_value": "NO",
      "scores": {
        "YES": 0.1878,
        "NO": 0.7297,
        "UNKNOWN": 0.0824
      },
      "score": 0.7297,
      "margin": 0.5419,
      "historical": false,
      "supersession": true,
      "conditional": false
    },
    {
      "text": "Earlier notification conditions are superseded.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.4973,
        "NO": 0.3914,
        "UNKNOWN": 0.1113
      },
      "score": 0.4973,
      "margin": 0.1059,
      "historical": false,
      "supersession": true,
      "conditional": false
    }
  ],
  "escalation": {
    "escalated": false,
    "requested_predicates": [
      "votability",
      "share_blocking",
      "poa_required",
      "registration_required",
      "beneficial_owner_disclosure_required",
      "holding_confirmation_required",
      "split_voting_restricted",
      "securities_lending_recall_required",
      "other_voting_restriction"
    ],
    "reasons": {
      "votability": [
        "LOW_RAW_SCORE",
        "LOW_MARGIN"
      ],
      "share_blocking": [
        "LOW_RAW_SCORE"
      ],
      "poa_required": [
        "LOW_RAW_SCORE",
        "LOW_MARGIN",
        "EVIDENCE_UNAVAILABLE"
      ],
      "registration_required": [
        "LOW_RAW_SCORE"
      ],
      "beneficial_owner_disclosure_required": [
        "LOW_RAW_SCORE"
      ],
      "holding_confirmation_required": [
        "UNKNOWN",
        "LOW_RAW_SCORE",
        "LOW_MARGIN",
        "EVIDENCE_UNAVAILABLE"
      ],
      "split_voting_restricted": [
        "UNKNOWN",
        "LOW_RAW_SCORE",
        "LOW_MARGIN",
        "EVIDENCE_UNAVAILABLE"
      ],
      "securities_lending_recall_required": [
        "LOW_RAW_SCORE"
      ],
      "other_voting_restriction": [
        "UNKNOWN",
        "PASSAGE_CONFLICT",
        "LOW_RAW_SCORE",
        "LOW_MARGIN",
        "EVIDENCE_UNAVAILABLE"
      ]
    }
  },
  "conflicts": [
    "other_voting_restriction:PASSAGE_CONFLICT"
  ],
  "reconciliation_for_field": []
}
```

## VALIDATION / TRAINED_LAYA / 192427e9aa3ca6f904eb505ac724d3c90e8eba48b9c676788a55d6e407fcb195 / securities_lending_recall_required

```text
[Message EL0206C | MT564]
Broker service update: the institutional ballot channel is now available for this agenda.
This is solely a cash-distribution advice; it offers no meeting ballot and no shareholder vote.
No requirement for a voting lock on the position applies.
No requirement for a compulsory attorney mandate applies.
No requirement for mandatory meeting registration applies.
No requirement for identification of the underlying owner applies.
No requirement for a custodial holding statement applies.
No requirement for a requirement to cast all votes identically applies.
No requirement for recall of lent securities applies.
No requirement for an in-person-only voting condition applies.


[Message EL0206D | MT568]
Please retain the replacement edition for operational reconciliation. Earlier notification conditions are superseded.

```

```json
{
  "truth": "NO",
  "prediction": {
    "value": "YES",
    "scores": {
      "YES": 0.8045,
      "NO": 0.1563,
      "UNKNOWN": 0.0393
    },
    "native_score": 0.8045,
    "confidence": null,
    "source": "REGISTERED_LAYA_PASSAGES",
    "evidence": [
      {
        "valid": true,
        "text": "No requirement for a custodial holding statement applies.",
        "start": 454,
        "end": 511,
        "source": "NATIVE_LAYA_PASSAGE_WITH_DETERMINISTIC_SCOPE"
      }
    ],
    "aggregation_reason": "STRONG_CURRENT_RELEVANT_EVIDENCE"
  },
  "whole_notice_scores": {
    "YES": 0.4992,
    "NO": 0.4082,
    "UNKNOWN": 0.0926
  },
  "passage_scores": [
    {
      "text": "[Message EL0206C | MT564]",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.5572,
        "NO": 0.2849,
        "UNKNOWN": 0.1579
      },
      "score": 0.5572,
      "margin": 0.27230000000000004,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "Broker service update: the institutional ballot channel is now available for this agenda.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.5641,
        "NO": 0.2808,
        "UNKNOWN": 0.1551
      },
      "score": 0.5641,
      "margin": 0.28330000000000005,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "This is solely a cash-distribution advice; it offers no meeting ballot and no shareholder vote.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.6127,
        "NO": 0.3202,
        "UNKNOWN": 0.0671
      },
      "score": 0.6127,
      "margin": 0.29250000000000004,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for a voting lock on the position applies.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.7005,
        "NO": 0.2407,
        "UNKNOWN": 0.0588
      },
      "score": 0.7005,
      "margin": 0.4598,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for a compulsory attorney mandate applies.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.6965,
        "NO": 0.2437,
        "UNKNOWN": 0.0598
      },
      "score": 0.6965,
      "margin": 0.4528,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for mandatory meeting registration applies.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.6962,
        "NO": 0.2351,
        "UNKNOWN": 0.0687
      },
      "score": 0.6962,
      "margin": 0.46110000000000007,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for identification of the underlying owner applies.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.6681,
        "NO": 0.2491,
        "UNKNOWN": 0.0828
      },
      "score": 0.6681,
      "margin": 0.41900000000000004,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for a custodial holding statement applies.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.8045,
        "NO": 0.1563,
        "UNKNOWN": 0.0393
      },
      "score": 0.8045,
      "margin": 0.6482,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for a requirement to cast all votes identically applies.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.4843,
        "NO": 0.442,
        "UNKNOWN": 0.0737
      },
      "score": 0.4843,
      "margin": 0.042300000000000004,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for recall of lent securities applies.",
      "state": "NEGATIVE",
      "native_value": "NO",
      "scores": {
        "YES": 0.3439,
        "NO": 0.6291,
        "UNKNOWN": 0.0271
      },
      "score": 0.6291,
      "margin": 0.2852,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for an in-person-only voting condition applies.",
      "state": "UNKNOWN",
      "native_value": "NO",
      "scores": {
        "YES": 0.2737,
        "NO": 0.547,
        "UNKNOWN": 0.1794
      },
      "score": 0.547,
      "margin": 0.27330000000000004,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "[Message EL0206D | MT568]",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.5434,
        "NO": 0.2793,
        "UNKNOWN": 0.1772
      },
      "score": 0.5434,
      "margin": 0.2641,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "Please retain the replacement edition for operational reconciliation.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.5096,
        "NO": 0.375,
        "UNKNOWN": 0.1154
      },
      "score": 0.5096,
      "margin": 0.13460000000000005,
      "historical": false,
      "supersession": true,
      "conditional": false
    },
    {
      "text": "Earlier notification conditions are superseded.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.6434,
        "NO": 0.2655,
        "UNKNOWN": 0.0912
      },
      "score": 0.6434,
      "margin": 0.37789999999999996,
      "historical": false,
      "supersession": true,
      "conditional": false
    }
  ],
  "escalation": {
    "escalated": false,
    "requested_predicates": [
      "votability",
      "share_blocking",
      "poa_required",
      "registration_required",
      "beneficial_owner_disclosure_required",
      "holding_confirmation_required",
      "split_voting_restricted",
      "securities_lending_recall_required",
      "other_voting_restriction"
    ],
    "reasons": {
      "votability": [
        "LOW_RAW_SCORE",
        "LOW_MARGIN"
      ],
      "share_blocking": [
        "LOW_RAW_SCORE"
      ],
      "poa_required": [
        "LOW_RAW_SCORE",
        "LOW_MARGIN",
        "EVIDENCE_UNAVAILABLE"
      ],
      "registration_required": [
        "LOW_RAW_SCORE"
      ],
      "beneficial_owner_disclosure_required": [
        "LOW_RAW_SCORE"
      ],
      "holding_confirmation_required": [
        "UNKNOWN",
        "LOW_RAW_SCORE",
        "LOW_MARGIN",
        "EVIDENCE_UNAVAILABLE"
      ],
      "split_voting_restricted": [
        "UNKNOWN",
        "LOW_RAW_SCORE",
        "LOW_MARGIN",
        "EVIDENCE_UNAVAILABLE"
      ],
      "securities_lending_recall_required": [
        "LOW_RAW_SCORE"
      ],
      "other_voting_restriction": [
        "UNKNOWN",
        "PASSAGE_CONFLICT",
        "LOW_RAW_SCORE",
        "LOW_MARGIN",
        "EVIDENCE_UNAVAILABLE"
      ]
    }
  },
  "conflicts": [
    "other_voting_restriction:PASSAGE_CONFLICT"
  ],
  "reconciliation_for_field": []
}
```

## VALIDATION / TRAINED_LAYA / 192427e9aa3ca6f904eb505ac724d3c90e8eba48b9c676788a55d6e407fcb195 / other_voting_restriction

```text
[Message EL0206C | MT564]
Broker service update: the institutional ballot channel is now available for this agenda.
This is solely a cash-distribution advice; it offers no meeting ballot and no shareholder vote.
No requirement for a voting lock on the position applies.
No requirement for a compulsory attorney mandate applies.
No requirement for mandatory meeting registration applies.
No requirement for identification of the underlying owner applies.
No requirement for a custodial holding statement applies.
No requirement for a requirement to cast all votes identically applies.
No requirement for recall of lent securities applies.
No requirement for an in-person-only voting condition applies.


[Message EL0206D | MT568]
Please retain the replacement edition for operational reconciliation. Earlier notification conditions are superseded.

```

```json
{
  "truth": "NO",
  "prediction": {
    "value": "UNKNOWN",
    "scores": {},
    "native_score": null,
    "confidence": null,
    "source": "REGISTERED_LAYA_PASSAGES",
    "evidence": [],
    "aggregation_reason": "CURRENT_PASSAGE_CONFLICT_OR_DISTINCT_VOTING_ROUTES"
  },
  "whole_notice_scores": {
    "YES": 0.4683,
    "NO": 0.4513,
    "UNKNOWN": 0.0804
  },
  "passage_scores": [
    {
      "text": "[Message EL0206C | MT564]",
      "state": "UNKNOWN",
      "native_value": "NO",
      "scores": {
        "YES": 0.2579,
        "NO": 0.6784,
        "UNKNOWN": 0.0636
      },
      "score": 0.6784,
      "margin": 0.4205,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "Broker service update: the institutional ballot channel is now available for this agenda.",
      "state": "UNKNOWN",
      "native_value": "NO",
      "scores": {
        "YES": 0.4009,
        "NO": 0.5341,
        "UNKNOWN": 0.065
      },
      "score": 0.5341,
      "margin": 0.13320000000000004,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "This is solely a cash-distribution advice; it offers no meeting ballot and no shareholder vote.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.7233,
        "NO": 0.2397,
        "UNKNOWN": 0.037
      },
      "score": 0.7233,
      "margin": 0.48360000000000003,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for a voting lock on the position applies.",
      "state": "NEGATIVE",
      "native_value": "NO",
      "scores": {
        "YES": 0.3462,
        "NO": 0.6097,
        "UNKNOWN": 0.0441
      },
      "score": 0.6097,
      "margin": 0.2635,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for a compulsory attorney mandate applies.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.554,
        "NO": 0.3869,
        "UNKNOWN": 0.0591
      },
      "score": 0.554,
      "margin": 0.16710000000000003,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for mandatory meeting registration applies.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.5881,
        "NO": 0.3641,
        "UNKNOWN": 0.0478
      },
      "score": 0.5881,
      "margin": 0.22399999999999998,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for identification of the underlying owner applies.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.7306,
        "NO": 0.221,
        "UNKNOWN": 0.0484
      },
      "score": 0.7306,
      "margin": 0.5096,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for a custodial holding statement applies.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.6657,
        "NO": 0.2841,
        "UNKNOWN": 0.0502
      },
      "score": 0.6657,
      "margin": 0.38159999999999994,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for a requirement to cast all votes identically applies.",
      "state": "NEGATIVE",
      "native_value": "NO",
      "scores": {
        "YES": 0.3537,
        "NO": 0.6118,
        "UNKNOWN": 0.0345
      },
      "score": 0.6118,
      "margin": 0.2581,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for recall of lent securities applies.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.6418,
        "NO": 0.3127,
        "UNKNOWN": 0.0454
      },
      "score": 0.6418,
      "margin": 0.32910000000000006,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for an in-person-only voting condition applies.",
      "state": "NEGATIVE",
      "native_value": "NO",
      "scores": {
        "YES": 0.1626,
        "NO": 0.7841,
        "UNKNOWN": 0.0533
      },
      "score": 0.7841,
      "margin": 0.6215,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "[Message EL0206D | MT568]",
      "state": "UNKNOWN",
      "native_value": "NO",
      "scores": {
        "YES": 0.2428,
        "NO": 0.7054,
        "UNKNOWN": 0.0518
      },
      "score": 0.7054,
      "margin": 0.4626,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "Please retain the replacement edition for operational reconciliation.",
      "state": "UNKNOWN",
      "native_value": "NO",
      "scores": {
        "YES": 0.2761,
        "NO": 0.648,
        "UNKNOWN": 0.0759
      },
      "score": 0.648,
      "margin": 0.3719,
      "historical": false,
      "supersession": true,
      "conditional": false
    },
    {
      "text": "Earlier notification conditions are superseded.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.5653,
        "NO": 0.3643,
        "UNKNOWN": 0.0704
      },
      "score": 0.5653,
      "margin": 0.201,
      "historical": false,
      "supersession": true,
      "conditional": false
    }
  ],
  "escalation": {
    "escalated": false,
    "requested_predicates": [
      "votability",
      "share_blocking",
      "poa_required",
      "registration_required",
      "beneficial_owner_disclosure_required",
      "holding_confirmation_required",
      "split_voting_restricted",
      "securities_lending_recall_required",
      "other_voting_restriction"
    ],
    "reasons": {
      "votability": [
        "LOW_RAW_SCORE",
        "LOW_MARGIN"
      ],
      "share_blocking": [
        "LOW_RAW_SCORE"
      ],
      "poa_required": [
        "LOW_RAW_SCORE",
        "LOW_MARGIN",
        "EVIDENCE_UNAVAILABLE"
      ],
      "registration_required": [
        "LOW_RAW_SCORE"
      ],
      "beneficial_owner_disclosure_required": [
        "LOW_RAW_SCORE"
      ],
      "holding_confirmation_required": [
        "UNKNOWN",
        "LOW_RAW_SCORE",
        "LOW_MARGIN",
        "EVIDENCE_UNAVAILABLE"
      ],
      "split_voting_restricted": [
        "UNKNOWN",
        "LOW_RAW_SCORE",
        "LOW_MARGIN",
        "EVIDENCE_UNAVAILABLE"
      ],
      "securities_lending_recall_required": [
        "LOW_RAW_SCORE"
      ],
      "other_voting_restriction": [
        "UNKNOWN",
        "PASSAGE_CONFLICT",
        "LOW_RAW_SCORE",
        "LOW_MARGIN",
        "EVIDENCE_UNAVAILABLE"
      ]
    }
  },
  "conflicts": [
    "other_voting_restriction:PASSAGE_CONFLICT"
  ],
  "reconciliation_for_field": []
}
```

## VALIDATION / TRAINED_LAYA / 255328bb369bd44fa7cb0a788d797be6085e4bdab88a810f35f8b14469f269d2 / votability

```text
[Message EL0107C | MT564]
Issuer secretariat memorandum concerning arrangements for the forthcoming extraordinary assembly.
Participation may become possible, but the agent has not established whether this holder can vote.
For this vote, voting-related immobilisation is required.
The receiving agent has not resolved whether an obligatory power-of-attorney document is required for this vote.
No requirement for a required voter registration form applies.
No requirement for beneficial-owner disclosure applies.
For this vote, documentary confirmation of ownership is required.
No requirement for a ban on splitting voting instructions applies.
No requirement for retrieval of loaned voting positions applies.
No requirement for a mandatory paper-only ballot applies.


[Message EL0107D | MT568]
Please retain the replacement edition for operational reconciliation. Earlier notification conditions are superseded.

```

```json
{
  "truth": "UNCERTAIN",
  "prediction": {
    "value": "NOT_VOTABLE",
    "scores": {
      "VOTABLE": 0.1913,
      "NOT_VOTABLE": 0.5411,
      "UNCERTAIN": 0.2676
    },
    "native_score": 0.5411,
    "confidence": null,
    "source": "REGISTERED_LAYA_WHOLE_NOTICE",
    "evidence": [
      {
        "valid": true,
        "normalisation": "identity",
        "text": "[Message EL0107C | MT564]",
        "start": 0,
        "end": 25,
        "source": "MATCHING_NATIVE_PASSAGE"
      }
    ]
  },
  "whole_notice_scores": null,
  "passage_scores": [],
  "escalation": {
    "escalated": false,
    "requested_predicates": [
      "votability",
      "share_blocking",
      "poa_required",
      "registration_required",
      "beneficial_owner_disclosure_required",
      "holding_confirmation_required",
      "split_voting_restricted",
      "securities_lending_recall_required",
      "other_voting_restriction"
    ],
    "reasons": {
      "votability": [
        "LOW_RAW_SCORE",
        "LOW_MARGIN"
      ],
      "share_blocking": [
        "LOW_RAW_SCORE"
      ],
      "poa_required": [
        "UNKNOWN",
        "LOW_RAW_SCORE",
        "LOW_MARGIN",
        "EVIDENCE_UNAVAILABLE"
      ],
      "registration_required": [
        "LOW_RAW_SCORE"
      ],
      "beneficial_owner_disclosure_required": [
        "LOW_RAW_SCORE"
      ],
      "holding_confirmation_required": [
        "LOW_RAW_SCORE"
      ],
      "split_voting_restricted": [
        "LOW_RAW_SCORE"
      ],
      "securities_lending_recall_required": [
        "LOW_RAW_SCORE"
      ],
      "other_voting_restriction": [
        "LOW_RAW_SCORE"
      ]
    }
  },
  "conflicts": [],
  "reconciliation_for_field": []
}
```

## VALIDATION / TRAINED_LAYA / 255328bb369bd44fa7cb0a788d797be6085e4bdab88a810f35f8b14469f269d2 / registration_required

```text
[Message EL0107C | MT564]
Issuer secretariat memorandum concerning arrangements for the forthcoming extraordinary assembly.
Participation may become possible, but the agent has not established whether this holder can vote.
For this vote, voting-related immobilisation is required.
The receiving agent has not resolved whether an obligatory power-of-attorney document is required for this vote.
No requirement for a required voter registration form applies.
No requirement for beneficial-owner disclosure applies.
For this vote, documentary confirmation of ownership is required.
No requirement for a ban on splitting voting instructions applies.
No requirement for retrieval of loaned voting positions applies.
No requirement for a mandatory paper-only ballot applies.


[Message EL0107D | MT568]
Please retain the replacement edition for operational reconciliation. Earlier notification conditions are superseded.

```

```json
{
  "truth": "NO",
  "prediction": {
    "value": "YES",
    "scores": {
      "YES": 0.8479,
      "NO": 0.082,
      "UNKNOWN": 0.0701
    },
    "native_score": 0.8479,
    "confidence": null,
    "source": "REGISTERED_LAYA_PASSAGES",
    "evidence": [
      {
        "valid": true,
        "text": "The receiving agent has not resolved whether an obligatory power-of-attorney document is required for this vote.",
        "start": 281,
        "end": 393,
        "source": "NATIVE_LAYA_PASSAGE_WITH_DETERMINISTIC_SCOPE"
      }
    ],
    "aggregation_reason": "STRONG_CURRENT_RELEVANT_EVIDENCE"
  },
  "whole_notice_scores": {
    "YES": 0.1461,
    "NO": 0.8218,
    "UNKNOWN": 0.032
  },
  "passage_scores": [
    {
      "text": "[Message EL0107C | MT564]",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.4683,
        "NO": 0.3075,
        "UNKNOWN": 0.2242
      },
      "score": 0.4683,
      "margin": 0.1608,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "Issuer secretariat memorandum concerning arrangements for the forthcoming extraordinary assembly.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.6038,
        "NO": 0.3606,
        "UNKNOWN": 0.0355
      },
      "score": 0.6038,
      "margin": 0.24320000000000003,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "Participation may become possible, but the agent has not established whether this holder can vote.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.6385,
        "NO": 0.2578,
        "UNKNOWN": 0.1037
      },
      "score": 0.6385,
      "margin": 0.3807,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "For this vote, voting-related immobilisation is required.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.5601,
        "NO": 0.3592,
        "UNKNOWN": 0.0807
      },
      "score": 0.5601,
      "margin": 0.20090000000000002,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "The receiving agent has not resolved whether an obligatory power-of-attorney document is required for this vote.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.8479,
        "NO": 0.082,
        "UNKNOWN": 0.0701
      },
      "score": 0.8479,
      "margin": 0.7659,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for a required voter registration form applies.",
      "state": "NEGATIVE",
      "native_value": "NO",
      "scores": {
        "YES": 0.3223,
        "NO": 0.6322,
        "UNKNOWN": 0.0455
      },
      "score": 0.6322,
      "margin": 0.3099,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for beneficial-owner disclosure applies.",
      "state": "UNKNOWN",
      "native_value": "NO",
      "scores": {
        "YES": 0.3614,
        "NO": 0.5935,
        "UNKNOWN": 0.0451
      },
      "score": 0.5935,
      "margin": 0.23210000000000003,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "For this vote, documentary confirmation of ownership is required.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.8133,
        "NO": 0.129,
        "UNKNOWN": 0.0577
      },
      "score": 0.8133,
      "margin": 0.6843,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for a ban on splitting voting instructions applies.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.8032,
        "NO": 0.1731,
        "UNKNOWN": 0.0237
      },
      "score": 0.8032,
      "margin": 0.6301,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for retrieval of loaned voting positions applies.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.5694,
        "NO": 0.3459,
        "UNKNOWN": 0.0847
      },
      "score": 0.5694,
      "margin": 0.22350000000000003,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for a mandatory paper-only ballot applies.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.624,
        "NO": 0.3461,
        "UNKNOWN": 0.0299
      },
      "score": 0.624,
      "margin": 0.2779,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "[Message EL0107D | MT568]",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.4165,
        "NO": 0.3356,
        "UNKNOWN": 0.2478
      },
      "score": 0.4165,
      "margin": 0.08089999999999997,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "Please retain the replacement edition for operational reconciliation.",
      "state": "UNKNOWN",
      "native_value": "NO",
      "scores": {
        "YES": 0.3889,
        "NO": 0.5066,
        "UNKNOWN": 0.1045
      },
      "score": 0.5066,
      "margin": 0.11770000000000003,
      "historical": false,
      "supersession": true,
      "conditional": false
    },
    {
      "text": "Earlier notification conditions are superseded.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.597,
        "NO": 0.3291,
        "UNKNOWN": 0.0739
      },
      "score": 0.597,
      "margin": 0.26789999999999997,
      "historical": false,
      "supersession": true,
      "conditional": false
    }
  ],
  "escalation": {
    "escalated": false,
    "requested_predicates": [
      "votability",
      "share_blocking",
      "poa_required",
      "registration_required",
      "beneficial_owner_disclosure_required",
      "holding_confirmation_required",
      "split_voting_restricted",
      "securities_lending_recall_required",
      "other_voting_restriction"
    ],
    "reasons": {
      "votability": [
        "LOW_RAW_SCORE",
        "LOW_MARGIN"
      ],
      "share_blocking": [
        "LOW_RAW_SCORE"
      ],
      "poa_required": [
        "UNKNOWN",
        "LOW_RAW_SCORE",
        "LOW_MARGIN",
        "EVIDENCE_UNAVAILABLE"
      ],
      "registration_required": [
        "LOW_RAW_SCORE"
      ],
      "beneficial_owner_disclosure_required": [
        "LOW_RAW_SCORE"
      ],
      "holding_confirmation_required": [
        "LOW_RAW_SCORE"
      ],
      "split_voting_restricted": [
        "LOW_RAW_SCORE"
      ],
      "securities_lending_recall_required": [
        "LOW_RAW_SCORE"
      ],
      "other_voting_restriction": [
        "LOW_RAW_SCORE"
      ]
    }
  },
  "conflicts": [],
  "reconciliation_for_field": []
}
```

## VALIDATION / TRAINED_LAYA / 255328bb369bd44fa7cb0a788d797be6085e4bdab88a810f35f8b14469f269d2 / split_voting_restricted

```text
[Message EL0107C | MT564]
Issuer secretariat memorandum concerning arrangements for the forthcoming extraordinary assembly.
Participation may become possible, but the agent has not established whether this holder can vote.
For this vote, voting-related immobilisation is required.
The receiving agent has not resolved whether an obligatory power-of-attorney document is required for this vote.
No requirement for a required voter registration form applies.
No requirement for beneficial-owner disclosure applies.
For this vote, documentary confirmation of ownership is required.
No requirement for a ban on splitting voting instructions applies.
No requirement for retrieval of loaned voting positions applies.
No requirement for a mandatory paper-only ballot applies.


[Message EL0107D | MT568]
Please retain the replacement edition for operational reconciliation. Earlier notification conditions are superseded.

```

```json
{
  "truth": "NO",
  "prediction": {
    "value": "YES",
    "scores": {
      "YES": 0.8776,
      "NO": 0.0942,
      "UNKNOWN": 0.0282
    },
    "native_score": 0.8776,
    "confidence": null,
    "source": "REGISTERED_LAYA_PASSAGES",
    "evidence": [
      {
        "valid": true,
        "text": "No requirement for a ban on splitting voting instructions applies.",
        "start": 579,
        "end": 645,
        "source": "NATIVE_LAYA_PASSAGE_WITH_DETERMINISTIC_SCOPE"
      }
    ],
    "aggregation_reason": "STRONG_CURRENT_RELEVANT_EVIDENCE"
  },
  "whole_notice_scores": {
    "YES": 0.2907,
    "NO": 0.6729,
    "UNKNOWN": 0.0363
  },
  "passage_scores": [
    {
      "text": "[Message EL0107C | MT564]",
      "state": "UNKNOWN",
      "native_value": "NO",
      "scores": {
        "YES": 0.2059,
        "NO": 0.4621,
        "UNKNOWN": 0.332
      },
      "score": 0.4621,
      "margin": 0.1301,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "Issuer secretariat memorandum concerning arrangements for the forthcoming extraordinary assembly.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.6891,
        "NO": 0.2824,
        "UNKNOWN": 0.0285
      },
      "score": 0.6891,
      "margin": 0.40670000000000006,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "Participation may become possible, but the agent has not established whether this holder can vote.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.4281,
        "NO": 0.3666,
        "UNKNOWN": 0.2053
      },
      "score": 0.4281,
      "margin": 0.0615,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "For this vote, voting-related immobilisation is required.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.739,
        "NO": 0.1797,
        "UNKNOWN": 0.0813
      },
      "score": 0.739,
      "margin": 0.5593,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "The receiving agent has not resolved whether an obligatory power-of-attorney document is required for this vote.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.7723,
        "NO": 0.1186,
        "UNKNOWN": 0.1091
      },
      "score": 0.7723,
      "margin": 0.6537,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for a required voter registration form applies.",
      "state": "UNKNOWN",
      "native_value": "NO",
      "scores": {
        "YES": 0.4632,
        "NO": 0.4702,
        "UNKNOWN": 0.0666
      },
      "score": 0.4702,
      "margin": 0.007000000000000006,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for beneficial-owner disclosure applies.",
      "state": "UNKNOWN",
      "native_value": "NO",
      "scores": {
        "YES": 0.1339,
        "NO": 0.7214,
        "UNKNOWN": 0.1447
      },
      "score": 0.7214,
      "margin": 0.5767,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "For this vote, documentary confirmation of ownership is required.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.7301,
        "NO": 0.1693,
        "UNKNOWN": 0.1006
      },
      "score": 0.7301,
      "margin": 0.5608,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for a ban on splitting voting instructions applies.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.8776,
        "NO": 0.0942,
        "UNKNOWN": 0.0282
      },
      "score": 0.8776,
      "margin": 0.7834000000000001,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for retrieval of loaned voting positions applies.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.5739,
        "NO": 0.3204,
        "UNKNOWN": 0.1057
      },
      "score": 0.5739,
      "margin": 0.25349999999999995,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for a mandatory paper-only ballot applies.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.513,
        "NO": 0.4345,
        "UNKNOWN": 0.0525
      },
      "score": 0.513,
      "margin": 0.07850000000000001,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "[Message EL0107D | MT568]",
      "state": "UNKNOWN",
      "native_value": "NO",
      "scores": {
        "YES": 0.1092,
        "NO": 0.6218,
        "UNKNOWN": 0.269
      },
      "score": 0.6218,
      "margin": 0.3528,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "Please retain the replacement edition for operational reconciliation.",
      "state": "UNKNOWN",
      "native_value": "NO",
      "scores": {
        "YES": 0.1878,
        "NO": 0.7297,
        "UNKNOWN": 0.0824
      },
      "score": 0.7297,
      "margin": 0.5419,
      "historical": false,
      "supersession": true,
      "conditional": false
    },
    {
      "text": "Earlier notification conditions are superseded.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.4973,
        "NO": 0.3914,
        "UNKNOWN": 0.1113
      },
      "score": 0.4973,
      "margin": 0.1059,
      "historical": false,
      "supersession": true,
      "conditional": false
    }
  ],
  "escalation": {
    "escalated": false,
    "requested_predicates": [
      "votability",
      "share_blocking",
      "poa_required",
      "registration_required",
      "beneficial_owner_disclosure_required",
      "holding_confirmation_required",
      "split_voting_restricted",
      "securities_lending_recall_required",
      "other_voting_restriction"
    ],
    "reasons": {
      "votability": [
        "LOW_RAW_SCORE",
        "LOW_MARGIN"
      ],
      "share_blocking": [
        "LOW_RAW_SCORE"
      ],
      "poa_required": [
        "UNKNOWN",
        "LOW_RAW_SCORE",
        "LOW_MARGIN",
        "EVIDENCE_UNAVAILABLE"
      ],
      "registration_required": [
        "LOW_RAW_SCORE"
      ],
      "beneficial_owner_disclosure_required": [
        "LOW_RAW_SCORE"
      ],
      "holding_confirmation_required": [
        "LOW_RAW_SCORE"
      ],
      "split_voting_restricted": [
        "LOW_RAW_SCORE"
      ],
      "securities_lending_recall_required": [
        "LOW_RAW_SCORE"
      ],
      "other_voting_restriction": [
        "LOW_RAW_SCORE"
      ]
    }
  },
  "conflicts": [],
  "reconciliation_for_field": []
}
```

## VALIDATION / TRAINED_LAYA / 255328bb369bd44fa7cb0a788d797be6085e4bdab88a810f35f8b14469f269d2 / securities_lending_recall_required

```text
[Message EL0107C | MT564]
Issuer secretariat memorandum concerning arrangements for the forthcoming extraordinary assembly.
Participation may become possible, but the agent has not established whether this holder can vote.
For this vote, voting-related immobilisation is required.
The receiving agent has not resolved whether an obligatory power-of-attorney document is required for this vote.
No requirement for a required voter registration form applies.
No requirement for beneficial-owner disclosure applies.
For this vote, documentary confirmation of ownership is required.
No requirement for a ban on splitting voting instructions applies.
No requirement for retrieval of loaned voting positions applies.
No requirement for a mandatory paper-only ballot applies.


[Message EL0107D | MT568]
Please retain the replacement edition for operational reconciliation. Earlier notification conditions are superseded.

```

```json
{
  "truth": "NO",
  "prediction": {
    "value": "YES",
    "scores": {
      "YES": 0.7864,
      "NO": 0.1765,
      "UNKNOWN": 0.0371
    },
    "native_score": 0.7864,
    "confidence": null,
    "source": "REGISTERED_LAYA_PASSAGES",
    "evidence": [
      {
        "valid": true,
        "text": "No requirement for a ban on splitting voting instructions applies.",
        "start": 579,
        "end": 645,
        "source": "NATIVE_LAYA_PASSAGE_WITH_DETERMINISTIC_SCOPE"
      }
    ],
    "aggregation_reason": "STRONG_CURRENT_RELEVANT_EVIDENCE"
  },
  "whole_notice_scores": {
    "YES": 0.2336,
    "NO": 0.7251,
    "UNKNOWN": 0.0413
  },
  "passage_scores": [
    {
      "text": "[Message EL0107C | MT564]",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.537,
        "NO": 0.3061,
        "UNKNOWN": 0.157
      },
      "score": 0.537,
      "margin": 0.23090000000000005,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "Issuer secretariat memorandum concerning arrangements for the forthcoming extraordinary assembly.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.5404,
        "NO": 0.3777,
        "UNKNOWN": 0.0819
      },
      "score": 0.5404,
      "margin": 0.1627,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "Participation may become possible, but the agent has not established whether this holder can vote.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.5427,
        "NO": 0.3087,
        "UNKNOWN": 0.1486
      },
      "score": 0.5427,
      "margin": 0.23399999999999999,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "For this vote, voting-related immobilisation is required.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.7666,
        "NO": 0.1556,
        "UNKNOWN": 0.0779
      },
      "score": 0.7666,
      "margin": 0.611,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "The receiving agent has not resolved whether an obligatory power-of-attorney document is required for this vote.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.7425,
        "NO": 0.1586,
        "UNKNOWN": 0.0988
      },
      "score": 0.7425,
      "margin": 0.5839000000000001,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for a required voter registration form applies.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.5264,
        "NO": 0.3962,
        "UNKNOWN": 0.0774
      },
      "score": 0.5264,
      "margin": 0.13019999999999998,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for beneficial-owner disclosure applies.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.5311,
        "NO": 0.3741,
        "UNKNOWN": 0.0948
      },
      "score": 0.5311,
      "margin": 0.15700000000000003,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "For this vote, documentary confirmation of ownership is required.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.7744,
        "NO": 0.1381,
        "UNKNOWN": 0.0874
      },
      "score": 0.7744,
      "margin": 0.6363,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for a ban on splitting voting instructions applies.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.7864,
        "NO": 0.1765,
        "UNKNOWN": 0.0371
      },
      "score": 0.7864,
      "margin": 0.6099,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for retrieval of loaned voting positions applies.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.6289,
        "NO": 0.2869,
        "UNKNOWN": 0.0842
      },
      "score": 0.6289,
      "margin": 0.342,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for a mandatory paper-only ballot applies.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.7254,
        "NO": 0.2372,
        "UNKNOWN": 0.0374
      },
      "score": 0.7254,
      "margin": 0.4882000000000001,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "[Message EL0107D | MT568]",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.5104,
        "NO": 0.3234,
        "UNKNOWN": 0.1661
      },
      "score": 0.5104,
      "margin": 0.18699999999999994,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "Please retain the replacement edition for operational reconciliation.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.5096,
        "NO": 0.375,
        "UNKNOWN": 0.1154
      },
      "score": 0.5096,
      "margin": 0.13460000000000005,
      "historical": false,
      "supersession": true,
      "conditional": false
    },
    {
      "text": "Earlier notification conditions are superseded.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.6434,
        "NO": 0.2655,
        "UNKNOWN": 0.0912
      },
      "score": 0.6434,
      "margin": 0.37789999999999996,
      "historical": false,
      "supersession": true,
      "conditional": false
    }
  ],
  "escalation": {
    "escalated": false,
    "requested_predicates": [
      "votability",
      "share_blocking",
      "poa_required",
      "registration_required",
      "beneficial_owner_disclosure_required",
      "holding_confirmation_required",
      "split_voting_restricted",
      "securities_lending_recall_required",
      "other_voting_restriction"
    ],
    "reasons": {
      "votability": [
        "LOW_RAW_SCORE",
        "LOW_MARGIN"
      ],
      "share_blocking": [
        "LOW_RAW_SCORE"
      ],
      "poa_required": [
        "UNKNOWN",
        "LOW_RAW_SCORE",
        "LOW_MARGIN",
        "EVIDENCE_UNAVAILABLE"
      ],
      "registration_required": [
        "LOW_RAW_SCORE"
      ],
      "beneficial_owner_disclosure_required": [
        "LOW_RAW_SCORE"
      ],
      "holding_confirmation_required": [
        "LOW_RAW_SCORE"
      ],
      "split_voting_restricted": [
        "LOW_RAW_SCORE"
      ],
      "securities_lending_recall_required": [
        "LOW_RAW_SCORE"
      ],
      "other_voting_restriction": [
        "LOW_RAW_SCORE"
      ]
    }
  },
  "conflicts": [],
  "reconciliation_for_field": []
}
```

## VALIDATION / TRAINED_LAYA / 25150120b9a9e92a98ab8b33fb003cab98a2ec6b4230ec908fda5c15d2bbc7d7 / share_blocking

```text
[Message EL0105C | MT564]
Issuer secretariat memorandum concerning arrangements for the forthcoming extraordinary assembly.
The current agenda is open for shareholder voting instructions.
No requirement for voting-related immobilisation applies.
No requirement for an obligatory power-of-attorney document applies.
For this vote, a required voter registration form is required.
No requirement for beneficial-owner disclosure applies.
No requirement for documentary confirmation of ownership applies.
No requirement for a ban on splitting voting instructions applies.
For this vote, retrieval of loaned voting positions is required.
No requirement for a mandatory paper-only ballot applies.


[Message EL0105D | MT568]
Please retain the replacement edition for operational reconciliation. Earlier notification conditions are superseded.

```

```json
{
  "truth": "NO",
  "prediction": {
    "value": "YES",
    "scores": {
      "YES": 0.9632,
      "NO": 0.0123,
      "UNKNOWN": 0.0244
    },
    "native_score": 0.9632,
    "confidence": null,
    "source": "REGISTERED_LAYA_PASSAGES",
    "evidence": [
      {
        "valid": true,
        "text": "Earlier notification conditions are superseded.",
        "start": 788,
        "end": 835,
        "source": "NATIVE_LAYA_PASSAGE_WITH_DETERMINISTIC_SCOPE"
      }
    ],
    "aggregation_reason": "STRONG_CURRENT_RELEVANT_EVIDENCE"
  },
  "whole_notice_scores": {
    "YES": 0.5452,
    "NO": 0.3448,
    "UNKNOWN": 0.11
  },
  "passage_scores": [
    {
      "text": "[Message EL0105C | MT564]",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.9335,
        "NO": 0.0295,
        "UNKNOWN": 0.0369
      },
      "score": 0.9335,
      "margin": 0.8966,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "Issuer secretariat memorandum concerning arrangements for the forthcoming extraordinary assembly.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.8912,
        "NO": 0.0831,
        "UNKNOWN": 0.0257
      },
      "score": 0.8912,
      "margin": 0.8081,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "The current agenda is open for shareholder voting instructions.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.7926,
        "NO": 0.1291,
        "UNKNOWN": 0.0782
      },
      "score": 0.7926,
      "margin": 0.6635,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for voting-related immobilisation applies.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.9416,
        "NO": 0.0445,
        "UNKNOWN": 0.0138
      },
      "score": 0.9416,
      "margin": 0.8971,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for an obligatory power-of-attorney document applies.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.8869,
        "NO": 0.0734,
        "UNKNOWN": 0.0397
      },
      "score": 0.8869,
      "margin": 0.8135,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "For this vote, a required voter registration form is required.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.9322,
        "NO": 0.0298,
        "UNKNOWN": 0.038
      },
      "score": 0.9322,
      "margin": 0.8942,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for beneficial-owner disclosure applies.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.8787,
        "NO": 0.0756,
        "UNKNOWN": 0.0457
      },
      "score": 0.8787,
      "margin": 0.8031,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for documentary confirmation of ownership applies.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.9257,
        "NO": 0.0501,
        "UNKNOWN": 0.0242
      },
      "score": 0.9257,
      "margin": 0.8755999999999999,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for a ban on splitting voting instructions applies.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.9567,
        "NO": 0.0233,
        "UNKNOWN": 0.02
      },
      "score": 0.9567,
      "margin": 0.9334,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "For this vote, retrieval of loaned voting positions is required.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.8708,
        "NO": 0.0624,
        "UNKNOWN": 0.0668
      },
      "score": 0.8708,
      "margin": 0.804,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for a mandatory paper-only ballot applies.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.8633,
        "NO": 0.0911,
        "UNKNOWN": 0.0457
      },
      "score": 0.8633,
      "margin": 0.7722,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "[Message EL0105D | MT568]",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.9334,
        "NO": 0.0319,
        "UNKNOWN": 0.0347
      },
      "score": 0.9334,
      "margin": 0.8987,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "Please retain the replacement edition for operational reconciliation.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.9104,
        "NO": 0.053,
        "UNKNOWN": 0.0366
      },
      "score": 0.9104,
      "margin": 0.8573999999999999,
      "historical": false,
      "supersession": true,
      "conditional": false
    },
    {
      "text": "Earlier notification conditions are superseded.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.9632,
        "NO": 0.0123,
        "UNKNOWN": 0.0244
      },
      "score": 0.9632,
      "margin": 0.9388,
      "historical": false,
      "supersession": true,
      "conditional": false
    }
  ],
  "escalation": {
    "escalated": false,
    "requested_predicates": [
      "share_blocking",
      "poa_required",
      "registration_required",
      "beneficial_owner_disclosure_required",
      "holding_confirmation_required",
      "split_voting_restricted",
      "securities_lending_recall_required",
      "other_voting_restriction"
    ],
    "reasons": {
      "share_blocking": [
        "LOW_RAW_SCORE"
      ],
      "poa_required": [
        "LOW_RAW_SCORE"
      ],
      "registration_required": [
        "LOW_RAW_SCORE"
      ],
      "beneficial_owner_disclosure_required": [
        "LOW_RAW_SCORE"
      ],
      "holding_confirmation_required": [
        "LOW_RAW_SCORE"
      ],
      "split_voting_restricted": [
        "LOW_RAW_SCORE"
      ],
      "securities_lending_recall_required": [
        "LOW_RAW_SCORE"
      ],
      "other_voting_restriction": [
        "LOW_RAW_SCORE"
      ]
    }
  },
  "conflicts": [
    "votability:STRUCTURE_SEMANTIC_CONFLICT"
  ],
  "reconciliation_for_field": []
}
```

## VALIDATION / TRAINED_LAYA / 25150120b9a9e92a98ab8b33fb003cab98a2ec6b4230ec908fda5c15d2bbc7d7 / split_voting_restricted

```text
[Message EL0105C | MT564]
Issuer secretariat memorandum concerning arrangements for the forthcoming extraordinary assembly.
The current agenda is open for shareholder voting instructions.
No requirement for voting-related immobilisation applies.
No requirement for an obligatory power-of-attorney document applies.
For this vote, a required voter registration form is required.
No requirement for beneficial-owner disclosure applies.
No requirement for documentary confirmation of ownership applies.
No requirement for a ban on splitting voting instructions applies.
For this vote, retrieval of loaned voting positions is required.
No requirement for a mandatory paper-only ballot applies.


[Message EL0105D | MT568]
Please retain the replacement edition for operational reconciliation. Earlier notification conditions are superseded.

```

```json
{
  "truth": "NO",
  "prediction": {
    "value": "YES",
    "scores": {
      "YES": 0.8776,
      "NO": 0.0942,
      "UNKNOWN": 0.0282
    },
    "native_score": 0.8776,
    "confidence": null,
    "source": "REGISTERED_LAYA_PASSAGES",
    "evidence": [
      {
        "valid": true,
        "text": "No requirement for a ban on splitting voting instructions applies.",
        "start": 500,
        "end": 566,
        "source": "NATIVE_LAYA_PASSAGE_WITH_DETERMINISTIC_SCOPE"
      }
    ],
    "aggregation_reason": "STRONG_CURRENT_RELEVANT_EVIDENCE"
  },
  "whole_notice_scores": {
    "YES": 0.4047,
    "NO": 0.5216,
    "UNKNOWN": 0.0737
  },
  "passage_scores": [
    {
      "text": "[Message EL0105C | MT564]",
      "state": "UNKNOWN",
      "native_value": "NO",
      "scores": {
        "YES": 0.1967,
        "NO": 0.4941,
        "UNKNOWN": 0.3092
      },
      "score": 0.4941,
      "margin": 0.1849,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "Issuer secretariat memorandum concerning arrangements for the forthcoming extraordinary assembly.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.6891,
        "NO": 0.2824,
        "UNKNOWN": 0.0285
      },
      "score": 0.6891,
      "margin": 0.40670000000000006,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "The current agenda is open for shareholder voting instructions.",
      "state": "UNKNOWN",
      "native_value": "NO",
      "scores": {
        "YES": 0.1997,
        "NO": 0.6685,
        "UNKNOWN": 0.1318
      },
      "score": 0.6685,
      "margin": 0.4688,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for voting-related immobilisation applies.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.5293,
        "NO": 0.3713,
        "UNKNOWN": 0.0993
      },
      "score": 0.5293,
      "margin": 0.15799999999999997,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for an obligatory power-of-attorney document applies.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.6168,
        "NO": 0.3047,
        "UNKNOWN": 0.0785
      },
      "score": 0.6168,
      "margin": 0.3121,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "For this vote, a required voter registration form is required.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.8131,
        "NO": 0.1179,
        "UNKNOWN": 0.069
      },
      "score": 0.8131,
      "margin": 0.6952,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for beneficial-owner disclosure applies.",
      "state": "UNKNOWN",
      "native_value": "NO",
      "scores": {
        "YES": 0.1339,
        "NO": 0.7214,
        "UNKNOWN": 0.1447
      },
      "score": 0.7214,
      "margin": 0.5767,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for documentary confirmation of ownership applies.",
      "state": "UNKNOWN",
      "native_value": "NO",
      "scores": {
        "YES": 0.3582,
        "NO": 0.5515,
        "UNKNOWN": 0.0903
      },
      "score": 0.5515,
      "margin": 0.19329999999999997,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for a ban on splitting voting instructions applies.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.8776,
        "NO": 0.0942,
        "UNKNOWN": 0.0282
      },
      "score": 0.8776,
      "margin": 0.7834000000000001,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "For this vote, retrieval of loaned voting positions is required.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.6635,
        "NO": 0.229,
        "UNKNOWN": 0.1074
      },
      "score": 0.6635,
      "margin": 0.4345,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for a mandatory paper-only ballot applies.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.513,
        "NO": 0.4345,
        "UNKNOWN": 0.0525
      },
      "score": 0.513,
      "margin": 0.07850000000000001,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "[Message EL0105D | MT568]",
      "state": "UNKNOWN",
      "native_value": "NO",
      "scores": {
        "YES": 0.1502,
        "NO": 0.5727,
        "UNKNOWN": 0.2771
      },
      "score": 0.5727,
      "margin": 0.2956,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "Please retain the replacement edition for operational reconciliation.",
      "state": "UNKNOWN",
      "native_value": "NO",
      "scores": {
        "YES": 0.1878,
        "NO": 0.7297,
        "UNKNOWN": 0.0824
      },
      "score": 0.7297,
      "margin": 0.5419,
      "historical": false,
      "supersession": true,
      "conditional": false
    },
    {
      "text": "Earlier notification conditions are superseded.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.4973,
        "NO": 0.3914,
        "UNKNOWN": 0.1113
      },
      "score": 0.4973,
      "margin": 0.1059,
      "historical": false,
      "supersession": true,
      "conditional": false
    }
  ],
  "escalation": {
    "escalated": false,
    "requested_predicates": [
      "share_blocking",
      "poa_required",
      "registration_required",
      "beneficial_owner_disclosure_required",
      "holding_confirmation_required",
      "split_voting_restricted",
      "securities_lending_recall_required",
      "other_voting_restriction"
    ],
    "reasons": {
      "share_blocking": [
        "LOW_RAW_SCORE"
      ],
      "poa_required": [
        "LOW_RAW_SCORE"
      ],
      "registration_required": [
        "LOW_RAW_SCORE"
      ],
      "beneficial_owner_disclosure_required": [
        "LOW_RAW_SCORE"
      ],
      "holding_confirmation_required": [
        "LOW_RAW_SCORE"
      ],
      "split_voting_restricted": [
        "LOW_RAW_SCORE"
      ],
      "securities_lending_recall_required": [
        "LOW_RAW_SCORE"
      ],
      "other_voting_restriction": [
        "LOW_RAW_SCORE"
      ]
    }
  },
  "conflicts": [
    "votability:STRUCTURE_SEMANTIC_CONFLICT"
  ],
  "reconciliation_for_field": []
}
```

## VALIDATION / TRAINED_LAYA / 2414be60f4dff3cc46dcf385c748749f7c7c3dc05ef8f904052ec9797bdc2f19 / share_blocking

```text
[Message EL0104C | MT564]
Issuer secretariat memorandum concerning arrangements for the forthcoming extraordinary assembly.
The current agenda is open for shareholder voting instructions.
No requirement for voting-related immobilisation applies.
No requirement for an obligatory power-of-attorney document applies.
No requirement for a required voter registration form applies.
For this vote, beneficial-owner disclosure is required.
No requirement for documentary confirmation of ownership applies.
No requirement for a ban on splitting voting instructions applies.
No requirement for retrieval of loaned voting positions applies.
For this vote, a mandatory paper-only ballot is required.


[Message EL0104D | MT568]
Please retain the replacement edition for operational reconciliation. Earlier notification conditions are superseded.

```

```json
{
  "truth": "NO",
  "prediction": {
    "value": "YES",
    "scores": {
      "YES": 0.9632,
      "NO": 0.0123,
      "UNKNOWN": 0.0244
    },
    "native_score": 0.9632,
    "confidence": null,
    "source": "REGISTERED_LAYA_PASSAGES",
    "evidence": [
      {
        "valid": true,
        "text": "Earlier notification conditions are superseded.",
        "start": 788,
        "end": 835,
        "source": "NATIVE_LAYA_PASSAGE_WITH_DETERMINISTIC_SCOPE"
      }
    ],
    "aggregation_reason": "STRONG_CURRENT_RELEVANT_EVIDENCE"
  },
  "whole_notice_scores": {
    "YES": 0.6147,
    "NO": 0.3133,
    "UNKNOWN": 0.072
  },
  "passage_scores": [
    {
      "text": "[Message EL0104C | MT564]",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.9324,
        "NO": 0.0286,
        "UNKNOWN": 0.039
      },
      "score": 0.9324,
      "margin": 0.8934,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "Issuer secretariat memorandum concerning arrangements for the forthcoming extraordinary assembly.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.8912,
        "NO": 0.0831,
        "UNKNOWN": 0.0257
      },
      "score": 0.8912,
      "margin": 0.8081,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "The current agenda is open for shareholder voting instructions.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.7926,
        "NO": 0.1291,
        "UNKNOWN": 0.0782
      },
      "score": 0.7926,
      "margin": 0.6635,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for voting-related immobilisation applies.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.9416,
        "NO": 0.0445,
        "UNKNOWN": 0.0138
      },
      "score": 0.9416,
      "margin": 0.8971,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for an obligatory power-of-attorney document applies.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.8869,
        "NO": 0.0734,
        "UNKNOWN": 0.0397
      },
      "score": 0.8869,
      "margin": 0.8135,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for a required voter registration form applies.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.7931,
        "NO": 0.1483,
        "UNKNOWN": 0.0586
      },
      "score": 0.7931,
      "margin": 0.6448,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "For this vote, beneficial-owner disclosure is required.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.8825,
        "NO": 0.0705,
        "UNKNOWN": 0.047
      },
      "score": 0.8825,
      "margin": 0.8119999999999999,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for documentary confirmation of ownership applies.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.9257,
        "NO": 0.0501,
        "UNKNOWN": 0.0242
      },
      "score": 0.9257,
      "margin": 0.8755999999999999,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for a ban on splitting voting instructions applies.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.9567,
        "NO": 0.0233,
        "UNKNOWN": 0.02
      },
      "score": 0.9567,
      "margin": 0.9334,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for retrieval of loaned voting positions applies.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.8292,
        "NO": 0.1229,
        "UNKNOWN": 0.0479
      },
      "score": 0.8292,
      "margin": 0.7063,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "For this vote, a mandatory paper-only ballot is required.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.9478,
        "NO": 0.0264,
        "UNKNOWN": 0.0258
      },
      "score": 0.9478,
      "margin": 0.9214,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "[Message EL0104D | MT568]",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.9353,
        "NO": 0.0282,
        "UNKNOWN": 0.0365
      },
      "score": 0.9353,
      "margin": 0.8988,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "Please retain the replacement edition for operational reconciliation.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.9104,
        "NO": 0.053,
        "UNKNOWN": 0.0366
      },
      "score": 0.9104,
      "margin": 0.8573999999999999,
      "historical": false,
      "supersession": true,
      "conditional": false
    },
    {
      "text": "Earlier notification conditions are superseded.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.9632,
        "NO": 0.0123,
        "UNKNOWN": 0.0244
      },
      "score": 0.9632,
      "margin": 0.9388,
      "historical": false,
      "supersession": true,
      "conditional": false
    }
  ],
  "escalation": {
    "escalated": false,
    "requested_predicates": [
      "share_blocking",
      "poa_required",
      "registration_required",
      "beneficial_owner_disclosure_required",
      "holding_confirmation_required",
      "split_voting_restricted",
      "securities_lending_recall_required",
      "other_voting_restriction"
    ],
    "reasons": {
      "share_blocking": [
        "LOW_RAW_SCORE"
      ],
      "poa_required": [
        "LOW_RAW_SCORE"
      ],
      "registration_required": [
        "LOW_RAW_SCORE"
      ],
      "beneficial_owner_disclosure_required": [
        "LOW_RAW_SCORE",
        "LOW_MARGIN"
      ],
      "holding_confirmation_required": [
        "LOW_RAW_SCORE"
      ],
      "split_voting_restricted": [
        "LOW_RAW_SCORE"
      ],
      "securities_lending_recall_required": [
        "LOW_RAW_SCORE"
      ],
      "other_voting_restriction": [
        "UNKNOWN",
        "LOW_RAW_SCORE",
        "LOW_MARGIN",
        "EVIDENCE_UNAVAILABLE"
      ]
    }
  },
  "conflicts": [
    "votability:STRUCTURE_SEMANTIC_CONFLICT"
  ],
  "reconciliation_for_field": []
}
```

## VALIDATION / TRAINED_LAYA / 2414be60f4dff3cc46dcf385c748749f7c7c3dc05ef8f904052ec9797bdc2f19 / registration_required

```text
[Message EL0104C | MT564]
Issuer secretariat memorandum concerning arrangements for the forthcoming extraordinary assembly.
The current agenda is open for shareholder voting instructions.
No requirement for voting-related immobilisation applies.
No requirement for an obligatory power-of-attorney document applies.
No requirement for a required voter registration form applies.
For this vote, beneficial-owner disclosure is required.
No requirement for documentary confirmation of ownership applies.
No requirement for a ban on splitting voting instructions applies.
No requirement for retrieval of loaned voting positions applies.
For this vote, a mandatory paper-only ballot is required.


[Message EL0104D | MT568]
Please retain the replacement edition for operational reconciliation. Earlier notification conditions are superseded.

```

```json
{
  "truth": "NO",
  "prediction": {
    "value": "YES",
    "scores": {
      "YES": 0.871,
      "NO": 0.1085,
      "UNKNOWN": 0.0206
    },
    "native_score": 0.871,
    "confidence": null,
    "source": "REGISTERED_LAYA_PASSAGES",
    "evidence": [
      {
        "valid": true,
        "text": "For this vote, a mandatory paper-only ballot is required.",
        "start": 632,
        "end": 689,
        "source": "NATIVE_LAYA_PASSAGE_WITH_DETERMINISTIC_SCOPE"
      }
    ],
    "aggregation_reason": "STRONG_CURRENT_RELEVANT_EVIDENCE"
  },
  "whole_notice_scores": {
    "YES": 0.217,
    "NO": 0.6692,
    "UNKNOWN": 0.1137
  },
  "passage_scores": [
    {
      "text": "[Message EL0104C | MT564]",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.4962,
        "NO": 0.2837,
        "UNKNOWN": 0.2201
      },
      "score": 0.4962,
      "margin": 0.21249999999999997,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "Issuer secretariat memorandum concerning arrangements for the forthcoming extraordinary assembly.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.6038,
        "NO": 0.3606,
        "UNKNOWN": 0.0355
      },
      "score": 0.6038,
      "margin": 0.24320000000000003,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "The current agenda is open for shareholder voting instructions.",
      "state": "UNKNOWN",
      "native_value": "NO",
      "scores": {
        "YES": 0.1833,
        "NO": 0.7071,
        "UNKNOWN": 0.1096
      },
      "score": 0.7071,
      "margin": 0.5237999999999999,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for voting-related immobilisation applies.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.7715,
        "NO": 0.1901,
        "UNKNOWN": 0.0383
      },
      "score": 0.7715,
      "margin": 0.5813999999999999,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for an obligatory power-of-attorney document applies.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.7594,
        "NO": 0.2077,
        "UNKNOWN": 0.0329
      },
      "score": 0.7594,
      "margin": 0.5517,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for a required voter registration form applies.",
      "state": "NEGATIVE",
      "native_value": "NO",
      "scores": {
        "YES": 0.3223,
        "NO": 0.6322,
        "UNKNOWN": 0.0455
      },
      "score": 0.6322,
      "margin": 0.3099,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "For this vote, beneficial-owner disclosure is required.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.5295,
        "NO": 0.388,
        "UNKNOWN": 0.0824
      },
      "score": 0.5295,
      "margin": 0.14149999999999996,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for documentary confirmation of ownership applies.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.5764,
        "NO": 0.3823,
        "UNKNOWN": 0.0413
      },
      "score": 0.5764,
      "margin": 0.19410000000000005,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for a ban on splitting voting instructions applies.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.8032,
        "NO": 0.1731,
        "UNKNOWN": 0.0237
      },
      "score": 0.8032,
      "margin": 0.6301,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for retrieval of loaned voting positions applies.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.5694,
        "NO": 0.3459,
        "UNKNOWN": 0.0847
      },
      "score": 0.5694,
      "margin": 0.22350000000000003,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "For this vote, a mandatory paper-only ballot is required.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.871,
        "NO": 0.1085,
        "UNKNOWN": 0.0206
      },
      "score": 0.871,
      "margin": 0.7625,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "[Message EL0104D | MT568]",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.4486,
        "NO": 0.3003,
        "UNKNOWN": 0.2511
      },
      "score": 0.4486,
      "margin": 0.1483,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "Please retain the replacement edition for operational reconciliation.",
      "state": "UNKNOWN",
      "native_value": "NO",
      "scores": {
        "YES": 0.3889,
        "NO": 0.5066,
        "UNKNOWN": 0.1045
      },
      "score": 0.5066,
      "margin": 0.11770000000000003,
      "historical": false,
      "supersession": true,
      "conditional": false
    },
    {
      "text": "Earlier notification conditions are superseded.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.597,
        "NO": 0.3291,
        "UNKNOWN": 0.0739
      },
      "score": 0.597,
      "margin": 0.26789999999999997,
      "historical": false,
      "supersession": true,
      "conditional": false
    }
  ],
  "escalation": {
    "escalated": false,
    "requested_predicates": [
      "share_blocking",
      "poa_required",
      "registration_required",
      "beneficial_owner_disclosure_required",
      "holding_confirmation_required",
      "split_voting_restricted",
      "securities_lending_recall_required",
      "other_voting_restriction"
    ],
    "reasons": {
      "share_blocking": [
        "LOW_RAW_SCORE"
      ],
      "poa_required": [
        "LOW_RAW_SCORE"
      ],
      "registration_required": [
        "LOW_RAW_SCORE"
      ],
      "beneficial_owner_disclosure_required": [
        "LOW_RAW_SCORE",
        "LOW_MARGIN"
      ],
      "holding_confirmation_required": [
        "LOW_RAW_SCORE"
      ],
      "split_voting_restricted": [
        "LOW_RAW_SCORE"
      ],
      "securities_lending_recall_required": [
        "LOW_RAW_SCORE"
      ],
      "other_voting_restriction": [
        "UNKNOWN",
        "LOW_RAW_SCORE",
        "LOW_MARGIN",
        "EVIDENCE_UNAVAILABLE"
      ]
    }
  },
  "conflicts": [
    "votability:STRUCTURE_SEMANTIC_CONFLICT"
  ],
  "reconciliation_for_field": []
}
```

## VALIDATION / TRAINED_LAYA / 2414be60f4dff3cc46dcf385c748749f7c7c3dc05ef8f904052ec9797bdc2f19 / split_voting_restricted

```text
[Message EL0104C | MT564]
Issuer secretariat memorandum concerning arrangements for the forthcoming extraordinary assembly.
The current agenda is open for shareholder voting instructions.
No requirement for voting-related immobilisation applies.
No requirement for an obligatory power-of-attorney document applies.
No requirement for a required voter registration form applies.
For this vote, beneficial-owner disclosure is required.
No requirement for documentary confirmation of ownership applies.
No requirement for a ban on splitting voting instructions applies.
No requirement for retrieval of loaned voting positions applies.
For this vote, a mandatory paper-only ballot is required.


[Message EL0104D | MT568]
Please retain the replacement edition for operational reconciliation. Earlier notification conditions are superseded.

```

```json
{
  "truth": "NO",
  "prediction": {
    "value": "YES",
    "scores": {
      "YES": 0.8776,
      "NO": 0.0942,
      "UNKNOWN": 0.0282
    },
    "native_score": 0.8776,
    "confidence": null,
    "source": "REGISTERED_LAYA_PASSAGES",
    "evidence": [
      {
        "valid": true,
        "text": "No requirement for a ban on splitting voting instructions applies.",
        "start": 500,
        "end": 566,
        "source": "NATIVE_LAYA_PASSAGE_WITH_DETERMINISTIC_SCOPE"
      }
    ],
    "aggregation_reason": "STRONG_CURRENT_RELEVANT_EVIDENCE"
  },
  "whole_notice_scores": {
    "YES": 0.426,
    "NO": 0.5101,
    "UNKNOWN": 0.0639
  },
  "passage_scores": [
    {
      "text": "[Message EL0104C | MT564]",
      "state": "UNKNOWN",
      "native_value": "NO",
      "scores": {
        "YES": 0.2329,
        "NO": 0.4417,
        "UNKNOWN": 0.3254
      },
      "score": 0.4417,
      "margin": 0.11629999999999996,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "Issuer secretariat memorandum concerning arrangements for the forthcoming extraordinary assembly.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.6891,
        "NO": 0.2824,
        "UNKNOWN": 0.0285
      },
      "score": 0.6891,
      "margin": 0.40670000000000006,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "The current agenda is open for shareholder voting instructions.",
      "state": "UNKNOWN",
      "native_value": "NO",
      "scores": {
        "YES": 0.1997,
        "NO": 0.6685,
        "UNKNOWN": 0.1318
      },
      "score": 0.6685,
      "margin": 0.4688,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for voting-related immobilisation applies.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.5293,
        "NO": 0.3713,
        "UNKNOWN": 0.0993
      },
      "score": 0.5293,
      "margin": 0.15799999999999997,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for an obligatory power-of-attorney document applies.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.6168,
        "NO": 0.3047,
        "UNKNOWN": 0.0785
      },
      "score": 0.6168,
      "margin": 0.3121,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for a required voter registration form applies.",
      "state": "UNKNOWN",
      "native_value": "NO",
      "scores": {
        "YES": 0.4632,
        "NO": 0.4702,
        "UNKNOWN": 0.0666
      },
      "score": 0.4702,
      "margin": 0.007000000000000006,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "For this vote, beneficial-owner disclosure is required.",
      "state": "UNKNOWN",
      "native_value": "NO",
      "scores": {
        "YES": 0.3864,
        "NO": 0.5276,
        "UNKNOWN": 0.086
      },
      "score": 0.5276,
      "margin": 0.14119999999999994,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for documentary confirmation of ownership applies.",
      "state": "UNKNOWN",
      "native_value": "NO",
      "scores": {
        "YES": 0.3582,
        "NO": 0.5515,
        "UNKNOWN": 0.0903
      },
      "score": 0.5515,
      "margin": 0.19329999999999997,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for a ban on splitting voting instructions applies.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.8776,
        "NO": 0.0942,
        "UNKNOWN": 0.0282
      },
      "score": 0.8776,
      "margin": 0.7834000000000001,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for retrieval of loaned voting positions applies.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.5739,
        "NO": 0.3204,
        "UNKNOWN": 0.1057
      },
      "score": 0.5739,
      "margin": 0.25349999999999995,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "For this vote, a mandatory paper-only ballot is required.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.8258,
        "NO": 0.1202,
        "UNKNOWN": 0.054
      },
      "score": 0.8258,
      "margin": 0.7056,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "[Message EL0104D | MT568]",
      "state": "UNKNOWN",
      "native_value": "NO",
      "scores": {
        "YES": 0.1755,
        "NO": 0.5197,
        "UNKNOWN": 0.3048
      },
      "score": 0.5197,
      "margin": 0.21490000000000004,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "Please retain the replacement edition for operational reconciliation.",
      "state": "UNKNOWN",
      "native_value": "NO",
      "scores": {
        "YES": 0.1878,
        "NO": 0.7297,
        "UNKNOWN": 0.0824
      },
      "score": 0.7297,
      "margin": 0.5419,
      "historical": false,
      "supersession": true,
      "conditional": false
    },
    {
      "text": "Earlier notification conditions are superseded.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.4973,
        "NO": 0.3914,
        "UNKNOWN": 0.1113
      },
      "score": 0.4973,
      "margin": 0.1059,
      "historical": false,
      "supersession": true,
      "conditional": false
    }
  ],
  "escalation": {
    "escalated": false,
    "requested_predicates": [
      "share_blocking",
      "poa_required",
      "registration_required",
      "beneficial_owner_disclosure_required",
      "holding_confirmation_required",
      "split_voting_restricted",
      "securities_lending_recall_required",
      "other_voting_restriction"
    ],
    "reasons": {
      "share_blocking": [
        "LOW_RAW_SCORE"
      ],
      "poa_required": [
        "LOW_RAW_SCORE"
      ],
      "registration_required": [
        "LOW_RAW_SCORE"
      ],
      "beneficial_owner_disclosure_required": [
        "LOW_RAW_SCORE",
        "LOW_MARGIN"
      ],
      "holding_confirmation_required": [
        "LOW_RAW_SCORE"
      ],
      "split_voting_restricted": [
        "LOW_RAW_SCORE"
      ],
      "securities_lending_recall_required": [
        "LOW_RAW_SCORE"
      ],
      "other_voting_restriction": [
        "UNKNOWN",
        "LOW_RAW_SCORE",
        "LOW_MARGIN",
        "EVIDENCE_UNAVAILABLE"
      ]
    }
  },
  "conflicts": [
    "votability:STRUCTURE_SEMANTIC_CONFLICT"
  ],
  "reconciliation_for_field": []
}
```

## VALIDATION / TRAINED_LAYA / 2414be60f4dff3cc46dcf385c748749f7c7c3dc05ef8f904052ec9797bdc2f19 / securities_lending_recall_required

```text
[Message EL0104C | MT564]
Issuer secretariat memorandum concerning arrangements for the forthcoming extraordinary assembly.
The current agenda is open for shareholder voting instructions.
No requirement for voting-related immobilisation applies.
No requirement for an obligatory power-of-attorney document applies.
No requirement for a required voter registration form applies.
For this vote, beneficial-owner disclosure is required.
No requirement for documentary confirmation of ownership applies.
No requirement for a ban on splitting voting instructions applies.
No requirement for retrieval of loaned voting positions applies.
For this vote, a mandatory paper-only ballot is required.


[Message EL0104D | MT568]
Please retain the replacement edition for operational reconciliation. Earlier notification conditions are superseded.

```

```json
{
  "truth": "NO",
  "prediction": {
    "value": "YES",
    "scores": {
      "YES": 0.8894,
      "NO": 0.0868,
      "UNKNOWN": 0.0237
    },
    "native_score": 0.8894,
    "confidence": null,
    "source": "REGISTERED_LAYA_PASSAGES",
    "evidence": [
      {
        "valid": true,
        "text": "For this vote, a mandatory paper-only ballot is required.",
        "start": 632,
        "end": 689,
        "source": "NATIVE_LAYA_PASSAGE_WITH_DETERMINISTIC_SCOPE"
      }
    ],
    "aggregation_reason": "STRONG_CURRENT_RELEVANT_EVIDENCE"
  },
  "whole_notice_scores": {
    "YES": 0.2468,
    "NO": 0.6654,
    "UNKNOWN": 0.0877
  },
  "passage_scores": [
    {
      "text": "[Message EL0104C | MT564]",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.5459,
        "NO": 0.3059,
        "UNKNOWN": 0.1483
      },
      "score": 0.5459,
      "margin": 0.24000000000000005,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "Issuer secretariat memorandum concerning arrangements for the forthcoming extraordinary assembly.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.5404,
        "NO": 0.3777,
        "UNKNOWN": 0.0819
      },
      "score": 0.5404,
      "margin": 0.1627,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "The current agenda is open for shareholder voting instructions.",
      "state": "UNKNOWN",
      "native_value": "NO",
      "scores": {
        "YES": 0.31,
        "NO": 0.552,
        "UNKNOWN": 0.1381
      },
      "score": 0.552,
      "margin": 0.24200000000000005,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for voting-related immobilisation applies.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.7555,
        "NO": 0.1932,
        "UNKNOWN": 0.0513
      },
      "score": 0.7555,
      "margin": 0.5622999999999999,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for an obligatory power-of-attorney document applies.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.6798,
        "NO": 0.2593,
        "UNKNOWN": 0.0609
      },
      "score": 0.6798,
      "margin": 0.4205,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for a required voter registration form applies.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.5264,
        "NO": 0.3962,
        "UNKNOWN": 0.0774
      },
      "score": 0.5264,
      "margin": 0.13019999999999998,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "For this vote, beneficial-owner disclosure is required.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.616,
        "NO": 0.2656,
        "UNKNOWN": 0.1184
      },
      "score": 0.616,
      "margin": 0.3504,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for documentary confirmation of ownership applies.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.622,
        "NO": 0.2995,
        "UNKNOWN": 0.0785
      },
      "score": 0.622,
      "margin": 0.3225,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for a ban on splitting voting instructions applies.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.7864,
        "NO": 0.1765,
        "UNKNOWN": 0.0371
      },
      "score": 0.7864,
      "margin": 0.6099,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for retrieval of loaned voting positions applies.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.6289,
        "NO": 0.2869,
        "UNKNOWN": 0.0842
      },
      "score": 0.6289,
      "margin": 0.342,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "For this vote, a mandatory paper-only ballot is required.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.8894,
        "NO": 0.0868,
        "UNKNOWN": 0.0237
      },
      "score": 0.8894,
      "margin": 0.8026,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "[Message EL0104D | MT568]",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.5127,
        "NO": 0.3105,
        "UNKNOWN": 0.1768
      },
      "score": 0.5127,
      "margin": 0.20220000000000005,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "Please retain the replacement edition for operational reconciliation.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.5096,
        "NO": 0.375,
        "UNKNOWN": 0.1154
      },
      "score": 0.5096,
      "margin": 0.13460000000000005,
      "historical": false,
      "supersession": true,
      "conditional": false
    },
    {
      "text": "Earlier notification conditions are superseded.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.6434,
        "NO": 0.2655,
        "UNKNOWN": 0.0912
      },
      "score": 0.6434,
      "margin": 0.37789999999999996,
      "historical": false,
      "supersession": true,
      "conditional": false
    }
  ],
  "escalation": {
    "escalated": false,
    "requested_predicates": [
      "share_blocking",
      "poa_required",
      "registration_required",
      "beneficial_owner_disclosure_required",
      "holding_confirmation_required",
      "split_voting_restricted",
      "securities_lending_recall_required",
      "other_voting_restriction"
    ],
    "reasons": {
      "share_blocking": [
        "LOW_RAW_SCORE"
      ],
      "poa_required": [
        "LOW_RAW_SCORE"
      ],
      "registration_required": [
        "LOW_RAW_SCORE"
      ],
      "beneficial_owner_disclosure_required": [
        "LOW_RAW_SCORE",
        "LOW_MARGIN"
      ],
      "holding_confirmation_required": [
        "LOW_RAW_SCORE"
      ],
      "split_voting_restricted": [
        "LOW_RAW_SCORE"
      ],
      "securities_lending_recall_required": [
        "LOW_RAW_SCORE"
      ],
      "other_voting_restriction": [
        "UNKNOWN",
        "LOW_RAW_SCORE",
        "LOW_MARGIN",
        "EVIDENCE_UNAVAILABLE"
      ]
    }
  },
  "conflicts": [
    "votability:STRUCTURE_SEMANTIC_CONFLICT"
  ],
  "reconciliation_for_field": []
}
```

## VALIDATION / TRAINED_LAYA / 2414be60f4dff3cc46dcf385c748749f7c7c3dc05ef8f904052ec9797bdc2f19 / other_voting_restriction

```text
[Message EL0104C | MT564]
Issuer secretariat memorandum concerning arrangements for the forthcoming extraordinary assembly.
The current agenda is open for shareholder voting instructions.
No requirement for voting-related immobilisation applies.
No requirement for an obligatory power-of-attorney document applies.
No requirement for a required voter registration form applies.
For this vote, beneficial-owner disclosure is required.
No requirement for documentary confirmation of ownership applies.
No requirement for a ban on splitting voting instructions applies.
No requirement for retrieval of loaned voting positions applies.
For this vote, a mandatory paper-only ballot is required.


[Message EL0104D | MT568]
Please retain the replacement edition for operational reconciliation. Earlier notification conditions are superseded.

```

```json
{
  "truth": "YES",
  "prediction": {
    "value": "UNKNOWN",
    "scores": {},
    "native_score": null,
    "confidence": null,
    "source": "REGISTERED_LAYA_PASSAGES",
    "evidence": [],
    "aggregation_reason": "NO_STRONG_CURRENT_RELEVANT_STATEMENT"
  },
  "whole_notice_scores": {
    "YES": 0.2755,
    "NO": 0.626,
    "UNKNOWN": 0.0984
  },
  "passage_scores": [
    {
      "text": "[Message EL0104C | MT564]",
      "state": "UNKNOWN",
      "native_value": "NO",
      "scores": {
        "YES": 0.278,
        "NO": 0.6589,
        "UNKNOWN": 0.0631
      },
      "score": 0.6589,
      "margin": 0.3809,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "Issuer secretariat memorandum concerning arrangements for the forthcoming extraordinary assembly.",
      "state": "UNKNOWN",
      "native_value": "NO",
      "scores": {
        "YES": 0.357,
        "NO": 0.6124,
        "UNKNOWN": 0.0306
      },
      "score": 0.6124,
      "margin": 0.25540000000000007,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "The current agenda is open for shareholder voting instructions.",
      "state": "UNKNOWN",
      "native_value": "NO",
      "scores": {
        "YES": 0.242,
        "NO": 0.6778,
        "UNKNOWN": 0.0802
      },
      "score": 0.6778,
      "margin": 0.43579999999999997,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for voting-related immobilisation applies.",
      "state": "NEGATIVE",
      "native_value": "NO",
      "scores": {
        "YES": 0.4572,
        "NO": 0.4912,
        "UNKNOWN": 0.0517
      },
      "score": 0.4912,
      "margin": 0.03400000000000003,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for an obligatory power-of-attorney document applies.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.4857,
        "NO": 0.4527,
        "UNKNOWN": 0.0616
      },
      "score": 0.4857,
      "margin": 0.03300000000000003,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for a required voter registration form applies.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.4965,
        "NO": 0.4567,
        "UNKNOWN": 0.0468
      },
      "score": 0.4965,
      "margin": 0.0398,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "For this vote, beneficial-owner disclosure is required.",
      "state": "UNKNOWN",
      "native_value": "NO",
      "scores": {
        "YES": 0.4231,
        "NO": 0.501,
        "UNKNOWN": 0.0759
      },
      "score": 0.501,
      "margin": 0.07790000000000002,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for documentary confirmation of ownership applies.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.618,
        "NO": 0.3201,
        "UNKNOWN": 0.0619
      },
      "score": 0.618,
      "margin": 0.2979,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for a ban on splitting voting instructions applies.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.6466,
        "NO": 0.3255,
        "UNKNOWN": 0.0278
      },
      "score": 0.6466,
      "margin": 0.32109999999999994,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for retrieval of loaned voting positions applies.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.5354,
        "NO": 0.4241,
        "UNKNOWN": 0.0405
      },
      "score": 0.5354,
      "margin": 0.11130000000000001,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "For this vote, a mandatory paper-only ballot is required.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.6663,
        "NO": 0.2907,
        "UNKNOWN": 0.0429
      },
      "score": 0.6663,
      "margin": 0.3756,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "[Message EL0104D | MT568]",
      "state": "UNKNOWN",
      "native_value": "NO",
      "scores": {
        "YES": 0.2999,
        "NO": 0.6412,
        "UNKNOWN": 0.0589
      },
      "score": 0.6412,
      "margin": 0.3413,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "Please retain the replacement edition for operational reconciliation.",
      "state": "UNKNOWN",
      "native_value": "NO",
      "scores": {
        "YES": 0.2761,
        "NO": 0.648,
        "UNKNOWN": 0.0759
      },
      "score": 0.648,
      "margin": 0.3719,
      "historical": false,
      "supersession": true,
      "conditional": false
    },
    {
      "text": "Earlier notification conditions are superseded.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.5653,
        "NO": 0.3643,
        "UNKNOWN": 0.0704
      },
      "score": 0.5653,
      "margin": 0.201,
      "historical": false,
      "supersession": true,
      "conditional": false
    }
  ],
  "escalation": {
    "escalated": false,
    "requested_predicates": [
      "share_blocking",
      "poa_required",
      "registration_required",
      "beneficial_owner_disclosure_required",
      "holding_confirmation_required",
      "split_voting_restricted",
      "securities_lending_recall_required",
      "other_voting_restriction"
    ],
    "reasons": {
      "share_blocking": [
        "LOW_RAW_SCORE"
      ],
      "poa_required": [
        "LOW_RAW_SCORE"
      ],
      "registration_required": [
        "LOW_RAW_SCORE"
      ],
      "beneficial_owner_disclosure_required": [
        "LOW_RAW_SCORE",
        "LOW_MARGIN"
      ],
      "holding_confirmation_required": [
        "LOW_RAW_SCORE"
      ],
      "split_voting_restricted": [
        "LOW_RAW_SCORE"
      ],
      "securities_lending_recall_required": [
        "LOW_RAW_SCORE"
      ],
      "other_voting_restriction": [
        "UNKNOWN",
        "LOW_RAW_SCORE",
        "LOW_MARGIN",
        "EVIDENCE_UNAVAILABLE"
      ]
    }
  },
  "conflicts": [
    "votability:STRUCTURE_SEMANTIC_CONFLICT"
  ],
  "reconciliation_for_field": []
}
```

## VALIDATION / TRAINED_LAYA / 192427e9aa3ca6f904eb505ac724d3c90e8eba48b9c676788a55d6e407fcb195 / expected_final_status

```text
[Message EL0206C | MT564]
Broker service update: the institutional ballot channel is now available for this agenda.
This is solely a cash-distribution advice; it offers no meeting ballot and no shareholder vote.
No requirement for a voting lock on the position applies.
No requirement for a compulsory attorney mandate applies.
No requirement for mandatory meeting registration applies.
No requirement for identification of the underlying owner applies.
No requirement for a custodial holding statement applies.
No requirement for a requirement to cast all votes identically applies.
No requirement for recall of lent securities applies.
No requirement for an in-person-only voting condition applies.


[Message EL0206D | MT568]
Please retain the replacement edition for operational reconciliation. Earlier notification conditions are superseded.

```
```json
{
  "truth": "NOT_VOTABLE",
  "prediction": "UNCERTAIN_MANUAL_REVIEW",
  "decision": {
    "classification": "UNCERTAIN_MANUAL_REVIEW",
    "rule": "R1 unresolved conflicts",
    "rule_version": "semantic-decision-2",
    "manual_review_required": true,
    "automation_enabled": false,
    "review_reasons": [
      "other_voting_restriction:PASSAGE_CONFLICT",
      "Synthetic-only evaluation; customer quality gate not met"
    ]
  },
  "deadline": {
    "status": "OPEN",
    "comparisons": [
      {
        "source": "PROWIDE",
        "field_id": "prowide:9",
        "path": [
          "CAOPTN[1]"
        ],
        "deadline": {
          "iso": "2026-11-24T17:00:00+00:00",
          "offset_known": true,
          "precision": "SECOND"
        },
        "status": "OPEN",
        "field": {
          "components": [
            "RDDT",
            "20261124",
            "170000",
            "000",
            null,
            "00"
          ],
          "end": 226,
          "qualifier": "RDDT",
          "sequence_instance_path": [
            "CAOPTN[1]"
          ],
          "sequence_path": [
            "CAOPTN"
          ],
          "source": "PROWIDE",
          "source_text": ":98E::RDDT//20261124170000,000/00\n",
          "start": 192,
          "tag": "98E",
          "typed_field": "Field98E",
          "value": ":RDDT//20261124170000,000/00"
        }
      }
    ],
    "conflict": false,
    "source": "PROWIDE_COMPONENTS_DETERMINISTIC_COMPARISON",
    "reason": "Only RDDT is controlling. Bare local/date-only values require an agreed timezone profile; no UTC assumption."
  }
}
```

## VALIDATION / TRAINED_LAYA / 255328bb369bd44fa7cb0a788d797be6085e4bdab88a810f35f8b14469f269d2 / expected_final_status

```text
[Message EL0107C | MT564]
Issuer secretariat memorandum concerning arrangements for the forthcoming extraordinary assembly.
Participation may become possible, but the agent has not established whether this holder can vote.
For this vote, voting-related immobilisation is required.
The receiving agent has not resolved whether an obligatory power-of-attorney document is required for this vote.
No requirement for a required voter registration form applies.
No requirement for beneficial-owner disclosure applies.
For this vote, documentary confirmation of ownership is required.
No requirement for a ban on splitting voting instructions applies.
No requirement for retrieval of loaned voting positions applies.
No requirement for a mandatory paper-only ballot applies.


[Message EL0107D | MT568]
Please retain the replacement edition for operational reconciliation. Earlier notification conditions are superseded.

```
```json
{
  "truth": "UNCERTAIN_MANUAL_REVIEW",
  "prediction": "NOT_VOTABLE",
  "decision": {
    "classification": "NOT_VOTABLE",
    "rule": "R2 no current voting opportunity",
    "rule_version": "semantic-decision-2",
    "manual_review_required": true,
    "automation_enabled": false,
    "review_reasons": [
      "Synthetic-only evaluation; customer quality gate not met"
    ]
  },
  "deadline": {
    "status": "OPEN",
    "comparisons": [
      {
        "source": "PROWIDE",
        "field_id": "prowide:9",
        "path": [
          "CAOPTN[1]"
        ],
        "deadline": {
          "iso": "2026-11-24T17:00:00+00:00",
          "offset_known": true,
          "precision": "SECOND"
        },
        "status": "OPEN",
        "field": {
          "components": [
            "RDDT",
            "20261124",
            "170000",
            "000",
            null,
            "00"
          ],
          "end": 226,
          "qualifier": "RDDT",
          "sequence_instance_path": [
            "CAOPTN[1]"
          ],
          "sequence_path": [
            "CAOPTN"
          ],
          "source": "PROWIDE",
          "source_text": ":98E::RDDT//20261124170000,000/00\n",
          "start": 192,
          "tag": "98E",
          "typed_field": "Field98E",
          "value": ":RDDT//20261124170000,000/00"
        }
      }
    ],
    "conflict": false,
    "source": "PROWIDE_COMPONENTS_DETERMINISTIC_COMPARISON",
    "reason": "Only RDDT is controlling. Bare local/date-only values require an agreed timezone profile; no UTC assumption."
  }
}
```

## VALIDATION / TRAINED_LAYA / 25150120b9a9e92a98ab8b33fb003cab98a2ec6b4230ec908fda5c15d2bbc7d7 / expected_final_status

```text
[Message EL0105C | MT564]
Issuer secretariat memorandum concerning arrangements for the forthcoming extraordinary assembly.
The current agenda is open for shareholder voting instructions.
No requirement for voting-related immobilisation applies.
No requirement for an obligatory power-of-attorney document applies.
For this vote, a required voter registration form is required.
No requirement for beneficial-owner disclosure applies.
No requirement for documentary confirmation of ownership applies.
No requirement for a ban on splitting voting instructions applies.
For this vote, retrieval of loaned voting positions is required.
No requirement for a mandatory paper-only ballot applies.


[Message EL0105D | MT568]
Please retain the replacement edition for operational reconciliation. Earlier notification conditions are superseded.

```
```json
{
  "truth": "VOTABLE_WITH_RESTRICTION",
  "prediction": "UNCERTAIN_MANUAL_REVIEW",
  "decision": {
    "classification": "UNCERTAIN_MANUAL_REVIEW",
    "rule": "R1 unresolved conflicts",
    "rule_version": "semantic-decision-2",
    "manual_review_required": true,
    "automation_enabled": false,
    "review_reasons": [
      "votability:STRUCTURE_SEMANTIC_CONFLICT",
      "Synthetic-only evaluation; customer quality gate not met"
    ]
  },
  "deadline": {
    "status": "OPEN",
    "comparisons": [
      {
        "source": "PROWIDE",
        "field_id": "prowide:10",
        "path": [
          "CAOPTN[1]"
        ],
        "deadline": {
          "iso": "2026-11-24T17:00:00+00:00",
          "offset_known": true,
          "precision": "SECOND"
        },
        "status": "OPEN",
        "field": {
          "components": [
            "RDDT",
            "20261124",
            "170000",
            "000",
            null,
            "00"
          ],
          "end": 243,
          "qualifier": "RDDT",
          "sequence_instance_path": [
            "CAOPTN[1]"
          ],
          "sequence_path": [
            "CAOPTN"
          ],
          "source": "PROWIDE",
          "source_text": ":98E::RDDT//20261124170000,000/00\n",
          "start": 209,
          "tag": "98E",
          "typed_field": "Field98E",
          "value": ":RDDT//20261124170000,000/00"
        }
      }
    ],
    "conflict": false,
    "source": "PROWIDE_COMPONENTS_DETERMINISTIC_COMPARISON",
    "reason": "Only RDDT is controlling. Bare local/date-only values require an agreed timezone profile; no UTC assumption."
  }
}
```

## VALIDATION / TRAINED_LAYA / 2414be60f4dff3cc46dcf385c748749f7c7c3dc05ef8f904052ec9797bdc2f19 / expected_final_status

```text
[Message EL0104C | MT564]
Issuer secretariat memorandum concerning arrangements for the forthcoming extraordinary assembly.
The current agenda is open for shareholder voting instructions.
No requirement for voting-related immobilisation applies.
No requirement for an obligatory power-of-attorney document applies.
No requirement for a required voter registration form applies.
For this vote, beneficial-owner disclosure is required.
No requirement for documentary confirmation of ownership applies.
No requirement for a ban on splitting voting instructions applies.
No requirement for retrieval of loaned voting positions applies.
For this vote, a mandatory paper-only ballot is required.


[Message EL0104D | MT568]
Please retain the replacement edition for operational reconciliation. Earlier notification conditions are superseded.

```
```json
{
  "truth": "DEADLINE_PASSED",
  "prediction": "UNCERTAIN_MANUAL_REVIEW",
  "decision": {
    "classification": "UNCERTAIN_MANUAL_REVIEW",
    "rule": "R1 unresolved conflicts",
    "rule_version": "semantic-decision-2",
    "manual_review_required": true,
    "automation_enabled": false,
    "review_reasons": [
      "votability:STRUCTURE_SEMANTIC_CONFLICT",
      "Synthetic-only evaluation; customer quality gate not met"
    ]
  },
  "deadline": {
    "status": "PASSED",
    "comparisons": [
      {
        "source": "PROWIDE",
        "field_id": "prowide:10",
        "path": [
          "CAOPTN[1]"
        ],
        "deadline": {
          "iso": "2025-09-01T17:00:00+00:00",
          "offset_known": true,
          "precision": "SECOND"
        },
        "status": "PASSED",
        "field": {
          "components": [
            "RDDT",
            "20250901",
            "170000",
            "000",
            null,
            "00"
          ],
          "end": 243,
          "qualifier": "RDDT",
          "sequence_instance_path": [
            "CAOPTN[1]"
          ],
          "sequence_path": [
            "CAOPTN"
          ],
          "source": "PROWIDE",
          "source_text": ":98E::RDDT//20250901170000,000/00\n",
          "start": 209,
          "tag": "98E",
          "typed_field": "Field98E",
          "value": ":RDDT//20250901170000,000/00"
        }
      }
    ],
    "conflict": false,
    "source": "PROWIDE_COMPONENTS_DETERMINISTIC_COMPARISON",
    "reason": "Only RDDT is controlling. Bare local/date-only values require an agreed timezone profile; no UTC assumption."
  }
}
```

## VALIDATION / BASE_QWEN / 25150120b9a9e92a98ab8b33fb003cab98a2ec6b4230ec908fda5c15d2bbc7d7 / expected_final_status

```text
[Message EL0105C | MT564]
Issuer secretariat memorandum concerning arrangements for the forthcoming extraordinary assembly.
The current agenda is open for shareholder voting instructions.
No requirement for voting-related immobilisation applies.
No requirement for an obligatory power-of-attorney document applies.
For this vote, a required voter registration form is required.
No requirement for beneficial-owner disclosure applies.
No requirement for documentary confirmation of ownership applies.
No requirement for a ban on splitting voting instructions applies.
For this vote, retrieval of loaned voting positions is required.
No requirement for a mandatory paper-only ballot applies.


[Message EL0105D | MT568]
Please retain the replacement edition for operational reconciliation. Earlier notification conditions are superseded.

```
```json
{
  "truth": "VOTABLE_WITH_RESTRICTION",
  "prediction": "UNCERTAIN_MANUAL_REVIEW",
  "decision": {
    "classification": "UNCERTAIN_MANUAL_REVIEW",
    "rule": "R1 unresolved conflicts",
    "rule_version": "semantic-decision-2",
    "manual_review_required": true,
    "automation_enabled": false,
    "review_reasons": [
      "Message EL0105D states 'Earlier notification conditions are superseded' but does not specify which conditions or provide replacement terms, creating uncertainty about the final operative status of the conditions listed in EL0105C.",
      "Synthetic-only evaluation; customer quality gate not met"
    ]
  },
  "deadline": {
    "status": "OPEN",
    "comparisons": [
      {
        "source": "PROWIDE",
        "field_id": "prowide:10",
        "path": [
          "CAOPTN[1]"
        ],
        "deadline": {
          "iso": "2026-11-24T17:00:00+00:00",
          "offset_known": true,
          "precision": "SECOND"
        },
        "status": "OPEN",
        "field": {
          "components": [
            "RDDT",
            "20261124",
            "170000",
            "000",
            null,
            "00"
          ],
          "end": 243,
          "qualifier": "RDDT",
          "sequence_instance_path": [
            "CAOPTN[1]"
          ],
          "sequence_path": [
            "CAOPTN"
          ],
          "source": "PROWIDE",
          "source_text": ":98E::RDDT//20261124170000,000/00\n",
          "start": 209,
          "tag": "98E",
          "typed_field": "Field98E",
          "value": ":RDDT//20261124170000,000/00"
        }
      }
    ],
    "conflict": false,
    "source": "PROWIDE_COMPONENTS_DETERMINISTIC_COMPARISON",
    "reason": "Only RDDT is controlling. Bare local/date-only values require an agreed timezone profile; no UTC assumption."
  }
}
```

## VALIDATION / TRAINED_QWEN / 25150120b9a9e92a98ab8b33fb003cab98a2ec6b4230ec908fda5c15d2bbc7d7 / expected_final_status

```text
[Message EL0105C | MT564]
Issuer secretariat memorandum concerning arrangements for the forthcoming extraordinary assembly.
The current agenda is open for shareholder voting instructions.
No requirement for voting-related immobilisation applies.
No requirement for an obligatory power-of-attorney document applies.
For this vote, a required voter registration form is required.
No requirement for beneficial-owner disclosure applies.
No requirement for documentary confirmation of ownership applies.
No requirement for a ban on splitting voting instructions applies.
For this vote, retrieval of loaned voting positions is required.
No requirement for a mandatory paper-only ballot applies.


[Message EL0105D | MT568]
Please retain the replacement edition for operational reconciliation. Earlier notification conditions are superseded.

```
```json
{
  "truth": "VOTABLE_WITH_RESTRICTION",
  "prediction": "UNCERTAIN_MANUAL_REVIEW",
  "decision": {
    "classification": "UNCERTAIN_MANUAL_REVIEW",
    "rule": "R1 unresolved conflicts",
    "rule_version": "semantic-decision-2",
    "manual_review_required": true,
    "automation_enabled": false,
    "review_reasons": [
      "Message EL0105D states 'Earlier notification conditions are superseded' but does not specify which conditions or provide replacement terms, creating uncertainty about the final operative status of the conditions listed in EL0105C.",
      "Synthetic-only evaluation; customer quality gate not met"
    ]
  },
  "deadline": {
    "status": "OPEN",
    "comparisons": [
      {
        "source": "PROWIDE",
        "field_id": "prowide:10",
        "path": [
          "CAOPTN[1]"
        ],
        "deadline": {
          "iso": "2026-11-24T17:00:00+00:00",
          "offset_known": true,
          "precision": "SECOND"
        },
        "status": "OPEN",
        "field": {
          "components": [
            "RDDT",
            "20261124",
            "170000",
            "000",
            null,
            "00"
          ],
          "end": 243,
          "qualifier": "RDDT",
          "sequence_instance_path": [
            "CAOPTN[1]"
          ],
          "sequence_path": [
            "CAOPTN"
          ],
          "source": "PROWIDE",
          "source_text": ":98E::RDDT//20261124170000,000/00\n",
          "start": 209,
          "tag": "98E",
          "typed_field": "Field98E",
          "value": ":RDDT//20261124170000,000/00"
        }
      }
    ],
    "conflict": false,
    "source": "PROWIDE_COMPONENTS_DETERMINISTIC_COMPARISON",
    "reason": "Only RDDT is controlling. Bare local/date-only values require an agreed timezone profile; no UTC assumption."
  }
}
```

## VALIDATION / CASCADE_CONSERVATIVE / 192427e9aa3ca6f904eb505ac724d3c90e8eba48b9c676788a55d6e407fcb195 / share_blocking

```text
[Message EL0206C | MT564]
Broker service update: the institutional ballot channel is now available for this agenda.
This is solely a cash-distribution advice; it offers no meeting ballot and no shareholder vote.
No requirement for a voting lock on the position applies.
No requirement for a compulsory attorney mandate applies.
No requirement for mandatory meeting registration applies.
No requirement for identification of the underlying owner applies.
No requirement for a custodial holding statement applies.
No requirement for a requirement to cast all votes identically applies.
No requirement for recall of lent securities applies.
No requirement for an in-person-only voting condition applies.


[Message EL0206D | MT568]
Please retain the replacement edition for operational reconciliation. Earlier notification conditions are superseded.

```

```json
{
  "truth": "NO",
  "prediction": {
    "value": "UNKNOWN",
    "scores": {
      "YES": 0.9632,
      "NO": 0.0123,
      "UNKNOWN": 0.0244
    },
    "native_score": 0.9632,
    "confidence": null,
    "source": "UNRESOLVED_MODEL_DISAGREEMENT",
    "evidence": [
      {
        "valid": true,
        "text": "Earlier notification conditions are superseded.",
        "start": 799,
        "end": 846,
        "source": "NATIVE_LAYA_PASSAGE_WITH_DETERMINISTIC_SCOPE"
      }
    ],
    "aggregation_reason": "STRONG_CURRENT_RELEVANT_EVIDENCE"
  },
  "whole_notice_scores": {
    "YES": 0.8643,
    "NO": 0.0941,
    "UNKNOWN": 0.0416
  },
  "passage_scores": [
    {
      "text": "[Message EL0206C | MT564]",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.9274,
        "NO": 0.0274,
        "UNKNOWN": 0.0452
      },
      "score": 0.9274,
      "margin": 0.8822,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "Broker service update: the institutional ballot channel is now available for this agenda.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.858,
        "NO": 0.08,
        "UNKNOWN": 0.062
      },
      "score": 0.858,
      "margin": 0.778,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "This is solely a cash-distribution advice; it offers no meeting ballot and no shareholder vote.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.9437,
        "NO": 0.0315,
        "UNKNOWN": 0.0248
      },
      "score": 0.9437,
      "margin": 0.9122,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for a voting lock on the position applies.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.86,
        "NO": 0.0962,
        "UNKNOWN": 0.0438
      },
      "score": 0.86,
      "margin": 0.7638,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for a compulsory attorney mandate applies.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.9405,
        "NO": 0.0385,
        "UNKNOWN": 0.021
      },
      "score": 0.9405,
      "margin": 0.902,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for mandatory meeting registration applies.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.9214,
        "NO": 0.041,
        "UNKNOWN": 0.0376
      },
      "score": 0.9214,
      "margin": 0.8804,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for identification of the underlying owner applies.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.9292,
        "NO": 0.0368,
        "UNKNOWN": 0.0341
      },
      "score": 0.9292,
      "margin": 0.8924000000000001,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for a custodial holding statement applies.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.9021,
        "NO": 0.0575,
        "UNKNOWN": 0.0404
      },
      "score": 0.9021,
      "margin": 0.8446,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for a requirement to cast all votes identically applies.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.8764,
        "NO": 0.0703,
        "UNKNOWN": 0.0533
      },
      "score": 0.8764,
      "margin": 0.8060999999999999,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for recall of lent securities applies.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.9214,
        "NO": 0.0467,
        "UNKNOWN": 0.0319
      },
      "score": 0.9214,
      "margin": 0.8747,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for an in-person-only voting condition applies.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.5156,
        "NO": 0.3209,
        "UNKNOWN": 0.1634
      },
      "score": 0.5156,
      "margin": 0.19469999999999993,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "[Message EL0206D | MT568]",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.9297,
        "NO": 0.0283,
        "UNKNOWN": 0.042
      },
      "score": 0.9297,
      "margin": 0.8876999999999999,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "Please retain the replacement edition for operational reconciliation.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.9104,
        "NO": 0.053,
        "UNKNOWN": 0.0366
      },
      "score": 0.9104,
      "margin": 0.8573999999999999,
      "historical": false,
      "supersession": true,
      "conditional": false
    },
    {
      "text": "Earlier notification conditions are superseded.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.9632,
        "NO": 0.0123,
        "UNKNOWN": 0.0244
      },
      "score": 0.9632,
      "margin": 0.9388,
      "historical": false,
      "supersession": true,
      "conditional": false
    }
  ],
  "escalation": {
    "escalated": true,
    "requested_predicates": [
      "votability",
      "share_blocking",
      "poa_required",
      "registration_required",
      "beneficial_owner_disclosure_required",
      "holding_confirmation_required",
      "split_voting_restricted",
      "securities_lending_recall_required",
      "other_voting_restriction"
    ],
    "reasons": {
      "votability": [
        "LOW_RAW_SCORE",
        "LOW_MARGIN"
      ],
      "share_blocking": [
        "LOW_RAW_SCORE"
      ],
      "poa_required": [
        "LOW_RAW_SCORE",
        "LOW_MARGIN",
        "EVIDENCE_UNAVAILABLE"
      ],
      "registration_required": [
        "LOW_RAW_SCORE"
      ],
      "beneficial_owner_disclosure_required": [
        "LOW_RAW_SCORE"
      ],
      "holding_confirmation_required": [
        "UNKNOWN",
        "LOW_RAW_SCORE",
        "LOW_MARGIN",
        "EVIDENCE_UNAVAILABLE"
      ],
      "split_voting_restricted": [
        "UNKNOWN",
        "LOW_RAW_SCORE",
        "LOW_MARGIN",
        "EVIDENCE_UNAVAILABLE"
      ],
      "securities_lending_recall_required": [
        "LOW_RAW_SCORE"
      ],
      "other_voting_restriction": [
        "UNKNOWN",
        "PASSAGE_CONFLICT",
        "LOW_RAW_SCORE",
        "LOW_MARGIN",
        "EVIDENCE_UNAVAILABLE"
      ]
    }
  },
  "conflicts": [
    "registration_required:MODEL_DISAGREEMENT",
    "registration_required:PASSAGE_CONFLICT",
    "securities_lending_recall_required:MODEL_DISAGREEMENT",
    "securities_lending_recall_required:PASSAGE_CONFLICT",
    "share_blocking:MODEL_DISAGREEMENT",
    "share_blocking:PASSAGE_CONFLICT"
  ],
  "reconciliation_for_field": [
    {
      "stage": "LLM",
      "rule": "DISAGREEMENT_REVIEW",
      "predicate": "share_blocking",
      "earlier_value": "YES",
      "later_value": "NO",
      "supported": true
    }
  ]
}
```

## VALIDATION / CASCADE_CONSERVATIVE / 192427e9aa3ca6f904eb505ac724d3c90e8eba48b9c676788a55d6e407fcb195 / registration_required

```text
[Message EL0206C | MT564]
Broker service update: the institutional ballot channel is now available for this agenda.
This is solely a cash-distribution advice; it offers no meeting ballot and no shareholder vote.
No requirement for a voting lock on the position applies.
No requirement for a compulsory attorney mandate applies.
No requirement for mandatory meeting registration applies.
No requirement for identification of the underlying owner applies.
No requirement for a custodial holding statement applies.
No requirement for a requirement to cast all votes identically applies.
No requirement for recall of lent securities applies.
No requirement for an in-person-only voting condition applies.


[Message EL0206D | MT568]
Please retain the replacement edition for operational reconciliation. Earlier notification conditions are superseded.

```

```json
{
  "truth": "NO",
  "prediction": {
    "value": "UNKNOWN",
    "scores": {
      "YES": 0.8329,
      "NO": 0.1315,
      "UNKNOWN": 0.0356
    },
    "native_score": 0.8329,
    "confidence": null,
    "source": "UNRESOLVED_MODEL_DISAGREEMENT",
    "evidence": [
      {
        "valid": true,
        "text": "No requirement for a custodial holding statement applies.",
        "start": 454,
        "end": 511,
        "source": "NATIVE_LAYA_PASSAGE_WITH_DETERMINISTIC_SCOPE"
      }
    ],
    "aggregation_reason": "STRONG_CURRENT_RELEVANT_EVIDENCE"
  },
  "whole_notice_scores": {
    "YES": 0.3798,
    "NO": 0.4589,
    "UNKNOWN": 0.1614
  },
  "passage_scores": [
    {
      "text": "[Message EL0206C | MT564]",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.4786,
        "NO": 0.2675,
        "UNKNOWN": 0.2539
      },
      "score": 0.4786,
      "margin": 0.2111,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "Broker service update: the institutional ballot channel is now available for this agenda.",
      "state": "UNKNOWN",
      "native_value": "NO",
      "scores": {
        "YES": 0.3833,
        "NO": 0.4561,
        "UNKNOWN": 0.1606
      },
      "score": 0.4561,
      "margin": 0.07280000000000003,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "This is solely a cash-distribution advice; it offers no meeting ballot and no shareholder vote.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.7642,
        "NO": 0.2014,
        "UNKNOWN": 0.0344
      },
      "score": 0.7642,
      "margin": 0.5628,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for a voting lock on the position applies.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.685,
        "NO": 0.2818,
        "UNKNOWN": 0.0332
      },
      "score": 0.685,
      "margin": 0.40320000000000006,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for a compulsory attorney mandate applies.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.813,
        "NO": 0.1633,
        "UNKNOWN": 0.0237
      },
      "score": 0.813,
      "margin": 0.6496999999999999,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for mandatory meeting registration applies.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.6825,
        "NO": 0.2784,
        "UNKNOWN": 0.0391
      },
      "score": 0.6825,
      "margin": 0.4041,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for identification of the underlying owner applies.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.6885,
        "NO": 0.263,
        "UNKNOWN": 0.0485
      },
      "score": 0.6885,
      "margin": 0.4255,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for a custodial holding statement applies.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.8329,
        "NO": 0.1315,
        "UNKNOWN": 0.0356
      },
      "score": 0.8329,
      "margin": 0.7014,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for a requirement to cast all votes identically applies.",
      "state": "UNKNOWN",
      "native_value": "NO",
      "scores": {
        "YES": 0.3075,
        "NO": 0.6067,
        "UNKNOWN": 0.0858
      },
      "score": 0.6067,
      "margin": 0.2992,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for recall of lent securities applies.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.6795,
        "NO": 0.2704,
        "UNKNOWN": 0.05
      },
      "score": 0.6795,
      "margin": 0.4091,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for an in-person-only voting condition applies.",
      "state": "UNKNOWN",
      "native_value": "NO",
      "scores": {
        "YES": 0.1321,
        "NO": 0.6574,
        "UNKNOWN": 0.2105
      },
      "score": 0.6574,
      "margin": 0.44689999999999996,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "[Message EL0206D | MT568]",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.4527,
        "NO": 0.2911,
        "UNKNOWN": 0.2561
      },
      "score": 0.4527,
      "margin": 0.16159999999999997,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "Please retain the replacement edition for operational reconciliation.",
      "state": "UNKNOWN",
      "native_value": "NO",
      "scores": {
        "YES": 0.3889,
        "NO": 0.5066,
        "UNKNOWN": 0.1045
      },
      "score": 0.5066,
      "margin": 0.11770000000000003,
      "historical": false,
      "supersession": true,
      "conditional": false
    },
    {
      "text": "Earlier notification conditions are superseded.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.597,
        "NO": 0.3291,
        "UNKNOWN": 0.0739
      },
      "score": 0.597,
      "margin": 0.26789999999999997,
      "historical": false,
      "supersession": true,
      "conditional": false
    }
  ],
  "escalation": {
    "escalated": true,
    "requested_predicates": [
      "votability",
      "share_blocking",
      "poa_required",
      "registration_required",
      "beneficial_owner_disclosure_required",
      "holding_confirmation_required",
      "split_voting_restricted",
      "securities_lending_recall_required",
      "other_voting_restriction"
    ],
    "reasons": {
      "votability": [
        "LOW_RAW_SCORE",
        "LOW_MARGIN"
      ],
      "share_blocking": [
        "LOW_RAW_SCORE"
      ],
      "poa_required": [
        "LOW_RAW_SCORE",
        "LOW_MARGIN",
        "EVIDENCE_UNAVAILABLE"
      ],
      "registration_required": [
        "LOW_RAW_SCORE"
      ],
      "beneficial_owner_disclosure_required": [
        "LOW_RAW_SCORE"
      ],
      "holding_confirmation_required": [
        "UNKNOWN",
        "LOW_RAW_SCORE",
        "LOW_MARGIN",
        "EVIDENCE_UNAVAILABLE"
      ],
      "split_voting_restricted": [
        "UNKNOWN",
        "LOW_RAW_SCORE",
        "LOW_MARGIN",
        "EVIDENCE_UNAVAILABLE"
      ],
      "securities_lending_recall_required": [
        "LOW_RAW_SCORE"
      ],
      "other_voting_restriction": [
        "UNKNOWN",
        "PASSAGE_CONFLICT",
        "LOW_RAW_SCORE",
        "LOW_MARGIN",
        "EVIDENCE_UNAVAILABLE"
      ]
    }
  },
  "conflicts": [
    "registration_required:MODEL_DISAGREEMENT",
    "registration_required:PASSAGE_CONFLICT",
    "securities_lending_recall_required:MODEL_DISAGREEMENT",
    "securities_lending_recall_required:PASSAGE_CONFLICT",
    "share_blocking:MODEL_DISAGREEMENT",
    "share_blocking:PASSAGE_CONFLICT"
  ],
  "reconciliation_for_field": [
    {
      "stage": "LLM",
      "rule": "DISAGREEMENT_REVIEW",
      "predicate": "registration_required",
      "earlier_value": "YES",
      "later_value": "NO",
      "supported": true
    }
  ]
}
```

## VALIDATION / CASCADE_CONSERVATIVE / 192427e9aa3ca6f904eb505ac724d3c90e8eba48b9c676788a55d6e407fcb195 / securities_lending_recall_required

```text
[Message EL0206C | MT564]
Broker service update: the institutional ballot channel is now available for this agenda.
This is solely a cash-distribution advice; it offers no meeting ballot and no shareholder vote.
No requirement for a voting lock on the position applies.
No requirement for a compulsory attorney mandate applies.
No requirement for mandatory meeting registration applies.
No requirement for identification of the underlying owner applies.
No requirement for a custodial holding statement applies.
No requirement for a requirement to cast all votes identically applies.
No requirement for recall of lent securities applies.
No requirement for an in-person-only voting condition applies.


[Message EL0206D | MT568]
Please retain the replacement edition for operational reconciliation. Earlier notification conditions are superseded.

```

```json
{
  "truth": "NO",
  "prediction": {
    "value": "UNKNOWN",
    "scores": {
      "YES": 0.8045,
      "NO": 0.1563,
      "UNKNOWN": 0.0393
    },
    "native_score": 0.8045,
    "confidence": null,
    "source": "UNRESOLVED_MODEL_DISAGREEMENT",
    "evidence": [
      {
        "valid": true,
        "text": "No requirement for a custodial holding statement applies.",
        "start": 454,
        "end": 511,
        "source": "NATIVE_LAYA_PASSAGE_WITH_DETERMINISTIC_SCOPE"
      }
    ],
    "aggregation_reason": "STRONG_CURRENT_RELEVANT_EVIDENCE"
  },
  "whole_notice_scores": {
    "YES": 0.4992,
    "NO": 0.4082,
    "UNKNOWN": 0.0926
  },
  "passage_scores": [
    {
      "text": "[Message EL0206C | MT564]",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.5572,
        "NO": 0.2849,
        "UNKNOWN": 0.1579
      },
      "score": 0.5572,
      "margin": 0.27230000000000004,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "Broker service update: the institutional ballot channel is now available for this agenda.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.5641,
        "NO": 0.2808,
        "UNKNOWN": 0.1551
      },
      "score": 0.5641,
      "margin": 0.28330000000000005,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "This is solely a cash-distribution advice; it offers no meeting ballot and no shareholder vote.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.6127,
        "NO": 0.3202,
        "UNKNOWN": 0.0671
      },
      "score": 0.6127,
      "margin": 0.29250000000000004,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for a voting lock on the position applies.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.7005,
        "NO": 0.2407,
        "UNKNOWN": 0.0588
      },
      "score": 0.7005,
      "margin": 0.4598,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for a compulsory attorney mandate applies.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.6965,
        "NO": 0.2437,
        "UNKNOWN": 0.0598
      },
      "score": 0.6965,
      "margin": 0.4528,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for mandatory meeting registration applies.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.6962,
        "NO": 0.2351,
        "UNKNOWN": 0.0687
      },
      "score": 0.6962,
      "margin": 0.46110000000000007,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for identification of the underlying owner applies.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.6681,
        "NO": 0.2491,
        "UNKNOWN": 0.0828
      },
      "score": 0.6681,
      "margin": 0.41900000000000004,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for a custodial holding statement applies.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.8045,
        "NO": 0.1563,
        "UNKNOWN": 0.0393
      },
      "score": 0.8045,
      "margin": 0.6482,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for a requirement to cast all votes identically applies.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.4843,
        "NO": 0.442,
        "UNKNOWN": 0.0737
      },
      "score": 0.4843,
      "margin": 0.042300000000000004,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for recall of lent securities applies.",
      "state": "NEGATIVE",
      "native_value": "NO",
      "scores": {
        "YES": 0.3439,
        "NO": 0.6291,
        "UNKNOWN": 0.0271
      },
      "score": 0.6291,
      "margin": 0.2852,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for an in-person-only voting condition applies.",
      "state": "UNKNOWN",
      "native_value": "NO",
      "scores": {
        "YES": 0.2737,
        "NO": 0.547,
        "UNKNOWN": 0.1794
      },
      "score": 0.547,
      "margin": 0.27330000000000004,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "[Message EL0206D | MT568]",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.5434,
        "NO": 0.2793,
        "UNKNOWN": 0.1772
      },
      "score": 0.5434,
      "margin": 0.2641,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "Please retain the replacement edition for operational reconciliation.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.5096,
        "NO": 0.375,
        "UNKNOWN": 0.1154
      },
      "score": 0.5096,
      "margin": 0.13460000000000005,
      "historical": false,
      "supersession": true,
      "conditional": false
    },
    {
      "text": "Earlier notification conditions are superseded.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.6434,
        "NO": 0.2655,
        "UNKNOWN": 0.0912
      },
      "score": 0.6434,
      "margin": 0.37789999999999996,
      "historical": false,
      "supersession": true,
      "conditional": false
    }
  ],
  "escalation": {
    "escalated": true,
    "requested_predicates": [
      "votability",
      "share_blocking",
      "poa_required",
      "registration_required",
      "beneficial_owner_disclosure_required",
      "holding_confirmation_required",
      "split_voting_restricted",
      "securities_lending_recall_required",
      "other_voting_restriction"
    ],
    "reasons": {
      "votability": [
        "LOW_RAW_SCORE",
        "LOW_MARGIN"
      ],
      "share_blocking": [
        "LOW_RAW_SCORE"
      ],
      "poa_required": [
        "LOW_RAW_SCORE",
        "LOW_MARGIN",
        "EVIDENCE_UNAVAILABLE"
      ],
      "registration_required": [
        "LOW_RAW_SCORE"
      ],
      "beneficial_owner_disclosure_required": [
        "LOW_RAW_SCORE"
      ],
      "holding_confirmation_required": [
        "UNKNOWN",
        "LOW_RAW_SCORE",
        "LOW_MARGIN",
        "EVIDENCE_UNAVAILABLE"
      ],
      "split_voting_restricted": [
        "UNKNOWN",
        "LOW_RAW_SCORE",
        "LOW_MARGIN",
        "EVIDENCE_UNAVAILABLE"
      ],
      "securities_lending_recall_required": [
        "LOW_RAW_SCORE"
      ],
      "other_voting_restriction": [
        "UNKNOWN",
        "PASSAGE_CONFLICT",
        "LOW_RAW_SCORE",
        "LOW_MARGIN",
        "EVIDENCE_UNAVAILABLE"
      ]
    }
  },
  "conflicts": [
    "registration_required:MODEL_DISAGREEMENT",
    "registration_required:PASSAGE_CONFLICT",
    "securities_lending_recall_required:MODEL_DISAGREEMENT",
    "securities_lending_recall_required:PASSAGE_CONFLICT",
    "share_blocking:MODEL_DISAGREEMENT",
    "share_blocking:PASSAGE_CONFLICT"
  ],
  "reconciliation_for_field": [
    {
      "stage": "LLM",
      "rule": "DISAGREEMENT_REVIEW",
      "predicate": "securities_lending_recall_required",
      "earlier_value": "YES",
      "later_value": "NO",
      "supported": true
    }
  ]
}
```

## VALIDATION / CASCADE_CONSERVATIVE / 255328bb369bd44fa7cb0a788d797be6085e4bdab88a810f35f8b14469f269d2 / votability

```text
[Message EL0107C | MT564]
Issuer secretariat memorandum concerning arrangements for the forthcoming extraordinary assembly.
Participation may become possible, but the agent has not established whether this holder can vote.
For this vote, voting-related immobilisation is required.
The receiving agent has not resolved whether an obligatory power-of-attorney document is required for this vote.
No requirement for a required voter registration form applies.
No requirement for beneficial-owner disclosure applies.
For this vote, documentary confirmation of ownership is required.
No requirement for a ban on splitting voting instructions applies.
No requirement for retrieval of loaned voting positions applies.
No requirement for a mandatory paper-only ballot applies.


[Message EL0107D | MT568]
Please retain the replacement edition for operational reconciliation. Earlier notification conditions are superseded.

```

```json
{
  "truth": "UNCERTAIN",
  "prediction": {
    "value": "NOT_VOTABLE",
    "scores": {
      "VOTABLE": 0.1913,
      "NOT_VOTABLE": 0.5411,
      "UNCERTAIN": 0.2676
    },
    "native_score": 0.5411,
    "confidence": null,
    "source": "REGISTERED_LAYA_WHOLE_NOTICE",
    "evidence": [
      {
        "valid": true,
        "normalisation": "identity",
        "text": "[Message EL0107C | MT564]",
        "start": 0,
        "end": 25,
        "source": "MATCHING_NATIVE_PASSAGE"
      }
    ]
  },
  "whole_notice_scores": null,
  "passage_scores": [],
  "escalation": {
    "escalated": true,
    "requested_predicates": [
      "votability",
      "share_blocking",
      "poa_required",
      "registration_required",
      "beneficial_owner_disclosure_required",
      "holding_confirmation_required",
      "split_voting_restricted",
      "securities_lending_recall_required",
      "other_voting_restriction"
    ],
    "reasons": {
      "votability": [
        "LOW_RAW_SCORE",
        "LOW_MARGIN"
      ],
      "share_blocking": [
        "LOW_RAW_SCORE"
      ],
      "poa_required": [
        "UNKNOWN",
        "LOW_RAW_SCORE",
        "LOW_MARGIN",
        "EVIDENCE_UNAVAILABLE"
      ],
      "registration_required": [
        "LOW_RAW_SCORE"
      ],
      "beneficial_owner_disclosure_required": [
        "LOW_RAW_SCORE"
      ],
      "holding_confirmation_required": [
        "LOW_RAW_SCORE"
      ],
      "split_voting_restricted": [
        "LOW_RAW_SCORE"
      ],
      "securities_lending_recall_required": [
        "LOW_RAW_SCORE"
      ],
      "other_voting_restriction": [
        "LOW_RAW_SCORE"
      ]
    }
  },
  "conflicts": [
    "The agent has not established whether this holder can vote.",
    "The receiving agent has not resolved whether an obligatory power-of-attorney document is required for this vote.",
    "registration_required:MODEL_DISAGREEMENT",
    "registration_required:PASSAGE_CONFLICT",
    "securities_lending_recall_required:MODEL_DISAGREEMENT",
    "securities_lending_recall_required:PASSAGE_CONFLICT",
    "split_voting_restricted:MODEL_DISAGREEMENT",
    "split_voting_restricted:PASSAGE_CONFLICT"
  ],
  "reconciliation_for_field": [
    {
      "stage": "LLM",
      "rule": "LATER_ABSTENTION",
      "predicate": "votability",
      "supported": false
    }
  ]
}
```

## VALIDATION / CASCADE_CONSERVATIVE / 255328bb369bd44fa7cb0a788d797be6085e4bdab88a810f35f8b14469f269d2 / registration_required

```text
[Message EL0107C | MT564]
Issuer secretariat memorandum concerning arrangements for the forthcoming extraordinary assembly.
Participation may become possible, but the agent has not established whether this holder can vote.
For this vote, voting-related immobilisation is required.
The receiving agent has not resolved whether an obligatory power-of-attorney document is required for this vote.
No requirement for a required voter registration form applies.
No requirement for beneficial-owner disclosure applies.
For this vote, documentary confirmation of ownership is required.
No requirement for a ban on splitting voting instructions applies.
No requirement for retrieval of loaned voting positions applies.
No requirement for a mandatory paper-only ballot applies.


[Message EL0107D | MT568]
Please retain the replacement edition for operational reconciliation. Earlier notification conditions are superseded.

```

```json
{
  "truth": "NO",
  "prediction": {
    "value": "UNKNOWN",
    "scores": {
      "YES": 0.8479,
      "NO": 0.082,
      "UNKNOWN": 0.0701
    },
    "native_score": 0.8479,
    "confidence": null,
    "source": "UNRESOLVED_MODEL_DISAGREEMENT",
    "evidence": [
      {
        "valid": true,
        "text": "The receiving agent has not resolved whether an obligatory power-of-attorney document is required for this vote.",
        "start": 281,
        "end": 393,
        "source": "NATIVE_LAYA_PASSAGE_WITH_DETERMINISTIC_SCOPE"
      }
    ],
    "aggregation_reason": "STRONG_CURRENT_RELEVANT_EVIDENCE"
  },
  "whole_notice_scores": {
    "YES": 0.1461,
    "NO": 0.8218,
    "UNKNOWN": 0.032
  },
  "passage_scores": [
    {
      "text": "[Message EL0107C | MT564]",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.4683,
        "NO": 0.3075,
        "UNKNOWN": 0.2242
      },
      "score": 0.4683,
      "margin": 0.1608,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "Issuer secretariat memorandum concerning arrangements for the forthcoming extraordinary assembly.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.6038,
        "NO": 0.3606,
        "UNKNOWN": 0.0355
      },
      "score": 0.6038,
      "margin": 0.24320000000000003,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "Participation may become possible, but the agent has not established whether this holder can vote.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.6385,
        "NO": 0.2578,
        "UNKNOWN": 0.1037
      },
      "score": 0.6385,
      "margin": 0.3807,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "For this vote, voting-related immobilisation is required.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.5601,
        "NO": 0.3592,
        "UNKNOWN": 0.0807
      },
      "score": 0.5601,
      "margin": 0.20090000000000002,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "The receiving agent has not resolved whether an obligatory power-of-attorney document is required for this vote.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.8479,
        "NO": 0.082,
        "UNKNOWN": 0.0701
      },
      "score": 0.8479,
      "margin": 0.7659,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for a required voter registration form applies.",
      "state": "NEGATIVE",
      "native_value": "NO",
      "scores": {
        "YES": 0.3223,
        "NO": 0.6322,
        "UNKNOWN": 0.0455
      },
      "score": 0.6322,
      "margin": 0.3099,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for beneficial-owner disclosure applies.",
      "state": "UNKNOWN",
      "native_value": "NO",
      "scores": {
        "YES": 0.3614,
        "NO": 0.5935,
        "UNKNOWN": 0.0451
      },
      "score": 0.5935,
      "margin": 0.23210000000000003,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "For this vote, documentary confirmation of ownership is required.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.8133,
        "NO": 0.129,
        "UNKNOWN": 0.0577
      },
      "score": 0.8133,
      "margin": 0.6843,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for a ban on splitting voting instructions applies.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.8032,
        "NO": 0.1731,
        "UNKNOWN": 0.0237
      },
      "score": 0.8032,
      "margin": 0.6301,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for retrieval of loaned voting positions applies.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.5694,
        "NO": 0.3459,
        "UNKNOWN": 0.0847
      },
      "score": 0.5694,
      "margin": 0.22350000000000003,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for a mandatory paper-only ballot applies.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.624,
        "NO": 0.3461,
        "UNKNOWN": 0.0299
      },
      "score": 0.624,
      "margin": 0.2779,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "[Message EL0107D | MT568]",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.4165,
        "NO": 0.3356,
        "UNKNOWN": 0.2478
      },
      "score": 0.4165,
      "margin": 0.08089999999999997,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "Please retain the replacement edition for operational reconciliation.",
      "state": "UNKNOWN",
      "native_value": "NO",
      "scores": {
        "YES": 0.3889,
        "NO": 0.5066,
        "UNKNOWN": 0.1045
      },
      "score": 0.5066,
      "margin": 0.11770000000000003,
      "historical": false,
      "supersession": true,
      "conditional": false
    },
    {
      "text": "Earlier notification conditions are superseded.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.597,
        "NO": 0.3291,
        "UNKNOWN": 0.0739
      },
      "score": 0.597,
      "margin": 0.26789999999999997,
      "historical": false,
      "supersession": true,
      "conditional": false
    }
  ],
  "escalation": {
    "escalated": true,
    "requested_predicates": [
      "votability",
      "share_blocking",
      "poa_required",
      "registration_required",
      "beneficial_owner_disclosure_required",
      "holding_confirmation_required",
      "split_voting_restricted",
      "securities_lending_recall_required",
      "other_voting_restriction"
    ],
    "reasons": {
      "votability": [
        "LOW_RAW_SCORE",
        "LOW_MARGIN"
      ],
      "share_blocking": [
        "LOW_RAW_SCORE"
      ],
      "poa_required": [
        "UNKNOWN",
        "LOW_RAW_SCORE",
        "LOW_MARGIN",
        "EVIDENCE_UNAVAILABLE"
      ],
      "registration_required": [
        "LOW_RAW_SCORE"
      ],
      "beneficial_owner_disclosure_required": [
        "LOW_RAW_SCORE"
      ],
      "holding_confirmation_required": [
        "LOW_RAW_SCORE"
      ],
      "split_voting_restricted": [
        "LOW_RAW_SCORE"
      ],
      "securities_lending_recall_required": [
        "LOW_RAW_SCORE"
      ],
      "other_voting_restriction": [
        "LOW_RAW_SCORE"
      ]
    }
  },
  "conflicts": [
    "The agent has not established whether this holder can vote.",
    "The receiving agent has not resolved whether an obligatory power-of-attorney document is required for this vote.",
    "registration_required:MODEL_DISAGREEMENT",
    "registration_required:PASSAGE_CONFLICT",
    "securities_lending_recall_required:MODEL_DISAGREEMENT",
    "securities_lending_recall_required:PASSAGE_CONFLICT",
    "split_voting_restricted:MODEL_DISAGREEMENT",
    "split_voting_restricted:PASSAGE_CONFLICT"
  ],
  "reconciliation_for_field": [
    {
      "stage": "LLM",
      "rule": "DISAGREEMENT_REVIEW",
      "predicate": "registration_required",
      "earlier_value": "YES",
      "later_value": "NO",
      "supported": true
    }
  ]
}
```

## VALIDATION / CASCADE_CONSERVATIVE / 255328bb369bd44fa7cb0a788d797be6085e4bdab88a810f35f8b14469f269d2 / split_voting_restricted

```text
[Message EL0107C | MT564]
Issuer secretariat memorandum concerning arrangements for the forthcoming extraordinary assembly.
Participation may become possible, but the agent has not established whether this holder can vote.
For this vote, voting-related immobilisation is required.
The receiving agent has not resolved whether an obligatory power-of-attorney document is required for this vote.
No requirement for a required voter registration form applies.
No requirement for beneficial-owner disclosure applies.
For this vote, documentary confirmation of ownership is required.
No requirement for a ban on splitting voting instructions applies.
No requirement for retrieval of loaned voting positions applies.
No requirement for a mandatory paper-only ballot applies.


[Message EL0107D | MT568]
Please retain the replacement edition for operational reconciliation. Earlier notification conditions are superseded.

```

```json
{
  "truth": "NO",
  "prediction": {
    "value": "UNKNOWN",
    "scores": {
      "YES": 0.8776,
      "NO": 0.0942,
      "UNKNOWN": 0.0282
    },
    "native_score": 0.8776,
    "confidence": null,
    "source": "UNRESOLVED_MODEL_DISAGREEMENT",
    "evidence": [
      {
        "valid": true,
        "text": "No requirement for a ban on splitting voting instructions applies.",
        "start": 579,
        "end": 645,
        "source": "NATIVE_LAYA_PASSAGE_WITH_DETERMINISTIC_SCOPE"
      }
    ],
    "aggregation_reason": "STRONG_CURRENT_RELEVANT_EVIDENCE"
  },
  "whole_notice_scores": {
    "YES": 0.2907,
    "NO": 0.6729,
    "UNKNOWN": 0.0363
  },
  "passage_scores": [
    {
      "text": "[Message EL0107C | MT564]",
      "state": "UNKNOWN",
      "native_value": "NO",
      "scores": {
        "YES": 0.2059,
        "NO": 0.4621,
        "UNKNOWN": 0.332
      },
      "score": 0.4621,
      "margin": 0.1301,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "Issuer secretariat memorandum concerning arrangements for the forthcoming extraordinary assembly.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.6891,
        "NO": 0.2824,
        "UNKNOWN": 0.0285
      },
      "score": 0.6891,
      "margin": 0.40670000000000006,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "Participation may become possible, but the agent has not established whether this holder can vote.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.4281,
        "NO": 0.3666,
        "UNKNOWN": 0.2053
      },
      "score": 0.4281,
      "margin": 0.0615,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "For this vote, voting-related immobilisation is required.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.739,
        "NO": 0.1797,
        "UNKNOWN": 0.0813
      },
      "score": 0.739,
      "margin": 0.5593,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "The receiving agent has not resolved whether an obligatory power-of-attorney document is required for this vote.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.7723,
        "NO": 0.1186,
        "UNKNOWN": 0.1091
      },
      "score": 0.7723,
      "margin": 0.6537,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for a required voter registration form applies.",
      "state": "UNKNOWN",
      "native_value": "NO",
      "scores": {
        "YES": 0.4632,
        "NO": 0.4702,
        "UNKNOWN": 0.0666
      },
      "score": 0.4702,
      "margin": 0.007000000000000006,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for beneficial-owner disclosure applies.",
      "state": "UNKNOWN",
      "native_value": "NO",
      "scores": {
        "YES": 0.1339,
        "NO": 0.7214,
        "UNKNOWN": 0.1447
      },
      "score": 0.7214,
      "margin": 0.5767,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "For this vote, documentary confirmation of ownership is required.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.7301,
        "NO": 0.1693,
        "UNKNOWN": 0.1006
      },
      "score": 0.7301,
      "margin": 0.5608,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for a ban on splitting voting instructions applies.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.8776,
        "NO": 0.0942,
        "UNKNOWN": 0.0282
      },
      "score": 0.8776,
      "margin": 0.7834000000000001,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for retrieval of loaned voting positions applies.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.5739,
        "NO": 0.3204,
        "UNKNOWN": 0.1057
      },
      "score": 0.5739,
      "margin": 0.25349999999999995,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for a mandatory paper-only ballot applies.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.513,
        "NO": 0.4345,
        "UNKNOWN": 0.0525
      },
      "score": 0.513,
      "margin": 0.07850000000000001,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "[Message EL0107D | MT568]",
      "state": "UNKNOWN",
      "native_value": "NO",
      "scores": {
        "YES": 0.1092,
        "NO": 0.6218,
        "UNKNOWN": 0.269
      },
      "score": 0.6218,
      "margin": 0.3528,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "Please retain the replacement edition for operational reconciliation.",
      "state": "UNKNOWN",
      "native_value": "NO",
      "scores": {
        "YES": 0.1878,
        "NO": 0.7297,
        "UNKNOWN": 0.0824
      },
      "score": 0.7297,
      "margin": 0.5419,
      "historical": false,
      "supersession": true,
      "conditional": false
    },
    {
      "text": "Earlier notification conditions are superseded.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.4973,
        "NO": 0.3914,
        "UNKNOWN": 0.1113
      },
      "score": 0.4973,
      "margin": 0.1059,
      "historical": false,
      "supersession": true,
      "conditional": false
    }
  ],
  "escalation": {
    "escalated": true,
    "requested_predicates": [
      "votability",
      "share_blocking",
      "poa_required",
      "registration_required",
      "beneficial_owner_disclosure_required",
      "holding_confirmation_required",
      "split_voting_restricted",
      "securities_lending_recall_required",
      "other_voting_restriction"
    ],
    "reasons": {
      "votability": [
        "LOW_RAW_SCORE",
        "LOW_MARGIN"
      ],
      "share_blocking": [
        "LOW_RAW_SCORE"
      ],
      "poa_required": [
        "UNKNOWN",
        "LOW_RAW_SCORE",
        "LOW_MARGIN",
        "EVIDENCE_UNAVAILABLE"
      ],
      "registration_required": [
        "LOW_RAW_SCORE"
      ],
      "beneficial_owner_disclosure_required": [
        "LOW_RAW_SCORE"
      ],
      "holding_confirmation_required": [
        "LOW_RAW_SCORE"
      ],
      "split_voting_restricted": [
        "LOW_RAW_SCORE"
      ],
      "securities_lending_recall_required": [
        "LOW_RAW_SCORE"
      ],
      "other_voting_restriction": [
        "LOW_RAW_SCORE"
      ]
    }
  },
  "conflicts": [
    "The agent has not established whether this holder can vote.",
    "The receiving agent has not resolved whether an obligatory power-of-attorney document is required for this vote.",
    "registration_required:MODEL_DISAGREEMENT",
    "registration_required:PASSAGE_CONFLICT",
    "securities_lending_recall_required:MODEL_DISAGREEMENT",
    "securities_lending_recall_required:PASSAGE_CONFLICT",
    "split_voting_restricted:MODEL_DISAGREEMENT",
    "split_voting_restricted:PASSAGE_CONFLICT"
  ],
  "reconciliation_for_field": [
    {
      "stage": "LLM",
      "rule": "DISAGREEMENT_REVIEW",
      "predicate": "split_voting_restricted",
      "earlier_value": "YES",
      "later_value": "NO",
      "supported": true
    }
  ]
}
```

## VALIDATION / CASCADE_CONSERVATIVE / 255328bb369bd44fa7cb0a788d797be6085e4bdab88a810f35f8b14469f269d2 / securities_lending_recall_required

```text
[Message EL0107C | MT564]
Issuer secretariat memorandum concerning arrangements for the forthcoming extraordinary assembly.
Participation may become possible, but the agent has not established whether this holder can vote.
For this vote, voting-related immobilisation is required.
The receiving agent has not resolved whether an obligatory power-of-attorney document is required for this vote.
No requirement for a required voter registration form applies.
No requirement for beneficial-owner disclosure applies.
For this vote, documentary confirmation of ownership is required.
No requirement for a ban on splitting voting instructions applies.
No requirement for retrieval of loaned voting positions applies.
No requirement for a mandatory paper-only ballot applies.


[Message EL0107D | MT568]
Please retain the replacement edition for operational reconciliation. Earlier notification conditions are superseded.

```

```json
{
  "truth": "NO",
  "prediction": {
    "value": "UNKNOWN",
    "scores": {
      "YES": 0.7864,
      "NO": 0.1765,
      "UNKNOWN": 0.0371
    },
    "native_score": 0.7864,
    "confidence": null,
    "source": "UNRESOLVED_MODEL_DISAGREEMENT",
    "evidence": [
      {
        "valid": true,
        "text": "No requirement for a ban on splitting voting instructions applies.",
        "start": 579,
        "end": 645,
        "source": "NATIVE_LAYA_PASSAGE_WITH_DETERMINISTIC_SCOPE"
      }
    ],
    "aggregation_reason": "STRONG_CURRENT_RELEVANT_EVIDENCE"
  },
  "whole_notice_scores": {
    "YES": 0.2336,
    "NO": 0.7251,
    "UNKNOWN": 0.0413
  },
  "passage_scores": [
    {
      "text": "[Message EL0107C | MT564]",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.537,
        "NO": 0.3061,
        "UNKNOWN": 0.157
      },
      "score": 0.537,
      "margin": 0.23090000000000005,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "Issuer secretariat memorandum concerning arrangements for the forthcoming extraordinary assembly.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.5404,
        "NO": 0.3777,
        "UNKNOWN": 0.0819
      },
      "score": 0.5404,
      "margin": 0.1627,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "Participation may become possible, but the agent has not established whether this holder can vote.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.5427,
        "NO": 0.3087,
        "UNKNOWN": 0.1486
      },
      "score": 0.5427,
      "margin": 0.23399999999999999,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "For this vote, voting-related immobilisation is required.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.7666,
        "NO": 0.1556,
        "UNKNOWN": 0.0779
      },
      "score": 0.7666,
      "margin": 0.611,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "The receiving agent has not resolved whether an obligatory power-of-attorney document is required for this vote.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.7425,
        "NO": 0.1586,
        "UNKNOWN": 0.0988
      },
      "score": 0.7425,
      "margin": 0.5839000000000001,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for a required voter registration form applies.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.5264,
        "NO": 0.3962,
        "UNKNOWN": 0.0774
      },
      "score": 0.5264,
      "margin": 0.13019999999999998,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for beneficial-owner disclosure applies.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.5311,
        "NO": 0.3741,
        "UNKNOWN": 0.0948
      },
      "score": 0.5311,
      "margin": 0.15700000000000003,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "For this vote, documentary confirmation of ownership is required.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.7744,
        "NO": 0.1381,
        "UNKNOWN": 0.0874
      },
      "score": 0.7744,
      "margin": 0.6363,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for a ban on splitting voting instructions applies.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.7864,
        "NO": 0.1765,
        "UNKNOWN": 0.0371
      },
      "score": 0.7864,
      "margin": 0.6099,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for retrieval of loaned voting positions applies.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.6289,
        "NO": 0.2869,
        "UNKNOWN": 0.0842
      },
      "score": 0.6289,
      "margin": 0.342,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for a mandatory paper-only ballot applies.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.7254,
        "NO": 0.2372,
        "UNKNOWN": 0.0374
      },
      "score": 0.7254,
      "margin": 0.4882000000000001,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "[Message EL0107D | MT568]",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.5104,
        "NO": 0.3234,
        "UNKNOWN": 0.1661
      },
      "score": 0.5104,
      "margin": 0.18699999999999994,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "Please retain the replacement edition for operational reconciliation.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.5096,
        "NO": 0.375,
        "UNKNOWN": 0.1154
      },
      "score": 0.5096,
      "margin": 0.13460000000000005,
      "historical": false,
      "supersession": true,
      "conditional": false
    },
    {
      "text": "Earlier notification conditions are superseded.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.6434,
        "NO": 0.2655,
        "UNKNOWN": 0.0912
      },
      "score": 0.6434,
      "margin": 0.37789999999999996,
      "historical": false,
      "supersession": true,
      "conditional": false
    }
  ],
  "escalation": {
    "escalated": true,
    "requested_predicates": [
      "votability",
      "share_blocking",
      "poa_required",
      "registration_required",
      "beneficial_owner_disclosure_required",
      "holding_confirmation_required",
      "split_voting_restricted",
      "securities_lending_recall_required",
      "other_voting_restriction"
    ],
    "reasons": {
      "votability": [
        "LOW_RAW_SCORE",
        "LOW_MARGIN"
      ],
      "share_blocking": [
        "LOW_RAW_SCORE"
      ],
      "poa_required": [
        "UNKNOWN",
        "LOW_RAW_SCORE",
        "LOW_MARGIN",
        "EVIDENCE_UNAVAILABLE"
      ],
      "registration_required": [
        "LOW_RAW_SCORE"
      ],
      "beneficial_owner_disclosure_required": [
        "LOW_RAW_SCORE"
      ],
      "holding_confirmation_required": [
        "LOW_RAW_SCORE"
      ],
      "split_voting_restricted": [
        "LOW_RAW_SCORE"
      ],
      "securities_lending_recall_required": [
        "LOW_RAW_SCORE"
      ],
      "other_voting_restriction": [
        "LOW_RAW_SCORE"
      ]
    }
  },
  "conflicts": [
    "The agent has not established whether this holder can vote.",
    "The receiving agent has not resolved whether an obligatory power-of-attorney document is required for this vote.",
    "registration_required:MODEL_DISAGREEMENT",
    "registration_required:PASSAGE_CONFLICT",
    "securities_lending_recall_required:MODEL_DISAGREEMENT",
    "securities_lending_recall_required:PASSAGE_CONFLICT",
    "split_voting_restricted:MODEL_DISAGREEMENT",
    "split_voting_restricted:PASSAGE_CONFLICT"
  ],
  "reconciliation_for_field": [
    {
      "stage": "LLM",
      "rule": "DISAGREEMENT_REVIEW",
      "predicate": "securities_lending_recall_required",
      "earlier_value": "YES",
      "later_value": "NO",
      "supported": true
    }
  ]
}
```

## VALIDATION / CASCADE_CONSERVATIVE / 25150120b9a9e92a98ab8b33fb003cab98a2ec6b4230ec908fda5c15d2bbc7d7 / share_blocking

```text
[Message EL0105C | MT564]
Issuer secretariat memorandum concerning arrangements for the forthcoming extraordinary assembly.
The current agenda is open for shareholder voting instructions.
No requirement for voting-related immobilisation applies.
No requirement for an obligatory power-of-attorney document applies.
For this vote, a required voter registration form is required.
No requirement for beneficial-owner disclosure applies.
No requirement for documentary confirmation of ownership applies.
No requirement for a ban on splitting voting instructions applies.
For this vote, retrieval of loaned voting positions is required.
No requirement for a mandatory paper-only ballot applies.


[Message EL0105D | MT568]
Please retain the replacement edition for operational reconciliation. Earlier notification conditions are superseded.

```

```json
{
  "truth": "NO",
  "prediction": {
    "value": "UNKNOWN",
    "scores": {
      "YES": 0.9632,
      "NO": 0.0123,
      "UNKNOWN": 0.0244
    },
    "native_score": 0.9632,
    "confidence": null,
    "source": "UNRESOLVED_MODEL_DISAGREEMENT",
    "evidence": [
      {
        "valid": true,
        "text": "Earlier notification conditions are superseded.",
        "start": 788,
        "end": 835,
        "source": "NATIVE_LAYA_PASSAGE_WITH_DETERMINISTIC_SCOPE"
      }
    ],
    "aggregation_reason": "STRONG_CURRENT_RELEVANT_EVIDENCE"
  },
  "whole_notice_scores": {
    "YES": 0.5452,
    "NO": 0.3448,
    "UNKNOWN": 0.11
  },
  "passage_scores": [
    {
      "text": "[Message EL0105C | MT564]",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.9335,
        "NO": 0.0295,
        "UNKNOWN": 0.0369
      },
      "score": 0.9335,
      "margin": 0.8966,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "Issuer secretariat memorandum concerning arrangements for the forthcoming extraordinary assembly.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.8912,
        "NO": 0.0831,
        "UNKNOWN": 0.0257
      },
      "score": 0.8912,
      "margin": 0.8081,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "The current agenda is open for shareholder voting instructions.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.7926,
        "NO": 0.1291,
        "UNKNOWN": 0.0782
      },
      "score": 0.7926,
      "margin": 0.6635,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for voting-related immobilisation applies.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.9416,
        "NO": 0.0445,
        "UNKNOWN": 0.0138
      },
      "score": 0.9416,
      "margin": 0.8971,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for an obligatory power-of-attorney document applies.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.8869,
        "NO": 0.0734,
        "UNKNOWN": 0.0397
      },
      "score": 0.8869,
      "margin": 0.8135,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "For this vote, a required voter registration form is required.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.9322,
        "NO": 0.0298,
        "UNKNOWN": 0.038
      },
      "score": 0.9322,
      "margin": 0.8942,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for beneficial-owner disclosure applies.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.8787,
        "NO": 0.0756,
        "UNKNOWN": 0.0457
      },
      "score": 0.8787,
      "margin": 0.8031,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for documentary confirmation of ownership applies.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.9257,
        "NO": 0.0501,
        "UNKNOWN": 0.0242
      },
      "score": 0.9257,
      "margin": 0.8755999999999999,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for a ban on splitting voting instructions applies.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.9567,
        "NO": 0.0233,
        "UNKNOWN": 0.02
      },
      "score": 0.9567,
      "margin": 0.9334,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "For this vote, retrieval of loaned voting positions is required.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.8708,
        "NO": 0.0624,
        "UNKNOWN": 0.0668
      },
      "score": 0.8708,
      "margin": 0.804,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for a mandatory paper-only ballot applies.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.8633,
        "NO": 0.0911,
        "UNKNOWN": 0.0457
      },
      "score": 0.8633,
      "margin": 0.7722,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "[Message EL0105D | MT568]",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.9334,
        "NO": 0.0319,
        "UNKNOWN": 0.0347
      },
      "score": 0.9334,
      "margin": 0.8987,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "Please retain the replacement edition for operational reconciliation.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.9104,
        "NO": 0.053,
        "UNKNOWN": 0.0366
      },
      "score": 0.9104,
      "margin": 0.8573999999999999,
      "historical": false,
      "supersession": true,
      "conditional": false
    },
    {
      "text": "Earlier notification conditions are superseded.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.9632,
        "NO": 0.0123,
        "UNKNOWN": 0.0244
      },
      "score": 0.9632,
      "margin": 0.9388,
      "historical": false,
      "supersession": true,
      "conditional": false
    }
  ],
  "escalation": {
    "escalated": true,
    "requested_predicates": [
      "share_blocking",
      "poa_required",
      "registration_required",
      "beneficial_owner_disclosure_required",
      "holding_confirmation_required",
      "split_voting_restricted",
      "securities_lending_recall_required",
      "other_voting_restriction"
    ],
    "reasons": {
      "share_blocking": [
        "LOW_RAW_SCORE"
      ],
      "poa_required": [
        "LOW_RAW_SCORE"
      ],
      "registration_required": [
        "LOW_RAW_SCORE"
      ],
      "beneficial_owner_disclosure_required": [
        "LOW_RAW_SCORE"
      ],
      "holding_confirmation_required": [
        "LOW_RAW_SCORE"
      ],
      "split_voting_restricted": [
        "LOW_RAW_SCORE"
      ],
      "securities_lending_recall_required": [
        "LOW_RAW_SCORE"
      ],
      "other_voting_restriction": [
        "LOW_RAW_SCORE"
      ]
    }
  },
  "conflicts": [
    "Message EL0105D states 'Earlier notification conditions are superseded' but does not specify which conditions or provide replacement terms, creating uncertainty about the final operative status of the conditions listed in EL0105C.",
    "share_blocking:MODEL_DISAGREEMENT",
    "share_blocking:PASSAGE_CONFLICT",
    "split_voting_restricted:MODEL_DISAGREEMENT",
    "split_voting_restricted:PASSAGE_CONFLICT",
    "votability:STRUCTURE_SEMANTIC_CONFLICT"
  ],
  "reconciliation_for_field": [
    {
      "stage": "LLM",
      "rule": "DISAGREEMENT_REVIEW",
      "predicate": "share_blocking",
      "earlier_value": "YES",
      "later_value": "NO",
      "supported": true
    }
  ]
}
```

## VALIDATION / CASCADE_CONSERVATIVE / 25150120b9a9e92a98ab8b33fb003cab98a2ec6b4230ec908fda5c15d2bbc7d7 / split_voting_restricted

```text
[Message EL0105C | MT564]
Issuer secretariat memorandum concerning arrangements for the forthcoming extraordinary assembly.
The current agenda is open for shareholder voting instructions.
No requirement for voting-related immobilisation applies.
No requirement for an obligatory power-of-attorney document applies.
For this vote, a required voter registration form is required.
No requirement for beneficial-owner disclosure applies.
No requirement for documentary confirmation of ownership applies.
No requirement for a ban on splitting voting instructions applies.
For this vote, retrieval of loaned voting positions is required.
No requirement for a mandatory paper-only ballot applies.


[Message EL0105D | MT568]
Please retain the replacement edition for operational reconciliation. Earlier notification conditions are superseded.

```

```json
{
  "truth": "NO",
  "prediction": {
    "value": "UNKNOWN",
    "scores": {
      "YES": 0.8776,
      "NO": 0.0942,
      "UNKNOWN": 0.0282
    },
    "native_score": 0.8776,
    "confidence": null,
    "source": "UNRESOLVED_MODEL_DISAGREEMENT",
    "evidence": [
      {
        "valid": true,
        "text": "No requirement for a ban on splitting voting instructions applies.",
        "start": 500,
        "end": 566,
        "source": "NATIVE_LAYA_PASSAGE_WITH_DETERMINISTIC_SCOPE"
      }
    ],
    "aggregation_reason": "STRONG_CURRENT_RELEVANT_EVIDENCE"
  },
  "whole_notice_scores": {
    "YES": 0.4047,
    "NO": 0.5216,
    "UNKNOWN": 0.0737
  },
  "passage_scores": [
    {
      "text": "[Message EL0105C | MT564]",
      "state": "UNKNOWN",
      "native_value": "NO",
      "scores": {
        "YES": 0.1967,
        "NO": 0.4941,
        "UNKNOWN": 0.3092
      },
      "score": 0.4941,
      "margin": 0.1849,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "Issuer secretariat memorandum concerning arrangements for the forthcoming extraordinary assembly.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.6891,
        "NO": 0.2824,
        "UNKNOWN": 0.0285
      },
      "score": 0.6891,
      "margin": 0.40670000000000006,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "The current agenda is open for shareholder voting instructions.",
      "state": "UNKNOWN",
      "native_value": "NO",
      "scores": {
        "YES": 0.1997,
        "NO": 0.6685,
        "UNKNOWN": 0.1318
      },
      "score": 0.6685,
      "margin": 0.4688,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for voting-related immobilisation applies.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.5293,
        "NO": 0.3713,
        "UNKNOWN": 0.0993
      },
      "score": 0.5293,
      "margin": 0.15799999999999997,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for an obligatory power-of-attorney document applies.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.6168,
        "NO": 0.3047,
        "UNKNOWN": 0.0785
      },
      "score": 0.6168,
      "margin": 0.3121,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "For this vote, a required voter registration form is required.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.8131,
        "NO": 0.1179,
        "UNKNOWN": 0.069
      },
      "score": 0.8131,
      "margin": 0.6952,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for beneficial-owner disclosure applies.",
      "state": "UNKNOWN",
      "native_value": "NO",
      "scores": {
        "YES": 0.1339,
        "NO": 0.7214,
        "UNKNOWN": 0.1447
      },
      "score": 0.7214,
      "margin": 0.5767,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for documentary confirmation of ownership applies.",
      "state": "UNKNOWN",
      "native_value": "NO",
      "scores": {
        "YES": 0.3582,
        "NO": 0.5515,
        "UNKNOWN": 0.0903
      },
      "score": 0.5515,
      "margin": 0.19329999999999997,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for a ban on splitting voting instructions applies.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.8776,
        "NO": 0.0942,
        "UNKNOWN": 0.0282
      },
      "score": 0.8776,
      "margin": 0.7834000000000001,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "For this vote, retrieval of loaned voting positions is required.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.6635,
        "NO": 0.229,
        "UNKNOWN": 0.1074
      },
      "score": 0.6635,
      "margin": 0.4345,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for a mandatory paper-only ballot applies.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.513,
        "NO": 0.4345,
        "UNKNOWN": 0.0525
      },
      "score": 0.513,
      "margin": 0.07850000000000001,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "[Message EL0105D | MT568]",
      "state": "UNKNOWN",
      "native_value": "NO",
      "scores": {
        "YES": 0.1502,
        "NO": 0.5727,
        "UNKNOWN": 0.2771
      },
      "score": 0.5727,
      "margin": 0.2956,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "Please retain the replacement edition for operational reconciliation.",
      "state": "UNKNOWN",
      "native_value": "NO",
      "scores": {
        "YES": 0.1878,
        "NO": 0.7297,
        "UNKNOWN": 0.0824
      },
      "score": 0.7297,
      "margin": 0.5419,
      "historical": false,
      "supersession": true,
      "conditional": false
    },
    {
      "text": "Earlier notification conditions are superseded.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.4973,
        "NO": 0.3914,
        "UNKNOWN": 0.1113
      },
      "score": 0.4973,
      "margin": 0.1059,
      "historical": false,
      "supersession": true,
      "conditional": false
    }
  ],
  "escalation": {
    "escalated": true,
    "requested_predicates": [
      "share_blocking",
      "poa_required",
      "registration_required",
      "beneficial_owner_disclosure_required",
      "holding_confirmation_required",
      "split_voting_restricted",
      "securities_lending_recall_required",
      "other_voting_restriction"
    ],
    "reasons": {
      "share_blocking": [
        "LOW_RAW_SCORE"
      ],
      "poa_required": [
        "LOW_RAW_SCORE"
      ],
      "registration_required": [
        "LOW_RAW_SCORE"
      ],
      "beneficial_owner_disclosure_required": [
        "LOW_RAW_SCORE"
      ],
      "holding_confirmation_required": [
        "LOW_RAW_SCORE"
      ],
      "split_voting_restricted": [
        "LOW_RAW_SCORE"
      ],
      "securities_lending_recall_required": [
        "LOW_RAW_SCORE"
      ],
      "other_voting_restriction": [
        "LOW_RAW_SCORE"
      ]
    }
  },
  "conflicts": [
    "Message EL0105D states 'Earlier notification conditions are superseded' but does not specify which conditions or provide replacement terms, creating uncertainty about the final operative status of the conditions listed in EL0105C.",
    "share_blocking:MODEL_DISAGREEMENT",
    "share_blocking:PASSAGE_CONFLICT",
    "split_voting_restricted:MODEL_DISAGREEMENT",
    "split_voting_restricted:PASSAGE_CONFLICT",
    "votability:STRUCTURE_SEMANTIC_CONFLICT"
  ],
  "reconciliation_for_field": [
    {
      "stage": "LLM",
      "rule": "DISAGREEMENT_REVIEW",
      "predicate": "split_voting_restricted",
      "earlier_value": "YES",
      "later_value": "NO",
      "supported": true
    }
  ]
}
```

## VALIDATION / CASCADE_CONSERVATIVE / 2414be60f4dff3cc46dcf385c748749f7c7c3dc05ef8f904052ec9797bdc2f19 / share_blocking

```text
[Message EL0104C | MT564]
Issuer secretariat memorandum concerning arrangements for the forthcoming extraordinary assembly.
The current agenda is open for shareholder voting instructions.
No requirement for voting-related immobilisation applies.
No requirement for an obligatory power-of-attorney document applies.
No requirement for a required voter registration form applies.
For this vote, beneficial-owner disclosure is required.
No requirement for documentary confirmation of ownership applies.
No requirement for a ban on splitting voting instructions applies.
No requirement for retrieval of loaned voting positions applies.
For this vote, a mandatory paper-only ballot is required.


[Message EL0104D | MT568]
Please retain the replacement edition for operational reconciliation. Earlier notification conditions are superseded.

```

```json
{
  "truth": "NO",
  "prediction": {
    "value": "UNKNOWN",
    "scores": {
      "YES": 0.9632,
      "NO": 0.0123,
      "UNKNOWN": 0.0244
    },
    "native_score": 0.9632,
    "confidence": null,
    "source": "UNRESOLVED_MODEL_DISAGREEMENT",
    "evidence": [
      {
        "valid": true,
        "text": "Earlier notification conditions are superseded.",
        "start": 788,
        "end": 835,
        "source": "NATIVE_LAYA_PASSAGE_WITH_DETERMINISTIC_SCOPE"
      }
    ],
    "aggregation_reason": "STRONG_CURRENT_RELEVANT_EVIDENCE"
  },
  "whole_notice_scores": {
    "YES": 0.6147,
    "NO": 0.3133,
    "UNKNOWN": 0.072
  },
  "passage_scores": [
    {
      "text": "[Message EL0104C | MT564]",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.9324,
        "NO": 0.0286,
        "UNKNOWN": 0.039
      },
      "score": 0.9324,
      "margin": 0.8934,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "Issuer secretariat memorandum concerning arrangements for the forthcoming extraordinary assembly.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.8912,
        "NO": 0.0831,
        "UNKNOWN": 0.0257
      },
      "score": 0.8912,
      "margin": 0.8081,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "The current agenda is open for shareholder voting instructions.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.7926,
        "NO": 0.1291,
        "UNKNOWN": 0.0782
      },
      "score": 0.7926,
      "margin": 0.6635,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for voting-related immobilisation applies.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.9416,
        "NO": 0.0445,
        "UNKNOWN": 0.0138
      },
      "score": 0.9416,
      "margin": 0.8971,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for an obligatory power-of-attorney document applies.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.8869,
        "NO": 0.0734,
        "UNKNOWN": 0.0397
      },
      "score": 0.8869,
      "margin": 0.8135,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for a required voter registration form applies.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.7931,
        "NO": 0.1483,
        "UNKNOWN": 0.0586
      },
      "score": 0.7931,
      "margin": 0.6448,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "For this vote, beneficial-owner disclosure is required.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.8825,
        "NO": 0.0705,
        "UNKNOWN": 0.047
      },
      "score": 0.8825,
      "margin": 0.8119999999999999,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for documentary confirmation of ownership applies.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.9257,
        "NO": 0.0501,
        "UNKNOWN": 0.0242
      },
      "score": 0.9257,
      "margin": 0.8755999999999999,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for a ban on splitting voting instructions applies.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.9567,
        "NO": 0.0233,
        "UNKNOWN": 0.02
      },
      "score": 0.9567,
      "margin": 0.9334,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for retrieval of loaned voting positions applies.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.8292,
        "NO": 0.1229,
        "UNKNOWN": 0.0479
      },
      "score": 0.8292,
      "margin": 0.7063,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "For this vote, a mandatory paper-only ballot is required.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.9478,
        "NO": 0.0264,
        "UNKNOWN": 0.0258
      },
      "score": 0.9478,
      "margin": 0.9214,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "[Message EL0104D | MT568]",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.9353,
        "NO": 0.0282,
        "UNKNOWN": 0.0365
      },
      "score": 0.9353,
      "margin": 0.8988,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "Please retain the replacement edition for operational reconciliation.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.9104,
        "NO": 0.053,
        "UNKNOWN": 0.0366
      },
      "score": 0.9104,
      "margin": 0.8573999999999999,
      "historical": false,
      "supersession": true,
      "conditional": false
    },
    {
      "text": "Earlier notification conditions are superseded.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.9632,
        "NO": 0.0123,
        "UNKNOWN": 0.0244
      },
      "score": 0.9632,
      "margin": 0.9388,
      "historical": false,
      "supersession": true,
      "conditional": false
    }
  ],
  "escalation": {
    "escalated": true,
    "requested_predicates": [
      "share_blocking",
      "poa_required",
      "registration_required",
      "beneficial_owner_disclosure_required",
      "holding_confirmation_required",
      "split_voting_restricted",
      "securities_lending_recall_required",
      "other_voting_restriction"
    ],
    "reasons": {
      "share_blocking": [
        "LOW_RAW_SCORE"
      ],
      "poa_required": [
        "LOW_RAW_SCORE"
      ],
      "registration_required": [
        "LOW_RAW_SCORE"
      ],
      "beneficial_owner_disclosure_required": [
        "LOW_RAW_SCORE",
        "LOW_MARGIN"
      ],
      "holding_confirmation_required": [
        "LOW_RAW_SCORE"
      ],
      "split_voting_restricted": [
        "LOW_RAW_SCORE"
      ],
      "securities_lending_recall_required": [
        "LOW_RAW_SCORE"
      ],
      "other_voting_restriction": [
        "UNKNOWN",
        "LOW_RAW_SCORE",
        "LOW_MARGIN",
        "EVIDENCE_UNAVAILABLE"
      ]
    }
  },
  "conflicts": [
    "registration_required:MODEL_DISAGREEMENT",
    "registration_required:PASSAGE_CONFLICT",
    "securities_lending_recall_required:MODEL_DISAGREEMENT",
    "securities_lending_recall_required:PASSAGE_CONFLICT",
    "share_blocking:MODEL_DISAGREEMENT",
    "share_blocking:PASSAGE_CONFLICT",
    "split_voting_restricted:MODEL_DISAGREEMENT",
    "split_voting_restricted:PASSAGE_CONFLICT",
    "votability:STRUCTURE_SEMANTIC_CONFLICT"
  ],
  "reconciliation_for_field": [
    {
      "stage": "LLM",
      "rule": "DISAGREEMENT_REVIEW",
      "predicate": "share_blocking",
      "earlier_value": "YES",
      "later_value": "NO",
      "supported": true
    }
  ]
}
```

## VALIDATION / CASCADE_CONSERVATIVE / 2414be60f4dff3cc46dcf385c748749f7c7c3dc05ef8f904052ec9797bdc2f19 / registration_required

```text
[Message EL0104C | MT564]
Issuer secretariat memorandum concerning arrangements for the forthcoming extraordinary assembly.
The current agenda is open for shareholder voting instructions.
No requirement for voting-related immobilisation applies.
No requirement for an obligatory power-of-attorney document applies.
No requirement for a required voter registration form applies.
For this vote, beneficial-owner disclosure is required.
No requirement for documentary confirmation of ownership applies.
No requirement for a ban on splitting voting instructions applies.
No requirement for retrieval of loaned voting positions applies.
For this vote, a mandatory paper-only ballot is required.


[Message EL0104D | MT568]
Please retain the replacement edition for operational reconciliation. Earlier notification conditions are superseded.

```

```json
{
  "truth": "NO",
  "prediction": {
    "value": "UNKNOWN",
    "scores": {
      "YES": 0.871,
      "NO": 0.1085,
      "UNKNOWN": 0.0206
    },
    "native_score": 0.871,
    "confidence": null,
    "source": "UNRESOLVED_MODEL_DISAGREEMENT",
    "evidence": [
      {
        "valid": true,
        "text": "For this vote, a mandatory paper-only ballot is required.",
        "start": 632,
        "end": 689,
        "source": "NATIVE_LAYA_PASSAGE_WITH_DETERMINISTIC_SCOPE"
      }
    ],
    "aggregation_reason": "STRONG_CURRENT_RELEVANT_EVIDENCE"
  },
  "whole_notice_scores": {
    "YES": 0.217,
    "NO": 0.6692,
    "UNKNOWN": 0.1137
  },
  "passage_scores": [
    {
      "text": "[Message EL0104C | MT564]",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.4962,
        "NO": 0.2837,
        "UNKNOWN": 0.2201
      },
      "score": 0.4962,
      "margin": 0.21249999999999997,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "Issuer secretariat memorandum concerning arrangements for the forthcoming extraordinary assembly.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.6038,
        "NO": 0.3606,
        "UNKNOWN": 0.0355
      },
      "score": 0.6038,
      "margin": 0.24320000000000003,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "The current agenda is open for shareholder voting instructions.",
      "state": "UNKNOWN",
      "native_value": "NO",
      "scores": {
        "YES": 0.1833,
        "NO": 0.7071,
        "UNKNOWN": 0.1096
      },
      "score": 0.7071,
      "margin": 0.5237999999999999,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for voting-related immobilisation applies.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.7715,
        "NO": 0.1901,
        "UNKNOWN": 0.0383
      },
      "score": 0.7715,
      "margin": 0.5813999999999999,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for an obligatory power-of-attorney document applies.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.7594,
        "NO": 0.2077,
        "UNKNOWN": 0.0329
      },
      "score": 0.7594,
      "margin": 0.5517,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for a required voter registration form applies.",
      "state": "NEGATIVE",
      "native_value": "NO",
      "scores": {
        "YES": 0.3223,
        "NO": 0.6322,
        "UNKNOWN": 0.0455
      },
      "score": 0.6322,
      "margin": 0.3099,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "For this vote, beneficial-owner disclosure is required.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.5295,
        "NO": 0.388,
        "UNKNOWN": 0.0824
      },
      "score": 0.5295,
      "margin": 0.14149999999999996,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for documentary confirmation of ownership applies.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.5764,
        "NO": 0.3823,
        "UNKNOWN": 0.0413
      },
      "score": 0.5764,
      "margin": 0.19410000000000005,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for a ban on splitting voting instructions applies.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.8032,
        "NO": 0.1731,
        "UNKNOWN": 0.0237
      },
      "score": 0.8032,
      "margin": 0.6301,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for retrieval of loaned voting positions applies.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.5694,
        "NO": 0.3459,
        "UNKNOWN": 0.0847
      },
      "score": 0.5694,
      "margin": 0.22350000000000003,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "For this vote, a mandatory paper-only ballot is required.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.871,
        "NO": 0.1085,
        "UNKNOWN": 0.0206
      },
      "score": 0.871,
      "margin": 0.7625,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "[Message EL0104D | MT568]",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.4486,
        "NO": 0.3003,
        "UNKNOWN": 0.2511
      },
      "score": 0.4486,
      "margin": 0.1483,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "Please retain the replacement edition for operational reconciliation.",
      "state": "UNKNOWN",
      "native_value": "NO",
      "scores": {
        "YES": 0.3889,
        "NO": 0.5066,
        "UNKNOWN": 0.1045
      },
      "score": 0.5066,
      "margin": 0.11770000000000003,
      "historical": false,
      "supersession": true,
      "conditional": false
    },
    {
      "text": "Earlier notification conditions are superseded.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.597,
        "NO": 0.3291,
        "UNKNOWN": 0.0739
      },
      "score": 0.597,
      "margin": 0.26789999999999997,
      "historical": false,
      "supersession": true,
      "conditional": false
    }
  ],
  "escalation": {
    "escalated": true,
    "requested_predicates": [
      "share_blocking",
      "poa_required",
      "registration_required",
      "beneficial_owner_disclosure_required",
      "holding_confirmation_required",
      "split_voting_restricted",
      "securities_lending_recall_required",
      "other_voting_restriction"
    ],
    "reasons": {
      "share_blocking": [
        "LOW_RAW_SCORE"
      ],
      "poa_required": [
        "LOW_RAW_SCORE"
      ],
      "registration_required": [
        "LOW_RAW_SCORE"
      ],
      "beneficial_owner_disclosure_required": [
        "LOW_RAW_SCORE",
        "LOW_MARGIN"
      ],
      "holding_confirmation_required": [
        "LOW_RAW_SCORE"
      ],
      "split_voting_restricted": [
        "LOW_RAW_SCORE"
      ],
      "securities_lending_recall_required": [
        "LOW_RAW_SCORE"
      ],
      "other_voting_restriction": [
        "UNKNOWN",
        "LOW_RAW_SCORE",
        "LOW_MARGIN",
        "EVIDENCE_UNAVAILABLE"
      ]
    }
  },
  "conflicts": [
    "registration_required:MODEL_DISAGREEMENT",
    "registration_required:PASSAGE_CONFLICT",
    "securities_lending_recall_required:MODEL_DISAGREEMENT",
    "securities_lending_recall_required:PASSAGE_CONFLICT",
    "share_blocking:MODEL_DISAGREEMENT",
    "share_blocking:PASSAGE_CONFLICT",
    "split_voting_restricted:MODEL_DISAGREEMENT",
    "split_voting_restricted:PASSAGE_CONFLICT",
    "votability:STRUCTURE_SEMANTIC_CONFLICT"
  ],
  "reconciliation_for_field": [
    {
      "stage": "LLM",
      "rule": "DISAGREEMENT_REVIEW",
      "predicate": "registration_required",
      "earlier_value": "YES",
      "later_value": "NO",
      "supported": true
    }
  ]
}
```

## VALIDATION / CASCADE_CONSERVATIVE / 2414be60f4dff3cc46dcf385c748749f7c7c3dc05ef8f904052ec9797bdc2f19 / split_voting_restricted

```text
[Message EL0104C | MT564]
Issuer secretariat memorandum concerning arrangements for the forthcoming extraordinary assembly.
The current agenda is open for shareholder voting instructions.
No requirement for voting-related immobilisation applies.
No requirement for an obligatory power-of-attorney document applies.
No requirement for a required voter registration form applies.
For this vote, beneficial-owner disclosure is required.
No requirement for documentary confirmation of ownership applies.
No requirement for a ban on splitting voting instructions applies.
No requirement for retrieval of loaned voting positions applies.
For this vote, a mandatory paper-only ballot is required.


[Message EL0104D | MT568]
Please retain the replacement edition for operational reconciliation. Earlier notification conditions are superseded.

```

```json
{
  "truth": "NO",
  "prediction": {
    "value": "UNKNOWN",
    "scores": {
      "YES": 0.8776,
      "NO": 0.0942,
      "UNKNOWN": 0.0282
    },
    "native_score": 0.8776,
    "confidence": null,
    "source": "UNRESOLVED_MODEL_DISAGREEMENT",
    "evidence": [
      {
        "valid": true,
        "text": "No requirement for a ban on splitting voting instructions applies.",
        "start": 500,
        "end": 566,
        "source": "NATIVE_LAYA_PASSAGE_WITH_DETERMINISTIC_SCOPE"
      }
    ],
    "aggregation_reason": "STRONG_CURRENT_RELEVANT_EVIDENCE"
  },
  "whole_notice_scores": {
    "YES": 0.426,
    "NO": 0.5101,
    "UNKNOWN": 0.0639
  },
  "passage_scores": [
    {
      "text": "[Message EL0104C | MT564]",
      "state": "UNKNOWN",
      "native_value": "NO",
      "scores": {
        "YES": 0.2329,
        "NO": 0.4417,
        "UNKNOWN": 0.3254
      },
      "score": 0.4417,
      "margin": 0.11629999999999996,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "Issuer secretariat memorandum concerning arrangements for the forthcoming extraordinary assembly.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.6891,
        "NO": 0.2824,
        "UNKNOWN": 0.0285
      },
      "score": 0.6891,
      "margin": 0.40670000000000006,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "The current agenda is open for shareholder voting instructions.",
      "state": "UNKNOWN",
      "native_value": "NO",
      "scores": {
        "YES": 0.1997,
        "NO": 0.6685,
        "UNKNOWN": 0.1318
      },
      "score": 0.6685,
      "margin": 0.4688,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for voting-related immobilisation applies.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.5293,
        "NO": 0.3713,
        "UNKNOWN": 0.0993
      },
      "score": 0.5293,
      "margin": 0.15799999999999997,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for an obligatory power-of-attorney document applies.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.6168,
        "NO": 0.3047,
        "UNKNOWN": 0.0785
      },
      "score": 0.6168,
      "margin": 0.3121,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for a required voter registration form applies.",
      "state": "UNKNOWN",
      "native_value": "NO",
      "scores": {
        "YES": 0.4632,
        "NO": 0.4702,
        "UNKNOWN": 0.0666
      },
      "score": 0.4702,
      "margin": 0.007000000000000006,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "For this vote, beneficial-owner disclosure is required.",
      "state": "UNKNOWN",
      "native_value": "NO",
      "scores": {
        "YES": 0.3864,
        "NO": 0.5276,
        "UNKNOWN": 0.086
      },
      "score": 0.5276,
      "margin": 0.14119999999999994,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for documentary confirmation of ownership applies.",
      "state": "UNKNOWN",
      "native_value": "NO",
      "scores": {
        "YES": 0.3582,
        "NO": 0.5515,
        "UNKNOWN": 0.0903
      },
      "score": 0.5515,
      "margin": 0.19329999999999997,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for a ban on splitting voting instructions applies.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.8776,
        "NO": 0.0942,
        "UNKNOWN": 0.0282
      },
      "score": 0.8776,
      "margin": 0.7834000000000001,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for retrieval of loaned voting positions applies.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.5739,
        "NO": 0.3204,
        "UNKNOWN": 0.1057
      },
      "score": 0.5739,
      "margin": 0.25349999999999995,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "For this vote, a mandatory paper-only ballot is required.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.8258,
        "NO": 0.1202,
        "UNKNOWN": 0.054
      },
      "score": 0.8258,
      "margin": 0.7056,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "[Message EL0104D | MT568]",
      "state": "UNKNOWN",
      "native_value": "NO",
      "scores": {
        "YES": 0.1755,
        "NO": 0.5197,
        "UNKNOWN": 0.3048
      },
      "score": 0.5197,
      "margin": 0.21490000000000004,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "Please retain the replacement edition for operational reconciliation.",
      "state": "UNKNOWN",
      "native_value": "NO",
      "scores": {
        "YES": 0.1878,
        "NO": 0.7297,
        "UNKNOWN": 0.0824
      },
      "score": 0.7297,
      "margin": 0.5419,
      "historical": false,
      "supersession": true,
      "conditional": false
    },
    {
      "text": "Earlier notification conditions are superseded.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.4973,
        "NO": 0.3914,
        "UNKNOWN": 0.1113
      },
      "score": 0.4973,
      "margin": 0.1059,
      "historical": false,
      "supersession": true,
      "conditional": false
    }
  ],
  "escalation": {
    "escalated": true,
    "requested_predicates": [
      "share_blocking",
      "poa_required",
      "registration_required",
      "beneficial_owner_disclosure_required",
      "holding_confirmation_required",
      "split_voting_restricted",
      "securities_lending_recall_required",
      "other_voting_restriction"
    ],
    "reasons": {
      "share_blocking": [
        "LOW_RAW_SCORE"
      ],
      "poa_required": [
        "LOW_RAW_SCORE"
      ],
      "registration_required": [
        "LOW_RAW_SCORE"
      ],
      "beneficial_owner_disclosure_required": [
        "LOW_RAW_SCORE",
        "LOW_MARGIN"
      ],
      "holding_confirmation_required": [
        "LOW_RAW_SCORE"
      ],
      "split_voting_restricted": [
        "LOW_RAW_SCORE"
      ],
      "securities_lending_recall_required": [
        "LOW_RAW_SCORE"
      ],
      "other_voting_restriction": [
        "UNKNOWN",
        "LOW_RAW_SCORE",
        "LOW_MARGIN",
        "EVIDENCE_UNAVAILABLE"
      ]
    }
  },
  "conflicts": [
    "registration_required:MODEL_DISAGREEMENT",
    "registration_required:PASSAGE_CONFLICT",
    "securities_lending_recall_required:MODEL_DISAGREEMENT",
    "securities_lending_recall_required:PASSAGE_CONFLICT",
    "share_blocking:MODEL_DISAGREEMENT",
    "share_blocking:PASSAGE_CONFLICT",
    "split_voting_restricted:MODEL_DISAGREEMENT",
    "split_voting_restricted:PASSAGE_CONFLICT",
    "votability:STRUCTURE_SEMANTIC_CONFLICT"
  ],
  "reconciliation_for_field": [
    {
      "stage": "LLM",
      "rule": "DISAGREEMENT_REVIEW",
      "predicate": "split_voting_restricted",
      "earlier_value": "YES",
      "later_value": "NO",
      "supported": true
    }
  ]
}
```

## VALIDATION / CASCADE_CONSERVATIVE / 2414be60f4dff3cc46dcf385c748749f7c7c3dc05ef8f904052ec9797bdc2f19 / securities_lending_recall_required

```text
[Message EL0104C | MT564]
Issuer secretariat memorandum concerning arrangements for the forthcoming extraordinary assembly.
The current agenda is open for shareholder voting instructions.
No requirement for voting-related immobilisation applies.
No requirement for an obligatory power-of-attorney document applies.
No requirement for a required voter registration form applies.
For this vote, beneficial-owner disclosure is required.
No requirement for documentary confirmation of ownership applies.
No requirement for a ban on splitting voting instructions applies.
No requirement for retrieval of loaned voting positions applies.
For this vote, a mandatory paper-only ballot is required.


[Message EL0104D | MT568]
Please retain the replacement edition for operational reconciliation. Earlier notification conditions are superseded.

```

```json
{
  "truth": "NO",
  "prediction": {
    "value": "UNKNOWN",
    "scores": {
      "YES": 0.8894,
      "NO": 0.0868,
      "UNKNOWN": 0.0237
    },
    "native_score": 0.8894,
    "confidence": null,
    "source": "UNRESOLVED_MODEL_DISAGREEMENT",
    "evidence": [
      {
        "valid": true,
        "text": "For this vote, a mandatory paper-only ballot is required.",
        "start": 632,
        "end": 689,
        "source": "NATIVE_LAYA_PASSAGE_WITH_DETERMINISTIC_SCOPE"
      }
    ],
    "aggregation_reason": "STRONG_CURRENT_RELEVANT_EVIDENCE"
  },
  "whole_notice_scores": {
    "YES": 0.2468,
    "NO": 0.6654,
    "UNKNOWN": 0.0877
  },
  "passage_scores": [
    {
      "text": "[Message EL0104C | MT564]",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.5459,
        "NO": 0.3059,
        "UNKNOWN": 0.1483
      },
      "score": 0.5459,
      "margin": 0.24000000000000005,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "Issuer secretariat memorandum concerning arrangements for the forthcoming extraordinary assembly.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.5404,
        "NO": 0.3777,
        "UNKNOWN": 0.0819
      },
      "score": 0.5404,
      "margin": 0.1627,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "The current agenda is open for shareholder voting instructions.",
      "state": "UNKNOWN",
      "native_value": "NO",
      "scores": {
        "YES": 0.31,
        "NO": 0.552,
        "UNKNOWN": 0.1381
      },
      "score": 0.552,
      "margin": 0.24200000000000005,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for voting-related immobilisation applies.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.7555,
        "NO": 0.1932,
        "UNKNOWN": 0.0513
      },
      "score": 0.7555,
      "margin": 0.5622999999999999,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for an obligatory power-of-attorney document applies.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.6798,
        "NO": 0.2593,
        "UNKNOWN": 0.0609
      },
      "score": 0.6798,
      "margin": 0.4205,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for a required voter registration form applies.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.5264,
        "NO": 0.3962,
        "UNKNOWN": 0.0774
      },
      "score": 0.5264,
      "margin": 0.13019999999999998,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "For this vote, beneficial-owner disclosure is required.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.616,
        "NO": 0.2656,
        "UNKNOWN": 0.1184
      },
      "score": 0.616,
      "margin": 0.3504,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for documentary confirmation of ownership applies.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.622,
        "NO": 0.2995,
        "UNKNOWN": 0.0785
      },
      "score": 0.622,
      "margin": 0.3225,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for a ban on splitting voting instructions applies.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.7864,
        "NO": 0.1765,
        "UNKNOWN": 0.0371
      },
      "score": 0.7864,
      "margin": 0.6099,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for retrieval of loaned voting positions applies.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.6289,
        "NO": 0.2869,
        "UNKNOWN": 0.0842
      },
      "score": 0.6289,
      "margin": 0.342,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "For this vote, a mandatory paper-only ballot is required.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.8894,
        "NO": 0.0868,
        "UNKNOWN": 0.0237
      },
      "score": 0.8894,
      "margin": 0.8026,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "[Message EL0104D | MT568]",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.5127,
        "NO": 0.3105,
        "UNKNOWN": 0.1768
      },
      "score": 0.5127,
      "margin": 0.20220000000000005,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "Please retain the replacement edition for operational reconciliation.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.5096,
        "NO": 0.375,
        "UNKNOWN": 0.1154
      },
      "score": 0.5096,
      "margin": 0.13460000000000005,
      "historical": false,
      "supersession": true,
      "conditional": false
    },
    {
      "text": "Earlier notification conditions are superseded.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.6434,
        "NO": 0.2655,
        "UNKNOWN": 0.0912
      },
      "score": 0.6434,
      "margin": 0.37789999999999996,
      "historical": false,
      "supersession": true,
      "conditional": false
    }
  ],
  "escalation": {
    "escalated": true,
    "requested_predicates": [
      "share_blocking",
      "poa_required",
      "registration_required",
      "beneficial_owner_disclosure_required",
      "holding_confirmation_required",
      "split_voting_restricted",
      "securities_lending_recall_required",
      "other_voting_restriction"
    ],
    "reasons": {
      "share_blocking": [
        "LOW_RAW_SCORE"
      ],
      "poa_required": [
        "LOW_RAW_SCORE"
      ],
      "registration_required": [
        "LOW_RAW_SCORE"
      ],
      "beneficial_owner_disclosure_required": [
        "LOW_RAW_SCORE",
        "LOW_MARGIN"
      ],
      "holding_confirmation_required": [
        "LOW_RAW_SCORE"
      ],
      "split_voting_restricted": [
        "LOW_RAW_SCORE"
      ],
      "securities_lending_recall_required": [
        "LOW_RAW_SCORE"
      ],
      "other_voting_restriction": [
        "UNKNOWN",
        "LOW_RAW_SCORE",
        "LOW_MARGIN",
        "EVIDENCE_UNAVAILABLE"
      ]
    }
  },
  "conflicts": [
    "registration_required:MODEL_DISAGREEMENT",
    "registration_required:PASSAGE_CONFLICT",
    "securities_lending_recall_required:MODEL_DISAGREEMENT",
    "securities_lending_recall_required:PASSAGE_CONFLICT",
    "share_blocking:MODEL_DISAGREEMENT",
    "share_blocking:PASSAGE_CONFLICT",
    "split_voting_restricted:MODEL_DISAGREEMENT",
    "split_voting_restricted:PASSAGE_CONFLICT",
    "votability:STRUCTURE_SEMANTIC_CONFLICT"
  ],
  "reconciliation_for_field": [
    {
      "stage": "LLM",
      "rule": "DISAGREEMENT_REVIEW",
      "predicate": "securities_lending_recall_required",
      "earlier_value": "YES",
      "later_value": "NO",
      "supported": true
    }
  ]
}
```

## VALIDATION / CASCADE_CONSERVATIVE / 192427e9aa3ca6f904eb505ac724d3c90e8eba48b9c676788a55d6e407fcb195 / expected_final_status

```text
[Message EL0206C | MT564]
Broker service update: the institutional ballot channel is now available for this agenda.
This is solely a cash-distribution advice; it offers no meeting ballot and no shareholder vote.
No requirement for a voting lock on the position applies.
No requirement for a compulsory attorney mandate applies.
No requirement for mandatory meeting registration applies.
No requirement for identification of the underlying owner applies.
No requirement for a custodial holding statement applies.
No requirement for a requirement to cast all votes identically applies.
No requirement for recall of lent securities applies.
No requirement for an in-person-only voting condition applies.


[Message EL0206D | MT568]
Please retain the replacement edition for operational reconciliation. Earlier notification conditions are superseded.

```
```json
{
  "truth": "NOT_VOTABLE",
  "prediction": "UNCERTAIN_MANUAL_REVIEW",
  "decision": {
    "classification": "UNCERTAIN_MANUAL_REVIEW",
    "rule": "R1 unresolved conflicts",
    "rule_version": "semantic-decision-2",
    "manual_review_required": true,
    "automation_enabled": false,
    "review_reasons": [
      "registration_required:MODEL_DISAGREEMENT",
      "registration_required:PASSAGE_CONFLICT",
      "securities_lending_recall_required:MODEL_DISAGREEMENT",
      "securities_lending_recall_required:PASSAGE_CONFLICT",
      "share_blocking:MODEL_DISAGREEMENT",
      "share_blocking:PASSAGE_CONFLICT",
      "Synthetic-only evaluation; customer quality gate not met"
    ]
  },
  "deadline": {
    "status": "OPEN",
    "comparisons": [
      {
        "source": "PROWIDE",
        "field_id": "prowide:9",
        "path": [
          "CAOPTN[1]"
        ],
        "deadline": {
          "iso": "2026-11-24T17:00:00+00:00",
          "offset_known": true,
          "precision": "SECOND"
        },
        "status": "OPEN",
        "field": {
          "components": [
            "RDDT",
            "20261124",
            "170000",
            "000",
            null,
            "00"
          ],
          "end": 226,
          "qualifier": "RDDT",
          "sequence_instance_path": [
            "CAOPTN[1]"
          ],
          "sequence_path": [
            "CAOPTN"
          ],
          "source": "PROWIDE",
          "source_text": ":98E::RDDT//20261124170000,000/00\n",
          "start": 192,
          "tag": "98E",
          "typed_field": "Field98E",
          "value": ":RDDT//20261124170000,000/00"
        }
      }
    ],
    "conflict": false,
    "source": "PROWIDE_COMPONENTS_DETERMINISTIC_COMPARISON",
    "reason": "Only RDDT is controlling. Bare local/date-only values require an agreed timezone profile; no UTC assumption."
  }
}
```

## VALIDATION / CASCADE_CONSERVATIVE / 25150120b9a9e92a98ab8b33fb003cab98a2ec6b4230ec908fda5c15d2bbc7d7 / expected_final_status

```text
[Message EL0105C | MT564]
Issuer secretariat memorandum concerning arrangements for the forthcoming extraordinary assembly.
The current agenda is open for shareholder voting instructions.
No requirement for voting-related immobilisation applies.
No requirement for an obligatory power-of-attorney document applies.
For this vote, a required voter registration form is required.
No requirement for beneficial-owner disclosure applies.
No requirement for documentary confirmation of ownership applies.
No requirement for a ban on splitting voting instructions applies.
For this vote, retrieval of loaned voting positions is required.
No requirement for a mandatory paper-only ballot applies.


[Message EL0105D | MT568]
Please retain the replacement edition for operational reconciliation. Earlier notification conditions are superseded.

```
```json
{
  "truth": "VOTABLE_WITH_RESTRICTION",
  "prediction": "UNCERTAIN_MANUAL_REVIEW",
  "decision": {
    "classification": "UNCERTAIN_MANUAL_REVIEW",
    "rule": "R1 unresolved conflicts",
    "rule_version": "semantic-decision-2",
    "manual_review_required": true,
    "automation_enabled": false,
    "review_reasons": [
      "Message EL0105D states 'Earlier notification conditions are superseded' but does not specify which conditions or provide replacement terms, creating uncertainty about the final operative status of the conditions listed in EL0105C.",
      "share_blocking:MODEL_DISAGREEMENT",
      "share_blocking:PASSAGE_CONFLICT",
      "split_voting_restricted:MODEL_DISAGREEMENT",
      "split_voting_restricted:PASSAGE_CONFLICT",
      "votability:STRUCTURE_SEMANTIC_CONFLICT",
      "Synthetic-only evaluation; customer quality gate not met"
    ]
  },
  "deadline": {
    "status": "OPEN",
    "comparisons": [
      {
        "source": "PROWIDE",
        "field_id": "prowide:10",
        "path": [
          "CAOPTN[1]"
        ],
        "deadline": {
          "iso": "2026-11-24T17:00:00+00:00",
          "offset_known": true,
          "precision": "SECOND"
        },
        "status": "OPEN",
        "field": {
          "components": [
            "RDDT",
            "20261124",
            "170000",
            "000",
            null,
            "00"
          ],
          "end": 243,
          "qualifier": "RDDT",
          "sequence_instance_path": [
            "CAOPTN[1]"
          ],
          "sequence_path": [
            "CAOPTN"
          ],
          "source": "PROWIDE",
          "source_text": ":98E::RDDT//20261124170000,000/00\n",
          "start": 209,
          "tag": "98E",
          "typed_field": "Field98E",
          "value": ":RDDT//20261124170000,000/00"
        }
      }
    ],
    "conflict": false,
    "source": "PROWIDE_COMPONENTS_DETERMINISTIC_COMPARISON",
    "reason": "Only RDDT is controlling. Bare local/date-only values require an agreed timezone profile; no UTC assumption."
  }
}
```

## VALIDATION / CASCADE_CONSERVATIVE / 2414be60f4dff3cc46dcf385c748749f7c7c3dc05ef8f904052ec9797bdc2f19 / expected_final_status

```text
[Message EL0104C | MT564]
Issuer secretariat memorandum concerning arrangements for the forthcoming extraordinary assembly.
The current agenda is open for shareholder voting instructions.
No requirement for voting-related immobilisation applies.
No requirement for an obligatory power-of-attorney document applies.
No requirement for a required voter registration form applies.
For this vote, beneficial-owner disclosure is required.
No requirement for documentary confirmation of ownership applies.
No requirement for a ban on splitting voting instructions applies.
No requirement for retrieval of loaned voting positions applies.
For this vote, a mandatory paper-only ballot is required.


[Message EL0104D | MT568]
Please retain the replacement edition for operational reconciliation. Earlier notification conditions are superseded.

```
```json
{
  "truth": "DEADLINE_PASSED",
  "prediction": "UNCERTAIN_MANUAL_REVIEW",
  "decision": {
    "classification": "UNCERTAIN_MANUAL_REVIEW",
    "rule": "R1 unresolved conflicts",
    "rule_version": "semantic-decision-2",
    "manual_review_required": true,
    "automation_enabled": false,
    "review_reasons": [
      "registration_required:MODEL_DISAGREEMENT",
      "registration_required:PASSAGE_CONFLICT",
      "securities_lending_recall_required:MODEL_DISAGREEMENT",
      "securities_lending_recall_required:PASSAGE_CONFLICT",
      "share_blocking:MODEL_DISAGREEMENT",
      "share_blocking:PASSAGE_CONFLICT",
      "split_voting_restricted:MODEL_DISAGREEMENT",
      "split_voting_restricted:PASSAGE_CONFLICT",
      "votability:STRUCTURE_SEMANTIC_CONFLICT",
      "Synthetic-only evaluation; customer quality gate not met"
    ]
  },
  "deadline": {
    "status": "PASSED",
    "comparisons": [
      {
        "source": "PROWIDE",
        "field_id": "prowide:10",
        "path": [
          "CAOPTN[1]"
        ],
        "deadline": {
          "iso": "2025-09-01T17:00:00+00:00",
          "offset_known": true,
          "precision": "SECOND"
        },
        "status": "PASSED",
        "field": {
          "components": [
            "RDDT",
            "20250901",
            "170000",
            "000",
            null,
            "00"
          ],
          "end": 243,
          "qualifier": "RDDT",
          "sequence_instance_path": [
            "CAOPTN[1]"
          ],
          "sequence_path": [
            "CAOPTN"
          ],
          "source": "PROWIDE",
          "source_text": ":98E::RDDT//20250901170000,000/00\n",
          "start": 209,
          "tag": "98E",
          "typed_field": "Field98E",
          "value": ":RDDT//20250901170000,000/00"
        }
      }
    ],
    "conflict": false,
    "source": "PROWIDE_COMPONENTS_DETERMINISTIC_COMPARISON",
    "reason": "Only RDDT is controlling. Bare local/date-only values require an agreed timezone profile; no UTC assumption."
  }
}
```

## VALIDATION / CASCADE_MODERATE / 192427e9aa3ca6f904eb505ac724d3c90e8eba48b9c676788a55d6e407fcb195 / share_blocking

```text
[Message EL0206C | MT564]
Broker service update: the institutional ballot channel is now available for this agenda.
This is solely a cash-distribution advice; it offers no meeting ballot and no shareholder vote.
No requirement for a voting lock on the position applies.
No requirement for a compulsory attorney mandate applies.
No requirement for mandatory meeting registration applies.
No requirement for identification of the underlying owner applies.
No requirement for a custodial holding statement applies.
No requirement for a requirement to cast all votes identically applies.
No requirement for recall of lent securities applies.
No requirement for an in-person-only voting condition applies.


[Message EL0206D | MT568]
Please retain the replacement edition for operational reconciliation. Earlier notification conditions are superseded.

```

```json
{
  "truth": "NO",
  "prediction": {
    "value": "UNKNOWN",
    "scores": {
      "YES": 0.9632,
      "NO": 0.0123,
      "UNKNOWN": 0.0244
    },
    "native_score": 0.9632,
    "confidence": null,
    "source": "UNRESOLVED_MODEL_DISAGREEMENT",
    "evidence": [
      {
        "valid": true,
        "text": "Earlier notification conditions are superseded.",
        "start": 799,
        "end": 846,
        "source": "NATIVE_LAYA_PASSAGE_WITH_DETERMINISTIC_SCOPE"
      }
    ],
    "aggregation_reason": "STRONG_CURRENT_RELEVANT_EVIDENCE"
  },
  "whole_notice_scores": {
    "YES": 0.8643,
    "NO": 0.0941,
    "UNKNOWN": 0.0416
  },
  "passage_scores": [
    {
      "text": "[Message EL0206C | MT564]",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.9274,
        "NO": 0.0274,
        "UNKNOWN": 0.0452
      },
      "score": 0.9274,
      "margin": 0.8822,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "Broker service update: the institutional ballot channel is now available for this agenda.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.858,
        "NO": 0.08,
        "UNKNOWN": 0.062
      },
      "score": 0.858,
      "margin": 0.778,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "This is solely a cash-distribution advice; it offers no meeting ballot and no shareholder vote.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.9437,
        "NO": 0.0315,
        "UNKNOWN": 0.0248
      },
      "score": 0.9437,
      "margin": 0.9122,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for a voting lock on the position applies.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.86,
        "NO": 0.0962,
        "UNKNOWN": 0.0438
      },
      "score": 0.86,
      "margin": 0.7638,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for a compulsory attorney mandate applies.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.9405,
        "NO": 0.0385,
        "UNKNOWN": 0.021
      },
      "score": 0.9405,
      "margin": 0.902,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for mandatory meeting registration applies.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.9214,
        "NO": 0.041,
        "UNKNOWN": 0.0376
      },
      "score": 0.9214,
      "margin": 0.8804,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for identification of the underlying owner applies.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.9292,
        "NO": 0.0368,
        "UNKNOWN": 0.0341
      },
      "score": 0.9292,
      "margin": 0.8924000000000001,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for a custodial holding statement applies.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.9021,
        "NO": 0.0575,
        "UNKNOWN": 0.0404
      },
      "score": 0.9021,
      "margin": 0.8446,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for a requirement to cast all votes identically applies.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.8764,
        "NO": 0.0703,
        "UNKNOWN": 0.0533
      },
      "score": 0.8764,
      "margin": 0.8060999999999999,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for recall of lent securities applies.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.9214,
        "NO": 0.0467,
        "UNKNOWN": 0.0319
      },
      "score": 0.9214,
      "margin": 0.8747,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for an in-person-only voting condition applies.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.5156,
        "NO": 0.3209,
        "UNKNOWN": 0.1634
      },
      "score": 0.5156,
      "margin": 0.19469999999999993,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "[Message EL0206D | MT568]",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.9297,
        "NO": 0.0283,
        "UNKNOWN": 0.042
      },
      "score": 0.9297,
      "margin": 0.8876999999999999,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "Please retain the replacement edition for operational reconciliation.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.9104,
        "NO": 0.053,
        "UNKNOWN": 0.0366
      },
      "score": 0.9104,
      "margin": 0.8573999999999999,
      "historical": false,
      "supersession": true,
      "conditional": false
    },
    {
      "text": "Earlier notification conditions are superseded.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.9632,
        "NO": 0.0123,
        "UNKNOWN": 0.0244
      },
      "score": 0.9632,
      "margin": 0.9388,
      "historical": false,
      "supersession": true,
      "conditional": false
    }
  ],
  "escalation": {
    "escalated": true,
    "requested_predicates": [
      "votability",
      "share_blocking",
      "poa_required",
      "registration_required",
      "beneficial_owner_disclosure_required",
      "holding_confirmation_required",
      "split_voting_restricted",
      "securities_lending_recall_required",
      "other_voting_restriction"
    ],
    "reasons": {
      "votability": [
        "LOW_RAW_SCORE",
        "LOW_MARGIN"
      ],
      "share_blocking": [
        "LOW_RAW_SCORE"
      ],
      "poa_required": [
        "LOW_RAW_SCORE",
        "LOW_MARGIN"
      ],
      "registration_required": [
        "LOW_RAW_SCORE"
      ],
      "beneficial_owner_disclosure_required": [
        "LOW_RAW_SCORE"
      ],
      "holding_confirmation_required": [
        "UNKNOWN",
        "LOW_RAW_SCORE",
        "LOW_MARGIN",
        "UNSUPPORTED_NEGATIVE"
      ],
      "split_voting_restricted": [
        "UNKNOWN",
        "LOW_RAW_SCORE",
        "LOW_MARGIN",
        "UNSUPPORTED_NEGATIVE"
      ],
      "securities_lending_recall_required": [
        "LOW_RAW_SCORE"
      ],
      "other_voting_restriction": [
        "UNKNOWN",
        "PASSAGE_CONFLICT",
        "LOW_RAW_SCORE",
        "LOW_MARGIN",
        "UNSUPPORTED_NEGATIVE"
      ]
    }
  },
  "conflicts": [
    "registration_required:MODEL_DISAGREEMENT",
    "registration_required:PASSAGE_CONFLICT",
    "securities_lending_recall_required:MODEL_DISAGREEMENT",
    "securities_lending_recall_required:PASSAGE_CONFLICT",
    "share_blocking:MODEL_DISAGREEMENT",
    "share_blocking:PASSAGE_CONFLICT"
  ],
  "reconciliation_for_field": [
    {
      "stage": "LLM",
      "rule": "DISAGREEMENT_REVIEW",
      "predicate": "share_blocking",
      "earlier_value": "YES",
      "later_value": "NO",
      "supported": true
    }
  ]
}
```

## VALIDATION / CASCADE_MODERATE / 192427e9aa3ca6f904eb505ac724d3c90e8eba48b9c676788a55d6e407fcb195 / registration_required

```text
[Message EL0206C | MT564]
Broker service update: the institutional ballot channel is now available for this agenda.
This is solely a cash-distribution advice; it offers no meeting ballot and no shareholder vote.
No requirement for a voting lock on the position applies.
No requirement for a compulsory attorney mandate applies.
No requirement for mandatory meeting registration applies.
No requirement for identification of the underlying owner applies.
No requirement for a custodial holding statement applies.
No requirement for a requirement to cast all votes identically applies.
No requirement for recall of lent securities applies.
No requirement for an in-person-only voting condition applies.


[Message EL0206D | MT568]
Please retain the replacement edition for operational reconciliation. Earlier notification conditions are superseded.

```

```json
{
  "truth": "NO",
  "prediction": {
    "value": "UNKNOWN",
    "scores": {
      "YES": 0.8329,
      "NO": 0.1315,
      "UNKNOWN": 0.0356
    },
    "native_score": 0.8329,
    "confidence": null,
    "source": "UNRESOLVED_MODEL_DISAGREEMENT",
    "evidence": [
      {
        "valid": true,
        "text": "No requirement for a custodial holding statement applies.",
        "start": 454,
        "end": 511,
        "source": "NATIVE_LAYA_PASSAGE_WITH_DETERMINISTIC_SCOPE"
      }
    ],
    "aggregation_reason": "STRONG_CURRENT_RELEVANT_EVIDENCE"
  },
  "whole_notice_scores": {
    "YES": 0.3798,
    "NO": 0.4589,
    "UNKNOWN": 0.1614
  },
  "passage_scores": [
    {
      "text": "[Message EL0206C | MT564]",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.4786,
        "NO": 0.2675,
        "UNKNOWN": 0.2539
      },
      "score": 0.4786,
      "margin": 0.2111,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "Broker service update: the institutional ballot channel is now available for this agenda.",
      "state": "UNKNOWN",
      "native_value": "NO",
      "scores": {
        "YES": 0.3833,
        "NO": 0.4561,
        "UNKNOWN": 0.1606
      },
      "score": 0.4561,
      "margin": 0.07280000000000003,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "This is solely a cash-distribution advice; it offers no meeting ballot and no shareholder vote.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.7642,
        "NO": 0.2014,
        "UNKNOWN": 0.0344
      },
      "score": 0.7642,
      "margin": 0.5628,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for a voting lock on the position applies.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.685,
        "NO": 0.2818,
        "UNKNOWN": 0.0332
      },
      "score": 0.685,
      "margin": 0.40320000000000006,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for a compulsory attorney mandate applies.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.813,
        "NO": 0.1633,
        "UNKNOWN": 0.0237
      },
      "score": 0.813,
      "margin": 0.6496999999999999,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for mandatory meeting registration applies.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.6825,
        "NO": 0.2784,
        "UNKNOWN": 0.0391
      },
      "score": 0.6825,
      "margin": 0.4041,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for identification of the underlying owner applies.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.6885,
        "NO": 0.263,
        "UNKNOWN": 0.0485
      },
      "score": 0.6885,
      "margin": 0.4255,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for a custodial holding statement applies.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.8329,
        "NO": 0.1315,
        "UNKNOWN": 0.0356
      },
      "score": 0.8329,
      "margin": 0.7014,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for a requirement to cast all votes identically applies.",
      "state": "UNKNOWN",
      "native_value": "NO",
      "scores": {
        "YES": 0.3075,
        "NO": 0.6067,
        "UNKNOWN": 0.0858
      },
      "score": 0.6067,
      "margin": 0.2992,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for recall of lent securities applies.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.6795,
        "NO": 0.2704,
        "UNKNOWN": 0.05
      },
      "score": 0.6795,
      "margin": 0.4091,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for an in-person-only voting condition applies.",
      "state": "UNKNOWN",
      "native_value": "NO",
      "scores": {
        "YES": 0.1321,
        "NO": 0.6574,
        "UNKNOWN": 0.2105
      },
      "score": 0.6574,
      "margin": 0.44689999999999996,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "[Message EL0206D | MT568]",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.4527,
        "NO": 0.2911,
        "UNKNOWN": 0.2561
      },
      "score": 0.4527,
      "margin": 0.16159999999999997,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "Please retain the replacement edition for operational reconciliation.",
      "state": "UNKNOWN",
      "native_value": "NO",
      "scores": {
        "YES": 0.3889,
        "NO": 0.5066,
        "UNKNOWN": 0.1045
      },
      "score": 0.5066,
      "margin": 0.11770000000000003,
      "historical": false,
      "supersession": true,
      "conditional": false
    },
    {
      "text": "Earlier notification conditions are superseded.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.597,
        "NO": 0.3291,
        "UNKNOWN": 0.0739
      },
      "score": 0.597,
      "margin": 0.26789999999999997,
      "historical": false,
      "supersession": true,
      "conditional": false
    }
  ],
  "escalation": {
    "escalated": true,
    "requested_predicates": [
      "votability",
      "share_blocking",
      "poa_required",
      "registration_required",
      "beneficial_owner_disclosure_required",
      "holding_confirmation_required",
      "split_voting_restricted",
      "securities_lending_recall_required",
      "other_voting_restriction"
    ],
    "reasons": {
      "votability": [
        "LOW_RAW_SCORE",
        "LOW_MARGIN"
      ],
      "share_blocking": [
        "LOW_RAW_SCORE"
      ],
      "poa_required": [
        "LOW_RAW_SCORE",
        "LOW_MARGIN"
      ],
      "registration_required": [
        "LOW_RAW_SCORE"
      ],
      "beneficial_owner_disclosure_required": [
        "LOW_RAW_SCORE"
      ],
      "holding_confirmation_required": [
        "UNKNOWN",
        "LOW_RAW_SCORE",
        "LOW_MARGIN",
        "UNSUPPORTED_NEGATIVE"
      ],
      "split_voting_restricted": [
        "UNKNOWN",
        "LOW_RAW_SCORE",
        "LOW_MARGIN",
        "UNSUPPORTED_NEGATIVE"
      ],
      "securities_lending_recall_required": [
        "LOW_RAW_SCORE"
      ],
      "other_voting_restriction": [
        "UNKNOWN",
        "PASSAGE_CONFLICT",
        "LOW_RAW_SCORE",
        "LOW_MARGIN",
        "UNSUPPORTED_NEGATIVE"
      ]
    }
  },
  "conflicts": [
    "registration_required:MODEL_DISAGREEMENT",
    "registration_required:PASSAGE_CONFLICT",
    "securities_lending_recall_required:MODEL_DISAGREEMENT",
    "securities_lending_recall_required:PASSAGE_CONFLICT",
    "share_blocking:MODEL_DISAGREEMENT",
    "share_blocking:PASSAGE_CONFLICT"
  ],
  "reconciliation_for_field": [
    {
      "stage": "LLM",
      "rule": "DISAGREEMENT_REVIEW",
      "predicate": "registration_required",
      "earlier_value": "YES",
      "later_value": "NO",
      "supported": true
    }
  ]
}
```

## VALIDATION / CASCADE_MODERATE / 192427e9aa3ca6f904eb505ac724d3c90e8eba48b9c676788a55d6e407fcb195 / securities_lending_recall_required

```text
[Message EL0206C | MT564]
Broker service update: the institutional ballot channel is now available for this agenda.
This is solely a cash-distribution advice; it offers no meeting ballot and no shareholder vote.
No requirement for a voting lock on the position applies.
No requirement for a compulsory attorney mandate applies.
No requirement for mandatory meeting registration applies.
No requirement for identification of the underlying owner applies.
No requirement for a custodial holding statement applies.
No requirement for a requirement to cast all votes identically applies.
No requirement for recall of lent securities applies.
No requirement for an in-person-only voting condition applies.


[Message EL0206D | MT568]
Please retain the replacement edition for operational reconciliation. Earlier notification conditions are superseded.

```

```json
{
  "truth": "NO",
  "prediction": {
    "value": "UNKNOWN",
    "scores": {
      "YES": 0.8045,
      "NO": 0.1563,
      "UNKNOWN": 0.0393
    },
    "native_score": 0.8045,
    "confidence": null,
    "source": "UNRESOLVED_MODEL_DISAGREEMENT",
    "evidence": [
      {
        "valid": true,
        "text": "No requirement for a custodial holding statement applies.",
        "start": 454,
        "end": 511,
        "source": "NATIVE_LAYA_PASSAGE_WITH_DETERMINISTIC_SCOPE"
      }
    ],
    "aggregation_reason": "STRONG_CURRENT_RELEVANT_EVIDENCE"
  },
  "whole_notice_scores": {
    "YES": 0.4992,
    "NO": 0.4082,
    "UNKNOWN": 0.0926
  },
  "passage_scores": [
    {
      "text": "[Message EL0206C | MT564]",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.5572,
        "NO": 0.2849,
        "UNKNOWN": 0.1579
      },
      "score": 0.5572,
      "margin": 0.27230000000000004,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "Broker service update: the institutional ballot channel is now available for this agenda.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.5641,
        "NO": 0.2808,
        "UNKNOWN": 0.1551
      },
      "score": 0.5641,
      "margin": 0.28330000000000005,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "This is solely a cash-distribution advice; it offers no meeting ballot and no shareholder vote.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.6127,
        "NO": 0.3202,
        "UNKNOWN": 0.0671
      },
      "score": 0.6127,
      "margin": 0.29250000000000004,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for a voting lock on the position applies.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.7005,
        "NO": 0.2407,
        "UNKNOWN": 0.0588
      },
      "score": 0.7005,
      "margin": 0.4598,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for a compulsory attorney mandate applies.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.6965,
        "NO": 0.2437,
        "UNKNOWN": 0.0598
      },
      "score": 0.6965,
      "margin": 0.4528,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for mandatory meeting registration applies.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.6962,
        "NO": 0.2351,
        "UNKNOWN": 0.0687
      },
      "score": 0.6962,
      "margin": 0.46110000000000007,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for identification of the underlying owner applies.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.6681,
        "NO": 0.2491,
        "UNKNOWN": 0.0828
      },
      "score": 0.6681,
      "margin": 0.41900000000000004,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for a custodial holding statement applies.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.8045,
        "NO": 0.1563,
        "UNKNOWN": 0.0393
      },
      "score": 0.8045,
      "margin": 0.6482,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for a requirement to cast all votes identically applies.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.4843,
        "NO": 0.442,
        "UNKNOWN": 0.0737
      },
      "score": 0.4843,
      "margin": 0.042300000000000004,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for recall of lent securities applies.",
      "state": "NEGATIVE",
      "native_value": "NO",
      "scores": {
        "YES": 0.3439,
        "NO": 0.6291,
        "UNKNOWN": 0.0271
      },
      "score": 0.6291,
      "margin": 0.2852,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for an in-person-only voting condition applies.",
      "state": "UNKNOWN",
      "native_value": "NO",
      "scores": {
        "YES": 0.2737,
        "NO": 0.547,
        "UNKNOWN": 0.1794
      },
      "score": 0.547,
      "margin": 0.27330000000000004,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "[Message EL0206D | MT568]",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.5434,
        "NO": 0.2793,
        "UNKNOWN": 0.1772
      },
      "score": 0.5434,
      "margin": 0.2641,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "Please retain the replacement edition for operational reconciliation.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.5096,
        "NO": 0.375,
        "UNKNOWN": 0.1154
      },
      "score": 0.5096,
      "margin": 0.13460000000000005,
      "historical": false,
      "supersession": true,
      "conditional": false
    },
    {
      "text": "Earlier notification conditions are superseded.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.6434,
        "NO": 0.2655,
        "UNKNOWN": 0.0912
      },
      "score": 0.6434,
      "margin": 0.37789999999999996,
      "historical": false,
      "supersession": true,
      "conditional": false
    }
  ],
  "escalation": {
    "escalated": true,
    "requested_predicates": [
      "votability",
      "share_blocking",
      "poa_required",
      "registration_required",
      "beneficial_owner_disclosure_required",
      "holding_confirmation_required",
      "split_voting_restricted",
      "securities_lending_recall_required",
      "other_voting_restriction"
    ],
    "reasons": {
      "votability": [
        "LOW_RAW_SCORE",
        "LOW_MARGIN"
      ],
      "share_blocking": [
        "LOW_RAW_SCORE"
      ],
      "poa_required": [
        "LOW_RAW_SCORE",
        "LOW_MARGIN"
      ],
      "registration_required": [
        "LOW_RAW_SCORE"
      ],
      "beneficial_owner_disclosure_required": [
        "LOW_RAW_SCORE"
      ],
      "holding_confirmation_required": [
        "UNKNOWN",
        "LOW_RAW_SCORE",
        "LOW_MARGIN",
        "UNSUPPORTED_NEGATIVE"
      ],
      "split_voting_restricted": [
        "UNKNOWN",
        "LOW_RAW_SCORE",
        "LOW_MARGIN",
        "UNSUPPORTED_NEGATIVE"
      ],
      "securities_lending_recall_required": [
        "LOW_RAW_SCORE"
      ],
      "other_voting_restriction": [
        "UNKNOWN",
        "PASSAGE_CONFLICT",
        "LOW_RAW_SCORE",
        "LOW_MARGIN",
        "UNSUPPORTED_NEGATIVE"
      ]
    }
  },
  "conflicts": [
    "registration_required:MODEL_DISAGREEMENT",
    "registration_required:PASSAGE_CONFLICT",
    "securities_lending_recall_required:MODEL_DISAGREEMENT",
    "securities_lending_recall_required:PASSAGE_CONFLICT",
    "share_blocking:MODEL_DISAGREEMENT",
    "share_blocking:PASSAGE_CONFLICT"
  ],
  "reconciliation_for_field": [
    {
      "stage": "LLM",
      "rule": "DISAGREEMENT_REVIEW",
      "predicate": "securities_lending_recall_required",
      "earlier_value": "YES",
      "later_value": "NO",
      "supported": true
    }
  ]
}
```

## VALIDATION / CASCADE_MODERATE / 255328bb369bd44fa7cb0a788d797be6085e4bdab88a810f35f8b14469f269d2 / votability

```text
[Message EL0107C | MT564]
Issuer secretariat memorandum concerning arrangements for the forthcoming extraordinary assembly.
Participation may become possible, but the agent has not established whether this holder can vote.
For this vote, voting-related immobilisation is required.
The receiving agent has not resolved whether an obligatory power-of-attorney document is required for this vote.
No requirement for a required voter registration form applies.
No requirement for beneficial-owner disclosure applies.
For this vote, documentary confirmation of ownership is required.
No requirement for a ban on splitting voting instructions applies.
No requirement for retrieval of loaned voting positions applies.
No requirement for a mandatory paper-only ballot applies.


[Message EL0107D | MT568]
Please retain the replacement edition for operational reconciliation. Earlier notification conditions are superseded.

```

```json
{
  "truth": "UNCERTAIN",
  "prediction": {
    "value": "NOT_VOTABLE",
    "scores": {
      "VOTABLE": 0.1913,
      "NOT_VOTABLE": 0.5411,
      "UNCERTAIN": 0.2676
    },
    "native_score": 0.5411,
    "confidence": null,
    "source": "REGISTERED_LAYA_WHOLE_NOTICE",
    "evidence": [
      {
        "valid": true,
        "normalisation": "identity",
        "text": "[Message EL0107C | MT564]",
        "start": 0,
        "end": 25,
        "source": "MATCHING_NATIVE_PASSAGE"
      }
    ]
  },
  "whole_notice_scores": null,
  "passage_scores": [],
  "escalation": {
    "escalated": true,
    "requested_predicates": [
      "votability",
      "share_blocking",
      "poa_required",
      "registration_required",
      "holding_confirmation_required",
      "split_voting_restricted",
      "securities_lending_recall_required",
      "other_voting_restriction"
    ],
    "reasons": {
      "votability": [
        "LOW_RAW_SCORE",
        "LOW_MARGIN"
      ],
      "share_blocking": [
        "LOW_RAW_SCORE"
      ],
      "poa_required": [
        "UNKNOWN",
        "LOW_RAW_SCORE",
        "LOW_MARGIN",
        "UNSUPPORTED_NEGATIVE"
      ],
      "registration_required": [
        "LOW_RAW_SCORE"
      ],
      "holding_confirmation_required": [
        "LOW_RAW_SCORE"
      ],
      "split_voting_restricted": [
        "LOW_RAW_SCORE"
      ],
      "securities_lending_recall_required": [
        "LOW_RAW_SCORE"
      ],
      "other_voting_restriction": [
        "LOW_RAW_SCORE"
      ]
    }
  },
  "conflicts": [
    "The agent has not established whether this holder can vote.",
    "The receiving agent has not resolved whether an obligatory power-of-attorney document is required for this vote.",
    "registration_required:MODEL_DISAGREEMENT",
    "registration_required:PASSAGE_CONFLICT",
    "securities_lending_recall_required:MODEL_DISAGREEMENT",
    "securities_lending_recall_required:PASSAGE_CONFLICT",
    "split_voting_restricted:MODEL_DISAGREEMENT",
    "split_voting_restricted:PASSAGE_CONFLICT"
  ],
  "reconciliation_for_field": [
    {
      "stage": "LLM",
      "rule": "LATER_ABSTENTION",
      "predicate": "votability",
      "supported": false
    }
  ]
}
```

## VALIDATION / CASCADE_MODERATE / 255328bb369bd44fa7cb0a788d797be6085e4bdab88a810f35f8b14469f269d2 / registration_required

```text
[Message EL0107C | MT564]
Issuer secretariat memorandum concerning arrangements for the forthcoming extraordinary assembly.
Participation may become possible, but the agent has not established whether this holder can vote.
For this vote, voting-related immobilisation is required.
The receiving agent has not resolved whether an obligatory power-of-attorney document is required for this vote.
No requirement for a required voter registration form applies.
No requirement for beneficial-owner disclosure applies.
For this vote, documentary confirmation of ownership is required.
No requirement for a ban on splitting voting instructions applies.
No requirement for retrieval of loaned voting positions applies.
No requirement for a mandatory paper-only ballot applies.


[Message EL0107D | MT568]
Please retain the replacement edition for operational reconciliation. Earlier notification conditions are superseded.

```

```json
{
  "truth": "NO",
  "prediction": {
    "value": "UNKNOWN",
    "scores": {
      "YES": 0.8479,
      "NO": 0.082,
      "UNKNOWN": 0.0701
    },
    "native_score": 0.8479,
    "confidence": null,
    "source": "UNRESOLVED_MODEL_DISAGREEMENT",
    "evidence": [
      {
        "valid": true,
        "text": "The receiving agent has not resolved whether an obligatory power-of-attorney document is required for this vote.",
        "start": 281,
        "end": 393,
        "source": "NATIVE_LAYA_PASSAGE_WITH_DETERMINISTIC_SCOPE"
      }
    ],
    "aggregation_reason": "STRONG_CURRENT_RELEVANT_EVIDENCE"
  },
  "whole_notice_scores": {
    "YES": 0.1461,
    "NO": 0.8218,
    "UNKNOWN": 0.032
  },
  "passage_scores": [
    {
      "text": "[Message EL0107C | MT564]",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.4683,
        "NO": 0.3075,
        "UNKNOWN": 0.2242
      },
      "score": 0.4683,
      "margin": 0.1608,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "Issuer secretariat memorandum concerning arrangements for the forthcoming extraordinary assembly.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.6038,
        "NO": 0.3606,
        "UNKNOWN": 0.0355
      },
      "score": 0.6038,
      "margin": 0.24320000000000003,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "Participation may become possible, but the agent has not established whether this holder can vote.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.6385,
        "NO": 0.2578,
        "UNKNOWN": 0.1037
      },
      "score": 0.6385,
      "margin": 0.3807,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "For this vote, voting-related immobilisation is required.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.5601,
        "NO": 0.3592,
        "UNKNOWN": 0.0807
      },
      "score": 0.5601,
      "margin": 0.20090000000000002,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "The receiving agent has not resolved whether an obligatory power-of-attorney document is required for this vote.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.8479,
        "NO": 0.082,
        "UNKNOWN": 0.0701
      },
      "score": 0.8479,
      "margin": 0.7659,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for a required voter registration form applies.",
      "state": "NEGATIVE",
      "native_value": "NO",
      "scores": {
        "YES": 0.3223,
        "NO": 0.6322,
        "UNKNOWN": 0.0455
      },
      "score": 0.6322,
      "margin": 0.3099,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for beneficial-owner disclosure applies.",
      "state": "UNKNOWN",
      "native_value": "NO",
      "scores": {
        "YES": 0.3614,
        "NO": 0.5935,
        "UNKNOWN": 0.0451
      },
      "score": 0.5935,
      "margin": 0.23210000000000003,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "For this vote, documentary confirmation of ownership is required.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.8133,
        "NO": 0.129,
        "UNKNOWN": 0.0577
      },
      "score": 0.8133,
      "margin": 0.6843,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for a ban on splitting voting instructions applies.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.8032,
        "NO": 0.1731,
        "UNKNOWN": 0.0237
      },
      "score": 0.8032,
      "margin": 0.6301,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for retrieval of loaned voting positions applies.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.5694,
        "NO": 0.3459,
        "UNKNOWN": 0.0847
      },
      "score": 0.5694,
      "margin": 0.22350000000000003,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for a mandatory paper-only ballot applies.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.624,
        "NO": 0.3461,
        "UNKNOWN": 0.0299
      },
      "score": 0.624,
      "margin": 0.2779,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "[Message EL0107D | MT568]",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.4165,
        "NO": 0.3356,
        "UNKNOWN": 0.2478
      },
      "score": 0.4165,
      "margin": 0.08089999999999997,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "Please retain the replacement edition for operational reconciliation.",
      "state": "UNKNOWN",
      "native_value": "NO",
      "scores": {
        "YES": 0.3889,
        "NO": 0.5066,
        "UNKNOWN": 0.1045
      },
      "score": 0.5066,
      "margin": 0.11770000000000003,
      "historical": false,
      "supersession": true,
      "conditional": false
    },
    {
      "text": "Earlier notification conditions are superseded.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.597,
        "NO": 0.3291,
        "UNKNOWN": 0.0739
      },
      "score": 0.597,
      "margin": 0.26789999999999997,
      "historical": false,
      "supersession": true,
      "conditional": false
    }
  ],
  "escalation": {
    "escalated": true,
    "requested_predicates": [
      "votability",
      "share_blocking",
      "poa_required",
      "registration_required",
      "holding_confirmation_required",
      "split_voting_restricted",
      "securities_lending_recall_required",
      "other_voting_restriction"
    ],
    "reasons": {
      "votability": [
        "LOW_RAW_SCORE",
        "LOW_MARGIN"
      ],
      "share_blocking": [
        "LOW_RAW_SCORE"
      ],
      "poa_required": [
        "UNKNOWN",
        "LOW_RAW_SCORE",
        "LOW_MARGIN",
        "UNSUPPORTED_NEGATIVE"
      ],
      "registration_required": [
        "LOW_RAW_SCORE"
      ],
      "holding_confirmation_required": [
        "LOW_RAW_SCORE"
      ],
      "split_voting_restricted": [
        "LOW_RAW_SCORE"
      ],
      "securities_lending_recall_required": [
        "LOW_RAW_SCORE"
      ],
      "other_voting_restriction": [
        "LOW_RAW_SCORE"
      ]
    }
  },
  "conflicts": [
    "The agent has not established whether this holder can vote.",
    "The receiving agent has not resolved whether an obligatory power-of-attorney document is required for this vote.",
    "registration_required:MODEL_DISAGREEMENT",
    "registration_required:PASSAGE_CONFLICT",
    "securities_lending_recall_required:MODEL_DISAGREEMENT",
    "securities_lending_recall_required:PASSAGE_CONFLICT",
    "split_voting_restricted:MODEL_DISAGREEMENT",
    "split_voting_restricted:PASSAGE_CONFLICT"
  ],
  "reconciliation_for_field": [
    {
      "stage": "LLM",
      "rule": "DISAGREEMENT_REVIEW",
      "predicate": "registration_required",
      "earlier_value": "YES",
      "later_value": "NO",
      "supported": true
    }
  ]
}
```

## VALIDATION / CASCADE_MODERATE / 255328bb369bd44fa7cb0a788d797be6085e4bdab88a810f35f8b14469f269d2 / split_voting_restricted

```text
[Message EL0107C | MT564]
Issuer secretariat memorandum concerning arrangements for the forthcoming extraordinary assembly.
Participation may become possible, but the agent has not established whether this holder can vote.
For this vote, voting-related immobilisation is required.
The receiving agent has not resolved whether an obligatory power-of-attorney document is required for this vote.
No requirement for a required voter registration form applies.
No requirement for beneficial-owner disclosure applies.
For this vote, documentary confirmation of ownership is required.
No requirement for a ban on splitting voting instructions applies.
No requirement for retrieval of loaned voting positions applies.
No requirement for a mandatory paper-only ballot applies.


[Message EL0107D | MT568]
Please retain the replacement edition for operational reconciliation. Earlier notification conditions are superseded.

```

```json
{
  "truth": "NO",
  "prediction": {
    "value": "UNKNOWN",
    "scores": {
      "YES": 0.8776,
      "NO": 0.0942,
      "UNKNOWN": 0.0282
    },
    "native_score": 0.8776,
    "confidence": null,
    "source": "UNRESOLVED_MODEL_DISAGREEMENT",
    "evidence": [
      {
        "valid": true,
        "text": "No requirement for a ban on splitting voting instructions applies.",
        "start": 579,
        "end": 645,
        "source": "NATIVE_LAYA_PASSAGE_WITH_DETERMINISTIC_SCOPE"
      }
    ],
    "aggregation_reason": "STRONG_CURRENT_RELEVANT_EVIDENCE"
  },
  "whole_notice_scores": {
    "YES": 0.2907,
    "NO": 0.6729,
    "UNKNOWN": 0.0363
  },
  "passage_scores": [
    {
      "text": "[Message EL0107C | MT564]",
      "state": "UNKNOWN",
      "native_value": "NO",
      "scores": {
        "YES": 0.2059,
        "NO": 0.4621,
        "UNKNOWN": 0.332
      },
      "score": 0.4621,
      "margin": 0.1301,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "Issuer secretariat memorandum concerning arrangements for the forthcoming extraordinary assembly.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.6891,
        "NO": 0.2824,
        "UNKNOWN": 0.0285
      },
      "score": 0.6891,
      "margin": 0.40670000000000006,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "Participation may become possible, but the agent has not established whether this holder can vote.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.4281,
        "NO": 0.3666,
        "UNKNOWN": 0.2053
      },
      "score": 0.4281,
      "margin": 0.0615,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "For this vote, voting-related immobilisation is required.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.739,
        "NO": 0.1797,
        "UNKNOWN": 0.0813
      },
      "score": 0.739,
      "margin": 0.5593,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "The receiving agent has not resolved whether an obligatory power-of-attorney document is required for this vote.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.7723,
        "NO": 0.1186,
        "UNKNOWN": 0.1091
      },
      "score": 0.7723,
      "margin": 0.6537,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for a required voter registration form applies.",
      "state": "UNKNOWN",
      "native_value": "NO",
      "scores": {
        "YES": 0.4632,
        "NO": 0.4702,
        "UNKNOWN": 0.0666
      },
      "score": 0.4702,
      "margin": 0.007000000000000006,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for beneficial-owner disclosure applies.",
      "state": "UNKNOWN",
      "native_value": "NO",
      "scores": {
        "YES": 0.1339,
        "NO": 0.7214,
        "UNKNOWN": 0.1447
      },
      "score": 0.7214,
      "margin": 0.5767,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "For this vote, documentary confirmation of ownership is required.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.7301,
        "NO": 0.1693,
        "UNKNOWN": 0.1006
      },
      "score": 0.7301,
      "margin": 0.5608,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for a ban on splitting voting instructions applies.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.8776,
        "NO": 0.0942,
        "UNKNOWN": 0.0282
      },
      "score": 0.8776,
      "margin": 0.7834000000000001,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for retrieval of loaned voting positions applies.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.5739,
        "NO": 0.3204,
        "UNKNOWN": 0.1057
      },
      "score": 0.5739,
      "margin": 0.25349999999999995,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for a mandatory paper-only ballot applies.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.513,
        "NO": 0.4345,
        "UNKNOWN": 0.0525
      },
      "score": 0.513,
      "margin": 0.07850000000000001,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "[Message EL0107D | MT568]",
      "state": "UNKNOWN",
      "native_value": "NO",
      "scores": {
        "YES": 0.1092,
        "NO": 0.6218,
        "UNKNOWN": 0.269
      },
      "score": 0.6218,
      "margin": 0.3528,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "Please retain the replacement edition for operational reconciliation.",
      "state": "UNKNOWN",
      "native_value": "NO",
      "scores": {
        "YES": 0.1878,
        "NO": 0.7297,
        "UNKNOWN": 0.0824
      },
      "score": 0.7297,
      "margin": 0.5419,
      "historical": false,
      "supersession": true,
      "conditional": false
    },
    {
      "text": "Earlier notification conditions are superseded.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.4973,
        "NO": 0.3914,
        "UNKNOWN": 0.1113
      },
      "score": 0.4973,
      "margin": 0.1059,
      "historical": false,
      "supersession": true,
      "conditional": false
    }
  ],
  "escalation": {
    "escalated": true,
    "requested_predicates": [
      "votability",
      "share_blocking",
      "poa_required",
      "registration_required",
      "holding_confirmation_required",
      "split_voting_restricted",
      "securities_lending_recall_required",
      "other_voting_restriction"
    ],
    "reasons": {
      "votability": [
        "LOW_RAW_SCORE",
        "LOW_MARGIN"
      ],
      "share_blocking": [
        "LOW_RAW_SCORE"
      ],
      "poa_required": [
        "UNKNOWN",
        "LOW_RAW_SCORE",
        "LOW_MARGIN",
        "UNSUPPORTED_NEGATIVE"
      ],
      "registration_required": [
        "LOW_RAW_SCORE"
      ],
      "holding_confirmation_required": [
        "LOW_RAW_SCORE"
      ],
      "split_voting_restricted": [
        "LOW_RAW_SCORE"
      ],
      "securities_lending_recall_required": [
        "LOW_RAW_SCORE"
      ],
      "other_voting_restriction": [
        "LOW_RAW_SCORE"
      ]
    }
  },
  "conflicts": [
    "The agent has not established whether this holder can vote.",
    "The receiving agent has not resolved whether an obligatory power-of-attorney document is required for this vote.",
    "registration_required:MODEL_DISAGREEMENT",
    "registration_required:PASSAGE_CONFLICT",
    "securities_lending_recall_required:MODEL_DISAGREEMENT",
    "securities_lending_recall_required:PASSAGE_CONFLICT",
    "split_voting_restricted:MODEL_DISAGREEMENT",
    "split_voting_restricted:PASSAGE_CONFLICT"
  ],
  "reconciliation_for_field": [
    {
      "stage": "LLM",
      "rule": "DISAGREEMENT_REVIEW",
      "predicate": "split_voting_restricted",
      "earlier_value": "YES",
      "later_value": "NO",
      "supported": true
    }
  ]
}
```

## VALIDATION / CASCADE_MODERATE / 255328bb369bd44fa7cb0a788d797be6085e4bdab88a810f35f8b14469f269d2 / securities_lending_recall_required

```text
[Message EL0107C | MT564]
Issuer secretariat memorandum concerning arrangements for the forthcoming extraordinary assembly.
Participation may become possible, but the agent has not established whether this holder can vote.
For this vote, voting-related immobilisation is required.
The receiving agent has not resolved whether an obligatory power-of-attorney document is required for this vote.
No requirement for a required voter registration form applies.
No requirement for beneficial-owner disclosure applies.
For this vote, documentary confirmation of ownership is required.
No requirement for a ban on splitting voting instructions applies.
No requirement for retrieval of loaned voting positions applies.
No requirement for a mandatory paper-only ballot applies.


[Message EL0107D | MT568]
Please retain the replacement edition for operational reconciliation. Earlier notification conditions are superseded.

```

```json
{
  "truth": "NO",
  "prediction": {
    "value": "UNKNOWN",
    "scores": {
      "YES": 0.7864,
      "NO": 0.1765,
      "UNKNOWN": 0.0371
    },
    "native_score": 0.7864,
    "confidence": null,
    "source": "UNRESOLVED_MODEL_DISAGREEMENT",
    "evidence": [
      {
        "valid": true,
        "text": "No requirement for a ban on splitting voting instructions applies.",
        "start": 579,
        "end": 645,
        "source": "NATIVE_LAYA_PASSAGE_WITH_DETERMINISTIC_SCOPE"
      }
    ],
    "aggregation_reason": "STRONG_CURRENT_RELEVANT_EVIDENCE"
  },
  "whole_notice_scores": {
    "YES": 0.2336,
    "NO": 0.7251,
    "UNKNOWN": 0.0413
  },
  "passage_scores": [
    {
      "text": "[Message EL0107C | MT564]",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.537,
        "NO": 0.3061,
        "UNKNOWN": 0.157
      },
      "score": 0.537,
      "margin": 0.23090000000000005,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "Issuer secretariat memorandum concerning arrangements for the forthcoming extraordinary assembly.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.5404,
        "NO": 0.3777,
        "UNKNOWN": 0.0819
      },
      "score": 0.5404,
      "margin": 0.1627,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "Participation may become possible, but the agent has not established whether this holder can vote.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.5427,
        "NO": 0.3087,
        "UNKNOWN": 0.1486
      },
      "score": 0.5427,
      "margin": 0.23399999999999999,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "For this vote, voting-related immobilisation is required.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.7666,
        "NO": 0.1556,
        "UNKNOWN": 0.0779
      },
      "score": 0.7666,
      "margin": 0.611,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "The receiving agent has not resolved whether an obligatory power-of-attorney document is required for this vote.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.7425,
        "NO": 0.1586,
        "UNKNOWN": 0.0988
      },
      "score": 0.7425,
      "margin": 0.5839000000000001,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for a required voter registration form applies.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.5264,
        "NO": 0.3962,
        "UNKNOWN": 0.0774
      },
      "score": 0.5264,
      "margin": 0.13019999999999998,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for beneficial-owner disclosure applies.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.5311,
        "NO": 0.3741,
        "UNKNOWN": 0.0948
      },
      "score": 0.5311,
      "margin": 0.15700000000000003,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "For this vote, documentary confirmation of ownership is required.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.7744,
        "NO": 0.1381,
        "UNKNOWN": 0.0874
      },
      "score": 0.7744,
      "margin": 0.6363,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for a ban on splitting voting instructions applies.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.7864,
        "NO": 0.1765,
        "UNKNOWN": 0.0371
      },
      "score": 0.7864,
      "margin": 0.6099,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for retrieval of loaned voting positions applies.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.6289,
        "NO": 0.2869,
        "UNKNOWN": 0.0842
      },
      "score": 0.6289,
      "margin": 0.342,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for a mandatory paper-only ballot applies.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.7254,
        "NO": 0.2372,
        "UNKNOWN": 0.0374
      },
      "score": 0.7254,
      "margin": 0.4882000000000001,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "[Message EL0107D | MT568]",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.5104,
        "NO": 0.3234,
        "UNKNOWN": 0.1661
      },
      "score": 0.5104,
      "margin": 0.18699999999999994,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "Please retain the replacement edition for operational reconciliation.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.5096,
        "NO": 0.375,
        "UNKNOWN": 0.1154
      },
      "score": 0.5096,
      "margin": 0.13460000000000005,
      "historical": false,
      "supersession": true,
      "conditional": false
    },
    {
      "text": "Earlier notification conditions are superseded.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.6434,
        "NO": 0.2655,
        "UNKNOWN": 0.0912
      },
      "score": 0.6434,
      "margin": 0.37789999999999996,
      "historical": false,
      "supersession": true,
      "conditional": false
    }
  ],
  "escalation": {
    "escalated": true,
    "requested_predicates": [
      "votability",
      "share_blocking",
      "poa_required",
      "registration_required",
      "holding_confirmation_required",
      "split_voting_restricted",
      "securities_lending_recall_required",
      "other_voting_restriction"
    ],
    "reasons": {
      "votability": [
        "LOW_RAW_SCORE",
        "LOW_MARGIN"
      ],
      "share_blocking": [
        "LOW_RAW_SCORE"
      ],
      "poa_required": [
        "UNKNOWN",
        "LOW_RAW_SCORE",
        "LOW_MARGIN",
        "UNSUPPORTED_NEGATIVE"
      ],
      "registration_required": [
        "LOW_RAW_SCORE"
      ],
      "holding_confirmation_required": [
        "LOW_RAW_SCORE"
      ],
      "split_voting_restricted": [
        "LOW_RAW_SCORE"
      ],
      "securities_lending_recall_required": [
        "LOW_RAW_SCORE"
      ],
      "other_voting_restriction": [
        "LOW_RAW_SCORE"
      ]
    }
  },
  "conflicts": [
    "The agent has not established whether this holder can vote.",
    "The receiving agent has not resolved whether an obligatory power-of-attorney document is required for this vote.",
    "registration_required:MODEL_DISAGREEMENT",
    "registration_required:PASSAGE_CONFLICT",
    "securities_lending_recall_required:MODEL_DISAGREEMENT",
    "securities_lending_recall_required:PASSAGE_CONFLICT",
    "split_voting_restricted:MODEL_DISAGREEMENT",
    "split_voting_restricted:PASSAGE_CONFLICT"
  ],
  "reconciliation_for_field": [
    {
      "stage": "LLM",
      "rule": "DISAGREEMENT_REVIEW",
      "predicate": "securities_lending_recall_required",
      "earlier_value": "YES",
      "later_value": "NO",
      "supported": true
    }
  ]
}
```

## VALIDATION / CASCADE_MODERATE / 25150120b9a9e92a98ab8b33fb003cab98a2ec6b4230ec908fda5c15d2bbc7d7 / share_blocking

```text
[Message EL0105C | MT564]
Issuer secretariat memorandum concerning arrangements for the forthcoming extraordinary assembly.
The current agenda is open for shareholder voting instructions.
No requirement for voting-related immobilisation applies.
No requirement for an obligatory power-of-attorney document applies.
For this vote, a required voter registration form is required.
No requirement for beneficial-owner disclosure applies.
No requirement for documentary confirmation of ownership applies.
No requirement for a ban on splitting voting instructions applies.
For this vote, retrieval of loaned voting positions is required.
No requirement for a mandatory paper-only ballot applies.


[Message EL0105D | MT568]
Please retain the replacement edition for operational reconciliation. Earlier notification conditions are superseded.

```

```json
{
  "truth": "NO",
  "prediction": {
    "value": "UNKNOWN",
    "scores": {
      "YES": 0.9632,
      "NO": 0.0123,
      "UNKNOWN": 0.0244
    },
    "native_score": 0.9632,
    "confidence": null,
    "source": "UNRESOLVED_MODEL_DISAGREEMENT",
    "evidence": [
      {
        "valid": true,
        "text": "Earlier notification conditions are superseded.",
        "start": 788,
        "end": 835,
        "source": "NATIVE_LAYA_PASSAGE_WITH_DETERMINISTIC_SCOPE"
      }
    ],
    "aggregation_reason": "STRONG_CURRENT_RELEVANT_EVIDENCE"
  },
  "whole_notice_scores": {
    "YES": 0.5452,
    "NO": 0.3448,
    "UNKNOWN": 0.11
  },
  "passage_scores": [
    {
      "text": "[Message EL0105C | MT564]",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.9335,
        "NO": 0.0295,
        "UNKNOWN": 0.0369
      },
      "score": 0.9335,
      "margin": 0.8966,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "Issuer secretariat memorandum concerning arrangements for the forthcoming extraordinary assembly.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.8912,
        "NO": 0.0831,
        "UNKNOWN": 0.0257
      },
      "score": 0.8912,
      "margin": 0.8081,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "The current agenda is open for shareholder voting instructions.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.7926,
        "NO": 0.1291,
        "UNKNOWN": 0.0782
      },
      "score": 0.7926,
      "margin": 0.6635,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for voting-related immobilisation applies.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.9416,
        "NO": 0.0445,
        "UNKNOWN": 0.0138
      },
      "score": 0.9416,
      "margin": 0.8971,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for an obligatory power-of-attorney document applies.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.8869,
        "NO": 0.0734,
        "UNKNOWN": 0.0397
      },
      "score": 0.8869,
      "margin": 0.8135,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "For this vote, a required voter registration form is required.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.9322,
        "NO": 0.0298,
        "UNKNOWN": 0.038
      },
      "score": 0.9322,
      "margin": 0.8942,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for beneficial-owner disclosure applies.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.8787,
        "NO": 0.0756,
        "UNKNOWN": 0.0457
      },
      "score": 0.8787,
      "margin": 0.8031,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for documentary confirmation of ownership applies.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.9257,
        "NO": 0.0501,
        "UNKNOWN": 0.0242
      },
      "score": 0.9257,
      "margin": 0.8755999999999999,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for a ban on splitting voting instructions applies.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.9567,
        "NO": 0.0233,
        "UNKNOWN": 0.02
      },
      "score": 0.9567,
      "margin": 0.9334,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "For this vote, retrieval of loaned voting positions is required.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.8708,
        "NO": 0.0624,
        "UNKNOWN": 0.0668
      },
      "score": 0.8708,
      "margin": 0.804,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for a mandatory paper-only ballot applies.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.8633,
        "NO": 0.0911,
        "UNKNOWN": 0.0457
      },
      "score": 0.8633,
      "margin": 0.7722,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "[Message EL0105D | MT568]",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.9334,
        "NO": 0.0319,
        "UNKNOWN": 0.0347
      },
      "score": 0.9334,
      "margin": 0.8987,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "Please retain the replacement edition for operational reconciliation.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.9104,
        "NO": 0.053,
        "UNKNOWN": 0.0366
      },
      "score": 0.9104,
      "margin": 0.8573999999999999,
      "historical": false,
      "supersession": true,
      "conditional": false
    },
    {
      "text": "Earlier notification conditions are superseded.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.9632,
        "NO": 0.0123,
        "UNKNOWN": 0.0244
      },
      "score": 0.9632,
      "margin": 0.9388,
      "historical": false,
      "supersession": true,
      "conditional": false
    }
  ],
  "escalation": {
    "escalated": true,
    "requested_predicates": [
      "share_blocking",
      "poa_required",
      "registration_required",
      "holding_confirmation_required",
      "split_voting_restricted",
      "securities_lending_recall_required",
      "other_voting_restriction"
    ],
    "reasons": {
      "share_blocking": [
        "LOW_RAW_SCORE"
      ],
      "poa_required": [
        "LOW_RAW_SCORE"
      ],
      "registration_required": [
        "LOW_RAW_SCORE"
      ],
      "holding_confirmation_required": [
        "LOW_RAW_SCORE"
      ],
      "split_voting_restricted": [
        "LOW_RAW_SCORE"
      ],
      "securities_lending_recall_required": [
        "LOW_RAW_SCORE"
      ],
      "other_voting_restriction": [
        "LOW_RAW_SCORE"
      ]
    }
  },
  "conflicts": [
    "Message EL0105D states 'Earlier notification conditions are superseded' but does not specify which conditions or provide replacement terms, creating uncertainty about the final operative status of the conditions listed in EL0105C.",
    "share_blocking:MODEL_DISAGREEMENT",
    "share_blocking:PASSAGE_CONFLICT",
    "split_voting_restricted:MODEL_DISAGREEMENT",
    "split_voting_restricted:PASSAGE_CONFLICT",
    "votability:STRUCTURE_SEMANTIC_CONFLICT"
  ],
  "reconciliation_for_field": [
    {
      "stage": "LLM",
      "rule": "DISAGREEMENT_REVIEW",
      "predicate": "share_blocking",
      "earlier_value": "YES",
      "later_value": "NO",
      "supported": true
    }
  ]
}
```

## VALIDATION / CASCADE_MODERATE / 25150120b9a9e92a98ab8b33fb003cab98a2ec6b4230ec908fda5c15d2bbc7d7 / split_voting_restricted

```text
[Message EL0105C | MT564]
Issuer secretariat memorandum concerning arrangements for the forthcoming extraordinary assembly.
The current agenda is open for shareholder voting instructions.
No requirement for voting-related immobilisation applies.
No requirement for an obligatory power-of-attorney document applies.
For this vote, a required voter registration form is required.
No requirement for beneficial-owner disclosure applies.
No requirement for documentary confirmation of ownership applies.
No requirement for a ban on splitting voting instructions applies.
For this vote, retrieval of loaned voting positions is required.
No requirement for a mandatory paper-only ballot applies.


[Message EL0105D | MT568]
Please retain the replacement edition for operational reconciliation. Earlier notification conditions are superseded.

```

```json
{
  "truth": "NO",
  "prediction": {
    "value": "UNKNOWN",
    "scores": {
      "YES": 0.8776,
      "NO": 0.0942,
      "UNKNOWN": 0.0282
    },
    "native_score": 0.8776,
    "confidence": null,
    "source": "UNRESOLVED_MODEL_DISAGREEMENT",
    "evidence": [
      {
        "valid": true,
        "text": "No requirement for a ban on splitting voting instructions applies.",
        "start": 500,
        "end": 566,
        "source": "NATIVE_LAYA_PASSAGE_WITH_DETERMINISTIC_SCOPE"
      }
    ],
    "aggregation_reason": "STRONG_CURRENT_RELEVANT_EVIDENCE"
  },
  "whole_notice_scores": {
    "YES": 0.4047,
    "NO": 0.5216,
    "UNKNOWN": 0.0737
  },
  "passage_scores": [
    {
      "text": "[Message EL0105C | MT564]",
      "state": "UNKNOWN",
      "native_value": "NO",
      "scores": {
        "YES": 0.1967,
        "NO": 0.4941,
        "UNKNOWN": 0.3092
      },
      "score": 0.4941,
      "margin": 0.1849,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "Issuer secretariat memorandum concerning arrangements for the forthcoming extraordinary assembly.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.6891,
        "NO": 0.2824,
        "UNKNOWN": 0.0285
      },
      "score": 0.6891,
      "margin": 0.40670000000000006,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "The current agenda is open for shareholder voting instructions.",
      "state": "UNKNOWN",
      "native_value": "NO",
      "scores": {
        "YES": 0.1997,
        "NO": 0.6685,
        "UNKNOWN": 0.1318
      },
      "score": 0.6685,
      "margin": 0.4688,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for voting-related immobilisation applies.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.5293,
        "NO": 0.3713,
        "UNKNOWN": 0.0993
      },
      "score": 0.5293,
      "margin": 0.15799999999999997,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for an obligatory power-of-attorney document applies.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.6168,
        "NO": 0.3047,
        "UNKNOWN": 0.0785
      },
      "score": 0.6168,
      "margin": 0.3121,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "For this vote, a required voter registration form is required.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.8131,
        "NO": 0.1179,
        "UNKNOWN": 0.069
      },
      "score": 0.8131,
      "margin": 0.6952,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for beneficial-owner disclosure applies.",
      "state": "UNKNOWN",
      "native_value": "NO",
      "scores": {
        "YES": 0.1339,
        "NO": 0.7214,
        "UNKNOWN": 0.1447
      },
      "score": 0.7214,
      "margin": 0.5767,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for documentary confirmation of ownership applies.",
      "state": "UNKNOWN",
      "native_value": "NO",
      "scores": {
        "YES": 0.3582,
        "NO": 0.5515,
        "UNKNOWN": 0.0903
      },
      "score": 0.5515,
      "margin": 0.19329999999999997,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for a ban on splitting voting instructions applies.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.8776,
        "NO": 0.0942,
        "UNKNOWN": 0.0282
      },
      "score": 0.8776,
      "margin": 0.7834000000000001,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "For this vote, retrieval of loaned voting positions is required.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.6635,
        "NO": 0.229,
        "UNKNOWN": 0.1074
      },
      "score": 0.6635,
      "margin": 0.4345,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for a mandatory paper-only ballot applies.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.513,
        "NO": 0.4345,
        "UNKNOWN": 0.0525
      },
      "score": 0.513,
      "margin": 0.07850000000000001,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "[Message EL0105D | MT568]",
      "state": "UNKNOWN",
      "native_value": "NO",
      "scores": {
        "YES": 0.1502,
        "NO": 0.5727,
        "UNKNOWN": 0.2771
      },
      "score": 0.5727,
      "margin": 0.2956,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "Please retain the replacement edition for operational reconciliation.",
      "state": "UNKNOWN",
      "native_value": "NO",
      "scores": {
        "YES": 0.1878,
        "NO": 0.7297,
        "UNKNOWN": 0.0824
      },
      "score": 0.7297,
      "margin": 0.5419,
      "historical": false,
      "supersession": true,
      "conditional": false
    },
    {
      "text": "Earlier notification conditions are superseded.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.4973,
        "NO": 0.3914,
        "UNKNOWN": 0.1113
      },
      "score": 0.4973,
      "margin": 0.1059,
      "historical": false,
      "supersession": true,
      "conditional": false
    }
  ],
  "escalation": {
    "escalated": true,
    "requested_predicates": [
      "share_blocking",
      "poa_required",
      "registration_required",
      "holding_confirmation_required",
      "split_voting_restricted",
      "securities_lending_recall_required",
      "other_voting_restriction"
    ],
    "reasons": {
      "share_blocking": [
        "LOW_RAW_SCORE"
      ],
      "poa_required": [
        "LOW_RAW_SCORE"
      ],
      "registration_required": [
        "LOW_RAW_SCORE"
      ],
      "holding_confirmation_required": [
        "LOW_RAW_SCORE"
      ],
      "split_voting_restricted": [
        "LOW_RAW_SCORE"
      ],
      "securities_lending_recall_required": [
        "LOW_RAW_SCORE"
      ],
      "other_voting_restriction": [
        "LOW_RAW_SCORE"
      ]
    }
  },
  "conflicts": [
    "Message EL0105D states 'Earlier notification conditions are superseded' but does not specify which conditions or provide replacement terms, creating uncertainty about the final operative status of the conditions listed in EL0105C.",
    "share_blocking:MODEL_DISAGREEMENT",
    "share_blocking:PASSAGE_CONFLICT",
    "split_voting_restricted:MODEL_DISAGREEMENT",
    "split_voting_restricted:PASSAGE_CONFLICT",
    "votability:STRUCTURE_SEMANTIC_CONFLICT"
  ],
  "reconciliation_for_field": [
    {
      "stage": "LLM",
      "rule": "DISAGREEMENT_REVIEW",
      "predicate": "split_voting_restricted",
      "earlier_value": "YES",
      "later_value": "NO",
      "supported": true
    }
  ]
}
```

## VALIDATION / CASCADE_MODERATE / 2414be60f4dff3cc46dcf385c748749f7c7c3dc05ef8f904052ec9797bdc2f19 / share_blocking

```text
[Message EL0104C | MT564]
Issuer secretariat memorandum concerning arrangements for the forthcoming extraordinary assembly.
The current agenda is open for shareholder voting instructions.
No requirement for voting-related immobilisation applies.
No requirement for an obligatory power-of-attorney document applies.
No requirement for a required voter registration form applies.
For this vote, beneficial-owner disclosure is required.
No requirement for documentary confirmation of ownership applies.
No requirement for a ban on splitting voting instructions applies.
No requirement for retrieval of loaned voting positions applies.
For this vote, a mandatory paper-only ballot is required.


[Message EL0104D | MT568]
Please retain the replacement edition for operational reconciliation. Earlier notification conditions are superseded.

```

```json
{
  "truth": "NO",
  "prediction": {
    "value": "UNKNOWN",
    "scores": {
      "YES": 0.9632,
      "NO": 0.0123,
      "UNKNOWN": 0.0244
    },
    "native_score": 0.9632,
    "confidence": null,
    "source": "UNRESOLVED_MODEL_DISAGREEMENT",
    "evidence": [
      {
        "valid": true,
        "text": "Earlier notification conditions are superseded.",
        "start": 788,
        "end": 835,
        "source": "NATIVE_LAYA_PASSAGE_WITH_DETERMINISTIC_SCOPE"
      }
    ],
    "aggregation_reason": "STRONG_CURRENT_RELEVANT_EVIDENCE"
  },
  "whole_notice_scores": {
    "YES": 0.6147,
    "NO": 0.3133,
    "UNKNOWN": 0.072
  },
  "passage_scores": [
    {
      "text": "[Message EL0104C | MT564]",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.9324,
        "NO": 0.0286,
        "UNKNOWN": 0.039
      },
      "score": 0.9324,
      "margin": 0.8934,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "Issuer secretariat memorandum concerning arrangements for the forthcoming extraordinary assembly.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.8912,
        "NO": 0.0831,
        "UNKNOWN": 0.0257
      },
      "score": 0.8912,
      "margin": 0.8081,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "The current agenda is open for shareholder voting instructions.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.7926,
        "NO": 0.1291,
        "UNKNOWN": 0.0782
      },
      "score": 0.7926,
      "margin": 0.6635,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for voting-related immobilisation applies.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.9416,
        "NO": 0.0445,
        "UNKNOWN": 0.0138
      },
      "score": 0.9416,
      "margin": 0.8971,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for an obligatory power-of-attorney document applies.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.8869,
        "NO": 0.0734,
        "UNKNOWN": 0.0397
      },
      "score": 0.8869,
      "margin": 0.8135,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for a required voter registration form applies.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.7931,
        "NO": 0.1483,
        "UNKNOWN": 0.0586
      },
      "score": 0.7931,
      "margin": 0.6448,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "For this vote, beneficial-owner disclosure is required.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.8825,
        "NO": 0.0705,
        "UNKNOWN": 0.047
      },
      "score": 0.8825,
      "margin": 0.8119999999999999,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for documentary confirmation of ownership applies.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.9257,
        "NO": 0.0501,
        "UNKNOWN": 0.0242
      },
      "score": 0.9257,
      "margin": 0.8755999999999999,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for a ban on splitting voting instructions applies.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.9567,
        "NO": 0.0233,
        "UNKNOWN": 0.02
      },
      "score": 0.9567,
      "margin": 0.9334,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for retrieval of loaned voting positions applies.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.8292,
        "NO": 0.1229,
        "UNKNOWN": 0.0479
      },
      "score": 0.8292,
      "margin": 0.7063,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "For this vote, a mandatory paper-only ballot is required.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.9478,
        "NO": 0.0264,
        "UNKNOWN": 0.0258
      },
      "score": 0.9478,
      "margin": 0.9214,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "[Message EL0104D | MT568]",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.9353,
        "NO": 0.0282,
        "UNKNOWN": 0.0365
      },
      "score": 0.9353,
      "margin": 0.8988,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "Please retain the replacement edition for operational reconciliation.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.9104,
        "NO": 0.053,
        "UNKNOWN": 0.0366
      },
      "score": 0.9104,
      "margin": 0.8573999999999999,
      "historical": false,
      "supersession": true,
      "conditional": false
    },
    {
      "text": "Earlier notification conditions are superseded.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.9632,
        "NO": 0.0123,
        "UNKNOWN": 0.0244
      },
      "score": 0.9632,
      "margin": 0.9388,
      "historical": false,
      "supersession": true,
      "conditional": false
    }
  ],
  "escalation": {
    "escalated": true,
    "requested_predicates": [
      "share_blocking",
      "poa_required",
      "registration_required",
      "beneficial_owner_disclosure_required",
      "holding_confirmation_required",
      "split_voting_restricted",
      "securities_lending_recall_required",
      "other_voting_restriction"
    ],
    "reasons": {
      "share_blocking": [
        "LOW_RAW_SCORE"
      ],
      "poa_required": [
        "LOW_RAW_SCORE"
      ],
      "registration_required": [
        "LOW_RAW_SCORE"
      ],
      "beneficial_owner_disclosure_required": [
        "LOW_RAW_SCORE"
      ],
      "holding_confirmation_required": [
        "LOW_RAW_SCORE"
      ],
      "split_voting_restricted": [
        "LOW_RAW_SCORE"
      ],
      "securities_lending_recall_required": [
        "LOW_RAW_SCORE"
      ],
      "other_voting_restriction": [
        "UNKNOWN",
        "LOW_RAW_SCORE",
        "LOW_MARGIN",
        "UNSUPPORTED_NEGATIVE"
      ]
    }
  },
  "conflicts": [
    "registration_required:MODEL_DISAGREEMENT",
    "registration_required:PASSAGE_CONFLICT",
    "securities_lending_recall_required:MODEL_DISAGREEMENT",
    "securities_lending_recall_required:PASSAGE_CONFLICT",
    "share_blocking:MODEL_DISAGREEMENT",
    "share_blocking:PASSAGE_CONFLICT",
    "split_voting_restricted:MODEL_DISAGREEMENT",
    "split_voting_restricted:PASSAGE_CONFLICT",
    "votability:STRUCTURE_SEMANTIC_CONFLICT"
  ],
  "reconciliation_for_field": [
    {
      "stage": "LLM",
      "rule": "DISAGREEMENT_REVIEW",
      "predicate": "share_blocking",
      "earlier_value": "YES",
      "later_value": "NO",
      "supported": true
    }
  ]
}
```

## VALIDATION / CASCADE_MODERATE / 2414be60f4dff3cc46dcf385c748749f7c7c3dc05ef8f904052ec9797bdc2f19 / registration_required

```text
[Message EL0104C | MT564]
Issuer secretariat memorandum concerning arrangements for the forthcoming extraordinary assembly.
The current agenda is open for shareholder voting instructions.
No requirement for voting-related immobilisation applies.
No requirement for an obligatory power-of-attorney document applies.
No requirement for a required voter registration form applies.
For this vote, beneficial-owner disclosure is required.
No requirement for documentary confirmation of ownership applies.
No requirement for a ban on splitting voting instructions applies.
No requirement for retrieval of loaned voting positions applies.
For this vote, a mandatory paper-only ballot is required.


[Message EL0104D | MT568]
Please retain the replacement edition for operational reconciliation. Earlier notification conditions are superseded.

```

```json
{
  "truth": "NO",
  "prediction": {
    "value": "UNKNOWN",
    "scores": {
      "YES": 0.871,
      "NO": 0.1085,
      "UNKNOWN": 0.0206
    },
    "native_score": 0.871,
    "confidence": null,
    "source": "UNRESOLVED_MODEL_DISAGREEMENT",
    "evidence": [
      {
        "valid": true,
        "text": "For this vote, a mandatory paper-only ballot is required.",
        "start": 632,
        "end": 689,
        "source": "NATIVE_LAYA_PASSAGE_WITH_DETERMINISTIC_SCOPE"
      }
    ],
    "aggregation_reason": "STRONG_CURRENT_RELEVANT_EVIDENCE"
  },
  "whole_notice_scores": {
    "YES": 0.217,
    "NO": 0.6692,
    "UNKNOWN": 0.1137
  },
  "passage_scores": [
    {
      "text": "[Message EL0104C | MT564]",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.4962,
        "NO": 0.2837,
        "UNKNOWN": 0.2201
      },
      "score": 0.4962,
      "margin": 0.21249999999999997,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "Issuer secretariat memorandum concerning arrangements for the forthcoming extraordinary assembly.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.6038,
        "NO": 0.3606,
        "UNKNOWN": 0.0355
      },
      "score": 0.6038,
      "margin": 0.24320000000000003,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "The current agenda is open for shareholder voting instructions.",
      "state": "UNKNOWN",
      "native_value": "NO",
      "scores": {
        "YES": 0.1833,
        "NO": 0.7071,
        "UNKNOWN": 0.1096
      },
      "score": 0.7071,
      "margin": 0.5237999999999999,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for voting-related immobilisation applies.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.7715,
        "NO": 0.1901,
        "UNKNOWN": 0.0383
      },
      "score": 0.7715,
      "margin": 0.5813999999999999,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for an obligatory power-of-attorney document applies.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.7594,
        "NO": 0.2077,
        "UNKNOWN": 0.0329
      },
      "score": 0.7594,
      "margin": 0.5517,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for a required voter registration form applies.",
      "state": "NEGATIVE",
      "native_value": "NO",
      "scores": {
        "YES": 0.3223,
        "NO": 0.6322,
        "UNKNOWN": 0.0455
      },
      "score": 0.6322,
      "margin": 0.3099,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "For this vote, beneficial-owner disclosure is required.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.5295,
        "NO": 0.388,
        "UNKNOWN": 0.0824
      },
      "score": 0.5295,
      "margin": 0.14149999999999996,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for documentary confirmation of ownership applies.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.5764,
        "NO": 0.3823,
        "UNKNOWN": 0.0413
      },
      "score": 0.5764,
      "margin": 0.19410000000000005,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for a ban on splitting voting instructions applies.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.8032,
        "NO": 0.1731,
        "UNKNOWN": 0.0237
      },
      "score": 0.8032,
      "margin": 0.6301,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for retrieval of loaned voting positions applies.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.5694,
        "NO": 0.3459,
        "UNKNOWN": 0.0847
      },
      "score": 0.5694,
      "margin": 0.22350000000000003,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "For this vote, a mandatory paper-only ballot is required.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.871,
        "NO": 0.1085,
        "UNKNOWN": 0.0206
      },
      "score": 0.871,
      "margin": 0.7625,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "[Message EL0104D | MT568]",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.4486,
        "NO": 0.3003,
        "UNKNOWN": 0.2511
      },
      "score": 0.4486,
      "margin": 0.1483,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "Please retain the replacement edition for operational reconciliation.",
      "state": "UNKNOWN",
      "native_value": "NO",
      "scores": {
        "YES": 0.3889,
        "NO": 0.5066,
        "UNKNOWN": 0.1045
      },
      "score": 0.5066,
      "margin": 0.11770000000000003,
      "historical": false,
      "supersession": true,
      "conditional": false
    },
    {
      "text": "Earlier notification conditions are superseded.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.597,
        "NO": 0.3291,
        "UNKNOWN": 0.0739
      },
      "score": 0.597,
      "margin": 0.26789999999999997,
      "historical": false,
      "supersession": true,
      "conditional": false
    }
  ],
  "escalation": {
    "escalated": true,
    "requested_predicates": [
      "share_blocking",
      "poa_required",
      "registration_required",
      "beneficial_owner_disclosure_required",
      "holding_confirmation_required",
      "split_voting_restricted",
      "securities_lending_recall_required",
      "other_voting_restriction"
    ],
    "reasons": {
      "share_blocking": [
        "LOW_RAW_SCORE"
      ],
      "poa_required": [
        "LOW_RAW_SCORE"
      ],
      "registration_required": [
        "LOW_RAW_SCORE"
      ],
      "beneficial_owner_disclosure_required": [
        "LOW_RAW_SCORE"
      ],
      "holding_confirmation_required": [
        "LOW_RAW_SCORE"
      ],
      "split_voting_restricted": [
        "LOW_RAW_SCORE"
      ],
      "securities_lending_recall_required": [
        "LOW_RAW_SCORE"
      ],
      "other_voting_restriction": [
        "UNKNOWN",
        "LOW_RAW_SCORE",
        "LOW_MARGIN",
        "UNSUPPORTED_NEGATIVE"
      ]
    }
  },
  "conflicts": [
    "registration_required:MODEL_DISAGREEMENT",
    "registration_required:PASSAGE_CONFLICT",
    "securities_lending_recall_required:MODEL_DISAGREEMENT",
    "securities_lending_recall_required:PASSAGE_CONFLICT",
    "share_blocking:MODEL_DISAGREEMENT",
    "share_blocking:PASSAGE_CONFLICT",
    "split_voting_restricted:MODEL_DISAGREEMENT",
    "split_voting_restricted:PASSAGE_CONFLICT",
    "votability:STRUCTURE_SEMANTIC_CONFLICT"
  ],
  "reconciliation_for_field": [
    {
      "stage": "LLM",
      "rule": "DISAGREEMENT_REVIEW",
      "predicate": "registration_required",
      "earlier_value": "YES",
      "later_value": "NO",
      "supported": true
    }
  ]
}
```

## VALIDATION / CASCADE_MODERATE / 2414be60f4dff3cc46dcf385c748749f7c7c3dc05ef8f904052ec9797bdc2f19 / split_voting_restricted

```text
[Message EL0104C | MT564]
Issuer secretariat memorandum concerning arrangements for the forthcoming extraordinary assembly.
The current agenda is open for shareholder voting instructions.
No requirement for voting-related immobilisation applies.
No requirement for an obligatory power-of-attorney document applies.
No requirement for a required voter registration form applies.
For this vote, beneficial-owner disclosure is required.
No requirement for documentary confirmation of ownership applies.
No requirement for a ban on splitting voting instructions applies.
No requirement for retrieval of loaned voting positions applies.
For this vote, a mandatory paper-only ballot is required.


[Message EL0104D | MT568]
Please retain the replacement edition for operational reconciliation. Earlier notification conditions are superseded.

```

```json
{
  "truth": "NO",
  "prediction": {
    "value": "UNKNOWN",
    "scores": {
      "YES": 0.8776,
      "NO": 0.0942,
      "UNKNOWN": 0.0282
    },
    "native_score": 0.8776,
    "confidence": null,
    "source": "UNRESOLVED_MODEL_DISAGREEMENT",
    "evidence": [
      {
        "valid": true,
        "text": "No requirement for a ban on splitting voting instructions applies.",
        "start": 500,
        "end": 566,
        "source": "NATIVE_LAYA_PASSAGE_WITH_DETERMINISTIC_SCOPE"
      }
    ],
    "aggregation_reason": "STRONG_CURRENT_RELEVANT_EVIDENCE"
  },
  "whole_notice_scores": {
    "YES": 0.426,
    "NO": 0.5101,
    "UNKNOWN": 0.0639
  },
  "passage_scores": [
    {
      "text": "[Message EL0104C | MT564]",
      "state": "UNKNOWN",
      "native_value": "NO",
      "scores": {
        "YES": 0.2329,
        "NO": 0.4417,
        "UNKNOWN": 0.3254
      },
      "score": 0.4417,
      "margin": 0.11629999999999996,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "Issuer secretariat memorandum concerning arrangements for the forthcoming extraordinary assembly.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.6891,
        "NO": 0.2824,
        "UNKNOWN": 0.0285
      },
      "score": 0.6891,
      "margin": 0.40670000000000006,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "The current agenda is open for shareholder voting instructions.",
      "state": "UNKNOWN",
      "native_value": "NO",
      "scores": {
        "YES": 0.1997,
        "NO": 0.6685,
        "UNKNOWN": 0.1318
      },
      "score": 0.6685,
      "margin": 0.4688,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for voting-related immobilisation applies.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.5293,
        "NO": 0.3713,
        "UNKNOWN": 0.0993
      },
      "score": 0.5293,
      "margin": 0.15799999999999997,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for an obligatory power-of-attorney document applies.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.6168,
        "NO": 0.3047,
        "UNKNOWN": 0.0785
      },
      "score": 0.6168,
      "margin": 0.3121,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for a required voter registration form applies.",
      "state": "UNKNOWN",
      "native_value": "NO",
      "scores": {
        "YES": 0.4632,
        "NO": 0.4702,
        "UNKNOWN": 0.0666
      },
      "score": 0.4702,
      "margin": 0.007000000000000006,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "For this vote, beneficial-owner disclosure is required.",
      "state": "UNKNOWN",
      "native_value": "NO",
      "scores": {
        "YES": 0.3864,
        "NO": 0.5276,
        "UNKNOWN": 0.086
      },
      "score": 0.5276,
      "margin": 0.14119999999999994,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for documentary confirmation of ownership applies.",
      "state": "UNKNOWN",
      "native_value": "NO",
      "scores": {
        "YES": 0.3582,
        "NO": 0.5515,
        "UNKNOWN": 0.0903
      },
      "score": 0.5515,
      "margin": 0.19329999999999997,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for a ban on splitting voting instructions applies.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.8776,
        "NO": 0.0942,
        "UNKNOWN": 0.0282
      },
      "score": 0.8776,
      "margin": 0.7834000000000001,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for retrieval of loaned voting positions applies.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.5739,
        "NO": 0.3204,
        "UNKNOWN": 0.1057
      },
      "score": 0.5739,
      "margin": 0.25349999999999995,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "For this vote, a mandatory paper-only ballot is required.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.8258,
        "NO": 0.1202,
        "UNKNOWN": 0.054
      },
      "score": 0.8258,
      "margin": 0.7056,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "[Message EL0104D | MT568]",
      "state": "UNKNOWN",
      "native_value": "NO",
      "scores": {
        "YES": 0.1755,
        "NO": 0.5197,
        "UNKNOWN": 0.3048
      },
      "score": 0.5197,
      "margin": 0.21490000000000004,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "Please retain the replacement edition for operational reconciliation.",
      "state": "UNKNOWN",
      "native_value": "NO",
      "scores": {
        "YES": 0.1878,
        "NO": 0.7297,
        "UNKNOWN": 0.0824
      },
      "score": 0.7297,
      "margin": 0.5419,
      "historical": false,
      "supersession": true,
      "conditional": false
    },
    {
      "text": "Earlier notification conditions are superseded.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.4973,
        "NO": 0.3914,
        "UNKNOWN": 0.1113
      },
      "score": 0.4973,
      "margin": 0.1059,
      "historical": false,
      "supersession": true,
      "conditional": false
    }
  ],
  "escalation": {
    "escalated": true,
    "requested_predicates": [
      "share_blocking",
      "poa_required",
      "registration_required",
      "beneficial_owner_disclosure_required",
      "holding_confirmation_required",
      "split_voting_restricted",
      "securities_lending_recall_required",
      "other_voting_restriction"
    ],
    "reasons": {
      "share_blocking": [
        "LOW_RAW_SCORE"
      ],
      "poa_required": [
        "LOW_RAW_SCORE"
      ],
      "registration_required": [
        "LOW_RAW_SCORE"
      ],
      "beneficial_owner_disclosure_required": [
        "LOW_RAW_SCORE"
      ],
      "holding_confirmation_required": [
        "LOW_RAW_SCORE"
      ],
      "split_voting_restricted": [
        "LOW_RAW_SCORE"
      ],
      "securities_lending_recall_required": [
        "LOW_RAW_SCORE"
      ],
      "other_voting_restriction": [
        "UNKNOWN",
        "LOW_RAW_SCORE",
        "LOW_MARGIN",
        "UNSUPPORTED_NEGATIVE"
      ]
    }
  },
  "conflicts": [
    "registration_required:MODEL_DISAGREEMENT",
    "registration_required:PASSAGE_CONFLICT",
    "securities_lending_recall_required:MODEL_DISAGREEMENT",
    "securities_lending_recall_required:PASSAGE_CONFLICT",
    "share_blocking:MODEL_DISAGREEMENT",
    "share_blocking:PASSAGE_CONFLICT",
    "split_voting_restricted:MODEL_DISAGREEMENT",
    "split_voting_restricted:PASSAGE_CONFLICT",
    "votability:STRUCTURE_SEMANTIC_CONFLICT"
  ],
  "reconciliation_for_field": [
    {
      "stage": "LLM",
      "rule": "DISAGREEMENT_REVIEW",
      "predicate": "split_voting_restricted",
      "earlier_value": "YES",
      "later_value": "NO",
      "supported": true
    }
  ]
}
```

## VALIDATION / CASCADE_MODERATE / 2414be60f4dff3cc46dcf385c748749f7c7c3dc05ef8f904052ec9797bdc2f19 / securities_lending_recall_required

```text
[Message EL0104C | MT564]
Issuer secretariat memorandum concerning arrangements for the forthcoming extraordinary assembly.
The current agenda is open for shareholder voting instructions.
No requirement for voting-related immobilisation applies.
No requirement for an obligatory power-of-attorney document applies.
No requirement for a required voter registration form applies.
For this vote, beneficial-owner disclosure is required.
No requirement for documentary confirmation of ownership applies.
No requirement for a ban on splitting voting instructions applies.
No requirement for retrieval of loaned voting positions applies.
For this vote, a mandatory paper-only ballot is required.


[Message EL0104D | MT568]
Please retain the replacement edition for operational reconciliation. Earlier notification conditions are superseded.

```

```json
{
  "truth": "NO",
  "prediction": {
    "value": "UNKNOWN",
    "scores": {
      "YES": 0.8894,
      "NO": 0.0868,
      "UNKNOWN": 0.0237
    },
    "native_score": 0.8894,
    "confidence": null,
    "source": "UNRESOLVED_MODEL_DISAGREEMENT",
    "evidence": [
      {
        "valid": true,
        "text": "For this vote, a mandatory paper-only ballot is required.",
        "start": 632,
        "end": 689,
        "source": "NATIVE_LAYA_PASSAGE_WITH_DETERMINISTIC_SCOPE"
      }
    ],
    "aggregation_reason": "STRONG_CURRENT_RELEVANT_EVIDENCE"
  },
  "whole_notice_scores": {
    "YES": 0.2468,
    "NO": 0.6654,
    "UNKNOWN": 0.0877
  },
  "passage_scores": [
    {
      "text": "[Message EL0104C | MT564]",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.5459,
        "NO": 0.3059,
        "UNKNOWN": 0.1483
      },
      "score": 0.5459,
      "margin": 0.24000000000000005,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "Issuer secretariat memorandum concerning arrangements for the forthcoming extraordinary assembly.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.5404,
        "NO": 0.3777,
        "UNKNOWN": 0.0819
      },
      "score": 0.5404,
      "margin": 0.1627,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "The current agenda is open for shareholder voting instructions.",
      "state": "UNKNOWN",
      "native_value": "NO",
      "scores": {
        "YES": 0.31,
        "NO": 0.552,
        "UNKNOWN": 0.1381
      },
      "score": 0.552,
      "margin": 0.24200000000000005,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for voting-related immobilisation applies.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.7555,
        "NO": 0.1932,
        "UNKNOWN": 0.0513
      },
      "score": 0.7555,
      "margin": 0.5622999999999999,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for an obligatory power-of-attorney document applies.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.6798,
        "NO": 0.2593,
        "UNKNOWN": 0.0609
      },
      "score": 0.6798,
      "margin": 0.4205,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for a required voter registration form applies.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.5264,
        "NO": 0.3962,
        "UNKNOWN": 0.0774
      },
      "score": 0.5264,
      "margin": 0.13019999999999998,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "For this vote, beneficial-owner disclosure is required.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.616,
        "NO": 0.2656,
        "UNKNOWN": 0.1184
      },
      "score": 0.616,
      "margin": 0.3504,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for documentary confirmation of ownership applies.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.622,
        "NO": 0.2995,
        "UNKNOWN": 0.0785
      },
      "score": 0.622,
      "margin": 0.3225,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for a ban on splitting voting instructions applies.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.7864,
        "NO": 0.1765,
        "UNKNOWN": 0.0371
      },
      "score": 0.7864,
      "margin": 0.6099,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "No requirement for retrieval of loaned voting positions applies.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.6289,
        "NO": 0.2869,
        "UNKNOWN": 0.0842
      },
      "score": 0.6289,
      "margin": 0.342,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "For this vote, a mandatory paper-only ballot is required.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.8894,
        "NO": 0.0868,
        "UNKNOWN": 0.0237
      },
      "score": 0.8894,
      "margin": 0.8026,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "[Message EL0104D | MT568]",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.5127,
        "NO": 0.3105,
        "UNKNOWN": 0.1768
      },
      "score": 0.5127,
      "margin": 0.20220000000000005,
      "historical": false,
      "supersession": false,
      "conditional": false
    },
    {
      "text": "Please retain the replacement edition for operational reconciliation.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.5096,
        "NO": 0.375,
        "UNKNOWN": 0.1154
      },
      "score": 0.5096,
      "margin": 0.13460000000000005,
      "historical": false,
      "supersession": true,
      "conditional": false
    },
    {
      "text": "Earlier notification conditions are superseded.",
      "state": "AFFIRMATIVE",
      "native_value": "YES",
      "scores": {
        "YES": 0.6434,
        "NO": 0.2655,
        "UNKNOWN": 0.0912
      },
      "score": 0.6434,
      "margin": 0.37789999999999996,
      "historical": false,
      "supersession": true,
      "conditional": false
    }
  ],
  "escalation": {
    "escalated": true,
    "requested_predicates": [
      "share_blocking",
      "poa_required",
      "registration_required",
      "beneficial_owner_disclosure_required",
      "holding_confirmation_required",
      "split_voting_restricted",
      "securities_lending_recall_required",
      "other_voting_restriction"
    ],
    "reasons": {
      "share_blocking": [
        "LOW_RAW_SCORE"
      ],
      "poa_required": [
        "LOW_RAW_SCORE"
      ],
      "registration_required": [
        "LOW_RAW_SCORE"
      ],
      "beneficial_owner_disclosure_required": [
        "LOW_RAW_SCORE"
      ],
      "holding_confirmation_required": [
        "LOW_RAW_SCORE"
      ],
      "split_voting_restricted": [
        "LOW_RAW_SCORE"
      ],
      "securities_lending_recall_required": [
        "LOW_RAW_SCORE"
      ],
      "other_voting_restriction": [
        "UNKNOWN",
        "LOW_RAW_SCORE",
        "LOW_MARGIN",
        "UNSUPPORTED_NEGATIVE"
      ]
    }
  },
  "conflicts": [
    "registration_required:MODEL_DISAGREEMENT",
    "registration_required:PASSAGE_CONFLICT",
    "securities_lending_recall_required:MODEL_DISAGREEMENT",
    "securities_lending_recall_required:PASSAGE_CONFLICT",
    "share_blocking:MODEL_DISAGREEMENT",
    "share_blocking:PASSAGE_CONFLICT",
    "split_voting_restricted:MODEL_DISAGREEMENT",
    "split_voting_restricted:PASSAGE_CONFLICT",
    "votability:STRUCTURE_SEMANTIC_CONFLICT"
  ],
  "reconciliation_for_field": [
    {
      "stage": "LLM",
      "rule": "DISAGREEMENT_REVIEW",
      "predicate": "securities_lending_recall_required",
      "earlier_value": "YES",
      "later_value": "NO",
      "supported": true
    }
  ]
}
```

## VALIDATION / CASCADE_MODERATE / 192427e9aa3ca6f904eb505ac724d3c90e8eba48b9c676788a55d6e407fcb195 / expected_final_status

```text
[Message EL0206C | MT564]
Broker service update: the institutional ballot channel is now available for this agenda.
This is solely a cash-distribution advice; it offers no meeting ballot and no shareholder vote.
No requirement for a voting lock on the position applies.
No requirement for a compulsory attorney mandate applies.
No requirement for mandatory meeting registration applies.
No requirement for identification of the underlying owner applies.
No requirement for a custodial holding statement applies.
No requirement for a requirement to cast all votes identically applies.
No requirement for recall of lent securities applies.
No requirement for an in-person-only voting condition applies.


[Message EL0206D | MT568]
Please retain the replacement edition for operational reconciliation. Earlier notification conditions are superseded.

```
```json
{
  "truth": "NOT_VOTABLE",
  "prediction": "UNCERTAIN_MANUAL_REVIEW",
  "decision": {
    "classification": "UNCERTAIN_MANUAL_REVIEW",
    "rule": "R1 unresolved conflicts",
    "rule_version": "semantic-decision-2",
    "manual_review_required": true,
    "automation_enabled": false,
    "review_reasons": [
      "registration_required:MODEL_DISAGREEMENT",
      "registration_required:PASSAGE_CONFLICT",
      "securities_lending_recall_required:MODEL_DISAGREEMENT",
      "securities_lending_recall_required:PASSAGE_CONFLICT",
      "share_blocking:MODEL_DISAGREEMENT",
      "share_blocking:PASSAGE_CONFLICT",
      "Synthetic-only evaluation; customer quality gate not met"
    ]
  },
  "deadline": {
    "status": "OPEN",
    "comparisons": [
      {
        "source": "PROWIDE",
        "field_id": "prowide:9",
        "path": [
          "CAOPTN[1]"
        ],
        "deadline": {
          "iso": "2026-11-24T17:00:00+00:00",
          "offset_known": true,
          "precision": "SECOND"
        },
        "status": "OPEN",
        "field": {
          "components": [
            "RDDT",
            "20261124",
            "170000",
            "000",
            null,
            "00"
          ],
          "end": 226,
          "qualifier": "RDDT",
          "sequence_instance_path": [
            "CAOPTN[1]"
          ],
          "sequence_path": [
            "CAOPTN"
          ],
          "source": "PROWIDE",
          "source_text": ":98E::RDDT//20261124170000,000/00\n",
          "start": 192,
          "tag": "98E",
          "typed_field": "Field98E",
          "value": ":RDDT//20261124170000,000/00"
        }
      }
    ],
    "conflict": false,
    "source": "PROWIDE_COMPONENTS_DETERMINISTIC_COMPARISON",
    "reason": "Only RDDT is controlling. Bare local/date-only values require an agreed timezone profile; no UTC assumption."
  }
}
```

## VALIDATION / CASCADE_MODERATE / 25150120b9a9e92a98ab8b33fb003cab98a2ec6b4230ec908fda5c15d2bbc7d7 / expected_final_status

```text
[Message EL0105C | MT564]
Issuer secretariat memorandum concerning arrangements for the forthcoming extraordinary assembly.
The current agenda is open for shareholder voting instructions.
No requirement for voting-related immobilisation applies.
No requirement for an obligatory power-of-attorney document applies.
For this vote, a required voter registration form is required.
No requirement for beneficial-owner disclosure applies.
No requirement for documentary confirmation of ownership applies.
No requirement for a ban on splitting voting instructions applies.
For this vote, retrieval of loaned voting positions is required.
No requirement for a mandatory paper-only ballot applies.


[Message EL0105D | MT568]
Please retain the replacement edition for operational reconciliation. Earlier notification conditions are superseded.

```
```json
{
  "truth": "VOTABLE_WITH_RESTRICTION",
  "prediction": "UNCERTAIN_MANUAL_REVIEW",
  "decision": {
    "classification": "UNCERTAIN_MANUAL_REVIEW",
    "rule": "R1 unresolved conflicts",
    "rule_version": "semantic-decision-2",
    "manual_review_required": true,
    "automation_enabled": false,
    "review_reasons": [
      "Message EL0105D states 'Earlier notification conditions are superseded' but does not specify which conditions or provide replacement terms, creating uncertainty about the final operative status of the conditions listed in EL0105C.",
      "share_blocking:MODEL_DISAGREEMENT",
      "share_blocking:PASSAGE_CONFLICT",
      "split_voting_restricted:MODEL_DISAGREEMENT",
      "split_voting_restricted:PASSAGE_CONFLICT",
      "votability:STRUCTURE_SEMANTIC_CONFLICT",
      "Synthetic-only evaluation; customer quality gate not met"
    ]
  },
  "deadline": {
    "status": "OPEN",
    "comparisons": [
      {
        "source": "PROWIDE",
        "field_id": "prowide:10",
        "path": [
          "CAOPTN[1]"
        ],
        "deadline": {
          "iso": "2026-11-24T17:00:00+00:00",
          "offset_known": true,
          "precision": "SECOND"
        },
        "status": "OPEN",
        "field": {
          "components": [
            "RDDT",
            "20261124",
            "170000",
            "000",
            null,
            "00"
          ],
          "end": 243,
          "qualifier": "RDDT",
          "sequence_instance_path": [
            "CAOPTN[1]"
          ],
          "sequence_path": [
            "CAOPTN"
          ],
          "source": "PROWIDE",
          "source_text": ":98E::RDDT//20261124170000,000/00\n",
          "start": 209,
          "tag": "98E",
          "typed_field": "Field98E",
          "value": ":RDDT//20261124170000,000/00"
        }
      }
    ],
    "conflict": false,
    "source": "PROWIDE_COMPONENTS_DETERMINISTIC_COMPARISON",
    "reason": "Only RDDT is controlling. Bare local/date-only values require an agreed timezone profile; no UTC assumption."
  }
}
```

## VALIDATION / CASCADE_MODERATE / 2414be60f4dff3cc46dcf385c748749f7c7c3dc05ef8f904052ec9797bdc2f19 / expected_final_status

```text
[Message EL0104C | MT564]
Issuer secretariat memorandum concerning arrangements for the forthcoming extraordinary assembly.
The current agenda is open for shareholder voting instructions.
No requirement for voting-related immobilisation applies.
No requirement for an obligatory power-of-attorney document applies.
No requirement for a required voter registration form applies.
For this vote, beneficial-owner disclosure is required.
No requirement for documentary confirmation of ownership applies.
No requirement for a ban on splitting voting instructions applies.
No requirement for retrieval of loaned voting positions applies.
For this vote, a mandatory paper-only ballot is required.


[Message EL0104D | MT568]
Please retain the replacement edition for operational reconciliation. Earlier notification conditions are superseded.

```
```json
{
  "truth": "DEADLINE_PASSED",
  "prediction": "UNCERTAIN_MANUAL_REVIEW",
  "decision": {
    "classification": "UNCERTAIN_MANUAL_REVIEW",
    "rule": "R1 unresolved conflicts",
    "rule_version": "semantic-decision-2",
    "manual_review_required": true,
    "automation_enabled": false,
    "review_reasons": [
      "registration_required:MODEL_DISAGREEMENT",
      "registration_required:PASSAGE_CONFLICT",
      "securities_lending_recall_required:MODEL_DISAGREEMENT",
      "securities_lending_recall_required:PASSAGE_CONFLICT",
      "share_blocking:MODEL_DISAGREEMENT",
      "share_blocking:PASSAGE_CONFLICT",
      "split_voting_restricted:MODEL_DISAGREEMENT",
      "split_voting_restricted:PASSAGE_CONFLICT",
      "votability:STRUCTURE_SEMANTIC_CONFLICT",
      "Synthetic-only evaluation; customer quality gate not met"
    ]
  },
  "deadline": {
    "status": "PASSED",
    "comparisons": [
      {
        "source": "PROWIDE",
        "field_id": "prowide:10",
        "path": [
          "CAOPTN[1]"
        ],
        "deadline": {
          "iso": "2025-09-01T17:00:00+00:00",
          "offset_known": true,
          "precision": "SECOND"
        },
        "status": "PASSED",
        "field": {
          "components": [
            "RDDT",
            "20250901",
            "170000",
            "000",
            null,
            "00"
          ],
          "end": 243,
          "qualifier": "RDDT",
          "sequence_instance_path": [
            "CAOPTN[1]"
          ],
          "sequence_path": [
            "CAOPTN"
          ],
          "source": "PROWIDE",
          "source_text": ":98E::RDDT//20250901170000,000/00\n",
          "start": 209,
          "tag": "98E",
          "typed_field": "Field98E",
          "value": ":RDDT//20250901170000,000/00"
        }
      }
    ],
    "conflict": false,
    "source": "PROWIDE_COMPONENTS_DETERMINISTIC_COMPARISON",
    "reason": "Only RDDT is controlling. Bare local/date-only values require an agreed timezone profile; no UTC assumption."
  }
}
```
