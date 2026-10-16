"""Exercise official training integration contracts without pretending to train a model."""
import json
from pathlib import Path
import pytest
from classifier.laya_classifier import load_config
from apps.api.store import dumps
from training.train import train

def dataset(tmp_path):
    root=tmp_path/'golden';root.mkdir()
    labels=[dict(record_id=f'train-{i}',group_id=f'train-{i}',split='train',source_hash=f'train-{i}',revision=i) for i in range(20)]
    labels.extend(dict(record_id=f'validation-{i}',group_id=f'validation-{i}',split='validation',source_hash=f'validation-{i}',revision=i+20) for i in range(10))
    cfg=load_config()
    (root/'manifest.json').write_text(dumps({'counts':{'train':20,'validation':10,'test':5},'config':cfg,'label_revisions':labels}))
    for split in ['train','validation','test']:
        (root/f'{split}.jsonl').write_text(json.dumps({'state':f'Synthetic {split} input','questions':cfg['questions'],'expected':{'votable':'NO'}})+'\n')
    import hashlib
    p=root/'manifest.json';m=json.loads(p.read_text());m['file_hashes']={f'{split}.jsonl':hashlib.sha256((root/f'{split}.jsonl').read_bytes()).hexdigest() for split in ['train','validation','test']};p.write_text(dumps(m))
    return root

def test_dry_run_no_training(tmp_path):
    root=dataset(tmp_path)
    result=train(root,tmp_path/'output',dry_run=True)
    assert result['train']==20 and result['validation']==10
    assert result['config']['calib_frac']==0 and result['config']['calib_max']==0
    assert result['config']['eval_data'] is None
    assert not (tmp_path/'output').exists()

def test_training_never_reads_test(tmp_path,monkeypatch):
    import laya
    import laya.train as upstream
    import laya.calibrate as calibrate
    root=dataset(tmp_path);out=tmp_path/'model';seen={}
    def fit(data,model_dir,output_dir,config,device):
        seen['data']=data;seen['config']=config
        p=Path(output_dir);p.mkdir();(p/'model.safetensors').write_bytes(b'explicit synthetic test double weights')
        (p/'rl_agent_config.json').write_text('{"temperature":[1,1,1]}')
        return {'updates':1,'kind':'test double'}
    class Agent:
        cfg={'max_len':2048,'head_max_len':256};tok=None;model=None;device='cpu'
    monkeypatch.setattr(upstream,'finetune',fit)
    monkeypatch.setattr(laya,'load',lambda *a,**k:Agent())
    def read(path):
        seen['read_path']=path
        assert 'test.jsonl' not in path
        return []
    monkeypatch.setattr(upstream,'read_data',read)
    monkeypatch.setattr(upstream,'items_from_rows',lambda *a,**k:([1,2],{}))
    monkeypatch.setattr(upstream,'calibration_records',lambda *a,**k:[])
    monkeypatch.setattr(calibrate,'fit_temperature_map',lambda x:{'temperature':[1,2,1],'temperature_by_options':{}})
    train(root,out)
    assert seen['data'].endswith('train.jsonl') and seen['read_path'].endswith('validation.jsonl')
    cfg=json.loads((out/'voting-config.json').read_text())
    assert cfg['checkpoint_revision'].startswith('sha256:') and cfg['automation_enabled'] is False
    assert (out/'model-manifest.json').exists() and (out/'training-manifest.json').exists()
    with pytest.raises(ValueError,match='exists'):train(root,out)

def test_refuse_contaminated_manifest(tmp_path):
    root=dataset(tmp_path);p=root/'manifest.json';m=json.loads(p.read_text())
    m['label_revisions'][20]['group_id']='train-0';p.write_text(dumps(m))
    with pytest.raises(ValueError,match='Leakage'):train(root,tmp_path/'model',dry_run=True)


def test_refuse_modified_export(tmp_path):
    root=dataset(tmp_path);(root/'train.jsonl').write_text('changed')
    with pytest.raises(ValueError,match='checksum'):train(root,tmp_path/'model',dry_run=True)
