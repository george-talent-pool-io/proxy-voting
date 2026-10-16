"""Read-only experimental provenance views. No implicit model loading or writes."""
import json
from pathlib import Path
from hybrid.service import inspect as analyse
ROOT=Path(__file__).resolve().parents[2]
EXPERIMENT=ROOT/'data/experiments/iso-hybrid-v1'

def load(name,default=None):
    p=EXPERIMENT/name
    return json.loads(p.read_text()) if p.is_file() else default

def summary():
    public=load('public-parser-summary.json')
    corpus=ROOT/'data/iso15022_corpus/sources.jsonl'
    from collections import Counter
    counts=Counter(json.loads(x)['source_type'] for x in corpus.read_text().splitlines()) if corpus.exists() else Counter()
    return {'public_parser':public,'corpus_provenance_counts':dict(counts),'base':load('base-challenge-summary.json'),'fine_tuned':load('fine-challenge-summary.json'),'base_validation':load('base-validation-summary.json'),'fine_validation':load('fine-validation-summary.json'),'base_minimal_pairs':{k:v for k,v in (load('base-minimal-pairs.json',{}) or {}).items() if k!='rows'},'fine_minimal_pairs':{k:v for k,v in (load('fine-minimal-pairs.json',{}) or {}).items() if k!='rows'},'parser_verification':load('parser-verification.json'),'automation_enabled':False,'llm_enabled':False,'metrics_scope':'Public corpus: detector/parser-only. Semantic results: authored challenge and known leaky AI-synthetic validation, separately labelled. No independent customer accuracy.','routing':load('public-routing-summary.json'),'event_demo_available':bool(load('event-demo.json')),'available_examples':['clearstream-dscl-excerpt','derived-0002','derived-0004']}

def inspect(raw):return analyse(raw)

def example(identifier):
    if identifier not in summary()['available_examples']:raise ValueError('Unknown corpus example')
    folder='official_examples' if identifier.startswith('clearstream') else 'standards_derived'
    p=ROOT/'data/iso15022_corpus'/folder/(identifier+'.json');row=json.loads(p.read_text())
    persisted=load('demo-'+identifier+'.json')
    return {'source':{k:v for k,v in row.items() if k not in {'raw','expected'}},'analysis':persisted or analyse(row['raw'],message_type=row['message_type']),'semantic_executed':bool(persisted)}


def errors(model='fine',high_only=False):
    if model not in {'base','fine'}:raise ValueError('Unknown model')
    p=EXPERIMENT/f'{model}-challenge.jsonl';rows=[]
    if not p.exists():return {'model':model,'n':0,'items':[],'scope':'Not evaluated'}
    for line in p.read_text().splitlines():
        r=json.loads(line)
        if r['passed']:continue
        predicates=r['result']['semantic_analysis'].get('predicates',{})
        bad=[]
        for key,passed in r['checks'].items():
            if passed:continue
            score=predicates.get(key,{})
            if key=='other_restriction':
                # Legacy broad restriction is derived from five new predicates.
                # None of their individual probabilities is a probability of that union.
                components={k:a.get('scores',{}) for k,a in predicates.items() if k not in {'votable','share_blocking','poa_required'}}
                score={'scores':components,'confidence':None,'margin':None,'evidence':None}
            bad.append({'field':key,'expected':r['expected'][key],'predicted':r['observed'].get(key),'scores':score.get('scores',{}),'confidence':score.get('confidence'),'margin':score.get('margin'),'evidence':score.get('evidence')})
        high=any(x['confidence'] is not None and x['confidence']>=.98 for x in bad)
        if high_only and not high:continue
        rows.append({'id':r['id'],'text':r['text'],'expected':r['expected'],'observed':r['observed'],'failures':bad,'high_confidence_wrong':high,'tags':r['tags'],'market':'UNKNOWN','language':'UNKNOWN','source_type':'AUTHORED_CHALLENGE'})
    return {'model':model,'n':len(rows),'items':rows,'scope':'Authored regression errors; high confidence means a failing directly scored predicate >= .98, never a calibrated final-status probability'}
