"""Predeclared synthetic routing/aggregation validation, never model training.
Authored from predicate definitions and general contrasts, not challenge failures.
"""
from semantic_pipeline.schema import PREDICATES,RESTRICTIONS
from semantic_pipeline.decision import decide
PHRASES={
 'share_blocking':('shares will be blocked until the meeting closes','shares will not be blocked'),
 'poa_required':('a notarised power of attorney is required for voting','no power of attorney is required'),
 'registration_required':('registration of the holder is mandatory before voting','registration is not required'),
 'beneficial_owner_disclosure_required':('beneficial owner identity disclosure is a mandatory voting condition','no beneficial owner identity disclosure is required'),
 'holding_confirmation_required':('proof of holdings must accompany voting instructions','proof of holdings is not required'),
 'split_voting_restricted':('split voting is prohibited and all shares must vote identically','split voting is not restricted'),
 'securities_lending_recall_required':('loaned securities must be recalled to exercise voting rights','securities lending recall is not required for voting'),
 'other_voting_restriction':('only licensed professional investors are eligible to vote under an additional restriction','no additional voting restriction applies'),
}
CONTEXTS=[
 'Operations circular for a company meeting. Shareholders can return voting instructions through their custodian.',
 'Custody service update: the issuer is holding its annual shareholder meeting. Proxy ballots may be submitted.',
 'Issuer meeting bulletin. The beneficial owners may instruct votes electronically on the resolutions.',
 'A special general meeting has been convened. The intermediary accepts shareholder voting instructions.',
 'Notice to nominee accounts: holders are invited to vote on the scheme resolutions at the meeting.',
 'Voting service terms for the upcoming extraordinary general meeting. Custodians can transmit proxy votes.',
]
DEADLINE='Voting instructions must be received by 24 November 2026 at 17:00 UTC.'

def item(ident,text,values,kind):
    expected={'votability':'VOTABLE',**{k:'NO' for k in RESTRICTIONS},'deadline_status':'OPEN',**values}
    factors={k:{'value':v} for k,v in expected.items() if k in PREDICATES}
    expected['classification']=decide(factors,{'status':expected['deadline_status']})['classification']
    return {'id':ident,'text':text,'expected':expected,'source_type':'SYNTHETIC_VALIDATION_ONLY','pattern':kind,'not_for_training':True}

def build():
    out=[]
    for index,(field,(yes,no)) in enumerate(PHRASES.items()):
        variants=[(yes+'.','YES','affirmative'),(no+'.','NO','explicit_negative'),
            ('The preliminary notice stated that '+yes+'. Final terms: '+no+'.','NO','superseded'),
            ('Historically, '+yes+'. The current notice supplies no information on this condition.','UNKNOWN','historical_only'),
            ('The general market guide says '+yes+'. For this event, '+no+'.','NO','irrelevant_reference'),
            (yes+'. A different paragraph states that '+no+'. No clarification is supplied.','UNKNOWN','unresolved_conflict')]
        for j,(body,label,pattern) in enumerate(variants):
            text=CONTEXTS[(index+j)%len(CONTEXTS)]+' '+body+' '+DEADLINE
            out.append(item(f'CV-{len(out)+1:03d}',text,{field:label},pattern+':'+field))
    for i in range(16):
        fields=list(PHRASES);a=fields[i%8];b=fields[(i+3)%8];positive=i<8
        text=CONTEXTS[i%6]+' '+PHRASES[a][0]+'. '+('Final terms: ' if i>=8 else '')+PHRASES[b][0 if positive else 1]+'. '+DEADLINE
        out.append(item(f'CV-{len(out)+1:03d}',text,{a:'YES',b:'YES' if positive else 'NO'},'combined_restrictions'))
    nonvote=[
        'A mandatory cash dividend will be credited automatically. No shareholder vote or election is available.',
        'This stock split is mandatory. It does not offer any voting opportunity.',
        'The issuer has published an information circular about a bond interest payment. This is not a shareholder meeting and no vote is requested.',
        'Please ignore the prior proxy invitation: the meeting has been cancelled and voting is unavailable.',
        'A corporate name change will be implemented automatically; no voting instructions are solicited.',
        'This communication reports completed meeting results; no current voting opportunity is offered.',
        'An automatic redemption is notified. Shareholders cannot submit votes for this event.',
        'The tender election is an offer acceptance rather than a shareholder vote. No general meeting is involved.',
    ]
    for text in nonvote:out.append(item(f'CV-{len(out)+1:03d}',text,{'votability':'NOT_VOTABLE','deadline_status':'UNKNOWN'},'non_voting'))
    ambiguous=[
        'Participation terms are still under review. It is unclear whether any proxy voting channel will be offered.',
        'One operations team reports that shareholders can vote; another says no voting service is available. The conflict has not been resolved.',
        'Please ask your intermediary whether participation may be possible. No confirmed voting entitlement is provided.',
        'The notice is incomplete and refers to a voting appendix that is not included.',
        'Electronic participation is being considered, but the issuer has not confirmed that votes can be cast.',
        'This preliminary announcement refers to an unspecified shareholder action. Contact the agent for clarification.',
        'The custodian cannot yet confirm whether the account may lodge proxy instructions.',
        'A future meeting is contemplated; no confirmed voting offer or current instructions are supplied.',
    ]
    for text in ambiguous:out.append(item(f'CV-{len(out)+1:03d}',text,{'votability':'UNCERTAIN','deadline_status':'UNKNOWN'},'ambiguous_votability'))
    assert len(out)==80 and len({r['text'] for r in out})==80
    return out
