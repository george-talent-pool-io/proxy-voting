import json
from apps.api.store import connect,latest_run
from classifier.schema import Decision
from evaluation.metrics import compute_metrics,select_threshold
from evaluation.error_analysis import analyse_errors

def evaluation_rows(c,run_id,split='test'):
    reference=json.loads(c.execute('SELECT config FROM runs WHERE id=?',(run_id,)).fetchone()[0])['evaluation_date']
    rows=c.execute('''SELECT n.*,p.result,r.id AS review_revision,r.label,r.reviewer,r.reviewed_at,r.context FROM notices n
 JOIN predictions p ON p.record_id=n.id AND p.run_id=?
 JOIN reviews r ON r.id=(SELECT max(id) FROM reviews WHERE record_id=n.id)
 WHERE r.action='VERIFY' AND p.result IS NOT NULL AND (?='all' OR n.split=?)''',(run_id,split,split)).fetchall()
    if split in ['test','all'] and c.execute("SELECT name FROM sqlite_master WHERE name='study_label_locks'").fetchone():
        from training.study import STUDY_ID,fingerprint
        lock=c.execute('SELECT * FROM study_label_locks WHERE study_id=?',(STUDY_ID,)).fetchone()
        if lock:
            manifest=json.loads(lock['manifest'])
            if fingerprint(manifest)!=lock['sha256']:raise ValueError('Frozen test label checksum mismatch')
            pins=[r['revision'] for r in manifest['labels']]
            rows=[r for r in rows if r['split']!='test']
            if pins:
                rows+=c.execute('''SELECT n.*,p.result,r.id AS review_revision,r.label,r.reviewer,r.reviewed_at,r.context FROM notices n
 JOIN predictions p ON p.record_id=n.id AND p.run_id=? JOIN reviews r ON r.record_id=n.id
 WHERE r.action='VERIFY' AND n.split='test' AND p.result IS NOT NULL AND r.id IN ('''+','.join('?' for _ in pins)+')',(run_id,*pins)).fetchall()
    output=[]
    for row in rows:
        r=dict(row); ai=json.loads(r['result']); truth=Decision.model_validate_json(r['label']); meta=json.loads(r['metadata'])
        # Labels must have been reviewed before the run was declared as a held-out experiment.
        # Review-assisted label bias is disclosed; no claim that reviewers were blinded.
        context=json.loads(r['context'])
        if context.get('evaluation_date',reference)!=reference:continue
        confidence=ai['confidence']
        reasons=[s for s in ai['review_reasons'] if s!='Automation disabled pending validation']
        output.append(dict(id=r['id'],group_id=r['group_id'],split=r['split'],text=r['text'],
            review_revision=r['review_revision'],true=truth.status().value,predicted=ai['classification'],correct=truth.status().value==ai['classification'],
            true_votable=truth.votable,predicted_votable=ai['decision']['votable'],
            true_decision=truth.model_dump(),decision=ai['decision'],scores=ai['scores'],confidence=confidence,
            eligible=not reasons and ai['classification']!='UNCERTAIN_MANUAL_REVIEW',action=ai['action'],
            length_band='<2k' if len(r['text'])<2000 else '2k–8k' if len(r['text'])<8000 else '>8k',
            confidence_band=f'{int(confidence*10)*10}–{min(100,int(confidence*10)*10+10)}%',
            **{k:meta.get(k,'UNKNOWN') for k in ['country','market','language','event_type']}))
    return output

def evaluate(run_id=None,split='test',path=None):
    with connect(path) as c:
        run=latest_run(c) if not run_id else c.execute('SELECT * FROM runs WHERE id=?',(run_id,)).fetchone()
        if not run:return {'n':0,'accuracy':None,'curve':[],'errors':{},'message':'No model run'}
        rows=evaluation_rows(c,run['id'],split)
        labels=c.execute("SELECT count(*) FROM reviews r WHERE r.action='VERIFY' AND r.id=(SELECT max(id) FROM reviews WHERE record_id=r.record_id)").fetchone()[0]
    return {**compute_metrics(rows),'split':split,'run_id':run['id'],'verified_total':labels,
        'unique_groups':len(set(r['group_id'] for r in rows)),
        'label_revision_manifest':[{'record_id':r['id'],'true_decision':r['true_decision'],'review_revision':r['review_revision']} for r in rows],
        'errors':analyse_errors(rows),'reviewed_examples':[{k:v for k,v in r.items() if k not in ['text','scores']} for r in rows],
        'validation_policy_candidate':select_threshold(rows) if split=='validation' else None,
        'limitations':['Reviewers can see AI predictions; labels are not blinded.','Holdout metrics require domain-expert review; bucket support and unique source groups matter.','No automation policy is enabled by these exploratory metrics.']}

if __name__=='__main__':
    import argparse
    from pathlib import Path
    from apps.api.store import dumps,now
    p=argparse.ArgumentParser();p.add_argument('--run');p.add_argument('--split',choices=['test','validation','train','all'],default='test');p.add_argument('--output');a=p.parse_args()
    result=evaluate(a.run,a.split)
    if a.output:
        with open(a.output,'x') as f:f.write(dumps({'created_at':now(),**result}))
    else:print(dumps(result))
