"""Real-model customer workflow in an isolated AI-only client workspace.

Reuses the controlled corpus for engineering replay: NOT a new blind study.
Import -> revisioned AI labels -> protected freeze -> validation -> calibration
-> operating point -> persisted confidence/review simulation -> quality refusal.
No customer dataset, test model or calibrator is packaged with the product.
"""
import argparse
import json
import os
from pathlib import Path
from production import service, storage, worker, learning, qualification
from training.framework import jobs, seeds, event_data, releases
from training.framework.bundle import sha, write
from apps.api import store


def run(output,corpus,laya_job):
    output=Path(output).resolve();output.mkdir(parents=True,exist_ok=False)
    # Export once, then serving never needs this job's original dataset again.
    seed_path=output/'workspace/seeds/ai-engineering-parent'
    seed_path.parent.mkdir(parents=True)
    parent=seeds.export_derivative(laya_job,seed_path,origin='AI_TEST_DERIVATIVE')
    jobs.WORKSPACE=output/'workspace';store.DB_PATH=str(output/'client.sqlite')
    # This explicitly invoked isolated engineering runner executes real models.
    # It changes only this subprocess, never the deployed service defaults.
    os.environ['TRAINING_EXECUTION_ENABLED']='true'
    os.environ['AUTOMATION_ENABLED']='false'
    storage.initialise();worker.initialise()
    corpus=Path(corpus);manifest=json.loads((corpus/'manifest.json').read_text())
    actor={'name':'AI framework construction','expert_attested':False}
    reference='2026-10-18T12:00:00+00:00';population='AI_CLIENT_ENGINEERING_REPLAY'
    membership=[];input_by_event={};ordinal=0
    for role,entry in manifest['files'].items():
        path=corpus/entry['labels']
        if sha(path)!=entry['labels_sha256']:raise ValueError('Replay corpus drift')
        rows=[json.loads(line) for line in path.read_text().splitlines()]
        for start in range(0,len(rows),500):
            batch=rows[start:start+500];request=[]
            for row in batch:
                ordinal+=1;cid=f'AI{ordinal:06d}'
                request.append({'raw':row['text'],'sender':'AI_ENGINEERING_ONLY','source_type':'USER_PROVIDED',
                    'source_reference':'AI-authored ordinary notice; engineering replay, not customer production data',
                    'group_id':row['group'],'family':row['group'],'split':role,
                    'declared':{'corp':cid,'seme':cid,'function':'NEWM'},'language':'en','population':population})
            imported=service.import_rows('replay-'+role+'-'+str(start),request,actor['name'])
            if imported['rejected']:raise ValueError('Unexpected replay import rejection')
            for row,record in zip(batch,imported['rows']):
                eid=record['event_id'];view=service.source_view(eid)
                target={**row['expected'],'evidence':row['evidence_truth'],'ambiguities':[],
                        'deadline_information':{'deadline_mentioned':True,'deadline_text':'Voting instructions must reach the custodian by 24 November 2026 at 17:00 UTC.'}}
                service.review(eid,{'snapshot_hash':view['snapshot_hash'],'expected_revision':None,'target':target,
                    'notes':'AI construction facts; not independent expert labels','model_id':'Codex / GPT-6',
                    'evaluation_time':reference,'expected_final_status':row['final_status'],'expected_deadline_status':'OPEN'},actor,ai=True)
                membership.append(eid);input_by_event[eid]=row
    service.freeze('client-replay-v1',membership,actor['name'])
    bundle=jobs.member('bundles','client-replay-v1');event_data.export_reviews(bundle)
    spec={'bundle_id':'client-replay-v1','dataset_id':'client-replay-v1','actor':actor['name'],'reference':reference,'max_seconds':3600,
          'stages':[{'name':'frozen','reuse_seed':seed_path.name}],
          'candidates':[{'name':'SPECIALIST','mode':'LAYA_ONLY','laya_stage':'frozen','laya_inference':'WHOLE_NOTICE_SCOPED_EVIDENCE'}]}
    campaign=jobs.member('campaigns','client-replay-v1');learning.prepare(spec,campaign);result=learning.run(campaign)
    release_id=result['selected_release'];release=jobs.member('releases',release_id)
    cal=service.calibrate('client-replay-v1',dataset_id='client-replay-v1',release_id=release_id,population=population,
                           reference=reference,actor=actor['name'])
    point=service.select_operating_point('client-replay-v1',campaign_id=campaign.name,candidate='SPECIALIST',dataset_id='client-replay-v1',
                                         calibrator_id='client-replay-v1',population=population,actor=actor['name'])
    demos=[eid for eid,row in input_by_event.items() if row['role']=='TRAIN' and all(v!='UNKNOWN' for v in row['expected'].values())][:5]
    worker.submit('client-replay-inference','INFERENCE',{'release_id':release_id,'event_ids':demos,'calibrator_id':'client-replay-v1'},actor['name'])
    worker.run_once()
    # Real staged routing probe. Stage calibration opens only LAYA_STAGE; the
    # new cascade deliberately has no FINAL calibrator and remains review-only.
    stage=service.calibrate('client-stage-v1',dataset_id='client-replay-v1',release_id=release_id,population=population,
                            reference=reference,actor=actor['name'],stage='LAYA')
    stage_point=service.select_operating_point('client-stage-v1',campaign_id=campaign.name,candidate='SPECIALIST',dataset_id='client-replay-v1',
        calibrator_id='client-stage-v1',population=population,actor=actor['name'],stage='LAYA')
    original_qwen=Path(__file__).resolve().parents[1]/'data/training-workspace/seeds/frozen-learning-v3-qwen38-mlx'
    qwen=seeds.verify(original_qwen)
    qwen_seed=jobs.member('seeds','local-qwen-foundation')
    seeds.freeze(qwen['spec'],qwen_seed,prompt_path=original_qwen/'semantic-prompt.txt',questions_path=original_qwen/'laya-questions.json')
    cascade_id='client-calibrated-routing-probe'
    releases.prepare({'mode':'LAYA_QWEN','laya_seed':seed_path.name,'llm_seed':qwen_seed.name,
        'laya_inference':'WHOLE_NOTICE_SCOPED_EVIDENCE','laya_calibrator_id':'client-stage-v1',
        'laya_operating_point_id':'client-stage-v1'},jobs.member('releases',cascade_id))
    from production.cascade_policy import assess as assess_stage
    validation=[json.loads(line) for line in (campaign/'validation-SPECIALIST/predictions.jsonl').read_text().splitlines()]
    needs_escalation=[r for r in validation if not assess_stage(r['text'],r['result'],stage,stage_point,
        language='en',input_type='UNSTRUCTURED_NOTICE',population=population)['accept']]
    probe_ids=[r['id'] for r in (needs_escalation or validation)[:2]]
    worker.submit('client-stage-routing-probe','INFERENCE',{'release_id':cascade_id,'event_ids':probe_ids,
        'review_only_unsealed':True},actor['name']);worker.run_once()
    # Complete customer protocol must refuse production activation for AI truth.
    qualification.prepare('client-replay-v1',release_id=release_id,dataset_id='client-replay-v1',
        calibrator_path=jobs.member('customer-calibrators','client-replay-v1').with_suffix('.json'),population=population,
        policy={},reference=reference,actor=actor['name'])
    from production.resources import device
    from training.framework.resources import model_resource
    with device('customer-qualification'):
        with model_resource('customer-qualification'):certificate=qualification.evaluate('client-replay-v1')
    if certificate['customer_gate_passed']:raise ValueError('AI labels must never grant customer activation')
    with store.connect() as c:
        decisions=[json.loads(r[0]) for r in c.execute('SELECT payload FROM client_decisions ORDER BY created_at')]
        probes=[json.loads(r[0])['result'] for r in c.execute('SELECT payload FROM learning_executions WHERE job_id=?',(cascade_id,))]
    if len(probes)!=2:raise ValueError('Actual calibrated cascade probe did not persist both executions')
    if any(p.get('execution_error') or not any('calibrated_routing' in g for g in p.get('gear1_gates',{}).values()) for p in probes):
        raise ValueError('Actual stage routing failed instead of executing the calibrated policy')
    probe_decisions=[d for d in decisions if d['release_id']==cascade_id]
    if any(d['decision']['confidence'] is not None or not d['decision']['review_required'] for d in probe_decisions):
        raise ValueError('Uncalibrated final cascade inherited specialist confidence/automation')
    receipt={'scope':'AI_ENGINEERING_REPLAY_NOT_NEW_BLIND_QUALITY','workspace':str(jobs.WORKSPACE),'database':store.DB_PATH,
             'population':population,'events':len(membership),'seed_identity':parent['identity'],'release_id':release_id,
             'calibrator_sha256':cal['sha256'],'calibration_reports':cal['reports'],'operating_point':point,
             'saved_decisions':len(decisions),'numerical_final_confidences':sum(d['decision']['confidence'] is not None for d in decisions),
             'review_required':sum(d['decision']['review_required'] for d in decisions),'qualification':certificate,
             'audit':storage.verify_audit(),'automation_enabled':False,'test_models_in_product':False}
    receipt['calibrated_cascade_probe']={'stage_partition':stage['context']['calibration_partition'],
        'stage_operating_status':stage_point['status'],'persisted_executions':len(probes),
        'llm_invocations':sum(bool(((p.get('llm_stage') or {}).get('llm') or {}).get('invoked')) for p in probes),
        'final_confidence_not_inherited':True,'all_manual_review':True,'scope':'Real stage-routing integration, not final-pipeline quality qualification'}
    write(output/'receipt.json',receipt)
    return receipt

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('output');p.add_argument('--corpus',required=True);p.add_argument('--laya-job',required=True)
    a=p.parse_args();run(a.output,a.corpus,Path(a.laya_job))
