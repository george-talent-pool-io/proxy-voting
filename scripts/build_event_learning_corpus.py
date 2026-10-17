"""Fact-first engineering corpus, NOT representative production training data.

20 explicit linguistic families × 8 semantic combinations. All variants of a
family and all detected lexical duplicates are grouped before role assignment.
Old terms are intentionally different; only the replacement epoch is labelled.
"""
import argparse
import json
from pathlib import Path

from classifier.preprocessing import source_hash
from iso_adapter.benchmark import fin
from semantic_pipeline.schema import PREDICATES, RESTRICTIONS
from training.framework import events, event_data, jobs
from training.framework.bundle import write

AUTHOR = 'GPT-6 / Codex; AI-authored deterministic fact-first generator'
VERSION = 'event-learning-construction-v1'
INTRO = [
    'Custody operations circular. Please reconcile the enclosed voting entitlement against the account register.',
    'Issuer secretariat memorandum concerning arrangements for the forthcoming extraordinary assembly.',
    'Broker service update: the institutional ballot channel is now available for this agenda.',
    'Depository participant bulletin. Instructions for the special general meeting follow below.',
    'Legal notice to registered members: procedural conditions for participation are set out in this communication.',
    'Settlement desk handover note. This entry concerns a class meeting rather than a distribution election.',
    'Operational email from the proxy team. We have completed the processing arrangements described below.',
    'Registrar information sheet, extracted from the meeting administration pack. Please retain this version.',
    'Client account advice regarding the scheme meeting. The receiving agent uses the following participation process.',
    'Nominee-bank instruction sheet. Read the current conditions before transmitting the relevant ballot.',
    'Meeting services announcement for beneficial holders. The workflow in this announcement is operative.',
    'Revised corporate-secretary communication. The final participation terms are reproduced for account operators.',
    'Intermediary processing checklist. The assembly is administered under the account procedures below.',
    'Corporate actions desk message. Agenda participation and account documentation are described in the current extract.',
    'Voting-agent reply to custody queries. These statements replace the earlier provisional operating advice.',
    'Participant support notice. Apply the revised owner instructions rather than the preliminary meeting pack.',
    'Administrative appendix to the shareholder circular. The clauses below specify the current response channel.',
    'Service provider case note. Final arrangements have been confirmed for the investor participation process.',
    'Institutional proxy-processing summary. Account operators should use this replacement edition.',
    'Company meeting helpdesk correspondence. This message records the final instructions delivered to nominees.',
]
NAMES = {
    'share_blocking': ('share blocking', 'voting-related immobilisation', 'a voting lock on the position', 'blocking of instructed shares'),
    'poa_required': ('a mandatory power of attorney', 'a notarised voting authority', 'an obligatory power-of-attorney document', 'a compulsory attorney mandate'),
    'registration_required': ('mandatory meeting registration', 'advance enrolment for voting', 'compulsory participant registration', 'a required voter registration form'),
    'beneficial_owner_disclosure_required': ('beneficial-owner disclosure', 'identification of the underlying owner', 'a beneficial-holder identity declaration', 'disclosure of the ultimate investor'),
    'holding_confirmation_required': ('a holdings certificate', 'documentary confirmation of ownership', 'a custodial holding statement', 'proof of the held position'),
    'split_voting_restricted': ('a prohibition on split voting', 'a restriction on dividing the ballot', 'a ban on splitting voting instructions', 'a requirement to cast all votes identically'),
    'securities_lending_recall_required': ('recall of lent securities', 'return of shares on loan before voting', 'a mandatory stock-loan recall', 'retrieval of loaned voting positions'),
    'other_voting_restriction': ('a mandatory paper-only ballot', 'an in-person-only voting condition', 'a compulsory original wet-signature ballot', 'a prohibition on electronic voting'),
}


def message(seme, corp, function, narrative, *, mt='MT564', prev=None, voting=True, date='20261124170000'):
    header = f':16R:GENL\n:20C::SEME//{seme}\n:20C::CORP//{corp}\n'
    if prev: header += f':20C::PREV//{prev}\n'
    header += f':23G:{function}\n'
    if mt == 'MT564': header += ':22F::CAEV//' + ('MEET' if voting else 'DVCA') + '\n'
    header += ':16S:GENL\n'
    if mt == 'MT564':
        header += ':16R:CAOPTN\n:13A::CAON//001\n'
        if voting: header += ':22F::CAOP//PROX\n'
        header += f':98E::RDDT//{date},000/00\n:16S:CAOPTN\n'
    raw = fin(header + ':16R:ADDINFO\n:70E::ADTX//' + narrative + '\n:16S:ADDINFO')
    return raw.replace('{2:I564', '{2:I' + mt[2:])


def specification(family, variant):
    vote = 'NOT_VOTABLE' if variant == 6 else 'UNCERTAIN' if variant == 7 else 'VOTABLE'
    voting = [
        'Shareholders can submit a ballot on the resolutions at this meeting.',
        'The current agenda is open for shareholder voting instructions.',
        'Eligible members may exercise their votes through the proxy service.',
        'A live voting opportunity exists for owners responding to this assembly.',
    ][family % 4] if vote == 'VOTABLE' else (
        'This is solely a cash-distribution advice; it offers no meeting ballot and no shareholder vote.' if vote == 'NOT_VOTABLE' else
        'Participation may become possible, but the agent has not established whether this holder can vote.')
    clauses = [INTRO[family], voting]; target = {'votability': vote}; evidence = {'votability': [voting]}
    for i, key in enumerate(RESTRICTIONS):
        label = 'NO' if variant in (0, 6) else 'UNKNOWN' if (variant == 7 and i == family % 8) else 'YES' if (i + variant + family) % 4 == 0 else 'NO'
        name = NAMES[key][(family + i) % 4]
        if label == 'YES':
            phrase = [f'For this vote, {name} is required.', f'To exercise the ballot, the holder must comply with {name}.',
                      f'The current voting route is conditional upon {name}.', f'Participation in this vote requires {name}.'][(family // 4) % 4]
        elif label == 'UNKNOWN':
            phrase = f'The receiving agent has not resolved whether {name} is required for this vote.'
        else:
            phrase = [f'No requirement for {name} applies.', f'The operator expressly waives {name}.',
                      f'{name.capitalize()} is not required under these terms.', f'This route imposes no obligation concerning {name}.'][(family // 4) % 4]
        target[key] = label; evidence[key] = [phrase]; clauses.append(phrase)
    deadline = 'PASSED' if variant == 4 else 'OPEN'
    target.update(evidence=evidence, deadline_information={'deadline_mentioned': False, 'deadline_text': None}, ambiguities=[])
    from semantic_pipeline.decision import decide
    status = decide({k: {'value': target[k]} for k in PREDICATES}, {'status': deadline})['classification']
    return {'narrative': '\n'.join(clauses), 'target': target, 'deadline': deadline,
            'final_status': status, 'voting_option': vote == 'VOTABLE'}


def build(database, output, *, workspace=None):
    if workspace is not None: jobs.WORKSPACE = Path(workspace).resolve()
    # Partition complete connected families, including near-duplicate edges.
    specs = [(f, v, specification(f, v)) for f in range(20) for v in range(8)]
    from training.split import duplicate_groups
    groups = duplicate_groups([{'text': s['narrative']} for _, _, s in specs])
    parent = list(range(20))
    def find(i):
        while parent[i] != i: i = parent[i]
        return i
    seen = {}
    for (f, _, _), group in zip(specs, groups):
        if group in seen:
            a, b = find(f), find(seen[group]); parent[max(a, b)] = min(a, b)
        seen[group] = f
    units = sorted({find(f) for f in range(20)}, key=lambda f: source_hash(VERSION + ':' + str(f)))
    if len(units) < 8: raise ValueError('Too few independent generation families; diversify before splitting')
    roles = {u: 'FROZEN_TEST' if i < 2 else 'CALIBRATION' if i < 4 else 'VALIDATION' if i < 8 else 'TRAIN' for i, u in enumerate(units)}
    receipt = []
    for family, variant, spec in specs:
        identity = f'EL{family:02d}{variant:02d}'; corp = identity + 'CORP'; split = roles[find(family)]
        attrs = {'sender': 'SYNTHETIC-LEARNING-DESK', 'source_type': 'STANDARDS_DERIVED_SYNTHETIC',
                 'group_id': f'{VERSION}-group-{find(family)}', 'family': f'{VERSION}-family-{find(family)}',
                 'split': split, 'source_reference': f'{VERSION}; facts-first; authored by {AUTHOR}', 'database': database}
        old = identity + 'A'; supplement = identity + 'B'; replacement = identity + 'C'; addendum = identity + 'D'
        events.ingest(message(old, corp, 'NEWM', 'Provisional terms: shares will be blocked until the meeting.', date='20250901170000'), **attrs)
        events.ingest(message(supplement, corp, 'NEWM', 'This preliminary supplement belongs to the old notification and is not current after replacement.', mt='MT568', prev=old), **attrs)
        r = events.ingest(message(replacement, corp, 'REPL', spec['narrative'], prev=old,
                                 voting=spec['voting_option'], date='20250901170000' if spec['deadline'] == 'PASSED' else '20261124170000'), **attrs)
        events.ingest(message(addendum, corp, 'NEWM', 'Please retain the replacement edition for operational reconciliation. Earlier notification conditions are superseded.', mt='MT568', prev=replacement), **attrs)
        current = events.get(r['event_id'], database)
        prior = [review for review in current['reviews'] if review['snapshot_hash'] == current['snapshot_hash']]
        if prior and prior[-1]['payload']['target'] != spec['target']:
            raise ValueError('Existing review differs from construction facts; preserve it and use a fresh corpus namespace/database')
        review = prior[-1] if prior else events.review(r['event_id'], {
            'snapshot_hash': current['snapshot_hash'], 'target': spec['target'],
            'expected_deadline_status': spec['deadline'], 'expected_final_status': spec['final_status'],
            'provenance': {'origin': 'AI_AUTHORED', 'author': AUTHOR, 'model_id': 'GPT-6 / Codex',
                           'method': 'Fact-first finite grammar construction; no independent expert review',
                           'source_reference': VERSION, 'revision': VERSION},
            'notes': 'Engineering fixture; not customer data, not a human/expert golden label.'}, database)
        receipt.append({'event_id': r['event_id'], 'split': split, 'review_revision': review['id'],
                        'fact_specification': spec['target'], 'generation_family': attrs['family']})
    manifest = event_data.freeze_dataset(output, database)
    # Construction facts remain beside the protected keys, never a training source.
    write(Path(output) / 'private/construction.json', {'generator': AUTHOR, 'version': VERSION, 'events': receipt})
    return manifest


if __name__ == '__main__':
    p = argparse.ArgumentParser(); p.add_argument('--database', required=True); p.add_argument('--output', required=True); p.add_argument('--workspace')
    a = p.parse_args(); print(json.dumps(build(a.database, a.output, workspace=a.workspace), indent=2))
