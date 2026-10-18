"""Exercise the actual customer orchestrator with real registered models.

Reuses completed weights, runs four AI-labelled validation events, seals the
release, never opens calibration/frozen answers and never promotes automation.
"""
import argparse
from dataclasses import asdict
from training.framework import jobs
from production import learning
from fast_cascade.routing import Policy


def run(ident,qwen_seed,laya_job):
    spec={'bundle_id':'event-loop-v1','dataset_id':'event-loop-isolated-v2',
          'actor':'AI framework integration qualification','max_seconds':3600,
          'stages':[{'name':'specialist','reuse_job':laya_job},{'name':'generative','reuse_seed':qwen_seed}],
          'candidates':[{'name':'CASCADE_CONSERVATIVE','mode':'LAYA_QWEN','laya_stage':'specialist','llm_stage':'generative',
                         'policy':asdict(Policy('REAL_INTEGRATION_CONSERVATIVE',1.,1.,1.,1.,1.,False,False))}]}
    root=jobs.member('campaigns',ident)
    learning.prepare(spec,root)
    return learning.run(root)

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('id');p.add_argument('--qwen-seed',required=True);p.add_argument('--laya-job',required=True)
    a=p.parse_args();run(a.id,a.qwen_seed,a.laya_job)
