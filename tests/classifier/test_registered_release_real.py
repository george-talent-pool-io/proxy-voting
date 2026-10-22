"""Opt-in REAL registered Laya/Qwen release inference, never a model double.

RUN_RELEASE_REAL_MODEL=1 uv run pytest tests/classifier/test_registered_release_real.py -q
Requires a completed registered-release campaign (default release-learning-v3);
never trains implicitly.
"""
import os
import pytest

pytestmark = [pytest.mark.model, pytest.mark.local_llm,
              pytest.mark.skipif(os.environ.get('RUN_RELEASE_REAL_MODEL') != '1', reason='Explicit real release execution required')]


@pytest.fixture(scope='module')
def actual_release(tmp_path_factory):
    from training.framework import jobs, campaigns, releases
    from training.framework.event_data import load_inputs
    state = campaigns.status(jobs.member('campaigns', os.environ.get('RELEASE_CAMPAIGN', 'release-learning-v3')))
    assert state['state'] == 'COMPLETED'
    root = jobs.member('releases', state['report']['candidates']['CASCADE_CONSERVATIVE'])
    _, inputs = load_inputs(jobs.member('event-datasets', state['plan']['spec']['dataset_id']), 'VALIDATION')
    row = inputs[0]
    # Execute the actual durable customer worker, not just a model method.
    # Clone the database so opt-in tests cannot add decisions to a live workspace.
    import sqlite3
    from apps.api import store
    from production import storage, worker
    database=tmp_path_factory.mktemp('real-release-worker')/'state.sqlite'
    with store.connect() as source,sqlite3.connect(database) as target:source.backup(target)
    with pytest.MonkeyPatch.context() as patch:
        patch.setattr(store,'DB_PATH',str(database))
        patch.setenv('TRAINING_EXECUTION_ENABLED','true');patch.setenv('AUTOMATION_ENABLED','false')
        patch.setattr(worker,'STOP',False)
        storage.initialise();worker.initialise()
        assert not any(t['state']=='QUEUED' for t in worker.listing()), 'Integration snapshot must not contain pending customer work'
        task_id='real-release-'+__import__('uuid').uuid4().hex
        worker.submit(task_id,'INFERENCE',{'release_id':root.name,'event_ids':[row['id']]},'REAL_MODEL_INTEGRATION_TEST')
        assert worker.run_once()
        task=next(t for t in worker.listing() if t['id']==task_id)
        assert task['state']=='COMPLETED',task
        from training.framework import events
        execution=events.get(row['id'])['executions'][-1]
        with store.connect() as c:
            saved=__import__('json').loads(c.execute('SELECT payload FROM client_decisions WHERE execution_id=?',
                                                    (execution['id'],)).fetchone()[0])
        yield row['text'], execution['payload']['result'], saved, task, storage.verify_audit()


def test_real_registered_specialist_and_local_generative_model_execute(actual_release):
    _, r, *_ = actual_release
    assert r['laya']['passage_predictions'] and r['llm_stage']['llm']['invoked']
    from semantic_pipeline.schema import SemanticResult
    assert r['llm_stage']['llm']['valid'], 'A real invocation must also return validated structured semantics'
    SemanticResult.model_validate(r['llm_stage']['llm']['parsed'])
    assert r['release_identity'] and r['checkpoint_manifest_sha256']
    assert r['decision']['manual_review_required'] and not r['automation_enabled']


def test_real_release_has_native_scores_exact_evidence_and_honest_confidence(actual_release):
    text, r, *_ = actual_release
    for key, passages in r['laya']['passage_predictions'].items():
        for p in passages:
            assert abs(sum(p['scores'].values()) - 1) < .002
        for e in r['predicates'][key].get('evidence', []):
            if e.get('valid') and not str(r['predicates'][key].get('source')).startswith('PROWIDE'):
                assert e['text'] in text
    assert all(c['confidence'] is None for c in r['confidence'].values())  # tiny real cohort correctly refuses calibration


def test_real_customer_worker_persists_decision_review_confidence_and_audit(actual_release):
    _,result,saved,task,audit=actual_release
    assert task['state']=='COMPLETED' and task['progress']==1
    assert saved['decision']['classification']==result['decision']['classification']
    assert saved['decision']['review_required'] and not saved['decision']['automation_enabled']
    assert saved['decision']['confidence'] is None
    assert saved['execution_id'] and audit['valid']
