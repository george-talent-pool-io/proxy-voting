import copy
import json
from pathlib import Path
from types import SimpleNamespace
import pytest
from pydantic import ValidationError
from semantic_pipeline.schema import PREDICATES, RESTRICTIONS, SemanticResult
from semantic_pipeline.evidence import verify_evidence, validate_all
from semantic_pipeline.fallback import OllamaFallback, DisabledFallback, from_environment
from semantic_pipeline.models import factor
from semantic_pipeline.routing import RoutingConfig, escalate
from semantic_pipeline.reconcile import reconcile, llm_factors
from semantic_pipeline.decision import decide
from semantic_pipeline.metrics import field_metrics, summarize, truth
from semantic_pipeline.pipeline import prepare, resolve_deadline, run
from semantic_pipeline.benchmark import build

TEXT='Owners may vote. A power of attorney is mandatory.'

def parsed(**overrides):
    out={'votability':'VOTABLE',**{k:'NO' for k in RESTRICTIONS},
        'deadline_information':{'deadline_mentioned':False,'deadline_text':None},
        'evidence':{k:[] for k in PREDICATES},'ambiguities':[]}
    out['evidence']['votability']=['Owners may vote.']
    out.update(overrides);return out

def llm(data=None,source=TEXT):
    data=data or parsed();return {'invoked':True,'valid':True,'parsed':data,
        'evidence_validation':validate_all(source,data),'latency_ms':2}

def specialist(value='NO'):
    return {'predicates':{k:factor('VOTABLE' if k=='votability' else value,'LAYA',{'YES':.1,'NO':.9}) for k in PREDICATES},'latency_ms':1,'checkpoint':'TEST_DOUBLE','model_version':'fake','truncated':False}

@pytest.mark.parametrize('source,quote,ok',[('abc','b',True),('abc','B',False),('é😀\nXYZ','😀\nX',True),('e\u0301','é',False),('abc','',False),('abc','   ',False),('source','invented',False)])
def test_exact_evidence_offsets(source,quote,ok):
    r=verify_evidence(source,quote);assert r['valid']==ok
    if ok:assert source[r['start']:r['end']]==r['text']

def test_typed_output_rejects_extra_confidence_and_missing_factor():
    SemanticResult.model_validate(parsed())
    with pytest.raises(ValidationError):SemanticResult.model_validate({**parsed(),'confidence':.99})
    data=parsed();del data['holding_confirmation_required']
    with pytest.raises(ValidationError):SemanticResult.model_validate(data)

@pytest.mark.parametrize('field',RESTRICTIONS)
def test_output_enums_not_boolean_or_arbitrary(field):
    with pytest.raises(ValidationError):SemanticResult.model_validate(parsed(**{field:True}))
    with pytest.raises(ValidationError):SemanticResult.model_validate(parsed(**{field:'MAYBE'}))

@pytest.mark.parametrize('url',['https://example.com','http://10.0.0.1:11434','http://localhost:11434','http://127.0.0.1:11434/other','http://user:pass@127.0.0.1:11434'])
def test_external_runtime_rejected_before_network(url):
    with pytest.raises(ValueError):OllamaFallback({'base_url':url})

def test_default_disabled_even_when_runtime_installed(monkeypatch):
    monkeypatch.delenv('LLM_ENABLED',raising=False);assert isinstance(from_environment(),DisabledFallback)
    assert not DisabledFallback().analyse()['invoked']

def test_independent_context_cannot_contain_laya():
    m=object.__new__(OllamaFallback);m.prompt='test';m.config={'model':'x','think':False,'keep_alive':'1m','temperature':0,'seed':42,'num_ctx':8192,'num_predict':512}
    with pytest.raises(ValueError):m.request(TEXT,TEXT,{},specialist(),'INDEPENDENT')
    request=m.request(TEXT,TEXT,{},None,'INDEPENDENT')
    assert 'laya' not in request['messages'][1]['content'].lower()
    request=m.request(TEXT,TEXT,{},specialist(),'FALLBACK')
    assert 'reason_for_escalation' in request['messages'][1]['content']

@pytest.mark.parametrize('score',[float('nan'),-1,1.01])
def test_invalid_thresholds(score):
    with pytest.raises(ValueError):RoutingConfig(min_score=score)

def test_gate_reports_distinct_causes_and_never_enables_automation():
    a=specialist();a['predicates']['share_blocking']=factor('UNKNOWN','LAYA',{'YES':.4,'NO':.3,'UNKNOWN':.3},conflict=True)
    a['predicates']['holding_confirmation_required']=factor('NOT_SUPPORTED','LAYA')
    r=escalate(a,{},TEXT,RoutingConfig(min_score=.7,min_margin=.2))
    assert {'UNSUPPORTED_REQUIRED_PREDICATE','UNKNOWN_LAYA_OUTPUT','LOW_LAYA_SCORE','LOW_LAYA_MARGIN','CONFLICTING_PASSAGES'}<=set(r['reasons'])

def test_unsupported_is_not_silently_negative():
    a=specialist();a['predicates']['holding_confirmation_required']=factor('NOT_SUPPORTED','LAYA')
    r=reconcile({},a,None);assert r['predicates']['holding_confirmation_required']['value']=='NOT_SUPPORTED'
    assert decide(r['predicates'],{'status':'OPEN'})['classification']=='UNCERTAIN_MANUAL_REVIEW'

def test_disagreement_without_validation_preference_requires_review():
    data=parsed(poa_required='YES');data['evidence']['poa_required']=['A power of attorney is mandatory.']
    r=reconcile({},specialist(),llm(data));assert r['predicates']['poa_required']['value']=='UNKNOWN';assert r['conflicts']
    assert decide(r['predicates'],{'status':'OPEN'},r['conflicts'])['classification']=='UNCERTAIN_MANUAL_REVIEW'

def test_only_empirical_preference_may_resolve_disagreement():
    data=parsed(poa_required='YES');data['evidence']['poa_required']=['A power of attorney is mandatory.']
    r=reconcile({},specialist(),llm(data),{'poa_required':{'prefer':'LLM','disagreements':12,'wilson95_lower':.7}})
    assert r['predicates']['poa_required']['value']=='YES';assert not r['conflicts']

def test_authoritative_structure_never_overwritten():
    a=specialist();s={'votability':factor('NOT_VOTABLE','ISO15022')}
    r=reconcile(s,a,llm());assert r['predicates']['votability']['value']=='NOT_VOTABLE';assert r['conflicts']

def test_false_quote_cannot_be_displayed_or_support_a_positive():
    data=parsed(poa_required='YES');data['evidence']['poa_required']=['Fabricated requirement.']
    r=llm_factors(llm(data));assert r['poa_required']['value']=='UNKNOWN';assert not r['poa_required']['evidence']

def test_absent_negative_and_unsupported_are_distinct():
    data=parsed();r=llm_factors(llm(data));assert r['share_blocking']['value']=='NO';assert not r['share_blocking']['evidence']

@pytest.mark.parametrize('field',RESTRICTIONS)
def test_each_independent_restriction_derives_restricted_status(field):
    fs=specialist()['predicates'];fs[field]=factor('YES','MODEL')
    d=decide(fs,{'status':'OPEN'});assert d['classification']=='VOTABLE_WITH_RESTRICTION';assert not d['automation_enabled'];assert not d['manual_review_required']

def test_decision_precedence():
    fs=specialist()['predicates'];fs['share_blocking']=factor('YES','MODEL')
    assert decide(fs,{'status':'PASSED'})['classification']=='DEADLINE_PASSED'
    fs['votability']=factor('NOT_VOTABLE','MODEL')
    assert decide(fs,{'status':'PASSED'})['classification']=='NOT_VOTABLE'
    assert decide(fs,{'status':'PASSED'},['contradiction'])['classification']=='UNCERTAIN_MANUAL_REVIEW'

def test_deadline_source_validation_and_fixed_reference():
    text='Owners may vote. Voting instructions are due by 24 November 2026.'
    p=prepare(text)
    assert resolve_deadline(text,p,reference='2026-10-16T12:00:00+00:00')['status']=='OPEN'
    assert resolve_deadline(text,p,reference='2026-12-01T12:00:00+00:00')['status']=='PASSED'
    data=parsed();data['deadline_information']={'deadline_mentioned':True,'deadline_text':'Voting instructions are due by 2 January 2026.'}
    assert resolve_deadline(text,p,llm(data,text))['status']=='OPEN'

def test_positive_recall_exposes_majority_class_failure():
    m=field_metrics(['YES']*11+['NO']*80+['UNKNOWN']*9,['UNKNOWN']*11+['NO']*80+['UNKNOWN']*9)
    assert m['accuracy']==.89;assert m['positive_support']==11;assert m['positive_recall']==0
    assert m['negative_support']==80;assert m['negative_recall_specificity']==1

def test_partial_truth_and_not_supported_remain_in_denominator():
    assert truth({'share_blocking':True,'votable':'YES'})=={'share_blocking':'YES','votability':'VOTABLE'}
    m=field_metrics(['YES','NO'],['NOT_SUPPORTED','NO']);assert m['n']==2;assert m['accuracy']==.5;assert m['not_supported']==1

def test_complete_benchmark_label_completeness_and_uniqueness():
    rows=build();assert len(rows)==48;assert len({r['text'] for r in rows})==48
    for r in rows:assert set(r['expected'])==set(PREDICATES)|{'deadline_status','classification'}
    for k in RESTRICTIONS:assert any(r['expected'][k]=='YES' for r in rows)

def test_real_pipeline_contract_with_explicit_test_doubles():
    class Model:
        def analyse(self,text):return specialist('UNKNOWN')
    class Fallback:
        def analyse(self,**kwargs):return llm()
    result=run(TEXT,'E',laya_model=Model(),fallback=Fallback())
    assert result['escalation']['escalated'];assert result['llm']['invoked']
    assert result['laya']['predicates']['poa_required']['value']=='UNKNOWN'
    assert result['reconciliation']['predicates']['poa_required']['value']=='NO'
    assert result['parser']['raw']==TEXT
    assert not result['automation_enabled']

@pytest.mark.parametrize('bad',[None,'','  ',23,{}])
def test_invalid_inputs_rejected_cleanly(bad):
    with pytest.raises(ValueError):prepare(bad)


def test_structured_only_does_not_send_iso_tags_to_semantic_models():
    class Crash:
        def analyse(self,*a,**kw):raise AssertionError('No narrative should enter ML')
    source=':16R:GENL\n:20C::SEME//NOSEM001\n:23G:NEWM\n:22F::CAEV//MEET\n:16S:GENL'
    r=run(source,'E',laya_model=Crash(),fallback=Crash())
    assert not r['escalation']['escalated'];assert r['llm'] is None
    assert r['laya']['latency_ms']==0
    assert r['structured_facts']['iso15022_fields']
    assert r['decision']['classification']=='UNCERTAIN_MANUAL_REVIEW'


def test_generated_partial_messages_have_valid_supported_deadline_grammar():
    from hybrid.parser import parse, deadline_status
    count=0
    for row in build():
        if row['input_kind']=='STANDARDS_DERIVED_PARTIAL_ISO15022':
            p=parse(row['text']);assert not p['errors'];assert deadline_status(p,'2026-10-16T12:00:00+00:00')['status']=='OPEN';count+=1
    assert count==8


def test_structured_deadline_retained_while_narrative_conflict_escalates():
    source=':16R:GENL\n:20C::SEME//DATE001\n:23G:NEWM\n:22F::CAEV//MEET\n:16S:GENL\n:16R:CADETL\n:98E::RDDT//20261124170000/0000\n:70E::ADTX//Owners may vote. Custodian deadline: 4 September 2026.\n:16S:CADETL'
    p=prepare(source,True);d=resolve_deadline(source,p)
    assert d['status']=='OPEN';assert d['source']=='ISO15022_DETERMINISTIC';assert d['conflict']
