"""Native semantic YES is evidence; a lexical whitelist must not veto it.

Validation v1 found12/12 affirmative blocking passages with native YES=1.0
rejected solely by lexical relevance. Scope/history/negation/supersession and
contradictory current statements remain explicit. No model label is inverted.
"""
import re
from cascade.aggregation import states as previous_states,reduce_states,AggregationConfig,ANCHORS
VERSION='native-positive-evidence-aggregation-v4'

# OTHER is residual to the named heads. A sentence waiving a POA/recall/etc.
# cannot be negative evidence about unrelated eligibility restrictions. These
# cues scope negative evidence only; they never veto native semantic YES.
RESIDUAL_SCOPE=re.compile(r'\bother\b.{0,30}(?:vot|restrict|condition|require)|'
    r'eligib|residen|professional.investor|retail.holder|minimum.{0,20}(?:holding|position|shares)|'
    r'paper.only|wet.signature|in.person.only|notari[sz].{0,20}signature',re.I)
RESIDUAL_TOPICS={
    'INVESTOR_CLASS':r'professional.investor|retail.holder',
    'RESIDENCY':r'residen|domicil',
    'MINIMUM_POSITION':r'minimum.{0,20}(?:holding|position|shares)',
    'PHYSICAL_FORM':r'paper.only|wet.signature|in.person.only|notari[sz].{0,20}signature',
}

def states(text,predicate,native):
    result=previous_states(text,predicate,native)
    for p in result:
        p['lexical_anchor_matched']=p['relevant']
        if predicate=='other_voting_restriction' and p['native_value']=='NO':
            named=[k for k,anchor in ANCHORS.items() if k!=predicate and re.search(anchor,p['text'],re.I)]
            p['named_predicate_topics']=named
            if named and not RESIDUAL_SCOPE.search(p['text']):
                p.update(state='UNKNOWN',relevant=False,
                         reason='NAMED_RESTRICTION_NEGATIVE_IS_NOT_RESIDUAL_NEGATIVE')
        if predicate=='other_voting_restriction':
            p['residual_topics']=[key for key,pattern in RESIDUAL_TOPICS.items() if re.search(pattern,p['text'],re.I)]
        if p['native_value']=='YES':
            p['state']='AFFIRMATIVE';p['relevant']=True
            p['reason']='NATIVE_PREDICATE_AFFIRMATIVE; lexical wording does not veto model evidence'
        p['relevance_method']='NATIVE_SEMANTIC_POSITIVE_OR_SCOPED_NEGATIVE'
    if predicate=='other_voting_restriction':
        positive=[p for p in result if p['state']=='AFFIRMATIVE' and not p['historical'] and not p['background']]
        for p in result:
            # Removing a residency condition does not remove a separate minimum
            # position/investor-class condition. Unknown scopes remain reviewable.
            if (p['state']=='NEGATIVE' and p['residual_topics'] and positive and
                all(q['residual_topics'] and not set(p['residual_topics']) & set(q['residual_topics']) for q in positive) and
                not re.search(r'\b(?:all|any|other)\b.{0,20}(?:restrict|condition|require)',p['text'],re.I)):
                p.update(state='UNKNOWN',relevant=False,reason='NEGATIVE_DIFFERENT_RESIDUAL_TOPIC')
    return result

def aggregate(text,predicate,native,config=AggregationConfig()):
    result=reduce_states(states(text,predicate,native),config)
    result['aggregation_version']=VERSION
    result['previous_aggregation_version']='evidence-aggregation-v2'
    return result
