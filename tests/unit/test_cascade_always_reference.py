"""Counterfactual report controls use test doubles, never pretend to time a model."""
import copy,json
from cascade import always_reference
from semantic_pipeline.experiment import append,lines,read,sha
from tests.unit.test_cascade_reporting import rows


def test_always_reference_reuses_invoked_and_generates_all_accepted_regardless_of_truth(tmp_path,monkeypatch):
    monkeypatch.setattr(always_reference,'ROOT',tmp_path)
    monkeypatch.setattr(always_reference,'DATASETS',[('challenge',2),('complete',2)])
    monkeypatch.setattr(always_reference,'verify_core',lambda:None)
    (tmp_path/'PRIMARY-MODEL-SELECTION.json').write_text('{"selected":"GLM"}')
    (tmp_path/'LLM-CONFIGS-v3.json').write_text('{"GLM":{}}')
    monkeypatch.setattr(always_reference,'CommonFallback',lambda cfg:object())
    invoked=rows();invoked['id']='already-invoked'
    invoked['result']['escalation']['escalated']=True
    invoked['result']['llm']={'invoked':True,'valid':True}
    accepted=rows();accepted['id']='accepted-by-gate'
    accepted['result']['laya']['latency_ms']=123
    # Deliberately irrelevant truth proves that the selection is gate-based.
    accepted['expected']={'poa_required':'UNRECOGNISED_SOFTWARE_TEST_LABEL'}
    for dataset in ['challenge','complete']:
        append(tmp_path/f'{dataset}-C_SELECTIVE.jsonl',invoked)
        append(tmp_path/f'{dataset}-C_SELECTIVE.jsonl',accepted)
    calls=[]
    def execute(text,**kwargs):
        assert 'expected' not in kwargs and 'truth' not in kwargs
        assert kwargs['policy'].name=='ALWAYS'
        assert kwargs['precomputed']==accepted['result']['laya']
        calls.append(kwargs)
        result=copy.deepcopy(accepted['result']);result['llm']={'invoked':True,'valid':True}
        result['latencies']['total_ms']=456
        return result
    monkeypatch.setattr(always_reference,'execute',execute)
    value=always_reference.build()
    assert len(calls)==2
    for dataset in ['challenge','complete']:
        reused,generated=value[dataset]
        assert reused['reference_reused_invoked_result']
        assert reused['result']==invoked['result']
        assert not generated['reference_reused_invoked_result']
        assert generated['result']['latencies']['total_ms']==579
        assert generated['result']['latencies']['counterfactual_wall_ms']==456
        assert 'not fresh' in generated['result']['latencies']['timing_scope']
    commit=read(tmp_path/'ALWAYS-REFERENCE-COMMIT.json')
    assert commit['quality_reference_only']
    for path,h in commit['files'].items():assert sha(path)==h
    always_reference.build()
    assert len(calls)==2,'Resuming a complete reference must not regenerate its predictions'
