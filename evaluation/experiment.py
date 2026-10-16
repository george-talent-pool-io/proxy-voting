"""Read-only research evidence for the existing performance screen."""
import json
from pathlib import Path
from apps.api import store
from training.study import load_study
from evaluation.quality_gates import assess

ROOT=Path(__file__).resolve().parents[1]

def read(relative,default=None):
    p=ROOT/relative
    return json.loads(p.read_text()) if p.exists() else default

def evidence(path=None):
    study=load_study(path);selected={r['record_id']:r for r in study['records'] if r['selected']} if study else {}
    verified=0;expert=0;test_rows=[];validation_rows=[];locked=False
    with store.connect(path) as c:
        for r in c.execute("SELECT r.record_id,r.context FROM reviews r WHERE r.action='VERIFY' AND r.id=(SELECT max(id) FROM reviews WHERE record_id=r.record_id)"):
            if r['record_id'] in selected:
                verified+=1;expert+=int(bool(json.loads(r['context']).get('domain_expert_attested')))
        approved={r['id'] for r in c.execute("SELECT id,context FROM reviews WHERE action='VERIFY'") if json.loads(r['context']).get('domain_expert_attested') and json.loads(r['context']).get('blind_review')}
        run=store.latest_run(c)
        if run:
            from evaluation.evaluate import evaluation_rows
            test_rows=[r for r in evaluation_rows(c,run['id'],'test') if r['review_revision'] in approved]
            validation_rows=[r for r in evaluation_rows(c,run['id'],'validation') if r['review_revision'] in approved]
        if study and c.execute("SELECT name FROM sqlite_master WHERE name='study_label_locks'").fetchone():
            locked=bool(c.execute('SELECT study_id FROM study_label_locks WHERE study_id=?',(study['id'],)).fetchone())
    from evaluation.metrics import compute_metrics,select_threshold
    policy=select_threshold(validation_rows)
    base=read('data/reports/semantic-challenge.json',{})
    root='data/experiments/supplied-synthetic-v1/'
    scored=read(root+'TEST-SCORED.json');selection=read(root+'validation-selection.json')
    challenge=read(root+'fine-tuned-challenge.json')
    comparison=[]
    for name in ['base','fine-tuned']:
        m=scored['models'][name] if scored else None
        comparison.append({'name':'Base Laya' if name=='base' else 'Fine-Tuned Laya','test':{k:v for k,v in m.items() if k!='failures'} if m else None,'challenge_passed':base.get('passed') if name=='base' else challenge.get('passed') if challenge else None,'challenge_n':57})
    return {'provenance':'AI-authored synthetic experiment, not customer accuracy. Real public excerpts are unlabelled.',
      'study':{'id':study['id'] if study else None,'target':len(selected),'reviewed':verified,'expert_attested':expert,'targets':study['targets'] if study else {}},
      'comparison':comparison,'selected':selection['selected']['candidate'] if selection else None,
      'learning_curve':read(root+'learning-curve.json',{'points':[],'message':'Not measured yet'}),
      'automation':read(root+'automation-analysis.json',{'models':{},'message':'Not measured yet'}),
      'challenge_risk':read(root+'challenge-error-summary.json'),
      'quality_gate':assess(test_rows,compute_metrics(test_rows),frozen_labels=locked,validation_threshold=policy['threshold'] if policy else None),
      'limitations':['Synthetic dataset contains cross-split duplicates; supplied memberships were retained on instruction.','Two test rows were inspected before the blind protocol; results disclose those IDs and a 98-case sensitivity analysis.','Supplied customer-status priority is blocking > POA > other. The original application/challenge mapping is retained separately. Supplied OPEN labels also differ from the application deadline definition.','No expert-reviewed public frozen test exists. Automation remains disabled.'],
      'scored':bool(scored)}

def synthetic_errors(model='fine-tuned',dataset='challenge'):
    if dataset=='challenge':
        report=read('data/experiments/supplied-synthetic-v1/'+('base' if model=='base' else 'fine-tuned')+'-challenge.json')
        if not report:return []
        return [dict(id=r['id'],text=r['text'],expected={k:v for k,v in r['expected'].items() if k!='classification'},
          expected_customer_status=r['expected'].get('classification','NOT_ASSERTED'),observed=r['observed'],
          predicted_customer_status=r['observed']['classification'],failed_fields=[k for k,v in r['checks'].items() if not v],
          scores=r['result']['scores'],confidence=r['result']['confidence'],raw_answers=r['result']['raw_answers'],tags=r['tags']) for r in report['examples'] if not r['passed']]
    p=read('data/experiments/supplied-synthetic-v1/TEST-SCORED.json')
    if not p:return []
    if model not in p['models']:raise ValueError('Unknown experiment model')
    return p['models'][model]['failures']
