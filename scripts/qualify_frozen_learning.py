"""Actual local-model study; never packages synthetic corpora/test derivatives.

One explicit run, preserved inputs/configuration, durable predictions before
protected truth. Validation selects the Laya inference condition. CALIBRATION
fits/evaluates confidence; frozen results cannot change any selection.
"""
import gc
import json
import statistics
import time
from pathlib import Path
from production import confidence, operating
from production.qualification import decision_feature
from training.framework import jobs, seeds
from training.framework.bundle import sha, write, jsonl
from training.framework.passage_runtime import RegisteredPassages
from training.framework.runtime import RegisteredModel
from training.framework.whole_runtime import WholeNotice
from semantic_pipeline.metrics import summarize
from semantic_pipeline.schema import PREDICATES


def lines(path):
    return [json.loads(line) for line in Path(path).read_text().splitlines() if line.strip()]


def benchmark(model_factory, rows, output):
    output.mkdir(parents=True,exist_ok=False);started=time.perf_counter();predictions=[]
    model=model_factory();load_seconds=time.perf_counter()-started
    resources=[];external_workloads=set()
    try:
        with (output/'predictions.jsonl').open('x') as f:
            for row in rows:
                before=time.perf_counter()
                result=model.analyse(row['text'],use_iso=False,reference=row.get('evaluation_time','2026-10-18T12:00:00+00:00'))
                value={**row,'result':result,'request_ms':(time.perf_counter()-before)*1000}
                f.write(json.dumps(value,ensure_ascii=False,allow_nan=False)+'\n');f.flush()
                __import__('os').fsync(f.fileno());predictions.append(value)
                import psutil, torch
                for p in psutil.process_iter(['pid','cmdline']):
                    try:
                        args=p.info['cmdline'] or []
                        if (any(a.endswith('/local-llm-lab/lab/worker.py') for a in args) or
                            args and Path(args[0]).name=='ollama' and 'runner' in args):
                            external_workloads.add((p.info['pid'],'OTHER_PROJECT_LOCAL_MODEL_WORKER'))
                    except psutil.Error:pass
                resources.append({'process_rss_bytes':psutil.Process().memory_info().rss,
                                  'mps_driver_allocated_bytes':torch.mps.driver_allocated_memory() if torch.backends.mps.is_available() else None})
    finally:
        model.close();del model;gc.collect()
        import torch
        if torch.backends.mps.is_available():torch.mps.empty_cache()
    values=[r['request_ms'] for r in predictions]
    write(output/'PREDICTIONS_SAVED.json',{'count':len(predictions),'sha256':sha(output/'predictions.jsonl'),
          'answers_opened':False,'elapsed_seconds':time.perf_counter()-started,
          'model_load_seconds':load_seconds,'latency_scope':'Request inference; model initialisation measured separately; no external queue/network',
          'notices_per_second_including_load_and_persistence':len(predictions)/(time.perf_counter()-started),
          'sampled_resources':{'max_process_rss_bytes':max(r['process_rss_bytes'] for r in resources),
                               'max_mps_driver_allocated_bytes':max((r['mps_driver_allocated_bytes'] or 0) for r in resources),
                               'scope':'After-notice samples, not OS-wide peak unified memory'},
          'external_model_workloads_observed':[{'pid':pid,'kind':kind} for pid,kind in sorted(external_workloads)],
          'hardware_isolation':'CONTENDED_WITH_EXTERNAL_MODEL_WORKLOAD' if external_workloads else 'No known external model worker observed; general-purpose desktop, not an isolated benchmark host',
          'latency_seconds':{'median':statistics.median(values)/1000,'mean':statistics.mean(values)/1000,
                             'min':min(values)/1000,'max':max(values)/1000,
                             'p95':sorted(values)[min(len(values)-1,__import__('math').ceil(.95*len(values))-1)]/1000}})
    return predictions


def main(output, *, corpus, trained_job):
    from training.framework.resources import model_resource
    output=Path(output);output.mkdir(parents=True,exist_ok=False)
    corpus=Path(corpus); manifest=json.loads((corpus/'manifest.json').read_text())
    if manifest['excluded_training_bundle_sha256'] != json.loads((trained_job/'plan.json').read_text())['bundle_manifest_sha256']:
        raise ValueError('Controlled corpus exclusion does not match actual training')
    specs={name:json.loads(Path('training/framework/specs/'+name+'.json').read_text()) for name in ('laya','qwen38-mlx')}
    paths={}
    for name,spec in specs.items():
        path=jobs.member('seeds',output.name+'-'+name)
        paths[name]=str(path);seeds.freeze(spec,path)
    write(output/'EXPERIMENT_PLAN.json',{'scope':'AI_AUTHORED_CONTROLLED_ONLY','corpus_sha256':sha(corpus/'manifest.json'),
          'trained_job':str(trained_job),'seeds':paths,'training_updates':json.loads((trained_job/'result.json').read_text()),
          'conditions':['FROZEN_LAYA_WHOLE','TRAINED_LAYA_PASSAGES','TRAINED_LAYA_WHOLE'],
          'whole_notice_evidence':'WHOLE_NOTICE_SCOPED_EVIDENCE; document model labels never changed by evidence locator',
          'runtime_sources':{str(p):sha(p) for folder in ('training/framework','production') for p in Path(folder).glob('*.py')},
          'calibration_support':'DEFAULT_100_FIT_50_EVALUATION_GROUPS','automation_enabled':False})
    def inputs(role):
        entry=manifest['files'][role];path=corpus/entry['inputs']
        if sha(path)!=entry['inputs_sha256']:raise ValueError('Corpus input drift')
        return lines(path)
    def truth(role, predictions_saved):
        if not predictions_saved.is_file():raise ValueError('Predictions must precede answers')
        receipt=json.loads(predictions_saved.read_text())
        if sha(predictions_saved.parent/'predictions.jsonl')!=receipt['sha256']:raise ValueError('Prediction drift')
        entry=manifest['files'][role];path=corpus/entry['labels']
        if sha(path)!=entry['labels_sha256']:raise ValueError('Answer drift')
        return {r['id']:r for r in lines(path)}
    def metrics(predictions, answers):
        report=summarize([{'id':r['id'],'text':r['text'],'result':r['result'],'expected':answers[r['id']]['expected']} for r in predictions])
        report['benchmark_final_status']={'n':len(predictions),'correct':sum(r['result']['decision']['classification']==answers[r['id']]['final_status'] for r in predictions)}
        report['benchmark_deadline']={'n':len(predictions),'correct':sum(r['result']['deadline']['status']==answers[r['id']]['deadline_status'] for r in predictions)}
        return report
    validation=inputs('VALIDATION'); reports={}
    with model_resource('frozen-learning-qualification'):
        for name in ('FROZEN_LAYA_WHOLE','TRAINED_LAYA_PASSAGES','TRAINED_LAYA_WHOLE'):
            factory=(lambda:WholeNotice(paths['laya'],model_factory=seeds.FrozenModel)) if name=='FROZEN_LAYA_WHOLE' else (
                     lambda:WholeNotice(trained_job)) if name.endswith('WHOLE') else (lambda:RegisteredPassages(trained_job))
            out=output/name
            predictions=benchmark(factory,validation,out)
            answers=truth('VALIDATION',out/'PREDICTIONS_SAVED.json')
            reports[name]=metrics(predictions,answers);write(out/'metrics.json',reports[name])
        # Select solely on validation. The whole-notice and passage paths use
        # identical trained weights; their scores measure runtime formulation.
        def critical_errors(report):
            return {(e['id'],e['field']) for e in report['failures'] if e['field'] in ('votability','share_blocking','poa_required','registration_required') and e['expected'] in ('YES','VOTABLE')}
        eligible=[name for name,r in reports.items() if not critical_errors(r)-critical_errors(reports['FROZEN_LAYA_WHOLE'])]
        selected=max(eligible,key=lambda k:reports[k]['correct_assertions'])
        write(output/'MODEL_SELECTION.json',{'selected':selected,'validation_assertions':{k:r['correct_assertions'] for k,r in reports.items()},
                                             'frozen_answers_opened':False})
        def selected_model():
            return (WholeNotice(paths['laya'],model_factory=seeds.FrozenModel) if selected=='FROZEN_LAYA_WHOLE' else
                    WholeNotice(trained_job) if selected.endswith('WHOLE') else RegisteredPassages(trained_job))
        identity=__import__('production.storage',fromlist=['digest']).digest({'plan':sha(output/'EXPERIMENT_PLAN.json'),'selected':selected})
        out=output/'calibration'; predictions=benchmark(selected_model,inputs('CALIBRATION'),out)
        answers=truth('CALIBRATION',out/'PREDICTIONS_SAVED.json');records=[]
        def feature(row,key):
            result=row['result'];meta={'language':'en','input_type':'UNSTRUCTURED_NOTICE'}
            return (decision_feature(row['text'],result,meta) if key=='final_decision' else confidence.feature_row(
                row['text'],key,result['predicates'][key],**meta,conflicts=result['reconciliation']['conflicts']))
        for row in predictions:
            for key in (*PREDICATES,'final_decision'):
                correct=(row['result']['decision']['classification']==answers[row['id']]['final_status'] if key=='final_decision' else
                         row['result']['predicates'][key]['value']==answers[row['id']]['expected'][key])
                records.append({'id':row['id'],'role':'CALIBRATION','fold':row['fold'],'group':row['group'],'predicate':key,
                                'features':feature(row,key)['features'],'correct':correct,'origin':'AI_AUTHORED'})
        jsonl(out/'features.jsonl',records)
        cal=confidence.fit(records,identity=identity,population='AI_COMPOSITION_COHORT_V3',output=out/'calibrator.json')
        def risk_rows(predictions,answers,role):
            values=[]
            for row in predictions:
                trust={};blocked=False
                for key in (*PREDICATES,'final_decision'):
                    f=feature(row,key);blocked |= f['force_review']
                    trust[key]=confidence.predict(cal,key,f,identity=identity,population=cal['population'])
                p=min(trust.values()) if all(v is not None for v in trust.values()) else None
                pred={k:row['result']['predicates'][k]['value'] for k in PREDICATES}
                values.append({'id':row['id'],'role':role,'group':row['group'],'confidence':p,'force_review':blocked,
                               'predicate_confidence':trust,'exact_correct':pred==answers[row['id']]['expected'] and
                               row['result']['decision']['classification']==answers[row['id']]['final_status'] and
                               row['result']['deadline']['status']==answers[row['id']]['deadline_status'],
                               'truth':answers[row['id']]['expected'],'prediction':pred})
            return values
        prior=lines(output/selected/'predictions.jsonl')
        validation_truth=truth('VALIDATION',output/selected/'PREDICTIONS_SAVED.json')
        operating_rows=risk_rows(prior,validation_truth,'VALIDATION')
        point=operating.select(operating_rows,identity=identity,calibrator_hash=cal['sha256'],output=output/'OPERATING_POINT.json')
        write(output/'OPERATING_FREEZE.json',{'selection_sha256':sha(output/'MODEL_SELECTION.json'),'calibrator_sha256':cal['sha256'],
                                             'operating_point_sha256':point['sha256'],'source_corpus_sha256':sha(corpus/'manifest.json'),
                                             'source_hashes':{str(p):sha(p) for p in Path('production').glob('*.py')},'automation_enabled':False})
        out=output/'frozen'; predictions=benchmark(selected_model,inputs('FROZEN_TEST'),out)
        answers=truth('FROZEN_TEST',out/'PREDICTIONS_SAVED.json');measured=metrics(predictions,answers)
        write(out/'metrics.json',measured)
        risk=risk_rows(predictions,answers,'FROZEN_TEST');jsonl(out/'confidence.jsonl',risk)
        operational=operating.evaluate(risk,point,identity=identity,calibrator_hash=cal['sha256'])
        challenge_path=Path('tests/fixtures/semantic.json')
        if sha(challenge_path)!='0e2f5d991a33deed25f8e9a33682185071c5ff35afd2df9179c1f8565dd17649':raise ValueError('Frozen challenge changed')
        challenge=json.loads(challenge_path.read_text())
        challenge_inputs=[{'id':r['id'],'text':r['text'],'evaluation_time':'2026-10-16T12:00:00+00:00'} for r in challenge]
        challenge_reports={}
        for name,factory in [('FOUNDATION',lambda:WholeNotice(paths['laya'],model_factory=seeds.FrozenModel)),('SELECTED',selected_model)]:
            cp=benchmark(factory,challenge_inputs,output/('challenge-'+name))
            truth_by_id={r['id']:r['expected'] for r in challenge}
            challenge_reports[name]=summarize([{**r,'expected':truth_by_id[r['id']]} for r in cp])
            write(output/('challenge-'+name)/'metrics.json',challenge_reports[name])
        result={'selected':selected,'validation':{k:{n:r[n] for n in ('cases','assertions','correct_assertions','cases_satisfying_all_supplied_assertions','fields')} for k,r in reports.items()},
                'frozen':measured,'calibration':cal['reports'],'operating':operational,'calibrated_predicates':list(cal['models']),
                'confidence_available_events':sum(r['confidence'] is not None for r in risk),
                'challenge':challenge_reports,
                'latency':json.loads((out/'PREDICTIONS_SAVED.json').read_text())['latency_seconds'],
                'automation_enabled':False,'customer_accuracy':None}
        write(output/'result.json',result)
        return result

if __name__=='__main__':
    import argparse
    p=argparse.ArgumentParser();p.add_argument('output');p.add_argument('--corpus',required=True);p.add_argument('--trained-job',required=True)
    a=p.parse_args();main(a.output,corpus=a.corpus,trained_job=Path(a.trained_job))
