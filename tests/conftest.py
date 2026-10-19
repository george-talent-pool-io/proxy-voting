import copy
import json
import pytest
from pathlib import Path
from apps.api import store
from classifier.laya_classifier import load_config,LayaClassifier
from classifier.preprocessing import source_hash
from training.split import partition

class ContractAgent:
    """Deterministic SDK contract double. Never used by the app or for model quality claims."""
    def predict_batch(self,states,questions,**kwargs):
        out=[]
        for state in states:
            selected={'votable':'YES','share_blocking':'NO','poa_required':'NO','other_restriction':'NO','deadline_status':'OPEN'}
            answers={}
            for k,q in questions.items():
                win=selected[k];scores={v:.005 for v in q['criteria']};scores[win]=.99
                answers[k]={'choice':win,'probabilities':scores,'answer_confidence':.99,'confidence':.94,'type':'choice'}
            out.append({'answers':answers,'usage':{'truncated':False,'state_tokens_dropped':0}})
        return out

@pytest.fixture
def config():return load_config()
@pytest.fixture
def classifier(config):return LayaClassifier(config,agent=ContractAgent())
@pytest.fixture
def db(tmp_path,monkeypatch):
    # Contract API tests must never acquire the real application's model lease.
    from training.framework import jobs
    from apps.api import training_views
    monkeypatch.setattr(jobs,'WORKSPACE',tmp_path/'framework')
    monkeypatch.setattr(training_views,'WORKSPACE',tmp_path/'framework')
    monkeypatch.setattr(jobs,'active_experiments',lambda:[])
    path=str(tmp_path/'test.sqlite');monkeypatch.setattr(store,'DB_PATH',path);store.initialise()
    rows=[]
    # Find distinct deterministic groups in each partition.
    for split in ['train','validation','test']:
        g=next(f'group-{i}' for i in range(10000) if partition(f'group-{i}')==split)
        text=f'{split} Shareholders may vote at the Annual General Meeting. Deadline 20 October 2026.'
        rows.append(dict(id=split,text=text,source_hash=source_hash(text),group_id=g,split=split,issuer=f'{split} Issuer',source_file=split,
            country='UNKNOWN',market='UNKNOWN',language='en',event_type='Proxy excerpt',source_url='https://example.org/source',source_row=1))
    file=tmp_path/'normalised.jsonl';file.write_text(''.join(json.dumps(r)+'\n' for r in rows));store.import_normalised(file)
    return path

@pytest.fixture
def client(db):
    from fastapi.testclient import TestClient
    from apps.api.main import app
    with TestClient(app) as client:yield client

def pytest_configure(config):
    config.addinivalue_line('markers','local_llm: opt-in integration tests executing the pinned real local generative model')
    config.addinivalue_line('markers','qwen_local: opt-in real Qwen3.8 Direct/xhigh integration inference')
    config.addinivalue_line('markers','requires_artifact(path): verifies optional archived research evidence, excluded from source delivery')


def pytest_collection_modifyitems(items):
    for item in items:
        for mark in item.iter_markers('requires_artifact'):
            if not Path(mark.args[0]).exists():
                item.add_marker(pytest.mark.skip(reason='Optional historical research evidence excluded from source delivery: '+mark.args[0]))


@pytest.fixture(scope='session',autouse=True)
def portable_test_configuration():
    # Public model settings are not a corpus or inference results. Contract
    # tests use explicit model doubles; installed models are never fabricated.
    Path('artifacts').mkdir(exist_ok=True)
    path=Path('data/experiments/cascade-v2/LLM-CONFIGS-v3.json')
    created=not path.exists()
    if created:
        path.parent.mkdir(parents=True,exist_ok=True)
        path.write_bytes(Path('tests/fixtures/research_llm_config.json').read_bytes())
    yield
    if created:path.unlink()
