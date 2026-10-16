import copy
import json
import pytest
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
