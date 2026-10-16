"""Inspect supplied training ZIP without reading held-out answer keys."""
import csv,io,json,hashlib
from zipfile import ZipFile
from collections import Counter,defaultdict
from pathlib import Path
from classifier.preprocessing import source_hash,normalise,shingles
from training.split import duplicate_groups

def read_zip():
    with ZipFile('data/training/laya_voting_synthetic_500.zip') as z:
        rows=[]
        for name,split in [('synthetic_train_300.csv','train'),('synthetic_validation_100.csv','validation'),('synthetic_frozen_test_100_BLIND.csv','test')]:
            rows.extend({**r,'split':split} for r in csv.DictReader(io.StringIO(z.read(name).decode('utf-8-sig'))))
        return rows

def audit():
    rows=read_zip();groups=duplicate_groups(rows);exact=defaultdict(list);near=defaultdict(list)
    for r,g in zip(rows,groups):
        r['group_id']=g;r['source_hash']=source_hash(r['text']);r['normalised_hash']=source_hash(normalise(r['text']))
        if r['source_hash']!=r['text_sha256']:raise ValueError('Supplied text checksum mismatch')
        exact[r['normalised_hash']].append(r);near[g].append(r)
    cross=lambda pool:[{'ids':[r['id'] for r in rr],'splits':dict(Counter(r['split'] for r in rr))} for rr in pool.values() if len({r['split'] for r in rr})>1]
    seen_challenge=json.loads(Path('tests/fixtures/semantic.json').read_text());overlap=[]
    for r in rows:
        a=shingles(r['text'])
        for f in seen_challenge:
            b=shingles(f['text']);sim=len(a&b)/len(a|b) if a|b else 1
            if sim>=.85:overlap.append({'id':r['id'],'challenge':f['id'],'similarity':sim})
    conflicts=[]
    for h,rr in exact.items():
        labelled=[r for r in rr if r['split']!='test'];labels={tuple(r[k] for k in ['votability','share_blocking','poa_required','deadline_status','other_restriction']) for r in labelled}
        if len(labels)>1:conflicts.append([r['id'] for r in labelled])
    suspect=[r['id'] for r in rows if r['split']!='test' and r['deadline_status']=='OPEN' and not __import__('re').search(r'20\d{2}|\b\d{1,2}\s+(?:October|November|December)\b',r['text'])]
    out={'zip_sha256':hashlib.sha256(Path('data/training/laya_voting_synthetic_500.zip').read_bytes()).hexdigest(),'rows':len(rows),'unique_texts':len(exact),'near_groups':len(near),'cross_exact_groups':cross(exact),'cross_near_groups':cross(near),'challenge_overlap_085':overlap,'conflicting_exact_training_validation_labels':conflicts,'open_labels_without_explicit_year_or_supported_date':suspect,'heldout_answers_read':False}
    Path('data/reports/synthetic-input-audit.json').write_text(json.dumps(out,indent=2));print(json.dumps({k:len(v) if isinstance(v,list) else v for k,v in out.items()}))
    return rows,out
if __name__=='__main__':audit()
