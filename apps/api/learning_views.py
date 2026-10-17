"""Engineering learning loop. Local execution remains an explicit opt-in."""
import os
import json
import uuid
from typing import Literal

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field, ConfigDict
from training.framework import events, event_data, queue, selection, jobs, releases, campaigns
from apps.api.training_views import member

router = APIRouter(prefix='/api/learning')


@router.get('/readiness')
def readiness():
    from training.framework.operations import readiness
    return readiness()


def enabled():
    if os.environ.get('TRAINING_EXECUTION_ENABLED', 'false').lower() != 'true':
        raise HTTPException(403, 'Experimental training/execution is disabled; set TRAINING_EXECUTION_ENABLED=true explicitly')


def fail(exc):
    return HTTPException(409 if any(s in str(exc).lower() for s in ('conflict', 'changed', 'resource', 'benchmark', 'stale')) else 422, str(exc))


@router.get('/status')
def overview():
    return {'events': events.listing(), 'tasks': queue.listing(), 'selections': selection.history(),
            'release_history': releases.history(), 'campaigns': campaigns.listing(),
            'execution_enabled': os.environ.get('TRAINING_EXECUTION_ENABLED', 'false').lower() == 'true',
            'automation_enabled': False, 'customer_accuracy': None,
            'datasets': [p.parent.name for p in sorted((jobs.WORKSPACE / 'event-datasets').glob('*/manifest.json'))],
            'comparisons': [p.parent.name for p in sorted((jobs.WORKSPACE / 'comparisons').glob('*/comparison.json'))]}


class DeclaredIdentity(BaseModel):
    model_config = ConfigDict(extra='forbid')
    corp: str = Field(min_length=1, max_length=120)
    seme: str = Field(min_length=1, max_length=120)
    prev: str | None = Field(default=None, max_length=120)
    function: Literal['NEWM', 'REPL', 'CANC'] | None = None


class ImportMessage(BaseModel):
    model_config = ConfigDict(extra='forbid')
    raw: str = Field(min_length=1, max_length=2_000_000)
    sender: str = Field(min_length=1, max_length=120)
    source_type: Literal['STANDARDS_DERIVED_SYNTHETIC', 'PUBLIC_EXAMPLE', 'USER_PROVIDED']
    group_id: str = Field(min_length=1)
    family: str = Field(min_length=1)
    split: Literal['TRAIN', 'VALIDATION', 'CALIBRATION', 'FROZEN_TEST']
    source_reference: str = Field(min_length=1)
    declared: DeclaredIdentity | None = None


@router.post('/messages', status_code=201)
def ingest(body: ImportMessage):
    try: return events.ingest(**body.model_dump())
    except ValueError as exc: raise fail(exc)


@router.get('/events/{ident}')
def detail(ident: str):
    try:
        value = events.get(ident)
        if value['split'] in event_data.PROTECTED:
            value['reviews'] = []; value['executions'] = []; value['held_out_labels_hidden'] = True
        return value
    except ValueError as exc: raise HTTPException(404, str(exc))


@router.post('/events/{ident}/reviews', status_code=201)
def review(ident: str, body: events.Review):
    try:
        if events.get(ident)['split'] in event_data.PROTECTED: raise ValueError('Protected labels cannot be edited in development')
        return events.review(ident, body)
    except ValueError as exc: raise fail(exc)


class Version(BaseModel):
    id: str


@router.post('/exports', status_code=201)
def export(body: Version):
    try: return event_data.export_reviews(member('bundles', body.id))
    except (ValueError, FileExistsError) as exc: raise fail(exc)


@router.post('/datasets', status_code=201)
def freeze(body: Version):
    try: return event_data.freeze_dataset(member('event-datasets', body.id))
    except (ValueError, FileExistsError) as exc: raise fail(exc)


@router.post('/jobs/{ident}/enqueue', status_code=201)
def enqueue(ident: str):
    enabled()
    try: return queue.submit(ident)
    except (ValueError, FileNotFoundError) as exc: raise fail(exc)


@router.post('/dispatch', status_code=202)
def dispatch():
    enabled()
    try: return queue.spawn()
    except ValueError as exc: raise fail(exc)


@router.post('/tasks/{ident}/cancel')
def cancel(ident: str):
    try: return queue.cancel(ident)
    except ValueError as exc: raise fail(exc)


@router.post('/jobs/{ident}/restart', status_code=201)
def restart(ident: str):
    enabled()
    try:
        old = member('jobs', ident)
        _, p = jobs.verify_plan(old, check_sources=False)
        if jobs.status(old)['state'] not in ('FAILED', 'INTERRUPTED') and not any(t['job_id'] == ident and t['state'] in ('CANCELLED', 'INTERRUPTED') for t in queue.listing()):
            raise ValueError('Only an interrupted/failed/cancelled attempt can be restarted')
        new = str(uuid.uuid4()); path = member('jobs', new)
        plan = jobs.prepare(p['bundle'], p['spec'], path)
        jobs.events(path, {'state': 'PREPARED' if plan['preflight']['ready'] else 'BLOCKED',
                           'kind': 'EXPLICIT_NEW_ATTEMPT', 'previous_job': ident, 'optimizer_resume': False})
        return {'id': new, 'plan': plan, 'optimizer_resume': False, 'execution_started': False}
    except (ValueError, FileNotFoundError) as exc: raise fail(exc)


class Choose(BaseModel):
    job_id: str
    actor: str = Field(min_length=1)
    reason: str = Field(min_length=1)
    expected_previous_id: int | None = None
    rollback_id: int | None = None


@router.post('/selections', status_code=201)
def choose(body: Choose):
    try: return selection.choose(**body.model_dump())
    except (ValueError, FileNotFoundError) as exc: raise fail(exc)


class Analyse(BaseModel):
    job_id: str | None = None
    release_id: str | None = None
    reference: str = '2026-10-17T12:00:00+00:00'


@router.post('/events/{ident}/analyse', status_code=201)
def analyse(ident: str, body: Analyse):
    enabled()
    try:
        value = events.get(ident)
        if value['split'] in event_data.PROTECTED: raise ValueError('Use the protected comparison runner for held-out inputs')
        chosen = selection.history()
        release_history = releases.history()
        if body.job_id and body.release_id: raise ValueError('Choose checkpoint OR complete release')
        release_id = body.release_id or (release_history[-1]['release_id'] if release_history and not body.job_id else None)
        if release_id:
            from training.framework.resources import model_resource
            with model_resource('event-release-classification'):
                path = member('releases', release_id)
                model = releases.ReleaseModel(path)
                try: return events.classify(ident, path, reference=body.reference, model=model)
                finally: model.close()
        job_id = body.job_id or (chosen[-1]['job_id'] if chosen else None)
        if not job_id: raise ValueError('Select an experimental candidate or specify job_id')
        from training.framework.resources import model_resource
        with model_resource('event-classification'):
            return events.classify(ident, member('jobs', job_id), reference=body.reference)
    except (ValueError, RuntimeError, OSError) as exc: raise fail(exc)


class Comparison(BaseModel):
    dataset_id: str
    candidates: dict[str, str]
    role: Literal['VALIDATION', 'CALIBRATION', 'FROZEN_TEST'] = 'VALIDATION'
    selection_id: int | None = None


@router.post('/comparisons', status_code=201)
def compare(body: Comparison):
    enabled()
    try:
        from training.framework.comparison import compare
        from training.framework.resources import model_resource
        ident = str(uuid.uuid4())
        with model_resource('event-comparison'):
            result = compare(member('event-datasets', body.dataset_id), {k: member('jobs', v) for k, v in body.candidates.items()},
                             member('comparisons', ident), role=body.role, selection_id=body.selection_id)
        return {'id': ident, 'report': result}
    except (ValueError, RuntimeError, OSError) as exc: raise fail(exc)


@router.get('/comparisons/{ident}')
def comparison(ident: str):
    try: return json.loads((member('comparisons', ident) / 'comparison.json').read_text())
    except (ValueError, FileNotFoundError) as exc: raise HTTPException(404, str(exc))


class CampaignRequest(BaseModel):
    id: str
    spec: campaigns.CampaignSpec


@router.post('/campaigns', status_code=201)
def prepare_campaign(body: CampaignRequest):
    try: return campaigns.prepare(body.spec.model_dump(), member('campaigns', body.id))
    except (ValueError, FileExistsError, FileNotFoundError) as exc: raise fail(exc)


@router.get('/campaigns/{ident}')
def campaign_status(ident: str):
    try: return campaigns.status(member('campaigns', ident))
    except (ValueError, FileNotFoundError) as exc: raise fail(exc)


@router.post('/campaigns/{ident}/dispatch', status_code=202)
def dispatch_campaign(ident: str):
    enabled()
    try: return campaigns.spawn(member('campaigns', ident))
    except (ValueError, FileNotFoundError) as exc: raise fail(exc)


@router.post('/campaigns/{ident}/cancel')
def cancel_campaign(ident: str):
    try: return campaigns.cancel(member('campaigns', ident))
    except (ValueError, FileNotFoundError) as exc: raise fail(exc)


class SelectRelease(BaseModel):
    release_id: str
    actor: str = Field(min_length=1)
    reason: str = Field(min_length=1)
    expected_previous_id: int | None = None
    rollback_id: int | None = None


@router.post('/releases/select', status_code=201)
def select_release(body: SelectRelease):
    try: return releases.select(**body.model_dump())
    except (ValueError, FileNotFoundError) as exc: raise fail(exc)


@router.get('/releases/{ident}')
def release_detail(ident: str):
    try:
        root = member('releases', ident)
        return {'manifest': json.loads((root / 'release.json').read_text()),
                'seal': json.loads((root / 'SEALED.json').read_text()) if (root / 'SEALED.json').exists() else None}
    except (ValueError, FileNotFoundError) as exc: raise fail(exc)
