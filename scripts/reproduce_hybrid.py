"""Reproduce into a new directory without overwriting any historical artifact."""
import argparse,json,os,subprocess,sys
from pathlib import Path
SOURCE=Path(__file__).resolve().parents[1]

def prepare(destination,reuse_checkpoint=False):
    target=Path(destination).expanduser().resolve()
    if target.exists():raise ValueError('Destination must not exist; previous runs are never overwritten')
    target.mkdir(parents=True)
    for name in ['apps','classifier','training','hybrid','evaluation','scripts','tests']:(target/name).symlink_to(SOURCE/name,target_is_directory=True)
    for name in ['data/models','data/experiments','data/normalised','data/reports','artifacts']:(target/name).mkdir(parents=True,exist_ok=True)
    (target/'data/reports/ISO15022_PROXY_RESEARCH.md').symlink_to(SOURCE/'data/reports/ISO15022_PROXY_RESEARCH.md')
    for name in ['data/models/laya','data/training']:(target/name).symlink_to(SOURCE/name,target_is_directory=True)
    (target/'data/normalised/public.jsonl').symlink_to(SOURCE/'data/normalised/public.jsonl')
    (target/'data/experiments/supplied-synthetic-v1').symlink_to(SOURCE/'data/experiments/supplied-synthetic-v1',target_is_directory=True)
    if reuse_checkpoint:
        for name in ['data/models/narrow-v1','data/experiments/narrow-v1']:(target/name).symlink_to(SOURCE/name,target_is_directory=True)
    commands=[['-m','hybrid.corpus'],['-m','scripts.expand_iso_fixtures']]
    if not reuse_checkpoint:commands +=[['-m','training.narrow','prepare'],['-m','training.narrow','train']]
    commands +=[['-c',"from pathlib import Path; Path('data/experiments/iso-hybrid-v1').mkdir()"],['-m','scripts.hybrid_benchmark','freeze'],['-m','scripts.hybrid_benchmark','base'],['-m','scripts.hybrid_benchmark','fine','--model-path','data/models/narrow-v1'],['-m','scripts.audit_hybrid_routing'],['-m','scripts.verify_iso'],['-m','scripts.seed_iso_demo']]
    # Detector artifact independently reconstructed; no preexisting experiment writes.
    commands.insert(-3,['-c',"import json,hashlib,time; from collections import Counter; from pathlib import Path; from hybrid.parser import parse,VERSION; rows=[json.loads(x) for x in Path('data/normalised/public.jsonl').read_text().splitlines()]; start=time.perf_counter(); results=[parse(r['text']) for r in rows]; summary={'parser_version':VERSION,'records':len(rows),'counts':dict(Counter(p['kind'] for p in results)),'tags':dict(Counter(f['tag'] for p in results for f in p['fields'])),'failed_rows':0,'structured_values':sum(f['route']=='STRUCTURED_FACTS' and f['name']!='sequence' for p in results for f in p['facts']),'laya_executions':0,'llm_escalations':0,'elapsed_seconds':time.perf_counter()-start}; Path('data/experiments/iso-hybrid-v1/public-parser-summary.json').write_text(json.dumps(summary,indent=2))"])
    commands.append(['-m','scripts.report_iso_hybrid'])
    (target/'reproduction-plan.json').write_text(json.dumps({'source_code':str(SOURCE),'reuse_checkpoint':reuse_checkpoint,'commands':commands,'note':'Fresh outputs; shared source code and immutable source/model artifacts. No original answer key or test labels read for training/tuning.'},indent=2))
    return target,commands

def main():
    p=argparse.ArgumentParser();p.add_argument('destination');p.add_argument('--reuse-checkpoint',action='store_true');p.add_argument('--prepare-only',action='store_true');a=p.parse_args();target,commands=prepare(a.destination,a.reuse_checkpoint)
    print('Fresh reproduction workspace:',target,flush=True)
    if not a.prepare_only:
        for i,command in enumerate(commands):
            print('Step',i+1,command[:3],flush=True)
            with (target/'artifacts'/f'reproduction-{i+1:02d}.log').open('x') as f:subprocess.run([sys.executable,*command],cwd=target,env={**os.environ,'LAYA_DEVICE':'cpu'},stdout=f,stderr=subprocess.STDOUT,check=True)
if __name__=='__main__':main()
