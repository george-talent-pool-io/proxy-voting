"""Customer continuation uses completed registered lineage, not loose paths."""
import json
from pathlib import Path
import pytest
from production.installation import training_base_admission
from production.storage import digest
from training.framework import jobs, seeds, trainers
from training.framework.schema import TrainSpec
from training.framework.bundle import create_bundle
from tests.unit.test_training_framework import example
from tests.production.test_client_workflow import client_app, auth


@pytest.fixture
def completed_job(client_app,tmp_path,monkeypatch):
    model=tmp_path/'models/base';model.mkdir(parents=True)
    (model/'model.safetensors').write_bytes(b'EXPLICIT_FOUNDATION_DOUBLE')
    (model/'rl_agent_config.json').write_text('{}')
    bundle=jobs.member('bundles','continuation-contract')
    create_bundle([example(),example('validation','VALIDATION')],bundle)
    spec=TrainSpec(backend='LAYA_SDK',family='LAYA',model_path=str(model),
                   base_model_id='EXPLICIT_SOFTWARE_DOUBLE',base_revision='FIXTURE_V1',max_length=512)
    def kernel(bundle,output,spec):
        output.mkdir();(output/'model.safetensors').write_bytes(b'EXPLICIT_TRAINING_DOUBLE')
        (output/'rl_agent_config.json').write_text('{}')
        return {'backend':'EXPLICIT_SOFTWARE_DOUBLE','weights_updated':False,'reload_parity':{'passed':True}}
    monkeypatch.setattr(trainers,'train_laya',kernel)
    job=jobs.member('jobs','completed');jobs.prepare(bundle,spec,job);jobs.execute(job)
    return client_app,job,model.parent


def test_api_freezes_actual_registered_ai_lineage_without_origin_spoofing(completed_job):
    client,job,models=completed_job
    endpoint='/api/client/starting-checkpoints/from-job'
    payload={'id':'next-start','job_id':job.name}
    assert client.post(endpoint,json=payload,auth=auth('auditor')).status_code==403
    assert client.post(endpoint,json={**payload,'origin':'OFFICIAL_FOUNDATION'},auth=auth()).status_code==422
    response=client.post(endpoint,json=payload,auth=auth('trainer'))
    assert response.status_code==201,response.text
    seed=response.json();assert seed['origin']=='AI_TEST_DERIVATIVE'
    assert seed['lineage']['job_manifest_sha256'] and seed['contains_corpus'] is False
    assert client.post(endpoint,json=payload,auth=auth()).status_code==409
    spec=seeds.training_spec(jobs.member('seeds','next-start'))
    admission=training_base_admission(spec,models)
    assert admission['source']=='REGISTERED_FROZEN_DERIVATIVE'
    assert admission['parent_identity']==seed['identity']


@pytest.mark.parametrize('damage',['unregistered-path','false-lineage','changed-weights'])
def test_continuation_admission_rejects_unregistered_forged_and_corrupt_parents(completed_job,damage):
    client,job,models=completed_job
    root=jobs.member('seeds','next-start');seeds.export_derivative(job,root,origin='AI_TEST_DERIVATIVE')
    spec=seeds.training_spec(root)
    if damage=='unregistered-path':
        spec=spec.model_copy(update={'model_path':str(jobs.WORKSPACE/'loose/checkpoint')})
    elif damage=='changed-weights':
        (job/'checkpoint/model.safetensors').write_bytes(b'CORRUPTED')
    else:
        value=json.loads((root/'seed.json').read_text())
        value['lineage']['job_manifest_sha256']='forged'
        value['identity']=digest({k:v for k,v in value.items() if k not in ('identity','model_location','adapter_location')})
        (root/'seed.json').write_text(json.dumps(value))
    with pytest.raises(ValueError):training_base_admission(spec,models)
