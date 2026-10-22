# Every missed assertion — frozen study

AI-authored/synthetic data; diagnostic only. No training or threshold changes follow from these errors.

## FROZEN_TEST

### RC1-0715302

```text
- The agent requests voting choices on each item in the meeting agenda.
- The registrar requires the ultimate owner’s personal details before processing the ballot.
- Retail beneficial owners are excluded from this shareholder poll.
- A disposal restriction attaches to each share committed to this ballot.
- The holder is free to vote without arranging a restriction on dividing the votes.
- The registrar will reject the ballot unless the holder supplies a valid POA.
- The agent expressly waives the recall of lent stock for this ballot.
- Voting instructions must reach the custodian by 26 November 2026 at 16:00 UTC.
```

- {"field": "beneficial_owner_disclosure_required", "truth": "YES", "prediction": "NO", "native_scores": {"YES": 0.0006, "NO": 0.9986, "UNKNOWN": 0.0008}, "calibrated_correctness": 0.9874326750448833, "evidence": [], "conflict": null}

Decision/reconciliation: `{"decision": {"classification": "VOTABLE_WITH_RESTRICTION", "rule": "R5 one or more voting restrictions", "rule_version": "semantic-decision-2", "manual_review_required": true, "automation_enabled": false, "review_reasons": ["Synthetic-only evaluation; customer quality gate not met"]}, "conflicts": []}`

### RC1-0715331

```text
The registered nominee can represent the beneficial holder in the forthcoming vote.

The custodian voting deadline was 15 September 2026 at 12:00 UTC.

The full instructed position must be voted in one direction; split voting is prohibited.

A completed registration form must be delivered for the proxy vote.

Current instructions conflict about beneficial-owner disclosure; neither version has priority.

We cannot establish from the available terms whether a holdings certificate applies.

The proxy instruction must carry a wet-ink signature; digital signatures are refused.
```

- {"field": "other_voting_restriction", "truth": "YES", "prediction": "NO", "native_scores": {"YES": 0.4553, "NO": 0.5386, "UNKNOWN": 0.0062}, "calibrated_correctness": 0.49405063561459817, "evidence": [], "conflict": null}

Decision/reconciliation: `{"decision": {"classification": "DEADLINE_PASSED", "rule": "R4 controlling deadline passed", "rule_version": "semantic-decision-2", "manual_review_required": true, "automation_enabled": false, "review_reasons": ["Synthetic-only evaluation; customer quality gate not met"]}, "conflicts": []}`

### RC1-0715338

```text
A meeting of securityholders has been called to vote on the covenant amendments.

The register is administered by the issuer’s appointed transfer agent.

Disclosure of the underlying investor’s identity is required for acceptance of votes.

Electronic copies of account statements remain available through the portal.

Votes are accepted only after the registrar has enrolled the beneficial holder.

A minimum holding of five hundred shares is required to exercise the ballot.

Voting instructions must reach the custodian by 26 November 2026 at 16:00 UTC.

This communication is distributed through the usual securities-services channel.

The registrar’s postal address is unchanged from the previous circular.

Contact details for administrative enquiries appear in the service directory.

Holders should keep a copy of any correspondence for their own records.

The voting service requires a recall of the relevant securities-lending positions.

Routine settlement enquiries should quote the custody account reference.

The intermediary records timestamps when incoming documents are received.

Share blocking is optional and is not a prerequisite for voting.
```

- {"field": "holding_confirmation_required", "truth": "NO", "prediction": "YES", "native_scores": {"YES": 1.0, "NO": 0.0, "UNKNOWN": 0.0}, "calibrated_correctness": null, "evidence": [{"valid": true, "normalisation": "identity", "text": "A minimum holding of five hundred shares is required to exercise the ballot.", "start": 400, "end": 476, "source": "SCOPED_SOURCE_CANDIDATE", "entailment_independently_verified": false}], "conflict": null}

Decision/reconciliation: `{"decision": {"classification": "UNCERTAIN_MANUAL_REVIEW", "rule": "R1 unresolved conflicts", "rule_version": "semantic-decision-2", "manual_review_required": true, "automation_enabled": false, "review_reasons": ["share_blocking:SCOPED_EVIDENCE_CONFLICT_OR_CONDITION", "Synthetic-only evaluation; customer quality gate not met"]}, "conflicts": ["share_blocking:SCOPED_EVIDENCE_CONFLICT_OR_CONDITION"]}`

### RC1-0715346

```text
Custody operations communication
Owners can send proxy directions for the board election and proposed articles.
This market requires an original POA to authorise the nominee’s meeting vote.
Voting instructions must reach the custodian by 26 November 2026 at 16:00 UTC.
Voting eligibility must be supported by a current ownership certificate.
Shares on loan must be recalled before the holder can participate in this vote.
There is no requirement for a uniform-voting condition in the final terms.
There is no requirement for beneficial-owner disclosure in the final terms.
Instructed shares are locked against sale pending completion of the meeting.
Pre-registration for voting is not required for the current vote.
```

- {"field": "other_voting_restriction", "truth": "NO", "prediction": "YES", "native_scores": {"YES": 0.9997, "NO": 0.0002, "UNKNOWN": 0.0001}, "calibrated_correctness": null, "evidence": [], "conflict": null}

Decision/reconciliation: `{"decision": {"classification": "VOTABLE_WITH_RESTRICTION", "rule": "R5 one or more voting restrictions", "rule_version": "semantic-decision-2", "manual_review_required": true, "automation_enabled": false, "review_reasons": ["Synthetic-only evaluation; customer quality gate not met"]}, "conflicts": []}`

### RC1-0715382

```text
Custody operations communication
Owners can send proxy directions for the board election and proposed articles.
Whether voting requires a power of attorney remains unresolved pending clarification.
Voting instructions must reach the custodian by 26 November 2026 at 16:00 UTC.
Advance enrolment with the registrar is optional and is not a prerequisite for voting.
Owner-name disclosure is a compulsory condition of proxy participation.
The holder must use a uniform choice for all instructed shares on each motion.
The agent expressly waives an extra market-specific voting condition for this ballot.
A disposal restriction attaches to each share committed to this ballot.
The current proxy process does not impose a securities-loan recall.
```

- {"field": "other_voting_restriction", "truth": "NO", "prediction": "YES", "native_scores": {"YES": 0.9113, "NO": 0.0832, "UNKNOWN": 0.0055}, "calibrated_correctness": null, "evidence": [], "conflict": null}

Decision/reconciliation: `{"decision": {"classification": "VOTABLE_WITH_RESTRICTION", "rule": "R5 one or more voting restrictions", "rule_version": "semantic-decision-2", "manual_review_required": true, "automation_enabled": false, "review_reasons": ["Synthetic-only evaluation; customer quality gate not met"]}, "conflicts": []}`

### RC1-0715386

```text
- Instruct the custodian to vote for, against or abstain on the enclosed resolutions.
- We cannot establish from the available terms whether documentary proof of ownership applies.
- The holder must register its voting participation in advance.
- A prohibition on split voting is optional and is not a prerequisite for voting.
- Voting representation depends on receipt of the signed power-of-attorney instrument.
- Owner-name reporting is optional and is not a prerequisite for voting.
- Voting instructions must reach the custodian by 26 November 2026 at 16:00 UTC.
- The relevant annex is missing, leaving the condition concerning an extra market-specific voting condition uncertain.
- Shares on loan must be recalled before the holder can participate in this vote.
```

- {"field": "other_voting_restriction", "truth": "UNKNOWN", "prediction": "YES", "native_scores": {"YES": 0.3919, "NO": 0.2795, "UNKNOWN": 0.3286}, "calibrated_correctness": null, "evidence": [], "conflict": null}

Decision/reconciliation: `{"decision": {"classification": "VOTABLE_WITH_RESTRICTION", "rule": "R5 one or more voting restrictions", "rule_version": "semantic-decision-2", "manual_review_required": true, "automation_enabled": false, "review_reasons": ["Synthetic-only evaluation; customer quality gate not met"]}, "conflicts": []}`

### RC1-0715458

```text
Custody operations communication
The court-convened meeting will decide the proposed scheme by a shareholder vote.
The holder must register its voting participation in advance.
Copies of the published accounts can be requested from the company secretary.
Shares covered by an instruction cannot be sold before the end of the poll.
We cannot establish from the available terms whether a uniform-voting condition applies.
The custodian maintains an archive of notices for the reporting period.
The custodian must recall lent stock as a condition of proxy voting.
The custodian voting deadline was 15 September 2026 at 12:00 UTC.
The beneficial owner has to submit documentary proof of holding for this proxy ballot.
The voting form must identify the beneficial owner behind the custody account.
```

- {"field": "split_voting_restricted", "truth": "UNKNOWN", "prediction": "NO", "native_scores": {"YES": 0.0609, "NO": 0.8602, "UNKNOWN": 0.0789}, "calibrated_correctness": 0.925628940135754, "evidence": [], "conflict": null}
- {"field": "other_voting_restriction", "truth": "NO", "prediction": "YES", "native_scores": {"YES": 0.9356, "NO": 0.0375, "UNKNOWN": 0.0269}, "calibrated_correctness": null, "evidence": [], "conflict": null}

Decision/reconciliation: `{"decision": {"classification": "DEADLINE_PASSED", "rule": "R4 controlling deadline passed", "rule_version": "semantic-decision-2", "manual_review_required": true, "automation_enabled": false, "review_reasons": ["Synthetic-only evaluation; customer quality gate not met"]}, "conflicts": []}`

### RC1-0715478

```text
Bondholders have an opportunity to cast votes at the announced noteholder meeting. Holders should keep a copy of any correspondence for their own records. Whether voting requires a securities-loan recall remains unresolved pending clarification. Meeting registration is optional and is not a prerequisite for voting. The register is administered by the issuer’s appointed transfer agent. The intermediary records timestamps when incoming documents are received. Routine settlement enquiries should quote the custody account reference. A disposal restriction attaches to each share committed to this ballot. No ballot will be rejected because the holder has not arranged disclosure of the ultimate investor’s identity. The service desk is available during the custodian’s published business hours. Contact details for administrative enquiries appear in the service directory. A power of attorney is optional and is not a prerequisite for voting. A notarised signature on the voting form is mandatory in addition to the ordinary documents. Copies of the published accounts can be requested from the company secretary. This communication is distributed through the usual securities-services channel. Voting instructions must reach the custodian by 26 November 2026 at 16:00 UTC.
```

- {"field": "holding_confirmation_required", "truth": "NO", "prediction": "YES", "native_scores": {"YES": 0.9997, "NO": 0.0001, "UNKNOWN": 0.0001}, "calibrated_correctness": null, "evidence": [], "conflict": null}

Decision/reconciliation: `{"decision": {"classification": "UNCERTAIN_MANUAL_REVIEW", "rule": "R1 unresolved conflicts", "rule_version": "semantic-decision-2", "manual_review_required": true, "automation_enabled": false, "review_reasons": ["registration_required:SCOPED_EVIDENCE_CONFLICT_OR_CONDITION", "beneficial_owner_disclosure_required:SCOPED_EVIDENCE_CONFLICT_OR_CONDITION", "Synthetic-only evaluation; customer quality gate not met"]}, "conflicts": ["beneficial_owner_disclosure_required:SCOPED_EVIDENCE_CONFLICT_OR_CONDITION", "registration_required:SCOPED_EVIDENCE_CONFLICT_OR_CONDITION"]}`

### RC1-0715510

```text
This is an invitation to participate in the general-meeting poll by proxy.

Anonymous proxy directions are rejected; beneficial-owner identification is mandatory.

A further participation restriction is optional and is not a prerequisite for voting.

The agent has not confirmed whether a uniform-voting condition is compulsory for this ballot.

The lender has to complete a securities-loan recall to exercise the ballot.

Documentary proof of ownership is optional and is not a prerequisite for voting.

Voting instructions must reach the custodian by 26 November 2026 at 16:00 UTC.

A power of attorney is optional and is not a prerequisite for voting.
```

- {"field": "split_voting_restricted", "truth": "UNKNOWN", "prediction": "NO", "native_scores": {"YES": 0.0029, "NO": 0.9955, "UNKNOWN": 0.0015}, "calibrated_correctness": 0.9848654909567146, "evidence": [], "conflict": null}

Decision/reconciliation: `{"decision": {"classification": "VOTABLE_WITH_RESTRICTION", "rule": "R5 one or more voting restrictions", "rule_version": "semantic-decision-2", "manual_review_required": true, "automation_enabled": false, "review_reasons": ["Synthetic-only evaluation; customer quality gate not met"]}, "conflicts": []}`

### RC1-0715515

```text
Custody operations communication
The election of the supervisory board is subject to the current shareholder ballot.
Voting instructions must reach the custodian by 26 November 2026 at 16:00 UTC.
No ballot will be rejected because the holder has not arranged the recall of lent stock.
The custodian must block the instructed shares for the duration of the voting process.
Advance enrolment with the registrar is optional and is not a prerequisite for voting.
Voting eligibility must be supported by a current ownership certificate.
```

- {"field": "other_voting_restriction", "truth": "NO", "prediction": "YES", "native_scores": {"YES": 0.9986, "NO": 0.0011, "UNKNOWN": 0.0003}, "calibrated_correctness": null, "evidence": [], "conflict": null}

Decision/reconciliation: `{"decision": {"classification": "UNCERTAIN_MANUAL_REVIEW", "rule": "R1 unresolved conflicts", "rule_version": "semantic-decision-2", "manual_review_required": true, "automation_enabled": false, "review_reasons": ["securities_lending_recall_required:SCOPED_EVIDENCE_CONFLICT_OR_CONDITION", "Synthetic-only evaluation; customer quality gate not met"]}, "conflicts": ["securities_lending_recall_required:SCOPED_EVIDENCE_CONFLICT_OR_CONDITION"]}`

### RC1-0715598

```text
- We can transmit your ballot to the tabulator for the announced meeting.
- Owner-name disclosure is a compulsory condition of proxy participation.
- No ballot will be rejected because the holder has not arranged the mandatory return of securities on loan.
- Electronic copies of account statements remain available through the portal.
- A restriction on dividing the votes is optional and is not a prerequisite for voting.
- The register is administered by the issuer’s appointed transfer agent.
- Voting instructions must reach the custodian by 26 November 2026 at 16:00 UTC.
- An additional investor-eligibility restriction is optional and is not a prerequisite for voting.
- The agent expressly waives pre-registration for voting for this ballot.
- No ballot will be rejected because the holder has not arranged immobilisation of the voting shares.
- Whether voting requires a custodian position confirmation remains unresolved pending clarification.
- Current instructions conflict about a power of attorney; neither version has priority.
```

- {"field": "share_blocking", "truth": "NO", "prediction": "YES", "native_scores": {"YES": 0.9583, "NO": 0.0315, "UNKNOWN": 0.0102}, "calibrated_correctness": null, "evidence": [{"valid": true, "normalisation": "identity", "text": "- No ballot will be rejected because the holder has not arranged immobilisation of the voting shares.", "start": 751, "end": 852, "source": "SCOPED_SOURCE_CANDIDATE", "entailment_independently_verified": false}], "conflict": null}
- {"field": "beneficial_owner_disclosure_required", "truth": "YES", "prediction": "NO", "native_scores": {"YES": 0.422, "NO": 0.514, "UNKNOWN": 0.0641}, "calibrated_correctness": null, "evidence": [], "conflict": true}

Decision/reconciliation: `{"decision": {"classification": "UNCERTAIN_MANUAL_REVIEW", "rule": "R1 unresolved conflicts", "rule_version": "semantic-decision-2", "manual_review_required": true, "automation_enabled": false, "review_reasons": ["registration_required:SCOPED_EVIDENCE_CONFLICT_OR_CONDITION", "beneficial_owner_disclosure_required:SCOPED_EVIDENCE_CONFLICT_OR_CONDITION", "securities_lending_recall_required:SCOPED_EVIDENCE_CONFLICT_OR_CONDITION", "Synthetic-only evaluation; customer quality gate not met"]}, "conflicts": ["beneficial_owner_disclosure_required:SCOPED_EVIDENCE_CONFLICT_OR_CONDITION", "registration_required:SCOPED_EVIDENCE_CONFLICT_OR_CONDITION", "securities_lending_recall_required:SCOPED_EVIDENCE_CONFLICT_OR_CONDITION"]}`

### RC1-0715637

```text
We require your ballot preferences for the issuer’s annual meeting. The custodian voting deadline was 15 September 2026 at 12:00 UTC. The holder is free to vote without arranging immobilisation of the voting shares. An extra market-specific voting condition is not required for the current vote. The registrar will reject the ballot unless the holder supplies a valid POA. Account reconciliations are performed after the close of each business day. The intermediary records timestamps when incoming documents are received. Owner-name reporting is optional and is not a prerequisite for voting. The holder is free to vote without arranging a securities-loan recall. The beneficial owner has to submit documentary proof of holding for this proxy ballot.
```

- {"field": "other_voting_restriction", "truth": "NO", "prediction": "YES", "native_scores": {"YES": 0.9909, "NO": 0.0082, "UNKNOWN": 0.0009}, "calibrated_correctness": null, "evidence": [], "conflict": null}

Decision/reconciliation: `{"decision": {"classification": "DEADLINE_PASSED", "rule": "R4 controlling deadline passed", "rule_version": "semantic-decision-2", "manual_review_required": true, "automation_enabled": false, "review_reasons": ["Synthetic-only evaluation; customer quality gate not met"]}, "conflicts": []}`

### RC1-0715682

```text
Investors may exercise their voting rights through the nominee at this meeting. A beneficial ownership disclosure must accompany the meeting instruction. The agent has not confirmed whether an additional investor-eligibility restriction is compulsory for this ballot. A disposal restriction attaches to each share committed to this ballot. The custodian voting deadline was 15 September 2026 at 12:00 UTC. Any earlier condition for pre-registration for voting has been withdrawn and no longer applies. A custodian position confirmation is optional and is not a prerequisite for voting.
```

- {"field": "share_blocking", "truth": "YES", "prediction": "NO", "native_scores": {"YES": 0.4144, "NO": 0.53, "UNKNOWN": 0.0555}, "calibrated_correctness": null, "evidence": [], "conflict": true}

Decision/reconciliation: `{"decision": {"classification": "UNCERTAIN_MANUAL_REVIEW", "rule": "R1 unresolved conflicts", "rule_version": "semantic-decision-2", "manual_review_required": true, "automation_enabled": false, "review_reasons": ["share_blocking:SCOPED_EVIDENCE_CONFLICT_OR_CONDITION", "holding_confirmation_required:SCOPED_EVIDENCE_CONFLICT_OR_CONDITION", "Synthetic-only evaluation; customer quality gate not met"]}, "conflicts": ["holding_confirmation_required:SCOPED_EVIDENCE_CONFLICT_OR_CONDITION", "share_blocking:SCOPED_EVIDENCE_CONFLICT_OR_CONDITION"]}`

### RC1-0715683

```text
The election of the supervisory board is subject to the current shareholder ballot.

Different voting choices cannot be assigned to portions of the same position.

The registrar’s postal address is unchanged from the previous circular.

Immobilisation of the voting shares is optional and is not a prerequisite for voting.

Meeting registration is optional and is not a prerequisite for voting.

Voting instructions must reach the custodian by 26 November 2026 at 16:00 UTC.

The payment account and tax reporting arrangements are unaffected.

Holders should keep a copy of any correspondence for their own records.

Custody fees are reported separately on the periodic account statement.

The register is administered by the issuer’s appointed transfer agent.

The intermediary records timestamps when incoming documents are received.

The beneficial owner must execute the power of attorney before votes can be accepted.

Routine settlement enquiries should quote the custody account reference.

A holdings certificate must accompany the shareholder voting instruction.

Loaned shares are eligible only after a mandatory recall has settled.

The service desk is available during the custodian’s published business hours.
```

- {"field": "other_voting_restriction", "truth": "NO", "prediction": "YES", "native_scores": {"YES": 0.9563, "NO": 0.0428, "UNKNOWN": 0.0009}, "calibrated_correctness": null, "evidence": [], "conflict": null}

Decision/reconciliation: `{"decision": {"classification": "UNCERTAIN_MANUAL_REVIEW", "rule": "R1 unresolved conflicts", "rule_version": "semantic-decision-2", "manual_review_required": true, "automation_enabled": false, "review_reasons": ["share_blocking:SCOPED_EVIDENCE_CONFLICT_OR_CONDITION", "registration_required:SCOPED_EVIDENCE_CONFLICT_OR_CONDITION", "Synthetic-only evaluation; customer quality gate not met"]}, "conflicts": ["registration_required:SCOPED_EVIDENCE_CONFLICT_OR_CONDITION", "share_blocking:SCOPED_EVIDENCE_CONFLICT_OR_CONDITION"]}`

### RC1-0715951

```text
You may instruct an abstention or a voting preference for each meeting motion.

Shares covered by an instruction cannot be sold before the end of the poll.

Different voting choices cannot be assigned to portions of the same position.

Voting representation depends on receipt of the signed power-of-attorney instrument.

Registration with the meeting agent is compulsory before proxy instructions can be lodged.

Votes can be submitted only by physical attendance, with no remote voting route.

The custodian voting deadline was 15 September 2026 at 12:00 UTC.
```

- {"field": "beneficial_owner_disclosure_required", "truth": "NO", "prediction": "YES", "native_scores": {"YES": 0.9967, "NO": 0.0017, "UNKNOWN": 0.0016}, "calibrated_correctness": null, "evidence": [], "conflict": null}
- {"field": "holding_confirmation_required", "truth": "NO", "prediction": "YES", "native_scores": {"YES": 0.9835, "NO": 0.0161, "UNKNOWN": 0.0004}, "calibrated_correctness": null, "evidence": [], "conflict": null}

Decision/reconciliation: `{"decision": {"classification": "DEADLINE_PASSED", "rule": "R4 controlling deadline passed", "rule_version": "semantic-decision-2", "manual_review_required": true, "automation_enabled": false, "review_reasons": ["Synthetic-only evaluation; customer quality gate not met"]}, "conflicts": []}`

### RC1-0715990

```text
Please indicate how the registered holder should cast your shares at the general meeting. Whether voting requires advance enrolment with the registrar remains unresolved pending clarification. Holders may vote without a securities-loan recall. Voting instructions must reach the custodian by 26 November 2026 at 16:00 UTC. Voting requires the custodian to immobilise the securities until adjournment. The registrar is still investigating the possible requirement for a uniform-voting condition. The relevant annex is missing, leaving the condition concerning documentary proof of ownership uncertain.
```

- {"field": "split_voting_restricted", "truth": "UNKNOWN", "prediction": "NO", "native_scores": {"YES": 0.0027, "NO": 0.9946, "UNKNOWN": 0.0027}, "calibrated_correctness": 0.9858166550103946, "evidence": [], "conflict": null}

Decision/reconciliation: `{"decision": {"classification": "VOTABLE_WITH_RESTRICTION", "rule": "R5 one or more voting restrictions", "rule_version": "semantic-decision-2", "manual_review_required": true, "automation_enabled": false, "review_reasons": ["Synthetic-only evaluation; customer quality gate not met"]}, "conflicts": []}`

### RC1-0716238

```text
Custody operations communication
The nominee is accepting ballots on the resolutions at the upcoming annual assembly.
An outstanding securities loan must be terminated and the shares returned for this ballot.
Participation in the vote requires advance enrolment with the registrar.
There is no requirement for share blocking in the final terms.
Voting instructions must reach the custodian by 26 November 2026 at 16:00 UTC.
Anonymous proxy directions are rejected; beneficial-owner identification is mandatory.
A notarised voting power of attorney is compulsory for beneficial owners.
A confirmation of ownership from the custodian is mandatory for this vote.
```

- {"field": "registration_required", "truth": "YES", "prediction": "NO", "native_scores": {"YES": 0.0722, "NO": 0.9266, "UNKNOWN": 0.0013}, "calibrated_correctness": null, "evidence": [], "conflict": true}

Decision/reconciliation: `{"decision": {"classification": "UNCERTAIN_MANUAL_REVIEW", "rule": "R1 unresolved conflicts", "rule_version": "semantic-decision-2", "manual_review_required": true, "automation_enabled": false, "review_reasons": ["registration_required:SCOPED_EVIDENCE_CONFLICT_OR_CONDITION", "Synthetic-only evaluation; customer quality gate not met"]}, "conflicts": ["registration_required:SCOPED_EVIDENCE_CONFLICT_OR_CONDITION"]}`

### RC1-0716256

```text
- This is an invitation to participate in the general-meeting poll by proxy.
- Voting instructions must reach the custodian by 26 November 2026 at 16:00 UTC.
- The relevant annex is missing, leaving the condition concerning an extra market-specific voting condition uncertain.
- Whether voting requires a freeze on instructed securities remains unresolved pending clarification.
- An attorney mandate for voting is optional and is not a prerequisite for voting.
- Any earlier condition for a prohibition on split voting has been withdrawn and no longer applies.
- A holdings certificate must accompany the shareholder voting instruction.
```

- {"field": "other_voting_restriction", "truth": "UNKNOWN", "prediction": "NO", "native_scores": {"YES": 0.0019, "NO": 0.7982, "UNKNOWN": 0.1999}, "calibrated_correctness": null, "evidence": [], "conflict": null}

Decision/reconciliation: `{"decision": {"classification": "VOTABLE_WITH_RESTRICTION", "rule": "R5 one or more voting restrictions", "rule_version": "semantic-decision-2", "manual_review_required": true, "automation_enabled": false, "review_reasons": ["Synthetic-only evaluation; customer quality gate not met"]}, "conflicts": []}`

### RC1-0716288

```text
The attachment needed to determine whether a ballot exists is missing. The registrar’s postal address is unchanged from the previous circular. Custody fees are reported separately on the periodic account statement.
```

- {"field": "votability", "truth": "UNCERTAIN", "prediction": "NOT_VOTABLE", "native_scores": {"VOTABLE": 0.0, "NOT_VOTABLE": 0.9999, "UNCERTAIN": 0.0}, "calibrated_correctness": 0.9946140035906643, "evidence": [{"valid": true, "normalisation": "identity", "text": "The attachment needed to determine whether a ballot exists is missing.", "start": 0, "end": 70, "source": "SCOPED_SOURCE_CANDIDATE", "entailment_independently_verified": false}], "conflict": null}

Decision/reconciliation: `{"decision": {"classification": "NOT_VOTABLE", "rule": "R2 no current voting opportunity", "rule_version": "semantic-decision-2", "manual_review_required": true, "automation_enabled": false, "review_reasons": ["Synthetic-only evaluation; customer quality gate not met"]}, "conflicts": []}`

### RC1-0716325

```text
Please return the voting direction form for the general meeting. The registrar confirms that a uniform-voting condition is unnecessary for this event. The registrar requires documentary holdings confirmation before accepting proxy directions. The registrar is still investigating the possible requirement for advance enrolment with the registrar. The registrar is still investigating the possible requirement for beneficial-owner disclosure. A notarised voting power of attorney is compulsory for beneficial owners.
```

- {"field": "registration_required", "truth": "UNKNOWN", "prediction": "NO", "native_scores": {"YES": 0.0019, "NO": 0.9283, "UNKNOWN": 0.0699}, "calibrated_correctness": null, "evidence": [], "conflict": true}

Decision/reconciliation: `{"decision": {"classification": "UNCERTAIN_MANUAL_REVIEW", "rule": "R1 unresolved conflicts", "rule_version": "semantic-decision-2", "manual_review_required": true, "automation_enabled": false, "review_reasons": ["registration_required:SCOPED_EVIDENCE_CONFLICT_OR_CONDITION", "Synthetic-only evaluation; customer quality gate not met"]}, "conflicts": ["registration_required:SCOPED_EVIDENCE_CONFLICT_OR_CONDITION"]}`

### RC1-0716392

```text
Please return the voting direction form for the general meeting.

The ballot is subject to a prohibition on split votes.

Holders may vote without a custodian position confirmation.

A minimum holding of five hundred shares is required to exercise the ballot.

The intermediary records timestamps when incoming documents are received.

The custodian voting deadline was 15 September 2026 at 12:00 UTC.

Owner-name disclosure is a compulsory condition of proxy participation.

The issuer publishes financial reports through its investor-relations service.
```

- {"field": "holding_confirmation_required", "truth": "NO", "prediction": "YES", "native_scores": {"YES": 0.9997, "NO": 0.0002, "UNKNOWN": 0.0001}, "calibrated_correctness": null, "evidence": [{"valid": true, "normalisation": "identity", "text": "A minimum holding of five hundred shares is required to exercise the ballot.", "start": 183, "end": 259, "source": "SCOPED_SOURCE_CANDIDATE", "entailment_independently_verified": false}], "conflict": true}

Decision/reconciliation: `{"decision": {"classification": "UNCERTAIN_MANUAL_REVIEW", "rule": "R1 unresolved conflicts", "rule_version": "semantic-decision-2", "manual_review_required": true, "automation_enabled": false, "review_reasons": ["holding_confirmation_required:SCOPED_EVIDENCE_CONFLICT_OR_CONDITION", "Synthetic-only evaluation; customer quality gate not met"]}, "conflicts": ["holding_confirmation_required:SCOPED_EVIDENCE_CONFLICT_OR_CONDITION"]}`

### RC1-0716590

```text
Custody operations communication
We require your ballot preferences for the issuer’s annual meeting.
Voting instructions must reach the custodian by 26 November 2026 at 16:00 UTC.
The holder is free to vote without arranging immobilisation of the voting shares.
Whether voting requires an extra market-specific voting condition remains unresolved pending clarification.
A notarised voting power of attorney is compulsory for beneficial owners.
Voting eligibility must be supported by a current ownership certificate.
```

- {"field": "other_voting_restriction", "truth": "UNKNOWN", "prediction": "YES", "native_scores": {"YES": 0.9987, "NO": 0.0001, "UNKNOWN": 0.0012}, "calibrated_correctness": null, "evidence": [], "conflict": null}

Decision/reconciliation: `{"decision": {"classification": "VOTABLE_WITH_RESTRICTION", "rule": "R5 one or more voting restrictions", "rule_version": "semantic-decision-2", "manual_review_required": true, "automation_enabled": false, "review_reasons": ["Synthetic-only evaluation; customer quality gate not met"]}, "conflicts": []}`

### RC1-0716718

```text
The attachment needed to determine whether a ballot exists is missing. The custodian maintains an archive of notices for the reporting period. The payment account and tax reporting arrangements are unaffected. The service desk is available during the custodian’s published business hours. This communication is distributed through the usual securities-services channel. The register is administered by the issuer’s appointed transfer agent. Account reconciliations are performed after the close of each business day. The issuer publishes financial reports through its investor-relations service. Electronic copies of account statements remain available through the portal.
```

- {"field": "votability", "truth": "UNCERTAIN", "prediction": "NOT_VOTABLE", "native_scores": {"VOTABLE": 0.0005, "NOT_VOTABLE": 0.999, "UNCERTAIN": 0.0005}, "calibrated_correctness": null, "evidence": [{"valid": true, "normalisation": "identity", "text": "The attachment needed to determine whether a ballot exists is missing.", "start": 0, "end": 70, "source": "SCOPED_SOURCE_CANDIDATE", "entailment_independently_verified": false}], "conflict": null}

Decision/reconciliation: `{"decision": {"classification": "UNCERTAIN_MANUAL_REVIEW", "rule": "R1 unresolved conflicts", "rule_version": "semantic-decision-2", "manual_review_required": true, "automation_enabled": false, "review_reasons": ["share_blocking:SCOPED_EVIDENCE_CONFLICT_OR_CONDITION", "registration_required:SCOPED_EVIDENCE_CONFLICT_OR_CONDITION", "Synthetic-only evaluation; customer quality gate not met"]}, "conflicts": ["registration_required:SCOPED_EVIDENCE_CONFLICT_OR_CONDITION", "share_blocking:SCOPED_EVIDENCE_CONFLICT_OR_CONDITION"]}`

### RC1-0716720

```text
- A new extraordinary meeting has been scheduled and ballots may be lodged.
- Contact details for administrative enquiries appear in the service directory.
- Account reconciliations are performed after the close of each business day.
- The register is administered by the issuer’s appointed transfer agent.
- The service desk is available during the custodian’s published business hours.
- Different voting choices cannot be assigned to portions of the same position.
- A disposal restriction attaches to each share committed to this ballot.
- The payment account and tax reporting arrangements are unaffected.
- Routine settlement enquiries should quote the custody account reference.
- Voting instructions must reach the custodian by 26 November 2026 at 16:00 UTC.
- No ballot will be rejected because the holder has not arranged a securities-loan recall.
- Electronic copies of account statements remain available through the portal.
- The issuer publishes financial reports through its investor-relations service.
- The registrar requires the ultimate owner’s personal details before processing the ballot.
- Meeting registration is optional and is not a prerequisite for voting.
```

- {"field": "other_voting_restriction", "truth": "NO", "prediction": "YES", "native_scores": {"YES": 0.9574, "NO": 0.0367, "UNKNOWN": 0.006}, "calibrated_correctness": null, "evidence": [], "conflict": null}

Decision/reconciliation: `{"decision": {"classification": "UNCERTAIN_MANUAL_REVIEW", "rule": "R1 unresolved conflicts", "rule_version": "semantic-decision-2", "manual_review_required": true, "automation_enabled": false, "review_reasons": ["registration_required:SCOPED_EVIDENCE_CONFLICT_OR_CONDITION", "securities_lending_recall_required:SCOPED_EVIDENCE_CONFLICT_OR_CONDITION", "Synthetic-only evaluation; customer quality gate not met"]}, "conflicts": ["registration_required:SCOPED_EVIDENCE_CONFLICT_OR_CONDITION", "securities_lending_recall_required:SCOPED_EVIDENCE_CONFLICT_OR_CONDITION"]}`

### RC1-0716745

```text
Please indicate how the registered holder should cast your shares at the general meeting.

Shares on loan must be recalled before the holder can participate in this vote.

A duly signed power of attorney must accompany the voting direction.

We cannot establish from the available terms whether a freeze on instructed securities applies.

The holder must register its voting participation in advance.

The custodian voting deadline was 15 September 2026 at 12:00 UTC.

A holdings certificate must accompany the shareholder voting instruction.

The general market guide mentions disclosure of the ultimate investor’s identity, but this event is expressly exempt.
```

- {"field": "share_blocking", "truth": "UNKNOWN", "prediction": "NO", "native_scores": {"YES": 0.0001, "NO": 0.9887, "UNKNOWN": 0.0112}, "calibrated_correctness": null, "evidence": [], "conflict": true}

Decision/reconciliation: `{"decision": {"classification": "UNCERTAIN_MANUAL_REVIEW", "rule": "R1 unresolved conflicts", "rule_version": "semantic-decision-2", "manual_review_required": true, "automation_enabled": false, "review_reasons": ["share_blocking:SCOPED_EVIDENCE_CONFLICT_OR_CONDITION", "Synthetic-only evaluation; customer quality gate not met"]}, "conflicts": ["share_blocking:SCOPED_EVIDENCE_CONFLICT_OR_CONDITION"]}`

### RC1-0716769

```text
The company has opened its shareholder voting portal for the forthcoming poll. The register is administered by the issuer’s appointed transfer agent. Contact details for administrative enquiries appear in the service directory. The holder is free to vote without arranging owner-name reporting. The account currency does not change as a result of this notification. The custodian maintains an archive of notices for the reporting period. Copies of the published accounts can be requested from the company secretary. The voting service requires a recall of the relevant securities-lending positions. Routine settlement enquiries should quote the custody account reference. A completed registration form must be delivered for the proxy vote. An attorney mandate for voting is optional and is not a prerequisite for voting. The issuer publishes financial reports through its investor-relations service. This communication is distributed through the usual securities-services channel. Shares covered by an instruction cannot be sold before the end of the poll. The custodian voting deadline was 15 September 2026 at 12:00 UTC.
```

- {"field": "other_voting_restriction", "truth": "NO", "prediction": "YES", "native_scores": {"YES": 0.5376, "NO": 0.4569, "UNKNOWN": 0.0054}, "calibrated_correctness": null, "evidence": [], "conflict": null}

Decision/reconciliation: `{"decision": {"classification": "DEADLINE_PASSED", "rule": "R4 controlling deadline passed", "rule_version": "semantic-decision-2", "manual_review_required": true, "automation_enabled": false, "review_reasons": ["Synthetic-only evaluation; customer quality gate not met"]}, "conflicts": []}`

### RC1-0716843

```text
A new extraordinary meeting has been scheduled and ballots may be lodged. A custodian position confirmation is an optional service and is not a condition of voting. The registrar requires the ultimate owner’s personal details before processing the ballot. The register is administered by the issuer’s appointed transfer agent. Retail beneficial owners are excluded from this shareholder poll. Voting instructions must reach the custodian by 26 November 2026 at 16:00 UTC. Holders may vote without a signed POA. The holder must register its voting participation in advance. Contact details for administrative enquiries appear in the service directory.
```

- {"field": "beneficial_owner_disclosure_required", "truth": "YES", "prediction": "NO", "native_scores": {"YES": 0.0006, "NO": 0.9991, "UNKNOWN": 0.0003}, "calibrated_correctness": null, "evidence": [], "conflict": null}
- {"field": "holding_confirmation_required", "truth": "NO", "prediction": "YES", "native_scores": {"YES": 0.6617, "NO": 0.3355, "UNKNOWN": 0.0027}, "calibrated_correctness": null, "evidence": [], "conflict": true}
- {"field": "other_voting_restriction", "truth": "YES", "prediction": "NO", "native_scores": {"YES": 0.159, "NO": 0.8406, "UNKNOWN": 0.0004}, "calibrated_correctness": null, "evidence": [], "conflict": null}

Decision/reconciliation: `{"decision": {"classification": "UNCERTAIN_MANUAL_REVIEW", "rule": "R1 unresolved conflicts", "rule_version": "semantic-decision-2", "manual_review_required": true, "automation_enabled": false, "review_reasons": ["share_blocking:SCOPED_EVIDENCE_CONFLICT_OR_CONDITION", "holding_confirmation_required:SCOPED_EVIDENCE_CONFLICT_OR_CONDITION", "Synthetic-only evaluation; customer quality gate not met"]}, "conflicts": ["holding_confirmation_required:SCOPED_EVIDENCE_CONFLICT_OR_CONDITION", "share_blocking:SCOPED_EVIDENCE_CONFLICT_OR_CONDITION"]}`

### RC1-0716969

```text
The custodian will forward completed voting forms to the meeting registrar.

The holder is free to vote without arranging a further participation restriction.

Voting requires the custodian to immobilise the securities until adjournment.

The registrar is still investigating the possible requirement for a uniform-voting condition.

Voting instructions must reach the custodian by 26 November 2026 at 16:00 UTC.

The registrar will reject the ballot unless the holder supplies a valid POA.

Holders may vote without disclosure of the ultimate investor’s identity.

Voting requires the return of securities currently out on loan.

A completed registration form must be delivered for the proxy vote.
```

- {"field": "split_voting_restricted", "truth": "UNKNOWN", "prediction": "NO", "native_scores": {"YES": 0.0573, "NO": 0.9342, "UNKNOWN": 0.0085}, "calibrated_correctness": 0.9677303222973183, "evidence": [], "conflict": null}

Decision/reconciliation: `{"decision": {"classification": "VOTABLE_WITH_RESTRICTION", "rule": "R5 one or more voting restrictions", "rule_version": "semantic-decision-2", "manual_review_required": true, "automation_enabled": false, "review_reasons": ["Synthetic-only evaluation; customer quality gate not met"]}, "conflicts": []}`

### RC1-0716991

```text
Our custody service can lodge voting instructions for this issuer’s AGM. The account currency does not change as a result of this notification. The beneficial owner must execute the power of attorney before votes can be accepted. The register is administered by the issuer’s appointed transfer agent. The registrar confirms that share blocking is unnecessary for this event. This communication is distributed through the usual securities-services channel. Electronic copies of account statements remain available through the portal. The relevant annex is missing, leaving the condition concerning documentary proof of ownership uncertain. Votes are accepted only after the registrar has enrolled the beneficial holder. Account reconciliations are performed after the close of each business day. The custodian maintains an archive of notices for the reporting period. The registrar requires the ultimate owner’s personal details before processing the ballot. Voting instructions must reach the custodian by 26 November 2026 at 16:00 UTC. The payment account and tax reporting arrangements are unaffected. Custody fees are reported separately on the periodic account statement.
```

- {"field": "registration_required", "truth": "YES", "prediction": "NO", "native_scores": {"YES": 0.3757, "NO": 0.6218, "UNKNOWN": 0.0025}, "calibrated_correctness": null, "evidence": [], "conflict": true}
- {"field": "beneficial_owner_disclosure_required", "truth": "YES", "prediction": "UNKNOWN", "native_scores": {"YES": 0.0009, "NO": 0.0042, "UNKNOWN": 0.9949}, "calibrated_correctness": null, "evidence": [], "conflict": null}
- {"field": "securities_lending_recall_required", "truth": "NO", "prediction": "YES", "native_scores": {"YES": 0.8903, "NO": 0.1027, "UNKNOWN": 0.007}, "calibrated_correctness": null, "evidence": [], "conflict": null}

Decision/reconciliation: `{"decision": {"classification": "UNCERTAIN_MANUAL_REVIEW", "rule": "R1 unresolved conflicts", "rule_version": "semantic-decision-2", "manual_review_required": true, "automation_enabled": false, "review_reasons": ["share_blocking:SCOPED_EVIDENCE_CONFLICT_OR_CONDITION", "registration_required:SCOPED_EVIDENCE_CONFLICT_OR_CONDITION", "Synthetic-only evaluation; customer quality gate not met"]}, "conflicts": ["registration_required:SCOPED_EVIDENCE_CONFLICT_OR_CONDITION", "share_blocking:SCOPED_EVIDENCE_CONFLICT_OR_CONDITION"]}`

### RC1-0716992

```text
A meeting of securityholders has been called to vote on the covenant amendments. Copies of the published accounts can be requested from the company secretary. The current ballot is restricted to beneficial holders resident in the specified market. Holders should keep a copy of any correspondence for their own records. A nominee cannot divide its votes between different choices for the same resolution. A duly signed power of attorney must accompany the voting direction. Voting instructions must reach the custodian by 26 November 2026 at 16:00 UTC. Shares on loan must be recalled before the holder can participate in this vote. The general market guide mentions advance enrolment with the registrar, but this event is expressly exempt.
```

- {"field": "other_voting_restriction", "truth": "YES", "prediction": "NO", "native_scores": {"YES": 0.0593, "NO": 0.9399, "UNKNOWN": 0.0008}, "calibrated_correctness": null, "evidence": [], "conflict": true}

Decision/reconciliation: `{"decision": {"classification": "UNCERTAIN_MANUAL_REVIEW", "rule": "R1 unresolved conflicts", "rule_version": "semantic-decision-2", "manual_review_required": true, "automation_enabled": false, "review_reasons": ["other_voting_restriction:SCOPED_EVIDENCE_CONFLICT_OR_CONDITION", "Synthetic-only evaluation; customer quality gate not met"]}, "conflicts": ["other_voting_restriction:SCOPED_EVIDENCE_CONFLICT_OR_CONDITION"]}`

### RC1-0717128

```text
The shareholders’ assembly will vote on the remuneration report and election of directors. The custodian voting deadline was 15 September 2026 at 12:00 UTC. Contact details for administrative enquiries appear in the service directory. The beneficial owner must execute the power of attorney before votes can be accepted. The recall of lent stock is not required for the current vote. A custodian position confirmation is optional and is not a prerequisite for voting. There is no requirement for owner-name reporting in the final terms. Current instructions conflict about a uniform-voting condition; neither version has priority. Holders should keep a copy of any correspondence for their own records. The registrar is still investigating the possible requirement for a freeze on instructed securities.
```

- {"field": "split_voting_restricted", "truth": "UNKNOWN", "prediction": "NO", "native_scores": {"YES": 0.0075, "NO": 0.981, "UNKNOWN": 0.0115}, "calibrated_correctness": 0.9784078494131654, "evidence": [], "conflict": null}

Decision/reconciliation: `{"decision": {"classification": "DEADLINE_PASSED", "rule": "R4 controlling deadline passed", "rule_version": "semantic-decision-2", "manual_review_required": true, "automation_enabled": false, "review_reasons": ["Synthetic-only evaluation; customer quality gate not met"]}, "conflicts": []}`

### RC1-0717145

```text
Your beneficial holding carries a ballot on the proposed capital reorganisation.

The current proxy process does not impose a securities-loan recall.

Pre-registration for voting is optional and is not a prerequisite for voting.

The agent has not confirmed whether a power of attorney is compulsory for this ballot.

Whether voting requires share blocking remains unresolved pending clarification.

The ultimate beneficial owner’s name and address must be disclosed with each ballot.

Whether voting requires a custodian position confirmation remains unresolved pending clarification.

The custodian voting deadline was 15 September 2026 at 12:00 UTC.
```

- {"field": "other_voting_restriction", "truth": "NO", "prediction": "YES", "native_scores": {"YES": 0.9653, "NO": 0.0308, "UNKNOWN": 0.0039}, "calibrated_correctness": null, "evidence": [], "conflict": null}

Decision/reconciliation: `{"decision": {"classification": "DEADLINE_PASSED", "rule": "R4 controlling deadline passed", "rule_version": "semantic-decision-2", "manual_review_required": true, "automation_enabled": false, "review_reasons": ["Synthetic-only evaluation; customer quality gate not met"]}, "conflicts": []}`

### RC1-0717227

```text
Please return the voting direction form for the general meeting.

There is no requirement for a prohibition on split voting in the final terms.

The voting form must identify the beneficial owner behind the custody account.

An attorney mandate for voting is an optional service and is not a condition of voting.

The mandatory return of securities on loan is optional and is not a prerequisite for voting.

The holder is free to vote without arranging meeting registration.

The relevant annex is missing, leaving the condition concerning a freeze on instructed securities uncertain.

Voting instructions must reach the custodian by 26 November 2026 at 16:00 UTC.

An additional investor-eligibility restriction is optional and is not a prerequisite for voting.
```

- {"field": "share_blocking", "truth": "UNKNOWN", "prediction": "YES", "native_scores": {"YES": 0.9984, "NO": 0.0011, "UNKNOWN": 0.0005}, "calibrated_correctness": 0.9856373429084381, "evidence": [{"valid": true, "normalisation": "identity", "text": "The relevant annex is missing, leaving the condition concerning a freeze on instructed securities uncertain.", "start": 476, "end": 584, "source": "SCOPED_SOURCE_CANDIDATE", "entailment_independently_verified": false}], "conflict": null}

Decision/reconciliation: `{"decision": {"classification": "VOTABLE_WITH_RESTRICTION", "rule": "R5 one or more voting restrictions", "rule_version": "semantic-decision-2", "manual_review_required": true, "automation_enabled": false, "review_reasons": ["Synthetic-only evaluation; customer quality gate not met"]}, "conflicts": []}`

### RC1-0717246

```text
Custody operations communication
The proxy service described in the brochure is not being offered for any current meeting.
Routine settlement enquiries should quote the custody account reference.
The custodian maintains an archive of notices for the reporting period.
The service desk is available during the custodian’s published business hours.
Electronic copies of account statements remain available through the portal.
The intermediary records timestamps when incoming documents are received.
Custody fees are reported separately on the periodic account statement.
The account currency does not change as a result of this notification.
The issuer publishes financial reports through its investor-relations service.
```

- {"field": "votability", "truth": "NOT_VOTABLE", "prediction": "UNCERTAIN", "native_scores": {"VOTABLE": 0.0, "NOT_VOTABLE": 0.0013, "UNCERTAIN": 0.9987}, "calibrated_correctness": null, "evidence": [], "conflict": null}

Decision/reconciliation: `{"decision": {"classification": "UNCERTAIN_MANUAL_REVIEW", "rule": "R3 voting opportunity unresolved", "rule_version": "semantic-decision-2", "manual_review_required": true, "automation_enabled": false, "review_reasons": ["Synthetic-only evaluation; customer quality gate not met"]}, "conflicts": []}`

### RC1-0717283

```text
A new extraordinary meeting has been scheduled and ballots may be lodged.

The holder must use a uniform choice for all instructed shares on each motion.

No ballot will be rejected because the holder has not arranged pre-registration for voting.

The agent expressly waives a freeze on instructed securities for this ballot.

Contact details for administrative enquiries appear in the service directory.

The holder is free to vote without arranging owner-name reporting.

Voting instructions must reach the custodian by 26 November 2026 at 16:00 UTC.

Voting representation depends on receipt of the signed power-of-attorney instrument.

Routine settlement enquiries should quote the custody account reference.

Shares on loan must be recalled before the holder can participate in this vote.

The instruction is valid only when accompanied by the required position certificate.
```

- {"field": "other_voting_restriction", "truth": "NO", "prediction": "YES", "native_scores": {"YES": 0.9848, "NO": 0.0142, "UNKNOWN": 0.001}, "calibrated_correctness": null, "evidence": [], "conflict": null}

Decision/reconciliation: `{"decision": {"classification": "UNCERTAIN_MANUAL_REVIEW", "rule": "R1 unresolved conflicts", "rule_version": "semantic-decision-2", "manual_review_required": true, "automation_enabled": false, "review_reasons": ["registration_required:SCOPED_EVIDENCE_CONFLICT_OR_CONDITION", "Synthetic-only evaluation; customer quality gate not met"]}, "conflicts": ["registration_required:SCOPED_EVIDENCE_CONFLICT_OR_CONDITION"]}`

### RC1-0717344

```text
Bondholders have an opportunity to cast votes at the announced noteholder meeting. Meeting registration is optional and is not a prerequisite for voting. The holder must use a uniform choice for all instructed shares on each motion. The agent has not confirmed whether a securities-loan recall is compulsory for this ballot. The registrar confirms that an extra market-specific voting condition is unnecessary for this event. Voting instructions must reach the custodian by 26 November 2026 at 16:00 UTC. Proxy directions are admissible only with the required attorney mandate. Share blocking is not required for the current vote. There is no requirement for a custodian position confirmation in the final terms.
```

- {"field": "split_voting_restricted", "truth": "YES", "prediction": "NO", "native_scores": {"YES": 0.1148, "NO": 0.8818, "UNKNOWN": 0.0034}, "calibrated_correctness": 0.9395175177230165, "evidence": [], "conflict": null}

Decision/reconciliation: `{"decision": {"classification": "VOTABLE_WITH_RESTRICTION", "rule": "R5 one or more voting restrictions", "rule_version": "semantic-decision-2", "manual_review_required": true, "automation_enabled": false, "review_reasons": ["Synthetic-only evaluation; customer quality gate not met"]}, "conflicts": []}`

### RC1-0717396

```text
Custody operations communication
Please indicate how the registered holder should cast your shares at the general meeting.
Registration is mandatory even for holders voting electronically through the nominee.
Loaned shares are eligible only after a mandatory recall has settled.
Voting instructions must reach the custodian by 26 November 2026 at 16:00 UTC.
The proxy instruction must carry a wet-ink signature; digital signatures are refused.
Contact details for administrative enquiries appear in the service directory.
There is no requirement for a custodian position confirmation in the final terms.
Account reconciliations are performed after the close of each business day.
Shares covered by an instruction cannot be sold before the end of the poll.
```

- {"field": "other_voting_restriction", "truth": "YES", "prediction": "NO", "native_scores": {"YES": 0.0496, "NO": 0.9494, "UNKNOWN": 0.0011}, "calibrated_correctness": 0.9863167837682707, "evidence": [], "conflict": null}

Decision/reconciliation: `{"decision": {"classification": "VOTABLE_WITH_RESTRICTION", "rule": "R5 one or more voting restrictions", "rule_version": "semantic-decision-2", "manual_review_required": true, "automation_enabled": false, "review_reasons": ["Synthetic-only evaluation; customer quality gate not met"]}, "conflicts": []}`

### RC1-0717547

```text
Shareholders can give the nominee an instruction on the proposed change of domicile. Voting eligibility must be supported by a current ownership certificate. Pre-registration for voting is optional and is not a prerequisite for voting. Instructed shares are locked against sale pending completion of the meeting. An attorney mandate for voting is optional and is not a prerequisite for voting. This communication is distributed through the usual securities-services channel. Owner-name reporting is optional and is not a prerequisite for voting. The market accepts only one voting direction for the entire nominee position. The registrar is still investigating the possible requirement for a securities-loan recall. Copies of the published accounts can be requested from the company secretary.
```

- {"field": "other_voting_restriction", "truth": "NO", "prediction": "YES", "native_scores": {"YES": 0.9962, "NO": 0.0035, "UNKNOWN": 0.0003}, "calibrated_correctness": null, "evidence": [], "conflict": null}

Decision/reconciliation: `{"decision": {"classification": "VOTABLE_WITH_RESTRICTION", "rule": "R5 one or more voting restrictions", "rule_version": "semantic-decision-2", "manual_review_required": true, "automation_enabled": false, "review_reasons": ["Synthetic-only evaluation; customer quality gate not met"]}, "conflicts": []}`

### RC1-0717598

```text
The registered nominee can represent the beneficial holder in the forthcoming vote. The holder is free to vote without arranging a custodian position confirmation. There is no requirement for a prohibition on split voting in the final terms. Current instructions conflict about an extra market-specific voting condition; neither version has priority. We cannot establish from the available terms whether immobilisation of the voting shares applies. The custodian voting deadline was 15 September 2026 at 12:00 UTC. The account currency does not change as a result of this notification. The intermediary records timestamps when incoming documents are received. The registrar is still investigating the possible requirement for the mandatory return of securities on loan.
```

- {"field": "other_voting_restriction", "truth": "UNKNOWN", "prediction": "YES", "native_scores": {"YES": 0.4916, "NO": 0.1419, "UNKNOWN": 0.3665}, "calibrated_correctness": null, "evidence": [], "conflict": null}

Decision/reconciliation: `{"decision": {"classification": "UNCERTAIN_MANUAL_REVIEW", "rule": "R1 unresolved conflicts", "rule_version": "semantic-decision-2", "manual_review_required": true, "automation_enabled": false, "review_reasons": ["registration_required:SCOPED_EVIDENCE_CONFLICT_OR_CONDITION", "Synthetic-only evaluation; customer quality gate not met"]}, "conflicts": ["registration_required:SCOPED_EVIDENCE_CONFLICT_OR_CONDITION"]}`

### RC1-0717677

```text
- This operational notice invites proxy votes on current shareholder resolutions.
- Holders may vote without a uniform-voting condition.
- The current proxy process does not impose beneficial-owner disclosure.
- The registrar will reject the ballot unless the holder supplies a valid POA.
- The beneficial owner has to submit documentary proof of holding for this proxy ballot.
- The service desk is available during the custodian’s published business hours.
- Custody fees are reported separately on the periodic account statement.
- The registrar’s postal address is unchanged from the previous circular.
- Contact details for administrative enquiries appear in the service directory.
- Routine settlement enquiries should quote the custody account reference.
- The issuer publishes financial reports through its investor-relations service.
- The proxy instruction must carry a wet-ink signature; digital signatures are refused.
- Submission of proxy directions prevents transfer of the corresponding shares.
- The lender has to complete a securities-loan recall to exercise the ballot.
- The custodian maintains an archive of notices for the reporting period.
- Voting instructions must reach the custodian by 26 November 2026 at 16:00 UTC.
- The account currency does not change as a result of this notification.
```

- {"field": "split_voting_restricted", "truth": "NO", "prediction": "YES", "native_scores": {"YES": 0.9941, "NO": 0.0048, "UNKNOWN": 0.001}, "calibrated_correctness": null, "evidence": [], "conflict": null}

Decision/reconciliation: `{"decision": {"classification": "VOTABLE_WITH_RESTRICTION", "rule": "R5 one or more voting restrictions", "rule_version": "semantic-decision-2", "manual_review_required": true, "automation_enabled": false, "review_reasons": ["Synthetic-only evaluation; customer quality gate not met"]}, "conflicts": []}`

### RC1-0717729

```text
The nominee is accepting ballots on the resolutions at the upcoming annual assembly.

A custodian-issued shareholding statement is compulsory for meeting participation.

The general market guide mentions meeting registration, but this event is expressly exempt.

The beneficial owner must execute the power of attorney before votes can be accepted.

A securities-loan recall is optional and is not a prerequisite for voting.

Owner-name reporting is optional and is not a prerequisite for voting.

A uniform-voting condition is not required for the current vote.

Voting instructions must reach the custodian by 26 November 2026 at 16:00 UTC.
```

- {"field": "share_blocking", "truth": "NO", "prediction": "YES", "native_scores": {"YES": 0.9548, "NO": 0.016, "UNKNOWN": 0.0292}, "calibrated_correctness": null, "evidence": [], "conflict": null}

Decision/reconciliation: `{"decision": {"classification": "VOTABLE_WITH_RESTRICTION", "rule": "R5 one or more voting restrictions", "rule_version": "semantic-decision-2", "manual_review_required": true, "automation_enabled": false, "review_reasons": ["Synthetic-only evaluation; customer quality gate not met"]}, "conflicts": []}`

### RC1-0717767

```text
A ballot is available for eligible holders on the business in the circular.

Documentary proof of ownership is not required for the current vote.

Contact details for administrative enquiries appear in the service directory.

The custodian voting deadline was 15 September 2026 at 12:00 UTC.

A completed registration form must be delivered for the proxy vote.

Different voting choices cannot be assigned to portions of the same position.

Disclosure of the underlying investor’s identity is required for acceptance of votes.

The definitive instructions remove the preliminary requirement for a freeze on instructed securities.

The account currency does not change as a result of this notification.

Proxy directions are admissible only with the required attorney mandate.
```

- {"field": "other_voting_restriction", "truth": "NO", "prediction": "YES", "native_scores": {"YES": 0.9426, "NO": 0.056, "UNKNOWN": 0.0014}, "calibrated_correctness": null, "evidence": [], "conflict": null}

Decision/reconciliation: `{"decision": {"classification": "UNCERTAIN_MANUAL_REVIEW", "rule": "R1 unresolved conflicts", "rule_version": "semantic-decision-2", "manual_review_required": true, "automation_enabled": false, "review_reasons": ["share_blocking:SCOPED_EVIDENCE_CONFLICT_OR_CONDITION", "Synthetic-only evaluation; customer quality gate not met"]}, "conflicts": ["share_blocking:SCOPED_EVIDENCE_CONFLICT_OR_CONDITION"]}`

### RC1-0717769

```text
- Eligible holders have the right to vote on the resolutions listed in the current notice.
- Immobilisation of the voting shares is not required for the current vote.
- Account reconciliations are performed after the close of each business day.
- The holder is free to vote without arranging advance enrolment with the registrar.
- A restriction on dividing the votes is optional and is not a prerequisite for voting.
- Beneficial holders with lent shares must arrange their return before voting.
- The power of attorney is a mandatory document for this shareholder ballot.
- Custody fees are reported separately on the periodic account statement.
- Voting instructions must reach the custodian by 26 November 2026 at 16:00 UTC.
- Voting eligibility must be supported by a current ownership certificate.
```

- {"field": "other_voting_restriction", "truth": "NO", "prediction": "YES", "native_scores": {"YES": 0.9878, "NO": 0.0114, "UNKNOWN": 0.0008}, "calibrated_correctness": null, "evidence": [], "conflict": null}

Decision/reconciliation: `{"decision": {"classification": "VOTABLE_WITH_RESTRICTION", "rule": "R5 one or more voting restrictions", "rule_version": "semantic-decision-2", "manual_review_required": true, "automation_enabled": false, "review_reasons": ["Synthetic-only evaluation; customer quality gate not met"]}, "conflicts": []}`

### RC1-0717783

```text
- The nominee is accepting ballots on the resolutions at the upcoming annual assembly.
- The agent has not confirmed whether the recall of lent stock is compulsory for this ballot.
- The registrar requires the ultimate owner’s personal details before processing the ballot.
- Contact details for administrative enquiries appear in the service directory.
- Holders should keep a copy of any correspondence for their own records.
- A custodian-issued shareholding statement is compulsory for meeting participation.
- A nominee cannot divide its votes between different choices for the same resolution.
- An additional investor-eligibility restriction is optional and is not a prerequisite for voting.
- The custodian voting deadline was 15 September 2026 at 12:00 UTC.
- No ballot will be rejected because the holder has not arranged pre-registration for voting.
- The definitive instructions remove the preliminary requirement for an attorney mandate for voting.
```

- {"field": "beneficial_owner_disclosure_required", "truth": "YES", "prediction": "NO", "native_scores": {"YES": 0.0562, "NO": 0.9397, "UNKNOWN": 0.004}, "calibrated_correctness": null, "evidence": [], "conflict": null}

Decision/reconciliation: `{"decision": {"classification": "UNCERTAIN_MANUAL_REVIEW", "rule": "R1 unresolved conflicts", "rule_version": "semantic-decision-2", "manual_review_required": true, "automation_enabled": false, "review_reasons": ["poa_required:SCOPED_EVIDENCE_CONFLICT_OR_CONDITION", "registration_required:SCOPED_EVIDENCE_CONFLICT_OR_CONDITION", "Synthetic-only evaluation; customer quality gate not met"]}, "conflicts": ["poa_required:SCOPED_EVIDENCE_CONFLICT_OR_CONDITION", "registration_required:SCOPED_EVIDENCE_CONFLICT_OR_CONDITION"]}`

### RC1-0717946

```text
Voting on the auditor appointment is now available through the proxy service. Loaned shares are eligible only after a mandatory recall has settled. Disclosure of the ultimate investor’s identity is optional and is not a prerequisite for voting. The relevant annex is missing, leaving the condition concerning a power of attorney uncertain. The proxy instruction must carry a wet-ink signature; digital signatures are refused.
```

- {"field": "split_voting_restricted", "truth": "NO", "prediction": "YES", "native_scores": {"YES": 0.5253, "NO": 0.4707, "UNKNOWN": 0.004}, "calibrated_correctness": null, "evidence": [], "conflict": null}

Decision/reconciliation: `{"decision": {"classification": "VOTABLE_WITH_RESTRICTION", "rule": "R5 one or more voting restrictions", "rule_version": "semantic-decision-2", "manual_review_required": true, "automation_enabled": false, "review_reasons": ["Synthetic-only evaluation; customer quality gate not met"]}, "conflicts": []}`

### RC1-0717990

```text
You can direct the votes attached to the position shown on this meeting notification. The intermediary records timestamps when incoming documents are received. The current ballot is restricted to beneficial holders resident in the specified market. Voting representation depends on receipt of the signed power-of-attorney instrument. There is no requirement for a uniform-voting condition in the final terms. The voting form must identify the beneficial owner behind the custody account. Account reconciliations are performed after the close of each business day. We cannot establish from the available terms whether a custodian position confirmation applies.
```

- {"field": "other_voting_restriction", "truth": "YES", "prediction": "NO", "native_scores": {"YES": 0.0318, "NO": 0.9673, "UNKNOWN": 0.0009}, "calibrated_correctness": null, "evidence": [], "conflict": true}

Decision/reconciliation: `{"decision": {"classification": "UNCERTAIN_MANUAL_REVIEW", "rule": "R1 unresolved conflicts", "rule_version": "semantic-decision-2", "manual_review_required": true, "automation_enabled": false, "review_reasons": ["other_voting_restriction:SCOPED_EVIDENCE_CONFLICT_OR_CONDITION", "Synthetic-only evaluation; customer quality gate not met"]}, "conflicts": ["other_voting_restriction:SCOPED_EVIDENCE_CONFLICT_OR_CONDITION"]}`

### RC1-0718154

```text
Custody operations communication
These are historical proxy statistics for the preceding financial year.
Custody fees are reported separately on the periodic account statement.
The account currency does not change as a result of this notification.
Contact details for administrative enquiries appear in the service directory.
The registrar’s postal address is unchanged from the previous circular.
This communication is distributed through the usual securities-services channel.
Copies of the published accounts can be requested from the company secretary.
Account reconciliations are performed after the close of each business day.
Holders should keep a copy of any correspondence for their own records.
```

- {"field": "holding_confirmation_required", "truth": "NO", "prediction": "YES", "native_scores": {"YES": 0.992, "NO": 0.0078, "UNKNOWN": 0.0002}, "calibrated_correctness": null, "evidence": [], "conflict": null}

Decision/reconciliation: `{"decision": {"classification": "NOT_VOTABLE", "rule": "R2 no current voting opportunity", "rule_version": "semantic-decision-2", "manual_review_required": true, "automation_enabled": false, "review_reasons": ["Synthetic-only evaluation; customer quality gate not met"]}, "conflicts": []}`

### RC1-0718246

```text
- We can transmit your ballot to the tabulator for the announced meeting.
- The registrar’s postal address is unchanged from the previous circular.
- A nominee cannot divide its votes between different choices for the same resolution.
- Voting instructions must reach the custodian by 26 November 2026 at 16:00 UTC.
- This communication is distributed through the usual securities-services channel.
- Custody fees are reported separately on the periodic account statement.
- The registrar is still investigating the possible requirement for owner-name reporting.
- Copies of the published accounts can be requested from the company secretary.
- Routine settlement enquiries should quote the custody account reference.
- Electronic copies of account statements remain available through the portal.
- The registrar will reject the ballot unless the holder supplies a valid POA.
- An extra market-specific voting condition is optional and is not a prerequisite for voting.
- The custodian maintains an archive of notices for the reporting period.
- Account reconciliations are performed after the close of each business day.
- The agent expressly waives the recall of lent stock for this ballot.
- Lodging a ballot immobilises the voted position until the meeting concludes.
```

- {"field": "other_voting_restriction", "truth": "NO", "prediction": "YES", "native_scores": {"YES": 0.8928, "NO": 0.1, "UNKNOWN": 0.0072}, "calibrated_correctness": null, "evidence": [], "conflict": null}

Decision/reconciliation: `{"decision": {"classification": "VOTABLE_WITH_RESTRICTION", "rule": "R5 one or more voting restrictions", "rule_version": "semantic-decision-2", "manual_review_required": true, "automation_enabled": false, "review_reasons": ["Synthetic-only evaluation; customer quality gate not met"]}, "conflicts": []}`

### RC1-0718301

```text
Custody operations communication
The issuer is collecting shareholder votes on the acquisition agreement.
The beneficial owner must execute the power of attorney before votes can be accepted.
The agent expressly waives advance enrolment with the registrar for this ballot.
We cannot establish from the available terms whether a prohibition on split voting applies.
The relevant annex is missing, leaving the condition concerning documentary proof of ownership uncertain.
The voting service requires a recall of the relevant securities-lending positions.
The general market guide mentions a freeze on instructed securities, but this event is expressly exempt.
Voting instructions must reach the custodian by 26 November 2026 at 16:00 UTC.
```

- {"field": "beneficial_owner_disclosure_required", "truth": "NO", "prediction": "UNKNOWN", "native_scores": {"YES": 0.0016, "NO": 0.2271, "UNKNOWN": 0.7713}, "calibrated_correctness": null, "evidence": [], "conflict": null}

Decision/reconciliation: `{"decision": {"classification": "VOTABLE_WITH_RESTRICTION", "rule": "R5 one or more voting restrictions", "rule_version": "semantic-decision-2", "manual_review_required": true, "automation_enabled": false, "review_reasons": ["Synthetic-only evaluation; customer quality gate not met"]}, "conflicts": []}`

## CHALLENGE

### poa

```text
Beneficial owners wishing to vote must submit a valid power of attorney.
```

- {"field": "votability", "truth": "VOTABLE", "prediction": "NOT_VOTABLE", "native_scores": {"VOTABLE": 0.0316, "NOT_VOTABLE": 0.9684, "UNCERTAIN": 0.0001}, "calibrated_correctness": null, "evidence": [{"valid": true, "normalisation": "identity", "text": "Beneficial owners wishing to vote must submit a valid power of attorney.", "start": 0, "end": 72, "source": "SCOPED_SOURCE_CANDIDATE", "entailment_independently_verified": false}], "conflict": null}

Decision/reconciliation: `{"decision": {"classification": "NOT_VOTABLE", "rule": "R2 no current voting opportunity", "rule_version": "semantic-decision-2", "manual_review_required": true, "automation_enabled": false, "review_reasons": ["Synthetic-only evaluation; customer quality gate not met"]}, "conflicts": []}`

### ambiguous

```text
Please contact your custodian for information regarding possible participation.
```

- {"field": "classification", "truth": "UNCERTAIN_MANUAL_REVIEW", "prediction": "NOT_VOTABLE", "native_scores": null, "calibrated_correctness": null, "evidence": null, "conflict": null}
- {"field": "votability", "truth": "UNCERTAIN", "prediction": "NOT_VOTABLE", "native_scores": {"VOTABLE": 0.0, "NOT_VOTABLE": 1.0, "UNCERTAIN": 0.0}, "calibrated_correctness": null, "evidence": [], "conflict": null}

Decision/reconciliation: `{"decision": {"classification": "NOT_VOTABLE", "rule": "R2 no current voting opportunity", "rule_version": "semantic-decision-2", "manual_review_required": true, "automation_enabled": false, "review_reasons": ["Synthetic-only evaluation; customer quality gate not met"]}, "conflicts": []}`

### historical-results

```text
At last year’s AGM, 97% voted in favour of the remuneration policy. These are final historical results; no vote is currently open.
```

- {"field": "votability", "truth": "NOT_VOTABLE", "prediction": "UNCERTAIN", "native_scores": {"VOTABLE": 0.0001, "NOT_VOTABLE": 0.0001, "UNCERTAIN": 0.9999}, "calibrated_correctness": null, "evidence": [], "conflict": null}

Decision/reconciliation: `{"decision": {"classification": "UNCERTAIN_MANUAL_REVIEW", "rule": "R3 voting opportunity unresolved", "rule_version": "semantic-decision-2", "manual_review_required": true, "automation_enabled": false, "review_reasons": ["Synthetic-only evaluation; customer quality gate not met"]}, "conflicts": []}`

### legal-poa

```text
The borrower grants the security agent a power of attorney to enforce collateral. This loan agreement does not concern shareholder voting.
```

- {"field": "poa_required", "truth": "NO", "prediction": "YES", "native_scores": {"YES": 1.0, "NO": 0.0, "UNKNOWN": 0.0}, "calibrated_correctness": null, "evidence": [{"valid": true, "normalisation": "identity", "text": "The borrower grants the security agent a power of attorney to enforce collateral.", "start": 0, "end": 81, "source": "SCOPED_SOURCE_CANDIDATE", "entailment_independently_verified": false}], "conflict": null}

Decision/reconciliation: `{"decision": {"classification": "UNCERTAIN_MANUAL_REVIEW", "rule": "R1 unresolved conflicts", "rule_version": "semantic-decision-2", "manual_review_required": true, "automation_enabled": false, "review_reasons": ["securities_lending_recall_required:SCOPED_EVIDENCE_CONFLICT_OR_CONDITION", "Synthetic-only evaluation; customer quality gate not met"]}, "conflicts": ["securities_lending_recall_required:SCOPED_EVIDENCE_CONFLICT_OR_CONDITION"]}`

### eligibility

```text
Only holders of Class A shares may vote on resolution 3 at the EGM. Class B shares have no voting entitlement.
```

- {"field": "other_restriction", "truth": "YES", "prediction": "NO", "native_scores": null, "calibrated_correctness": null, "evidence": null, "conflict": null}

Decision/reconciliation: `{"decision": {"classification": "UNCERTAIN_MANUAL_REVIEW", "rule": "R7 deadline unresolved", "rule_version": "semantic-decision-2", "manual_review_required": true, "automation_enabled": false, "review_reasons": ["Synthetic-only evaluation; customer quality gate not met"]}, "conflicts": []}`

### contradiction

```text
Voting instructions are accepted. Voting instructions are not accepted. Both statements apply to the same meeting and no superseding notice is identified.
```

- {"field": "votability", "truth": "UNCERTAIN", "prediction": "NOT_VOTABLE", "native_scores": {"VOTABLE": 0.0001, "NOT_VOTABLE": 0.9689, "UNCERTAIN": 0.0311}, "calibrated_correctness": null, "evidence": [{"valid": true, "normalisation": "identity", "text": "Both statements apply to the same meeting and no superseding notice is identified.", "start": 72, "end": 154, "source": "SCOPED_SOURCE_CANDIDATE", "entailment_independently_verified": false}], "conflict": null}

Decision/reconciliation: `{"decision": {"classification": "NOT_VOTABLE", "rule": "R2 no current voting opportunity", "rule_version": "semantic-decision-2", "manual_review_required": true, "automation_enabled": false, "review_reasons": ["Synthetic-only evaluation; customer quality gate not met"]}, "conflicts": []}`

### same-day

```text
Vote at the AGM. Voting deadline: 16 October 2026, 17:00 Tokyo time. The reference supplies a date but no time.
```

- {"field": "deadline_status", "truth": "UNKNOWN", "prediction": "PASSED", "native_scores": null, "calibrated_correctness": null, "evidence": null, "conflict": null}

Decision/reconciliation: `{"decision": {"classification": "DEADLINE_PASSED", "rule": "R4 controlling deadline passed", "rule_version": "semantic-decision-2", "manual_review_required": true, "automation_enabled": false, "review_reasons": ["Synthetic-only evaluation; customer quality gate not met"]}, "conflicts": []}`

### poa-waived

```text
A POA was required last year. This year that requirement has been waived for all beneficial owners voting at the AGM.
```

- {"field": "votability", "truth": "VOTABLE", "prediction": "NOT_VOTABLE", "native_scores": {"VOTABLE": 0.0076, "NOT_VOTABLE": 0.9924, "UNCERTAIN": 0.0}, "calibrated_correctness": null, "evidence": [{"valid": true, "normalisation": "identity", "text": "This year that requirement has been waived for all beneficial owners voting at the AGM.", "start": 30, "end": 117, "source": "SCOPED_SOURCE_CANDIDATE", "entailment_independently_verified": false}], "conflict": null}

Decision/reconciliation: `{"decision": {"classification": "NOT_VOTABLE", "rule": "R2 no current voting opportunity", "rule_version": "semantic-decision-2", "manual_review_required": true, "automation_enabled": false, "review_reasons": ["Synthetic-only evaluation; customer quality gate not met"]}, "conflicts": []}`

### blocking-waived

```text
Share blocking is no longer required for the current shareholder vote.
```

- {"field": "votability", "truth": "VOTABLE", "prediction": "NOT_VOTABLE", "native_scores": {"VOTABLE": 0.0, "NOT_VOTABLE": 1.0, "UNCERTAIN": 0.0}, "calibrated_correctness": null, "evidence": [{"valid": true, "normalisation": "identity", "text": "Share blocking is no longer required for the current shareholder vote.", "start": 0, "end": 70, "source": "SCOPED_SOURCE_CANDIDATE", "entailment_independently_verified": false}], "conflict": null}

Decision/reconciliation: `{"decision": {"classification": "NOT_VOTABLE", "rule": "R2 no current voting opportunity", "rule_version": "semantic-decision-2", "manual_review_required": true, "automation_enabled": false, "review_reasons": ["Synthetic-only evaluation; customer quality gate not met"]}, "conflicts": []}`

### sell-restricted

```text
Holders submitting voting instructions may not sell their shares until after the EGM.
```

- {"field": "share_blocking", "truth": "YES", "prediction": "NO", "native_scores": {"YES": 0.0, "NO": 1.0, "UNKNOWN": 0.0}, "calibrated_correctness": null, "evidence": [], "conflict": null}

Decision/reconciliation: `{"decision": {"classification": "UNCERTAIN_MANUAL_REVIEW", "rule": "R7 deadline unresolved", "rule_version": "semantic-decision-2", "manual_review_required": true, "automation_enabled": false, "review_reasons": ["Synthetic-only evaluation; customer quality gate not met"]}, "conflicts": []}`

### de-vote

```text
Aktionäre können ihre Stimmrechte auf der Hauptversammlung ausüben und Weisungen zur Stimmabgabe einreichen.
```

- {"field": "votability", "truth": "VOTABLE", "prediction": "NOT_VOTABLE", "native_scores": {"VOTABLE": 0.0, "NOT_VOTABLE": 0.9999, "UNCERTAIN": 0.0}, "calibrated_correctness": null, "evidence": [], "conflict": null}

Decision/reconciliation: `{"decision": {"classification": "NOT_VOTABLE", "rule": "R2 no current voting opportunity", "rule_version": "semantic-decision-2", "manual_review_required": true, "automation_enabled": false, "review_reasons": ["Synthetic-only evaluation; customer quality gate not met"]}, "conflicts": []}`

### fr-poa

```text
Les bénéficiaires souhaitant voter à l’assemblée doivent fournir une procuration notariée obligatoire.
```

- {"field": "poa_required", "truth": "YES", "prediction": "NO", "native_scores": {"YES": 0.0, "NO": 1.0, "UNKNOWN": 0.0}, "calibrated_correctness": null, "evidence": [], "conflict": null}

Decision/reconciliation: `{"decision": {"classification": "UNCERTAIN_MANUAL_REVIEW", "rule": "R7 deadline unresolved", "rule_version": "semantic-decision-2", "manual_review_required": true, "automation_enabled": false, "review_reasons": ["Synthetic-only evaluation; customer quality gate not met"]}, "conflicts": []}`

### de-no-block

```text
Aktionäre dürfen abstimmen. Eine Sperrung der Aktien ist nicht erforderlich.
```

- {"field": "votability", "truth": "VOTABLE", "prediction": "NOT_VOTABLE", "native_scores": {"VOTABLE": 0.0, "NOT_VOTABLE": 1.0, "UNCERTAIN": 0.0}, "calibrated_correctness": null, "evidence": [], "conflict": null}

Decision/reconciliation: `{"decision": {"classification": "NOT_VOTABLE", "rule": "R2 no current voting opportunity", "rule_version": "semantic-decision-2", "manual_review_required": true, "automation_enabled": false, "review_reasons": ["Synthetic-only evaluation; customer quality gate not met"]}, "conflicts": []}`

### foreign-restriction

```text
Foreign shareholders may vote only after obtaining local regulatory permission; domestic holders may vote freely.
```

- {"field": "other_restriction", "truth": "YES", "prediction": "NO", "native_scores": null, "calibrated_correctness": null, "evidence": null, "conflict": null}

Decision/reconciliation: `{"decision": {"classification": "UNCERTAIN_MANUAL_REVIEW", "rule": "R7 deadline unresolved", "rule_version": "semantic-decision-2", "manual_review_required": true, "automation_enabled": false, "review_reasons": ["Synthetic-only evaluation; customer quality gate not met"]}, "conflicts": []}`

### blank-like

```text
Meeting: TBD. Participation: TBD. Voting: TBD.
```

- {"field": "votability", "truth": "UNCERTAIN", "prediction": "NOT_VOTABLE", "native_scores": {"VOTABLE": 0.0034, "NOT_VOTABLE": 0.813, "UNCERTAIN": 0.1836}, "calibrated_correctness": null, "evidence": [{"valid": true, "normalisation": "identity", "text": "Voting: TBD.", "start": 34, "end": 46, "source": "SCOPED_SOURCE_CANDIDATE", "entailment_independently_verified": false}], "conflict": null}

Decision/reconciliation: `{"decision": {"classification": "NOT_VOTABLE", "rule": "R2 no current voting opportunity", "rule_version": "semantic-decision-2", "manual_review_required": true, "automation_enabled": false, "review_reasons": ["Synthetic-only evaluation; customer quality gate not met"]}, "conflicts": []}`

