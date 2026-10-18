"""Controlled composition-held-out AI corpus; deliberately NOT expert labels.

Semantic atoms are reused from the disclosed AI-authored development grammar.
This tests new combinations, calibration plumbing and selective risk, not unseen
linguistic styles or representative client generalisation. All conditions are
explicit, with exact evidence. No challenge material is read.
"""
import itertools
import json
import random
from collections import Counter
from pathlib import Path
from classifier.preprocessing import source_hash
from training.split import duplicate_groups
from training.framework.bundle import jsonl, write, sha
from semantic_pipeline.schema import RESTRICTIONS, PREDICATES
from semantic_pipeline.decision import decide
from qwen_domain.material import POSITIVE, NEGATIVE, NAMES, DISTRACTORS

VERSION = 'controlled-composition-confidence-v3'
REFERENCE = '2026-10-18T12:00:00+00:00'
OPTIONAL = {
 'share_blocking':'An investor may voluntarily freeze its position, but lodging a vote never blocks the shares.',
 'poa_required':'A power of attorney is available as an optional convenience; holders can vote without it.',
 'registration_required':'Registration for the webcast is optional and is not required for proxy voting.',
 'beneficial_owner_disclosure_required':'Providing the ultimate owner name is voluntary; anonymous voting instructions remain accepted.',
 'holding_confirmation_required':'A holdings certificate may be supplied voluntarily, but no proof of ownership is required with the ballot.',
 'split_voting_restricted':'A holder may choose one direction for all shares or split them freely; no uniform-vote requirement applies.',
 'securities_lending_recall_required':'Lending accounts may arrange a voluntary loan recall, but recall is not a condition for this vote.',
 'other_voting_restriction':'Professional-investor registration is an optional service; retail holders can vote without it.'}


def build(output, exclusion_bundle=None):
    root=Path(output); root.mkdir(parents=True,exist_ok=False)
    states=[]
    rng=random.Random(81827)
    excluded=[]
    if exclusion_bundle:
        from training.framework.bundle import load_bundle
        _, examples=load_bundle(exclusion_bundle)
        excluded=[e for e in examples if e.split=='TRAIN']
    signatures={tuple(getattr(e.target,k) for k in RESTRICTIONS) for e in excluded}
    while len(states)<1000:
        values=rng.choices(('YES','NO_WAIVED','NO_OPTIONAL','NO_UNSTATED'),weights=(.36,.24,.24,.16),k=8)
        if rng.random()<.12:values[rng.randrange(8)]='UNKNOWN'
        state=tuple(values)
        labels=tuple('NO' if v.startswith('NO_') else v for v in state)
        if state not in states and labels not in signatures:states.append(state)
    rows=[]
    for state in states:
        composition=source_hash(json.dumps(state))
        for variant in range(2):
            r=random.Random(int(composition[:12],16)+variant)
            vote=r.choice(['Shareholders may lodge their votes on the meeting resolutions through their custodian.',
                           'The current general meeting offers eligible shareholders a proxy ballot.',
                           'Voting instructions are invited for the forthcoming shareholder assembly.'])
            clauses=[vote]; evidence={'votability':[vote]}; target={'votability':'VOTABLE'}
            order=list(zip(RESTRICTIONS,state));r.shuffle(order)
            for key,value in order:
                if value=='NO_UNSTATED':target[key]='NO';evidence[key]=[];continue
                text=(r.choice(POSITIVE[key]) if value=='YES' else
                      r.choice(NEGATIVE).format(noun=NAMES[key][2]) if value=='NO_WAIVED' else
                      OPTIONAL[key] if value=='NO_OPTIONAL' else
                      'The agent has not established whether '+NAMES[key][2]+' is mandatory for this vote; confirmation is pending.')
                clauses.append(text);target[key]='NO' if value.startswith('NO_') else value;evidence[key]=[text]
            r.shuffle(clauses)
            deadline='Voting instructions must reach the custodian by 24 November 2026 at 17:00 UTC.'
            clauses += [deadline, r.choice(DISTRACTORS)]
            text=('\n' if variant==0 else '\n\n' if variant==1 else ' ').join(clauses)
            pred={k:{'value':v} for k,v in target.items()}
            rows.append({'id':f'CC-{composition[:16]}-{variant}', 'text':text,'source_hash':source_hash(text),
                         'composition_group':composition,'language':'en','evaluation_time':REFERENCE,
                         'fact_specification':dict(zip(RESTRICTIONS,state)),
                         'expected':target,'evidence_truth':evidence,'deadline_status':'OPEN',
                         'final_status':decide(pred,{'status':'OPEN'})['classification'],
                         'origin':'AI_AUTHORED','author':'Codex / GPT-6', 'generator':VERSION})
    if excluded:
        joined=duplicate_groups([{'text':e.text} for e in excluded]+rows)
        protected=set(joined[:len(excluded)])
        blocked={r['composition_group'] for r,g in zip(rows,joined[len(excluded):]) if g in protected}
        rows=[r for r in rows if r['composition_group'] not in blocked]
    duplicate=duplicate_groups(rows)
    parent={r['composition_group']:r['composition_group'] for r in rows}
    def find(k):
        while parent[k]!=k:parent[k]=parent[parent[k]];k=parent[k]
        return k
    seen={}
    for row,d in zip(rows,duplicate):
        if d in seen:parent[find(row['composition_group'])]=find(seen[d])
        seen[d]=row['composition_group']
    groups=sorted({find(r['composition_group']) for r in rows}, key=lambda g:source_hash(VERSION+g))
    if len(groups)<700:raise ValueError('Insufficient distinct composition groups after deduplication')
    roles={g:('TRAIN' if i<len(groups)*.10 else 'VALIDATION' if i<len(groups)*.40 else
              'CALIBRATION' if i<len(groups)*.80 else 'FROZEN_TEST') for i,g in enumerate(groups)}
    cal=sorted(g for g in groups if roles[g]=='CALIBRATION')
    folds={g:('FIT' if i<len(cal)*2/3 else 'EVALUATION') for i,g in enumerate(cal)}
    manifest={'version':VERSION,'source_type':'AI_AUTHORED_CONTROLLED_COMPOSITIONS','reference':REFERENCE,
              'limitations':['Restrictions NO includes not stated, explicit waiver and optional arrangements under the fixed notice-level criteria.',
                            'Shared AI-authored linguistic atoms across roles; only complete fact compositions and lexical near-duplicates are isolated.',
                            'Generation groups are controlled synthetic compositions, not independent real-world issuer/custodian families.',
                            'English only; no non-votable examples in this restriction-focused cohort.'],
              'excluded_training_bundle_sha256':sha(Path(exclusion_bundle)/'manifest.json') if exclusion_bundle else None,
              'counts':{},'groups':len(groups),'files':{},'automation_enabled':False}
    for role in ('TRAIN','VALIDATION','CALIBRATION','FROZEN_TEST'):
        subset=[]
        for row in rows:
            group=find(row['composition_group'])
            if roles[group]!=role:continue
            subset.append({**row,'role':role,'group':group,'fold':folds.get(group)})
        inputs=[{k:r[k] for k in ('id','text','source_hash','language','evaluation_time','group','role','fold')} for r in subset]
        jsonl(root/(role+'.inputs.jsonl'),inputs)
        # TRAIN/VALIDATION are development-only. Private evaluation keys never
        # enter a model or a deployment package.
        directory=root/('development' if role in ('TRAIN','VALIDATION') else 'private');directory.mkdir(exist_ok=True)
        key=directory/(role+'.labels.jsonl');jsonl(key,subset)
        manifest['files'][role]={'inputs':role+'.inputs.jsonl','inputs_sha256':sha(root/(role+'.inputs.jsonl')),
                                'labels':str(key.relative_to(root)),'labels_sha256':sha(key)}
        manifest['counts'][role]={'examples':len(subset),'groups':len({r['group'] for r in subset}),
                                  'classes':{k:dict(Counter(r['expected'][k] for r in subset)) for k in PREDICATES}}
    write(root/'manifest.json',manifest)
    return manifest

if __name__=='__main__':
    import argparse
    p=argparse.ArgumentParser();p.add_argument('output');p.add_argument('--exclude-training-bundle');a=p.parse_args()
    m=build(a.output,a.exclude_training_bundle);print(json.dumps({'counts':{k:v['examples'] for k,v in m['counts'].items()},'groups':m['groups']}))
