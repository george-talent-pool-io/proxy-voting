"""Fine-tune the official Laya implementation with strict isolation by default.
The explicitly named supplied-synthetic protocol is a separate, disclosed experiment;
its labels are never described as human golden data.
"""
import argparse
import json
from pathlib import Path

def train(dataset,output,epochs=4,device='auto',dry_run=False,freeze_encoder=True,seed=42,supplied_synthetic_protocol=False):
    from laya.train import finetune,TrainConfig,read_data,items_from_rows
    from classifier.laya_classifier import load_config,prepare_config
    import os
    os.environ.update(HF_HUB_OFFLINE='1',TRANSFORMERS_OFFLINE='1',USE_TF='0')
    dataset=Path(dataset);output=Path(output)
    if output.exists():raise ValueError('Output already exists; preserve previous models')
    manifest=json.loads((dataset/'manifest.json').read_text())
    manifest['config']=prepare_config(manifest['config'])
    import hashlib
    for split in ['train','validation']:
        file=dataset/f'{split}.jsonl'
        if hashlib.sha256(file.read_bytes()).hexdigest()!=manifest.get('file_hashes',{}).get(file.name):raise ValueError('Training export checksum mismatch; create a fresh verified export')
        for line in (dataset/f'{split}.jsonl').read_text().splitlines():
            row=json.loads(line)
            if list(row.get('questions',{}))!=manifest['config']['question_order']:raise ValueError('Training question order differs from inference schema')
            for key,q in row.get('questions',{}).items():
                if list(q['criteria'])!=manifest['config']['option_order'][key]:raise ValueError('Training question option order differs from inference schema')
    from training.split import verify_isolation
    if supplied_synthetic_protocol:
        # Explicit user-requested reproduction of a known leaky supplied split.
        # This exception is isolated from golden-data training and must not imply independence.
        from training.synthetic_protocol import rows as supplied_rows
        expected={(r['id'],s,r['text_sha256']) for s in ['train','validation'] for r in supplied_rows(s)}
        actual={(r['record_id'],r['split'],r['source_hash']) for r in manifest['label_revisions']}
        valid=actual==expected
        if supplied_synthetic_protocol=='nested-subset':
            valid=actual<=expected and {x for x in actual if x[1]=='validation'}=={x for x in expected if x[1]=='validation'}
        if not valid or manifest.get('kind')!='supplied AI synthetic experiment; not verified golden data':
            raise ValueError('Supplied synthetic exception requires exact original train/validation membership')
        from training.synthetic_protocol import decision as supplied_decision
        from classifier.preprocessing import normalise
        supplied={r['id']:r for s in ['train','validation'] for r in supplied_rows(s)}
        for s in ['train','validation']:
            revisions=[r for r in manifest['label_revisions'] if r['split']==s]
            exported=[json.loads(line) for line in (dataset/f'{s}.jsonl').read_text().splitlines()]
            if len(exported)!=len(revisions) or len(exported)!=manifest['counts'][s]:raise ValueError('Supplied row count mismatch')
            for r,e in zip(revisions,exported):
                source=supplied[r['record_id']]
                values=supplied_decision(source).model_dump(exclude={'manual_review_required'})
                target={k:'YES' if v is True else 'NO' if v is False else 'UNKNOWN' if v is None else v for k,v in values.items()}
                state=f'Reference date (UTC): {manifest["config"]["evaluation_date"]}\n\nNotice:\n{normalise(source["text"])}'
                if e['state']!=state or e['expected']!=target:raise ValueError('Supplied training content or labels changed')
        manifest['leakage_warning']='Known exact and near duplicates across supplied splits; retained on explicit user instruction. Not an independent test.'
    else:
        verify_isolation(manifest['label_revisions'])
    from training.study import challenge_guard
    challenge_guard(manifest['label_revisions'])
    if manifest['counts']['train']<20 or manifest['counts']['validation']<10:
        raise ValueError('At least 20 distinct reviewed training inputs and 10 validation inputs required; this is a smoke-test minimum, not statistical sufficiency')
    # Official SDK internal calibration is disabled; it otherwise splits at question level.
    # Group-separated validation is used for calibration AFTER weight optimisation.
    cfg=TrainConfig(epochs=epochs,seed=seed,calib_frac=0,calib_max=0,shuffle_options=('choice',),
        micro_batch=1,grad_accum=8,max_len=manifest['config']['max_len'],head_max_len=manifest['config']['head_max_len'],
        freeze_encoder=freeze_encoder,loss='soft-ce',eval_data=None,log_every=100)
    model_dir=manifest['config']['model_path']
    if dry_run:return {'train':manifest['counts']['train'],'validation':manifest['counts']['validation'],'config':vars(cfg)}
    result=finetune(str(dataset/'train.jsonl'),model_dir,str(output),cfg,device=device)
    # Fit native temperatures on validation only, never test. Use exact official SDK encoding.
    import laya
    from laya.train import calibration_records
    from laya.calibrate import fit_temperature_map
    agent=laya.load(str(output),device=None if device=='auto' else device)
    rows=read_data(str(dataset/'validation.jsonl'))
    items,skipped=items_from_rows(agent.tok,rows,agent.cfg['max_len'],agent.cfg['head_max_len'])
    if skipped:raise ValueError(f'Validation examples skipped: {skipped}')
    records=calibration_records(agent.model,agent.tok,items,agent.device,agent.cfg['max_len'],agent.cfg['head_max_len'],parallel=getattr(agent,'parallel_options',False))
    fitted=fit_temperature_map(records)
    config_path=output/'rl_agent_config.json'
    exported=json.loads(config_path.read_text());exported.update(fitted)
    config_path.write_text(json.dumps(exported,indent=2))
    (output/'training-manifest.json').write_text(json.dumps({'source':manifest,'training':result,'validation_calibration':fitted},default=str,indent=2))
    import hashlib
    files={str(p.relative_to(output)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(output.rglob('*')) if p.is_file()}
    model_revision='sha256:'+files['model.safetensors']
    (output/'model-manifest.json').write_text(json.dumps({'repository':'local-fine-tune','revision':model_revision,'files':files},indent=2))
    inference_config={**manifest['config'],'model_path':str(output),'checkpoint_revision':model_revision,'automation_enabled':False}
    (output/'voting-config.json').write_text(json.dumps(inference_config,indent=2))
    return result

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('dataset');p.add_argument('output');p.add_argument('--epochs',type=int,default=4);p.add_argument('--device',default='auto');p.add_argument('--dry-run',action='store_true');a=p.parse_args()
    print(json.dumps(train(a.dataset,a.output,a.epochs,a.device,a.dry_run),default=str,indent=2))
