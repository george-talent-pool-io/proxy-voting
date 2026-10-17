"""Resumable one-model-at-a-time study. Frozen labels never enter inference."""
import os,sys,time,traceback,threading
from qwen_domain.protocol import STUDY,read,append,now
from qwen_domain import study
from qwen_domain.reporting import publish_progress,reports,confidence_diagnostics

def run():
    import fcntl
    STUDY.mkdir(parents=True,exist_ok=True)
    lock=(STUDY/'RUNNER.lock').open('a');fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
    if not (STUDY/'FORMULATION-FREEZE.json').exists():study.freeze()
    study.verify();current={'stage':'Starting frozen normal/constrained study'};stop=threading.Event()
    def heartbeat():
        while not stop.wait(20):publish_progress('RUNNING',current['stage'],pid=os.getpid())
    thread=threading.Thread(target=heartbeat,daemon=True);thread.start()
    def stage(name,fn):
        current['stage']=name;publish_progress('RUNNING',name,pid=os.getpid());print(now(),name,flush=True);return fn()
    try:
        for a in study.ARCHITECTURES:stage(f'{a} / VALIDATION',lambda a=a:study.benchmark(a,'VALIDATION'))
        if not (STUDY/'TRAINING-DECISION.json').exists():stage('Validation-only training-decision gate',study.training_decision)
        for a in study.ARCHITECTURES:
            stage(f'{a} / CALIBRATION',lambda a=a:study.benchmark(a,'CALIBRATION'))
            if not (STUDY/f'{a}-CALIBRATION.json').exists():stage(f'{a} / isolated calibration fitting',lambda a=a:study.calibrate(a))
            stage(f'{a} / held-out confidence diagnostics',lambda a=a:confidence_diagnostics(a))
            stage(f'{a} / 200 x 3 repeatability',lambda a=a:study.consistency(a))
        for split in ('SYNTHETIC_FROZEN_TEST','ADVERSARIAL_TEST','OOD_TEST'):
            for a in study.ARCHITECTURES:stage(f'{a} / sealed {split} predictions',lambda a=a,s=split:study.benchmark(a,s))
        d=read(STUDY/'TRAINING-DECISION.json')
        if d['status']!='NO_FINE_TUNING_CURRENTLY_JUSTIFIED':
            stop.set();thread.join();publish_progress('TRAINING_AUDIT_REQUIRED','Predictions sealed; training target requires data/trainer audit before model selection and frozen scoring',pid=os.getpid());reports();return
        if not (STUDY/'SELECTED-MODEL-FREEZE.json').exists():stage('Freeze no-training selection',study.selection_freeze)
        if not (STUDY/'SCORED.json').exists():stage('Open frozen answers after prediction commits',study.final_score)
        for a in study.ARCHITECTURES:stage(f'{a} / unchanged authored challenge',lambda a=a:study.challenge(a))
        if not (STUDY/'SEMANTIC-CHALLENGE-SCORED.json').exists():stage('Score partial challenge assertions with exact denominators',study.score_challenge)
        for a in study.ARCHITECTURES:stage(f'{a} / public explicit partial benchmark',lambda a=a:study.public_explicit(a))
        stop.set();thread.join();publish_progress('BENCHMARK_COMPLETE','Base/constrained evaluation completed; production/customer accuracy remains unknown',pid=os.getpid());reports()
    except BaseException as e:
        stop.set();thread.join();append(STUDY/'RUNNER-FAILURES.jsonl',{'timestamp':now(),'stage':current['stage'],'error':repr(e),'traceback':traceback.format_exc()})
        publish_progress('FAILED',current['stage'],error=repr(e),pid=os.getpid());reports();raise
    finally:stop.set();lock.close()
if __name__=='__main__':run()
