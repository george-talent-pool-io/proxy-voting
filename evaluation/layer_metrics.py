"""Separate denominators for parsing, semantic predicates and final decisions.
Counts are evaluation observations, never pytest pass rates or model confidence.
"""
from collections import Counter

FACTORS=('votable','share_blocking','poa_required','other_restriction','deadline_status')

def semantic_case(row):
    # Only evaluate reference-labelled native model outputs. A software-derived deadline
    # is not a semantic prediction, and deadline-presence truth cannot be inferred from
    # OPEN/PASSED/UNKNOWN labels (unknown timezones can still have an explicit deadline).
    keys=[k for k in FACTORS if k in row['scores']]
    return {'expected':{k:row['true_decision'][k] for k in keys},'observed':{k:row['decision'][k] for k in keys}}

def field_accuracy(cases,unit):
    correct=total=exact=0
    for case in cases:
        expected=case['expected'];observed=case['observed']
        if not expected:raise ValueError('An evaluation case needs explicit reference labels')
        checks=[key in observed and observed[key]==value for key,value in expected.items()]
        correct+=sum(checks);total+=len(checks);exact+=all(checks)
    return dict(accuracy=correct/total if total else None,correct=correct,total=total,records=len(cases),unit=unit,exact_match_accuracy=exact/len(cases) if cases else None)

def measure_layers(parser_cases=(),semantic_cases=(),decision_cases=()):
    parser_cases=list(parser_cases);semantic_cases=list(semantic_cases);decision_cases=list(decision_cases)
    parser=field_accuracy(parser_cases,'reference-labelled ISO15022 fields')
    semantic=field_accuracy(semantic_cases,'reference-labelled semantic predicates')
    correct=sum(r.get('observed')==r['expected'] and 'observed' in r for r in decision_cases)
    final=dict(accuracy=correct/len(decision_cases) if decision_cases else None,correct=correct,total=len(decision_cases),records=len(decision_cases),unit='reference-labelled final events')
    return {'parser':{**parser,'title':'Parser accuracy','definition':'Exact field extraction against reference values; includes missing and malformed required outputs.'},
      'semantic':{**semantic,'title':'Semantic-model accuracy','definition':'Predicate correctness against reference labels; independent of the final display-status mapping.'},
      'end_to_end':{**final,'title':'End-to-end decision accuracy','definition':'Final event classification against separately supplied event labels; never inferred by multiplying layer accuracies.'}}

def public_layers(run_id=None,path=None):
    from apps.api import store
    from evaluation.evaluate import evaluation_rows
    from training.study import STUDY_ID
    import json
    with store.connect(path) as c:
        run=c.execute('SELECT * FROM runs WHERE id=?',(run_id,)).fetchone() if run_id else store.latest_run(c)
        locked=False;rows=[]
        if c.execute("SELECT name FROM sqlite_master WHERE name='study_label_locks'").fetchone():
            locked=bool(c.execute('SELECT study_id FROM study_label_locks WHERE study_id=?',(STUDY_ID,)).fetchone())
        if run and locked:
            approved={r['id'] for r in c.execute('SELECT id,context FROM reviews') if json.loads(r['context']).get('domain_expert_attested') and json.loads(r['context']).get('blind_review')}
            rows=[r for r in evaluation_rows(c,run['id'],'test') if r['review_revision'] in approved]
    # Existing reviews label factors; their display statuses are derived, not independent
    # end-to-end event labels. Do not relabel that agreement as end-to-end accuracy.
    cases=[semantic_case(r) for r in rows]
    metrics=measure_layers(semantic_cases=[r for r in cases if r['expected']])
    metrics['parser']['reason']='No ISO15022 parser benchmark or reference extraction labels are available in this corpus.'
    metrics['end_to_end']['reason']='No separately verified final event labels; existing review statuses are derived from factor labels.'
    metrics['semantic']['reason']=None if rows else 'No locked, blind, expert-attested predicate test labels.'
    return {'scope':'Independent public-data test evidence only; synthetic experiments remain separate','run_id':run['id'] if run else None,'layers':metrics,'synthetic_included':False}

def diagnose_layers(cases):
    """Descriptive mismatches when ALL layer references exist; not causal proof."""
    counts=Counter()
    for row in cases:
        if not all(k in row for k in ('parser_correct','semantic_correct','final_correct')):
            counts['insufficient_reference_labels']+=1;continue
        if row['final_correct']:
            counts['correct_final_with_intermediate_mismatch' if not row['parser_correct'] or not row['semantic_correct'] else 'correct_all_layers']+=1
        elif not row['parser_correct'] and not row['semantic_correct']:counts['parser_and_semantic_mismatch']+=1
        elif not row['parser_correct']:counts['parser_mismatch']+=1
        elif not row['semantic_correct']:counts['semantic_mismatch']+=1
        else:counts['business_rule_or_final_label_mismatch']+=1
    return dict(counts)
