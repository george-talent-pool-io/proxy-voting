import copy
import json
from pathlib import Path
from semantic_pipeline.metrics import summarize
from semantic_pipeline.reporting import transition_analysis, report
from tests.unit.test_semantic_pipeline import TEXT,specialist,llm,parsed
from semantic_pipeline.pipeline import run


def result(value='UNKNOWN'):
    class Model:
        def analyse(self,text):return specialist(value)
    class Fallback:
        def analyse(self,**kw):return llm()
    return run(TEXT,'E',laya_model=Model(),fallback=Fallback())


def test_unlabelled_predicates_never_count_as_correct():
    row={'id':'case','text':TEXT,'expected':{'poa_required':'NO'},'result':result()}
    m=summarize([row]);assert m['assertions']==1;assert set(m['fields'])=={'poa_required'}
    assert m['final_status_labelled_cases']==0;assert m['customer_status_accuracy'] is None


def test_oracle_and_transition_denominators_are_assertion_specific():
    a=result();row={'id':'case','text':TEXT,'expected':{'poa_required':'NO'},'result':a}
    t=transition_analysis([row],'E',[row],[row]);assert t['oracle']['semantic_assertions']==1
    assert t['semantic_assertion_transition_reconciled']=={'wrong → correct':1}
    assert t['oracle']['oracle_cases_correct']==1


def test_full_report_path_uses_commit_then_key_and_writes_all_denominators(tmp_path,monkeypatch):
    from semantic_pipeline import experiment,reporting
    monkeypatch.setattr(experiment,'verify',lambda:None)
    (tmp_path/'FREEZE.json').write_text('{}')
    (tmp_path/'PREDICTION-COMMIT.json').write_text(json.dumps({'files':{}}))
    expected={'poa_required':'NO'}
    value=result()
    for dataset in ('challenge','synthetic-development','complete'):
        for arm in 'ABCDE':
            row={'id':'CASE','run_id':'test-only','input_hash':__import__('hashlib').sha256(TEXT.encode()).hexdigest(),
                'text':TEXT,'expected':expected,'result':value}
            (tmp_path/f'{dataset}-{arm}.jsonl').write_text(json.dumps(row)+'\n')
    calls=[]
    class FakeZip:
        def __init__(self,*a):calls.append('key-opened')
        def __enter__(self):return self
        def __exit__(self,*a):pass
        def read(self,name):
            assert (tmp_path/'PREDICTION-COMMIT.json').exists()
            return b'id,votability,share_blocking,poa_required,other_restriction,deadline_status,expected_customer_status\nCASE,VOTABLE,NO,NO,NO,UNKNOWN,UNCERTAIN_MANUAL_REVIEW\n'
    monkeypatch.setattr(reporting,'ZipFile',FakeZip)
    out=report(tmp_path,report_path=tmp_path/'REPORT.md')
    assert calls==['key-opened'];assert out['datasets']['challenge']['A']['assertions']==1
    assert out['datasets']['challenge']['D']['final_status_labelled_cases']==0
    assert out['datasets']['synthetic-development']['A']['final_status_labelled_cases']==1
    assert not out['quality_gate']['passed'];assert not out['automation_enabled']
    assert (tmp_path/'REPORT.md').exists();assert (tmp_path/'complete-FAILURES.json').exists()
