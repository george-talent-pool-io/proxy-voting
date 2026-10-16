"""Counterfactual quality control for the SAME capable specialist with always fallback.
Reuse actually invoked identical-context results; generate only missing accepted cases.
This is not a fresh independently timed architecture. No truth selects invocations.
"""
import json,uuid
from pathlib import Path
from semantic_pipeline.experiment import read,write,lines,append,sha,now
from cascade.study import ROOT,verify_core
from cascade.fallback import CommonFallback
from cascade.pipeline import execute
from cascade.routing import Policy
DATASETS=[('challenge',57),('complete',48)]

def build():
    verify_core();selected=read(ROOT/'PRIMARY-MODEL-SELECTION.json')['selected'];model=CommonFallback(read(ROOT/'LLM-CONFIGS-v3.json')[selected])
    manifest_path=ROOT/'ALWAYS-REFERENCE-MANIFEST.json'
    if not manifest_path.exists():
        names=['ALWAYS-REFERENCE-PROTOCOL.json','FINAL-SELECTION-FREEZE.json','LLM-CONFIGS-v3.json']+[f'{d}-C_SELECTIVE.jsonl' for d,_ in DATASETS]
        write(manifest_path,{'reference_run_id':str(uuid.uuid4()),'created_at':now(),'condition':'CAPABLE_ALWAYS_QUALITY_CONTROL',
            'primary_model':selected,'files':{n:sha(ROOT/n) for n in names if (ROOT/n).exists()},
            'implementation_sha256':sha(__file__),'timing_scope':'Untimed quality control; actual invoked generations reused, missing accepted cases generated without using labels.'})
    manifest=read(manifest_path)
    files=[]
    for dataset,n in DATASETS:
        path=ROOT/f'{dataset}-CAPABLE-ALWAYS-REFERENCE.jsonl';saved={r['id']:r for r in lines(path)}
        for row in lines(ROOT/f'{dataset}-C_SELECTIVE.jsonl'):
            if row['id'] in saved:continue
            old=row['result']
            if old['escalation']['escalated']:
                reference={**row,'reference_reused_invoked_result':True,'reference_scope':'Same semantic request and reconciliation already executed; policy selected an LLM call. Not another independent timing sample.'}
            else:
                value=execute(row['text'],precomputed=old['laya'],fallback=model,policy=Policy(name='ALWAYS'))
                value['latencies']['counterfactual_wall_ms']=value['latencies']['total_ms']
                value['latencies']['total_ms']+=old['laya']['latency_ms']
                value['latencies']['timing_scope']='Recomposed recorded specialist time plus fresh counterfactual fallback; not fresh full-architecture timing'
                reference={**row,'result':value,'reference_reused_invoked_result':False,'reference_scope':'New generation for a gate-accepted case; selection ignores expected labels. Not main timed A–E inference.','timestamp':now()}
                print('Always-fallback quality reference',dataset,row['id'],value['llm']['valid'],flush=True)
            reference['reference_policy']='ALWAYS'
            reference['reference_condition']='CAPABLE_ALWAYS_QUALITY_CONTROL'
            reference['reference_run_id']=manifest['reference_run_id']
            reference['parent_prediction_run_id']=row.get('run_id')
            append(path,reference)
        rows=lines(path)
        assert len(rows)==n and len({r['id'] for r in rows})==n
        files.append(path)
    target=ROOT/'ALWAYS-REFERENCE-COMMIT.json'
    if not target.exists():write(target,{'created_at':now(),'files':{str(p):sha(p) for p in files},'manifest_sha256':sha(manifest_path),'quality_reference_only':True,'no_labels_used_to_select_calls':True,'timing':'Mixture of existing invoked outcomes and recomposed missing-case outcomes; not an independent timed benchmark.'})
    return {d:lines(ROOT/f'{d}-CAPABLE-ALWAYS-REFERENCE.jsonl') for d in ['challenge','complete']}
