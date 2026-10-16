"""Completion gate executed only after full A–E/common-model/oracle reports exist."""
import json,os,subprocess,sys,hashlib,math,zipfile
from pathlib import Path
from importlib.metadata import distributions
from semantic_pipeline.experiment import lines,read,write,sha,now
from cascade.study import ROOT,verify_core
from cascade.reporting import CONDITIONS

def run_tests(label,args,env):
    log=Path('artifacts')/(label+'.log')
    with log.open('w') as f:r=subprocess.run([sys.executable,'-m','pytest',*args],stdout=f,stderr=subprocess.STDOUT,env=env)
    if r.returncode:raise RuntimeError(f'{label} failed; inspect {log}')
    return {'log':str(log),'sha256':sha(log),'summary':log.read_text().splitlines()[-1]}

def main():
    verify_core();baseline=read(ROOT/'PRE_AGGREGATION_FIX_BASELINE.json')
    analysis_freeze=read(ROOT/'ANALYSIS-IMPLEMENTATION-FREEZE.json')
    for p,h in analysis_freeze['files'].items():assert sha(p)==h,p
    for p,h in baseline['existing_checkpoint_and_inference_freeze']['files'].items():assert sha(p)==h,p
    commit=read(ROOT/'PREDICTION-COMMIT.json')
    for p,h in commit['files'].items():assert sha(p)==h,p
    reference_commit=read(ROOT/'ALWAYS-REFERENCE-COMMIT.json')
    for p,h in reference_commit['files'].items():assert sha(p)==h,p
    assert sha(ROOT/'ALWAYS-REFERENCE-MANIFEST.json')==reference_commit['manifest_sha256']
    assert reference_commit['quality_reference_only'] and reference_commit['no_labels_used_to_select_calls']
    reference_count=0
    for dataset,n in [('challenge',57),('complete',48)]:
        refs=lines(ROOT/f'{dataset}-CAPABLE-ALWAYS-REFERENCE.jsonl')
        assert len(refs)==n and len({r['id'] for r in refs})==n
        for row in refs:
            assert row['reference_policy']=='ALWAYS'
            assert row['result']['llm']['invoked']
            assert sha_text(row['text'])==row['result']['input_hash']
        reference_count+=len(refs)
    freeze=read(ROOT/'FINAL-SELECTION-FREEZE.json')
    for p,h in freeze['selection_files'].items():assert sha(p)==h
    count=calls=0;diag_hashes={};schema_errors=0
    for dataset,n in [('challenge',57),('complete',48)]:
        for c in CONDITIONS:
            rows=lines(ROOT/f'{dataset}-{c}.jsonl');assert len(rows)==n and len({r['id'] for r in rows})==n
            for row in rows:
                count+=1;r=row['result'];assert sha_text(row['text'])==r['input_hash']
                assert r['decision']['manual_review_required'] and not r['automation_enabled']
                if c in ('C1','C2','C3'):diag_hashes.setdefault((dataset,row['id']),set()).add(row['specialist_diagnostic_hash'])
                for p in r['reconciliation']['predicates'].values():
                    scores=p.get('scores',{})
                    if scores:assert all(math.isfinite(v) and 0<=v<=1 for v in scores.values()) and abs(sum(scores.values())-1)<.002
                    for e in p.get('evidence',[]):assert e['valid'] and row['text'][e['start']:e['end']]==e['text']
                l=r.get('llm')
                if not l:continue
                calls+=bool(l.get('invoked'));schema_errors+=not l.get('valid')
                context=json.loads(l['request']['messages'][1]['content']);assert 'expected' not in context
                if c in ('D3','C3'):assert l['request']['think']=='xhigh'
                if c in ('D1','D2','C1','C2'):assert l['request']['think'] is False
                if l.get('valid'):assert l['raw_response']['eval_count']>0
                if c.startswith('D'):assert 'laya_diagnostic' not in context and context['mode']=='INDEPENDENT'
                for name in ('raw_response','repair_raw_response'):
                    raw=l.get(name)
                    if raw:assert 'thinking' not in raw['message'];assert not raw['thinking_diagnostics']['raw_reasoning_stored']
    assert count==1155;assert all(len(h)==1 for h in diag_hashes.values()),'Different specialist inputs in the controlled model comparison'
    summary=read(ROOT/'SUMMARY.json');assert summary['datasets']['challenge']['A']['correct_assertions']==59
    assert summary['datasets']['challenge']['B']['correct_assertions']==73
    assert not summary['automation_enabled'] and summary['customer_accuracy'] is None
    # One model at a time in memory; integration tests are separate from warm timings.
    from cascade.fallback import CommonFallback
    cfg=read(ROOT/'LLM-CONFIGS-v3.json')['QWEN_DIRECT'];client=CommonFallback(cfg)
    for m in client.http('/api/ps')['models']:client.http('/api/generate',{'model':m['name'],'keep_alive':0})
    env={**os.environ,'RUN_LOCAL_LLM':'0','RUN_QWEN_LOCAL':'0','RUN_E2E':'0'}
    tests={}
    tests['software']=run_tests('cascade-final-software',['-m','not model and not e2e and not local_llm and not qwen_local','-q'],env)
    tests['browser']=run_tests('cascade-final-browser',['tests/e2e','-q'],{**env,'RUN_E2E':'1'})
    tests['qwen_real']=run_tests('cascade-final-real-qwen',['-m','qwen_local','-q'],{**env,'RUN_QWEN_LOCAL':'1'})
    for m in client.http('/api/ps')['models']:client.http('/api/generate',{'model':m['name'],'keep_alive':0})
    tests['legacy_real_llm']=run_tests('cascade-final-real-glm',['-m','local_llm','-q'],{**env,'RUN_LOCAL_LLM':'1'})
    reports=['C_GAIN_DECOMPOSITION.md','GLM_VS_QWEN_DISAGREEMENTS.md','GLM_QWEN_MODEL_SELECTION.md','QWEN_THINKING_REPAIR_DAMAGE.md','AGGREGATION_SELECTIVE_CASCADE_EVALUATION.md','CASCADE_V2_ASSERTION_ERRORS.md']
    for name in reports:assert (Path('data/reports')/name).stat().st_size>100
    # Archive all executable/scoring source, including exact prompts; no model weights/private inputs.
    files=[]
    for folder in ['cascade','classifier','hybrid','semantic_pipeline','semantic_runtime','training','evaluation','apps','scripts','tests']:
        files.extend(p for p in Path(folder).rglob('*') if p.is_file() and p.suffix in ('.py','.json','.txt','.js','.css','.html','.sh') and '__pycache__' not in p.parts)
    files += [Path(x) for x in ['README.md','pyproject.toml','uv.lock','requirements-hybrid.txt']]
    archive=ROOT/'EXECUTABLE-SOURCE.zip'
    if not archive.exists():
        with zipfile.ZipFile(archive,'x',zipfile.ZIP_DEFLATED) as z:
            for p in files:z.write(p,str(p))
    result={'verified_at':now(),'status':'RESEARCH_COMPLETION_GATE_MET','evaluation_prediction_rows':count,'timed_evaluation_llm_calls':calls,
        'quality_only_always_reference_rows':reference_count,'always_reference_is_independent_latency_benchmark':False,
        'final_invalid_llm_results':schema_errors,'identical_specialist_inputs_C1_C2_C3':True,'same_legacy_checkpoints':True,'challenge_unchanged':True,
        'no_training':True,'tests':tests,'automation_enabled':False,'customer_accuracy':None,
        'required_reports_sha256':{n:sha(Path('data/reports')/n) for n in reports},'source_archive_sha256':sha(archive),
        'source_files_sha256':{str(p):sha(p) for p in files},'installed_packages':{d.metadata['Name']:d.version for d in distributions()},
        'known_quality_failures':'Historical unchanged base/fine-tuned semantic tests still fail27/20; no expected assertion was weakened. These are distinct from software regressions.'}
    write(ROOT/'FINAL-VERIFICATION.json',result);print(json.dumps({k:result[k] for k in ['status','evaluation_prediction_rows','timed_evaluation_llm_calls','automation_enabled']},indent=2))

def sha_text(s):return hashlib.sha256(s.encode()).hexdigest()
if __name__=='__main__':main()
