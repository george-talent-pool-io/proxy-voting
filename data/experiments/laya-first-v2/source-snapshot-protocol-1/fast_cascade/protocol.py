"""Explicit new experiment; never resumes the user-stopped domain study."""
from qwen_domain.protocol import ROOT,CORPUS,read,write,append,sha,digest,rows,now
STUDY=ROOT/'data/experiments/laya-first-v2'
VERSION='laya-first-three-gear-v2'

def atomic(path,value):
    import json
    path.parent.mkdir(parents=True,exist_ok=True);temp=path.with_suffix('.tmp');temp.write_text(json.dumps(value,ensure_ascii=False,indent=2,allow_nan=False)+'\n');temp.replace(path)

def status(state,stage,**extra):
    counts={p.stem:sum(bool(s.strip()) for s in p.open()) for p in (STUDY/'predictions').glob('*.jsonl')}
    atomic(STUDY/'LIVE-STATUS.json',{'timestamp':now(),'state':state,'stage':stage,'persisted_rows':counts,'automation_enabled':False,'customer_accuracy':None,**extra})

def stopped():return (STUDY/'STOP').exists()

def check_stop():
    if stopped():raise InterruptedError('User requested cooperative stop; current completed row is preserved')
