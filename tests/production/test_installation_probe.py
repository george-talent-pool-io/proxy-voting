"""Contracts use explicit doubles; real installation receipts are separate."""
import pytest
from scripts import qualify_model_installation as probe


def test_linux_probe_uses_actual_model_admission(monkeypatch,tmp_path):
    from production import installation
    monkeypatch.setattr(probe.releases,'verify_seal',lambda p:({'identity':'TEST'},{}))
    monkeypatch.setattr(probe.platform,'system',lambda:'Linux')
    def denied(root):raise ValueError('MLX checkpoint is not a Linux serving artifact')
    monkeypatch.setattr(installation,'inference_admission',denied)
    with pytest.raises(ValueError,match='MLX checkpoint'):probe.preflight(tmp_path)


def test_unsealed_probe_needs_explicit_research_option(monkeypatch,tmp_path):
    def denied(root):raise ValueError('Missing source seal')
    monkeypatch.setattr(probe.releases,'verify_seal',denied)
    with pytest.raises(ValueError,match='source seal'):probe.preflight(tmp_path)
    monkeypatch.setattr(probe.releases,'verify',lambda p:{'identity':'TEST'})
    monkeypatch.setattr(probe.platform,'system',lambda:'Darwin')
    assert probe.preflight(tmp_path,allow_unsealed=True)[0]['identity']=='TEST'


def test_reproducibility_signature_ignores_latency_not_semantics():
    from tests.unit.test_learning_comparison import result
    a=result();b=result();b['latencies']={'total_ms':1234}
    assert probe.semantic_signature(a)==probe.semantic_signature(b)
    b['predicates']['share_blocking']['value']='YES'
    assert probe.semantic_signature(a)!=probe.semantic_signature(b)


def test_probe_cannot_pass_with_an_unexercised_configured_llm(monkeypatch,tmp_path):
    from contextlib import nullcontext
    from training.framework import resources
    from tests.unit.test_learning_comparison import result
    manifest={'identity':'EXPLICIT_TEST','sources':{},'models':{'laya':{},'llm':{}}}
    monkeypatch.setattr(probe,'preflight',lambda *a,**kw:(manifest,{}))
    monkeypatch.setattr(probe.releases,'verify',lambda root:manifest)
    monkeypatch.setattr(resources,'model_resource',lambda *a,**kw:nullcontext())
    class SpecialistOnlyDouble:
        def __init__(self,*a,**kw):pass
        def analyse(self,*a,**kw):
            r=result();r['laya']={'explicit_test_double':True};r['llm']=None;return r
        def close(self):pass
    receipt=probe.probe('EXPLICIT_TEST',tmp_path/'probe',reference='2026-10-22T12:00:00+00:00',
                        model_factory=SpecialistOnlyDouble)
    assert not receipt['runtime_execution_passed']
    assert receipt['configured_models_not_exercised']==['llm']
    assert receipt['semantic_reload_stable'] and not receipt['production_or_automation_certified']
