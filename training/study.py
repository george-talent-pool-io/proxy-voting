"""Freeze study membership before annotation. Labels remain append-only review revisions."""
import hashlib
import json
import math
from collections import Counter,defaultdict
from pathlib import Path
from apps.api import store
from classifier.preprocessing import normalise,source_hash
from training.split import verify_isolation

STUDY_ID='laya-supervised-v1'
CHALLENGE=Path(__file__).resolve().parents[1]/'tests/fixtures/semantic.json'

def fingerprint(value):return hashlib.sha256(store.dumps(value).encode()).hexdigest()

def install(c):
    c.executescript('''CREATE TABLE IF NOT EXISTS studies(id TEXT PRIMARY KEY,created_at TEXT NOT NULL,manifest TEXT NOT NULL,sha256 TEXT NOT NULL);
CREATE TRIGGER IF NOT EXISTS immutable_studies_update BEFORE UPDATE ON studies BEGIN SELECT RAISE(ABORT,'Frozen study is immutable'); END;
CREATE TRIGGER IF NOT EXISTS immutable_studies_delete BEFORE DELETE ON studies BEGIN SELECT RAISE(ABORT,'Frozen study is immutable'); END;
CREATE TABLE IF NOT EXISTS study_label_locks(study_id TEXT PRIMARY KEY REFERENCES studies(id),created_at TEXT NOT NULL,manifest TEXT NOT NULL,sha256 TEXT NOT NULL);
CREATE TRIGGER IF NOT EXISTS immutable_label_locks_update BEFORE UPDATE ON study_label_locks BEGIN SELECT RAISE(ABORT,'Frozen labels are immutable'); END;
CREATE TRIGGER IF NOT EXISTS immutable_label_locks_delete BEFORE DELETE ON study_label_locks BEGIN SELECT RAISE(ABORT,'Frozen labels are immutable'); END;''')

def load_study(path=None,study_id=STUDY_ID):
    with store.connect(path) as c:
        if not c.execute("SELECT name FROM sqlite_master WHERE name='studies'").fetchone():return None
        row=c.execute('SELECT * FROM studies WHERE id=?',(study_id,)).fetchone()
        if not row:return None
        m=json.loads(row['manifest'])
        if fingerprint(m)!=row['sha256']:raise ValueError('Frozen study checksum mismatch')
        return m

def challenge_guard(records):
    cases=json.loads(CHALLENGE.read_text())
    blocked_ids={x['id'] for x in cases};blocked_hashes={source_hash(normalise(x['text'])) for x in cases}
    for r in records:
        if r.get('record_id',r.get('id')) in blocked_ids or r.get('normalised_hash') in blocked_hashes:
            raise ValueError('Semantic challenge set must never enter training or validation')

def dimensions(r):
    m=json.loads(r['metadata']);a=json.loads(r['result']) if r.get('result') else None
    conf=a['confidence'] if a else 0
    d=a['decision'] if a else {}
    return {'category':a['classification'] if a else 'UNCLASSIFIED','confidence':'low' if conf<.5 else 'medium' if conf<.7 else 'high',
      **{k:m.get(k) or 'UNKNOWN' for k in ['event_type','market','country','language']},
      'length':'short' if len(r['text'])<500 else 'medium' if len(r['text'])<4000 else 'long',
      'restriction':'yes' if any(d.get(k) is True for k in ['share_blocking','poa_required','other_restriction']) else 'unknown' if any(d.get(k) is None for k in ['share_blocking','poa_required','other_restriction']) else 'no',
      'conflict':'yes' if a and any('Conflicting' in x for x in a['review_reasons']) else 'no',
      'unusual':'yes' if a and (a['usage'].get('truncated') or d.get('votable')=='UNCERTAIN') else 'no'}

def create_study(output,path=None,study_id=STUDY_ID,targets=None):
    targets=targets or {'train':600,'validation':200,'test':200}
    output=Path(output)
    if output.exists():raise ValueError('Study output already exists')
    with store.connect(path) as c:
        install(c)
        if c.execute('SELECT id FROM studies WHERE id=?',(study_id,)).fetchone():raise ValueError('Study already frozen')
        if c.execute("SELECT count(*) FROM reviews WHERE action='VERIFY'").fetchone()[0]:raise ValueError('Freeze membership before creating verified study labels')
        run=c.execute("SELECT * FROM runs WHERE status='COMPLETED' ORDER BY created_at DESC LIMIT 1").fetchone()
        # Older run ledgers use COMPLETE; accept only a complete, all-row run.
        if not run:run=c.execute("SELECT * FROM runs WHERE status='COMPLETE' ORDER BY created_at DESC LIMIT 1").fetchone()
        if not run:raise ValueError('Complete a baseline first')
        rows=[dict(r) for r in c.execute('SELECT n.*,p.result FROM notices n LEFT JOIN predictions p ON p.record_id=n.id AND p.run_id=? ORDER BY n.id',(run['id'],))]
        if any(not r['result'] for r in rows):raise ValueError('Baseline has missing predictions')
        verify_isolation(rows)
        groups=defaultdict(list)
        for r in rows:r['strata']=dimensions(r);groups[r['group_id']].append(r)
        candidates=[]
        for g,items in sorted(groups.items()):
            # Prefer informative excerpts within a filing, not publisher extraction fields.
            def priority(r):
                d=r['strata'];return (int(d['restriction']=='yes')+int(d['conflict']=='yes')+int(d['unusual']=='yes'),-json.loads(r['result'])['confidence'],fingerprint(r['id']))
            candidates.append(max(items,key=priority))
        selected=[]
        for split,target in targets.items():
            pool=[r for r in candidates if r['split']==split]
            if len(pool)<target:raise ValueError(f'Not enough independent {split} groups for target {target}')
            population=Counter((k,v) for r in pool for k,v in r['strata'].items());counts=Counter()
            for _ in range(target):
                def gain(r):
                    s=r['strata']
                    diversity=sum(1/(1+counts[k,v])/math.sqrt(population[k,v]) for k,v in s.items())
                    oversample=.05*(int(s['confidence']=='low')+int(s['restriction']=='yes')+int(s['conflict']=='yes')+int(s['unusual']=='yes'))
                    return diversity+oversample,fingerprint(r['id'])
                best=max(pool,key=gain);pool.remove(best);counts.update(best['strata'].items());selected.append(best['id'])
        memberships=[dict(record_id=r['id'],source_hash=r['source_hash'],normalised_hash=source_hash(normalise(r['text'])),group_id=r['group_id'],split=r['split'],partition={'train':'TRAIN','validation':'VALIDATION','test':'FROZEN_TEST'}[r['split']],source_file=json.loads(r['metadata']).get('source_file'),selected=r['id'] in selected,strata=r['strata']) for r in rows]
        challenge_guard(memberships)
        manifest={'id':study_id,'created_at':store.now(),'baseline_run_id':run['id'],'baseline_config_version':run['config_version'],'seed':'laya-voting-2026-v1','sampling':'Deterministic greedy marginal diversity with rare strata and low-confidence/restriction/conflict oversampling; one excerpt per duplicate/filing group. Not a population-random sample.',
          'targets':targets,'challenge_sha256':hashlib.sha256(CHALLENGE.read_bytes()).hexdigest(),'challenge_role':'REGRESSION_ONLY_NEVER_TRAIN','records':memberships,
          'limitations':['Unknown country/market are retained as UNKNOWN, never inferred.','This enriched cohort estimates cohort performance, not population prevalence.','Independent review and adjudication required; no AI labels are golden.','Frozen test membership is public for audit; training code excludes its entire groups.']}
        digest=fingerprint(manifest)
        c.execute('INSERT INTO studies VALUES(?,?,?,?)',(study_id,manifest['created_at'],store.dumps(manifest),digest))
    output.mkdir(parents=True)
    (output/'membership.json').write_text(store.dumps(manifest)+'\n')
    (output/'membership.sha256').write_text(digest+'\n')
    byid={r['id']:r for r in rows}
    (output/'labelling_queue.jsonl').write_text(''.join(store.dumps({'record_id':i,'text':byid[i]['text'],'source_hash':byid[i]['source_hash'],'split':byid[i]['split'],'group_id':byid[i]['group_id'],'strata':byid[i]['strata'],'review_status':'UNLABELLED'})+'\n' for i in selected))
    return manifest

def lock_test_labels(path=None,study_id=STUDY_ID):
    """Pin actual human review revisions once complete. Later corrections require a new study."""
    study=load_study(path,study_id)
    if not study:raise ValueError('No frozen study')
    ids=[r['record_id'] for r in study['records'] if r['selected'] and r['split']=='test']
    with store.connect(path) as c:
        install(c);labels=[]
        for rid in ids:
            r=store.latest_review(c,rid)
            if not r or r['action']!='VERIFY':raise ValueError('All selected frozen-test records need human verification')
            context=json.loads(r['context'])
            if not context.get('domain_expert_attested') or not context.get('blind_review'):raise ValueError('Frozen test requires blind domain-expert attestation')
            labels.append({'record_id':rid,'revision':r['id'],'label':r['label'],'reviewer':r['reviewer'],'context':context})
        manifest={'study_id':study_id,'study_sha256':fingerprint(study),'labels':labels}
        c.execute('INSERT INTO study_label_locks VALUES(?,?,?,?)',(study_id,store.now(),store.dumps(manifest),fingerprint(manifest)))
    return manifest

if __name__=='__main__':
    import argparse
    p=argparse.ArgumentParser();p.add_argument('output');p.add_argument('--study-id',default=STUDY_ID);a=p.parse_args()
    m=create_study(a.output,study_id=a.study_id);print({'id':m['id'],'targets':m['targets'],'members':len(m['records'])})
