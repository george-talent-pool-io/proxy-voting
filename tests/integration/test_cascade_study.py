import json
from pathlib import Path
from semantic_pipeline.models import WholeLaya
from cascade import study
from tests.unit.test_semantic_pipeline import llm,TEXT

def test_common_comparison_uses_identical_specialist_diagnostics_and_resumes(tmp_path,monkeypatch,classifier):
    monkeypatch.setattr(study,'ROOT',tmp_path);monkeypatch.setattr(study,'verify_core',lambda:{})
    monkeypatch.setattr(study,'unload_other',lambda *a:None)
    whole=WholeLaya(classifier=classifier);native=whole.analyse(TEXT)
    monkeypatch.setattr(study,'WholeLaya',lambda **kw:whole)
    configs={'GLM':{'model':'test-model'}};(tmp_path/'LLM-CONFIGS-v3.json').write_text(json.dumps(configs))
    (tmp_path/'COMMON-CONDITION-FREEZE.json').write_text('{}')
    (tmp_path/'validation-specialists.jsonl').write_text(json.dumps({'id':'one','whole':native})+'\n')
    calls=[]
    class Fallback:
        def __init__(self,config):pass
        def http(self,*a):return {'models':[]}
        def analyse(self,**kw):
            calls.append(kw);return llm()
    monkeypatch.setattr(study,'CommonFallback',Fallback)
    row={'id':'one','text':TEXT,'expected':{'votability':'VOTABLE'}}
    first=study.benchmark_condition('validation','C1','GLM',[row])
    assert first[0]['result']['llm']['valid'];assert calls[-1]['mode']=='FALLBACK'
    assert calls[-1]['laya_result']['predicates']['votability']['value']=='VOTABLE'
    again=study.benchmark_condition('validation','C1','GLM',[row])
    assert first==again;assert len(calls)==2  # One warm-up + one actual call; resume invokes no model.
    independent=study.benchmark_condition('validation','D1','GLM',[row])
    assert calls[-1]['mode']=='INDEPENDENT';assert calls[-1].get('laya_result') is None


def test_complete_validation_is_not_training_and_has_all_truth():
    from cascade.validation import build
    from semantic_pipeline.schema import PREDICATES
    rows=build();assert len(rows)==80
    assert all(set(PREDICATES)|{'classification','deadline_status'}<=set(r['expected']) for r in rows)
    assert all(r['not_for_training'] and r['source_type']=='SYNTHETIC_VALIDATION_ONLY' for r in rows)
