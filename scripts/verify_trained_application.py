"""Real opt-in API proof using registered models and a labelled synthetic FIN input.

Runs a temporary loopback server, persists traces, restarts, verifies persistence.
Does not alter reviews, source notices, default architecture or automation flags.
"""
import json
import os
import socket
import subprocess
import sys
import time
import urllib.request
from pathlib import Path

from iso_adapter.benchmark import fin
from training.framework.bundle import load_bundle
from training.framework.jobs import WORKSPACE


def verify(qwen_job, laya_job, output='artifacts/trained-application-proof-v2.json'):
    _, examples = load_bundle(WORKSPACE / 'bundles/qualification-v1')
    e = next(e for e in examples if e.split == 'VALIDATION' and e.target.votability == 'VOTABLE')
    raw = fin(':16R:GENL\n:20C::SEME//FRAMEWORK-PROOF\n:20C::CORP//SYNTHETIC-EVENT\n'
              ':23G:NEWM\n:22F::CAEV//MEET\n:16S:GENL\n'
              ':16R:CAOPTN\n:13A::CAON//001\n:22F::CAOP//PROX\n'
              ':98E::RDDT//20261124170000,000/00\n:16S:CAOPTN\n'
              ':16R:ADDINFO\n:70E::ADTX//' + e.text + '\n:16S:ADDINFO')
    with socket.socket() as s:
        s.bind(('127.0.0.1',0)); port=s.getsockname()[1]
    base = f'http://127.0.0.1:{port}'
    env = {**os.environ, 'TRAINED_CANDIDATES_ENABLED':'true'}
    logpath = Path('artifacts/trained-application-proof-server.log')
    def start():
        with logpath.open('ab',buffering=0) as log:
            p=subprocess.Popen([sys.executable,'-m','uvicorn','apps.api.main:app','--host','127.0.0.1','--port',str(port)],
                                env=env,stdin=subprocess.DEVNULL,stdout=log,stderr=log)
        for _ in range(100):
            try:
                urllib.request.urlopen(base+'/api/health',timeout=1);return p
            except OSError:time.sleep(.1)
        p.terminate();p.wait();raise RuntimeError('Proof server did not start')
    process=start();results=[]
    try:
        for job in [laya_job,qwen_job]:
            req=urllib.request.Request(base+f'/api/training/jobs/{job}/analyse',data=json.dumps({'text':raw,'source_type':'STANDARDS_DERIVED_SYNTHETIC'}).encode(),
                                       headers={'Content-Type':'application/json'})
            began=time.perf_counter()
            with urllib.request.urlopen(req,timeout=600) as response:value=json.load(response)
            result=value['result']
            assert result['parser']['parser']=='PROWIDE'
            assert value['raw_source']==raw and result['decision']['manual_review_required']
            assert result['automation_enabled'] is False
            for field in result['reconciliation']['predicates'].values():
                for quote in field.get('evidence',[]):
                    if quote.get('valid'):assert raw[quote['start']:quote['end']]==quote['text']
            results.append({'job':job,'api_wall_seconds':time.perf_counter()-began,'execution':value})
        process.terminate();process.wait(20);process=start()
        for row in results:
            with urllib.request.urlopen(base+'/api/training/executions/'+row['execution']['id'],timeout=20) as response:
                saved=json.load(response)
            assert saved==row['execution']
        receipt={'source_type':'STANDARDS_DERIVED_SYNTHETIC','semantic_source_id':e.id,
                 'purpose':'Real application path and persistence verification, not classification accuracy',
                 'model_runs':results,'restart_persistence_verified':True,'automation_enabled':False}
        with Path(output).open('x') as f:json.dump(receipt,f,ensure_ascii=False,indent=2)
        print(json.dumps({'passed':True,'executions':[r['execution']['id'] for r in results]},indent=2))
    finally:
        process.terminate();process.wait(20)


if __name__=='__main__':
    import argparse
    p=argparse.ArgumentParser();p.add_argument('qwen_job');p.add_argument('laya_job');p.add_argument('--output',default='artifacts/trained-application-proof-v2.json');a=p.parse_args()
    verify(a.qwen_job,a.laya_job,a.output)
