import copy
import json
import subprocess
import sys
import pytest
from apps.api import store
from production import storage, service, worker, resources
from tests.production.test_client_workflow import row, body
from tests.unit.test_learning_comparison import result
from training.framework import jobs, releases


def test_real_worker_persists_trace_and_uncalibrated_review(db,monkeypatch):
    storage.initialise();worker.initialise();monkeypatch.setenv('TRAINING_EXECUTION_ENABLED','true')
    text='Shareholders may vote. Shares will be blocked. Voting deadline 20 October 2026.'
    imported=service.import_rows('worker-source',[row(text=text)],'AI_operator');eid=imported['rows'][0]['event_id']
    class ExplicitDouble:
        def __init__(self,*a,**kw):pass
        def analyse(self,text,**kw):return result()
        def close(self):pass
    monkeypatch.setattr(releases,'ReleaseModel',ExplicitDouble)
    worker.submit('batch','INFERENCE',{'release_id':'EXPLICIT_TEST_DOUBLE','event_ids':[eid]},'AI_operator')
    assert worker.run_once() and worker.listing()[0]['state']=='COMPLETED'
    with store.connect() as c:
        saved=json.loads(c.execute('SELECT payload FROM client_decisions').fetchone()[0])
        assert c.execute('SELECT count(*) FROM learning_executions').fetchone()[0]==1
    assert saved['decision']['review_required'] and saved['decision']['confidence'] is None
    assert not saved['decision']['automation_enabled']
    assert all(p['confidence'] is None for p in saved['decision']['predicate_confidence'].values())
    # Controlled post-release-error fixture. No qualification is manufactured.
    saved['id']='SIMULATED_AUTO_RESULT';saved['decision'].update(review_required=False,qualification_id='SOFTWARE_TEST_ONLY')
    with store.connect() as c:c.execute('INSERT INTO client_decisions VALUES(?,?,?,?,?)',(saved['id'],store.now(),eid,saved['execution_id'],store.dumps(saved)))
    view=service.source_view(eid);label=body(view);label['target']['share_blocking']='YES';label['expected_final_status']='VOTABLE_WITH_RESTRICTION'
    service.review(eid,label,{'name':'authenticated_expert_fixture','expert_attested':True})
    with store.connect() as c:
        suspension=json.loads(c.execute('SELECT payload FROM client_suspensions').fetchone()[0])
    assert 'share_blocking' in suspension['fields']


def test_managed_lease_recovery_never_reclaims_unknown_owner(db):
    storage.initialise();jobs.WORKSPACE.mkdir(exist_ok=True)
    lease=jobs.WORKSPACE/'model-training.lock'
    lease.write_text(json.dumps({'purpose':'UNKNOWN_OWNER'}))
    with pytest.raises(ValueError,match='Unrecognised'):
        with resources.device('new'):pass
    assert lease.exists();lease.unlink()
    with resources.device('old-task'):
        lease.write_text(json.dumps({'purpose':'old-task'}))
    with resources.device('new-task'): assert not lease.exists()
    assert 'STALE_MANAGED' in (jobs.WORKSPACE/'events.jsonl').read_text()


def test_training_child_retains_device_lock_if_parent_scope_exits(db):
    with resources.device('parent'):
        fd=resources.inherited_fd()
        child=subprocess.Popen([sys.executable,'-c','import time; time.sleep(.3)'],pass_fds=(fd,))
    try:
        with pytest.raises(ValueError,match='busy'):
            with resources.device('other'):pass
    finally:child.wait(timeout=3)
    with resources.device('after-child'):pass


def test_population_mismatch_routes_to_review_not_an_exception():
    from production.qualification import assess
    cal={'identity':'model','population':'population-A','models':{}}
    meta={'language':'en','input_type':'UNSTRUCTURED_NOTICE','population':'population-B'}
    r=assess('Notice',result(),meta,cal,'model',.99)
    assert not r['eligible'] and r['final_decision_confidence'] is None
    assert 'POPULATION_NOT_IN_CALIBRATION_SCOPE' in r['review_reasons']


def test_training_admission_rejects_underpowered_container(tmp_path,monkeypatch):
    from production import installation
    from training.framework.schema import TrainSpec
    monkeypatch.setattr(installation,'memory_limit',lambda:3*1024**3)
    spec=TrainSpec(backend='LAYA_SDK',family='LAYA',model_path=str(tmp_path),base_model_id='CONTROLLED_FIXTURE',
                   base_revision='TEST',max_length=512)
    with pytest.raises(ValueError,match='memory admission'):installation.training_admission(spec)


def test_serving_admission_requires_linux_artifact_and_capacity(db,tmp_path,monkeypatch):
    from production import installation
    job=jobs.member('jobs','capacity-fixture');job.mkdir(parents=True);(job/'checkpoint').mkdir()
    spec={'backend':'LAYA_SDK','device':'cpu','model_path':str(tmp_path)}
    (job/'plan.json').write_text(json.dumps({'spec':spec}))
    release=tmp_path/'release';release.mkdir();(release/'release.json').write_text(json.dumps({'models':{'laya':{'job_id':job.name}}}))
    monkeypatch.setattr(installation,'memory_limit',lambda:3*1024**3)
    with pytest.raises(ValueError,match='serving memory'):installation.inference_admission(release)
    monkeypatch.setattr(installation,'memory_limit',lambda:64*1024**3)
    assert installation.inference_admission(release)['minimum_bytes']==8*1024**3
    spec['backend']='MLX_QLORA';(job/'plan.json').write_text(json.dumps({'spec':spec}))
    with pytest.raises(ValueError,match='not a Linux'):installation.inference_admission(release)


def test_worker_liveness_is_measured_and_stale_state_is_not_ready(db,monkeypatch):
    storage.initialise();worker.initialise()
    assert not worker.health()['healthy']
    monkeypatch.setattr(worker.time,'time',lambda:1000)
    worker.heartbeat();assert worker.health()['healthy']
    monkeypatch.setattr(worker.time,'time',lambda:1031)
    assert not worker.health()['healthy']
    worker.heartbeat('STOPPED');assert not worker.health()['healthy']
