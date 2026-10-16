import copy,json
from cascade import reporting
from cascade.routing import Policy
from cascade.pipeline import execute
from semantic_pipeline.reconcile import reconcile
from semantic_pipeline.decision import decide
from tests.unit.test_semantic_pipeline import specialist,llm,parsed,TEXT
from semantic_pipeline.schema import RESTRICTIONS,PREDICATES


def rows():
    source=TEXT;s=specialist('NO');r=execute(source,precomputed=s,policy=Policy(name='AGGRESSIVE',require_positive_evidence=False,escalate_unknown=False))
    expected={'votability':'VOTABLE',**{k:'NO' for k in RESTRICTIONS},'poa_required':'YES','deadline_status':'UNKNOWN','classification':'VOTABLE_WITH_RESTRICTION'}
    row={'id':'software-fixture','text':source,'expected':expected,'result':r}
    return row


def test_pairs_preserve_denominators_and_identify_repairs():
    a=rows();b=copy.deepcopy(a);b['result']['reconciliation']['predicates']['poa_required']['value']='YES'
    b['result']['decision']['classification']='VOTABLE_WITH_RESTRICTION'
    m=reporting.paired_comparison({'D1':[a],'D2':[b]},('D1','D2'))
    assert sum(m['all_assertions'].values())==11;assert m['all_assertions']['right_only_correct']==2
    assert len(m['disagreements'])==2;assert m['TWO_LLM_ORACLE']['correct']==11


def test_oracle_generates_only_missing_wrong_cases_and_does_not_pass_truth(monkeypatch,tmp_path):
    row=rows();monkeypatch.setattr(reporting,'ROOT',tmp_path)
    (tmp_path/'LLM-CONFIGS-v3.json').write_text('{"GLM":{}}')
    payload=parsed(poa_required='YES');payload['evidence']['poa_required']=['A power of attorney is mandatory.']
    calls=[]
    class Model:
        def __init__(self,cfg):pass
        def request(self,*args):return {'only':'same-experimental-context'}
        def analyse(self,**kwargs):
            assert 'expected' not in kwargs;assert 'truth' not in kwargs
            calls.append(kwargs);return llm(payload)
    monkeypatch.setattr(reporting,'CommonFallback',Model)
    result=reporting.actual_oracles({'challenge':{'C_SELECTIVE':[row],'E_SELECTIVE':[row]}},'GLM')
    # Identical fallback requests are reused only in this untimed analytical oracle.
    assert len(calls)==1
    m=result['challenge']['C_SELECTIVE']['all_assertions']
    assert m['assertions']==11;assert m['laya_errors']==2;assert m['llm_correct_on_errors']==2;assert m['oracle_correct']==11
    assert not result['challenge']['C_SELECTIVE']['deployable']


def test_no_llm_usage_metrics_are_not_fabricated():
    m=reporting.inference_stats([rows()]);assert m['llm_calls']==0
    assert m['median_llm_ms'] is None;assert m['tokens']=={}


def test_absent_predicate_truth_not_counted_in_pair_metrics():
    row=rows();row['expected']={'poa_required':'YES'}
    m=reporting.paired_comparison({'D1':[row],'D2':[row]},('D1','D2'))
    assert set(m['per_predicate'])=={'poa_required'}
    assert sum(m['all_assertions'].values())==1


def test_entire_report_and_plot_pipeline_with_explicit_software_fixtures(tmp_path,monkeypatch):
    """Exercises every report path without claiming fake fixtures as real-model data."""
    from semantic_pipeline.experiment import append
    from semantic_pipeline.metrics import summarize
    monkeypatch.chdir(tmp_path);root=tmp_path/'study';root.mkdir();(tmp_path/'data/reports').mkdir(parents=True)
    monkeypatch.setattr(reporting,'ROOT',root);monkeypatch.setattr(reporting,'verify_core',lambda:None)
    monkeypatch.setattr(reporting,'expected_rows',lambda dataset:1)
    monkeypatch.setattr(reporting,'actual_oracles',lambda *a:{'SOFTWARE_FIXTURE_ONLY':True})
    row=rows();row['input_hash']=row['result']['input_hash'];row['run_id']='SOFTWARE_FIXTURE';row['timestamp']='2026-10-16T12:00:00Z'
    from cascade import always_reference
    monkeypatch.setattr(always_reference,'build',lambda:{d:[row] for d in ['challenge','complete']})
    base=summarize([row]);positive_misses={k:0 for k in PREDICATES}
    policy={'name':'ALWAYS','min_score':.9,'min_margin':.4}
    candidate={'policy':policy,'semantic_agreement':.8,'llm_call_rate':1,'llm_invocations':1,'laya_only_coverage':0,'fields':base['fields'],'positive_misses':positive_misses}
    for name,value in [('PREDICTION-COMMIT.json',{'files':{}}),('PRIMARY-MODEL-SELECTION.json',{'selected':'GLM','metrics':{},'ranking':'SOFTWARE FIXTURE'}),('ROUTING-SELECTION.json',{'selected':candidate,'always':candidate,'candidates':[candidate]}),('COMMON-CONDITION-FREEZE.json',{}),('FINAL-SELECTION-FREEZE.json',{})]:
        (root/name).write_text(json.dumps(value))
    for dataset in ['challenge','complete']:
        for c in reporting.CONDITIONS:append(root/f'{dataset}-{c}.jsonl',row)
        append(root/f'{dataset}-SPECIALISTS.jsonl',{'id':row['id'],'expected':row['expected'],'capable':row['result']['laya'],'narrow':row['result']['laya'],'fixed_narrow':row['result']['laya']})
    reporting.report()
    assert (root/'SUMMARY.json').exists();assert (root/'COVERAGE-QUALITY.png').stat().st_size>1000
    for name in ['GLM_VS_QWEN_DISAGREEMENTS.md','GLM_QWEN_MODEL_SELECTION.md','QWEN_THINKING_REPAIR_DAMAGE.md','AGGREGATION_SELECTIVE_CASCADE_EVALUATION.md']:
        assert (tmp_path/'data/reports'/name).stat().st_size>100
