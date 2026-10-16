"""Separately authored synthetic evaluation material; NEVER model-training data.
Every factor is labelled under the explicit 'not stated = NO' notice-level policy.
These are controlled examples, not expert-reviewed customer truth.
"""
from semantic_pipeline.schema import RESTRICTIONS
from semantic_pipeline.decision import decide
from semantic_pipeline.models import factor

# Distinct language per condition, including current negations and supersession.
CONDITIONS = {
'share_blocking': [
 ('The custodian will immobilise the instructed position until the poll concludes; transfers from that position cannot settle.', 'YES'),
 ('Sending us a ballot does not immobilise the position, and trading can continue throughout the poll.', 'NO'),
 ('A prior circular anticipated immobilisation. The definitive circular withdraws that term and permits unrestricted transfers after a ballot is lodged.', 'NO')],
'poa_required': [
 ('An executed power-of-attorney instrument must reach the agent before it will accept an owner\'s ballot.', 'YES'),
 ('Appointment of our optional proxy service is available; a power-of-attorney instrument is expressly unnecessary for voting.', 'NO'),
 ('The draft requested an attorney authorisation. The operative amendment waives the power-of-attorney document for this ballot.', 'NO')],
'registration_required': [
 ('Before lodging a ballot, the holder must first enrol its shares on the temporary participation register.', 'YES'),
 ('Registration of shareholders for the poll has been waived; we accept ballots without enrolment.', 'NO'),
 ('The preliminary enrolment requirement is superseded. Under the final terms holders submit ballots directly without registration.', 'NO')],
'beneficial_owner_disclosure_required': [
 ('Anonymous omnibus ballots will be rejected: the underlying beneficial owners\' identities must accompany the voting file.', 'YES'),
 ('Omnibus voting is accepted anonymously; disclosing the identity of the underlying beneficial owners is not a voting condition.', 'NO'),
 ('Names of underlying owners were requested in an earlier draft. The definitive instructions remove that disclosure requirement.', 'NO')],
'holding_confirmation_required': [
 ('Attach a dated custody certificate confirming the quantity held; ballots without that proof of ownership will be rejected.', 'YES'),
 ('No custody certificate or ownership confirmation needs to be attached to the ballot.', 'NO'),
 ('An ownership certificate was initially envisaged. The revised terms eliminate documentary proof of holdings for this vote.', 'NO')],
'split_voting_restricted': [
 ('An omnibus position must cast all shares identically; splitting votes among the resolutions\' alternatives is prohibited.', 'YES'),
 ('The nominee may split its voting position freely between votes for, against and abstentions.', 'NO'),
 ('Earlier instructions disallowed split ballots. The final amendment now permits the nominee to divide votes without limitation.', 'NO')],
'securities_lending_recall_required': [
 ('For this poll, an owner with securities out on loan must recall them before its ballot can be accepted.', 'YES'),
 ('Owners need not recall their securities loans as a condition of this ballot; the notice imposes no lending-recall requirement.', 'NO'),
 ('A preliminary loan-recall requirement is withdrawn. The final participation terms expressly waive recalling lent securities.', 'NO')],
'other_voting_restriction': [
 ('Only holders resident in the eligible jurisdiction may cast ballots in this class poll; nonresident holders are excluded.', 'YES'),
 ('Residency, minimum position size and notarisation impose no additional conditions on this vote.', 'NO'),
 ('The preliminary rules imposed a minimum position size for voting. That eligibility condition has been removed by the definitive circular.', 'NO')],
}

def build():
    records=[]
    def add(text, values=None, vote='VOTABLE', deadline='OPEN', kind='UNSTRUCTURED', note=''):
        expected={'votability':vote,**{k:'NO' for k in RESTRICTIONS},'deadline_status':deadline}
        expected.update(values or {})
        fs={k:factor(expected[k],'SYNTHETIC_TRUTH') for k in ('votability',)+RESTRICTIONS}
        expected['classification']=decide(fs,{'status':deadline})['classification']
        records.append({'id':f'COMPLETE-{len(records)+1:03d}','text':text,'expected':expected,
            'source_type':'SYNTHETIC_COMPLETE_BENCHMARK','input_kind':kind,
            'notes':note,'reference_date':'2026-10-16','language':'en'})
    for key,items in CONDITIONS.items():
        for i,(sentence,value) in enumerate(items):
            # Three broad contexts, not copied from challenge text or training templates.
            intro=['Ballots are invited for the holders\' class meeting concerning the proposed combination.',
                   'The agent is collecting proxy ballots for the forthcoming extraordinary meeting.',
                   'The revised circular invites the registered owners to exercise their voting rights.'][i]
            add(intro+' '+sentence+' Custodian cutoff for voting instructions: submit by 24 November 2026.',{key:value})
    # Independent combined conditions and operational distinctions.
    add('Vote on the merger resolutions by returning the ballot. The nominee must disclose every underlying owner and attach a holdings certificate. Voting instructions are due by 27 November 2026.',{'beneficial_owner_disclosure_required':'YES','holding_confirmation_required':'YES'})
    add('Proxy ballots for the class meeting must be accompanied by a power of attorney. Instructed shares cannot be transferred until the poll finishes. Custodian deadline: 29 November 2026.',{'poa_required':'YES','share_blocking':'YES'})
    add('The trustee invites votes on the scheme. Enrol the holder in the participation register and return any securities loans before voting. Instructions are due by 26 November 2026.',{'registration_required':'YES','securities_lending_recall_required':'YES'})
    add('The share class may vote in the scheme poll. A notarised signature on each ballot is compulsory and split voting is forbidden. Instructions are due by 23 November 2026.',{'other_voting_restriction':'YES','split_voting_restricted':'YES'})
    add('The nominee may send proxy ballots. Ownership on the normal record date determines entitlement, but does not prevent selling shares afterwards. Voting instructions are due by 22 November 2026.')
    add('Owners may cast proxy votes. Lending positions must be recalled to vote, but submitting the ballot never blocks transfers. Custodian deadline: 21 November 2026.',{'securities_lending_recall_required':'YES'})
    add('The circular offers cash or new shares in a mandatory distribution. Your election concerns the consideration only; there is no meeting, proxy ballot or vote.',vote='NOT_VOTABLE',deadline='UNKNOWN')
    add('This exchange offer permits tendering securities for cancellation. Tender instructions are not shareholder votes and no proxy opportunity is offered.',vote='NOT_VOTABLE',deadline='UNKNOWN')
    add('Notice of the published poll results: the concluded annual meeting approved every resolution. This document offers no current ballot or voting instruction.',vote='NOT_VOTABLE',deadline='UNKNOWN')
    add('Coupon payment advice. The account will be credited automatically and the instrument holders have no voting decision in this announcement.',vote='NOT_VOTABLE',deadline='UNKNOWN')
    add('Participation arrangements are under discussion. We cannot yet confirm whether owners will be offered a ballot or only attendance.',vote='UNCERTAIN',deadline='UNKNOWN')
    add('The attachment allegedly describes a shareholder poll but it is missing. Contact operations to establish whether this communication offers any voting right.',vote='UNCERTAIN',deadline='UNKNOWN')
    add('Owners may return proxy ballots. The current instruction sheet requires an attorney document; the accompanying equally current instructions say no power of attorney is needed. Neither is designated as superseding the other. Voting instructions are due by 20 November 2026.',{'poa_required':'UNKNOWN'})
    add('The class is invited to vote. The current cover note prohibits transfers of instructed holdings, but its current annex explicitly allows all transfers after instruction. Neither document has priority. Custodian deadline: 20 November 2026.',{'share_blocking':'UNKNOWN'})
    add('Owners could lodge ballots for the current class meeting. Voting instructions were due by 4 September 2026.',deadline='PASSED')
    add('A ballot is available for the extraordinary meeting scheduled in December. Voting instructions are due by 14 October 2026.',deadline='PASSED')
    # Eight standards-derived partial messages: no claim of production-message validity.
    for i,key in enumerate(RESTRICTIONS):
        narrative='Holders may submit a proxy ballot for this class meeting. '+CONDITIONS[key][0][0]
        raw=f'{{1:F01TESTGB2LXXXX0000000000}}{{2:I564TESTGB2LXXXXN}}{{4:\n:16R:GENL\n:20C::SEME//COMP{i:03d}\n:20C::CORP//CMEET{i:03d}\n:23G:NEWM\n:22F::CAEV//MEET\n:16S:GENL\n:16R:CADETL\n:98E::RDDT//20261124170000/0000\n:70E::ADTX//{narrative}\n:16S:CADETL\n:16R:CAOPTN\n:13A::CAON//001\n:22F::CAOP//PROX\n:16S:CAOPTN\n-}}'
        add(raw,{key:'YES'},kind='STANDARDS_DERIVED_PARTIAL_ISO15022',note='Grammar subset previously researched; synthetic and partial, not a FIN conformance reference.')
    return records
