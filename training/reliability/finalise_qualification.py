"""Supervised sequential real-model checks after the paired study exits.

No concurrent neural workloads, no automation promotion and no source changes.
Each subprocess has its own job-scoped sleep assertion and bounded lifetime.
"""
import argparse
import json
import os
import signal
import sqlite3
import subprocess
import sys
import time
from pathlib import Path


def save(path,value):
    with Path(path).open('x') as f:json.dump(value,f,indent=2)


def execute(args,output,*,env=None,max_seconds=7200):
    with Path(output).open('xb') as log:
        child=subprocess.Popen(args,stdout=log,stderr=subprocess.STDOUT,env=env,start_new_session=True)
        assertion=subprocess.Popen(['/usr/bin/caffeinate','-is','-w',str(child.pid)])
        start=time.perf_counter();wall=time.time();reason=None
        try:
            while child.poll() is None:
                elapsed=time.perf_counter()-start
                if elapsed>max_seconds or time.time()-wall-elapsed>20:
                    reason='BUDGET_OR_HOST_SUSPENSION';os.killpg(child.pid,signal.SIGINT)
                    try:child.wait(20)
                    except subprocess.TimeoutExpired:os.killpg(child.pid,signal.SIGKILL)
                    break
                time.sleep(10)
            code=child.wait()
        finally:
            if assertion.poll() is None:assertion.terminate()
            assertion.wait()
    receipt={'command':args,'returncode':code,'seconds':time.perf_counter()-start,'stop_reason':reason}
    print(json.dumps(receipt),flush=True)
    return receipt


def run(experiment,supervisor):
    root=Path(experiment);receipts=[]
    start=time.perf_counter()
    while not Path(supervisor).exists():
        if time.perf_counter()-start>23000:raise TimeoutError('Parent qualification supervisor did not finish')
        time.sleep(15)
    parent=json.loads(Path(supervisor).read_text())
    if not (root/'RESULT.json').exists():raise ValueError('Parent qualification incomplete; no follow-up inference started')
    out=root/'follow-up';out.mkdir(exist_ok=False)
    save(out/'SUPERVISOR_RECEIPT.json',parent)
    receipts.append(execute([sys.executable,'-u','-m','training.reliability.post_qualification',str(root)],out/'post-freeze.log'))
    # A real durable customer worker: isolated SQLite clone, existing tiny
    # development-only event bundle, current models and fresh release identity.
    database=out/'client.sqlite'
    source=Path('data/experiments/reliability-real-customer-path-20261022/state.sqlite').resolve()
    with sqlite3.connect('file:'+str(source)+'?mode=ro',uri=True) as a,sqlite3.connect(database) as b:a.backup(b)
    env={**os.environ,'VOTING_DB':str(database.resolve()),'TRAINING_EXECUTION_ENABLED':'true','AUTOMATION_ENABLED':'false'}
    campaign=root.name+'-customer-integration'
    code="""import copy,json
from pathlib import Path
from training.framework import jobs
from production import learning
spec=copy.deepcopy(json.loads(Path('data/training-workspace/campaigns/reliability-real-current-20261022/campaign.json').read_text())['spec'])
spec['actor']='AI current indexed-framework integration; not customer qualification'
spec['stages'][1]['reuse_seed']='qwen38-indexed-evidence-foundation-v1'
spec['candidates'][0]['laya_inference']='WHOLE_NOTICE_WITH_PASSAGE_EVIDENCE'
spec['max_seconds']=1800
root=jobs.member('campaigns',__import__('sys').argv[1])
learning.prepare(spec,root);learning.run(root)
"""
    receipts.append(execute([sys.executable,'-u','-c',code,campaign],out/'customer-campaign.log',env=env,max_seconds=2400))
    if receipts[-1]['returncode']==0:
        testenv={**env,'RUN_RELEASE_REAL_MODEL':'1','RELEASE_CAMPAIGN':campaign}
        receipts.append(execute([sys.executable,'-m','pytest','-q','tests/classifier/test_registered_release_real.py'],
                                out/'real-worker-tests.log',env=testenv,max_seconds=1800))
    refs=json.loads((root/'RESULT.json').read_text())['releases']
    release=Path(refs['HYBRID']['path']).name
    receipts.append(execute([sys.executable,'-u','-m','scripts.qualify_model_installation','--release',release,
        '--output',str(out/'installation-probe'),'--reference','2026-10-23T12:00:00+00:00'],
        out/'installation-probe.log',max_seconds=2400))
    save(out/'RESULT.json',{'checks':receipts,'all_commands_passed':all(r['returncode']==0 for r in receipts),
        'automation_enabled':False,'customer_accuracy':None,'customer_qualified':False})


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('experiment');p.add_argument('supervisor');a=p.parse_args();run(a.experiment,a.supervisor)
