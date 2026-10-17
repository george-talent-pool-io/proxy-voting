"""Native semantic YES is evidence; a lexical whitelist must not veto it.

Validation v1 found12/12 affirmative blocking passages with native YES=1.0
rejected solely by lexical relevance. Scope/history/negation/supersession and
contradictory current statements remain explicit. No model label is inverted.
"""
from cascade.aggregation import states as previous_states,reduce_states,AggregationConfig
VERSION='native-positive-evidence-aggregation-v3'

def states(text,predicate,native):
    result=previous_states(text,predicate,native)
    for p in result:
        p['lexical_anchor_matched']=p['relevant']
        if p['native_value']=='YES':
            p['state']='AFFIRMATIVE';p['relevant']=True
            p['reason']='NATIVE_PREDICATE_AFFIRMATIVE; lexical wording does not veto model evidence'
        p['relevance_method']='NATIVE_SEMANTIC_POSITIVE_OR_SCOPED_NEGATIVE'
    return result

def aggregate(text,predicate,native,config=AggregationConfig()):
    result=reduce_states(states(text,predicate,native),config)
    result['aggregation_version']=VERSION
    result['previous_aggregation_version']='evidence-aggregation-v2'
    return result
