"""Small real-model reproduction check in a separate database; no golden labels."""
import json
from pathlib import Path
from apps.api import store
from scripts.run_batch import run_batch

def main(name="real-reproduction"):
    if not name.replace("-", "").isalnum():raise ValueError("Use a simple artifact name")
    path=Path(f'artifacts/{name}.sqlite')
    if path.exists():raise ValueError('Reproduction artifact exists; preserve it or choose a new workspace')
    rows=[json.loads(x) for x in Path('data/normalised/public.jsonl').read_text().splitlines()][:4]
    inputs=Path(f'artifacts/{name}-input.jsonl');inputs.write_text(''.join(store.dumps(r)+'\n' for r in rows))
    store.initialise(str(path));store.import_normalised(inputs,str(path))
    first=run_batch(str(path));second=run_batch(str(path),reproduce=first)
    with store.connect(str(path)) as c:
        a={r['record_id']:json.loads(r['result']) for r in c.execute('SELECT * FROM predictions WHERE run_id=?',(first,))}
        b={r['record_id']:json.loads(r['result']) for r in c.execute('SELECT * FROM predictions WHERE run_id=?',(second,))}
        comparison=[{'id':k,'same_factors':a[k]['decision']==b[k]['decision'],'same_scores':a[k]['scores']==b[k]['scores']} for k in a]
        runs=[dict(r) for r in c.execute('SELECT * FROM runs')]
    result={'kind':'actual local Laya reproduction, no test double','first_run':first,'second_run':second,'records':len(rows),
        'same_dataset_hash':runs[0]['dataset_hash']==runs[1]['dataset_hash'],'same_configuration_hash':runs[0]['config_version']==runs[1]['config_version'],
        'comparisons':comparison,'all_equal':all(r['same_factors'] and r['same_scores'] for r in comparison)}
    with open(f'artifacts/{name}.json','x') as f:f.write(store.dumps(result))
    if not result['all_equal']:raise RuntimeError('Reproduced scores differ; inspect report')
    print(store.dumps(result))
if __name__=='__main__':
    import argparse
    p=argparse.ArgumentParser();p.add_argument('--name',default='real-reproduction');a=p.parse_args();main(a.name)
