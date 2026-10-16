from collections import Counter,defaultdict
import re

def analyse_errors(rows,high_threshold=.98):
    factors=['votable','share_blocking','poa_required','other_restriction','deadline_status']
    rows=[{**r,'failed_fields':[k for k in factors if 'true_decision' in r and r['true_decision'][k]!=r['decision'][k]]} for r in rows]
    errors=[r for r in rows if not r['correct'] or r['failed_fields']]
    groups={}
    for key in ['predicted','true','country','market','language','event_type','length_band','confidence_band']:
        all_counts=Counter(r.get(key,'UNKNOWN') for r in rows)
        bad=Counter(r.get(key,'UNKNOWN') for r in errors)
        groups[key]=[dict(value=k,n=n,errors=bad[k],error_rate=bad[k]/n) for k,n in all_counts.items()]
    # Count observed repeated phrases; do not generate causal explanations.
    phrases=Counter()
    for r in errors:
        words=re.findall(r'\b[a-z]{3,}\b',r.get('text','').lower())
        phrases.update(set(' '.join(words[i:i+3]) for i in range(len(words)-2)))
    return dict(errors=[{k:v for k,v in r.items() if k!='text'} for r in errors],
        high_confidence_errors=[r['id'] for r in errors if r['confidence']>=high_threshold],
        high_confidence_factor_errors=[dict(id=r['id'],factor=k,winning_probability=max(r['scores'][k].values())) for r in errors for k in r['failed_fields'] if k in r.get('scores',{}) and max(r['scores'][k].values())>=high_threshold],
        groups=groups,repeated_error_phrases=[dict(phrase=k,records=n) for k,n in phrases.most_common(20) if n>1])
