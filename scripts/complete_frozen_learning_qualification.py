"""Serial, real-model completion checks after the controlled study finishes.

All artifacts are AI-only engineering evidence and excluded from delivery.
Optional PID wait never interrupts another workload or resumes a failed run.
"""
import argparse
import json
import os
import subprocess
import sys
import time
from pathlib import Path
from training.framework.bundle import write


def run(study,corpus,output,wait_pid=None):
    output=Path(output);output.mkdir(parents=True,exist_ok=False);study=Path(study)
    if wait_pid:
        import psutil
        try:
            p=psutil.Process(wait_pid)
            if 'customer-domain-adaptation' not in ' '.join(p.cmdline()):raise ValueError('Not the requested study worker')
            while p.is_running() and p.status()!=psutil.STATUS_ZOMBIE:time.sleep(5)
        except psutil.NoSuchProcess:pass
    result=json.loads((study/'result.json').read_text())
    jobs=result['jobs'];selected=result['selected']
    engineering_condition=selected if selected in jobs else max(jobs,key=lambda k:result['validation'][k]['correct_assertions'])
    job=jobs[engineering_condition]
    write(output/'PLAN.json',{'study':str(study),'quality_selected':selected,'engineering_derivative':engineering_condition,
          'model_job':job,'engineering_replay_not_new_blind_quality':True,'automation_enabled':False})
    def execute(name,args,env=None):
        print('START '+name,flush=True)
        with (output/(name+'.log')).open('xb') as log:
            subprocess.run([sys.executable,*args],stdout=log,stderr=subprocess.STDOUT,check=True,env={**os.environ,**(env or {})})
        print('PASS '+name,flush=True)
    continuation=output/'continuation'
    execute('frozen-continuation',['-m','scripts.verify_frozen_continuation',str(continuation),'--corpus',corpus,'--laya-job',job])
    campaign=output.name+'-integration'
    execute('real-customer-release',['-m','scripts.verify_current_customer_release',campaign,'--qwen-seed','frozen-learning-v3-qwen38-mlx','--laya-job',Path(job).name])
    execute('real-model-tests',['-m','pytest','-q','tests/classifier/test_registered_release_real.py'],
            {'RUN_RELEASE_REAL_MODEL':'1','RELEASE_CAMPAIGN':campaign})
    replay=output/'customer-replay'
    execute('customer-replay',['-m','scripts.verify_client_calibrated_loop',str(replay),'--corpus',corpus,'--laya-job',job])
    browser=output/'customer-browser'
    execute('calibrated-browser',['-m','scripts.verify_calibrated_client_browser',str(replay),str(browser)])
    receipt={'scope':'AI_ENGINEERING_QUALIFICATION_ONLY','study':str(study),'quality_selected':selected,
             'engineering_derivative':engineering_condition,'real_model_tests':2,'campaign':campaign,
             'continuation_receipt':str(continuation/'result.json'),'client_receipt':str(replay/'receipt.json'),
             'browser_receipt':str(browser/'receipt.json'),'automation_enabled':False}
    write(output/'receipt.json',receipt)
    execute('report',['-m','scripts.report_customer_adaptation',str(study),'data/reports/FROZEN_CHECKPOINT_LEARNING_EVALUATION.md',
        '--replay',str(replay/'receipt.json'),'--continuation',str(continuation/'result.json'),
        '--browser',str(browser/'receipt.json'),'--integration',str(output/'receipt.json')])
    return receipt


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('study');p.add_argument('corpus');p.add_argument('output');p.add_argument('--wait-pid',type=int)
    a=p.parse_args();run(a.study,a.corpus,a.output,a.wait_pid)
