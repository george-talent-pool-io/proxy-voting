"""Run real Laya against authored challenge cases; never add them to golden data."""
import argparse
import json
from pathlib import Path
from apps.api.store import dumps,now
from classifier.laya_classifier import LayaClassifier,load_config

def benchmark(output,config=None):
    fixtures=json.loads(Path('tests/fixtures/semantic.json').read_text())
    cfg=config or load_config();model=LayaClassifier(cfg)
    rows=[]
    for start in range(0,len(fixtures),cfg['batch_size']):
        chunk=fixtures[start:start+cfg['batch_size']]
        results=model.classify_batch([f['text'] for f in chunk])
        for f,r in zip(chunk,results):
            observed={**r.decision.model_dump(),'classification':r.classification.value}
            checks={k:observed[k]==v for k,v in f['expected'].items()}
            rows.append(dict(id=f['id'],tags=f['tags'],text=f['text'],expected=f['expected'],observed=observed,checks=checks,
                passed=all(checks.values()),result=r.model_dump(mode='json')))
    report={'created_at':now(),'kind':'authored semantic challenge; not customer test accuracy', 'reference_date':cfg['evaluation_date'],
        'configuration_version':model.configuration_version,'model_version':cfg['checkpoint_revision'],
        'cases':len(rows),'passed':sum(r['passed'] for r in rows),'failed':sum(not r['passed'] for r in rows),'examples':rows}
    with open(output,'x') as f:f.write(dumps(report))
    print(dumps({k:v for k,v in report.items() if k!='examples'}))
    return report
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('output');p.add_argument('--config');a=p.parse_args();benchmark(a.output,load_config(a.config) if a.config else None)
