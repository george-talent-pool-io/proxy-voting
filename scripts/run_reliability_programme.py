"""Bounded, actual-model study; private AI corpus never enters source delivery.

Run validation first. Qualification requires its immutable selection receipt.
No challenge answers are available to selection/training functions.
"""
import argparse
import json
import statistics
from pathlib import Path
from production import confidence, operating
from production.qualification import decision_feature, CRITICAL
from production.storage import digest
from semantic_pipeline.schema import PREDICATES
from semantic_pipeline.metrics import summarize
from training.framework import jobs, releases, seeds
from training.framework.bundle import write, sha, jsonl
from training.framework.whole_runtime import WholeNotice
from training.framework.resources import model_resource
from scripts.qualify_frozen_learning import benchmark, lines

ROOT=Path('data/experiments/reliability-programme-20261022')
CORPUS=Path('data/qualification-corpora/reliable-voting-v1')
PARENT='framework-domain-upgrade-20261022-selected'
CANDIDATE='reliable-voting-balanced-v1-2epoch'
POPULATION='AI_BALANCED_COMPOSITIONS_V1_ENGLISH_ONLY'


def inputs(role):
    m=json.loads((CORPUS/'manifest.json').read_text());entry=m['files'][role];p=CORPUS/entry['inputs']
    if sha(p)!=entry['inputs_sha256']:raise ValueError('Input drift')
    return lines(p)


def answers(role,predictions_saved):
    receipt=json.loads(Path(predictions_saved).read_text())
    if receipt['sha256']!=sha(Path(predictions_saved).parent/'predictions.jsonl'):raise ValueError('Persisted predictions drift')
    m=json.loads((CORPUS/'manifest.json').read_text());entry=m['files'][role];p=CORPUS/entry['labels']
    if sha(p)!=entry['labels_sha256']:raise ValueError('Answer drift')
    return {r['id']:r for r in lines(p)}


def measure(predictions,truth):
    out=summarize([{**r,'expected':truth[r['id']]['expected']} for r in predictions])
    out['complete_fields_exact_match']={'n':len(predictions),'correct':sum(
        all(r['result']['predicates'][k]['value']==truth[r['id']]['expected'][k] for k in PREDICATES) for r in predictions)}
    out['final_status']={'n':len(predictions),'correct':sum(r['result']['decision']['classification']==truth[r['id']]['final_status'] for r in predictions)}
    out['deadline']={'n':len(predictions),'correct':sum(r['result']['deadline']['status']==truth[r['id']]['deadline_status'] for r in predictions)}
    return out


def validation():
    target=ROOT/'validation';target.mkdir(exist_ok=False)
    factories={'PARENT':lambda:WholeNotice(jobs.member('seeds',PARENT),model_factory=seeds.FrozenModel),
               'BALANCED_2EPOCH':lambda:WholeNotice(jobs.member('jobs',CANDIDATE))}
    reports={}
    with model_resource('balanced-reliability-validation'):
        for name,factory in factories.items():
            out=target/name;p=benchmark(factory,inputs('VALIDATION'),out)
            reports[name]=measure(p,answers('VALIDATION',out/'PREDICTIONS_SAVED.json'));write(out/'metrics.json',reports[name])
    def misses(m):return {(r['id'],r['field']) for r in m['failures'] if r['field'] in CRITICAL and r['expected'] in ('YES','VOTABLE')}
    new=sorted(misses(reports['BALANCED_2EPOCH'])-misses(reports['PARENT']))
    scores={k:statistics.mean(f['balanced_accuracy'] for f in m['fields'].values()) for k,m in reports.items()}
    selected='BALANCED_2EPOCH' if scores['BALANCED_2EPOCH']>scores['PARENT'] and not new else 'PARENT'
    selected_source={'kind':'job','id':CANDIDATE} if selected=='BALANCED_2EPOCH' else {'kind':'seed','id':PARENT}
    receipt={'selected':selected,'source':selected_source,'validation_macro_balanced_accuracy':scores,
             'new_critical_positive_misses':new,'selection_rule':'Higher mean predicate balanced accuracy, with no new critical-positive validation misses',
             'validation_predictions':{k:sha(target/k/'predictions.jsonl') for k in factories},
             'runtime_sources':releases.source_files(),'corpus_sha256':sha(CORPUS/'manifest.json'),
             'protected_answers_opened':False,'customer_accuracy':None,'automation_enabled':False}
    write(ROOT/'SELECTION_FREEZE.json',receipt)
    return receipt


def feature(row,key):
    r=row['result'];meta={'language':'en','input_type':'UNSTRUCTURED_NOTICE'}
    return decision_feature(row['text'],r,meta) if key=='final_decision' else confidence.feature_row(
        row['text'],key,r['predicates'][key],**meta,conflicts=r['reconciliation']['conflicts'])


def calibrate(predictions,truth,identity,out,partition):
    records=[]
    for r in predictions:
        for k in (*PREDICATES,'final_decision'):
            correct=(r['result']['decision']['classification']==truth[r['id']]['final_status'] if k=='final_decision' else
                     r['result']['predicates'][k]['value']==truth[r['id']]['expected'][k])
            records.append({'id':r['id'],'role':'CALIBRATION','fold':r['fold'],'group':r['group'],
                'predicate':k,'features':feature(r,k)['features'],'correct':correct,'origin':'AI_AUTHORED'})
    jsonl(out/'features.jsonl',records)
    return confidence.fit(records,identity=identity,population=POPULATION,output=out/'calibrator.json',
        context={'corpus_sha256':sha(CORPUS/'manifest.json'),'calibration_partition':partition})


def risk(predictions,truth,cal,role):
    rows=[]
    for r in predictions:
        trust={};blocked=False
        for k in (*PREDICATES,'final_decision'):
            f=feature(r,k);blocked|=f['force_review']
            trust[k]=confidence.predict(cal,k,f,identity=cal['identity'],population=cal['population'])
        pred={k:r['result']['predicates'][k]['value'] for k in PREDICATES}
        exact=(pred==truth[r['id']]['expected'] and r['result']['decision']['classification']==truth[r['id']]['final_status'] and
               r['result']['deadline']['status']==truth[r['id']]['deadline_status'])
        rows.append({'id':r['id'],'role':role,'group':r['group'],'confidence':min(trust.values()) if all(v is not None for v in trust.values()) else None,
                     'predicate_confidence':trust,'force_review':blocked or (pred['votability']=='VOTABLE' and r['result']['deadline']['status']=='UNKNOWN'),
                     'truth':truth[r['id']]['expected'],'prediction':pred,'exact_correct':exact})
    return rows


def qualification():
    frozen=json.loads((ROOT/'SELECTION_FREEZE.json').read_text())
    if frozen['runtime_sources']!=releases.source_files() or frozen['corpus_sha256']!=sha(CORPUS/'manifest.json'):raise ValueError('Selection source/corpus drift')
    source=frozen['source'];factory=(lambda:WholeNotice(jobs.member('jobs',source['id']))) if source['kind']=='job' else (
        lambda:WholeNotice(jobs.member('seeds',source['id']),model_factory=seeds.FrozenModel))
    identity=digest(frozen);reports={}
    with model_resource('balanced-reliability-qualification'):
        # Two independent partitions, never pooled or re-used to train a model.
        for role in ('LAYA_STAGE','CASCADE_FINAL'):
            out=ROOT/role;p=benchmark(factory,inputs(role),out)
            truth=answers(role,out/'PREDICTIONS_SAVED.json');write(out/'metrics.json',measure(p,truth))
            # This second pass measures specialist-only final calibration. It
            # does NOT qualify a hybrid: changed LLM sources remain unsupported.
            partition='LAYA_STAGE' if role=='LAYA_STAGE' else 'SPECIALIST_FINAL_ONLY_NOT_HYBRID'
            reports[role]=calibrate(p,truth,identity,out,partition)
        validation_path=ROOT/'validation'/frozen['selected']
        vr=lines(validation_path/'predictions.jsonl');vt=answers('VALIDATION',validation_path/'PREDICTIONS_SAVED.json')
        cal=reports['CASCADE_FINAL']
        point=operating.select(risk(vr,vt,cal,'VALIDATION'),identity=identity,calibrator_hash=cal['sha256'],output=ROOT/'OPERATING_POINT.json')
        write(ROOT/'OPERATING_FREEZE.json',{'selection_sha256':sha(ROOT/'SELECTION_FREEZE.json'),'point_sha256':point['sha256'],
            'calibrator_sha256':cal['sha256'],'runtime_sources':releases.source_files(),'automation_enabled':False})
        out=ROOT/'FROZEN_TEST';p=benchmark(factory,inputs('FROZEN_TEST'),out)
        truth=answers('FROZEN_TEST',out/'PREDICTIONS_SAVED.json');metrics=measure(p,truth);write(out/'metrics.json',metrics)
        rr=risk(p,truth,cal,'FROZEN_TEST');jsonl(out/'confidence.jsonl',rr)
        curves=[operating.summarize(rr,t) for t in (.70,.80,.90,.95,.98,.99)]
        measured=operating.evaluate(rr,point,identity=identity,calibrator_hash=cal['sha256'])
        path=Path('tests/fixtures/semantic.json')
        if sha(path)!='0e2f5d991a33deed25f8e9a33682185071c5ff35afd2df9179c1f8565dd17649':raise ValueError('Challenge drift')
        challenge=json.loads(path.read_text());ci=[{'id':r['id'],'text':r['text'],'evaluation_time':'2026-10-16T12:00:00+00:00'} for r in challenge]
        cp=benchmark(factory,ci,ROOT/'CHALLENGE');ct={r['id']:r['expected'] for r in challenge}
        cm=summarize([{**r,'expected':ct[r['id']]} for r in cp]);write(ROOT/'CHALLENGE'/'metrics.json',cm)
        result={'selected':frozen['selected'],'frozen':metrics,'challenge':cm,'operating':measured,'coverage_curve':curves,
            'calibration':{role:c['reports'] for role,c in reports.items()},
            'confidence_available_events':sum(r['confidence'] is not None for r in rr),'events':len(rr),
            'latency':json.loads((out/'PREDICTIONS_SAVED.json').read_text()),
            'hybrid_calibration_status':'NOT_FITTED_HERE; specialist-only calibration cannot qualify LLM results',
            'qwen4_status':'NO_OFFICIAL_DOWNLOADABLE_WEIGHTS_FOUND','customer_accuracy':None,'automation_enabled':False}
        write(ROOT/'result.json',result)
    return result


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('phase',choices=['validation','qualification']);args=p.parse_args()
    result=validation() if args.phase=='validation' else qualification()
    print(json.dumps({'phase':args.phase,'selected':result['selected'],'report':str(ROOT)}))
