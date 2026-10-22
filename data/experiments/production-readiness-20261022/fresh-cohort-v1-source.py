"""Private fact-first qualification material, excluded from customer delivery.

No challenge/test failure is read by this generator. New phrasing is segregated
by role. Composition/lexical groups do not establish independent human truth.
"""
import random
from collections import Counter
from pathlib import Path
from classifier.preprocessing import source_hash
from classifier.deadlines import extract_deadline
from semantic_pipeline.schema import PREDICATES, RESTRICTIONS, SemanticResult
from semantic_pipeline.decision import decide
from training.split import duplicate_groups
from training.framework.bundle import write, jsonl, sha

VERSION = 'fresh-evidence-cohort-v1'
REFERENCE = '2026-10-22T12:00:00+00:00'
# Each column is authored separately, then permanently assigned to a role.
# Predicate names are necessarily shared; source sentences are role-specific.
SUBJECTS = {
 'share_blocking': ('Blocking of the voted securities', 'Immobilisation of instructed stock', 'A freeze on selling the shares used to vote'),
 'poa_required': ('Delivery of a power-of-attorney instrument', 'A signed POA from the beneficial holder', 'The beneficial owner\'s power of attorney'),
 'registration_required': ('Advance registration for voting', 'Enrolment of the voting holder', 'Pre-registration of the person casting the ballot'),
 'beneficial_owner_disclosure_required': ('Disclosure of the beneficial owner\'s identity', 'Submission of beneficial-owner identification', 'Providing the ultimate holder\'s identity'),
 'holding_confirmation_required': ('A certificate confirming the holding', 'Proof of ownership of the voting position', 'An ownership confirmation from the custodian'),
 'split_voting_restricted': ('A prohibition on splitting votes between opposing directions', 'A restriction requiring one direction for all votes', 'A ban on dividing the position between voting choices'),
 'securities_lending_recall_required': ('Recall of securities on loan before voting', 'Retrieval of lent shares to exercise the vote', 'Recalling the voting securities from the borrower'),
 'other_voting_restriction': ('A minimum holding of 500 shares to exercise voting rights', 'Professional-investor eligibility as a condition of voting', 'A residency eligibility condition for casting votes'),
}
VOTES = {
 'VOTABLE': ('The current meeting accepts shareholder votes on the resolutions.',
             'This is an invitation for holders to cast ballots at the forthcoming AGM.',
             'Beneficial holders have a current right to instruct votes at this general meeting.'),
 'NOT_VOTABLE': ('This cash distribution is automatic; there is no shareholder ballot.',
                 'This payment advice is informational and offers no voting opportunity.',
                 'The notice concerns a redemption payment, with no meeting or vote to instruct.'),
 'UNCERTAIN': ('The communication does not establish whether shareholders can vote.',
               'Operations cannot determine from this preliminary advice whether voting is available.',
               'Possible participation is mentioned, but the existence of a voting opportunity is unresolved.'),
}
FORMS = {
 'YES': ('{s} is mandatory for this vote.', '{s} is a prerequisite for valid voting instructions.',
         'Voting instructions will be rejected unless the following condition is met: {s}.'),
 'NO': ('{s} is expressly not required for this vote.', '{s} is unnecessary for the current voting service.',
        'The voting service imposes no requirement for {s}.'),
 'OPTIONAL': ('{s} is available voluntarily and is not a voting prerequisite.',
              'Holders may choose {s}; exercising votes does not depend on that choice.',
              'Clients can opt for {s}, but their votes remain valid without it.'),
 'UNKNOWN': ('The requirement for {s} is unresolved; obtain confirmation before proceeding.',
             'Whether {s} applies to this vote has not yet been established.',
             'The source provides no definitive answer about the applicability of {s}.'),
}


def make(index, role):
    column = ('VALIDATION','CALIBRATION','FROZEN_TEST').index(role)
    rng = random.Random(8820100 + index + column * 10000)
    vote = rng.choices(list(VOTES), [.75,.18,.07])[0]
    facts = {k:'NO' for k in RESTRICTIONS}; facts['votability']=vote
    intro = VOTES[vote][column]; parts=[intro]; ev={k:[] for k in PREDICATES}; ev['votability']=[intro]
    specifications={}
    if vote=='VOTABLE':
        active=rng.sample(list(RESTRICTIONS), rng.choice([1,2,3,4]))
        for key in RESTRICTIONS:
            state=rng.choices(['YES','NO','OPTIONAL','UNKNOWN'],[.65,.15,.15,.05])[0] if key in active else rng.choice(['NO','OPTIONAL'])
            facts[key]='NO' if state=='OPTIONAL' else state
            subject=SUBJECTS[key][column]; clause=FORMS[state][column].format(s=subject)
            # Separating fields prevents an unrelated negative from changing
            # another predicate; prose still has to be interpreted by the model.
            parts.append(clause); ev[key]=[clause]; specifications[key]=state
        deadline_status='PASSED' if rng.random()<.15 else 'OPEN'
        deadline=('The custodian voting deadline was 15 September 2026 at 12:00 UTC.' if deadline_status=='PASSED'
                  else 'Voting instructions must reach the custodian by 26 November 2026 at 16:00 UTC.')
        parts.append(deadline)
    else: deadline_status='UNKNOWN'; deadline=None
    # Facts precede text. No model infers the label from arbitrary generated prose.
    rest=parts[1:];rng.shuffle(rest)
    text=intro+'\n\n'+'\n'.join(rest)
    target={**facts,'deadline_information':{'deadline_mentioned':bool(deadline),'deadline_text':deadline},
            'evidence':ev,'ambiguities':[]}
    SemanticResult.model_validate(target)
    if any(q not in text for quotes in ev.values() for q in quotes):raise ValueError('Evidence construction drift')
    assert extract_deadline(text,REFERENCE)['status']==deadline_status
    final=decide({k:{'value':facts[k]} for k in PREDICATES},{'status':deadline_status})['classification']
    return {'id':f'FE1-{role}-{index:05d}','role':role,'text':text,'source_hash':source_hash(text),
            'expected':facts,'final_status':final,'deadline_status':deadline_status,'target':target,
            'evaluation_time':REFERENCE,'language':'en','origin':'AI_AUTHORED','generator_model':'Codex/GPT-6',
            'prompt_version':VERSION,'fact_specification':specifications,'generation_family':VERSION+'-'+role,
            'source_type':'AI_AUTHORED_FACT_FIRST_CONTROLLED_COMPOSITION'}


def build(output, counts=None):
    root=Path(output);root.mkdir(parents=True,exist_ok=False)
    counts=counts or {'VALIDATION':160,'CALIBRATION':360,'FROZEN_TEST':240}
    rows=[make(i,role) for role,count in counts.items() for i in range(count)]
    groups=duplicate_groups(rows); memberships={}
    for row,group in zip(rows,groups):memberships.setdefault(group,set()).add(row['role'])
    # Drop entire components crossing roles instead of weakening isolation.
    cross={g for g,roles in memberships.items() if len(roles)>1}
    kept=[]
    for row,group in zip(rows,groups):
        if group in cross:continue
        row['group']=group
        row['fold']='EVALUATION' if int(source_hash('fold-'+group)[:8],16)%3==0 else 'FIT'
        kept.append(row)
    manifest={'version':VERSION,'reference':REFERENCE,'source_sha256':sha(__file__),'files':{},
              'original_count':len(rows),'count':len(kept),'cross_role_components_excluded':len(cross),
              'unique_text_hashes':len({r['source_hash'] for r in kept}),
              'groups':len({r['group'] for r in kept}),'label_origin':'AI_AUTHORED',
              'limitations':['One separately authored linguistic column per role; controlled phrasing, not broad linguistic diversity.',
                            'Compositional/lexical groups are not independent human-labelled families.',
                            'English only; two controlled date formulations; not customer accuracy or a production certificate.'],
              'automation_enabled':False,'customer_accuracy':None}
    for role in counts:
        selected=[r for r in kept if r['role']==role]
        key=root/('private' if role=='FROZEN_TEST' else 'development')/(role+'.labels.jsonl')
        key.parent.mkdir(exist_ok=True); source=root/(role+'.inputs.jsonl')
        jsonl(source,[{k:r[k] for k in ('id','role','text','source_hash','evaluation_time','language','group','fold')} for r in selected])
        jsonl(key,selected)
        manifest['files'][role]={'inputs':source.name,'inputs_sha256':sha(source),'labels':str(key.relative_to(root)),
            'labels_sha256':sha(key),'n':len(selected),'groups':len({r['group'] for r in selected}),
            'labels_by_field':{k:dict(Counter(r['expected'][k] for r in selected)) for k in PREDICATES}}
    write(root/'manifest.json',manifest);return manifest
