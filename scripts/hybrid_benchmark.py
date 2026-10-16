"""Persist narrow-Laya challenge outputs and synthetic validation diagnostics.
No original synthetic test/answer-key access; no training on challenges/ISO fixtures.
"""
import argparse,hashlib,json,os,time
from pathlib import Path
from hybrid.pipeline import analyse
from hybrid.semantics import NarrowLaya,aggregate
from hybrid.rules import decide
OUT=Path('data/experiments/iso-hybrid-v1')

def freeze():
    files={str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(Path('hybrid').glob('*.py'))}
    files['hybrid/minimal_pairs.json']=hashlib.sha256(Path('hybrid/minimal_pairs.json').read_bytes()).hexdigest()
    files['scripts/hybrid_benchmark.py']=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    with (OUT/'PIPELINE-FREEZE.json').open('x') as f:json.dump({'files':files,'evaluation_time':'2026-10-16T12:00:00+00:00','automation_enabled':False,'selection':'No challenge-driven changes. Three aggregation strategies diagnostic only; default conflict_abstain fixed before evaluation.'},f,indent=2)

def run(name,model_path):
    from sklearn.metrics import accuracy_score,f1_score,confusion_matrix
    freeze=json.loads((OUT/'PIPELINE-FREEZE.json').read_text())
    for path,digest in freeze['files'].items():
        if hashlib.sha256(Path(path).read_bytes()).hexdigest()!=digest:raise ValueError('Frozen hybrid code changed; create a new experiment')
    target=OUT/f'{name}-challenge.jsonl';model=NarrowLaya(model_path);fixtures=json.loads(Path('tests/fixtures/semantic.json').read_text());n=0
    with target.open('x') as f:
        for row in fixtures:
            result=analyse(row['text'],model,evaluation_time='2026-10-16T12:00:00+00:00')
            observed={**result['decision_facts'],'classification':result['decision']['classification']}
            # Legacy authored 'other' includes the expanded specific restrictions.
            vals=[observed.get(k,'UNKNOWN') for k in ['registration_required','beneficial_owner_disclosure_required','split_voting_restricted','securities_lending_recall_required','other_voting_restriction']]
            observed['other_restriction']=True if 'YES' in vals else False if all(v=='NO' for v in vals) else None
            for key in ['share_blocking','poa_required']:observed[key]=True if observed[key]=='YES' else False if observed[key]=='NO' else None
            checks={k:observed.get(k)==v for k,v in row['expected'].items()}
            output={'id':row['id'],'text':row['text'],'expected':row['expected'],'observed':observed,'checks':checks,'passed':all(checks.values()),'tags':row['tags'],'result':result}
            f.write(json.dumps(output,allow_nan=False)+'\n');f.flush();os.fsync(f.fileno());n+=output['passed'];print(name,row['id'],output['passed'],flush=True)
    rows=[json.loads(x) for x in target.read_text().splitlines()]
    summary={'name':name,'cases':len(rows),'passed':n,'failed':len(rows)-n,'model_version':model.model_version,'configuration_version':model.config_hash,'scope':'Authored regression challenge; partial expected labels, not independent customer accuracy','fields':{},'aggregation_comparison':{}}
    for key in ['votable','share_blocking','poa_required','other_restriction','deadline_status']:
        use=[r for r in rows if key in r['expected']];truth=[str(r['expected'][key]) for r in use];pred=[str(r['observed'][key]) for r in use];labels=sorted(set(truth+pred))
        summary['fields'][key]={'n':len(use),'accuracy':float(accuracy_score(truth,pred)) if use else None,'macro_f1':float(f1_score(truth,pred,labels=labels,average='macro',zero_division=0)) if use else None,'labels':labels,'confusion_matrix':confusion_matrix(truth,pred,labels=labels).tolist() if use else []}
    for strategy in ['conflict_abstain','any_positive','max_confidence']:
        counts={k:{'correct':0,'n':0} for k in ['votable','share_blocking','poa_required']}
        for row in rows:
            for key in counts:
                if key not in row['expected']:continue
                p=aggregate(row['result']['semantic_analysis']['passage_predictions'].get(key,[]),strategy)['value']
                if key!='votable':p=True if p=='YES' else False if p=='NO' else None
                counts[key]['n']+=1;counts[key]['correct']+=p==row['expected'][key]
        summary['aggregation_comparison'][strategy]=counts
    with (OUT/f'{name}-challenge-summary.json').open('x') as f:json.dump(summary,f,indent=2)
    # Validation only, existing known AI-synthetic labels, three compatible targets.
    from training.synthetic_protocol import rows as supplied
    validation=[]
    with (OUT/f'{name}-validation.jsonl').open('x') as f:
        for r in supplied('validation'):
            result=model.analyse(r['text'],requested_predicates=['votable','share_blocking','poa_required'])
            expected={'votable':{'VOTABLE':'YES','NOT_VOTABLE':'NO','UNCERTAIN':'UNCERTAIN'}[r['votability']],**{k:r[k] for k in ['share_blocking','poa_required']}}
            out={'id':r['id'],'expected':expected,'result':result};validation.append(out);f.write(json.dumps(out,allow_nan=False)+'\n');f.flush()
    val={}
    for key in ['votable','share_blocking','poa_required']:
        y=[r['expected'][key] for r in validation];p=[r['result']['predicates'][key]['value'] for r in validation];labels=sorted(set(y+p));val[key]={'n':100,'accuracy':float(accuracy_score(y,p)),'macro_f1':float(f1_score(y,p,labels=labels,average='macro',zero_division=0)),'labels':labels,'confusion_matrix':confusion_matrix(y,p,labels=labels).tolist()}
    (OUT/f'{name}-validation-summary.json').write_text(json.dumps(val,indent=2))
    pairs=[]
    for r in json.loads(Path('hybrid/minimal_pairs.json').read_text()):
        result=model.analyse(r['text']);checks={k:result['predicates'][k]['value']==v for k,v in r['expected'].items()}
        pairs.append({**r,'result':result,'checks':checks,'passed':all(checks.values())})
    (OUT/f'{name}-minimal-pairs.json').write_text(json.dumps({'kind':'New authored diagnostic/adversarial cases; not human customer labels; never training','passed':sum(r['passed'] for r in pairs),'n':len(pairs),'rows':pairs},indent=2))
    # Reload consistency on same passage sequence, exact native probabilities.
    before=model.analyse(fixtures[0]['text']);del model
    after=NarrowLaya(model_path).analyse(fixtures[0]['text'])
    stable=lambda r:{k:{x:v for x,v in a.items() if x not in []} for k,a in r['predicates'].items()}
    if stable(before)!=stable(after):raise AssertionError('Checkpoint reload changed predictions')
    (OUT/f'{name}-reload.json').write_text(json.dumps({'identical':True,'source_hash':hashlib.sha256(fixtures[0]['text'].encode()).hexdigest()}))
    print(summary,flush=True)
if __name__=='__main__':
    a=argparse.ArgumentParser();a.add_argument('name');a.add_argument('--model-path');args=a.parse_args()
    if args.name=='freeze':freeze()
    else:run(args.name,args.model_path or 'data/models/laya/multilingual')
