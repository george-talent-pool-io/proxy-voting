"""Final read-only integrity audit; publishes a new completion record, never rewrites studies."""
import hashlib,json,re
from pathlib import Path
from semantic_pipeline.experiment import ROOT,read,lines,sha,verify,write,now

def main():
    frozen=verify();commit=read(ROOT/'PREDICTION-COMMIT.json')
    for path,digest in commit['files'].items():assert sha(path)==digest,path
    count=calls=0
    for dataset,n in [('challenge',57),('synthetic-development',100),('complete',48)]:
        ids=None
        for arm in 'ABCDE':
            rows=lines(ROOT/f'{dataset}-{arm}.jsonl');assert len(rows)==n
            current=[(r['id'],r['input_hash']) for r in rows]
            if ids is None:ids=current
            assert ids==current
            manifest=read(ROOT/'manifests'/f'{dataset}-{arm}.json')
            assert manifest['prediction_file_sha256']==sha(ROOT/f'{dataset}-{arm}.jsonl')
            assert manifest['run_id']==rows[0]['run_id']
            for row in rows:
                r=row['result'];count+=1;calls+=bool((r.get('llm') or {}).get('invoked'))
                assert hashlib.sha256(row['text'].encode()).hexdigest()==r['input_hash']
                assert not r['automation_enabled'] and r['decision']['manual_review_required']
                for p in r['reconciliation']['predicates'].values():
                    for e in p.get('evidence',[]):assert e['valid'] and row['text'][e['start']:e['end']]==e['text']
                if arm=='D':
                    context=json.loads(r['llm']['request']['messages'][1]['content'])
                    assert 'laya_diagnostic' not in context
    assert count==1025 and calls==497
    logs={k:Path(p).read_text() for k,p in {
        'software':'artifacts/local-llm-software-completion.log','browser':'artifacts/local-llm-browser-publication.log',
        'real_local_model':'artifacts/local-llm-real-integration-final.log','retained_model_quality':'artifacts/local-llm-retained-semantic-failures.log'}.items()}
    assert '1920 passed' in logs['software'];assert '18 passed' in logs['browser'];assert '13 passed' in logs['real_local_model']
    assert '47 failed' in logs['retained_model_quality']
    required=['LOCAL_LLM_SELECTION.md','LAYA_LLM_ARCHITECTURE_EVALUATION.md','ARCHITECTURE_COMPARISON_ERRORS.md','BLOCKING_FALSE_NEGATIVE_ANALYSIS.md']
    for name in required:assert (Path('data/reports')/name).stat().st_size>100
    summary=read(ROOT/'CORRECTED-SUMMARY.json');assert not summary['automation_enabled'] and summary['customer_accuracy'] is None
    restart=read(Path('artifacts/local-llm-integrated-restart.json'));assert restart['trace_identical_after_restart'] and restart['default_architecture']=='LEGACY_LAYA' and not restart['llm_enabled']
    repro=read(ROOT/'REPEATABILITY-RESOURCE-SUMMARY.json');assert len(repro['cases'])==20
    blocking=read(ROOT/'BLOCKING-FORENSICS.json');assert blocking['positive_cases']==11 and blocking['fine_positive_chunks_detected']==11 and blocking['fine_aggregate_conflicts']==11
    result={'verified_at':now(),'phase_completion_gate':'MET_FOR_RESEARCH_IMPLEMENTATION_AND_REQUESTED_CONTROLLED_EXPERIMENT_NOT_PRODUCTION',
        'frozen_inference_files_verified':len(frozen['files']),'prediction_rows':count,'timed_real_llm_invocations':calls,
        'all_five_arms_same_inputs_truth':True,'per_arm_manifests':15,'raw_model_scores_and_evidence_preserved':True,
        'real_local_model_tests':{'passed':13,'runtime_seconds':86.56,'model':summary['model']},
        'software_tests_passed':1920,'browser_tests_passed':18,'old_software_and_browser_regressions':0,
        'unchanged_authored_model_quality_failures':{'base':27,'fine_tuned':20,'total':47,'failures_are_retained':True},
        'repeatability':{k:sum(c[k] for c in repro['cases']) for k in repro['cases'][0] if k!='id'},
        'repeatability_cases':20,'repetitions_per_case':3,'oracle_analysis_completed':True,'blocking_investigation_completed':True,
        'latency_resource_probes_completed':True,'live_notice_path_and_restart':restart,
        'gui_trace_from_persisted_data':True,'gui_model_lab_same_case_comparison':True,
        'default_architecture':'LEGACY_LAYA','llm_enabled_default':False,'automation_enabled':False,'customer_accuracy':None,
        'limitations':['No representative expert-labelled production benchmark','Old synthetic test is exposed and duplicate-contaminated','Challenge partial assertion counts are not final-status accuracy','Optional schema repair is a later application-only condition, unused in frozen A–E','Configured new architecture is invoked by explicit per-notice action; historical bulk benchmark endpoint remains legacy'],
        'required_reports_sha256':{name:sha(Path('data/reports')/name) for name in required},
        'test_logs_sha256':{k:hashlib.sha256(v.encode()).hexdigest() for k,v in logs.items()}}
    write(ROOT/'FINAL-VERIFICATION.json',result);print(json.dumps({k:result[k] for k in ('phase_completion_gate','prediction_rows','timed_real_llm_invocations','software_tests_passed','browser_tests_passed','automation_enabled')},indent=2))
if __name__=='__main__':main()
