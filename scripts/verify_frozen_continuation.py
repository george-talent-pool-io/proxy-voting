"""Real customer-style continuation from frozen Laya and Qwen derivatives.

AI-only qualification artifacts. A tiny continuation proves optimizer/lineage
mechanics, not further semantic improvement. Frozen parent bytes must not change.
"""
import json
from pathlib import Path
from training.framework import jobs, seeds
from training.framework.bundle import create_bundle, sha, write
from training.framework.schema import Example


def run(output,corpus,laya_job):
    output=Path(output);output.mkdir(parents=True,exist_ok=False)
    manifest=json.loads((Path(corpus)/'manifest.json').read_text());examples=[]
    for role in ('TRAIN','VALIDATION'):
        entry=manifest['files'][role];path=Path(corpus)/entry['labels']
        if sha(path)!=entry['labels_sha256']:raise ValueError('Development label drift')
        rows=[json.loads(line) for line in path.read_text().splitlines()]
        chosen=[];groups=set()
        for row in rows:
            if row['group'] in groups:continue
            chosen.append(row);groups.add(row['group'])
            if len(chosen)==2:break
        for row in chosen:
            target={**row['expected'],'evidence':row['evidence_truth'],'ambiguities':[],
                    'deadline_information':{'deadline_mentioned':True,'deadline_text':'Voting instructions must reach the custodian by 24 November 2026 at 17:00 UTC.'}}
            examples.append(Example(id=row['id'],text=row['text'],source_hash=row['source_hash'],group_id=row['group'],
                generation_family=row['group'],split=role,target=target,
                provenance={'origin':'AI_AUTHORED','author':'Codex','model_id':'GPT-6','method':'Controlled fact-first composition',
                            'source_reference':manifest['version'],'revision':'frozen-continuation-v1'}))
    bundle=jobs.member('bundles',output.name);create_bundle(examples,bundle)
    results={}
    for family,parent_job in [('LAYA',laya_job),('QWEN',jobs.member('jobs','48471af2-1c7e-4ab5-ab51-df5b5109e369'))]:
        seed_path=jobs.member('seeds',output.name+'-'+family)
        parent=seeds.export_derivative(parent_job,seed_path,origin='AI_TEST_DERIVATIVE')
        overrides=({'epochs':1,'batch_size':2,'gradient_accumulation':1,'encoder_learning_rate':.000025,
                    'learning_rate':.0001,'freeze_encoder':False,'laya_gradient_checkpointing':True,
                    'laya_sdk_validation':False,'mps_memory_fraction':.45} if family=='LAYA' else
                   {'max_steps':1,'batch_size':1,'gradient_accumulation':1})
        spec=seeds.training_spec(seed_path,overrides)
        job=jobs.member('jobs',output.name+'-'+family)
        jobs.prepare(bundle,spec,job)
        model=jobs.execute(job)
        after=seeds.verify(seed_path)
        if parent['identity']!=after['identity']:raise ValueError('Parent changed during customer continuation')
        results[family]={'parent_identity':parent['identity'],'parent_unchanged':True,'job':str(job),
                         'result':json.loads((job/'result.json').read_text()),'model_manifest_sha256':sha(job/'model-manifest.json')}
        write(output/(family+'.json'),results[family])
    write(output/'result.json',{'results':results,'scope':'AI_TEST_CONTINUATION_MECHANICS_ONLY','automation_enabled':False,
                               'eligible_training_examples':2,'new_validation_examples':2,
                               'qwen_optimizer_steps':1,'qwen_examples_consumed':1,
                               'test_models_in_production_delivery':False})
    return results

if __name__=='__main__':
    import argparse
    p=argparse.ArgumentParser();p.add_argument('output');p.add_argument('--corpus',required=True);p.add_argument('--laya-job',required=True)
    a=p.parse_args();run(a.output,a.corpus,Path(a.laya_job))
