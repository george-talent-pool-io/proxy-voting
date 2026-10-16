"""Unattended, resumable study. No completion flag is written until every gate runs."""
import json,os,sys,time,subprocess,traceback
from pathlib import Path
from datetime import datetime,timezone
ROOT=Path('data/experiments/cascade-v2')

def stamp():return datetime.now(timezone.utc).isoformat()
def count(name):
    p=ROOT/name
    if not p.exists():return 0
    return len(p.read_text().splitlines())
def status(state,stage,**extra):
    value={'state':state,'stage':stage,'pid':os.getpid(),'timestamp':stamp(),'automation_enabled':False,'customer_accuracy':None,**extra}
    path=ROOT/'LIVE-STATUS.json';tmp=path.with_suffix('.pending');tmp.write_text(json.dumps(value,indent=2));os.replace(tmp,path)
    with (ROOT/'EXECUTION-EVENTS.jsonl').open('a') as f:f.write(json.dumps(value)+'\n');f.flush();os.fsync(f.fileno())

def complete(stage):
    if stage=='validate':return all(count(f'validation-{a}.jsonl')==40 for a in ['C1','C2','C3','D1','D2','D3'])
    if stage=='repeat':return count('MODEL-REPEATABILITY.jsonl')==18
    if stage=='select-model':return (ROOT/'PRIMARY-MODEL-SELECTION.json').exists()
    if stage=='routing-validation':return count('routing-validation-FALLBACK_ALWAYS.jsonl')==80 and count('ROUTING-ASSERTION-DATASET.jsonl')==720
    if stage=='select-routing':return (ROOT/'ROUTING-SELECTION.json').exists()
    if stage=='freeze-final':return (ROOT/'FINAL-SELECTION-FREEZE.json').exists()
    if stage=='evaluation-specialists':return count('challenge-SPECIALISTS.jsonl')==57 and count('complete-SPECIALISTS.jsonl')==48
    if stage=='legacy':return all(count(f'{d}-{a}.jsonl')==n for d,n in [('challenge',57),('complete',48)] for a in 'AB')
    if stage=='evaluate-common':return all(count(f'{d}-{a}.jsonl')==n for d,n in [('challenge',57),('complete',48)] for a in ['C1','C2','C3','D1','D2','D3'])
    if stage=='evaluate-selected':return (ROOT/'PREDICTION-COMMIT.json').exists()
    return False

def main():
    from cascade.study import verify_core
    from scripts.start_cascade_runtime import ensure
    ensure();verify_core()
    # Exclusive runner lock; crash/restart can reclaim only a dead process.
    lock=ROOT/'RUNNER-LOCK.json'
    if lock.exists():
        old=json.loads(lock.read_text())
        import psutil
        if psutil.pid_exists(old['pid']):raise RuntimeError('A study runner is already active')
        lock.unlink()
    with lock.open('x') as f:json.dump({'pid':os.getpid(),'timestamp':stamp()},f)
    if Path('/usr/bin/caffeinate').exists():
        subprocess.Popen(['/usr/bin/caffeinate','-i','-w',str(os.getpid())],stdin=subprocess.DEVNULL,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,start_new_session=True)
    try:
        for stage in ['validate','repeat','select-model','routing-validation','select-routing','freeze-final','evaluation-specialists','legacy','evaluate-common','evaluate-selected']:
            if complete(stage):continue
            status('RUNNING',stage);print(stamp(),'START',stage,flush=True)
            subprocess.run([sys.executable,'-u','-m','cascade.study',stage],check=True)
            assert complete(stage),f'Incomplete stage {stage}'
            status('RUNNING',stage,stage_completed=True)
        for module in ['cascade.reporting','scripts.verify_cascade_phase']:
            status('RUNNING',module);subprocess.run([sys.executable,'-u','-m',module],check=True)
        status('COMPLETE','ALL_GATES_PASSED',note='Research implementation/evaluation complete; automation disabled and customer accuracy unknown')
    except BaseException as exc:
        status('FAILED','EXPLICIT_FAILURE',error=f'{type(exc).__name__}: {exc}')
        traceback.print_exc();raise
    finally:lock.unlink(missing_ok=True)
if __name__=='__main__':main()
