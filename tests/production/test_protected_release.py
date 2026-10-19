"""Full customer qualification protocol using explicit non-model doubles."""
import json
from pathlib import Path
from contextlib import contextmanager
import pytest
from apps.api import store
from production import storage, service, qualification, confidence, evaluation
from training.framework import jobs, events, releases
from training.framework.bundle import write
from tests.unit.test_trainable_releases import registered, prepared, validation
from tests.unit.test_learning_comparison import result
from tests.production.test_client_workflow import row, body


def prepare_case():
    storage.initialise()
    imported = service.import_rows('fixture-import', [row('FROZEN_TEST')], 'AI_operator')
    eid = imported['rows'][0]['event_id']; view = service.source_view(eid)
    target = {**body(view), 'model_id':'EXPLICIT_SOFTWARE_FIXTURE'}
    service.review(eid, target, {'name':'AI_operator','expert_attested':False}, ai=True)
    service.freeze('fixture-frozen', [eid], 'AI_operator')
    release = prepared(mode='QWEN_ONLY')
    identity = releases.verify(release)['identity']; validation(release/'valid', identity); releases.seal(release,release/'valid')
    cal = jobs.WORKSPACE/'customer-calibrators'/'fixture.json';cal.parent.mkdir()
    confidence.fit([{'id':'x','role':'CALIBRATION','fold':'FIT','group':'x','predicate':'votability',
                     'features':{'language':'en'},'correct':True,'origin':'AI_AUTHORED'}],
                   identity=identity,population='AI_FRAMEWORK',output=cal)
    return eid, release, cal


def test_ai_framework_evaluation_cannot_promote_even_if_predictions_match(registered, monkeypatch):
    eid, release, cal = prepare_case()
    qualification.prepare('q1', release_id=release.name,dataset_id='fixture-frozen',calibrator_path=cal,
                          population='AI_FRAMEWORK',policy={},reference='2026-10-18T12:00:00+00:00',actor='AI_operator')
    output = qualification.root('q1')
    class ExplicitDouble:
        def __init__(self,p,**kw): pass
        def analyse(self,text,**kwargs):
            # A model must never receive any expected target/review objects.
            assert set(kwargs) <= {'use_iso','reference','structured_context','deadline_override'}
            assert not (output/'PREDICTIONS_SAVED.json').exists()
            return result()
        def close(self): pass
    monkeypatch.setattr(releases,'ReleaseModel',ExplicitDouble)
    original = store.connect
    @contextmanager
    def guarded(*a,**kw):
        with original(*a,**kw) as c:
            def authorizer(action, table, *rest):
                if action == __import__('sqlite3').SQLITE_READ and table in ('learning_reviews','client_review_identity'):
                    assert (output/'PREDICTIONS_SAVED.json').exists(), 'Answer read before durable blind predictions'
                return __import__('sqlite3').SQLITE_OK
            c.set_authorizer(authorizer)
            yield c
    monkeypatch.setattr(store,'connect',guarded)
    receipt = qualification.evaluate('q1')
    assert receipt['metrics']['all_fields_exact_correct'] == 1
    assert not receipt['customer_gate_passed']
    assert 'SYNTHETIC_OR_NONEXPERT_TEST_LABELS' in receipt['reasons']
    assert 'EXPERT_CALIBRATION_REQUIRED' in receipt['reasons']
    qualification.verify('q1')
    with pytest.raises(ValueError, match='already reserved'):
        qualification.prepare('q2',release_id=release.name,dataset_id='fixture-frozen',calibrator_path=cal,
                              population='AI_FRAMEWORK',policy={'threshold':.5},reference='2026-10-18T12:00:00+00:00',actor='AI_operator')
    with pytest.raises(ValueError,match='quality gate'): service.promote('q1','administrator',None)
    plan=json.loads((output/'plan.json').read_text());plan['policy']['threshold']=.5
    (output/'plan.json').write_text(json.dumps(plan))
    with pytest.raises(ValueError,match='changed'): qualification.verify('q1')


def test_lexical_duplicates_and_declared_families_form_one_independent_component():
    a='Shareholders may vote at the Annual General Meeting and must register by the deadline.'
    rows=[{'id':'a','text':a,'group_id':'g1','generation_family':'f1'},
          {'id':'b','text':a,'group_id':'g2','generation_family':'f2'},
          {'id':'c','text':'A completely unrelated cash redemption closes shortly.','group_id':'g3','generation_family':'f2'}]
    groups=qualification.independent_groups(rows)
    assert len(set(groups.values()))==1


def test_active_structured_snapshot_defines_input_type_without_message_parser_key(db):
    storage.initialise()
    row={'id':'unregistered','messages':[{'id':1}], 'active_structure':{'parser':'PROWIDE'}}
    assert evaluation.input_metadata(row)['input_type']=='PROWIDE_PARSEABLE'
    row['context_kind']='RECOVERED_REVIEW_CONTEXT'
    assert evaluation.input_metadata(row)['input_type']=='LENIENT_ISO_RECOVERABLE'


def test_legacy_snapshot_without_raw_sources_rejected_before_model_load(tmp_path,monkeypatch):
    legacy={'id':'legacy','messages':[{'id':1,'source_hash':'archived'}]}
    monkeypatch.setattr(evaluation,'load_inputs',lambda *a:({},[legacy]))
    def unexpected(*a,**kw): pytest.fail('Legacy provenance must fail before loading any model')
    monkeypatch.setattr(releases,'ReleaseModel',unexpected)
    with pytest.raises(ValueError,match='raw-message provenance'):
        evaluation.predict('dataset','VALIDATION','release',tmp_path/'predictions','2026-10-18T12:00:00+00:00')
    assert not (tmp_path/'predictions').exists()


def test_final_truth_inconsistency_and_timezone_are_rejected(db):
    storage.initialise()
    r=service.import_rows('a',[row()],'operator');eid=r['rows'][0]['event_id']
    v=service.source_view(eid);data=body(v);data['expected_final_status']='NOT_VOTABLE';data['model_id']='AI_fixture'
    with pytest.raises(ValueError,match='conflicts'): service.review(eid,data,{'name':'AI','expert_attested':False},ai=True)
    data=body(v);data['evaluation_time']='2026-10-18T12:00:00';data['model_id']='AI_fixture'
    with pytest.raises(ValueError,match='timezone'): service.review(eid,data,{'name':'AI','expert_attested':False},ai=True)


def test_customer_training_never_opens_calibration_or_frozen_keys(registered, tmp_path, monkeypatch):
    # A CLI campaign must also work before the customer API has ever started.
    with store.connect() as c:
        assert not c.execute("SELECT name FROM sqlite_master WHERE name='client_metadata'").fetchone()
    from production import learning
    from training.framework import campaigns
    from training.framework.bundle import jsonl, sha
    from training.framework.event_data import write_role_answers
    from classifier.preprocessing import source_hash
    from types import SimpleNamespace
    data=jobs.member('event-datasets','development');data.mkdir(parents=True);(data/'private').mkdir()
    rows=[{'id':r,'text':'Notice','source_hash':source_hash('Notice'),'snapshot_hash':r,'split':r,
           'group_id':r,'generation_family':r,'messages':[]} for r in ['TRAIN','VALIDATION','CALIBRATION','FROZEN_TEST']]
    jsonl(data/'inputs.jsonl',rows)
    answers=[{'id':r['id'],'snapshot_hash':r['snapshot_hash'],'split':r['split'],
              'target':{k:'VOTABLE' if k=='votability' else 'NO' for k in events.PREDICATES},
              'provenance':{'origin':'AI_AUTHORED'}} for r in rows]
    answer_files=write_role_answers(data,rows,answers)
    write(data/'manifest.json',{'roles':{r['split']:1 for r in rows},'input_file':'inputs.jsonl',
                               'input_sha256':sha(data/'inputs.jsonl'),'answer_files':answer_files})
    bundle=jobs.member('bundles','development');bundle.mkdir(parents=True);write(bundle/'manifest.json',{})
    monkeypatch.setattr(campaigns,'load_bundle',lambda p:({'label_origins':{'AI_AUTHORED':2}},
                         [SimpleNamespace(id=r['id'],source_hash=r['source_hash'],split=r['split']) for r in rows[:2]]))
    root=jobs.member('campaigns','customer')
    learning.prepare({'bundle_id':'development','dataset_id':'development','actor':'AI_fixture',
                      'stages':[{'name':'qwen','reuse_job':'qwen'}],
                      'candidates':[{'name':'qwen','mode':'QWEN_ONLY','llm_stage':'qwen'}]},root)
    original=Path.read_text
    def guard(path,*a,**kw):
        if path.name in ('calibration-answers.jsonl','frozen_test-answers.jsonl'):pytest.fail('Customer development opened protected truth')
        return original(path,*a,**kw)
    monkeypatch.setattr(Path,'read_text',guard)
    class Model:
        def __init__(self,*a,**kw):pass
        def analyse(self,*a,**kw):return result()
        def close(self):pass
    monkeypatch.setattr(releases,'ReleaseModel',Model)
    report=learning.run(root)
    with store.connect() as c:
        assert c.execute("SELECT name FROM sqlite_master WHERE name='client_metadata'").fetchone()
    assert report['calibration_or_test_answers_opened'] is False
    assert (jobs.member('releases',report['selected_release'])/'SEALED.json').exists()
    assert campaigns.status(root)['state']=='COMPLETED'
