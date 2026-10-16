import copy,json
import pytest
from semantic_runtime.config import configured_architecture,ARCHITECTURES
from semantic_runtime.fallback import BoundedRepairFallback,configured_fallback
from semantic_pipeline.fallback import OllamaFallback,DisabledFallback
from tests.unit.test_semantic_pipeline import llm,TEXT
from evaluation.ae_extended_analysis import disagreement
from evaluation.ae_validation_strategies import select

@pytest.mark.parametrize('name,arm',list(ARCHITECTURES.items()))
def test_configured_architecture(monkeypatch,name,arm):
    monkeypatch.setenv('CLASSIFICATION_ARCHITECTURE',name);assert configured_architecture()==(name,arm)

def test_default_and_invalid_config(monkeypatch):
    monkeypatch.delenv('CLASSIFICATION_ARCHITECTURE',raising=False);assert configured_architecture()==('LEGACY_LAYA','A')
    monkeypatch.setenv('CLASSIFICATION_ARCHITECTURE','BAD')
    with pytest.raises(ValueError):configured_architecture()

def test_disabled_llm_is_default(monkeypatch):
    monkeypatch.delenv('LLM_ENABLED',raising=False);assert isinstance(configured_fallback(),DisabledFallback)

@pytest.mark.parametrize('repair_valid',[True,False])
def test_bounded_schema_repair_preserves_original(monkeypatch,repair_valid):
    first={'valid':False,'raw_response':{'done':True,'done_reason':'stop','message':{'role':'assistant','content':'bad-json'}},
        'request':{'messages':[{'role':'user','content':TEXT}]},'prompt_version':'initial-v1','latency_ms':1,'parsed':None}
    monkeypatch.setattr(OllamaFallback,'analyse',lambda self,**kw:copy.deepcopy(first))
    obj=object.__new__(BoundedRepairFallback);obj.config={'num_ctx':16384,'num_predict':2048}
    monkeypatch.setattr(obj,'check_identity',lambda:None);calls=[]
    def http(path,req):
        calls.append(req)
        return {'done':True,'done_reason':'stop','message':{'content':json.dumps(llm()['parsed']) if repair_valid else '{broken'}}
    monkeypatch.setattr(obj,'http',http)
    result=obj.analyse(original_text=TEXT,narrative_text=TEXT,structured_facts={})
    assert len(calls)==1;assert result['valid']==repair_valid
    assert result['schema_handling']['repair_attempts']==1
    assert result['schema_handling']['final_failure']==(not repair_valid)
    assert result['first_attempt']['raw_response']['message']['content']=='bad-json'
    assert result['prompt_version']!='initial-v1'
    assert calls[0]['messages'][0]['content']==TEXT

@pytest.mark.parametrize('raw',[None,{'done_reason':'length','message':{'content':'{unfinished'}}])
def test_no_retry_of_runtime_failure_or_truncation(monkeypatch,raw):
    monkeypatch.setattr(OllamaFallback,'analyse',lambda self,**kw:{'valid':False,'raw_response':raw})
    obj=object.__new__(BoundedRepairFallback)
    result=obj.analyse(original_text=TEXT);assert result['schema_handling']['repair_attempts']==0

def test_successful_first_pass_no_retry(monkeypatch):
    monkeypatch.setattr(OllamaFallback,'analyse',lambda self,**kw:{'valid':True})
    obj=object.__new__(BoundedRepairFallback);r=obj.analyse(original_text=TEXT)
    assert r['schema_handling']['first_pass_success'];assert not r['schema_handling']['final_failure']

@pytest.mark.parametrize('a,b,g,category',[
    ('YES','YES','YES','agree_correct'),('NO','NO','YES','agree_wrong'),
    ('YES','NO','YES','disagree_laya_correct'),('NO','YES','YES','disagree_llm_correct'),
    ('UNKNOWN','UNKNOWN','YES','both_effectively_uncertain')])
def test_disagreement_bins(a,b,g,category):assert disagreement(a,b,g)[category]==1

@pytest.mark.parametrize('strategy,t,expected',[
    ('UNKNOWN',None,False),('SCORE',.8,True),('SCORE',.5,False),('MARGIN',.2,True),
    ('UNKNOWN_OR_MARGIN_OR_EVIDENCE',.2,True),('CRITICAL_POSITIVE_OR_UNKNOWN',None,True)])
def test_validation_strategy_conditions(strategy,t,expected):
    from semantic_pipeline.schema import PREDICATES
    p={k:{'value':'VOTABLE' if k=='votability' else 'NO','confidence':.7,'margin':.1,'evidence':[]} for k in PREDICATES}
    assert select(p,strategy,t)==expected


def test_immutable_execution_publication(tmp_path):
    from semantic_runtime.persistence import persist
    row={'run_id':'d74edb8d-fccb-4a29-95d1-c8748dcff617','text':'Unicode € 😀'}
    path=persist(tmp_path,row);assert json.loads(path.read_text())==row
    with pytest.raises(FileExistsError):persist(tmp_path,{**row,'text':'replacement'})
    assert json.loads(path.read_text())==row;assert not list(tmp_path.glob('*.pending'))


def test_invalid_execution_never_published(tmp_path):
    from semantic_runtime.persistence import persist
    with pytest.raises(ValueError):persist(tmp_path,{'run_id':'d74edb8d-fccb-4a29-95d1-c8748dcff617','invalid_score':float('nan')})
    assert not list(tmp_path.iterdir())
