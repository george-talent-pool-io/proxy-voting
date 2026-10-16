import json
import pytest
from semantic_pipeline.schema import PREDICATES
from semantic_pipeline.models import factor
from cascade.routing import Policy,gate,features
from cascade.pipeline import execute
from tests.unit.test_semantic_pipeline import llm,TEXT,parsed

def specialist():
    preds={k:factor('VOTABLE' if k=='votability' else 'NO','TEST',({'YES':.99,'NO':.01} if k=='votability' else {'YES':.01,'NO':.99}),evidence=[]) for k in PREDICATES}
    preds['votability']['evidence']=[{'valid':True,'text':'Owners may vote.','start':0,'end':16}]
    return {'predicates':preds,'checkpoint':'TEST_DOUBLE','model_version':'test','latency_ms':1,'truncated':False}

def test_easy_supported_notice_does_not_escalate():
    r=gate(TEXT,specialist(),{},Policy());assert not r['escalated']

@pytest.mark.parametrize('field',PREDICATES)
def test_unknown_always_escalates_in_moderate(field):
    s=specialist();s['predicates'][field]['value']='UNCERTAIN' if field=='votability' else 'UNKNOWN'
    assert gate(TEXT,s,{},Policy())['escalated']

@pytest.mark.parametrize('signal',['score','margin','conflict','evidence','unsupported','structured'])
def test_auditable_gate_signals(signal):
    s=specialist();st={}
    if signal=='score':s['predicates']['share_blocking']['confidence']=.1
    elif signal=='margin':s['predicates']['share_blocking']['margin']=.01
    elif signal=='conflict':s['predicates']['share_blocking']['conflict']=True
    elif signal=='evidence':s['predicates']['share_blocking']['value']='YES'
    elif signal=='unsupported':s['predicates']['share_blocking']['value']='NOT_SUPPORTED'
    else:st={'votability':{'value':'NOT_VOTABLE'}}
    assert gate(TEXT,s,st,Policy())['escalated']

def test_no_iso_structure_is_not_a_review_conflict():
    r=execute(TEXT,precomputed=specialist(),use_parser=True,policy=Policy())
    assert r['parser_status']=='NOT_APPLICABLE';assert r['parser'] is None
    assert not r['escalation']['escalated'];assert not r['reconciliation']['conflicts']
    assert r['decision']['manual_review_required'];assert not r['automation_enabled']


def test_actual_fallback_called_on_unknown_and_stages_remain():
    s=specialist();s['predicates']['share_blocking']['value']='UNKNOWN'
    class Fallback:
        def analyse(self,**kw):
            assert kw['mode']=='FALLBACK';assert kw['laya_result']
            return llm()
    r=execute(TEXT,precomputed=s,fallback=Fallback())
    assert r['llm']['invoked'];assert r['laya']['predicates']['share_blocking']['value']=='UNKNOWN'
    assert r['reconciliation']['predicates']['share_blocking']['value']=='NO'


def test_reasoning_stream_never_leaks_to_result():
    from cascade.fallback import CommonFallback
    class Response:
        def __enter__(self):return self
        def __exit__(self,*a):pass
        def __iter__(self):
            for x in [{'message':{'thinking':'PRIVATE_REASONING_MARKER'}},{'message':{'content':json.dumps(parsed())}},{'done':True,'done_reason':'stop','eval_count':20,'message':{}}]:yield json.dumps(x).encode()
    class Opener:
        def open(self,*a,**kw):return Response()
    m=object.__new__(CommonFallback);m.config={'base_url':'http://127.0.0.1:11434','timeout_seconds':3};m.opener=Opener()
    result=m.http('/api/chat',{'messages':[]})
    assert json.loads(result['message']['content'])==parsed()
    assert result['thinking_diagnostics']['characters']==24
    assert 'PRIVATE_REASONING_MARKER' not in json.dumps(result)
    assert result['thinking_diagnostics']['time_to_first_token_ms'] is not None


def test_unvalidated_prose_is_not_persisted_as_a_structured_answer():
    from cascade.fallback import CommonFallback
    class Response:
        def __enter__(self):return self
        def __exit__(self,*a):pass
        def __iter__(self):yield json.dumps({'done':True,'done_reason':'stop','message':{'content':'PRIVATE_INVALID_PROSE'}}).encode()
    class Opener:
        def open(self,*a,**kw):return Response()
    m=object.__new__(CommonFallback);m.config={'base_url':'http://127.0.0.1:11435','timeout_seconds':3};m.opener=Opener()
    result=m.http('/api/chat',{})
    assert result['answer_validation_error']['unvalidated_text_stored'] is False
    assert result['message']['content']=='{}';assert 'PRIVATE_INVALID_PROSE' not in json.dumps(result)
