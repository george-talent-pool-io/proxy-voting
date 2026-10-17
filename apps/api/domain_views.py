"""Read-only domain research views plus explicit opt-in, append-only Qwen analyses."""
import os,json,uuid
from pathlib import Path
from fastapi import APIRouter,HTTPException
from pydantic import BaseModel,Field,ConfigDict
from typing import Literal
from apps.api import store
from qwen_domain.protocol import ROOT,STUDY,CORPUS,read,now,digest
router=APIRouter(prefix='/api/domain')
def optional(path):
    try:return read(path)
    except (FileNotFoundError,json.JSONDecodeError):return None
@router.get('/status')
def status():
    manifest=optional(CORPUS/'MANIFEST.json')
    return {'state':optional(STUDY/'LIVE-STATUS.json'),'corpus':{k:{q:v[q] for q in ['n','groups','languages','difficulty']} for k,v in manifest['splits'].items()} if manifest else None,
        'calibration':{a:optional(STUDY/f'{a}-CALIBRATION.json') for a in ['BASE_QWEN_DIRECT','CONSTRAINED_QWEN']},
        'training_decision':(optional(STUDY/'TRAINING-DECISION.json') or {}).get('status'),'summary':optional(STUDY/'SUMMARY.json'),
        'confidence_kind':'HEURISTIC / NOT YET CALIBRATED' if not (STUDY/'BASE_QWEN_DIRECT-CALIBRATION.json').exists() else 'See per-predicate held-out support; unavailable probabilities remain null',
        'confidence':None,'automation_enabled':False,'customer_accuracy':None,'scope':'Benchmark performance only; synthetic calibration is not customer calibration',
        'confidence_diagnostics':{a:optional(STUDY/f'{a}-CALIBRATION-CONFIDENCE-DIAGNOSTICS.json') for a in ['BASE_QWEN_DIRECT','CONSTRAINED_QWEN']}}
def latest(record_id):
    with store.connect() as c:
        if not c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='domain_executions'").fetchone():return None
        r=c.execute('SELECT * FROM domain_executions WHERE record_id=? ORDER BY created_at DESC,rowid DESC LIMIT 1',(record_id,)).fetchone()
        if not r:return None
        out=dict(r);out['result']=json.loads(out['result']);return out
class Analyse(BaseModel):record_id:str
@router.post('/analyse')
def analyse(body:Analyse):
    if os.environ.get('DOMAIN_QWEN_ENABLED','false').lower()!='true':raise HTTPException(403,'Qwen domain analysis is opt-in; benchmark/calibration is still experimental')
    with store.connect() as c:
        row=c.execute('SELECT * FROM notices WHERE id=?',(body.record_id,)).fetchone()
        if not row:raise HTTPException(404,'Notice not found')
        source=dict(row)
    from qwen_domain.pipeline import DomainPipeline
    from qwen_domain.confidence import CorrectnessCalibrator
    from qwen_domain.study import verify
    try:
        verify();pipeline=DomainPipeline('BASE_QWEN_DIRECT')
        cal=STUDY/'BASE_QWEN_DIRECT-calibrator.joblib'
        if cal.exists():pipeline.calibrator=CorrectnessCalibrator.load(cal,pipeline.identity)
        result=pipeline.analyse(source['text'],language=json.loads(source['metadata']).get('language','en'))
    except (ValueError,RuntimeError,OSError) as e:raise HTTPException(503,str(e))
    ident=str(uuid.uuid4());created=now()
    with store.connect() as c:
        tables(c)
        c.execute('INSERT INTO domain_executions VALUES(?,?,?,?,?)',(ident,body.record_id,digest(source['text']),created,json.dumps(result,ensure_ascii=False)))
    return {'id':ident,'record_id':body.record_id,'source_hash':digest(source['text']),'created_at':created,'result':result}

def tables(c):
    c.executescript('''
CREATE TABLE IF NOT EXISTS domain_executions(id TEXT PRIMARY KEY,record_id TEXT NOT NULL REFERENCES notices(id),source_hash TEXT NOT NULL,created_at TEXT NOT NULL,result TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS domain_reviews(id INTEGER PRIMARY KEY AUTOINCREMENT,record_id TEXT NOT NULL REFERENCES notices(id),previous_revision INTEGER REFERENCES domain_reviews(id),source_hash TEXT NOT NULL,created_at TEXT NOT NULL,reviewer TEXT NOT NULL,label TEXT NOT NULL,context TEXT NOT NULL,previous_prediction TEXT);
CREATE TRIGGER IF NOT EXISTS immutable_domain_execution_update BEFORE UPDATE ON domain_executions BEGIN SELECT RAISE(ABORT,'Domain executions are immutable'); END;
CREATE TRIGGER IF NOT EXISTS immutable_domain_execution_delete BEFORE DELETE ON domain_executions BEGIN SELECT RAISE(ABORT,'Domain executions are immutable'); END;
CREATE TRIGGER IF NOT EXISTS immutable_domain_review_update BEFORE UPDATE ON domain_reviews BEGIN SELECT RAISE(ABORT,'Domain reviews are immutable'); END;
CREATE TRIGGER IF NOT EXISTS immutable_domain_review_delete BEFORE DELETE ON domain_reviews BEGIN SELECT RAISE(ABORT,'Domain reviews are immutable'); END;
''')

class FullLabel(BaseModel):
    model_config=ConfigDict(extra='forbid')
    votability:Literal['VOTABLE','NOT_VOTABLE','UNCERTAIN']
    share_blocking:Literal['YES','NO','UNKNOWN']
    poa_required:Literal['YES','NO','UNKNOWN']
    registration_required:Literal['YES','NO','UNKNOWN']
    beneficial_owner_disclosure_required:Literal['YES','NO','UNKNOWN']
    holding_confirmation_required:Literal['YES','NO','UNKNOWN']
    split_voting_restricted:Literal['YES','NO','UNKNOWN']
    securities_lending_recall_required:Literal['YES','NO','UNKNOWN']
    other_voting_restriction:Literal['YES','NO','UNKNOWN']
    deadline_status:Literal['OPEN','PASSED','UNKNOWN']

class FullReview(BaseModel):
    record_id:str
    expected_revision:int|None=None
    reviewer:str=Field(min_length=1,max_length=120)
    label:FullLabel
    notes:str=Field(default='',max_length=10000)
    domain_expert_attested:bool=False
    blind_review:bool=False
    evaluation_time:str='2026-10-17T12:00:00+00:00'

@router.get('/reviews/{record_id}')
def reviews(record_id:str):
    with store.connect() as c:
        if not c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='domain_reviews'").fetchone():return {'items':[]}
        items=[]
        for row in c.execute('SELECT id,record_id,previous_revision,source_hash,created_at,reviewer,label,context FROM domain_reviews WHERE record_id=? ORDER BY id',(record_id,)):
            r=dict(row);r['label']=json.loads(r['label']);r['context']=json.loads(r['context']);items.append(r)
        return {'items':items}

@router.post('/reviews',status_code=201)
def review(body:FullReview):
    from datetime import datetime
    from semantic_pipeline.decision import decide
    if not body.reviewer.strip():raise HTTPException(422,'Reviewer identity required')
    try:
        ref=datetime.fromisoformat(body.evaluation_time.replace('Z','+00:00'))
        if ref.tzinfo is None:raise ValueError()
    except ValueError:raise HTTPException(422,'Evaluation time must be ISO8601 with timezone')
    prediction=latest(body.record_id)
    from apps.api.fast_cascade_views import latest as latest_cascade
    cascade_prediction=latest_cascade(body.record_id)
    if cascade_prediction and (prediction is None or cascade_prediction['created_at']>prediction['created_at']):prediction=cascade_prediction
    with store.connect() as c:
        tables(c);c.execute('BEGIN IMMEDIATE')
        record=c.execute('SELECT source_hash,group_id,split FROM notices WHERE id=?',(body.record_id,)).fetchone()
        if not record:raise HTTPException(404,'Notice not found')
        old=c.execute('SELECT id FROM domain_reviews WHERE record_id=? ORDER BY id DESC LIMIT 1',(body.record_id,)).fetchone()
        previous=old['id'] if old else None
        if previous!=body.expected_revision:raise HTTPException(409,'Review changed; reload before saving')
        label=body.label.model_dump();status=decide({k:{'value':v} for k,v in label.items() if k!='deadline_status'},{'status':label['deadline_status']})['classification']
        context={'schema':'domain-nine-predicate-v1','evaluation_time':ref.isoformat(),'classification':status,'split':record['split'],'duplicate_group':record['group_id'],
            'domain_expert_attested':body.domain_expert_attested,'blind_review_attested':body.blind_review,'validation_type':'HUMAN_ENTRY_EXPERTISE_NOT_INDEPENDENTLY_AUTHENTICATED','notes':body.notes,'source_hash':record['source_hash'],
            'training_eligible':record['split']=='train','previous_prediction_execution_id':prediction['id'] if prediction else None,
            'previous_prediction_architecture':prediction['result'].get('architecture') if prediction else None,
            'ai_exact_match':all(prediction['result']['predicates'].get(k,{}).get('value')==v for k,v in label.items()) if prediction else None}
        r=c.execute('INSERT INTO domain_reviews(record_id,previous_revision,source_hash,created_at,reviewer,label,context,previous_prediction) VALUES (?,?,?,?,?,?,?,?)',
            (body.record_id,previous,record['source_hash'],now(),body.reviewer.strip(),json.dumps(label),json.dumps(context),json.dumps(prediction) if prediction else None))
        return {'revision':r.lastrowid,'classification':status,'training_eligible':context['training_eligible'],'automation_enabled':False}
