# Event learning qualification — every scored failure

AI-authored synthetic engineering labels only. Scores are native model outputs; calibrated confidence is unavailable. Do not reuse frozen errors as training data.


## VALIDATION / 1 / Laya / 192427e9aa3ca6f904eb505ac724d3c90e8eba48b9c676788a55d6e407fcb195

```json
{
  "candidate": "Laya",
  "id": "192427e9aa3ca6f904eb505ac724d3c90e8eba48b9c676788a55d6e407fcb195",
  "text": "[Message EL0206C | MT564]\nBroker service update: the institutional ballot channel is now available for this agenda.\nThis is solely a cash-distribution advice; it offers no meeting ballot and no shareholder vote.\nNo requirement for a voting lock on the position applies.\nNo requirement for a compulsory attorney mandate applies.\nNo requirement for mandatory meeting registration applies.\nNo requirement for identification of the underlying owner applies.\nNo requirement for a custodial holding statement applies.\nNo requirement for a requirement to cast all votes identically applies.\nNo requirement for recall of lent securities applies.\nNo requirement for an in-person-only voting condition applies.\n\n\n[Message EL0206D | MT568]\nPlease retain the replacement edition for operational reconciliation. Earlier notification conditions are superseded.\n",
  "predicate": "share_blocking",
  "truth": "NO",
  "prediction": {
    "value": "YES",
    "scores": {
      "YES": 0.9242,
      "NO": 0.0505,
      "UNKNOWN": 0.0253
    },
    "confidence": null,
    "native_score": 0.9242,
    "source": "REGISTERED_LAYA_WHOLE_NOTICE",
    "evidence": [],
    "evidence_status": "UNAVAILABLE: this decision head does not extract quotations"
  },
  "decision": {
    "classification": "NOT_VOTABLE",
    "rule": "R2 no current voting opportunity",
    "rule_version": "semantic-decision-2",
    "manual_review_required": true,
    "automation_enabled": false,
    "review_reasons": [
      "Synthetic-only evaluation; customer quality gate not met"
    ]
  }
}
```


## VALIDATION / 2 / Laya / 192427e9aa3ca6f904eb505ac724d3c90e8eba48b9c676788a55d6e407fcb195

```json
{
  "candidate": "Laya",
  "id": "192427e9aa3ca6f904eb505ac724d3c90e8eba48b9c676788a55d6e407fcb195",
  "text": "[Message EL0206C | MT564]\nBroker service update: the institutional ballot channel is now available for this agenda.\nThis is solely a cash-distribution advice; it offers no meeting ballot and no shareholder vote.\nNo requirement for a voting lock on the position applies.\nNo requirement for a compulsory attorney mandate applies.\nNo requirement for mandatory meeting registration applies.\nNo requirement for identification of the underlying owner applies.\nNo requirement for a custodial holding statement applies.\nNo requirement for a requirement to cast all votes identically applies.\nNo requirement for recall of lent securities applies.\nNo requirement for an in-person-only voting condition applies.\n\n\n[Message EL0206D | MT568]\nPlease retain the replacement edition for operational reconciliation. Earlier notification conditions are superseded.\n",
  "predicate": "registration_required",
  "truth": "NO",
  "prediction": {
    "value": "YES",
    "scores": {
      "YES": 0.4292,
      "NO": 0.4262,
      "UNKNOWN": 0.1446
    },
    "confidence": null,
    "native_score": 0.4292,
    "source": "REGISTERED_LAYA_WHOLE_NOTICE",
    "evidence": [],
    "evidence_status": "UNAVAILABLE: this decision head does not extract quotations"
  },
  "decision": {
    "classification": "NOT_VOTABLE",
    "rule": "R2 no current voting opportunity",
    "rule_version": "semantic-decision-2",
    "manual_review_required": true,
    "automation_enabled": false,
    "review_reasons": [
      "Synthetic-only evaluation; customer quality gate not met"
    ]
  }
}
```


## VALIDATION / 3 / Laya / 192427e9aa3ca6f904eb505ac724d3c90e8eba48b9c676788a55d6e407fcb195

```json
{
  "candidate": "Laya",
  "id": "192427e9aa3ca6f904eb505ac724d3c90e8eba48b9c676788a55d6e407fcb195",
  "text": "[Message EL0206C | MT564]\nBroker service update: the institutional ballot channel is now available for this agenda.\nThis is solely a cash-distribution advice; it offers no meeting ballot and no shareholder vote.\nNo requirement for a voting lock on the position applies.\nNo requirement for a compulsory attorney mandate applies.\nNo requirement for mandatory meeting registration applies.\nNo requirement for identification of the underlying owner applies.\nNo requirement for a custodial holding statement applies.\nNo requirement for a requirement to cast all votes identically applies.\nNo requirement for recall of lent securities applies.\nNo requirement for an in-person-only voting condition applies.\n\n\n[Message EL0206D | MT568]\nPlease retain the replacement edition for operational reconciliation. Earlier notification conditions are superseded.\n",
  "predicate": "holding_confirmation_required",
  "truth": "NO",
  "prediction": {
    "value": "YES",
    "scores": {
      "YES": 0.5881,
      "NO": 0.2247,
      "UNKNOWN": 0.1872
    },
    "confidence": null,
    "native_score": 0.5881,
    "source": "REGISTERED_LAYA_WHOLE_NOTICE",
    "evidence": [],
    "evidence_status": "UNAVAILABLE: this decision head does not extract quotations"
  },
  "decision": {
    "classification": "NOT_VOTABLE",
    "rule": "R2 no current voting opportunity",
    "rule_version": "semantic-decision-2",
    "manual_review_required": true,
    "automation_enabled": false,
    "review_reasons": [
      "Synthetic-only evaluation; customer quality gate not met"
    ]
  }
}
```


## VALIDATION / 4 / Laya / 192427e9aa3ca6f904eb505ac724d3c90e8eba48b9c676788a55d6e407fcb195

```json
{
  "candidate": "Laya",
  "id": "192427e9aa3ca6f904eb505ac724d3c90e8eba48b9c676788a55d6e407fcb195",
  "text": "[Message EL0206C | MT564]\nBroker service update: the institutional ballot channel is now available for this agenda.\nThis is solely a cash-distribution advice; it offers no meeting ballot and no shareholder vote.\nNo requirement for a voting lock on the position applies.\nNo requirement for a compulsory attorney mandate applies.\nNo requirement for mandatory meeting registration applies.\nNo requirement for identification of the underlying owner applies.\nNo requirement for a custodial holding statement applies.\nNo requirement for a requirement to cast all votes identically applies.\nNo requirement for recall of lent securities applies.\nNo requirement for an in-person-only voting condition applies.\n\n\n[Message EL0206D | MT568]\nPlease retain the replacement edition for operational reconciliation. Earlier notification conditions are superseded.\n",
  "predicate": "securities_lending_recall_required",
  "truth": "NO",
  "prediction": {
    "value": "YES",
    "scores": {
      "YES": 0.5857,
      "NO": 0.3415,
      "UNKNOWN": 0.0728
    },
    "confidence": null,
    "native_score": 0.5857,
    "source": "REGISTERED_LAYA_WHOLE_NOTICE",
    "evidence": [],
    "evidence_status": "UNAVAILABLE: this decision head does not extract quotations"
  },
  "decision": {
    "classification": "NOT_VOTABLE",
    "rule": "R2 no current voting opportunity",
    "rule_version": "semantic-decision-2",
    "manual_review_required": true,
    "automation_enabled": false,
    "review_reasons": [
      "Synthetic-only evaluation; customer quality gate not met"
    ]
  }
}
```


## VALIDATION / 5 / Laya / 192427e9aa3ca6f904eb505ac724d3c90e8eba48b9c676788a55d6e407fcb195

```json
{
  "candidate": "Laya",
  "id": "192427e9aa3ca6f904eb505ac724d3c90e8eba48b9c676788a55d6e407fcb195",
  "text": "[Message EL0206C | MT564]\nBroker service update: the institutional ballot channel is now available for this agenda.\nThis is solely a cash-distribution advice; it offers no meeting ballot and no shareholder vote.\nNo requirement for a voting lock on the position applies.\nNo requirement for a compulsory attorney mandate applies.\nNo requirement for mandatory meeting registration applies.\nNo requirement for identification of the underlying owner applies.\nNo requirement for a custodial holding statement applies.\nNo requirement for a requirement to cast all votes identically applies.\nNo requirement for recall of lent securities applies.\nNo requirement for an in-person-only voting condition applies.\n\n\n[Message EL0206D | MT568]\nPlease retain the replacement edition for operational reconciliation. Earlier notification conditions are superseded.\n",
  "predicate": "other_voting_restriction",
  "truth": "NO",
  "prediction": {
    "value": "YES",
    "scores": {
      "YES": 0.5337,
      "NO": 0.3905,
      "UNKNOWN": 0.0758
    },
    "confidence": null,
    "native_score": 0.5337,
    "source": "REGISTERED_LAYA_WHOLE_NOTICE",
    "evidence": [],
    "evidence_status": "UNAVAILABLE: this decision head does not extract quotations"
  },
  "decision": {
    "classification": "NOT_VOTABLE",
    "rule": "R2 no current voting opportunity",
    "rule_version": "semantic-decision-2",
    "manual_review_required": true,
    "automation_enabled": false,
    "review_reasons": [
      "Synthetic-only evaluation; customer quality gate not met"
    ]
  }
}
```


## VALIDATION / 6 / Laya / 255328bb369bd44fa7cb0a788d797be6085e4bdab88a810f35f8b14469f269d2

```json
{
  "candidate": "Laya",
  "id": "255328bb369bd44fa7cb0a788d797be6085e4bdab88a810f35f8b14469f269d2",
  "text": "[Message EL0107C | MT564]\nIssuer secretariat memorandum concerning arrangements for the forthcoming extraordinary assembly.\nParticipation may become possible, but the agent has not established whether this holder can vote.\nFor this vote, voting-related immobilisation is required.\nThe receiving agent has not resolved whether an obligatory power-of-attorney document is required for this vote.\nNo requirement for a required voter registration form applies.\nNo requirement for beneficial-owner disclosure applies.\nFor this vote, documentary confirmation of ownership is required.\nNo requirement for a ban on splitting voting instructions applies.\nNo requirement for retrieval of loaned voting positions applies.\nNo requirement for a mandatory paper-only ballot applies.\n\n\n[Message EL0107D | MT568]\nPlease retain the replacement edition for operational reconciliation. Earlier notification conditions are superseded.\n",
  "predicate": "votability",
  "truth": "UNCERTAIN",
  "prediction": {
    "value": "NOT_VOTABLE",
    "scores": {
      "VOTABLE": 0.1924,
      "NOT_VOTABLE": 0.5364,
      "UNCERTAIN": 0.2713
    },
    "confidence": null,
    "native_score": 0.5364,
    "source": "REGISTERED_LAYA_WHOLE_NOTICE",
    "evidence": [],
    "evidence_status": "UNAVAILABLE: this decision head does not extract quotations"
  },
  "decision": {
    "classification": "NOT_VOTABLE",
    "rule": "R2 no current voting opportunity",
    "rule_version": "semantic-decision-2",
    "manual_review_required": true,
    "automation_enabled": false,
    "review_reasons": [
      "Synthetic-only evaluation; customer quality gate not met"
    ]
  }
}
```


## VALIDATION / 7 / Laya / 255328bb369bd44fa7cb0a788d797be6085e4bdab88a810f35f8b14469f269d2

```json
{
  "candidate": "Laya",
  "id": "255328bb369bd44fa7cb0a788d797be6085e4bdab88a810f35f8b14469f269d2",
  "text": "[Message EL0107C | MT564]\nIssuer secretariat memorandum concerning arrangements for the forthcoming extraordinary assembly.\nParticipation may become possible, but the agent has not established whether this holder can vote.\nFor this vote, voting-related immobilisation is required.\nThe receiving agent has not resolved whether an obligatory power-of-attorney document is required for this vote.\nNo requirement for a required voter registration form applies.\nNo requirement for beneficial-owner disclosure applies.\nFor this vote, documentary confirmation of ownership is required.\nNo requirement for a ban on splitting voting instructions applies.\nNo requirement for retrieval of loaned voting positions applies.\nNo requirement for a mandatory paper-only ballot applies.\n\n\n[Message EL0107D | MT568]\nPlease retain the replacement edition for operational reconciliation. Earlier notification conditions are superseded.\n",
  "predicate": "poa_required",
  "truth": "UNKNOWN",
  "prediction": {
    "value": "NO",
    "scores": {
      "YES": 0.0579,
      "NO": 0.9147,
      "UNKNOWN": 0.0273
    },
    "confidence": null,
    "native_score": 0.9147,
    "source": "REGISTERED_LAYA_WHOLE_NOTICE",
    "evidence": [],
    "evidence_status": "UNAVAILABLE: this decision head does not extract quotations"
  },
  "decision": {
    "classification": "NOT_VOTABLE",
    "rule": "R2 no current voting opportunity",
    "rule_version": "semantic-decision-2",
    "manual_review_required": true,
    "automation_enabled": false,
    "review_reasons": [
      "Synthetic-only evaluation; customer quality gate not met"
    ]
  }
}
```


## VALIDATION / 8 / Laya / 25150120b9a9e92a98ab8b33fb003cab98a2ec6b4230ec908fda5c15d2bbc7d7

```json
{
  "candidate": "Laya",
  "id": "25150120b9a9e92a98ab8b33fb003cab98a2ec6b4230ec908fda5c15d2bbc7d7",
  "text": "[Message EL0105C | MT564]\nIssuer secretariat memorandum concerning arrangements for the forthcoming extraordinary assembly.\nThe current agenda is open for shareholder voting instructions.\nNo requirement for voting-related immobilisation applies.\nNo requirement for an obligatory power-of-attorney document applies.\nFor this vote, a required voter registration form is required.\nNo requirement for beneficial-owner disclosure applies.\nNo requirement for documentary confirmation of ownership applies.\nNo requirement for a ban on splitting voting instructions applies.\nFor this vote, retrieval of loaned voting positions is required.\nNo requirement for a mandatory paper-only ballot applies.\n\n\n[Message EL0105D | MT568]\nPlease retain the replacement edition for operational reconciliation. Earlier notification conditions are superseded.\n",
  "predicate": "share_blocking",
  "truth": "NO",
  "prediction": {
    "value": "YES",
    "scores": {
      "YES": 0.6645,
      "NO": 0.2454,
      "UNKNOWN": 0.0901
    },
    "confidence": null,
    "native_score": 0.6645,
    "source": "REGISTERED_LAYA_WHOLE_NOTICE",
    "evidence": [],
    "evidence_status": "UNAVAILABLE: this decision head does not extract quotations"
  },
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
  }
}
```


## VALIDATION / 9 / Laya / 25150120b9a9e92a98ab8b33fb003cab98a2ec6b4230ec908fda5c15d2bbc7d7

```json
{
  "candidate": "Laya",
  "id": "25150120b9a9e92a98ab8b33fb003cab98a2ec6b4230ec908fda5c15d2bbc7d7",
  "text": "[Message EL0105C | MT564]\nIssuer secretariat memorandum concerning arrangements for the forthcoming extraordinary assembly.\nThe current agenda is open for shareholder voting instructions.\nNo requirement for voting-related immobilisation applies.\nNo requirement for an obligatory power-of-attorney document applies.\nFor this vote, a required voter registration form is required.\nNo requirement for beneficial-owner disclosure applies.\nNo requirement for documentary confirmation of ownership applies.\nNo requirement for a ban on splitting voting instructions applies.\nFor this vote, retrieval of loaned voting positions is required.\nNo requirement for a mandatory paper-only ballot applies.\n\n\n[Message EL0105D | MT568]\nPlease retain the replacement edition for operational reconciliation. Earlier notification conditions are superseded.\n",
  "predicate": "registration_required",
  "truth": "YES",
  "prediction": {
    "value": "NO",
    "scores": {
      "YES": 0.1431,
      "NO": 0.7753,
      "UNKNOWN": 0.0816
    },
    "confidence": null,
    "native_score": 0.7753,
    "source": "REGISTERED_LAYA_WHOLE_NOTICE",
    "evidence": [],
    "evidence_status": "UNAVAILABLE: this decision head does not extract quotations"
  },
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
  }
}
```


## VALIDATION / 10 / Laya / 25150120b9a9e92a98ab8b33fb003cab98a2ec6b4230ec908fda5c15d2bbc7d7

```json
{
  "candidate": "Laya",
  "id": "25150120b9a9e92a98ab8b33fb003cab98a2ec6b4230ec908fda5c15d2bbc7d7",
  "text": "[Message EL0105C | MT564]\nIssuer secretariat memorandum concerning arrangements for the forthcoming extraordinary assembly.\nThe current agenda is open for shareholder voting instructions.\nNo requirement for voting-related immobilisation applies.\nNo requirement for an obligatory power-of-attorney document applies.\nFor this vote, a required voter registration form is required.\nNo requirement for beneficial-owner disclosure applies.\nNo requirement for documentary confirmation of ownership applies.\nNo requirement for a ban on splitting voting instructions applies.\nFor this vote, retrieval of loaned voting positions is required.\nNo requirement for a mandatory paper-only ballot applies.\n\n\n[Message EL0105D | MT568]\nPlease retain the replacement edition for operational reconciliation. Earlier notification conditions are superseded.\n",
  "predicate": "securities_lending_recall_required",
  "truth": "YES",
  "prediction": {
    "value": "NO",
    "scores": {
      "YES": 0.2256,
      "NO": 0.6878,
      "UNKNOWN": 0.0866
    },
    "confidence": null,
    "native_score": 0.6878,
    "source": "REGISTERED_LAYA_WHOLE_NOTICE",
    "evidence": [],
    "evidence_status": "UNAVAILABLE: this decision head does not extract quotations"
  },
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
  }
}
```


## VALIDATION / 11 / Laya / 2414be60f4dff3cc46dcf385c748749f7c7c3dc05ef8f904052ec9797bdc2f19

```json
{
  "candidate": "Laya",
  "id": "2414be60f4dff3cc46dcf385c748749f7c7c3dc05ef8f904052ec9797bdc2f19",
  "text": "[Message EL0104C | MT564]\nIssuer secretariat memorandum concerning arrangements for the forthcoming extraordinary assembly.\nThe current agenda is open for shareholder voting instructions.\nNo requirement for voting-related immobilisation applies.\nNo requirement for an obligatory power-of-attorney document applies.\nNo requirement for a required voter registration form applies.\nFor this vote, beneficial-owner disclosure is required.\nNo requirement for documentary confirmation of ownership applies.\nNo requirement for a ban on splitting voting instructions applies.\nNo requirement for retrieval of loaned voting positions applies.\nFor this vote, a mandatory paper-only ballot is required.\n\n\n[Message EL0104D | MT568]\nPlease retain the replacement edition for operational reconciliation. Earlier notification conditions are superseded.\n",
  "predicate": "share_blocking",
  "truth": "NO",
  "prediction": {
    "value": "YES",
    "scores": {
      "YES": 0.7381,
      "NO": 0.2015,
      "UNKNOWN": 0.0604
    },
    "confidence": null,
    "native_score": 0.7381,
    "source": "REGISTERED_LAYA_WHOLE_NOTICE",
    "evidence": [],
    "evidence_status": "UNAVAILABLE: this decision head does not extract quotations"
  },
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
  }
}
```


## VALIDATION / 12 / Laya / 2414be60f4dff3cc46dcf385c748749f7c7c3dc05ef8f904052ec9797bdc2f19

```json
{
  "candidate": "Laya",
  "id": "2414be60f4dff3cc46dcf385c748749f7c7c3dc05ef8f904052ec9797bdc2f19",
  "text": "[Message EL0104C | MT564]\nIssuer secretariat memorandum concerning arrangements for the forthcoming extraordinary assembly.\nThe current agenda is open for shareholder voting instructions.\nNo requirement for voting-related immobilisation applies.\nNo requirement for an obligatory power-of-attorney document applies.\nNo requirement for a required voter registration form applies.\nFor this vote, beneficial-owner disclosure is required.\nNo requirement for documentary confirmation of ownership applies.\nNo requirement for a ban on splitting voting instructions applies.\nNo requirement for retrieval of loaned voting positions applies.\nFor this vote, a mandatory paper-only ballot is required.\n\n\n[Message EL0104D | MT568]\nPlease retain the replacement edition for operational reconciliation. Earlier notification conditions are superseded.\n",
  "predicate": "beneficial_owner_disclosure_required",
  "truth": "YES",
  "prediction": {
    "value": "NO",
    "scores": {
      "YES": 0.0293,
      "NO": 0.9074,
      "UNKNOWN": 0.0633
    },
    "confidence": null,
    "native_score": 0.9074,
    "source": "REGISTERED_LAYA_WHOLE_NOTICE",
    "evidence": [],
    "evidence_status": "UNAVAILABLE: this decision head does not extract quotations"
  },
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
  }
}
```


## VALIDATION / 13 / Laya / 2414be60f4dff3cc46dcf385c748749f7c7c3dc05ef8f904052ec9797bdc2f19

```json
{
  "candidate": "Laya",
  "id": "2414be60f4dff3cc46dcf385c748749f7c7c3dc05ef8f904052ec9797bdc2f19",
  "text": "[Message EL0104C | MT564]\nIssuer secretariat memorandum concerning arrangements for the forthcoming extraordinary assembly.\nThe current agenda is open for shareholder voting instructions.\nNo requirement for voting-related immobilisation applies.\nNo requirement for an obligatory power-of-attorney document applies.\nNo requirement for a required voter registration form applies.\nFor this vote, beneficial-owner disclosure is required.\nNo requirement for documentary confirmation of ownership applies.\nNo requirement for a ban on splitting voting instructions applies.\nNo requirement for retrieval of loaned voting positions applies.\nFor this vote, a mandatory paper-only ballot is required.\n\n\n[Message EL0104D | MT568]\nPlease retain the replacement edition for operational reconciliation. Earlier notification conditions are superseded.\n",
  "predicate": "split_voting_restricted",
  "truth": "NO",
  "prediction": {
    "value": "YES",
    "scores": {
      "YES": 0.4837,
      "NO": 0.4681,
      "UNKNOWN": 0.0483
    },
    "confidence": null,
    "native_score": 0.4837,
    "source": "REGISTERED_LAYA_WHOLE_NOTICE",
    "evidence": [],
    "evidence_status": "UNAVAILABLE: this decision head does not extract quotations"
  },
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
  }
}
```


## VALIDATION / 14 / Laya / 2414be60f4dff3cc46dcf385c748749f7c7c3dc05ef8f904052ec9797bdc2f19

```json
{
  "candidate": "Laya",
  "id": "2414be60f4dff3cc46dcf385c748749f7c7c3dc05ef8f904052ec9797bdc2f19",
  "text": "[Message EL0104C | MT564]\nIssuer secretariat memorandum concerning arrangements for the forthcoming extraordinary assembly.\nThe current agenda is open for shareholder voting instructions.\nNo requirement for voting-related immobilisation applies.\nNo requirement for an obligatory power-of-attorney document applies.\nNo requirement for a required voter registration form applies.\nFor this vote, beneficial-owner disclosure is required.\nNo requirement for documentary confirmation of ownership applies.\nNo requirement for a ban on splitting voting instructions applies.\nNo requirement for retrieval of loaned voting positions applies.\nFor this vote, a mandatory paper-only ballot is required.\n\n\n[Message EL0104D | MT568]\nPlease retain the replacement edition for operational reconciliation. Earlier notification conditions are superseded.\n",
  "predicate": "other_voting_restriction",
  "truth": "YES",
  "prediction": {
    "value": "NO",
    "scores": {
      "YES": 0.2799,
      "NO": 0.6295,
      "UNKNOWN": 0.0907
    },
    "confidence": null,
    "native_score": 0.6295,
    "source": "REGISTERED_LAYA_WHOLE_NOTICE",
    "evidence": [],
    "evidence_status": "UNAVAILABLE: this decision head does not extract quotations"
  },
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
  }
}
```


## VALIDATION / 15 / Qwen / 255328bb369bd44fa7cb0a788d797be6085e4bdab88a810f35f8b14469f269d2

```json
{
  "candidate": "Qwen",
  "id": "255328bb369bd44fa7cb0a788d797be6085e4bdab88a810f35f8b14469f269d2",
  "text": "[Message EL0107C | MT564]\nIssuer secretariat memorandum concerning arrangements for the forthcoming extraordinary assembly.\nParticipation may become possible, but the agent has not established whether this holder can vote.\nFor this vote, voting-related immobilisation is required.\nThe receiving agent has not resolved whether an obligatory power-of-attorney document is required for this vote.\nNo requirement for a required voter registration form applies.\nNo requirement for beneficial-owner disclosure applies.\nFor this vote, documentary confirmation of ownership is required.\nNo requirement for a ban on splitting voting instructions applies.\nNo requirement for retrieval of loaned voting positions applies.\nNo requirement for a mandatory paper-only ballot applies.\n\n\n[Message EL0107D | MT568]\nPlease retain the replacement edition for operational reconciliation. Earlier notification conditions are superseded.\n",
  "predicate": "share_blocking",
  "truth": "YES",
  "prediction": {
    "value": "UNKNOWN",
    "source": "REGISTERED_LOCAL_LLM",
    "confidence": null,
    "scores": {},
    "evidence": []
  },
  "decision": {
    "classification": "UNCERTAIN_MANUAL_REVIEW",
    "rule": "R1 unresolved conflicts",
    "rule_version": "semantic-decision-2",
    "manual_review_required": true,
    "automation_enabled": false,
    "review_reasons": [
      "LLM_OUTPUT_SCHEMA_FAILURE",
      "Synthetic-only evaluation; customer quality gate not met"
    ]
  }
}
```


## VALIDATION / 16 / Qwen / 255328bb369bd44fa7cb0a788d797be6085e4bdab88a810f35f8b14469f269d2

```json
{
  "candidate": "Qwen",
  "id": "255328bb369bd44fa7cb0a788d797be6085e4bdab88a810f35f8b14469f269d2",
  "text": "[Message EL0107C | MT564]\nIssuer secretariat memorandum concerning arrangements for the forthcoming extraordinary assembly.\nParticipation may become possible, but the agent has not established whether this holder can vote.\nFor this vote, voting-related immobilisation is required.\nThe receiving agent has not resolved whether an obligatory power-of-attorney document is required for this vote.\nNo requirement for a required voter registration form applies.\nNo requirement for beneficial-owner disclosure applies.\nFor this vote, documentary confirmation of ownership is required.\nNo requirement for a ban on splitting voting instructions applies.\nNo requirement for retrieval of loaned voting positions applies.\nNo requirement for a mandatory paper-only ballot applies.\n\n\n[Message EL0107D | MT568]\nPlease retain the replacement edition for operational reconciliation. Earlier notification conditions are superseded.\n",
  "predicate": "registration_required",
  "truth": "NO",
  "prediction": {
    "value": "UNKNOWN",
    "source": "REGISTERED_LOCAL_LLM",
    "confidence": null,
    "scores": {},
    "evidence": []
  },
  "decision": {
    "classification": "UNCERTAIN_MANUAL_REVIEW",
    "rule": "R1 unresolved conflicts",
    "rule_version": "semantic-decision-2",
    "manual_review_required": true,
    "automation_enabled": false,
    "review_reasons": [
      "LLM_OUTPUT_SCHEMA_FAILURE",
      "Synthetic-only evaluation; customer quality gate not met"
    ]
  }
}
```


## VALIDATION / 17 / Qwen / 255328bb369bd44fa7cb0a788d797be6085e4bdab88a810f35f8b14469f269d2

```json
{
  "candidate": "Qwen",
  "id": "255328bb369bd44fa7cb0a788d797be6085e4bdab88a810f35f8b14469f269d2",
  "text": "[Message EL0107C | MT564]\nIssuer secretariat memorandum concerning arrangements for the forthcoming extraordinary assembly.\nParticipation may become possible, but the agent has not established whether this holder can vote.\nFor this vote, voting-related immobilisation is required.\nThe receiving agent has not resolved whether an obligatory power-of-attorney document is required for this vote.\nNo requirement for a required voter registration form applies.\nNo requirement for beneficial-owner disclosure applies.\nFor this vote, documentary confirmation of ownership is required.\nNo requirement for a ban on splitting voting instructions applies.\nNo requirement for retrieval of loaned voting positions applies.\nNo requirement for a mandatory paper-only ballot applies.\n\n\n[Message EL0107D | MT568]\nPlease retain the replacement edition for operational reconciliation. Earlier notification conditions are superseded.\n",
  "predicate": "beneficial_owner_disclosure_required",
  "truth": "NO",
  "prediction": {
    "value": "UNKNOWN",
    "source": "REGISTERED_LOCAL_LLM",
    "confidence": null,
    "scores": {},
    "evidence": []
  },
  "decision": {
    "classification": "UNCERTAIN_MANUAL_REVIEW",
    "rule": "R1 unresolved conflicts",
    "rule_version": "semantic-decision-2",
    "manual_review_required": true,
    "automation_enabled": false,
    "review_reasons": [
      "LLM_OUTPUT_SCHEMA_FAILURE",
      "Synthetic-only evaluation; customer quality gate not met"
    ]
  }
}
```


## VALIDATION / 18 / Qwen / 255328bb369bd44fa7cb0a788d797be6085e4bdab88a810f35f8b14469f269d2

```json
{
  "candidate": "Qwen",
  "id": "255328bb369bd44fa7cb0a788d797be6085e4bdab88a810f35f8b14469f269d2",
  "text": "[Message EL0107C | MT564]\nIssuer secretariat memorandum concerning arrangements for the forthcoming extraordinary assembly.\nParticipation may become possible, but the agent has not established whether this holder can vote.\nFor this vote, voting-related immobilisation is required.\nThe receiving agent has not resolved whether an obligatory power-of-attorney document is required for this vote.\nNo requirement for a required voter registration form applies.\nNo requirement for beneficial-owner disclosure applies.\nFor this vote, documentary confirmation of ownership is required.\nNo requirement for a ban on splitting voting instructions applies.\nNo requirement for retrieval of loaned voting positions applies.\nNo requirement for a mandatory paper-only ballot applies.\n\n\n[Message EL0107D | MT568]\nPlease retain the replacement edition for operational reconciliation. Earlier notification conditions are superseded.\n",
  "predicate": "holding_confirmation_required",
  "truth": "YES",
  "prediction": {
    "value": "UNKNOWN",
    "source": "REGISTERED_LOCAL_LLM",
    "confidence": null,
    "scores": {},
    "evidence": []
  },
  "decision": {
    "classification": "UNCERTAIN_MANUAL_REVIEW",
    "rule": "R1 unresolved conflicts",
    "rule_version": "semantic-decision-2",
    "manual_review_required": true,
    "automation_enabled": false,
    "review_reasons": [
      "LLM_OUTPUT_SCHEMA_FAILURE",
      "Synthetic-only evaluation; customer quality gate not met"
    ]
  }
}
```


## VALIDATION / 19 / Qwen / 255328bb369bd44fa7cb0a788d797be6085e4bdab88a810f35f8b14469f269d2

```json
{
  "candidate": "Qwen",
  "id": "255328bb369bd44fa7cb0a788d797be6085e4bdab88a810f35f8b14469f269d2",
  "text": "[Message EL0107C | MT564]\nIssuer secretariat memorandum concerning arrangements for the forthcoming extraordinary assembly.\nParticipation may become possible, but the agent has not established whether this holder can vote.\nFor this vote, voting-related immobilisation is required.\nThe receiving agent has not resolved whether an obligatory power-of-attorney document is required for this vote.\nNo requirement for a required voter registration form applies.\nNo requirement for beneficial-owner disclosure applies.\nFor this vote, documentary confirmation of ownership is required.\nNo requirement for a ban on splitting voting instructions applies.\nNo requirement for retrieval of loaned voting positions applies.\nNo requirement for a mandatory paper-only ballot applies.\n\n\n[Message EL0107D | MT568]\nPlease retain the replacement edition for operational reconciliation. Earlier notification conditions are superseded.\n",
  "predicate": "split_voting_restricted",
  "truth": "NO",
  "prediction": {
    "value": "UNKNOWN",
    "source": "REGISTERED_LOCAL_LLM",
    "confidence": null,
    "scores": {},
    "evidence": []
  },
  "decision": {
    "classification": "UNCERTAIN_MANUAL_REVIEW",
    "rule": "R1 unresolved conflicts",
    "rule_version": "semantic-decision-2",
    "manual_review_required": true,
    "automation_enabled": false,
    "review_reasons": [
      "LLM_OUTPUT_SCHEMA_FAILURE",
      "Synthetic-only evaluation; customer quality gate not met"
    ]
  }
}
```


## VALIDATION / 20 / Qwen / 255328bb369bd44fa7cb0a788d797be6085e4bdab88a810f35f8b14469f269d2

```json
{
  "candidate": "Qwen",
  "id": "255328bb369bd44fa7cb0a788d797be6085e4bdab88a810f35f8b14469f269d2",
  "text": "[Message EL0107C | MT564]\nIssuer secretariat memorandum concerning arrangements for the forthcoming extraordinary assembly.\nParticipation may become possible, but the agent has not established whether this holder can vote.\nFor this vote, voting-related immobilisation is required.\nThe receiving agent has not resolved whether an obligatory power-of-attorney document is required for this vote.\nNo requirement for a required voter registration form applies.\nNo requirement for beneficial-owner disclosure applies.\nFor this vote, documentary confirmation of ownership is required.\nNo requirement for a ban on splitting voting instructions applies.\nNo requirement for retrieval of loaned voting positions applies.\nNo requirement for a mandatory paper-only ballot applies.\n\n\n[Message EL0107D | MT568]\nPlease retain the replacement edition for operational reconciliation. Earlier notification conditions are superseded.\n",
  "predicate": "securities_lending_recall_required",
  "truth": "NO",
  "prediction": {
    "value": "UNKNOWN",
    "source": "REGISTERED_LOCAL_LLM",
    "confidence": null,
    "scores": {},
    "evidence": []
  },
  "decision": {
    "classification": "UNCERTAIN_MANUAL_REVIEW",
    "rule": "R1 unresolved conflicts",
    "rule_version": "semantic-decision-2",
    "manual_review_required": true,
    "automation_enabled": false,
    "review_reasons": [
      "LLM_OUTPUT_SCHEMA_FAILURE",
      "Synthetic-only evaluation; customer quality gate not met"
    ]
  }
}
```


## VALIDATION / 21 / Qwen / 255328bb369bd44fa7cb0a788d797be6085e4bdab88a810f35f8b14469f269d2

```json
{
  "candidate": "Qwen",
  "id": "255328bb369bd44fa7cb0a788d797be6085e4bdab88a810f35f8b14469f269d2",
  "text": "[Message EL0107C | MT564]\nIssuer secretariat memorandum concerning arrangements for the forthcoming extraordinary assembly.\nParticipation may become possible, but the agent has not established whether this holder can vote.\nFor this vote, voting-related immobilisation is required.\nThe receiving agent has not resolved whether an obligatory power-of-attorney document is required for this vote.\nNo requirement for a required voter registration form applies.\nNo requirement for beneficial-owner disclosure applies.\nFor this vote, documentary confirmation of ownership is required.\nNo requirement for a ban on splitting voting instructions applies.\nNo requirement for retrieval of loaned voting positions applies.\nNo requirement for a mandatory paper-only ballot applies.\n\n\n[Message EL0107D | MT568]\nPlease retain the replacement edition for operational reconciliation. Earlier notification conditions are superseded.\n",
  "predicate": "other_voting_restriction",
  "truth": "NO",
  "prediction": {
    "value": "UNKNOWN",
    "source": "REGISTERED_LOCAL_LLM",
    "confidence": null,
    "scores": {},
    "evidence": []
  },
  "decision": {
    "classification": "UNCERTAIN_MANUAL_REVIEW",
    "rule": "R1 unresolved conflicts",
    "rule_version": "semantic-decision-2",
    "manual_review_required": true,
    "automation_enabled": false,
    "review_reasons": [
      "LLM_OUTPUT_SCHEMA_FAILURE",
      "Synthetic-only evaluation; customer quality gate not met"
    ]
  }
}
```


## CALIBRATION / 1 / Laya / 02ddd88c0f4d0a7d69379ac818daa40b8ec9ff52de5bd57714e6db65ebd236b8

```json
{
  "candidate": "Laya",
  "id": "02ddd88c0f4d0a7d69379ac818daa40b8ec9ff52de5bd57714e6db65ebd236b8",
  "text": "[Message EL1304C | MT564]\nCorporate actions desk message. Agenda participation and account documentation are described in the current extract.\nThe current agenda is open for shareholder voting instructions.\nThis route imposes no obligation concerning voting-related immobilisation.\nThis route imposes no obligation concerning an obligatory power-of-attorney document.\nThis route imposes no obligation concerning a required voter registration form.\nParticipation in this vote requires beneficial-owner disclosure.\nThis route imposes no obligation concerning documentary confirmation of ownership.\nThis route imposes no obligation concerning a ban on splitting voting instructions.\nThis route imposes no obligation concerning retrieval of loaned voting positions.\nParticipation in this vote requires a mandatory paper-only ballot.\n\n\n[Message EL1304D | MT568]\nPlease retain the replacement edition for operational reconciliation. Earlier notification conditions are superseded.\n",
  "predicate": "share_blocking",
  "truth": "NO",
  "prediction": {
    "value": "YES",
    "scores": {
      "YES": 0.606,
      "NO": 0.3594,
      "UNKNOWN": 0.0346
    },
    "confidence": null,
    "native_score": 0.606,
    "source": "REGISTERED_LAYA_WHOLE_NOTICE",
    "evidence": [],
    "evidence_status": "UNAVAILABLE: this decision head does not extract quotations"
  },
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
  }
}
```


## CALIBRATION / 2 / Laya / 02ddd88c0f4d0a7d69379ac818daa40b8ec9ff52de5bd57714e6db65ebd236b8

```json
{
  "candidate": "Laya",
  "id": "02ddd88c0f4d0a7d69379ac818daa40b8ec9ff52de5bd57714e6db65ebd236b8",
  "text": "[Message EL1304C | MT564]\nCorporate actions desk message. Agenda participation and account documentation are described in the current extract.\nThe current agenda is open for shareholder voting instructions.\nThis route imposes no obligation concerning voting-related immobilisation.\nThis route imposes no obligation concerning an obligatory power-of-attorney document.\nThis route imposes no obligation concerning a required voter registration form.\nParticipation in this vote requires beneficial-owner disclosure.\nThis route imposes no obligation concerning documentary confirmation of ownership.\nThis route imposes no obligation concerning a ban on splitting voting instructions.\nThis route imposes no obligation concerning retrieval of loaned voting positions.\nParticipation in this vote requires a mandatory paper-only ballot.\n\n\n[Message EL1304D | MT568]\nPlease retain the replacement edition for operational reconciliation. Earlier notification conditions are superseded.\n",
  "predicate": "beneficial_owner_disclosure_required",
  "truth": "YES",
  "prediction": {
    "value": "NO",
    "scores": {
      "YES": 0.0913,
      "NO": 0.8361,
      "UNKNOWN": 0.0726
    },
    "confidence": null,
    "native_score": 0.8361,
    "source": "REGISTERED_LAYA_WHOLE_NOTICE",
    "evidence": [],
    "evidence_status": "UNAVAILABLE: this decision head does not extract quotations"
  },
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
  }
}
```


## CALIBRATION / 3 / Laya / 02ddd88c0f4d0a7d69379ac818daa40b8ec9ff52de5bd57714e6db65ebd236b8

```json
{
  "candidate": "Laya",
  "id": "02ddd88c0f4d0a7d69379ac818daa40b8ec9ff52de5bd57714e6db65ebd236b8",
  "text": "[Message EL1304C | MT564]\nCorporate actions desk message. Agenda participation and account documentation are described in the current extract.\nThe current agenda is open for shareholder voting instructions.\nThis route imposes no obligation concerning voting-related immobilisation.\nThis route imposes no obligation concerning an obligatory power-of-attorney document.\nThis route imposes no obligation concerning a required voter registration form.\nParticipation in this vote requires beneficial-owner disclosure.\nThis route imposes no obligation concerning documentary confirmation of ownership.\nThis route imposes no obligation concerning a ban on splitting voting instructions.\nThis route imposes no obligation concerning retrieval of loaned voting positions.\nParticipation in this vote requires a mandatory paper-only ballot.\n\n\n[Message EL1304D | MT568]\nPlease retain the replacement edition for operational reconciliation. Earlier notification conditions are superseded.\n",
  "predicate": "split_voting_restricted",
  "truth": "NO",
  "prediction": {
    "value": "YES",
    "scores": {
      "YES": 0.5457,
      "NO": 0.3685,
      "UNKNOWN": 0.0858
    },
    "confidence": null,
    "native_score": 0.5457,
    "source": "REGISTERED_LAYA_WHOLE_NOTICE",
    "evidence": [],
    "evidence_status": "UNAVAILABLE: this decision head does not extract quotations"
  },
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
  }
}
```


## CALIBRATION / 4 / Laya / 02ddd88c0f4d0a7d69379ac818daa40b8ec9ff52de5bd57714e6db65ebd236b8

```json
{
  "candidate": "Laya",
  "id": "02ddd88c0f4d0a7d69379ac818daa40b8ec9ff52de5bd57714e6db65ebd236b8",
  "text": "[Message EL1304C | MT564]\nCorporate actions desk message. Agenda participation and account documentation are described in the current extract.\nThe current agenda is open for shareholder voting instructions.\nThis route imposes no obligation concerning voting-related immobilisation.\nThis route imposes no obligation concerning an obligatory power-of-attorney document.\nThis route imposes no obligation concerning a required voter registration form.\nParticipation in this vote requires beneficial-owner disclosure.\nThis route imposes no obligation concerning documentary confirmation of ownership.\nThis route imposes no obligation concerning a ban on splitting voting instructions.\nThis route imposes no obligation concerning retrieval of loaned voting positions.\nParticipation in this vote requires a mandatory paper-only ballot.\n\n\n[Message EL1304D | MT568]\nPlease retain the replacement edition for operational reconciliation. Earlier notification conditions are superseded.\n",
  "predicate": "other_voting_restriction",
  "truth": "YES",
  "prediction": {
    "value": "NO",
    "scores": {
      "YES": 0.2545,
      "NO": 0.6861,
      "UNKNOWN": 0.0594
    },
    "confidence": null,
    "native_score": 0.6861,
    "source": "REGISTERED_LAYA_WHOLE_NOTICE",
    "evidence": [],
    "evidence_status": "UNAVAILABLE: this decision head does not extract quotations"
  },
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
  }
}
```


## CALIBRATION / 5 / Laya / 2e47a544fd4c1d0247a92fbb6f242fbb828171a83540c94f4a36c5d3fa40ce03

```json
{
  "candidate": "Laya",
  "id": "2e47a544fd4c1d0247a92fbb6f242fbb828171a83540c94f4a36c5d3fa40ce03",
  "text": "[Message EL1301C | MT564]\nCorporate actions desk message. Agenda participation and account documentation are described in the current extract.\nThe current agenda is open for shareholder voting instructions.\nThis route imposes no obligation concerning voting-related immobilisation.\nThis route imposes no obligation concerning an obligatory power-of-attorney document.\nParticipation in this vote requires a required voter registration form.\nThis route imposes no obligation concerning beneficial-owner disclosure.\nThis route imposes no obligation concerning documentary confirmation of ownership.\nThis route imposes no obligation concerning a ban on splitting voting instructions.\nParticipation in this vote requires retrieval of loaned voting positions.\nThis route imposes no obligation concerning a mandatory paper-only ballot.\n\n\n[Message EL1301D | MT568]\nPlease retain the replacement edition for operational reconciliation. Earlier notification conditions are superseded.\n",
  "predicate": "share_blocking",
  "truth": "NO",
  "prediction": {
    "value": "YES",
    "scores": {
      "YES": 0.6098,
      "NO": 0.3498,
      "UNKNOWN": 0.0404
    },
    "confidence": null,
    "native_score": 0.6098,
    "source": "REGISTERED_LAYA_WHOLE_NOTICE",
    "evidence": [],
    "evidence_status": "UNAVAILABLE: this decision head does not extract quotations"
  },
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
  }
}
```


## CALIBRATION / 6 / Laya / 2e47a544fd4c1d0247a92fbb6f242fbb828171a83540c94f4a36c5d3fa40ce03

```json
{
  "candidate": "Laya",
  "id": "2e47a544fd4c1d0247a92fbb6f242fbb828171a83540c94f4a36c5d3fa40ce03",
  "text": "[Message EL1301C | MT564]\nCorporate actions desk message. Agenda participation and account documentation are described in the current extract.\nThe current agenda is open for shareholder voting instructions.\nThis route imposes no obligation concerning voting-related immobilisation.\nThis route imposes no obligation concerning an obligatory power-of-attorney document.\nParticipation in this vote requires a required voter registration form.\nThis route imposes no obligation concerning beneficial-owner disclosure.\nThis route imposes no obligation concerning documentary confirmation of ownership.\nThis route imposes no obligation concerning a ban on splitting voting instructions.\nParticipation in this vote requires retrieval of loaned voting positions.\nThis route imposes no obligation concerning a mandatory paper-only ballot.\n\n\n[Message EL1301D | MT568]\nPlease retain the replacement edition for operational reconciliation. Earlier notification conditions are superseded.\n",
  "predicate": "registration_required",
  "truth": "YES",
  "prediction": {
    "value": "NO",
    "scores": {
      "YES": 0.2025,
      "NO": 0.7024,
      "UNKNOWN": 0.0951
    },
    "confidence": null,
    "native_score": 0.7024,
    "source": "REGISTERED_LAYA_WHOLE_NOTICE",
    "evidence": [],
    "evidence_status": "UNAVAILABLE: this decision head does not extract quotations"
  },
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
  }
}
```


## CALIBRATION / 7 / Laya / 2e47a544fd4c1d0247a92fbb6f242fbb828171a83540c94f4a36c5d3fa40ce03

```json
{
  "candidate": "Laya",
  "id": "2e47a544fd4c1d0247a92fbb6f242fbb828171a83540c94f4a36c5d3fa40ce03",
  "text": "[Message EL1301C | MT564]\nCorporate actions desk message. Agenda participation and account documentation are described in the current extract.\nThe current agenda is open for shareholder voting instructions.\nThis route imposes no obligation concerning voting-related immobilisation.\nThis route imposes no obligation concerning an obligatory power-of-attorney document.\nParticipation in this vote requires a required voter registration form.\nThis route imposes no obligation concerning beneficial-owner disclosure.\nThis route imposes no obligation concerning documentary confirmation of ownership.\nThis route imposes no obligation concerning a ban on splitting voting instructions.\nParticipation in this vote requires retrieval of loaned voting positions.\nThis route imposes no obligation concerning a mandatory paper-only ballot.\n\n\n[Message EL1301D | MT568]\nPlease retain the replacement edition for operational reconciliation. Earlier notification conditions are superseded.\n",
  "predicate": "split_voting_restricted",
  "truth": "NO",
  "prediction": {
    "value": "YES",
    "scores": {
      "YES": 0.5394,
      "NO": 0.3537,
      "UNKNOWN": 0.1069
    },
    "confidence": null,
    "native_score": 0.5394,
    "source": "REGISTERED_LAYA_WHOLE_NOTICE",
    "evidence": [],
    "evidence_status": "UNAVAILABLE: this decision head does not extract quotations"
  },
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
  }
}
```


## CALIBRATION / 8 / Laya / 2e47a544fd4c1d0247a92fbb6f242fbb828171a83540c94f4a36c5d3fa40ce03

```json
{
  "candidate": "Laya",
  "id": "2e47a544fd4c1d0247a92fbb6f242fbb828171a83540c94f4a36c5d3fa40ce03",
  "text": "[Message EL1301C | MT564]\nCorporate actions desk message. Agenda participation and account documentation are described in the current extract.\nThe current agenda is open for shareholder voting instructions.\nThis route imposes no obligation concerning voting-related immobilisation.\nThis route imposes no obligation concerning an obligatory power-of-attorney document.\nParticipation in this vote requires a required voter registration form.\nThis route imposes no obligation concerning beneficial-owner disclosure.\nThis route imposes no obligation concerning documentary confirmation of ownership.\nThis route imposes no obligation concerning a ban on splitting voting instructions.\nParticipation in this vote requires retrieval of loaned voting positions.\nThis route imposes no obligation concerning a mandatory paper-only ballot.\n\n\n[Message EL1301D | MT568]\nPlease retain the replacement edition for operational reconciliation. Earlier notification conditions are superseded.\n",
  "predicate": "securities_lending_recall_required",
  "truth": "YES",
  "prediction": {
    "value": "NO",
    "scores": {
      "YES": 0.3176,
      "NO": 0.5924,
      "UNKNOWN": 0.09
    },
    "confidence": null,
    "native_score": 0.5924,
    "source": "REGISTERED_LAYA_WHOLE_NOTICE",
    "evidence": [],
    "evidence_status": "UNAVAILABLE: this decision head does not extract quotations"
  },
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
  }
}
```


## CALIBRATION / 9 / Laya / 41a7ad038250f102befebd7f25ee6b17023c5cf154015dc1ce5f213fab2e6843

```json
{
  "candidate": "Laya",
  "id": "41a7ad038250f102befebd7f25ee6b17023c5cf154015dc1ce5f213fab2e6843",
  "text": "[Message EL0802C | MT564]\nClient account advice regarding the scheme meeting. The receiving agent uses the following participation process.\nShareholders can submit a ballot on the resolutions at this meeting.\nShare blocking is not required under these terms.\nA notarised voting authority is not required under these terms.\nThe current voting route is conditional upon compulsory participant registration.\nDisclosure of the ultimate investor is not required under these terms.\nA holdings certificate is not required under these terms.\nA restriction on dividing the ballot is not required under these terms.\nThe current voting route is conditional upon a mandatory stock-loan recall.\nA prohibition on electronic voting is not required under these terms.\n\n\n[Message EL0802D | MT568]\nPlease retain the replacement edition for operational reconciliation. Earlier notification conditions are superseded.\n",
  "predicate": "share_blocking",
  "truth": "NO",
  "prediction": {
    "value": "YES",
    "scores": {
      "YES": 0.6027,
      "NO": 0.3657,
      "UNKNOWN": 0.0316
    },
    "confidence": null,
    "native_score": 0.6027,
    "source": "REGISTERED_LAYA_WHOLE_NOTICE",
    "evidence": [],
    "evidence_status": "UNAVAILABLE: this decision head does not extract quotations"
  },
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
  }
}
```


## CALIBRATION / 10 / Laya / 41a7ad038250f102befebd7f25ee6b17023c5cf154015dc1ce5f213fab2e6843

```json
{
  "candidate": "Laya",
  "id": "41a7ad038250f102befebd7f25ee6b17023c5cf154015dc1ce5f213fab2e6843",
  "text": "[Message EL0802C | MT564]\nClient account advice regarding the scheme meeting. The receiving agent uses the following participation process.\nShareholders can submit a ballot on the resolutions at this meeting.\nShare blocking is not required under these terms.\nA notarised voting authority is not required under these terms.\nThe current voting route is conditional upon compulsory participant registration.\nDisclosure of the ultimate investor is not required under these terms.\nA holdings certificate is not required under these terms.\nA restriction on dividing the ballot is not required under these terms.\nThe current voting route is conditional upon a mandatory stock-loan recall.\nA prohibition on electronic voting is not required under these terms.\n\n\n[Message EL0802D | MT568]\nPlease retain the replacement edition for operational reconciliation. Earlier notification conditions are superseded.\n",
  "predicate": "registration_required",
  "truth": "YES",
  "prediction": {
    "value": "NO",
    "scores": {
      "YES": 0.1791,
      "NO": 0.7921,
      "UNKNOWN": 0.0288
    },
    "confidence": null,
    "native_score": 0.7921,
    "source": "REGISTERED_LAYA_WHOLE_NOTICE",
    "evidence": [],
    "evidence_status": "UNAVAILABLE: this decision head does not extract quotations"
  },
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
  }
}
```


## CALIBRATION / 11 / Laya / 41a7ad038250f102befebd7f25ee6b17023c5cf154015dc1ce5f213fab2e6843

```json
{
  "candidate": "Laya",
  "id": "41a7ad038250f102befebd7f25ee6b17023c5cf154015dc1ce5f213fab2e6843",
  "text": "[Message EL0802C | MT564]\nClient account advice regarding the scheme meeting. The receiving agent uses the following participation process.\nShareholders can submit a ballot on the resolutions at this meeting.\nShare blocking is not required under these terms.\nA notarised voting authority is not required under these terms.\nThe current voting route is conditional upon compulsory participant registration.\nDisclosure of the ultimate investor is not required under these terms.\nA holdings certificate is not required under these terms.\nA restriction on dividing the ballot is not required under these terms.\nThe current voting route is conditional upon a mandatory stock-loan recall.\nA prohibition on electronic voting is not required under these terms.\n\n\n[Message EL0802D | MT568]\nPlease retain the replacement edition for operational reconciliation. Earlier notification conditions are superseded.\n",
  "predicate": "holding_confirmation_required",
  "truth": "NO",
  "prediction": {
    "value": "YES",
    "scores": {
      "YES": 0.4965,
      "NO": 0.2503,
      "UNKNOWN": 0.2532
    },
    "confidence": null,
    "native_score": 0.4965,
    "source": "REGISTERED_LAYA_WHOLE_NOTICE",
    "evidence": [],
    "evidence_status": "UNAVAILABLE: this decision head does not extract quotations"
  },
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
  }
}
```


## CALIBRATION / 12 / Laya / 41a7ad038250f102befebd7f25ee6b17023c5cf154015dc1ce5f213fab2e6843

```json
{
  "candidate": "Laya",
  "id": "41a7ad038250f102befebd7f25ee6b17023c5cf154015dc1ce5f213fab2e6843",
  "text": "[Message EL0802C | MT564]\nClient account advice regarding the scheme meeting. The receiving agent uses the following participation process.\nShareholders can submit a ballot on the resolutions at this meeting.\nShare blocking is not required under these terms.\nA notarised voting authority is not required under these terms.\nThe current voting route is conditional upon compulsory participant registration.\nDisclosure of the ultimate investor is not required under these terms.\nA holdings certificate is not required under these terms.\nA restriction on dividing the ballot is not required under these terms.\nThe current voting route is conditional upon a mandatory stock-loan recall.\nA prohibition on electronic voting is not required under these terms.\n\n\n[Message EL0802D | MT568]\nPlease retain the replacement edition for operational reconciliation. Earlier notification conditions are superseded.\n",
  "predicate": "securities_lending_recall_required",
  "truth": "YES",
  "prediction": {
    "value": "NO",
    "scores": {
      "YES": 0.2694,
      "NO": 0.6999,
      "UNKNOWN": 0.0307
    },
    "confidence": null,
    "native_score": 0.6999,
    "source": "REGISTERED_LAYA_WHOLE_NOTICE",
    "evidence": [],
    "evidence_status": "UNAVAILABLE: this decision head does not extract quotations"
  },
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
  }
}
```


## CALIBRATION / 13 / Laya / 349455a6aadafbf2092fdaf93307a4603306397cba4c26b6b272972e9cda30d2

```json
{
  "candidate": "Laya",
  "id": "349455a6aadafbf2092fdaf93307a4603306397cba4c26b6b272972e9cda30d2",
  "text": "[Message EL0800C | MT564]\nClient account advice regarding the scheme meeting. The receiving agent uses the following participation process.\nShareholders can submit a ballot on the resolutions at this meeting.\nShare blocking is not required under these terms.\nA notarised voting authority is not required under these terms.\nCompulsory participant registration is not required under these terms.\nDisclosure of the ultimate investor is not required under these terms.\nA holdings certificate is not required under these terms.\nA restriction on dividing the ballot is not required under these terms.\nA mandatory stock-loan recall is not required under these terms.\nA prohibition on electronic voting is not required under these terms.\n\n\n[Message EL0800D | MT568]\nPlease retain the replacement edition for operational reconciliation. Earlier notification conditions are superseded.\n",
  "predicate": "share_blocking",
  "truth": "NO",
  "prediction": {
    "value": "YES",
    "scores": {
      "YES": 0.6475,
      "NO": 0.3252,
      "UNKNOWN": 0.0274
    },
    "confidence": null,
    "native_score": 0.6475,
    "source": "REGISTERED_LAYA_WHOLE_NOTICE",
    "evidence": [],
    "evidence_status": "UNAVAILABLE: this decision head does not extract quotations"
  },
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
  }
}
```


## CALIBRATION / 14 / Laya / 349455a6aadafbf2092fdaf93307a4603306397cba4c26b6b272972e9cda30d2

```json
{
  "candidate": "Laya",
  "id": "349455a6aadafbf2092fdaf93307a4603306397cba4c26b6b272972e9cda30d2",
  "text": "[Message EL0800C | MT564]\nClient account advice regarding the scheme meeting. The receiving agent uses the following participation process.\nShareholders can submit a ballot on the resolutions at this meeting.\nShare blocking is not required under these terms.\nA notarised voting authority is not required under these terms.\nCompulsory participant registration is not required under these terms.\nDisclosure of the ultimate investor is not required under these terms.\nA holdings certificate is not required under these terms.\nA restriction on dividing the ballot is not required under these terms.\nA mandatory stock-loan recall is not required under these terms.\nA prohibition on electronic voting is not required under these terms.\n\n\n[Message EL0800D | MT568]\nPlease retain the replacement edition for operational reconciliation. Earlier notification conditions are superseded.\n",
  "predicate": "holding_confirmation_required",
  "truth": "NO",
  "prediction": {
    "value": "YES",
    "scores": {
      "YES": 0.5338,
      "NO": 0.2586,
      "UNKNOWN": 0.2076
    },
    "confidence": null,
    "native_score": 0.5338,
    "source": "REGISTERED_LAYA_WHOLE_NOTICE",
    "evidence": [],
    "evidence_status": "UNAVAILABLE: this decision head does not extract quotations"
  },
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
  }
}
```


## FROZEN_TEST / 1 / Laya / 296e71ad2ee773d2b0377f9ff94f110218a6b3f363ab6db3ea400957926467a2

```json
{
  "candidate": "Laya",
  "id": "296e71ad2ee773d2b0377f9ff94f110218a6b3f363ab6db3ea400957926467a2",
  "text": "[Message EL1905C | MT564]\nCompany meeting helpdesk correspondence. This message records the final instructions delivered to nominees.\nA live voting opportunity exists for owners responding to this assembly.\nFor this vote, blocking of instructed shares is required.\nNo requirement for a mandatory power of attorney applies.\nNo requirement for advance enrolment for voting applies.\nNo requirement for a beneficial-holder identity declaration applies.\nFor this vote, proof of the held position is required.\nNo requirement for a prohibition on split voting applies.\nNo requirement for return of shares on loan before voting applies.\nNo requirement for a compulsory original wet-signature ballot applies.\n\n\n[Message EL1905D | MT568]\nPlease retain the replacement edition for operational reconciliation. Earlier notification conditions are superseded.\n",
  "predicate": "split_voting_restricted",
  "truth": "NO",
  "prediction": {
    "value": "YES",
    "scores": {
      "YES": 0.4753,
      "NO": 0.4668,
      "UNKNOWN": 0.0579
    },
    "confidence": null,
    "native_score": 0.4753,
    "source": "REGISTERED_LAYA_WHOLE_NOTICE",
    "evidence": [],
    "evidence_status": "UNAVAILABLE: this decision head does not extract quotations"
  },
  "decision": {
    "classification": "VOTABLE_WITH_RESTRICTION",
    "rule": "R5 one or more voting restrictions",
    "rule_version": "semantic-decision-2",
    "manual_review_required": true,
    "automation_enabled": false,
    "review_reasons": [
      "Synthetic-only evaluation; customer quality gate not met"
    ]
  }
}
```


## FROZEN_TEST / 2 / Laya / 296e71ad2ee773d2b0377f9ff94f110218a6b3f363ab6db3ea400957926467a2

```json
{
  "candidate": "Laya",
  "id": "296e71ad2ee773d2b0377f9ff94f110218a6b3f363ab6db3ea400957926467a2",
  "text": "[Message EL1905C | MT564]\nCompany meeting helpdesk correspondence. This message records the final instructions delivered to nominees.\nA live voting opportunity exists for owners responding to this assembly.\nFor this vote, blocking of instructed shares is required.\nNo requirement for a mandatory power of attorney applies.\nNo requirement for advance enrolment for voting applies.\nNo requirement for a beneficial-holder identity declaration applies.\nFor this vote, proof of the held position is required.\nNo requirement for a prohibition on split voting applies.\nNo requirement for return of shares on loan before voting applies.\nNo requirement for a compulsory original wet-signature ballot applies.\n\n\n[Message EL1905D | MT568]\nPlease retain the replacement edition for operational reconciliation. Earlier notification conditions are superseded.\n",
  "predicate": "securities_lending_recall_required",
  "truth": "NO",
  "prediction": {
    "value": "YES",
    "scores": {
      "YES": 0.4525,
      "NO": 0.452,
      "UNKNOWN": 0.0955
    },
    "confidence": null,
    "native_score": 0.4525,
    "source": "REGISTERED_LAYA_WHOLE_NOTICE",
    "evidence": [],
    "evidence_status": "UNAVAILABLE: this decision head does not extract quotations"
  },
  "decision": {
    "classification": "VOTABLE_WITH_RESTRICTION",
    "rule": "R5 one or more voting restrictions",
    "rule_version": "semantic-decision-2",
    "manual_review_required": true,
    "automation_enabled": false,
    "review_reasons": [
      "Synthetic-only evaluation; customer quality gate not met"
    ]
  }
}
```


## FROZEN_TEST / 3 / Laya / 296e71ad2ee773d2b0377f9ff94f110218a6b3f363ab6db3ea400957926467a2

```json
{
  "candidate": "Laya",
  "id": "296e71ad2ee773d2b0377f9ff94f110218a6b3f363ab6db3ea400957926467a2",
  "text": "[Message EL1905C | MT564]\nCompany meeting helpdesk correspondence. This message records the final instructions delivered to nominees.\nA live voting opportunity exists for owners responding to this assembly.\nFor this vote, blocking of instructed shares is required.\nNo requirement for a mandatory power of attorney applies.\nNo requirement for advance enrolment for voting applies.\nNo requirement for a beneficial-holder identity declaration applies.\nFor this vote, proof of the held position is required.\nNo requirement for a prohibition on split voting applies.\nNo requirement for return of shares on loan before voting applies.\nNo requirement for a compulsory original wet-signature ballot applies.\n\n\n[Message EL1905D | MT568]\nPlease retain the replacement edition for operational reconciliation. Earlier notification conditions are superseded.\n",
  "predicate": "other_voting_restriction",
  "truth": "NO",
  "prediction": {
    "value": "YES",
    "scores": {
      "YES": 0.5137,
      "NO": 0.4134,
      "UNKNOWN": 0.0729
    },
    "confidence": null,
    "native_score": 0.5137,
    "source": "REGISTERED_LAYA_WHOLE_NOTICE",
    "evidence": [],
    "evidence_status": "UNAVAILABLE: this decision head does not extract quotations"
  },
  "decision": {
    "classification": "VOTABLE_WITH_RESTRICTION",
    "rule": "R5 one or more voting restrictions",
    "rule_version": "semantic-decision-2",
    "manual_review_required": true,
    "automation_enabled": false,
    "review_reasons": [
      "Synthetic-only evaluation; customer quality gate not met"
    ]
  }
}
```


## FROZEN_TEST / 4 / Laya / 019842df38bde1866068a249a668dec26d8242dcee828d768d468663a727e34c

```json
{
  "candidate": "Laya",
  "id": "019842df38bde1866068a249a668dec26d8242dcee828d768d468663a727e34c",
  "text": "[Message EL1900C | MT564]\nCompany meeting helpdesk correspondence. This message records the final instructions delivered to nominees.\nA live voting opportunity exists for owners responding to this assembly.\nNo requirement for blocking of instructed shares applies.\nNo requirement for a mandatory power of attorney applies.\nNo requirement for advance enrolment for voting applies.\nNo requirement for a beneficial-holder identity declaration applies.\nNo requirement for proof of the held position applies.\nNo requirement for a prohibition on split voting applies.\nNo requirement for return of shares on loan before voting applies.\nNo requirement for a compulsory original wet-signature ballot applies.\n\n\n[Message EL1900D | MT568]\nPlease retain the replacement edition for operational reconciliation. Earlier notification conditions are superseded.\n",
  "predicate": "share_blocking",
  "truth": "NO",
  "prediction": {
    "value": "YES",
    "scores": {
      "YES": 0.7145,
      "NO": 0.2498,
      "UNKNOWN": 0.0357
    },
    "confidence": null,
    "native_score": 0.7145,
    "source": "REGISTERED_LAYA_WHOLE_NOTICE",
    "evidence": [],
    "evidence_status": "UNAVAILABLE: this decision head does not extract quotations"
  },
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
  }
}
```


## FROZEN_TEST / 5 / Laya / 019842df38bde1866068a249a668dec26d8242dcee828d768d468663a727e34c

```json
{
  "candidate": "Laya",
  "id": "019842df38bde1866068a249a668dec26d8242dcee828d768d468663a727e34c",
  "text": "[Message EL1900C | MT564]\nCompany meeting helpdesk correspondence. This message records the final instructions delivered to nominees.\nA live voting opportunity exists for owners responding to this assembly.\nNo requirement for blocking of instructed shares applies.\nNo requirement for a mandatory power of attorney applies.\nNo requirement for advance enrolment for voting applies.\nNo requirement for a beneficial-holder identity declaration applies.\nNo requirement for proof of the held position applies.\nNo requirement for a prohibition on split voting applies.\nNo requirement for return of shares on loan before voting applies.\nNo requirement for a compulsory original wet-signature ballot applies.\n\n\n[Message EL1900D | MT568]\nPlease retain the replacement edition for operational reconciliation. Earlier notification conditions are superseded.\n",
  "predicate": "holding_confirmation_required",
  "truth": "NO",
  "prediction": {
    "value": "YES",
    "scores": {
      "YES": 0.4827,
      "NO": 0.4202,
      "UNKNOWN": 0.0971
    },
    "confidence": null,
    "native_score": 0.4827,
    "source": "REGISTERED_LAYA_WHOLE_NOTICE",
    "evidence": [],
    "evidence_status": "UNAVAILABLE: this decision head does not extract quotations"
  },
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
  }
}
```


## FROZEN_TEST / 6 / Laya / 2646bc0ea8720488bf53c04676f218140e514f7ef4d7211857d5ecb5f0e9942d

```json
{
  "candidate": "Laya",
  "id": "2646bc0ea8720488bf53c04676f218140e514f7ef4d7211857d5ecb5f0e9942d",
  "text": "[Message EL0606C | MT564]\nOperational email from the proxy team. We have completed the processing arrangements described below.\nThis is solely a cash-distribution advice; it offers no meeting ballot and no shareholder vote.\nThe operator expressly waives a voting lock on the position.\nThe operator expressly waives a compulsory attorney mandate.\nThe operator expressly waives mandatory meeting registration.\nThe operator expressly waives identification of the underlying owner.\nThe operator expressly waives a custodial holding statement.\nThe operator expressly waives a requirement to cast all votes identically.\nThe operator expressly waives recall of lent securities.\nThe operator expressly waives an in-person-only voting condition.\n\n\n[Message EL0606D | MT568]\nPlease retain the replacement edition for operational reconciliation. Earlier notification conditions are superseded.\n",
  "predicate": "share_blocking",
  "truth": "NO",
  "prediction": {
    "value": "YES",
    "scores": {
      "YES": 0.764,
      "NO": 0.1947,
      "UNKNOWN": 0.0414
    },
    "confidence": null,
    "native_score": 0.764,
    "source": "REGISTERED_LAYA_WHOLE_NOTICE",
    "evidence": [],
    "evidence_status": "UNAVAILABLE: this decision head does not extract quotations"
  },
  "decision": {
    "classification": "NOT_VOTABLE",
    "rule": "R2 no current voting opportunity",
    "rule_version": "semantic-decision-2",
    "manual_review_required": true,
    "automation_enabled": false,
    "review_reasons": [
      "Synthetic-only evaluation; customer quality gate not met"
    ]
  }
}
```


## FROZEN_TEST / 7 / Laya / 2646bc0ea8720488bf53c04676f218140e514f7ef4d7211857d5ecb5f0e9942d

```json
{
  "candidate": "Laya",
  "id": "2646bc0ea8720488bf53c04676f218140e514f7ef4d7211857d5ecb5f0e9942d",
  "text": "[Message EL0606C | MT564]\nOperational email from the proxy team. We have completed the processing arrangements described below.\nThis is solely a cash-distribution advice; it offers no meeting ballot and no shareholder vote.\nThe operator expressly waives a voting lock on the position.\nThe operator expressly waives a compulsory attorney mandate.\nThe operator expressly waives mandatory meeting registration.\nThe operator expressly waives identification of the underlying owner.\nThe operator expressly waives a custodial holding statement.\nThe operator expressly waives a requirement to cast all votes identically.\nThe operator expressly waives recall of lent securities.\nThe operator expressly waives an in-person-only voting condition.\n\n\n[Message EL0606D | MT568]\nPlease retain the replacement edition for operational reconciliation. Earlier notification conditions are superseded.\n",
  "predicate": "registration_required",
  "truth": "NO",
  "prediction": {
    "value": "YES",
    "scores": {
      "YES": 0.4477,
      "NO": 0.4413,
      "UNKNOWN": 0.111
    },
    "confidence": null,
    "native_score": 0.4477,
    "source": "REGISTERED_LAYA_WHOLE_NOTICE",
    "evidence": [],
    "evidence_status": "UNAVAILABLE: this decision head does not extract quotations"
  },
  "decision": {
    "classification": "NOT_VOTABLE",
    "rule": "R2 no current voting opportunity",
    "rule_version": "semantic-decision-2",
    "manual_review_required": true,
    "automation_enabled": false,
    "review_reasons": [
      "Synthetic-only evaluation; customer quality gate not met"
    ]
  }
}
```


## FROZEN_TEST / 8 / Laya / 2646bc0ea8720488bf53c04676f218140e514f7ef4d7211857d5ecb5f0e9942d

```json
{
  "candidate": "Laya",
  "id": "2646bc0ea8720488bf53c04676f218140e514f7ef4d7211857d5ecb5f0e9942d",
  "text": "[Message EL0606C | MT564]\nOperational email from the proxy team. We have completed the processing arrangements described below.\nThis is solely a cash-distribution advice; it offers no meeting ballot and no shareholder vote.\nThe operator expressly waives a voting lock on the position.\nThe operator expressly waives a compulsory attorney mandate.\nThe operator expressly waives mandatory meeting registration.\nThe operator expressly waives identification of the underlying owner.\nThe operator expressly waives a custodial holding statement.\nThe operator expressly waives a requirement to cast all votes identically.\nThe operator expressly waives recall of lent securities.\nThe operator expressly waives an in-person-only voting condition.\n\n\n[Message EL0606D | MT568]\nPlease retain the replacement edition for operational reconciliation. Earlier notification conditions are superseded.\n",
  "predicate": "holding_confirmation_required",
  "truth": "NO",
  "prediction": {
    "value": "YES",
    "scores": {
      "YES": 0.6092,
      "NO": 0.2416,
      "UNKNOWN": 0.1493
    },
    "confidence": null,
    "native_score": 0.6092,
    "source": "REGISTERED_LAYA_WHOLE_NOTICE",
    "evidence": [],
    "evidence_status": "UNAVAILABLE: this decision head does not extract quotations"
  },
  "decision": {
    "classification": "NOT_VOTABLE",
    "rule": "R2 no current voting opportunity",
    "rule_version": "semantic-decision-2",
    "manual_review_required": true,
    "automation_enabled": false,
    "review_reasons": [
      "Synthetic-only evaluation; customer quality gate not met"
    ]
  }
}
```


## FROZEN_TEST / 9 / Laya / 2646bc0ea8720488bf53c04676f218140e514f7ef4d7211857d5ecb5f0e9942d

```json
{
  "candidate": "Laya",
  "id": "2646bc0ea8720488bf53c04676f218140e514f7ef4d7211857d5ecb5f0e9942d",
  "text": "[Message EL0606C | MT564]\nOperational email from the proxy team. We have completed the processing arrangements described below.\nThis is solely a cash-distribution advice; it offers no meeting ballot and no shareholder vote.\nThe operator expressly waives a voting lock on the position.\nThe operator expressly waives a compulsory attorney mandate.\nThe operator expressly waives mandatory meeting registration.\nThe operator expressly waives identification of the underlying owner.\nThe operator expressly waives a custodial holding statement.\nThe operator expressly waives a requirement to cast all votes identically.\nThe operator expressly waives recall of lent securities.\nThe operator expressly waives an in-person-only voting condition.\n\n\n[Message EL0606D | MT568]\nPlease retain the replacement edition for operational reconciliation. Earlier notification conditions are superseded.\n",
  "predicate": "split_voting_restricted",
  "truth": "NO",
  "prediction": {
    "value": "YES",
    "scores": {
      "YES": 0.5161,
      "NO": 0.3906,
      "UNKNOWN": 0.0933
    },
    "confidence": null,
    "native_score": 0.5161,
    "source": "REGISTERED_LAYA_WHOLE_NOTICE",
    "evidence": [],
    "evidence_status": "UNAVAILABLE: this decision head does not extract quotations"
  },
  "decision": {
    "classification": "NOT_VOTABLE",
    "rule": "R2 no current voting opportunity",
    "rule_version": "semantic-decision-2",
    "manual_review_required": true,
    "automation_enabled": false,
    "review_reasons": [
      "Synthetic-only evaluation; customer quality gate not met"
    ]
  }
}
```


## FROZEN_TEST / 10 / Laya / 2646bc0ea8720488bf53c04676f218140e514f7ef4d7211857d5ecb5f0e9942d

```json
{
  "candidate": "Laya",
  "id": "2646bc0ea8720488bf53c04676f218140e514f7ef4d7211857d5ecb5f0e9942d",
  "text": "[Message EL0606C | MT564]\nOperational email from the proxy team. We have completed the processing arrangements described below.\nThis is solely a cash-distribution advice; it offers no meeting ballot and no shareholder vote.\nThe operator expressly waives a voting lock on the position.\nThe operator expressly waives a compulsory attorney mandate.\nThe operator expressly waives mandatory meeting registration.\nThe operator expressly waives identification of the underlying owner.\nThe operator expressly waives a custodial holding statement.\nThe operator expressly waives a requirement to cast all votes identically.\nThe operator expressly waives recall of lent securities.\nThe operator expressly waives an in-person-only voting condition.\n\n\n[Message EL0606D | MT568]\nPlease retain the replacement edition for operational reconciliation. Earlier notification conditions are superseded.\n",
  "predicate": "securities_lending_recall_required",
  "truth": "NO",
  "prediction": {
    "value": "YES",
    "scores": {
      "YES": 0.6859,
      "NO": 0.2466,
      "UNKNOWN": 0.0675
    },
    "confidence": null,
    "native_score": 0.6859,
    "source": "REGISTERED_LAYA_WHOLE_NOTICE",
    "evidence": [],
    "evidence_status": "UNAVAILABLE: this decision head does not extract quotations"
  },
  "decision": {
    "classification": "NOT_VOTABLE",
    "rule": "R2 no current voting opportunity",
    "rule_version": "semantic-decision-2",
    "manual_review_required": true,
    "automation_enabled": false,
    "review_reasons": [
      "Synthetic-only evaluation; customer quality gate not met"
    ]
  }
}
```


## FROZEN_TEST / 11 / Laya / 2cc72583da330b87cb5ac0ecb5daad44af2b9689ae77a62533ab6e5c0d061148

```json
{
  "candidate": "Laya",
  "id": "2cc72583da330b87cb5ac0ecb5daad44af2b9689ae77a62533ab6e5c0d061148",
  "text": "[Message EL0602C | MT564]\nOperational email from the proxy team. We have completed the processing arrangements described below.\nEligible members may exercise their votes through the proxy service.\nTo exercise the ballot, the holder must comply with a voting lock on the position.\nThe operator expressly waives a compulsory attorney mandate.\nThe operator expressly waives mandatory meeting registration.\nThe operator expressly waives identification of the underlying owner.\nTo exercise the ballot, the holder must comply with a custodial holding statement.\nThe operator expressly waives a requirement to cast all votes identically.\nThe operator expressly waives recall of lent securities.\nThe operator expressly waives an in-person-only voting condition.\n\n\n[Message EL0602D | MT568]\nPlease retain the replacement edition for operational reconciliation. Earlier notification conditions are superseded.\n",
  "predicate": "share_blocking",
  "truth": "YES",
  "prediction": {
    "value": "NO",
    "scores": {
      "YES": 0.3859,
      "NO": 0.5861,
      "UNKNOWN": 0.0281
    },
    "confidence": null,
    "native_score": 0.5861,
    "source": "REGISTERED_LAYA_WHOLE_NOTICE",
    "evidence": [],
    "evidence_status": "UNAVAILABLE: this decision head does not extract quotations"
  },
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
  }
}
```
