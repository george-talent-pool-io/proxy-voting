"""Narrow customer service. Research/debug APIs are deliberately not mounted."""
import json
import os
import time
import uuid
from collections import OrderedDict
from contextlib import asynccontextmanager
from pathlib import Path
from urllib.parse import urlsplit

from fastapi import FastAPI, Request, Depends, HTTPException
from fastapi.responses import JSONResponse, FileResponse, Response
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, ConfigDict, Field, model_validator
from apps.api import store
from production import security, storage, service, worker, qualification
from training.framework import jobs, events, event_data, campaigns, releases

ROOT = Path(__file__).resolve().parents[2]


def require(*roles):
    def permission(request: Request):
        user = request.state.user
        if not set(user['roles']) & set(roles): raise HTTPException(403, 'Role not permitted')
        return user
    return permission


def create_app():
    @asynccontextmanager
    async def lifespan(app):
        app.state.users, app.state.origin = security.configuration()
        storage.initialise(); worker.initialise(); jobs.WORKSPACE.mkdir(parents=True, exist_ok=True)
        yield
        from iso_adapter.routing import _REFERENCE
        _REFERENCE.close()
    app = FastAPI(title='Voting Intelligence Framework', version='1.0.0', lifespan=lifespan,
                  docs_url=None, redoc_url=None, openapi_url=None)
    failures = OrderedDict()

    @app.middleware('http')
    async def boundary(request, call_next):
        request_id = str(uuid.uuid4())
        if request.url.path == '/health/live': return JSONResponse({'status': 'alive'})
        if request.headers.get('host', '').lower() != urlsplit(app.state.origin).netloc.lower(): return JSONResponse({'detail': 'Host not permitted'}, 403)
        ip = request.client.host if request.client else 'unknown'; now = time.monotonic()
        failed, until = failures.get(ip, (0, now))
        if failed >= 10 and now < until: return JSONResponse({'detail': 'Authentication temporarily rate limited'}, 429, headers={'Retry-After': str(max(1, int(until-now)))})
        user = security.authenticate(request.headers.get('authorization', ''), app.state.users)
        if user is None:
            failures[ip] = ((failed if now < until else 0) + 1, now + 60)
            if len(failures) > 10000: failures.popitem(last=False)
            return JSONResponse({'detail': 'Named-user authentication required'}, 401, headers={'WWW-Authenticate': 'Basic realm="Voting Intelligence Framework", charset="UTF-8"'})
        failures.pop(ip, None); request.state.user = user
        if request.method not in ('GET', 'HEAD', 'OPTIONS'):
            origin = request.headers.get('origin')
            if (origin and origin != app.state.origin) or request.headers.get('sec-fetch-site') == 'cross-site': return JSONResponse({'detail': 'Cross-origin write rejected'}, 403)
            try:
                if int(request.headers.get('content-length', '0')) > 16 * 1024 * 1024: return JSONResponse({'detail': 'Request too large'}, 413)
            except ValueError: return JSONResponse({'detail': 'Invalid content length'}, 400)
            chunks = []; total = 0
            async for chunk in request.stream():
                total += len(chunk)
                if total > 16 * 1024 * 1024: return JSONResponse({'detail': 'Request too large'}, 413)
                chunks.append(chunk)
            request._body = b''.join(chunks)
        try: response = await call_next(request)
        except Exception:
            storage.audit(user['name'], 'REQUEST_FAILED', {'request_id': request_id, 'path': request.url.path})
            response = JSONResponse({'detail': 'Operation failed; inspect local audit using request ID', 'request_id': request_id}, 500)
        response.headers.update({'X-Request-ID': request_id, 'X-Content-Type-Options': 'nosniff', 'Cache-Control': 'no-store',
            'Referrer-Policy': 'no-referrer', 'Strict-Transport-Security': 'max-age=31536000',
            'Content-Security-Policy': "default-src 'self'; script-src 'self'; style-src 'self'; img-src 'self' data:; connect-src 'self'; frame-ancestors 'none'; base-uri 'self'; form-action 'self'"})
        return response

    @app.exception_handler(ValueError)
    async def bad_value(request, exc): return JSONResponse({'detail': str(exc)}, 409)
    @app.exception_handler(FileNotFoundError)
    async def missing(request, exc): return JSONResponse({'detail': 'Requested local artifact not found'}, 404)
    @app.exception_handler(FileExistsError)
    async def exists(request, exc): return JSONResponse({'detail': 'Immutable artifact already exists; choose a new identifier'}, 409)

    read = require('ADMIN', 'TRAINER', 'REVIEWER', 'AUDITOR')
    train = require('ADMIN', 'TRAINER')
    admin = require('ADMIN')

    @app.get('/')
    def index(user=Depends(read)): return FileResponse(ROOT / 'apps/web/client.html')
    app.mount('/assets', StaticFiles(directory=ROOT / 'apps/web'), name='assets')

    @app.get('/api/client/status')
    def status(user=Depends(read)):
        with store.connect() as c:
            counts = dict(c.execute('SELECT split,count(*) FROM learning_events GROUP BY split').fetchall())
            latest = c.execute('SELECT payload FROM client_promotions ORDER BY id DESC LIMIT 1').fetchone()
            reviews = dict(c.execute("SELECT json_extract(payload,'$.provenance.origin'),count(*) FROM learning_reviews GROUP BY 1").fetchall())
            n = c.execute('SELECT count(*) FROM client_decisions').fetchone()[0]
            reviewed = c.execute("SELECT count(*) FROM client_decisions WHERE json_extract(payload,'$.decision.review_required')=1").fetchone()[0]
            audits = c.execute("SELECT count(*) FROM client_decisions WHERE json_extract(payload,'$.decision.audit_selection.selected')=1").fetchone()[0]
            eligible = c.execute("SELECT count(*) FROM client_decisions WHERE json_extract(payload,'$.decision.audit_selection.pre_audit_eligible')=1").fetchone()[0]
            suspensions = c.execute('SELECT count(*) FROM client_suspensions').fetchone()[0]
        return {'identity': user, 'events_by_role': counts, 'label_revisions_by_origin': reviews,
                'tasks': worker.listing(), 'worker': worker.health(), 'campaigns': [{'id': x['id'], 'state': x['state']} for x in campaigns.listing()], 'audit': storage.verify_audit(),
                'production_promotion': json.loads(latest[0]) if latest else None,
                'processed': n, 'review_required': reviewed, 'observed_review_rate': reviewed / n if n else None,
                'monitoring': {'otherwise_accepted_decisions': eligible, 'random_audit_reviews': audits,
                               'other_review_decisions': reviewed - audits, 'release_suspensions': suspensions,
                               'observed_random_audit_rate': audits / eligible if eligible else None},
                'automation_switch': os.environ.get('AUTOMATION_ENABLED', 'false') == 'true',
                'customer_accuracy': None, 'deployment': 'SINGLE_TENANT_LINUX',
                'qualification_required': True, 'training_enabled': os.environ.get('TRAINING_EXECUTION_ENABLED', 'false') == 'true'}

    @app.get('/api/client/ready')
    def ready(user=Depends(read)):
        with store.connect() as c: ok = c.execute('PRAGMA quick_check').fetchone()[0] == 'ok'
        jar = ROOT / 'tools/prowide/target/prowide-helper-1.0.0.jar'
        import shutil
        checks = {'database': ok, 'jvm': bool(shutil.which('java')), 'prowide_helper': jar.exists(),
                  'workspace_writable': os.access(jobs.WORKSPACE, os.W_OK), 'named_identities': bool(app.state.users), 'audit': storage.verify_audit()['valid']}
        if os.environ.get('VOTING_REQUIRE_WORKER','false')=='true':checks['model_worker_alive']=worker.health()['healthy']
        return JSONResponse({'ready': all(checks.values()), 'checks': checks, 'model_qualified': bool(status(user)['production_promotion'])}, 200 if all(checks.values()) else 503)

    class Import(BaseModel):
        model_config = ConfigDict(extra='forbid')
        id: str
        rows: list[dict] = Field(min_length=1, max_length=1000)
    @app.post('/api/client/imports', status_code=201)
    def imports(body: Import, user=Depends(train)): return service.import_rows(body.id, body.rows, user['name'])

    @app.get('/api/client/events')
    def listing(q: str = '', split: str = '', offset: int = 0, user=Depends(read)):
        if offset < 0: raise ValueError('Invalid offset')
        values = [r for r in events.listing() if (not q or q.casefold() in (r['corp'] + r['sender']).casefold()) and (not split or r['split'] == split)]
        return {'total': len(values), 'items': values[offset:offset+100]}
    @app.get('/api/client/events/{ident}')
    def detail(ident: str, user=Depends(read)): return service.source_view(ident)

    class ReviewBody(BaseModel):
        model_config = ConfigDict(extra='forbid')
        snapshot_hash: str
        expected_revision: int | None = None
        target: __import__('semantic_pipeline.schema', fromlist=['SemanticResult']).SemanticResult
        notes: str = Field(default='', max_length=10000)
        expected_deadline_status: LiteralDeadline | None = None
        expected_final_status: str | None = None
        model_id: str | None = None
        evaluation_time: str | None = None
    @app.post('/api/client/events/{ident}/reviews', status_code=201)
    def review(ident: str, body: ReviewBody, user=Depends(require('REVIEWER'))):
        if body.model_id: raise ValueError('Human review cannot claim an AI model; use AI-label import')
        return service.review(ident, body.model_dump(exclude={'model_id'}), user)
    @app.post('/api/client/events/{ident}/ai-labels', status_code=201)
    def ai_label(ident: str, body: ReviewBody, user=Depends(train)):
        return service.review(ident, body.model_dump(), user, ai=True)

    class Freeze(BaseModel):
        id: str
        event_ids: list[str] = Field(min_length=1, max_length=100000)
    @app.post('/api/client/datasets', status_code=201)
    def freeze(body: Freeze, user=Depends(train)): return service.freeze(body.id, body.event_ids, user['name'])

    class Export(BaseModel):
        id: str
    @app.post('/api/client/training-bundles', status_code=201)
    def bundle(body: Export, user=Depends(train)):
        result = event_data.export_reviews(jobs.member('bundles', body.id)); storage.audit(user['name'], 'TRAINING_BUNDLE_EXPORTED', {'id': body.id}); return result

    @app.get('/api/client/starting-checkpoints')
    def starting_checkpoints(user=Depends(read)):
        from training.framework.profiles import seed_readiness
        values = [{'id': p.parent.name, **json.loads(p.read_text())} for p in (jobs.WORKSPACE / 'seeds').glob('*/seed.json')]
        return [{**value, 'readiness': seed_readiness(value)} for value in values]

    @app.get('/api/client/training-profiles')
    def training_profiles(user=Depends(read)):
        from training.framework.profiles import listing
        return listing(linux_only=True)

    class DerivativeSeed(BaseModel):
        model_config=ConfigDict(extra='forbid')
        id: str
        job_id: str

    @app.post('/api/client/starting-checkpoints/from-job',status_code=201)
    def freeze_derivative(body: DerivativeSeed,user=Depends(train)):
        from training.framework import seeds
        from training.framework.runtime import verify_checkpoint
        job=jobs.member('jobs',body.job_id)
        _,_,manifest=verify_checkpoint(job)
        origin='AI_TEST_DERIVATIVE' if any(k.startswith('AI') for k in manifest['label_origins']) else 'CUSTOMER_DERIVATIVE'
        result=seeds.export_derivative(job,jobs.member('seeds',body.id),origin=origin)
        storage.audit(user['name'],'DERIVATIVE_CHECKPOINT_FROZEN',{'id':body.id,'job':body.job_id,
                      'identity':result['identity'],'origin':origin})
        return result

    @app.get('/api/client/calibrators')
    def calibrators(user=Depends(read)):
        return [{'id':p.stem, **{k:v for k,v in json.loads(p.read_text()).items() if k!='models'}}
                for p in (jobs.WORKSPACE/'customer-calibrators').glob('*.json')]

    @app.post('/api/client/operating-points/{ident}', status_code=201)
    def operating_point(ident: str, body: OperatingPointBody, user=Depends(train)):
        return service.select_operating_point(ident,**body.model_dump(),actor=user['name'])

    @app.post('/api/client/releases/{ident}', status_code=201)
    def prepare_release(ident: str, body: releases.ReleaseSpec, user=Depends(train)):
        result = releases.prepare(body, jobs.member('releases', ident))
        storage.audit(user['name'], 'RELEASE_PREPARED', {'id': ident, 'identity': result['identity']})
        return result

    @app.post('/api/client/campaigns/{ident}', status_code=201)
    def campaign(ident: str, body: dict, user=Depends(train)):
        spec = campaigns.CampaignSpec.model_validate({**body, 'actor': user['name']})
        models = Path(os.environ.get('VOTING_MODELS_ROOT', ROOT / 'data/models')).resolve()
        for stage in spec.stages:
            if stage.training:
                if stage.training.parent_seed_path and Path(stage.training.parent_seed_path).resolve().parent != (jobs.WORKSPACE/'seeds').resolve():
                    raise ValueError('Training parent must be a managed frozen starting checkpoint')
                if stage.training.backend == 'MLX_QLORA' or stage.training.runtime_python: raise ValueError('Linux uses LAYA_SDK or TRANSFORMERS_PEFT; executable paths are not accepted')
                from production.installation import training_admission,training_base_admission
                training_base_admission(stage.training,models)
                training_admission(stage.training)
        from production import learning
        result = learning.prepare(spec.model_dump(), jobs.member('campaigns', ident))
        storage.audit(user['name'], 'CAMPAIGN_PREPARED', {'id': ident}); return result

    @app.post('/api/client/campaigns/{ident}/start', status_code=202)
    def start(ident: str, user=Depends(train)):
        if os.environ.get('TRAINING_EXECUTION_ENABLED', 'false') != 'true': raise HTTPException(403, 'Training execution is disabled')
        from production import learning
        result = learning.spawn(jobs.member('campaigns', ident)); storage.audit(user['name'], 'CAMPAIGN_STARTED', {'id': ident}); return result
    @app.post('/api/client/campaigns/{ident}/cancel')
    def cancel_campaign(ident: str, user=Depends(train)):
        result = campaigns.cancel(jobs.member('campaigns', ident)); storage.audit(user['name'], 'CAMPAIGN_CANCELLED', {'id': ident}); return result

    @app.post('/api/client/tasks/{ident}', status_code=202)
    def submit(ident: str, body: TaskBody, user=Depends(train)):
        from production.installation import inference_admission
        payload = body.payload
        if body.kind == 'INFERENCE':
            request = Inference.model_validate(payload); payload = request.model_dump()
            (releases.verify if request.review_only_unsealed else releases.verify_seal)(jobs.member('releases', request.release_id))
            inference_admission(jobs.member('releases', request.release_id))
            for eid in request.event_ids:
                if events.get(eid)['split'] in ('CALIBRATION', 'FROZEN_TEST'): raise ValueError('Protected input cannot be explored through inference')
        elif body.kind == 'CALIBRATION':
            payload = Calibration.model_validate(payload).model_dump()
            inference_admission(jobs.member('releases', payload['release_id']))
        else:
            payload = QualificationRun.model_validate(payload).model_dump()
            plan = qualification.verify_plan(payload['id'])
            inference_admission(jobs.member('releases', plan['release_id']))
        return worker.submit(ident, body.kind, payload, user['name'])
    @app.post('/api/client/tasks/{ident}/cancel')
    def cancel_task(ident: str, user=Depends(train)): return worker.cancel(ident, user['name'])

    @app.post('/api/client/qualifications/{ident}', status_code=201)
    def prepare_qualification(ident: str, body: QualificationBody, user=Depends(train)):
        result = qualification.prepare(ident, **body.model_dump(), actor=user['name'])
        storage.audit(user['name'], 'QUALIFICATION_PLAN_FROZEN', {'id': ident}); return result
    @app.post('/api/client/promotions/{ident}')
    def promote(ident: str, body: PromotionBody, user=Depends(admin)): return service.promote(ident, user['name'], body.expected_previous_id)

    @app.get('/api/client/decisions')
    def decisions(user=Depends(read)):
        with store.connect() as c: return [json.loads(r[0]) for r in c.execute('SELECT payload FROM client_decisions ORDER BY created_at DESC LIMIT 100')]
    @app.get('/api/client/review-queue')
    def review_queue(user=Depends(require('REVIEWER', 'ADMIN'))):
        with store.connect() as c:
            rows = c.execute('''SELECT d.payload,e.corp,e.sender FROM client_decisions d JOIN learning_events e ON e.id=d.event_id
            WHERE d.rowid=(SELECT max(n.rowid) FROM client_decisions n WHERE n.event_id=d.event_id)
            AND json_extract(d.payload,'$.decision.review_required')=1
            AND NOT EXISTS(SELECT 1 FROM learning_reviews r JOIN client_review_identity i ON i.review_id=r.id
              WHERE r.event_id=d.event_id AND r.created_at>d.created_at AND i.source_kind='HUMAN')''').fetchall()
        values = [{**json.loads(r['payload']), 'corp': r['corp'], 'sender': r['sender']} for r in rows]
        values.sort(key=lambda r: r['decision']['confidence'] if r['decision']['confidence'] is not None else -1)
        return {'total': len(values), 'items': values[:100], 'ordering': 'Unresolved first, then ascending calibrated confidence'}
    @app.get('/api/client/qualifications')
    def qualifications(user=Depends(read)):
        with store.connect() as c: return [json.loads(r[0]) for r in c.execute('SELECT payload FROM client_qualifications ORDER BY created_at DESC LIMIT 100')]
    @app.get('/api/client/audit')
    def audit(user=Depends(require('ADMIN', 'AUDITOR'))):
        with store.connect() as c: return {'integrity': storage.verify_audit(), 'entries': [dict(r) for r in c.execute('SELECT * FROM client_audit ORDER BY id DESC LIMIT 200')]}
    return app


from typing import Literal
LiteralDeadline = Literal['OPEN', 'PASSED', 'UNKNOWN']
class StrictBody(BaseModel):
    model_config = ConfigDict(extra='forbid')
class TaskBody(StrictBody):
    kind: Literal['INFERENCE', 'CALIBRATION', 'QUALIFICATION']
    payload: dict
class Inference(StrictBody):
    release_id: str
    event_ids: list[str] = Field(min_length=1, max_length=1000)
    qualification_id: str | None = None
    calibrator_id: str | None = None
    simulation_threshold: float = Field(default=.99, ge=.5, le=1)
    review_only_unsealed: bool = False

    @model_validator(mode='after')
    def bootstrap_is_review_only(self):
        if self.review_only_unsealed and (self.qualification_id or self.calibrator_id):
            raise ValueError('Unsealed bootstrap cannot attach qualification/calibration')
        return self
class Calibration(StrictBody):
    ident: str
    dataset_id: str
    release_id: str
    population: str
    reference: str
    stage: Literal['FINAL','LAYA'] = 'FINAL'
class QualificationRun(StrictBody):
    id: str
class QualificationBody(StrictBody):
    release_id: str
    dataset_id: str
    calibrator_path: str
    population: str
    reference: str
    policy: qualification.Policy
class PromotionBody(StrictBody):
    expected_previous_id: int | None = None

class OperatingPointBody(StrictBody):
    campaign_id: str
    candidate: str
    dataset_id: str
    calibrator_id: str
    population: str
    stage: Literal['FINAL','LAYA']='FINAL'

app = create_app()
