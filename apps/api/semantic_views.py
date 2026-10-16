"""Local experiment API. Reading provenance never invokes a model."""
import json
import os
import threading
import time
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Literal
from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field

ROOT=Path(__file__).resolve().parents[2]
EXPERIMENT=ROOT/'data/experiments/local-llm-v1'
router=APIRouter(prefix='/api/semantic')
LOCK=threading.Lock()

class AnalyseRequest(BaseModel):
    text:str|None=Field(default=None,min_length=1,max_length=2_000_000)
    record_id:str|None=Field(default=None,max_length=256)
    architecture:Literal['A','B','C','D','E']|None=None

def load(path,default=None):
    return json.loads(path.read_text()) if path.exists() else default

def records(dataset,arm):
    if dataset not in ('challenge','complete','synthetic-development') or arm not in 'ABCDE' or len(arm)!=1:
        raise ValueError('Unknown evaluation dataset or architecture')
    p=EXPERIMENT/f'{dataset}-{arm}.jsonl'
    if not p.exists():return []
    rows=[]
    for s in p.read_text().splitlines():
        try:rows.append(json.loads(s))
        except json.JSONDecodeError:continue  # Last append may still be in progress; never return a partial record.
    if dataset=='synthetic-development':
        gold=load(EXPERIMENT/'synthetic-development-truth.json',{})
        rows=[{**r,'expected':gold.get(r['id'],r['expected'])} for r in rows]
    return rows

@router.get('/experiment')
def summary():
    scored=load(EXPERIMENT/'CORRECTED-SUMMARY.json') or load(EXPERIMENT/'SUMMARY.json')
    return {'status':'SCORED' if scored else 'IN_PROGRESS' if (EXPERIMENT/'PROTOCOL.json').exists() else 'NOT_RUN',
        'summary':scored,'selection':load(EXPERIMENT/'VALIDATION-SELECTION.json'),
        'model':load(ROOT/'semantic_pipeline/llm-config.json'),
        'application_architecture':__import__('semantic_runtime.config',fromlist=['configured_architecture']).configured_architecture()[0],
        'on_demand_llm_enabled':os.environ.get('LLM_ENABLED','false').lower()=='true',
        'automation_enabled':False,'customer_accuracy':None,
        'scope':'Authored/synthetic research only; no verified customer accuracy',
        'progress':{dataset:{arm:len(records(dataset,arm)) for arm in 'ABCDE'} for dataset in ('challenge','complete','synthetic-development')}}

@router.get('/records')
def list_records(dataset:str='challenge',architecture:str='E',errors_only:bool=False,
                 high_only:bool=False,field:str='',expected:str='',predicted:str='',q:str='',
                 page:int=Query(1,ge=1),page_size:int=Query(25,ge=1,le=100)):
    from semantic_pipeline.metrics import summarize
    try:rows=records(dataset,architecture)
    except ValueError as e:raise HTTPException(400,str(e))
    if (EXPERIMENT/'CORRECTED-SUMMARY.json').exists():
        from evaluation.ae_scoring import project
        scoring_rows,_=project(rows,architecture)
    else:scoring_rows=rows
    errors=summarize(scoring_rows)['failures'];by_id={}
    for e in errors:by_id.setdefault(e['id'],[]).append(e)
    selected=[]
    for r in rows:
        failures=by_id.get(r['id'],[])
        if errors_only and not failures:continue
        if high_only and not any(e['confidence'] is not None and e['confidence']>=.98 for e in failures):continue
        if field or expected or predicted:
            if not any((not field or e['field']==field) and (not expected or e['expected']==expected) and (not predicted or e['predicted']==predicted) for e in failures):continue
        if q and q.lower() not in (r['id']+' '+r['text']).lower():continue
        selected.append({'id':r['id'],'text':r['text'],'failures':failures,'run_id':r['run_id'],
            'escalated':r['result']['escalation']['escalated'],
            'llm_invoked':bool((r['result'].get('llm') or {}).get('invoked')),
            'classification':r['result']['decision']['classification']})
    return {'total':len(selected),'items':selected[(page-1)*page_size:page*page_size],
        'dataset':dataset,'architecture':architecture}

@router.get('/record')
def record(id:str,dataset:str='challenge',architecture:str='E'):
    try:rows=records(dataset,architecture)
    except ValueError as e:raise HTTPException(400,str(e))
    row=next((r for r in rows if r['id']==id),None)
    if row is None:raise HTTPException(404,'Unknown experiment record')
    if (EXPERIMENT/'CORRECTED-SUMMARY.json').exists():
        from evaluation.ae_scoring import project
        from semantic_pipeline.metrics import observed
        projected,changes=project([row],architecture)
        row={**row,'scoring_version':'SCORER-v2','evaluation_projection':observed(projected[0]['result']),'projection_changes':changes}
    return row

@router.post('/analyse')
def analyse(request:AnalyseRequest):
    # Explicit local action, persisted separately from historical whole-text predictions.
    from semantic_runtime.config import configured_architecture
    architecture=request.architecture or configured_architecture()[1]
    text=request.text
    if request.record_id:
        from apps.api import store
        with store.connect() as c:
            notice=c.execute('SELECT text FROM notices WHERE id=?',(request.record_id,)).fetchone()
        if not notice:raise HTTPException(404,'Notice not found')
        if text is not None and text!=notice['text']:raise HTTPException(422,'Source text does not match persisted notice')
        text=notice['text']
    if text is None or not text.strip():raise HTTPException(422,'Nonempty notice text required')
    if not LOCK.acquire(blocking=False):raise HTTPException(409,'Another semantic analysis is active')
    try:
        started=time.perf_counter()
        from semantic_pipeline.experiment import laya_for
        from semantic_runtime.persistence import persist
        from semantic_pipeline.pipeline import run
        from semantic_pipeline.routing import RoutingConfig
        from semantic_runtime.fallback import configured_fallback
        selection=load(EXPERIMENT/'VALIDATION-SELECTION.json',{})
        if os.environ.get('SEMANTIC_PIPELINE_VERSION','v1')=='v2' and architecture in ('C','E'):
            from cascade.application import classify
            result=classify(text,architecture)
            model_load_ms=None  # v2 total includes model construction; no fabricated warm load duration.
        else:
            model=laya_for(architecture)
            model_load_ms=(time.perf_counter()-started)*1000
            result=run(text,architecture,laya_model=model,fallback=configured_fallback() if architecture in ('C','D','E') else None,
                routing=RoutingConfig(**selection.get('routing',{}).get(architecture,{})),
                reconciliation_policy=selection.get('reconciliation_policies',{}).get(architecture,{}))
        result['latencies']['model_load_ms']=model_load_ms
        result['latencies']['request_wall_total_ms']=(time.perf_counter()-started)*1000
        run_id=str(uuid.uuid4());target=ROOT/'data/semantic-runs';target.mkdir(exist_ok=True)
        row={'id':run_id,'run_id':run_id,'text':text,'record_id':request.record_id,'application_architecture':configured_architecture()[0],'result':result,'timestamp':datetime.now(timezone.utc).isoformat(),'source_type':'EXISTING_NOTICE_UNLABELLED' if request.record_id else 'USER_SUPPLIED_UNLABELLED','expected':{}}
        persist(target,row)
        return row
    except ValueError as e:raise HTTPException(422,str(e))
    except Exception as e:raise HTTPException(503,f'Local semantic inference unavailable: {type(e).__name__}: {e}')
    finally:LOCK.release()

@router.get('/analyses')
def analyses():
    folder=ROOT/'data/semantic-runs';out=[]
    if folder.exists():
        for p in sorted(folder.glob('*.jsonl'),key=lambda x:x.stat().st_mtime,reverse=True)[:100]:
            row=json.loads(p.read_text().splitlines()[0]);r=row['result']
            out.append({'id':row['id'],'run_id':row['run_id'],'timestamp':row['timestamp'],
                'architecture':r['architecture'],'classification':r['decision']['classification'],
                'llm_invoked':bool((r.get('llm') or {}).get('invoked')),'manual_review_required':True})
    return out

@router.get('/analysis/{run_id}')
def analysis(run_id:str):
    try:identifier=str(uuid.UUID(run_id))
    except ValueError:raise HTTPException(404,'Unknown analysis')
    p=ROOT/'data/semantic-runs'/(identifier+'.jsonl')
    if not p.exists():raise HTTPException(404,'Unknown analysis')
    return json.loads(p.read_text().splitlines()[0])


def latest_notice_analysis(record_id):
    folder=ROOT/'data/semantic-runs'
    if not folder.exists():return None
    for p in sorted(folder.glob('*.jsonl'),key=lambda p:p.stat().st_mtime,reverse=True):
        row=json.loads(p.read_text().splitlines()[0])
        if row.get('record_id')==record_id:return row
    return None

@router.get('/comparison-case')
def comparison_case(id:str,dataset:str='challenge'):
    from semantic_pipeline.metrics import truth,observed
    rows={a:record(id,dataset,a) for a in 'ABCDE'}
    return {'dataset':dataset,'id':id,'ground_truth':truth(rows['A']['expected']),
        'evaluated':{a:r.get('evaluation_projection') or observed(r['result']) for a,r in rows.items()},'architectures':rows}

@router.get('/diagnostics')
def diagnostics():
    data=load(EXPERIMENT/'LATENCY-RESOURCES.json',{})
    return {**data,'extended':load(EXPERIMENT/'EXTENDED-ASSERTION-DIAGNOSTICS.json'),
        'validation_strategies':load(EXPERIMENT/'VALIDATION-STRATEGY-COMPARISON-v2.json') or load(EXPERIMENT/'VALIDATION-STRATEGY-COMPARISON.json'),
        'repeatability':load(EXPERIMENT/'REPEATABILITY-RESOURCE-SUMMARY.json'),
        'automation_enabled':False,'customer_accuracy':None}
