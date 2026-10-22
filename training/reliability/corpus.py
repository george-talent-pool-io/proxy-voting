"""Disclosed, fact-first controlled population for real-model engineering.

Compositions and lexical duplicate components are held out. Linguistic atoms
are reused: these are not independent real-world linguistic families or expert
truth. In particular, no customer accuracy/automation certificate can follow.
"""
import json
import random
from collections import Counter
from pathlib import Path
from classifier.preprocessing import source_hash, normalise
from classifier.deadlines import extract_deadline
from semantic_pipeline.schema import PREDICATES, RESTRICTIONS, SemanticResult
from semantic_pipeline.decision import decide
from training.split import duplicate_groups
from training.framework.bundle import write,jsonl,sha,create_bundle
from training.framework.schema import Example
from training.reliability import material as m

VERSION='balanced-notice-compositions-v1'
REFERENCE='2026-10-22T12:00:00+00:00'
ROLES=('TRAIN','VALIDATION','LAYA_STAGE','CASCADE_FINAL','FROZEN_TEST')


def make(seed):
    rng=random.Random(seed)
    vote=rng.choices(['VOTABLE','NOT_VOTABLE','UNCERTAIN'],weights=[.40,.35,.25])[0]
    facts={k:'NO' for k in RESTRICTIONS};evidence={k:[] for k in PREDICATES}
    intro=rng.choice(m.VOTE if vote=='VOTABLE' else m.NO_VOTE if vote=='NOT_VOTABLE' else m.UNCERTAIN)
    facts['votability']=vote;evidence['votability']=[intro];clauses=[intro]
    states={}
    if vote=='VOTABLE':
        for key in RESTRICTIONS:
            state=rng.choices(['YES','NO_UNSTATED','NO_WAIVED','NO_OPTIONAL','UNKNOWN'],[.30,.25,.23,.10,.12])[0]
            facts[key]='NO' if state.startswith('NO_') else state;states[key]=state
            if state=='NO_UNSTATED':continue
            subject=rng.choice(m.SUBJECT[key])
            text=(rng.choice(m.POSITIVE[key]) if state=='YES' else
                  rng.choice(m.UNRESOLVED).format(subject=subject) if state=='UNKNOWN' else
                  (subject+' is optional and is not a prerequisite for voting.') if state=='NO_OPTIONAL' else
                  rng.choice(m.NEGATIVE).format(subject=subject))
            text=text[0].upper()+text[1:];clauses.append(text);evidence[key]=[text]
    # Clear/no-vote/ambiguous classes all receive short and long formats.
    length=rng.choices(['SHORT','MEDIUM','LONG'],[.50,.35,.15])[0]
    if length=='MEDIUM':clauses += rng.sample(m.DISTRACTORS,2)
    elif length=='LONG':clauses += rng.sample(m.DISTRACTORS,8)
    deadline=None;deadline_status='UNKNOWN'
    if vote=='VOTABLE':
        when=rng.choices(['OPEN','PASSED','UNKNOWN'],[.65,.25,.10])[0]
        if when!='UNKNOWN':
            deadline=('Voting instructions must reach the custodian by 26 November 2026 at 16:00 UTC.' if when=='OPEN' else
                      'The custodian voting deadline was 15 September 2026 at 12:00 UTC.')
            clauses.append(deadline);deadline_status=when
    # Keep the opportunity before conditions, with varied remaining ordering.
    tail=clauses[1:];rng.shuffle(tail);clauses=clauses[:1]+tail
    layout=rng.choice(['PARAGRAPHS','SENTENCES','BULLETS','OPERATIONAL'])
    separator='\n\n' if layout=='PARAGRAPHS' else ' ' if layout=='SENTENCES' else '\n'
    text=separator.join(('- '+c if layout=='BULLETS' else c) for c in clauses)
    if layout=='OPERATIONAL':text='Custody operations communication\n'+text
    target={**facts,'deadline_information':{'deadline_mentioned':deadline is not None,'deadline_text':deadline},
            'evidence':evidence,'ambiguities':[]}
    SemanticResult.model_validate(target)
    if any(q not in text for qs in evidence.values() for q in qs):raise ValueError('Construction evidence drift')
    observed=extract_deadline(text,REFERENCE)['status']
    if observed!=deadline_status:raise ValueError('Construction deadline not deterministically recoverable')
    final=decide({k:{'value':facts[k]} for k in PREDICATES},{'status':deadline_status})['classification']
    return {'id':f'RC1-{seed:07d}','text':text,'source_hash':source_hash(text),
            'expected':facts,'target':target,'language':'en','evaluation_time':REFERENCE,
            'deadline_status':deadline_status,'final_status':final,'states':states,
            'length_kind':length,'layout':layout,'origin':'AI_AUTHORED','generator_model':'Codex/GPT-6',
            'prompt_version':VERSION,'seed':seed,'source_type':'AI_AUTHORED_CONTROLLED_COMPOSITION'}


def build(output,count=3200):
    root=Path(output);root.mkdir(parents=True,exist_ok=False)
    rows=[make(715200+i) for i in range(count)]
    groups=duplicate_groups(rows)
    # Entire exact/normalised/near-duplicate components share one role/fold.
    for row,group in zip(rows,groups):
        f=int(source_hash(VERSION+group)[:12],16)/16**12
        row['role']='TRAIN' if f<.25 else 'VALIDATION' if f<.375 else 'LAYA_STAGE' if f<.625 else 'CASCADE_FINAL' if f<.875 else 'FROZEN_TEST'
        row['group']=group;row['generation_family']=group
        row['fold']='FIT' if int(source_hash('cal-fold-'+group)[:8],16)%3 else 'EVALUATION'
    manifest={'version':VERSION,'reference':REFERENCE,'count':len(rows),'groups':len(set(groups)),'files':{},
              'construction_sha256':sha(__file__),'material_sha256':sha(m.__file__),
              'label_origin':'AI_AUTHORED','customer_accuracy':None,'automation_enabled':False,
              'limitations':['Controlled synthetic notice compositions, not a representative customer sample.',
                            'Shared authored linguistic atoms across roles; composition/lexical isolation does not prove independent linguistic generalisation.',
                            'English only. Difficult/UNKNOWN conditions are deliberately oversampled; review rate is not a customer forecast.']}
    for role in ROLES:
        selected=[r for r in rows if r['role']==role]
        directory=root/('development' if role in ('TRAIN','VALIDATION') else 'private');directory.mkdir(exist_ok=True)
        source=root/(role+'.inputs.jsonl');key=directory/(role+'.labels.jsonl')
        jsonl(source,[{k:r[k] for k in ('id','text','source_hash','language','evaluation_time','role','group','fold')} for r in selected])
        jsonl(key,selected)
        manifest['files'][role]={'inputs':source.name,'inputs_sha256':sha(source),'labels':str(key.relative_to(root)),'labels_sha256':sha(key),
          'n':len(selected),'groups':len({r['group'] for r in selected}),
          'labels_by_field':{k:dict(Counter(r['expected'][k] for r in selected)) for k in PREDICATES},
          'lengths':dict(Counter(r['length_kind'] for r in selected))}
    write(root/'manifest.json',manifest)
    return manifest


def development_bundle(corpus,output):
    root=Path(corpus);manifest=json.loads((root/'manifest.json').read_text());examples=[]
    for role in ('TRAIN','VALIDATION'):
        entry=manifest['files'][role];path=root/entry['labels']
        if sha(path)!=entry['labels_sha256']:raise ValueError('Development answer drift')
        for line in path.read_text().splitlines():
            r=json.loads(line)
            examples.append(Example(id=r['id'],text=r['text'],source_hash=r['source_hash'],split=role,
              group_id=r['group'],generation_family=r['generation_family'],target=r['target'],
              provenance={'origin':'AI_AUTHORED','author':'Codex','model_id':'GPT-6',
                 'method':'Fact-first controlled composition; declared shared language atoms',
                 'source_reference':str(root/'manifest.json'),'revision':VERSION}))
    return create_bundle(examples,output,source_manifest={'sha256':sha(root/'manifest.json'),
              'roles_read':['TRAIN','VALIDATION'],'protected_answers_opened':False})


if __name__=='__main__':
    import argparse
    parser=argparse.ArgumentParser();parser.add_argument('output');parser.add_argument('--count',type=int,default=3200)
    args=parser.parse_args();result=build(args.output,args.count)
    print(json.dumps({k:{'n':v['n'],'groups':v['groups']} for k,v in result['files'].items()}))
