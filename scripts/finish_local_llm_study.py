"""Wait for the prediction commit, then run dependent post-processing/checks.
This does not modify frozen inference or select models from test results.
"""
import os,subprocess,sys,time
from pathlib import Path
from semantic_pipeline.experiment import ROOT

if __name__=='__main__':
    while not (ROOT/'PREDICTION-COMMIT.json').exists():time.sleep(2)
    commands=[
        [sys.executable,'-m','semantic_pipeline.experiment','report'],
        [sys.executable,'-m','evaluation.ae_scoring'],
        [sys.executable,'-m','evaluation.ae_analysis'],
        [sys.executable,'-m','evaluation.ae_date_ablation'],
        [sys.executable,'-m','scripts.verify_local_llm_experiment'],
        [sys.executable,'-m','evaluation.ae_oracle'],
        [sys.executable,'-m','evaluation.ae_reproducibility'],
    ]
    for cmd in commands:
        print('Executing:',cmd,flush=True);subprocess.run(cmd,check=True)
    env={**os.environ,'RUN_LOCAL_LLM':'1'}
    subprocess.run([sys.executable,'-m','pytest','tests/classifier/test_real_local_llm.py','-q'],env=env,check=True)
    print('Post-processing and real-model checks completed',flush=True)
