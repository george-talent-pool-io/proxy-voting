from semantic_pipeline.decision import decide
from semantic_pipeline.schema import PREDICATES


def test_clear_semantics_cannot_grant_automation_or_invent_population_origin():
    facts={k:{'value':'VOTABLE' if k=='votability' else 'NO'} for k in PREDICATES}
    r=decide(facts,{'status':'OPEN'})
    assert r['classification']=='VOTABLE' and not r['manual_review_required']
    assert not r['automation_enabled'] and not r['review_reasons']
    r=decide(facts,{'status':'OPEN'},['ACTUAL_FACT_CONFLICT'])
    assert r['classification']=='UNCERTAIN_MANUAL_REVIEW' and r['manual_review_required']
    assert 'ACTUAL_FACT_CONFLICT' in r['review_reasons'] and not r['automation_enabled']


def test_repaired_llm_output_remains_review_only_with_no_borrowed_confidence(monkeypatch):
    from production import qualification as q,confidence
    from tests.unit.test_learning_comparison import result
    value=result();value['llm']={'invoked':True,'schema_handling':{'repair_attempts':1}}
    seen=[]
    def score(cal,key,f,**kwargs):
        seen.append(f)
        return None if f['force_review'] else .999
    monkeypatch.setattr(confidence,'predict',score)
    assessed=q.assess('Notice',value,{'language':'en','input_type':'UNSTRUCTURED_NOTICE','population':'AI'},
        {'identity':'MODEL','population':'AI'},'MODEL',.99)
    assert not assessed['eligible'] and assessed['final_decision_confidence'] is None
    assert 'LLM_SCHEMA_REPAIR_REQUIRES_REVIEW' in assessed['review_reasons']
    assert len(seen)==10 and all(f['force_review'] and f['features']['schema_repairs']==1 for f in seen)
