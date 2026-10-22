"""Actual registered-path evidence/routing/calibration qualification.

Private research harness, excluded from delivery. No training and no promotion.
Prediction receipts precede every protected answer read. Outputs are single-use.
"""
import json
import time
from pathlib import Path
from production import confidence, operating
from production.qualification import predicate_feature, decision_feature
from production.storage import digest
from semantic_pipeline.schema import PREDICATES
from training.framework import jobs, releases
from training.framework.bundle import write, sha, jsonl
from training.framework.resources import model_resource
from scripts.qualify_frozen_learning import benchmark, lines
from scripts.run_reliability_programme import measure

ROOT=Path('data/experiments/production-readiness-20261022')
CORPUS=Path('data/qualification-corpora/fresh-evidence-v1')
POPULATION='AI_FRESH_EVIDENCE_COMPOSITIONS_V1_ENGLISH'


def inputs(role):
    m=json.loads((CORPUS/'manifest.json').read_text());e=m['files'][role];p=CORPUS/e['inputs']
    if sha(p)!=e['inputs_sha256']:raise ValueError('Input drift')
    return lines(p)


def answers(role, saved):
    receipt=json.loads(saved.read_text())
    if receipt['sha256']!=sha(saved.parent/'predictions.jsonl'):raise ValueError('Predictions changed')
    m=json.loads((CORPUS/'manifest.json').read_text());e=m['files'][role];p=CORPUS/e['labels']
    if sha(p)!=e['labels_sha256']:raise ValueError('Answer drift')
    return {r['id']:r for r in lines(p)}


def feature(row,key):
    meta={'language':'en','input_type':'UNSTRUCTURED_NOTICE'}
    return (decision_feature(row['text'],row['result'],meta) if key=='final_decision' else
            predicate_feature(row['text'],key,row['result'],meta))


def calibrate(rows,truth,identity,output,partition):
    records=[]
    for row in rows:
        for key in (*PREDICATES,'final_decision'):
            correct=(row['result']['decision']['classification']==truth[row['id']]['final_status'] if key=='final_decision' else
                     row['result']['predicates'][key]['value']==truth[row['id']]['expected'][key])
            records.append({'id':row['id'],'role':'CALIBRATION','fold':row['fold'],'group':row['group'],
                'predicate':key,'features':feature(row,key)['features'],'correct':bool(correct),'origin':'AI_AUTHORED'})
    jsonl(output/'features.jsonl',records)
    return confidence.fit(records,identity=identity,population=POPULATION,output=output/'calibrator.json',
                          context={'corpus_sha256':sha(CORPUS/'manifest.json'),'calibration_partition':partition})


def risk(rows,truth,cal,role):
    out=[]
    for row in rows:
        trust={};blocked=False
        for key in (*PREDICATES,'final_decision'):
            f=feature(row,key);blocked|=f['force_review']
            trust[key]=confidence.predict(cal,key,f,identity=cal['identity'],population=cal['population'])
        pred={k:row['result']['predicates'][k]['value'] for k in PREDICATES}
        exact=(pred==truth[row['id']]['expected'] and row['result']['decision']['classification']==truth[row['id']]['final_status'] and
               row['result']['deadline']['status']==truth[row['id']]['deadline_status'])
        out.append({'id':row['id'],'role':role,'group':row['group'],
            'confidence':min(trust.values()) if all(v is not None for v in trust.values()) else None,
            'predicate_confidence':trust,'force_review':blocked or row['result']['decision']['classification']=='UNCERTAIN_MANUAL_REVIEW',
            'truth':truth[row['id']]['expected'],'prediction':pred,'exact_correct':exact})
    return out


def run():
    policy=json.loads((ROOT/'VALIDATION_ROUTING_ABLATION.json').read_text())['results'][1]['policy']
    selected={'laya_job':'reliable-voting-balanced-v1-head-isolated',
              'laya_inference':'WHOLE_NOTICE_WITH_PASSAGE_EVIDENCE','policy':policy}
    references={}
    for name,extra in [('SPECIALIST',{'mode':'LAYA_ONLY'}),('HYBRID',{'mode':'LAYA_QWEN','llm_seed':'frozen-learning-v3-qwen38-mlx'})]:
        root=jobs.member('releases','production-evidence-v1-'+name.lower())
        m=releases.prepare({**selected,**extra},root);references[name]={'path':str(root),'identity':m['identity']}
    freeze={'version':'production-evidence-study-v1','releases':references,'corpus_sha256':sha(CORPUS/'manifest.json'),
        'routing_selection':'Conservative among three predeclared policies: >99% observed complete-output validation correctness and zero accepted critical-positive misses; NOT an automation gate',
        'routing_calibration':'Raw routing candidate; final outputs independently calibrated. No claim of calibrated routing acceptance.',
        'routing_ablation_sha256':sha(ROOT/'VALIDATION_ROUTING_ABLATION.json'),'runtime_sources':releases.source_files(),
        'checkpoint_training_in_this_study':False,'challenge_used_for_selection':False,'frozen_answers_opened':False,
        'automation_enabled':False,'customer_accuracy':None}
    write(ROOT/'INFERENCE_FREEZE.json',freeze)
    with model_resource('production-registered-calibration'):
        for name,ref in references.items():
            # Same frozen weights and source path used in the actual application.
            factory=lambda ref=ref:releases.ReleaseModel(ref['path'],sealed=False)
            reports={};cal=None;point=None
            for role in ('CALIBRATION','VALIDATION','FROZEN_TEST'):
                if freeze['runtime_sources']!=releases.source_files():raise ValueError('Frozen serving condition drift')
                if role=='FROZEN_TEST':
                    write(ROOT/(name+'-OPERATING_FREEZE.json'),{'release_identity':ref['identity'],
                        'calibrator_sha256':cal['sha256'],'operating_point_sha256':point['sha256'],
                        'corpus_sha256':sha(CORPUS/'manifest.json'),'frozen_answers_opened':False})
                out=ROOT/(name+'-'+role);predictions=benchmark(factory,inputs(role),out)
                truth=answers(role,out/'PREDICTIONS_SAVED.json');reports[role]=measure(predictions,truth)
                write(out/'metrics.json',reports[role])
                if role=='CALIBRATION':
                    cal=calibrate(predictions,truth,ref['identity'],out,'SPECIALIST_FINAL' if name=='SPECIALIST' else 'ACTUAL_HYBRID_FINAL')
                else:
                    rr=risk(predictions,truth,cal,role);jsonl(out/'confidence.jsonl',rr)
                    if role=='VALIDATION':
                        point=operating.select(rr,identity=ref['identity'],calibrator_hash=cal['sha256'],output=out/'operating-point.json')
                    else:
                        write(out/'operating-evaluation.json',operating.evaluate(rr,point,identity=ref['identity'],calibrator_hash=cal['sha256']))
                        write(out/'coverage-curve.json',[operating.summarize(rr,t) for t in (.7,.8,.9,.95,.98,.99)])
                print(json.dumps({'condition':name,'role':role,'assertions':reports[role]['correct_assertions'],
                                  'final_status':reports[role]['final_status']},sort_keys=True),flush=True)
            write(ROOT/(name+'-RESULT.json'),{'metrics':reports,'release':ref,'calibration_reports':cal['reports'],
                'operating_point':point,'automation_enabled':False,'customer_accuracy':None})


if __name__=='__main__':run()
