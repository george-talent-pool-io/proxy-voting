from contextlib import asynccontextmanager
import csv
import io
import json
import os
import subprocess
import sys
import threading
from pathlib import Path
from fastapi import FastAPI,HTTPException,Query
from fastapi.responses import FileResponse,StreamingResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel,Field
from apps.api import store
from classifier.schema import Decision,Status
from evaluation.evaluate import evaluate

@asynccontextmanager
async def lifespan(app):
    store.initialise()
    yield
app=FastAPI(title='Laya Voting Intelligence',version='0.1.0',lifespan=lifespan)
ROOT=Path(__file__).resolve().parents[2]
job_lock=threading.Lock()

@app.middleware('http')
async def local_boundary(request,call_next):
    host=request.headers.get('host','').split(':')[0]
    if host not in ['localhost','127.0.0.1','testserver','[']:return __import__('starlette.responses',fromlist=['JSONResponse']).JSONResponse({'detail':'Local access only'},status_code=403)
    if request.method not in ['GET','HEAD','OPTIONS']:
        origin=request.headers.get('origin')
        if origin and origin not in [f'http://{request.headers.get("host")}',f'https://{request.headers.get("host")}']:
            return __import__('starlette.responses',fromlist=['JSONResponse']).JSONResponse({'detail':'Cross-origin write rejected'},status_code=403)
    response=await call_next(request)
    response.headers['Content-Security-Policy']="default-src 'self'; script-src 'self'; style-src 'self'; img-src 'self' data:; connect-src 'self'; frame-ancestors 'none'; base-uri 'self'; form-action 'self'"
    response.headers['X-Content-Type-Options']='nosniff'
    return response

@app.get('/api/health')
def health():return {'status':'ok','mode':'local','external_inference':False}

@app.get('/api/hybrid/summary')
def hybrid_summary():
    from apps.api.hybrid_views import summary
    return summary()

@app.get('/api/hybrid/event-demo')
def hybrid_event_demo():
    from apps.api.hybrid_views import load
    return load('event-demo.json',{'state':None,'note':'Synthetic lifecycle demo not seeded'})

@app.get('/api/hybrid/errors')
def hybrid_errors(model:str='fine',high_only:bool=False):
    from apps.api.hybrid_views import errors
    try:return errors(model,high_only)
    except ValueError as e:raise HTTPException(400,str(e))

@app.get('/api/hybrid/example')
def hybrid_example(id:str):
    from apps.api.hybrid_views import example
    try:return example(id)
    except ValueError as e:raise HTTPException(404,str(e))

@app.get('/api/profile')
def profile():
    p=ROOT/'data/reports/profile.json'
    return json.loads(p.read_text()) if p.exists() else {'records':0,'message':'Import and profile a dataset first'}

@app.get('/api/demo')
def demo_examples():
    p=ROOT/'data/reports/demo_examples.json'
    if not p.exists():return []
    examples=json.loads(p.read_text())
    with store.connect() as c:
        return [r for r in examples if c.execute('SELECT id FROM notices WHERE id=?',(r['id'],)).fetchone()]

@app.get('/api/dataset-revisions')
def dataset_revisions():
    with store.connect() as c:
        if not c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='dataset_revisions'").fetchone():return []
        return [{**dict(r),'metadata':json.loads(r['metadata'])} for r in c.execute('SELECT * FROM dataset_revisions ORDER BY created_at DESC')]

@app.get('/api/runs')
def runs():
    with store.connect() as c:
        output=[]
        for r in c.execute('SELECT * FROM runs ORDER BY created_at DESC'):
            d=dict(r)
            for key in ['config','manifest','benchmark']:d[key]=json.loads(d[key]) if d[key] else None
            d['persisted']=c.execute('SELECT count(*) FROM predictions WHERE run_id=?',(r['id'],)).fetchone()[0]
            output.append(d)
    return output

@app.get('/api/overview')
def overview(run_id:str|None=None):
    with store.connect() as c:
        run=dict(c.execute('SELECT * FROM runs WHERE id=?',(run_id,)).fetchone() or {}) if run_id else store.latest_run(c)
        n=c.execute('SELECT count(*) FROM notices').fetchone()[0]
        results=[json.loads(r['result']) for r in c.execute('SELECT result FROM predictions WHERE run_id=? AND result IS NOT NULL',(run['id'] if run else '',))]
        from collections import Counter
        counts=dict(Counter(r['classification'] for r in results))
        bins=[sum(i/10<=r['confidence']<(i+1)/10 or (i==9 and r['confidence']==1) for r in results) for i in range(10)]
        auto=sum(r['action']=='AUTO_CLASSIFY' for r in results)
    metrics=evaluate(run['id'] if run else None)
    from evaluation.layer_metrics import public_layers
    return dict(total=n,analysed=len(results),auto=auto,manual=len(results)-auto,distribution=counts,confidence_bins=bins,
        run_id=run['id'] if run else None,verified_test=metrics['n'],test_accuracy=metrics['accuracy'],verified_total=metrics.get('verified_total',0),metric_layers=public_layers(run['id'] if run else None))

@app.get('/api/metric-layers')
def metric_layers(run_id:str|None=None):
    from evaluation.layer_metrics import public_layers
    return public_layers(run_id)

@app.get('/api/notices')
def notices(q:str='',classification:str='',country:str='',market:str='',language:str='',event_type:str='',review:str='',
            correct:str='',min_confidence:float=0,max_confidence:float=1,queue:bool=False,cohort:bool=False,run_id:str|None=None,
            page:int=Query(1,ge=1),page_size:int=Query(40,ge=1,le=200)):
    from training.study import load_study
    study=load_study() if cohort else None
    cohort_ids={r['record_id'] for r in study['records'] if r['selected']} if study else None
    with store.connect() as c:
        run=store.latest_run(c); rid=run_id or (run['id'] if run else '')
        rows=c.execute('''SELECT n.*, p.result,p.error,r.action AS review_action,r.label AS review_label
 FROM notices n LEFT JOIN predictions p ON p.record_id=n.id AND p.run_id=?
 LEFT JOIN reviews r ON r.id=(SELECT max(id) FROM reviews WHERE record_id=n.id)
 WHERE (?='' OR instr(lower(n.text),lower(?))>0 OR instr(lower(n.metadata),lower(?))>0 OR instr(lower(n.id),lower(?))>0)''',(rid,q,q,q,q)).fetchall()
        output=[]
        for row in rows:
            r=dict(row);m=json.loads(r['metadata']); ai=json.loads(r['result']) if r['result'] else None
            if cohort_ids is not None and r['id'] not in cohort_ids:continue
            verified=r['review_action']=='VERIFY'
            truth=Decision.model_validate_json(r['review_label']) if verified else None
            is_correct=(truth.status().value==ai['classification']) if truth and ai else None
            if classification and (not ai or ai['classification']!=classification):continue
            if any(v and m.get(k)!=v for k,v in [('country',country),('market',market),('language',language),('event_type',event_type)]):continue
            if ai and not min_confidence<=ai['confidence']<=max_confidence:continue
            if review=='verified' and not verified:continue
            if review=='unreviewed' and verified:continue
            if correct=='correct' and is_correct is not True:continue
            if correct=='incorrect' and is_correct is not False:continue
            if queue and (verified or not ai):continue
            output.append(dict(id=r['id'],**{k:m.get(k) for k in ['issuer','isin','market','country','event_type','meeting_date','language']},
                split=r['split'],classification=ai['classification'] if ai else None,confidence=ai['confidence'] if ai else None,
                action=ai['action'] if ai else None,review_status='Verified' if verified else 'Flagged' if r['review_action']=='FLAG' else 'Unreviewed',
                correct=is_correct,error=r['error'],priority=(ai['confidence'] if ai else 1,
                    0 if ai and any('Conflicting' in x for x in ai['review_reasons']) else 1,
                    0 if ai and ai['decision']['votable']=='YES' else 1,
                    0 if ai and (ai['decision']['share_blocking'] or ai['decision']['poa_required']) else 1)))
        if queue:output.sort(key=lambda r:r['priority'])
        for r in output:r.pop('priority')
    return {'items':output[(page-1)*page_size:page*page_size],'total':len(output),'page':page,'page_size':page_size}

@app.get('/api/facets')
def facets():
    from collections import defaultdict
    fields=defaultdict(set)
    with store.connect() as c:
        for r in c.execute('SELECT metadata FROM notices'):
            m=json.loads(r[0])
            for key in ['country','market','language','event_type']:fields[key].add(m.get(key) or 'UNKNOWN')
    return {k:sorted(v) for k,v in fields.items()}

@app.get('/api/notice')
def detail(id:str,run_id:str|None=None,blind:bool=False):
    with store.connect() as c:
        r=c.execute('SELECT * FROM notices WHERE id=?',(id,)).fetchone()
        if not r:raise HTTPException(404,'Notice not found')
        result=dict(r);result['metadata']=json.loads(result['metadata']);result['prediction']=store.prediction(c,id,run_id)
        run=store.latest_run(c);result['run_id']=run_id or (run['id'] if run else None)
        config=c.execute('SELECT config FROM runs WHERE id=?',(result['run_id'],)).fetchone()
        from classifier.laya_classifier import load_config
        result['evaluation_date']=json.loads(config[0])['evaluation_date'] if config else load_config()['evaluation_date']
        failure=c.execute('SELECT error FROM predictions WHERE record_id=? AND run_id=?',(id,result['run_id'])).fetchone()
        result['classification_error']=failure[0] if failure else None
        result['review']=store.latest_review(c,id)
        result['history']=[dict(x) for x in c.execute('SELECT id,reviewer,reviewed_at,label,notes,action,previous_revision,run_id FROM reviews WHERE record_id=? ORDER BY id DESC',(id,))]
        result['blind_review']=blind
        if blind:
            result['prediction']=None
            if result['review']:result['review']['previous_prediction']=None
        from apps.api.decision_evidence import decision_evidence,VERSION
        result['decision_evidence']=decision_evidence(result['text'],result['metadata'],result['prediction'],result['evaluation_date'])
        result['decision_evidence_version']=VERSION
        result['decision_configuration']=None if blind or not config else json.loads(config[0])
        from apps.api.hybrid_views import inspect
        result['hybrid_inspection']=None if blind else inspect(result['text'])
        from apps.api.semantic_views import latest_notice_analysis
        from semantic_runtime.config import configured_architecture
        result['semantic_execution']=None if blind else latest_notice_analysis(id)
        from apps.api.domain_views import latest
        result['domain_execution']=None if blind else latest(id)
        from apps.api.fast_cascade_views import latest as latest_cascade
        result['fast_cascade_execution']=None if blind else latest_cascade(id)
        result['fast_cascade_enabled']=not blind and os.environ.get('LAYA_FIRST_ENABLED','false').lower()=='true'
        result['classification_architecture']=configured_architecture()[0]
    return result

class ReviewRequest(BaseModel):
    record_id:str
    run_id:str|None=None
    reviewer:str=Field(min_length=1,max_length=120)
    decision:Decision|None=None
    notes:str=Field(default='',max_length=10000)
    action:str='VERIFY'
    expected_revision:int|None=None
    domain_expert_attested:bool=False
    blind_review:bool=False

@app.post('/api/reviews',status_code=201)
def review(body:ReviewRequest):
    if body.action not in ['VERIFY','FLAG']:raise HTTPException(422,'Invalid review action')
    if body.action=='VERIFY' and body.decision is None:raise HTTPException(422,'Verified factors required')
    if not body.reviewer.strip():raise HTTPException(422,'Reviewer identity required')
    with store.connect() as c:
        c.execute('BEGIN IMMEDIATE')
        if not c.execute('SELECT id FROM notices WHERE id=?',(body.record_id,)).fetchone():raise HTTPException(404,'Notice not found')
        previous=store.latest_review(c,body.record_id)
        if body.expected_revision != (previous['id'] if previous else None):raise HTTPException(409,'Review changed; reload before saving')
        if body.run_id and not c.execute('SELECT id FROM runs WHERE id=?',(body.run_id,)).fetchone():raise HTTPException(404,'Run not found')
        ai=store.prediction(c,body.record_id,body.run_id)
        correct=all(body.decision.model_dump()[k]==ai['decision'][k] for k in ['votable','share_blocking','poa_required','other_restriction','deadline_status']) if body.decision and ai else None
        from classifier.laya_classifier import load_config
        ref=c.execute('SELECT config FROM runs WHERE id=?',(body.run_id,)).fetchone() if body.run_id else None
        context={'evaluation_date':json.loads(ref[0])['evaluation_date'] if ref else load_config()['evaluation_date'],'schema_version':'factorised-v1','source_hash':c.execute('SELECT source_hash FROM notices WHERE id=?',(body.record_id,)).fetchone()[0]}
        context.update(domain_expert_attested=body.domain_expert_attested,blind_review=body.blind_review,provenance='Human entry; expertise and blindness are reviewer attestations, not independently authenticated')
        cur=c.execute('INSERT INTO reviews(record_id,run_id,previous_revision,reviewer,reviewed_at,label,notes,action,previous_prediction,ai_correct,context) VALUES (?,?,?,?,?,?,?,?,?,?,?)',
            (body.record_id,body.run_id,previous['id'] if previous else None,body.reviewer.strip(),store.now(),body.decision.model_dump_json() if body.decision else None,body.notes,body.action,store.dumps(ai) if ai else None,correct,store.dumps(context)))
        return {'revision':cur.lastrowid,'golden':body.action=='VERIFY'}

@app.get('/api/performance')
def performance(run_id:str|None=None,split:str='test'):
    if split not in ['test','validation','train','all']:raise HTTPException(422,'Unknown split')
    return evaluate(run_id,split)

@app.get('/api/experiment')
def experiment():
    from evaluation.experiment import evidence
    return evidence()

@app.get('/api/experiment/errors')
def experiment_errors(model:str='fine-tuned',dataset:str='challenge',field:str='',expected:str='',predicted:str='',min_confidence:float=Query(0,ge=0,le=1)):
    from evaluation.experiment import synthetic_errors
    if model not in ['base','fine-tuned']:raise HTTPException(422,'Unknown model')
    if dataset not in ['test','challenge']:raise HTTPException(422,'Unknown evaluation corpus')
    rows=synthetic_errors(model,dataset)
    if field and field not in ['votable','share_blocking','poa_required','other_restriction','deadline_status']:raise HTTPException(422,'Unknown factor')
    def value(v):return 'UNKNOWN' if v is None else 'YES' if v is True else 'NO' if v is False else v
    return {'provenance':'Authored partial-assertion semantic challenge' if dataset=='challenge' else 'AI-authored synthetic test, not customer accuracy','dataset':dataset,'items':[r for r in rows if r['confidence']>=min_confidence and (not field or field in r['failed_fields']) and (not expected or expected==(value(r['expected'].get(field)) if field else r['expected_customer_status'])) and (not predicted or predicted==(value(r['observed'].get(field)) if field else r['predicted_customer_status']))]}

@app.get('/api/experiment/figure')
def experiment_figure(name:str):
    if name not in ['learning-curve.svg','automation-curve.svg','training-loss.png']:raise HTTPException(422,'Unknown figure')
    p=ROOT/'data/experiments/supplied-synthetic-v1'/name
    if not p.is_file():raise HTTPException(404,'Figure has not been generated')
    return FileResponse(p)

@app.get('/api/comparison')
def comparison(split:str='test'):
    if split not in ['test','validation','all']:raise HTTPException(422,'Unknown split')
    with store.connect() as c:
        runs=[dict(r) for r in c.execute('SELECT * FROM runs ORDER BY created_at DESC')]
    output=[]
    for r in runs:
        m=evaluate(r['id'],split)
        b=json.loads(r['benchmark']) if r['benchmark'] else {}
        output.append({'run_id':r['id'],'model':r['model'],'model_version':r['model_version'],
            'status':r['status'],'verified_n':m['n'],'accuracy':m['accuracy'],'macro_f1':m.get('macro_f1'),
            'auto_coverage':m.get('auto_processed',0)/m['n'] if m['n'] else None,
            'median_latency_ms':b.get('median_amortised_inference_ms')})
    return output

@app.get('/api/export')
def export(kind:str='results',run_id:str|None=None):
    if kind not in ['results','golden','audit','evaluation']:raise HTTPException(422,'Unknown export type')
    if kind=='evaluation':
        content=store.dumps(evaluate(run_id))+'\n'
    else:
        with store.connect() as c:
            run=store.latest_run(c);rid=run_id or (run['id'] if run else '')
            if kind=='results':
                rows=c.execute('SELECT p.*,n.text,n.metadata,n.split,n.group_id FROM predictions p JOIN notices n ON n.id=p.record_id WHERE p.run_id=? ORDER BY p.record_id',(rid,)).fetchall()
                data=[]
                for row in rows:
                    r=dict(row);r['human_review']=store.latest_review(c,r['record_id']); data.append(r)
            else:
                query='SELECT r.*,n.text,n.source_hash,n.group_id,n.split FROM reviews r JOIN notices n ON n.id=r.record_id'
                if kind=='golden':query+=" WHERE r.action='VERIFY' AND r.id=(SELECT max(id) FROM reviews WHERE record_id=r.record_id)"
                data=[dict(r) for r in c.execute(query)]
            for r in data:
                for key in ['result','metadata','label','previous_prediction','context']:
                    if isinstance(r.get(key),str):r[key]=json.loads(r[key])
            content=''.join(store.dumps(r)+'\n' for r in data)
    return StreamingResponse(iter([content]),media_type='application/x-ndjson',headers={'Content-Disposition':f'attachment; filename="laya-{kind}.jsonl"'})

class RunRequest(BaseModel):
    reproduce:str|None=None
    resume:str|None=None

@app.post('/api/runs',status_code=202)
def start_run(body:RunRequest):
    if os.environ.get("VOTING_DISABLE_JOBS")=="1":raise HTTPException(403,"Batch jobs disabled in this test environment")
    # One model worker at a time, including across API restarts via the persisted run state.
    with store.connect() as c:
        if c.execute("SELECT id FROM runs WHERE status='RUNNING'").fetchone():raise HTTPException(409,'A run is active; resume an interrupted run from CLI if needed')
        if body.reproduce:
            parent=c.execute('SELECT config FROM runs WHERE id=?',(body.reproduce,)).fetchone()
            if not parent:raise HTTPException(404,'Unknown run')
            if 'option_order' not in json.loads(parent[0]):raise HTTPException(422,'Legacy run predates explicit option ordering; use its source archive to inspect the original schema and start a new run')
    if not job_lock.acquire(blocking=False):raise HTTPException(409,'A batch is already starting')
    def work():
        try:
            from scripts.run_batch import run_batch
            run_batch(reproduce=body.reproduce,resume=body.resume)
        finally:job_lock.release()
    threading.Thread(target=work,daemon=True).start()
    return {'status':'starting'}

app.mount('/assets',StaticFiles(directory=ROOT/'apps/web'),name='assets')
@app.get('/')
def index():return FileResponse(ROOT/'apps/web/index.html')

# Versioned complete architecture, separate from historical frozen run format.
from apps.api.semantic_views import router as semantic_router
app.include_router(semantic_router)

from apps.api.cascade_views import router as cascade_router
app.include_router(cascade_router)

from apps.api.domain_views import router as domain_router
app.include_router(domain_router)

from apps.api.fast_cascade_views import router as fast_cascade_router
app.include_router(fast_cascade_router)
