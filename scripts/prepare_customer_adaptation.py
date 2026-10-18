"""Customer-style TRAIN-only adaptation; fixed validation, no held-out keys."""
import json
from pathlib import Path
from training.framework import jobs,seeds
from training.framework.bundle import create_bundle,load_bundle,sha,write
from training.framework.schema import Example


def prepare(corpus,ident):
    corpus=Path(corpus);m=json.loads((corpus/'manifest.json').read_text());data=[]
    for role in ('TRAIN','VALIDATION'):
        entry=m['files'][role];path=corpus/entry['labels']
        if sha(path)!=entry['labels_sha256']:raise ValueError('Development corpus drift')
        for row in [json.loads(line) for line in path.read_text().splitlines()]:
            target={**row['expected'],'evidence':row['evidence_truth'],'ambiguities':[],
                    'deadline_information':{'deadline_mentioned':True,'deadline_text':'Voting instructions must reach the custodian by 24 November 2026 at 17:00 UTC.'}}
            data.append(Example(id=row['id'],text=row['text'],source_hash=row['source_hash'],group_id=row['group'],
                generation_family=row['group'],split=role,target=target,
                provenance={'origin':'AI_AUTHORED','author':'Codex','model_id':'GPT-6',
                    'method':'Controlled fact-first mandatory/optional/waived/unstated composition',
                    'source_reference':m['version'],'revision':'customer-adaptation-v1'}))
    _,old=load_bundle(jobs.member('bundles','laya-domain-controlled-v1'))
    train=[e for e in old if e.split=='TRAIN']
    replay=[e for e in train if e.target.votability!='VOTABLE']
    replay += [e for e in train if e.target.votability=='VOTABLE'][:32-len(replay)]
    data += replay
    bundle=jobs.member('bundles',ident);manifest=create_bundle(data,bundle)
    spec=seeds.training_spec(jobs.member('seeds','frozen-learning-v3-laya'),
        {'epochs':4,'learning_rate':.0001,'encoder_learning_rate':.000025,'batch_size':8,
         'gradient_accumulation':2,'freeze_encoder':False,'max_length':2048,'seed':42})
    job=jobs.member('jobs',ident);plan=jobs.prepare(bundle,spec,job)
    return {'job':str(job),'bundle':str(bundle),'counts':manifest['counts'],
            'parent_identity':plan['preflight']['parent_checkpoint_identity'],'protected_roles_used':False}

if __name__=='__main__':
    import argparse
    p=argparse.ArgumentParser();p.add_argument('corpus');p.add_argument('id');a=p.parse_args()
    print(json.dumps(prepare(a.corpus,a.id)))
