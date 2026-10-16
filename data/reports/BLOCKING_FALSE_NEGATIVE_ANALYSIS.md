# Blocking false-negative investigation

All 11 affirmative validation records were inspected. The original document-level output detects zero, while sentence-level fine-tuned Laya detects a confident YES passage in 11/11. All 11 documents are then changed to UNKNOWN by `conflict_abstain`: an unrelated introductory sentence classified NO is treated as contradicting the affirmative restriction sentence. This is an aggregation/formulation defect, not evidence that the checkpoint cannot recognise blocking.

The same frozen fine-tuned checkpoint classified the whole document YES in 11/11 fresh validation-only component probes. These probes do not alter any A–E result, model or threshold.

Training distribution: `{'NO': 243, 'YES': 32, 'UNKNOWN': 25}`; validation: `{'NO': 80, 'YES': 11, 'UNKNOWN': 9}`. Original training records retain the source strings and labels exactly: True. The YES/NO option mapping is direct; there is no inversion. Native passage scores explicitly favour YES on the blocking clause. Checkpoint weights are covered by both historical and A–E freeze hashes, and reload native-score equality was separately demonstrated.

Training uses whole notices whereas inference asks independent sentence questions. In the choice formulation, NO includes “not stated”; absence in one sentence is not a negative assertion about another sentence. The reducer incorrectly equates these meanings. Its selected-passage scores are retained even when the aggregate abstains; they are not document-level probabilities. The .70 activity cutoff exposes opposing confident passage predictions rather than causing the affirmative passage to disappear.

Imbalance and repetitive synthetic language remain limitations, but do not explain this particular 0/11 result. Preprocessing preserves the affirmative clause (offsets and passage text below); none is truncated. Whole-document/sentence contrast and direct positive passage detection rule out a global training/loading failure. Distribution mismatch is real (document training, sentence inference), and the deterministic conflict policy amplifies it.

Next experiment: distinguish explicit negation from absence of mention, then validate a scope-aware reducer on independently labelled multi-paragraph notices including supersession. A naive any-positive reducer would recover these eleven cases but can incorrectly revive historical/waived restrictions. No such fix was applied after examining the challenge set.

## Every affirmative validation case

### SYN-0491

Voting instructions may be submitted for Helios Medical NV's Scheme Meeting. Once a valid instruction is received, the instructed shares will be blocked and cannot be sold or transferred until the meeting has concluded.

Expected: SHARE_BLOCKING = YES.

```json
{
  "expected": "YES",
  "chunks": [
    {
      "text": "Voting instructions may be submitted for Helios Medical NV's Scheme Meeting.",
      "start": 0,
      "end": 76,
      "boundary": "sentence"
    },
    {
      "text": "Once a valid instruction is received, the instructed shares will be blocked and cannot be sold or transferred until the meeting has concluded.",
      "start": 77,
      "end": 219,
      "boundary": "sentence"
    }
  ],
  "original": {
    "base": {
      "aggregate": {
        "value": "YES",
        "scores": {
          "YES": 0.9798,
          "NO": 0.0072,
          "UNKNOWN": 0.013
        },
        "confidence": 0.9798,
        "margin": 0.9668,
        "evidence": {
          "text": "Once a valid instruction is received, the instructed shares will be blocked and cannot be sold or transferred until the meeting has concluded.",
          "start": 77,
          "end": 219,
          "boundary": "sentence",
          "source": "sentence-level Laya candidate; exact substring, not human-verified explanation"
        },
        "sdk_confidence": 0.8981,
        "truncated": false,
        "conflict": false,
        "aggregation": "conflict_abstain",
        "passage_count": 2,
        "score_definition": "Native scores for selected passage; not aggregate document probabilities"
      },
      "passages": [
        {
          "value": "YES",
          "scores": {
            "YES": 0.935,
            "NO": 0.0203,
            "UNKNOWN": 0.0447
          },
          "confidence": 0.935,
          "margin": 0.8903000000000001,
          "evidence": {
            "text": "Voting instructions may be submitted for Helios Medical NV's Scheme Meeting.",
            "start": 0,
            "end": 76,
            "boundary": "sentence",
            "source": "sentence-level Laya candidate; exact substring, not human-verified explanation"
          },
          "sdk_confidence": 0.7443,
          "truncated": false
        },
        {
          "value": "YES",
          "scores": {
            "YES": 0.9798,
            "NO": 0.0072,
            "UNKNOWN": 0.013
          },
          "confidence": 0.9798,
          "margin": 0.9668,
          "evidence": {
            "text": "Once a valid instruction is received, the instructed shares will be blocked and cannot be sold or transferred until the meeting has concluded.",
            "start": 77,
            "end": 219,
            "boundary": "sentence",
            "source": "sentence-level Laya candidate; exact substring, not human-verified explanation"
          },
          "sdk_confidence": 0.8981,
          "truncated": false
        }
      ]
    },
    "fine": {
      "aggregate": {
        "value": "UNKNOWN",
        "scores": {
          "YES": 0.0,
          "NO": 1.0,
          "UNKNOWN": 0.0
        },
        "confidence": null,
        "margin": null,
        "evidence": null,
        "sdk_confidence": 1.0,
        "truncated": false,
        "conflict": true,
        "aggregation": "conflict_abstain",
        "passage_count": 2,
        "abstention_reason": "Opposing passage predictions; no reliable supersession established",
        "score_definition": "Native scores for selected passage; not aggregate document probabilities"
      },
      "passages": [
        {
          "value": "NO",
          "scores": {
            "YES": 0.0,
            "NO": 1.0,
            "UNKNOWN": 0.0
          },
          "confidence": 1.0,
          "margin": 1.0,
          "evidence": null,
          "sdk_confidence": 1.0,
          "truncated": false
        },
        {
          "value": "YES",
          "scores": {
            "YES": 1.0,
            "NO": 0.0,
            "UNKNOWN": 0.0
          },
          "confidence": 1.0,
          "margin": 1.0,
          "evidence": {
            "text": "Once a valid instruction is received, the instructed shares will be blocked and cannot be sold or transferred until the meeting has concluded.",
            "start": 77,
            "end": 219,
            "boundary": "sentence",
            "source": "sentence-level Laya candidate; exact substring, not human-verified explanation"
          },
          "sdk_confidence": 1.0,
          "truncated": false
        }
      ]
    }
  },
  "whole_document_probe": {
    "base": {
      "type": "choice",
      "choice": "YES",
      "probabilities": {
        "YES": 0.9523,
        "NO": 0.016,
        "UNKNOWN": 0.0317
      },
      "confidence": 0.7978,
      "answer_confidence": 0.9523,
      "action": {
        "act_probability": 1.0
      }
    },
    "fine": {
      "type": "choice",
      "choice": "YES",
      "probabilities": {
        "YES": 1.0,
        "NO": 0.0,
        "UNKNOWN": 0.0
      },
      "confidence": 1.0,
      "answer_confidence": 1.0,
      "action": {
        "act_probability": 1.0
      }
    }
  }
}
```

### SYN-0073

Eligible holders may vote by proxy. Positions instructed for voting are immobilised from receipt of the instruction through the end of the Scheme Meeting.

Expected: SHARE_BLOCKING = YES.

```json
{
  "expected": "YES",
  "chunks": [
    {
      "text": "Eligible holders may vote by proxy.",
      "start": 0,
      "end": 35,
      "boundary": "sentence"
    },
    {
      "text": "Positions instructed for voting are immobilised from receipt of the instruction through the end of the Scheme Meeting.",
      "start": 36,
      "end": 154,
      "boundary": "sentence"
    }
  ],
  "original": {
    "base": {
      "aggregate": {
        "value": "YES",
        "scores": {
          "YES": 0.9773,
          "NO": 0.0123,
          "UNKNOWN": 0.0104
        },
        "confidence": 0.9773,
        "margin": 0.965,
        "evidence": {
          "text": "Positions instructed for voting are immobilised from receipt of the instruction through the end of the Scheme Meeting.",
          "start": 36,
          "end": 154,
          "boundary": "sentence",
          "source": "sentence-level Laya candidate; exact substring, not human-verified explanation"
        },
        "sdk_confidence": 0.8873,
        "truncated": false,
        "conflict": false,
        "aggregation": "conflict_abstain",
        "passage_count": 2,
        "score_definition": "Native scores for selected passage; not aggregate document probabilities"
      },
      "passages": [
        {
          "value": "YES",
          "scores": {
            "YES": 0.9329,
            "NO": 0.0375,
            "UNKNOWN": 0.0296
          },
          "confidence": 0.9329,
          "margin": 0.8954,
          "evidence": {
            "text": "Eligible holders may vote by proxy.",
            "start": 0,
            "end": 35,
            "boundary": "sentence",
            "source": "sentence-level Laya candidate; exact substring, not human-verified explanation"
          },
          "sdk_confidence": 0.7341,
          "truncated": false
        },
        {
          "value": "YES",
          "scores": {
            "YES": 0.9773,
            "NO": 0.0123,
            "UNKNOWN": 0.0104
          },
          "confidence": 0.9773,
          "margin": 0.965,
          "evidence": {
            "text": "Positions instructed for voting are immobilised from receipt of the instruction through the end of the Scheme Meeting.",
            "start": 36,
            "end": 154,
            "boundary": "sentence",
            "source": "sentence-level Laya candidate; exact substring, not human-verified explanation"
          },
          "sdk_confidence": 0.8873,
          "truncated": false
        }
      ]
    },
    "fine": {
      "aggregate": {
        "value": "UNKNOWN",
        "scores": {
          "YES": 0.0,
          "NO": 1.0,
          "UNKNOWN": 0.0
        },
        "confidence": null,
        "margin": null,
        "evidence": null,
        "sdk_confidence": 1.0,
        "truncated": false,
        "conflict": true,
        "aggregation": "conflict_abstain",
        "passage_count": 2,
        "abstention_reason": "Opposing passage predictions; no reliable supersession established",
        "score_definition": "Native scores for selected passage; not aggregate document probabilities"
      },
      "passages": [
        {
          "value": "NO",
          "scores": {
            "YES": 0.0,
            "NO": 1.0,
            "UNKNOWN": 0.0
          },
          "confidence": 1.0,
          "margin": 1.0,
          "evidence": null,
          "sdk_confidence": 1.0,
          "truncated": false
        },
        {
          "value": "YES",
          "scores": {
            "YES": 1.0,
            "NO": 0.0,
            "UNKNOWN": 0.0
          },
          "confidence": 1.0,
          "margin": 1.0,
          "evidence": {
            "text": "Positions instructed for voting are immobilised from receipt of the instruction through the end of the Scheme Meeting.",
            "start": 36,
            "end": 154,
            "boundary": "sentence",
            "source": "sentence-level Laya candidate; exact substring, not human-verified explanation"
          },
          "sdk_confidence": 1.0,
          "truncated": false
        }
      ]
    }
  },
  "whole_document_probe": {
    "base": {
      "type": "choice",
      "choice": "YES",
      "probabilities": {
        "YES": 0.9785,
        "NO": 0.0117,
        "UNKNOWN": 0.0098
      },
      "confidence": 0.8919,
      "answer_confidence": 0.9785,
      "action": {
        "act_probability": 1.0
      }
    },
    "fine": {
      "type": "choice",
      "choice": "YES",
      "probabilities": {
        "YES": 1.0,
        "NO": 0.0,
        "UNKNOWN": 0.0
      },
      "confidence": 1.0,
      "answer_confidence": 1.0,
      "action": {
        "act_probability": 1.0
      }
    }
  }
}
```

### SYN-0383

Eligible holders may vote by proxy. Positions instructed for voting are immobilised from receipt of the instruction through the end of the Annual General Meeting.

Expected: SHARE_BLOCKING = YES.

```json
{
  "expected": "YES",
  "chunks": [
    {
      "text": "Eligible holders may vote by proxy.",
      "start": 0,
      "end": 35,
      "boundary": "sentence"
    },
    {
      "text": "Positions instructed for voting are immobilised from receipt of the instruction through the end of the Annual General Meeting.",
      "start": 36,
      "end": 162,
      "boundary": "sentence"
    }
  ],
  "original": {
    "base": {
      "aggregate": {
        "value": "YES",
        "scores": {
          "YES": 0.9816,
          "NO": 0.0084,
          "UNKNOWN": 0.0099
        },
        "confidence": 0.9816,
        "margin": 0.9717,
        "evidence": {
          "text": "Positions instructed for voting are immobilised from receipt of the instruction through the end of the Annual General Meeting.",
          "start": 36,
          "end": 162,
          "boundary": "sentence",
          "source": "sentence-level Laya candidate; exact substring, not human-verified explanation"
        },
        "sdk_confidence": 0.9051,
        "truncated": false,
        "conflict": false,
        "aggregation": "conflict_abstain",
        "passage_count": 2,
        "score_definition": "Native scores for selected passage; not aggregate document probabilities"
      },
      "passages": [
        {
          "value": "YES",
          "scores": {
            "YES": 0.9329,
            "NO": 0.0375,
            "UNKNOWN": 0.0296
          },
          "confidence": 0.9329,
          "margin": 0.8954,
          "evidence": {
            "text": "Eligible holders may vote by proxy.",
            "start": 0,
            "end": 35,
            "boundary": "sentence",
            "source": "sentence-level Laya candidate; exact substring, not human-verified explanation"
          },
          "sdk_confidence": 0.7341,
          "truncated": false
        },
        {
          "value": "YES",
          "scores": {
            "YES": 0.9816,
            "NO": 0.0084,
            "UNKNOWN": 0.0099
          },
          "confidence": 0.9816,
          "margin": 0.9717,
          "evidence": {
            "text": "Positions instructed for voting are immobilised from receipt of the instruction through the end of the Annual General Meeting.",
            "start": 36,
            "end": 162,
            "boundary": "sentence",
            "source": "sentence-level Laya candidate; exact substring, not human-verified explanation"
          },
          "sdk_confidence": 0.9051,
          "truncated": false
        }
      ]
    },
    "fine": {
      "aggregate": {
        "value": "UNKNOWN",
        "scores": {
          "YES": 0.0,
          "NO": 1.0,
          "UNKNOWN": 0.0
        },
        "confidence": null,
        "margin": null,
        "evidence": null,
        "sdk_confidence": 1.0,
        "truncated": false,
        "conflict": true,
        "aggregation": "conflict_abstain",
        "passage_count": 2,
        "abstention_reason": "Opposing passage predictions; no reliable supersession established",
        "score_definition": "Native scores for selected passage; not aggregate document probabilities"
      },
      "passages": [
        {
          "value": "NO",
          "scores": {
            "YES": 0.0,
            "NO": 1.0,
            "UNKNOWN": 0.0
          },
          "confidence": 1.0,
          "margin": 1.0,
          "evidence": null,
          "sdk_confidence": 1.0,
          "truncated": false
        },
        {
          "value": "YES",
          "scores": {
            "YES": 1.0,
            "NO": 0.0,
            "UNKNOWN": 0.0
          },
          "confidence": 1.0,
          "margin": 1.0,
          "evidence": {
            "text": "Positions instructed for voting are immobilised from receipt of the instruction through the end of the Annual General Meeting.",
            "start": 36,
            "end": 162,
            "boundary": "sentence",
            "source": "sentence-level Laya candidate; exact substring, not human-verified explanation"
          },
          "sdk_confidence": 1.0,
          "truncated": false
        }
      ]
    }
  },
  "whole_document_probe": {
    "base": {
      "type": "choice",
      "choice": "YES",
      "probabilities": {
        "YES": 0.9802,
        "NO": 0.0096,
        "UNKNOWN": 0.0102
      },
      "confidence": 0.8988,
      "answer_confidence": 0.9802,
      "action": {
        "act_probability": 1.0
      }
    },
    "fine": {
      "type": "choice",
      "choice": "YES",
      "probabilities": {
        "YES": 1.0,
        "NO": 0.0,
        "UNKNOWN": 0.0
      },
      "confidence": 1.0,
      "answer_confidence": 1.0,
      "action": {
        "act_probability": 1.0
      }
    }
  }
}
```

### SYN-0247

The event is votable. Securities corresponding to the instructed quantity will be blocked in the account until the securities blocking period end date.

Expected: SHARE_BLOCKING = YES.

```json
{
  "expected": "YES",
  "chunks": [
    {
      "text": "The event is votable.",
      "start": 0,
      "end": 21,
      "boundary": "sentence"
    },
    {
      "text": "Securities corresponding to the instructed quantity will be blocked in the account until the securities blocking period end date.",
      "start": 22,
      "end": 151,
      "boundary": "sentence"
    }
  ],
  "original": {
    "base": {
      "aggregate": {
        "value": "YES",
        "scores": {
          "YES": 0.9711,
          "NO": 0.0135,
          "UNKNOWN": 0.0153
        },
        "confidence": 0.9711,
        "margin": 0.9558,
        "evidence": {
          "text": "The event is votable.",
          "start": 0,
          "end": 21,
          "boundary": "sentence",
          "source": "sentence-level Laya candidate; exact substring, not human-verified explanation"
        },
        "sdk_confidence": 0.8628,
        "truncated": false,
        "conflict": false,
        "aggregation": "conflict_abstain",
        "passage_count": 2,
        "score_definition": "Native scores for selected passage; not aggregate document probabilities"
      },
      "passages": [
        {
          "value": "YES",
          "scores": {
            "YES": 0.9711,
            "NO": 0.0135,
            "UNKNOWN": 0.0153
          },
          "confidence": 0.9711,
          "margin": 0.9558,
          "evidence": {
            "text": "The event is votable.",
            "start": 0,
            "end": 21,
            "boundary": "sentence",
            "source": "sentence-level Laya candidate; exact substring, not human-verified explanation"
          },
          "sdk_confidence": 0.8628,
          "truncated": false
        },
        {
          "value": "YES",
          "scores": {
            "YES": 0.9687,
            "NO": 0.0107,
            "UNKNOWN": 0.0206
          },
          "confidence": 0.9687,
          "margin": 0.9481,
          "evidence": {
            "text": "Securities corresponding to the instructed quantity will be blocked in the account until the securities blocking period end date.",
            "start": 22,
            "end": 151,
            "boundary": "sentence",
            "source": "sentence-level Laya candidate; exact substring, not human-verified explanation"
          },
          "sdk_confidence": 0.8548,
          "truncated": false
        }
      ]
    },
    "fine": {
      "aggregate": {
        "value": "UNKNOWN",
        "scores": {
          "YES": 1.0,
          "NO": 0.0,
          "UNKNOWN": 0.0
        },
        "confidence": null,
        "margin": null,
        "evidence": null,
        "sdk_confidence": 1.0,
        "truncated": false,
        "conflict": true,
        "aggregation": "conflict_abstain",
        "passage_count": 2,
        "abstention_reason": "Opposing passage predictions; no reliable supersession established",
        "score_definition": "Native scores for selected passage; not aggregate document probabilities"
      },
      "passages": [
        {
          "value": "NO",
          "scores": {
            "YES": 0.0001,
            "NO": 0.9999,
            "UNKNOWN": 0.0
          },
          "confidence": 0.9999,
          "margin": 0.9998,
          "evidence": null,
          "sdk_confidence": 0.9994,
          "truncated": false
        },
        {
          "value": "YES",
          "scores": {
            "YES": 1.0,
            "NO": 0.0,
            "UNKNOWN": 0.0
          },
          "confidence": 1.0,
          "margin": 1.0,
          "evidence": {
            "text": "Securities corresponding to the instructed quantity will be blocked in the account until the securities blocking period end date.",
            "start": 22,
            "end": 151,
            "boundary": "sentence",
            "source": "sentence-level Laya candidate; exact substring, not human-verified explanation"
          },
          "sdk_confidence": 1.0,
          "truncated": false
        }
      ]
    }
  },
  "whole_document_probe": {
    "base": {
      "type": "choice",
      "choice": "YES",
      "probabilities": {
        "YES": 0.9592,
        "NO": 0.0163,
        "UNKNOWN": 0.0245
      },
      "confidence": 0.8197,
      "answer_confidence": 0.9592,
      "action": {
        "act_probability": 1.0
      }
    },
    "fine": {
      "type": "choice",
      "choice": "YES",
      "probabilities": {
        "YES": 1.0,
        "NO": 0.0,
        "UNKNOWN": 0.0
      },
      "confidence": 1.0,
      "answer_confidence": 1.0,
      "action": {
        "act_probability": 1.0
      }
    }
  }
}
```

### SYN-0443

The event is votable. Securities corresponding to the instructed quantity will be blocked in the account until the securities blocking period end date.

Expected: SHARE_BLOCKING = YES.

```json
{
  "expected": "YES",
  "chunks": [
    {
      "text": "The event is votable.",
      "start": 0,
      "end": 21,
      "boundary": "sentence"
    },
    {
      "text": "Securities corresponding to the instructed quantity will be blocked in the account until the securities blocking period end date.",
      "start": 22,
      "end": 151,
      "boundary": "sentence"
    }
  ],
  "original": {
    "base": {
      "aggregate": {
        "value": "YES",
        "scores": {
          "YES": 0.9711,
          "NO": 0.0135,
          "UNKNOWN": 0.0153
        },
        "confidence": 0.9711,
        "margin": 0.9558,
        "evidence": {
          "text": "The event is votable.",
          "start": 0,
          "end": 21,
          "boundary": "sentence",
          "source": "sentence-level Laya candidate; exact substring, not human-verified explanation"
        },
        "sdk_confidence": 0.8628,
        "truncated": false,
        "conflict": false,
        "aggregation": "conflict_abstain",
        "passage_count": 2,
        "score_definition": "Native scores for selected passage; not aggregate document probabilities"
      },
      "passages": [
        {
          "value": "YES",
          "scores": {
            "YES": 0.9711,
            "NO": 0.0135,
            "UNKNOWN": 0.0153
          },
          "confidence": 0.9711,
          "margin": 0.9558,
          "evidence": {
            "text": "The event is votable.",
            "start": 0,
            "end": 21,
            "boundary": "sentence",
            "source": "sentence-level Laya candidate; exact substring, not human-verified explanation"
          },
          "sdk_confidence": 0.8628,
          "truncated": false
        },
        {
          "value": "YES",
          "scores": {
            "YES": 0.9687,
            "NO": 0.0107,
            "UNKNOWN": 0.0206
          },
          "confidence": 0.9687,
          "margin": 0.9481,
          "evidence": {
            "text": "Securities corresponding to the instructed quantity will be blocked in the account until the securities blocking period end date.",
            "start": 22,
            "end": 151,
            "boundary": "sentence",
            "source": "sentence-level Laya candidate; exact substring, not human-verified explanation"
          },
          "sdk_confidence": 0.8548,
          "truncated": false
        }
      ]
    },
    "fine": {
      "aggregate": {
        "value": "UNKNOWN",
        "scores": {
          "YES": 1.0,
          "NO": 0.0,
          "UNKNOWN": 0.0
        },
        "confidence": null,
        "margin": null,
        "evidence": null,
        "sdk_confidence": 1.0,
        "truncated": false,
        "conflict": true,
        "aggregation": "conflict_abstain",
        "passage_count": 2,
        "abstention_reason": "Opposing passage predictions; no reliable supersession established",
        "score_definition": "Native scores for selected passage; not aggregate document probabilities"
      },
      "passages": [
        {
          "value": "NO",
          "scores": {
            "YES": 0.0001,
            "NO": 0.9999,
            "UNKNOWN": 0.0
          },
          "confidence": 0.9999,
          "margin": 0.9998,
          "evidence": null,
          "sdk_confidence": 0.9994,
          "truncated": false
        },
        {
          "value": "YES",
          "scores": {
            "YES": 1.0,
            "NO": 0.0,
            "UNKNOWN": 0.0
          },
          "confidence": 1.0,
          "margin": 1.0,
          "evidence": {
            "text": "Securities corresponding to the instructed quantity will be blocked in the account until the securities blocking period end date.",
            "start": 22,
            "end": 151,
            "boundary": "sentence",
            "source": "sentence-level Laya candidate; exact substring, not human-verified explanation"
          },
          "sdk_confidence": 1.0,
          "truncated": false
        }
      ]
    }
  },
  "whole_document_probe": {
    "base": {
      "type": "choice",
      "choice": "YES",
      "probabilities": {
        "YES": 0.9592,
        "NO": 0.0163,
        "UNKNOWN": 0.0245
      },
      "confidence": 0.8197,
      "answer_confidence": 0.9592,
      "action": {
        "act_probability": 1.0
      }
    },
    "fine": {
      "type": "choice",
      "choice": "YES",
      "probabilities": {
        "YES": 1.0,
        "NO": 0.0,
        "UNKNOWN": 0.0
      },
      "confidence": 1.0,
      "answer_confidence": 1.0,
      "action": {
        "act_probability": 1.0
      }
    }
  }
}
```

### SYN-0137

Eligible holders may vote by proxy. Positions instructed for voting are immobilised from receipt of the instruction through the end of the Extraordinary General Meeting.

Expected: SHARE_BLOCKING = YES.

```json
{
  "expected": "YES",
  "chunks": [
    {
      "text": "Eligible holders may vote by proxy.",
      "start": 0,
      "end": 35,
      "boundary": "sentence"
    },
    {
      "text": "Positions instructed for voting are immobilised from receipt of the instruction through the end of the Extraordinary General Meeting.",
      "start": 36,
      "end": 169,
      "boundary": "sentence"
    }
  ],
  "original": {
    "base": {
      "aggregate": {
        "value": "YES",
        "scores": {
          "YES": 0.9822,
          "NO": 0.0098,
          "UNKNOWN": 0.008
        },
        "confidence": 0.9822,
        "margin": 0.9723999999999999,
        "evidence": {
          "text": "Positions instructed for voting are immobilised from receipt of the instruction through the end of the Extraordinary General Meeting.",
          "start": 36,
          "end": 169,
          "boundary": "sentence",
          "source": "sentence-level Laya candidate; exact substring, not human-verified explanation"
        },
        "sdk_confidence": 0.9077,
        "truncated": false,
        "conflict": false,
        "aggregation": "conflict_abstain",
        "passage_count": 2,
        "score_definition": "Native scores for selected passage; not aggregate document probabilities"
      },
      "passages": [
        {
          "value": "YES",
          "scores": {
            "YES": 0.9329,
            "NO": 0.0375,
            "UNKNOWN": 0.0296
          },
          "confidence": 0.9329,
          "margin": 0.8954,
          "evidence": {
            "text": "Eligible holders may vote by proxy.",
            "start": 0,
            "end": 35,
            "boundary": "sentence",
            "source": "sentence-level Laya candidate; exact substring, not human-verified explanation"
          },
          "sdk_confidence": 0.7341,
          "truncated": false
        },
        {
          "value": "YES",
          "scores": {
            "YES": 0.9822,
            "NO": 0.0098,
            "UNKNOWN": 0.008
          },
          "confidence": 0.9822,
          "margin": 0.9723999999999999,
          "evidence": {
            "text": "Positions instructed for voting are immobilised from receipt of the instruction through the end of the Extraordinary General Meeting.",
            "start": 36,
            "end": 169,
            "boundary": "sentence",
            "source": "sentence-level Laya candidate; exact substring, not human-verified explanation"
          },
          "sdk_confidence": 0.9077,
          "truncated": false
        }
      ]
    },
    "fine": {
      "aggregate": {
        "value": "UNKNOWN",
        "scores": {
          "YES": 0.0,
          "NO": 1.0,
          "UNKNOWN": 0.0
        },
        "confidence": null,
        "margin": null,
        "evidence": null,
        "sdk_confidence": 1.0,
        "truncated": false,
        "conflict": true,
        "aggregation": "conflict_abstain",
        "passage_count": 2,
        "abstention_reason": "Opposing passage predictions; no reliable supersession established",
        "score_definition": "Native scores for selected passage; not aggregate document probabilities"
      },
      "passages": [
        {
          "value": "NO",
          "scores": {
            "YES": 0.0,
            "NO": 1.0,
            "UNKNOWN": 0.0
          },
          "confidence": 1.0,
          "margin": 1.0,
          "evidence": null,
          "sdk_confidence": 1.0,
          "truncated": false
        },
        {
          "value": "YES",
          "scores": {
            "YES": 1.0,
            "NO": 0.0,
            "UNKNOWN": 0.0
          },
          "confidence": 1.0,
          "margin": 1.0,
          "evidence": {
            "text": "Positions instructed for voting are immobilised from receipt of the instruction through the end of the Extraordinary General Meeting.",
            "start": 36,
            "end": 169,
            "boundary": "sentence",
            "source": "sentence-level Laya candidate; exact substring, not human-verified explanation"
          },
          "sdk_confidence": 1.0,
          "truncated": false
        }
      ]
    }
  },
  "whole_document_probe": {
    "base": {
      "type": "choice",
      "choice": "YES",
      "probabilities": {
        "YES": 0.9776,
        "NO": 0.0119,
        "UNKNOWN": 0.0105
      },
      "confidence": 0.8884,
      "answer_confidence": 0.9776,
      "action": {
        "act_probability": 1.0
      }
    },
    "fine": {
      "type": "choice",
      "choice": "YES",
      "probabilities": {
        "YES": 1.0,
        "NO": 0.0,
        "UNKNOWN": 0.0
      },
      "confidence": 1.0,
      "answer_confidence": 1.0,
      "action": {
        "act_probability": 1.0
      }
    }
  }
}
```

### SYN-0089

Eligible holders may vote by proxy. Positions instructed for voting are immobilised from receipt of the instruction through the end of the Scheme Meeting.

Expected: SHARE_BLOCKING = YES.

```json
{
  "expected": "YES",
  "chunks": [
    {
      "text": "Eligible holders may vote by proxy.",
      "start": 0,
      "end": 35,
      "boundary": "sentence"
    },
    {
      "text": "Positions instructed for voting are immobilised from receipt of the instruction through the end of the Scheme Meeting.",
      "start": 36,
      "end": 154,
      "boundary": "sentence"
    }
  ],
  "original": {
    "base": {
      "aggregate": {
        "value": "YES",
        "scores": {
          "YES": 0.9773,
          "NO": 0.0123,
          "UNKNOWN": 0.0104
        },
        "confidence": 0.9773,
        "margin": 0.965,
        "evidence": {
          "text": "Positions instructed for voting are immobilised from receipt of the instruction through the end of the Scheme Meeting.",
          "start": 36,
          "end": 154,
          "boundary": "sentence",
          "source": "sentence-level Laya candidate; exact substring, not human-verified explanation"
        },
        "sdk_confidence": 0.8873,
        "truncated": false,
        "conflict": false,
        "aggregation": "conflict_abstain",
        "passage_count": 2,
        "score_definition": "Native scores for selected passage; not aggregate document probabilities"
      },
      "passages": [
        {
          "value": "YES",
          "scores": {
            "YES": 0.9329,
            "NO": 0.0375,
            "UNKNOWN": 0.0296
          },
          "confidence": 0.9329,
          "margin": 0.8954,
          "evidence": {
            "text": "Eligible holders may vote by proxy.",
            "start": 0,
            "end": 35,
            "boundary": "sentence",
            "source": "sentence-level Laya candidate; exact substring, not human-verified explanation"
          },
          "sdk_confidence": 0.7341,
          "truncated": false
        },
        {
          "value": "YES",
          "scores": {
            "YES": 0.9773,
            "NO": 0.0123,
            "UNKNOWN": 0.0104
          },
          "confidence": 0.9773,
          "margin": 0.965,
          "evidence": {
            "text": "Positions instructed for voting are immobilised from receipt of the instruction through the end of the Scheme Meeting.",
            "start": 36,
            "end": 154,
            "boundary": "sentence",
            "source": "sentence-level Laya candidate; exact substring, not human-verified explanation"
          },
          "sdk_confidence": 0.8873,
          "truncated": false
        }
      ]
    },
    "fine": {
      "aggregate": {
        "value": "UNKNOWN",
        "scores": {
          "YES": 0.0,
          "NO": 1.0,
          "UNKNOWN": 0.0
        },
        "confidence": null,
        "margin": null,
        "evidence": null,
        "sdk_confidence": 1.0,
        "truncated": false,
        "conflict": true,
        "aggregation": "conflict_abstain",
        "passage_count": 2,
        "abstention_reason": "Opposing passage predictions; no reliable supersession established",
        "score_definition": "Native scores for selected passage; not aggregate document probabilities"
      },
      "passages": [
        {
          "value": "NO",
          "scores": {
            "YES": 0.0,
            "NO": 1.0,
            "UNKNOWN": 0.0
          },
          "confidence": 1.0,
          "margin": 1.0,
          "evidence": null,
          "sdk_confidence": 1.0,
          "truncated": false
        },
        {
          "value": "YES",
          "scores": {
            "YES": 1.0,
            "NO": 0.0,
            "UNKNOWN": 0.0
          },
          "confidence": 1.0,
          "margin": 1.0,
          "evidence": {
            "text": "Positions instructed for voting are immobilised from receipt of the instruction through the end of the Scheme Meeting.",
            "start": 36,
            "end": 154,
            "boundary": "sentence",
            "source": "sentence-level Laya candidate; exact substring, not human-verified explanation"
          },
          "sdk_confidence": 1.0,
          "truncated": false
        }
      ]
    }
  },
  "whole_document_probe": {
    "base": {
      "type": "choice",
      "choice": "YES",
      "probabilities": {
        "YES": 0.9785,
        "NO": 0.0117,
        "UNKNOWN": 0.0098
      },
      "confidence": 0.8919,
      "answer_confidence": 0.9785,
      "action": {
        "act_probability": 1.0
      }
    },
    "fine": {
      "type": "choice",
      "choice": "YES",
      "probabilities": {
        "YES": 1.0,
        "NO": 0.0,
        "UNKNOWN": 0.0
      },
      "confidence": 1.0,
      "answer_confidence": 1.0,
      "action": {
        "act_probability": 1.0
      }
    }
  }
}
```

### SYN-0486

Voting instructions may be submitted for Silverline Logistics SE's Extraordinary General Meeting. Once a valid instruction is received, the instructed shares will be blocked and cannot be sold or transferred until the meeting has concluded.

Expected: SHARE_BLOCKING = YES.

```json
{
  "expected": "YES",
  "chunks": [
    {
      "text": "Voting instructions may be submitted for Silverline Logistics SE's Extraordinary General Meeting.",
      "start": 0,
      "end": 97,
      "boundary": "sentence"
    },
    {
      "text": "Once a valid instruction is received, the instructed shares will be blocked and cannot be sold or transferred until the meeting has concluded.",
      "start": 98,
      "end": 240,
      "boundary": "sentence"
    }
  ],
  "original": {
    "base": {
      "aggregate": {
        "value": "YES",
        "scores": {
          "YES": 0.9798,
          "NO": 0.0072,
          "UNKNOWN": 0.013
        },
        "confidence": 0.9798,
        "margin": 0.9668,
        "evidence": {
          "text": "Once a valid instruction is received, the instructed shares will be blocked and cannot be sold or transferred until the meeting has concluded.",
          "start": 98,
          "end": 240,
          "boundary": "sentence",
          "source": "sentence-level Laya candidate; exact substring, not human-verified explanation"
        },
        "sdk_confidence": 0.8981,
        "truncated": false,
        "conflict": false,
        "aggregation": "conflict_abstain",
        "passage_count": 2,
        "score_definition": "Native scores for selected passage; not aggregate document probabilities"
      },
      "passages": [
        {
          "value": "YES",
          "scores": {
            "YES": 0.9301,
            "NO": 0.0273,
            "UNKNOWN": 0.0426
          },
          "confidence": 0.9301,
          "margin": 0.8875000000000001,
          "evidence": {
            "text": "Voting instructions may be submitted for Silverline Logistics SE's Extraordinary General Meeting.",
            "start": 0,
            "end": 97,
            "boundary": "sentence",
            "source": "sentence-level Laya candidate; exact substring, not human-verified explanation"
          },
          "sdk_confidence": 0.7267,
          "truncated": false
        },
        {
          "value": "YES",
          "scores": {
            "YES": 0.9798,
            "NO": 0.0072,
            "UNKNOWN": 0.013
          },
          "confidence": 0.9798,
          "margin": 0.9668,
          "evidence": {
            "text": "Once a valid instruction is received, the instructed shares will be blocked and cannot be sold or transferred until the meeting has concluded.",
            "start": 98,
            "end": 240,
            "boundary": "sentence",
            "source": "sentence-level Laya candidate; exact substring, not human-verified explanation"
          },
          "sdk_confidence": 0.8981,
          "truncated": false
        }
      ]
    },
    "fine": {
      "aggregate": {
        "value": "UNKNOWN",
        "scores": {
          "YES": 0.0,
          "NO": 1.0,
          "UNKNOWN": 0.0
        },
        "confidence": null,
        "margin": null,
        "evidence": null,
        "sdk_confidence": 1.0,
        "truncated": false,
        "conflict": true,
        "aggregation": "conflict_abstain",
        "passage_count": 2,
        "abstention_reason": "Opposing passage predictions; no reliable supersession established",
        "score_definition": "Native scores for selected passage; not aggregate document probabilities"
      },
      "passages": [
        {
          "value": "NO",
          "scores": {
            "YES": 0.0,
            "NO": 1.0,
            "UNKNOWN": 0.0
          },
          "confidence": 1.0,
          "margin": 1.0,
          "evidence": null,
          "sdk_confidence": 1.0,
          "truncated": false
        },
        {
          "value": "YES",
          "scores": {
            "YES": 1.0,
            "NO": 0.0,
            "UNKNOWN": 0.0
          },
          "confidence": 1.0,
          "margin": 1.0,
          "evidence": {
            "text": "Once a valid instruction is received, the instructed shares will be blocked and cannot be sold or transferred until the meeting has concluded.",
            "start": 98,
            "end": 240,
            "boundary": "sentence",
            "source": "sentence-level Laya candidate; exact substring, not human-verified explanation"
          },
          "sdk_confidence": 1.0,
          "truncated": false
        }
      ]
    }
  },
  "whole_document_probe": {
    "base": {
      "type": "choice",
      "choice": "YES",
      "probabilities": {
        "YES": 0.9696,
        "NO": 0.0131,
        "UNKNOWN": 0.0173
      },
      "confidence": 0.8573,
      "answer_confidence": 0.9696,
      "action": {
        "act_probability": 1.0
      }
    },
    "fine": {
      "type": "choice",
      "choice": "YES",
      "probabilities": {
        "YES": 1.0,
        "NO": 0.0,
        "UNKNOWN": 0.0
      },
      "confidence": 1.0,
      "answer_confidence": 1.0,
      "action": {
        "act_probability": 1.0
      }
    }
  }
}
```

### SYN-0378

Voting is available for Danube Infrastructure SA's Scheme Meeting. As conditions of participation, the instructed shares will be blocked until the meeting ends; beneficial-owner details must be disclosed.

Expected: SHARE_BLOCKING = YES.

```json
{
  "expected": "YES",
  "chunks": [
    {
      "text": "Voting is available for Danube Infrastructure SA's Scheme Meeting.",
      "start": 0,
      "end": 66,
      "boundary": "sentence"
    },
    {
      "text": "As conditions of participation, the instructed shares will be blocked until the meeting ends; beneficial-owner details must be disclosed.",
      "start": 67,
      "end": 204,
      "boundary": "sentence"
    }
  ],
  "original": {
    "base": {
      "aggregate": {
        "value": "YES",
        "scores": {
          "YES": 0.9536,
          "NO": 0.0234,
          "UNKNOWN": 0.023
        },
        "confidence": 0.9536,
        "margin": 0.9302,
        "evidence": {
          "text": "As conditions of participation, the instructed shares will be blocked until the meeting ends; beneficial-owner details must be disclosed.",
          "start": 67,
          "end": 204,
          "boundary": "sentence",
          "source": "sentence-level Laya candidate; exact substring, not human-verified explanation"
        },
        "sdk_confidence": 0.7999,
        "truncated": false,
        "conflict": false,
        "aggregation": "conflict_abstain",
        "passage_count": 2,
        "score_definition": "Native scores for selected passage; not aggregate document probabilities"
      },
      "passages": [
        {
          "value": "YES",
          "scores": {
            "YES": 0.895,
            "NO": 0.0563,
            "UNKNOWN": 0.0487
          },
          "confidence": 0.895,
          "margin": 0.8387,
          "evidence": {
            "text": "Voting is available for Danube Infrastructure SA's Scheme Meeting.",
            "start": 0,
            "end": 66,
            "boundary": "sentence",
            "source": "sentence-level Laya candidate; exact substring, not human-verified explanation"
          },
          "sdk_confidence": 0.6283,
          "truncated": false
        },
        {
          "value": "YES",
          "scores": {
            "YES": 0.9536,
            "NO": 0.0234,
            "UNKNOWN": 0.023
          },
          "confidence": 0.9536,
          "margin": 0.9302,
          "evidence": {
            "text": "As conditions of participation, the instructed shares will be blocked until the meeting ends; beneficial-owner details must be disclosed.",
            "start": 67,
            "end": 204,
            "boundary": "sentence",
            "source": "sentence-level Laya candidate; exact substring, not human-verified explanation"
          },
          "sdk_confidence": 0.7999,
          "truncated": false
        }
      ]
    },
    "fine": {
      "aggregate": {
        "value": "UNKNOWN",
        "scores": {
          "YES": 0.0,
          "NO": 1.0,
          "UNKNOWN": 0.0
        },
        "confidence": null,
        "margin": null,
        "evidence": null,
        "sdk_confidence": 1.0,
        "truncated": false,
        "conflict": true,
        "aggregation": "conflict_abstain",
        "passage_count": 2,
        "abstention_reason": "Opposing passage predictions; no reliable supersession established",
        "score_definition": "Native scores for selected passage; not aggregate document probabilities"
      },
      "passages": [
        {
          "value": "NO",
          "scores": {
            "YES": 0.0,
            "NO": 1.0,
            "UNKNOWN": 0.0
          },
          "confidence": 1.0,
          "margin": 1.0,
          "evidence": null,
          "sdk_confidence": 1.0,
          "truncated": false
        },
        {
          "value": "YES",
          "scores": {
            "YES": 1.0,
            "NO": 0.0,
            "UNKNOWN": 0.0
          },
          "confidence": 1.0,
          "margin": 1.0,
          "evidence": {
            "text": "As conditions of participation, the instructed shares will be blocked until the meeting ends; beneficial-owner details must be disclosed.",
            "start": 67,
            "end": 204,
            "boundary": "sentence",
            "source": "sentence-level Laya candidate; exact substring, not human-verified explanation"
          },
          "sdk_confidence": 1.0,
          "truncated": false
        }
      ]
    }
  },
  "whole_document_probe": {
    "base": {
      "type": "choice",
      "choice": "YES",
      "probabilities": {
        "YES": 0.9287,
        "NO": 0.0409,
        "UNKNOWN": 0.0305
      },
      "confidence": 0.7217,
      "answer_confidence": 0.9287,
      "action": {
        "act_probability": 1.0
      }
    },
    "fine": {
      "type": "choice",
      "choice": "YES",
      "probabilities": {
        "YES": 1.0,
        "NO": 0.0,
        "UNKNOWN": 0.0
      },
      "confidence": 1.0,
      "answer_confidence": 1.0,
      "action": {
        "act_probability": 1.0
      }
    }
  }
}
```

### SYN-0154

Voting is available for Alpine Systems AG's Extraordinary General Meeting. As conditions of participation, the instructed shares will be blocked until the meeting ends; a valid power of attorney must be on file; beneficial-owner details must be disclosed.

Expected: SHARE_BLOCKING = YES.

```json
{
  "expected": "YES",
  "chunks": [
    {
      "text": "Voting is available for Alpine Systems AG's Extraordinary General Meeting.",
      "start": 0,
      "end": 74,
      "boundary": "sentence"
    },
    {
      "text": "As conditions of participation, the instructed shares will be blocked until the meeting ends; a valid power of attorney must be on file; beneficial-owner details must be disclosed.",
      "start": 75,
      "end": 255,
      "boundary": "sentence"
    }
  ],
  "original": {
    "base": {
      "aggregate": {
        "value": "YES",
        "scores": {
          "YES": 0.9589,
          "NO": 0.0191,
          "UNKNOWN": 0.022
        },
        "confidence": 0.9589,
        "margin": 0.9369,
        "evidence": {
          "text": "As conditions of participation, the instructed shares will be blocked until the meeting ends; a valid power of attorney must be on file; beneficial-owner details must be disclosed.",
          "start": 75,
          "end": 255,
          "boundary": "sentence",
          "source": "sentence-level Laya candidate; exact substring, not human-verified explanation"
        },
        "sdk_confidence": 0.8183,
        "truncated": false,
        "conflict": false,
        "aggregation": "conflict_abstain",
        "passage_count": 2,
        "score_definition": "Native scores for selected passage; not aggregate document probabilities"
      },
      "passages": [
        {
          "value": "YES",
          "scores": {
            "YES": 0.9466,
            "NO": 0.0244,
            "UNKNOWN": 0.029
          },
          "confidence": 0.9466,
          "margin": 0.9176,
          "evidence": {
            "text": "Voting is available for Alpine Systems AG's Extraordinary General Meeting.",
            "start": 0,
            "end": 74,
            "boundary": "sentence",
            "source": "sentence-level Laya candidate; exact substring, not human-verified explanation"
          },
          "sdk_confidence": 0.7768,
          "truncated": false
        },
        {
          "value": "YES",
          "scores": {
            "YES": 0.9589,
            "NO": 0.0191,
            "UNKNOWN": 0.022
          },
          "confidence": 0.9589,
          "margin": 0.9369,
          "evidence": {
            "text": "As conditions of participation, the instructed shares will be blocked until the meeting ends; a valid power of attorney must be on file; beneficial-owner details must be disclosed.",
            "start": 75,
            "end": 255,
            "boundary": "sentence",
            "source": "sentence-level Laya candidate; exact substring, not human-verified explanation"
          },
          "sdk_confidence": 0.8183,
          "truncated": false
        }
      ]
    },
    "fine": {
      "aggregate": {
        "value": "UNKNOWN",
        "scores": {
          "YES": 0.0,
          "NO": 1.0,
          "UNKNOWN": 0.0
        },
        "confidence": null,
        "margin": null,
        "evidence": null,
        "sdk_confidence": 1.0,
        "truncated": false,
        "conflict": true,
        "aggregation": "conflict_abstain",
        "passage_count": 2,
        "abstention_reason": "Opposing passage predictions; no reliable supersession established",
        "score_definition": "Native scores for selected passage; not aggregate document probabilities"
      },
      "passages": [
        {
          "value": "NO",
          "scores": {
            "YES": 0.0,
            "NO": 1.0,
            "UNKNOWN": 0.0
          },
          "confidence": 1.0,
          "margin": 1.0,
          "evidence": null,
          "sdk_confidence": 1.0,
          "truncated": false
        },
        {
          "value": "YES",
          "scores": {
            "YES": 1.0,
            "NO": 0.0,
            "UNKNOWN": 0.0
          },
          "confidence": 1.0,
          "margin": 1.0,
          "evidence": {
            "text": "As conditions of participation, the instructed shares will be blocked until the meeting ends; a valid power of attorney must be on file; beneficial-owner details must be disclosed.",
            "start": 75,
            "end": 255,
            "boundary": "sentence",
            "source": "sentence-level Laya candidate; exact substring, not human-verified explanation"
          },
          "sdk_confidence": 1.0,
          "truncated": false
        }
      ]
    }
  },
  "whole_document_probe": {
    "base": {
      "type": "choice",
      "choice": "YES",
      "probabilities": {
        "YES": 0.9633,
        "NO": 0.017,
        "UNKNOWN": 0.0197
      },
      "confidence": 0.8336,
      "answer_confidence": 0.9633,
      "action": {
        "act_probability": 1.0
      }
    },
    "fine": {
      "type": "choice",
      "choice": "YES",
      "probabilities": {
        "YES": 1.0,
        "NO": 0.0,
        "UNKNOWN": 0.0
      },
      "confidence": 1.0,
      "answer_confidence": 1.0,
      "action": {
        "act_probability": 1.0
      }
    }
  }
}
```

### SYN-0362

Voting is available for Helios Medical NV's Extraordinary General Meeting. As conditions of participation, the instructed shares will be blocked until the meeting ends; a valid power of attorney must be on file; beneficial-owner details must be disclosed.

Expected: SHARE_BLOCKING = YES.

```json
{
  "expected": "YES",
  "chunks": [
    {
      "text": "Voting is available for Helios Medical NV's Extraordinary General Meeting.",
      "start": 0,
      "end": 74,
      "boundary": "sentence"
    },
    {
      "text": "As conditions of participation, the instructed shares will be blocked until the meeting ends; a valid power of attorney must be on file; beneficial-owner details must be disclosed.",
      "start": 75,
      "end": 255,
      "boundary": "sentence"
    }
  ],
  "original": {
    "base": {
      "aggregate": {
        "value": "YES",
        "scores": {
          "YES": 0.9589,
          "NO": 0.0191,
          "UNKNOWN": 0.022
        },
        "confidence": 0.9589,
        "margin": 0.9369,
        "evidence": {
          "text": "As conditions of participation, the instructed shares will be blocked until the meeting ends; a valid power of attorney must be on file; beneficial-owner details must be disclosed.",
          "start": 75,
          "end": 255,
          "boundary": "sentence",
          "source": "sentence-level Laya candidate; exact substring, not human-verified explanation"
        },
        "sdk_confidence": 0.8183,
        "truncated": false,
        "conflict": false,
        "aggregation": "conflict_abstain",
        "passage_count": 2,
        "score_definition": "Native scores for selected passage; not aggregate document probabilities"
      },
      "passages": [
        {
          "value": "YES",
          "scores": {
            "YES": 0.9551,
            "NO": 0.0183,
            "UNKNOWN": 0.0266
          },
          "confidence": 0.9551,
          "margin": 0.9285,
          "evidence": {
            "text": "Voting is available for Helios Medical NV's Extraordinary General Meeting.",
            "start": 0,
            "end": 74,
            "boundary": "sentence",
            "source": "sentence-level Laya candidate; exact substring, not human-verified explanation"
          },
          "sdk_confidence": 0.8055,
          "truncated": false
        },
        {
          "value": "YES",
          "scores": {
            "YES": 0.9589,
            "NO": 0.0191,
            "UNKNOWN": 0.022
          },
          "confidence": 0.9589,
          "margin": 0.9369,
          "evidence": {
            "text": "As conditions of participation, the instructed shares will be blocked until the meeting ends; a valid power of attorney must be on file; beneficial-owner details must be disclosed.",
            "start": 75,
            "end": 255,
            "boundary": "sentence",
            "source": "sentence-level Laya candidate; exact substring, not human-verified explanation"
          },
          "sdk_confidence": 0.8183,
          "truncated": false
        }
      ]
    },
    "fine": {
      "aggregate": {
        "value": "UNKNOWN",
        "scores": {
          "YES": 0.0,
          "NO": 1.0,
          "UNKNOWN": 0.0
        },
        "confidence": null,
        "margin": null,
        "evidence": null,
        "sdk_confidence": 1.0,
        "truncated": false,
        "conflict": true,
        "aggregation": "conflict_abstain",
        "passage_count": 2,
        "abstention_reason": "Opposing passage predictions; no reliable supersession established",
        "score_definition": "Native scores for selected passage; not aggregate document probabilities"
      },
      "passages": [
        {
          "value": "NO",
          "scores": {
            "YES": 0.0,
            "NO": 1.0,
            "UNKNOWN": 0.0
          },
          "confidence": 1.0,
          "margin": 1.0,
          "evidence": null,
          "sdk_confidence": 1.0,
          "truncated": false
        },
        {
          "value": "YES",
          "scores": {
            "YES": 1.0,
            "NO": 0.0,
            "UNKNOWN": 0.0
          },
          "confidence": 1.0,
          "margin": 1.0,
          "evidence": {
            "text": "As conditions of participation, the instructed shares will be blocked until the meeting ends; a valid power of attorney must be on file; beneficial-owner details must be disclosed.",
            "start": 75,
            "end": 255,
            "boundary": "sentence",
            "source": "sentence-level Laya candidate; exact substring, not human-verified explanation"
          },
          "sdk_confidence": 1.0,
          "truncated": false
        }
      ]
    }
  },
  "whole_document_probe": {
    "base": {
      "type": "choice",
      "choice": "YES",
      "probabilities": {
        "YES": 0.969,
        "NO": 0.0139,
        "UNKNOWN": 0.0171
      },
      "confidence": 0.8547,
      "answer_confidence": 0.969,
      "action": {
        "act_probability": 1.0
      }
    },
    "fine": {
      "type": "choice",
      "choice": "YES",
      "probabilities": {
        "YES": 1.0,
        "NO": 0.0,
        "UNKNOWN": 0.0
      },
      "confidence": 1.0,
      "answer_confidence": 1.0,
      "action": {
        "act_probability": 1.0
      }
    }
  }
}
```
