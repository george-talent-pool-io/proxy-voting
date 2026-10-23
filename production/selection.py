"""Validation ranking includes complete outputs, not semantic fields alone."""
from semantic_pipeline.schema import PREDICATES

VERSION='complete-output-selection-v1'


def evaluate(predictions,truth,*,role):
    if role!='VALIDATION':raise ValueError('Model selection uses VALIDATION only')
    if not predictions or len({r['id'] for r in predictions})!=len(predictions):raise ValueError('Unique validation predictions required')
    statuses=[];deadlines=[];complete=[]
    for row in predictions:
        key=truth[row['id']];r=row['result']
        final=key.get('expected_final_status');deadline=key.get('expected_deadline_status')
        if final is not None:statuses.append(r['decision']['classification']==final)
        if deadline is not None:deadlines.append(r['deadline']['status']==deadline)
        if final is not None and deadline is not None:
            complete.append(all(r['predicates'][k]['value']==key['target'][k] for k in PREDICATES) and
                            r['decision']['classification']==final and r['deadline']['status']==deadline)
    return {'version':VERSION,'cases':len(predictions),
        'final_status':{'support':len(statuses),'correct':sum(statuses)},
        'deadline_status':{'support':len(deadlines),'correct':sum(deadlines)},
        'complete_output':{'support':len(complete),'correct':sum(complete)},
        'scope':'Complete output = nine semantic fields, final status and deadline at the fixed reference time'}


def ranking(report):
    m=report['metrics'];d=report['decision_evaluation'];n=d['cases']
    if d['complete_output']['support']==n:
        primary=d['complete_output']['correct']/n
        secondary=d['final_status']['correct']/n
        scope='COMPLETE_OUTPUT'
    else:
        # Do not let four final labels masquerade as end-to-end selection.
        primary=m['cases_satisfying_all_supplied_assertions']/m['cases']
        secondary=m['correct_assertions']/m['assertions']
        scope='SEMANTIC_ONLY_INCOMPLETE_DECISION_TRUTH'
    return {'rank':(primary,secondary,m['correct_assertions']/m['assertions'],-m['median_latency_ms']),
            'scope':scope,'version':VERSION}
