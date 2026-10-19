"""Customer development campaigns stop at validation/sealing.

The research campaign deliberately scores its engineering frozen fixture. This
customer orchestrator never opens CALIBRATION/FROZEN_TEST answers: confidence
fitting and predeclared customer qualification are separate explicit jobs.
Training itself uses the existing registered job engines unchanged.
"""
import fcntl
import json
import os
import signal
import subprocess
import sys
import time
import uuid
from pathlib import Path
import psutil
from training.framework import jobs, campaigns, releases
from training.framework.bundle import write, sha
from training.framework.resources import model_resource
from production.resources import owned, note_job, inherited_fd


def prepare(spec, root):
    from production.qualification import source_hashes
    value = campaigns.prepare(spec, root)
    write(Path(root) / 'CUSTOMER_DEVELOPMENT_ONLY.json', {'version':'customer-development-v1',
          'plan_sha256':sha(Path(root)/'campaign.json'), 'production_sources':source_hashes(), 'calibration_or_test_scoring':False})
    return value


def spawn(root):
    root = Path(root)
    if campaigns.status(root)['state'] != 'PREPARED': raise ValueError('Only prepared campaigns can start')
    with (root/'worker.log').open('ab') as log:
        p = subprocess.Popen([sys.executable,'-m','production.learning',str(root)], cwd=jobs.ROOT,
                             env=os.environ.copy(), stdout=log, stderr=log, start_new_session=True)
    return {'worker_pid':p.pid,'automatic_resume':False,'protected_evaluation':False}


@owned
def run(root):
    # The standalone campaign CLI has no FastAPI lifespan to migrate the
    # operational database. Initialise before prediction metadata is queried.
    from production import storage
    storage.initialise()
    root = Path(root)
    with (root/'execution.lock').open('x'): pass
    plan = json.loads((root/'campaign.json').read_text())
    marker = json.loads((root/'CUSTOMER_DEVELOPMENT_ONLY.json').read_text())
    from production.qualification import source_hashes
    if sha(root/'campaign.json') != marker['plan_sha256'] or source_hashes()!=marker['production_sources']: raise ValueError('Customer campaign changed')
    spec = campaigns.CampaignSpec.model_validate(plan['spec']); began = time.monotonic()
    bundle=jobs.member('bundles',spec.bundle_id); dataset=jobs.member('event-datasets',spec.dataset_id)
    def check():
        if (root/'STOP').exists(): raise InterruptedError('Safe stop requested')
        if time.monotonic()-began > spec.max_seconds: raise TimeoutError('Campaign budget exceeded')
    with (jobs.WORKSPACE/'campaign-worker.lock').open('a') as lock:
        fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
        jobs.events(root,{'state':'RUNNING','pid':os.getpid(),'pid_started':psutil.Process().create_time()})
        try:
            if sha(bundle/'manifest.json') != plan['bundle_sha256'] or sha(dataset/'manifest.json') != plan['dataset_sha256'] or releases.source_files()!=plan['source_hashes']:
                raise ValueError('Campaign data/source changed')
            trained={};seed_stages={}
            for stage in spec.stages:
                check()
                if stage.reuse_seed:
                    seed_stages[stage.name]=stage.reuse_seed;continue
                if stage.reuse_job: trained[stage.name]=stage.reuse_job; continue
                ident=str(uuid.uuid4()); job=jobs.member('jobs',ident); jobs.prepare(bundle,stage.training,job)
                note_job(job)
                jobs.events(root,{'state':'RUNNING','phase':'TRAINING','stage':stage.name,'job_id':ident})
                child=None
                try:
                    with (root/(stage.name+'-training.log')).open('xb') as log:
                        child=subprocess.Popen([sys.executable,'-m','training.framework','execute',str(job)],cwd=jobs.ROOT,
                                               env=os.environ.copy(),stdout=log,stderr=log,start_new_session=True,pass_fds=(inherited_fd(),))
                        while child.poll() is None: check();time.sleep(.2)
                    if child.returncode: raise ValueError('Training failed; preserved job/log identify the failure')
                finally:
                    if child and child.poll() is None:
                        os.killpg(child.pid,signal.SIGINT)
                        try:child.wait(20)
                        except subprocess.TimeoutExpired:os.killpg(child.pid,signal.SIGKILL);child.wait()
                        lease=jobs.WORKSPACE/'model-training.lock'
                        if lease.exists() and json.loads(lease.read_text()).get('pid')==child.pid:lease.unlink()
                trained[stage.name]=ident
            from production.evaluation import predict
            from training.framework.event_data import load_answers
            from semantic_pipeline.metrics import summarize
            reports={}; candidates={}
            for candidate in spec.candidates:
                check(); ident=root.name+'-'+candidate.name; release=jobs.member('releases',ident)
                releases.prepare({'mode':candidate.mode,'laya_job':trained.get(candidate.laya_stage),
                                  'llm_job':trained.get(candidate.llm_stage),'policy':candidate.policy,
                                  'laya_seed':seed_stages.get(candidate.laya_stage),'llm_seed':seed_stages.get(candidate.llm_stage),
                                  'laya_inference':candidate.laya_inference,'laya_calibrator_id':candidate.laya_calibrator_id,
                                  'laya_operating_point_id':candidate.laya_operating_point_id},release)
                out=root/('validation-'+candidate.name)
                with model_resource('customer-validation'):
                    manifest,inputs,predictions=predict(dataset,'VALIDATION',release,out,spec.reference,check)
                truth=load_answers(dataset,manifest,'VALIDATION',inputs)
                rows=[{'id':r['id'],'text':r['text'],'result':r['result'],'expected':{k:truth[r['id']]['target'][k] for k in __import__('semantic_pipeline.schema',fromlist=['PREDICATES']).PREDICATES}} for r in predictions]
                metrics=summarize(rows)
                report={'role':'VALIDATION','release_identity':releases.verify(release)['identity'],'metrics':metrics}
                write(out/'evaluation.json',report); releases.seal(release,out)
                reports[candidate.name]=report; candidates[candidate.name]=ident
            baseline=next(iter(reports))
            def critical_errors(report):
                return {(f['id'],f['field']) for f in report['metrics']['failures'] if f['field'] in ('votability','share_blocking','poa_required','registration_required') and f['expected'] in ('YES','VOTABLE')}
            eligible=[k for k,v in reports.items() if not critical_errors(v)-critical_errors(reports[baseline])]
            winner=max(eligible,key=lambda k:(reports[k]['metrics']['correct_assertions'],-reports[k]['metrics']['median_latency_ms']))
            report={'stage_jobs':trained,'stage_seeds':seed_stages,'candidates':candidates,'validation':reports,'selected':winner,
                    'selected_release':candidates[winner],'calibration_or_test_answers_opened':False,
                    'scope':'DEVELOPMENT_ONLY_NOT_CUSTOMER_QUALIFICATION','automation_enabled':False}
            write(root/'result.json',report);jobs.events(root,{'state':'COMPLETED','result_sha256':sha(root/'result.json')})
            return report
        except BaseException as exc:
            jobs.events(root,{'state':'INTERRUPTED' if isinstance(exc,(KeyboardInterrupt,InterruptedError)) else 'FAILED',
                             'error':type(exc).__name__+': '+str(exc),'automatic_resume':False});raise


if __name__=='__main__':
    import argparse
    p=argparse.ArgumentParser();p.add_argument('campaign');run(p.parse_args().campaign)
