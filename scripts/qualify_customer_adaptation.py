"""Predeclared customer-style adaptation; validation selects, tests only score.

AI-only qualification artifacts. The data and learned models are not delivery
artifacts. No challenge example or protected answer is a training input.
"""
import json
from pathlib import Path
from scripts.qualify_frozen_learning import benchmark, lines
from training.framework import jobs, seeds
from training.framework.bundle import sha, write, jsonl
from training.framework.whole_runtime import WholeNotice
from training.framework.resources import model_resource
from semantic_pipeline.metrics import summarize
from semantic_pipeline.schema import PREDICATES
from production import confidence, operating
from production.qualification import decision_feature
from production.storage import digest


CRITICAL = ('votability', 'share_blocking', 'poa_required', 'registration_required')


def run(output, corpus, first_job, baseline, *, _isolated=False):
    if not _isolated:
        # The long trainer keeps its original loaded modules. Qualification
        # must load one coherent, source-pinned runtime in a fresh process.
        import os,sys
        # Replace this qualification driver so the completed trainer's Metal
        # context/caches cannot compete with the next model. Only this explicit
        # CLI orchestration uses exec; application training already exits its
        # isolated worker before serving/evaluating the new checkpoint.
        os.execv(sys.executable,[sys.executable,'-m','scripts.qualify_customer_adaptation',str(output),'--corpus',str(corpus),
            '--first-job',str(first_job),'--baseline',str(baseline),'--isolated'])
    output=Path(output); output.mkdir(parents=True,exist_ok=False)
    corpus=Path(corpus); first_job=Path(first_job); baseline=Path(baseline)
    manifest=json.loads((corpus/'manifest.json').read_text())
    protocol=Path('data/experiments/CUSTOMER_ADAPTATION_PROTOCOL_V3.json')
    if sha(corpus/'manifest.json')!=json.loads(protocol.read_text())['corpus_manifest_sha256']:
        raise ValueError('Preregistered cohort changed')
    from training.framework.bundle import load_bundle
    from training.framework.trainers import training_label_support
    _,development=load_bundle(json.loads((first_job/'plan.json').read_text())['bundle'])
    write(output/'PLAN.json',{'protocol_sha256':sha(protocol),'corpus_sha256':sha(corpus/'manifest.json'),
          'source_hashes':{str(p):sha(p) for folder in ('training/framework','production') for p in Path(folder).glob('*.py')},
          'scope':'AI_CONTROLLED_COMPOSITION_ONLY','test_comparison':['FROZEN_FOUNDATION','VALIDATION_SELECTED'],
          'training_label_support':training_label_support(development),
          'automation_enabled':False})
    def inputs(role):
        entry=manifest['files'][role];p=corpus/entry['inputs']
        if sha(p)!=entry['inputs_sha256']:raise ValueError('Input drift')
        return lines(p)
    def answers(role, directory):
        receipt=json.loads((directory/'PREDICTIONS_SAVED.json').read_text())
        if sha(directory/'predictions.jsonl')!=receipt['sha256']:raise ValueError('Unsaved/drifted predictions')
        entry=manifest['files'][role];p=corpus/entry['labels']
        if sha(p)!=entry['labels_sha256']:raise ValueError('Answer drift')
        return {r['id']:r for r in lines(p)}
    def score(predictions, truth):
        report=summarize([{**p,'expected':truth[p['id']]['expected']} for p in predictions])
        report['benchmark_final_status']={'n':len(predictions),'correct':sum(p['result']['decision']['classification']==truth[p['id']]['final_status'] for p in predictions)}
        report['benchmark_deadline']={'n':len(predictions),'correct':sum(p['result']['deadline']['status']==truth[p['id']]['deadline_status'] for p in predictions)}
        return report
    def critical_errors(report):
        return {(e['id'],e['field']) for e in report['failures'] if e['field'] in CRITICAL and e['expected'] in ('YES','VOTABLE')}
    foundation=jobs.member('seeds','frozen-learning-v3-laya')
    factories={'FOUNDATION':lambda:WholeNotice(foundation,model_factory=seeds.FrozenModel),
               'ADAPTED_4_EPOCHS':lambda:WholeNotice(first_job)}
    # Re-execute validation using exactly the current evidence/calibration
    # implementation. Historical result files may contain protected outcomes.
    reports={}
    validation=inputs('VALIDATION')
    with model_resource('customer-adaptation-validation'):
        base_out=output/'FOUNDATION'
        base_preds=benchmark(factories['FOUNDATION'],validation,base_out)
        reports['FOUNDATION']=score(base_preds,answers('VALIDATION',base_out));write(base_out/'metrics.json',reports['FOUNDATION'])
        out=output/'ADAPTED_4_EPOCHS'
        preds=benchmark(factories['ADAPTED_4_EPOCHS'],validation,out)
        reports['ADAPTED_4_EPOCHS']=score(preds,answers('VALIDATION',out));write(out/'metrics.json',reports['ADAPTED_4_EPOCHS'])
    four=reports['ADAPTED_4_EPOCHS']
    macro=sum(m['macro_f1'] for m in four['fields'].values())/len(four['fields'])
    extend=macro<.98 or any(four['fields'][p]['positive_recall']<.98 for p in CRITICAL)
    write(output/'VALIDATION_BUDGET_DECISION.json',{'macro_f1':macro,'critical_positive_recall':{p:four['fields'][p]['positive_recall'] for p in CRITICAL},
          'four_more_epochs':extend,'decision_uses':'VALIDATION_ONLY','frozen_results_inspected':False})
    jobs_by_condition={'ADAPTED_4_EPOCHS':str(first_job)}
    if extend:
        parent=jobs.member('seeds',output.name+'-4epoch-parent')
        seeds.export_derivative(first_job,parent,origin='AI_TEST_DERIVATIVE')
        spec=seeds.training_spec(parent,{'epochs':4,'learning_rate':.0001,'encoder_learning_rate':.000025,
                                        'batch_size':8,'gradient_accumulation':2,'freeze_encoder':False,'max_length':2048,'seed':42,
                                        'laya_gradient_checkpointing':True,'laya_sdk_validation':False,'mps_memory_fraction':.45})
        job=jobs.member('jobs',output.name+'-8epoch')
        bundle=Path(json.loads((first_job/'plan.json').read_text())['bundle'])
        jobs.prepare(bundle,spec,job)
        import subprocess,sys
        subprocess.run([sys.executable,'-m','training.framework','execute',str(job)],check=True)
        factories['ADAPTED_8_EPOCHS']=lambda:WholeNotice(job)
        jobs_by_condition['ADAPTED_8_EPOCHS']=str(job)
        with model_resource('customer-adaptation-extension-validation'):
            out=output/'ADAPTED_8_EPOCHS';preds=benchmark(factories['ADAPTED_8_EPOCHS'],validation,out)
            reports['ADAPTED_8_EPOCHS']=score(preds,answers('VALIDATION',out));write(out/'metrics.json',reports['ADAPTED_8_EPOCHS'])
    eligible=[k for k,r in reports.items() if not critical_errors(r)-critical_errors(reports['FOUNDATION'])]
    selected=max(eligible,key=lambda k:reports[k]['correct_assertions'])
    write(output/'MODEL_SELECTION.json',{'selected':selected,'eligible':eligible,'criterion':'Most correct validation assertions, with no new critical positive miss versus foundation',
          'validation_assertions':{k:r['correct_assertions'] for k,r in reports.items()},'jobs':jobs_by_condition,'frozen_results_inspected':False})
    factory=factories[selected]
    identity=digest({'plan':sha(output/'PLAN.json'),'selection':sha(output/'MODEL_SELECTION.json')})
    def feature(row,key):
        result=row['result'];meta={'language':'en','input_type':'UNSTRUCTURED_NOTICE'}
        return decision_feature(row['text'],result,meta) if key=='final_decision' else confidence.feature_row(
            row['text'],key,result['predicates'][key],**meta,conflicts=result['reconciliation']['conflicts'])
    def risk_rows(predictions,truth,role,cal):
        values=[]
        for row in predictions:
            ps={};blocked=False
            for key in (*PREDICATES,'final_decision'):
                f=feature(row,key);blocked |= f['force_review']
                ps[key]=confidence.predict(cal,key,f,identity=identity,population=cal['population'])
            pred={k:row['result']['predicates'][k]['value'] for k in PREDICATES}
            values.append({'id':row['id'],'role':role,'group':row['group'],'confidence':min(ps.values()) if all(p is not None for p in ps.values()) else None,
                'predicate_confidence':ps,'force_review':blocked,'exact_correct':pred==truth[row['id']]['expected'] and
                row['result']['decision']['classification']==truth[row['id']]['final_status'] and
                row['result']['deadline']['status']==truth[row['id']]['deadline_status'],
                'truth':truth[row['id']]['expected'],'prediction':pred})
        return values
    with model_resource('customer-adaptation-fixed-qualification'):
        out=output/'calibration';preds=benchmark(factory,inputs('CALIBRATION'),out);truth=answers('CALIBRATION',out);records=[]
        for row in preds:
            for key in (*PREDICATES,'final_decision'):
                correct=(row['result']['decision']['classification']==truth[row['id']]['final_status'] if key=='final_decision' else
                         row['result']['predicates'][key]['value']==truth[row['id']]['expected'][key])
                records.append({'id':row['id'],'role':'CALIBRATION','fold':row['fold'],'group':row['group'],'predicate':key,
                                'features':feature(row,key)['features'],'correct':correct,'origin':'AI_AUTHORED'})
        jsonl(out/'features.jsonl',records)
        cal=confidence.fit(records,identity=identity,population='AI_COMPOSITION_COHORT_V3',output=out/'calibrator.json',
                           context={'corpus_sha256':sha(corpus/'manifest.json'),'calibration_partition':'STANDALONE_FINAL'})
        prior_dir=output/selected
        vr=lines(prior_dir/'predictions.jsonl');vt=answers('VALIDATION',prior_dir)
        point=operating.select(risk_rows(vr,vt,'VALIDATION',cal),identity=identity,calibrator_hash=cal['sha256'],output=output/'OPERATING_POINT.json')
        write(output/'OPERATING_FREEZE.json',{'selection_sha256':sha(output/'MODEL_SELECTION.json'),'calibrator_sha256':cal['sha256'],
               'operating_point_sha256':point['sha256'],'automation_enabled':False,'protected_metrics_inspected':False})
        out=output/'frozen';preds=benchmark(factory,inputs('FROZEN_TEST'),out)
        base_preds=preds if selected=='FOUNDATION' else benchmark(factories['FOUNDATION'],inputs('FROZEN_TEST'),output/'frozen-foundation')
        # Every blind prediction is durable before this answer file is opened.
        truth=answers('FROZEN_TEST',out);frozen=score(preds,truth);write(out/'metrics.json',frozen)
        base_frozen=score(base_preds,truth)
        if selected!='FOUNDATION':write(output/'frozen-foundation/metrics.json',base_frozen)
        risk=risk_rows(preds,truth,'FROZEN_TEST',cal);jsonl(out/'confidence.jsonl',risk)
        measured=operating.evaluate(risk,point,identity=identity,calibrator_hash=cal['sha256'])
        ambiguity={}
        for name,unknown in [('FULLY_SPECIFIED',False),('TRUTH_CONTAINS_UNKNOWN',True)]:
            subset=[row for row in risk if ('UNKNOWN' in row['truth'].values())==unknown]
            ambiguity[name]={'n':len(subset),'selected_point':operating.evaluate(subset,point,identity=identity,calibrator_hash=cal['sha256']) if subset else None}
        challenge_path=Path('tests/fixtures/semantic.json')
        if sha(challenge_path)!='0e2f5d991a33deed25f8e9a33682185071c5ff35afd2df9179c1f8565dd17649':raise ValueError('Challenge changed')
        challenge=json.loads(challenge_path.read_text());out=output/'challenge'
        cp=benchmark(factory,[{'id':r['id'],'text':r['text'],'evaluation_time':'2026-10-16T12:00:00+00:00'} for r in challenge],out)
        by_id={r['id']:r['expected'] for r in challenge};cm=summarize([{**r,'expected':by_id[r['id']]} for r in cp]);write(out/'metrics.json',cm)
        base_challenge=cm
        if selected!='FOUNDATION':
            bp=benchmark(factories['FOUNDATION'],[{'id':r['id'],'text':r['text'],'evaluation_time':'2026-10-16T12:00:00+00:00'} for r in challenge],output/'challenge-foundation')
            base_challenge=summarize([{**r,'expected':by_id[r['id']]} for r in bp]);write(output/'challenge-foundation/metrics.json',base_challenge)
    result={'selected':selected,'jobs':jobs_by_condition,'validation':reports,'frozen':frozen,'frozen_foundation':base_frozen,
            'challenge':cm,'challenge_foundation':base_challenge,
            'calibration':cal['reports'],'operating':measured,'ambiguity_strata':ambiguity,
            'confidence_available_events':sum(r['confidence'] is not None for r in risk),
            'timing':json.loads((output/'frozen/PREDICTIONS_SAVED.json').read_text()),'automation_enabled':False,'customer_accuracy':None}
    write(output/'result.json',result)
    return result


if __name__=='__main__':
    import argparse
    p=argparse.ArgumentParser();p.add_argument('output');p.add_argument('--corpus',required=True);p.add_argument('--first-job',required=True);p.add_argument('--baseline',required=True);p.add_argument('--isolated',action='store_true')
    a=p.parse_args();run(a.output,a.corpus,a.first_job,a.baseline,_isolated=a.isolated)
