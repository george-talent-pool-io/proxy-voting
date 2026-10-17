"""Opt-in local execution, append-only traces; reading views never invokes models."""
import os,json,uuid,threading
from fastapi import APIRouter,HTTPException
from pydantic import BaseModel
from apps.api import store
from fast_cascade.protocol import ROOT,STUDY,read,digest,now
router=APIRouter(prefix='/api/fast-cascade');_pipeline=None;_lock=threading.RLock()
def optional(p):return read(p) if p.exists() else None

def tables(c):
    c.executescript('''CREATE TABLE IF NOT EXISTS fast_cascade_executions(id TEXT PRIMARY KEY,record_id TEXT NOT NULL REFERENCES notices(id),source_hash TEXT NOT NULL,created_at TEXT NOT NULL,result TEXT NOT NULL);
CREATE TRIGGER IF NOT EXISTS immutable_fast_execution_update BEFORE UPDATE ON fast_cascade_executions BEGIN SELECT RAISE(ABORT,'Cascade executions are immutable'); END;
CREATE TRIGGER IF NOT EXISTS immutable_fast_execution_delete BEFORE DELETE ON fast_cascade_executions BEGIN SELECT RAISE(ABORT,'Cascade executions are immutable'); END;''')
def latest(record_id):
    with store.connect() as c:
        if not c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='fast_cascade_executions'").fetchone():return None
        r=c.execute('SELECT * FROM fast_cascade_executions WHERE record_id=? ORDER BY created_at DESC,rowid DESC LIMIT 1',(record_id,)).fetchone()
        return {**dict(r),'result':json.loads(r['result'])} if r else None

def persist(record_id,text,result):
    if result.get('input_hash')!=digest(text):raise ValueError('Execution source hash mismatch')
    ident=str(uuid.uuid4());created=now()
    with store.connect() as c:
        tables(c);c.execute('INSERT INTO fast_cascade_executions VALUES(?,?,?,?,?)',(ident,record_id,digest(text),created,json.dumps(result,ensure_ascii=False,allow_nan=False)))
    return {'id':ident,'record_id':record_id,'created_at':created,'source_hash':digest(text),'result':result}

@router.get('/status')
def status():
    selection=optional(STUDY/'SELECTION.json')
    return {'state':optional(STUDY/'LIVE-STATUS.json'),'selection':selection,'calibration':optional(STUDY/'CALIBRATION.json'),'confidence_coverage':optional(STUDY/'CONFIDENCE-COVERAGE.json'),
        'throughput':{str(n):optional(STUDY/f'THROUGHPUT_{n}-MEASUREMENT.json') for n in [100,1000]},
        'metrics':{s:optional(STUDY/f'{s}-METRICS.json') for s in ['SYNTHETIC_FROZEN_TEST','ADVERSARIAL_TEST','OOD_TEST','CHALLENGE']},
        'batching':optional(STUDY/'LAYA-BATCH-BENCHMARK.json'),'report':'data/reports/LAYA_FIRST_CASCADE_EVALUATION.md',
        'enabled':os.environ.get('LAYA_FIRST_ENABLED','false').lower()=='true','automation_enabled':False,'customer_accuracy':None,'scope':'Synthetic/authored benchmark performance. Actual manual review remains mandatory.'}

@router.get('/cases')
def cases(split:str='CHALLENGE'):
    if split not in ['CHALLENGE','VALIDATION','SYNTHETIC_FROZEN_TEST','ADVERSARIAL_TEST','OOD_TEST']:raise HTTPException(422,'Unsupported benchmark split')
    from fast_cascade.study import cached
    r=cached(split,'SELECTED_CASCADE')
    if split=='VALIDATION' and not r:
        sel=optional(STUDY/'SELECTION.json');r=cached(split,sel['selected_policy']['name']) if sel else []
    return {'items':[{'id':v['id'],'classification':v['result']['decision']['classification'],'resolved_by':v['result']['resolved_by']} for v in r],'split':split}

@router.get('/case')
def case(id:str,split:str='CHALLENGE'):
    if split not in ['CHALLENGE','VALIDATION','SYNTHETIC_FROZEN_TEST','ADVERSARIAL_TEST','OOD_TEST']:raise HTTPException(422,'Unsupported benchmark split')
    from fast_cascade.study import cached,inputs,label_cases
    if not (STUDY/'SELECTION.json').exists():raise HTTPException(409,'Routing selection is not frozen; protected truth is unavailable')
    if split!='VALIDATION' and not (STUDY/f'{split}-METRICS.json').exists():raise HTTPException(409,'Protected comparison is unavailable until blind final predictions are persisted and scored')
    c=next((c for c in inputs(split) if c['id']==id),None)
    if not c:raise HTTPException(404,'Case not found')
    models={}
    for name in ['LAYA','GEAR2','FULL','SELECTED_CASCADE']:
        r=next((r for r in cached(split,name) if r['id']==id),None)
        if r:models[name]=r['result']
    if not models:raise HTTPException(404,'No persisted predictions')
    truth=next((r['expected'] for r in label_cases(split) if r['id']==id),{})
    from fast_cascade.evaluation import values
    from fast_cascade.study import semantic_reference
    observed={name:values(result if 'decision' in result else semantic_reference(c,result,name)) for name,result in models.items()}
    return {'id':id,'text':c['text'],'expected':truth,'models':models,'observed':observed,'automation_enabled':False,'customer_accuracy':None}

class Analyse(BaseModel):record_id:str
@router.post('/analyse')
def analyse(body:Analyse):
    if os.environ.get('LAYA_FIRST_ENABLED','false').lower()!='true':raise HTTPException(403,'Laya-first cascade is experimental and disabled by default')
    with store.connect() as c:
        r=c.execute('SELECT text,metadata FROM notices WHERE id=?',(body.record_id,)).fetchone()
        if not r:raise HTTPException(404,'Notice not found')
    global _pipeline
    with _lock:
        resource=None
        try:
            from training.framework.resources import model_resource
            resource=model_resource('fast-cascade-inference')
            resource.__enter__()
            from fast_cascade.study import verify
            from fast_cascade.pipeline import Pipeline
            from fast_cascade.models import SharedQwen
            from fast_cascade.laya import BatchedLaya
            from fast_cascade.routing import Policy
            from qwen_domain.confidence import CorrectnessCalibrator
            verify();sel=read(STUDY/'SELECTION.json')
            if _pipeline is None:
                _pipeline=Pipeline(Policy(**sel['selected_policy']),laya=BatchedLaya(8),qwen=SharedQwen(),preferences=sel['preferences'])
                cal=STUDY/'calibrator.joblib'
                if cal.exists():_pipeline.calibrator=CorrectnessCalibrator.load(cal,_pipeline.identity)
            result=_pipeline.analyse(r['text'],language=json.loads(r['metadata']).get('language','en'))
            return persist(body.record_id,r['text'],result)
        except (ValueError,RuntimeError,OSError) as e:raise HTTPException(503,str(e))
        finally:
            if resource is not None:resource.__exit__(None,None,None)
