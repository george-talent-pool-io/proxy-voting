"""New narrow task. Original frozen experiment is not changed or retuned.
Only supplied train/validation ZIP members are opened. No parser fixtures train ML.
Four available targets; absent labels for four new predicates are NOT invented.
"""
import hashlib,json,os
from pathlib import Path
from dataclasses import asdict
from hybrid.semantics import questions
ROOT=Path('data/experiments/narrow-v1')
MODEL=Path('data/models/narrow-v1')
TARGETS=['votable','share_blocking','poa_required']
# Other restriction's old definition overlaps registration/disclosure/split/recall;
# it is not equivalent to the new residual predicate and cannot be reused as gold.

def prepare():
    from training.synthetic_protocol import rows,sha,write
    ROOT.mkdir(parents=True,exist_ok=False)
    qs=questions();selected={k:qs[k] for k in TARGETS};membership={}
    challenge=json.loads(Path('tests/fixtures/semantic.json').read_text())
    forbidden={hashlib.sha256(r['text'].encode()).hexdigest() for r in challenge}
    for split in ['train','validation']:
        source=rows(split);data=[];membership[split]=[]
        for row in source:
            if row['text_sha256'] in forbidden:raise ValueError('Challenge contamination')
            target={'votable':{'VOTABLE':'YES','NOT_VOTABLE':'NO','UNCERTAIN':'UNCERTAIN'}[row['votability']],**{k:row[k] for k in TARGETS if k!='votable'}}
            data.append({'state':row['text'],'questions':selected,'expected':target})
            membership[split].append({'id':row['id'],'source_hash':row['text_sha256']})
        with (ROOT/f'{split}.jsonl').open('x') as f:
            for row in data:f.write(json.dumps(row)+'\n')
    protocol={'kind':'AI-authored synthetic narrow-predicate experiment; not expert labels or independent public accuracy','targets':TARGETS,'unlabelled_predicates':[k for k in qs if k not in TARGETS],'questions':qs,'seed':42,'epochs':4,'freeze_encoder':False,'calib_frac':0,'selection':'One predeclared 4-epoch candidate. Validation only for temperature fitting. No post-test selection.','prior_test_exposure':'Original synthetic test was scored in a prior study. It is not reused as a new independent test. Existing 57 challenge cases are regression tests, never training.','known_leakage':'Supplied train/validation membership retained; exact/near overlap exists, see supplied-synthetic-v1 audit.','membership':membership,'files':{s+'.jsonl':sha(ROOT/(s+'.jsonl')) for s in ['train','validation']}}
    write(ROOT/'protocol.json',protocol)
    return protocol

def train():
    import torch,laya
    from laya.train import TrainConfig,finetune,read_data,items_from_rows,calibration_records
    from laya.calibrate import fit_temperature_map
    from training.synthetic_protocol import write,sha
    protocol=json.loads((ROOT/'protocol.json').read_text())
    if MODEL.exists():raise ValueError('Never overwrite checkpoint')
    for name,digest in protocol['files'].items():
        if sha(ROOT/name)!=digest:raise ValueError('Dataset hash changed')
    os.environ.update(HF_HUB_OFFLINE='1',TRANSFORMERS_OFFLINE='1',USE_TF='0');torch.set_num_threads(4)
    device='mps' if torch.backends.mps.is_available() else 'cpu'
    cfg=TrainConfig(epochs=4,seed=42,calib_frac=0,calib_max=0,shuffle_options=('choice',),micro_batch=1,grad_accum=8,max_len=2048,head_max_len=256,freeze_encoder=False,loss='soft-ce',eval_data=None,log_every=100)
    write(ROOT/'training-config.json',vars(cfg))
    result=finetune(str(ROOT/'train.jsonl'),'data/models/laya/multilingual',str(MODEL),cfg,device=device)
    agent=laya.load(str(MODEL),device=device)
    items,skipped=items_from_rows(agent.tok,read_data(str(ROOT/'validation.jsonl')),agent.cfg['max_len'],agent.cfg['head_max_len'])
    if skipped:raise ValueError('Skipped validation inputs')
    records=calibration_records(agent.model,agent.tok,items,agent.device,agent.cfg['max_len'],agent.cfg['head_max_len'],parallel=getattr(agent,'parallel_options',False))
    fitted=fit_temperature_map(records);p=MODEL/'rl_agent_config.json';cfg=json.loads(p.read_text());cfg.update(fitted);p.write_text(json.dumps(cfg,indent=2))
    write(ROOT/'training-result.json',{'training':result,'validation_calibration':fitted})
    freeze={'model_path':str(MODEL),'model_files':{str(p):sha(p) for p in sorted(MODEL.rglob('*')) if p.is_file()},'code':{str(p):sha(p) for p in sorted(Path('hybrid').glob('*.py'))},'protocol_sha256':sha(ROOT/'protocol.json'),'automation_enabled':False}
    write(ROOT/'FREEZE.json',freeze)
    print('Narrow checkpoint frozen',flush=True)
if __name__=='__main__':
    import sys
    print(prepare() if sys.argv[1]=='prepare' else train())
