"""Portable lineage and calibrator/routing contracts; no model-quality doubles."""
import json
import shutil
import pytest
from production import confidence, operating
from training.framework import seeds
from training.framework.schema import TrainSpec


def tiny_seed(tmp_path):
    model = tmp_path / 'model'; model.mkdir()
    (model / 'model.safetensors').write_bytes(b'EXPLICIT_IDENTITY_FIXTURE_NOT_MODEL_WEIGHTS')
    spec = TrainSpec(backend='LAYA_SDK', family='LAYA', model_path=str(model),
                     base_model_id='EXPLICIT_TEST_FIXTURE', base_revision='fixed-test-revision')
    root = tmp_path / 'seed'
    seeds.freeze(spec, root)
    return root, model


def test_frozen_start_is_dataset_free_relocatable_and_immutable(tmp_path):
    root, model = tiny_seed(tmp_path)
    original = seeds.verify(root)
    relocated = tmp_path / 'relocated'; shutil.copytree(model, relocated)
    assert seeds.verify(root, model_location=relocated)['identity'] == original['identity']
    assert {p.name for p in root.iterdir()} == {'seed.json', 'semantic-prompt.txt', 'laya-questions.json'}
    spec = seeds.training_spec(root, {'epochs': 8, 'encoder_learning_rate': .00002})
    assert spec.epochs == 8 and spec.parent_seed_path == str(root)
    assert spec.initial_adapter_path is None
    with pytest.raises(ValueError, match='parent identity'): seeds.training_spec(root, {'model_path': '/other'})
    (root / 'semantic-prompt.txt').write_text('changed')
    with pytest.raises(ValueError, match='criteria'): seeds.verify(root)


def test_corrupt_weights_and_test_derivatives_cannot_be_foundation(tmp_path):
    root, model = tiny_seed(tmp_path)
    (model / 'model.safetensors').write_bytes(b'changed')
    with pytest.raises(ValueError, match='weights'): seeds.verify(root)
    (model / 'semantic-training-contract.json').write_text('{}')
    with pytest.raises(ValueError, match='foundation'): seeds.freeze(json.loads((root/'seed.json').read_text())['spec'], tmp_path/'bad')
    with pytest.raises(ValueError, match='derivative'): seeds.export_derivative('/missing', tmp_path/'bad', origin='OFFICIAL_FOUNDATION')


def test_frozen_criteria_cannot_silently_change_output_labels(tmp_path):
    root,model=tiny_seed(tmp_path);value=seeds.verify(root)
    questions=json.loads((root/'laya-questions.json').read_text())
    questions['share_blocking']['criteria']={'A':'Positive','B':'Negative','C':'Unresolved'}
    altered=tmp_path/'changed-criteria.json';altered.write_text(json.dumps(questions))
    with pytest.raises(ValueError,match='typed classification schema'):
        seeds.freeze(value['spec'],tmp_path/'invalid-seed',questions_path=altered)
    assert not (tmp_path/'invalid-seed').exists()


def test_dataset_free_starting_checkpoint_serves_without_job_or_bundle(tmp_path,monkeypatch):
    root,model=tiny_seed(tmp_path)
    import laya
    class IdentityContractDouble:
        def predict_batch(self,states,questions,**kwargs):
            answers={}
            for key,q in questions.items():
                label='VOTABLE' if key=='votability' else 'NO'
                answers[key]={'choice':label,'probabilities':{k:.98 if k==label else .01 for k in q['criteria']}}
            return [{'answers':answers,'usage':{}}]
    monkeypatch.setattr(laya,'load',lambda *a,**k:IdentityContractDouble())
    runtime=seeds.FrozenModel(root)
    result=runtime.analyse('Shareholders may vote. No blocking applies.',use_iso=False)
    assert result['job_id'].startswith('FROZEN:') and result['predicates']['votability']['value']=='VOTABLE'
    assert result['checkpoint_manifest_sha256'] and not result['automation_enabled']
    assert not (root/'bundle').exists() and not (root/'plan.json').exists()
    runtime.close()


def rows(correct=True):
    return [{'id':fold+str(i), 'role':'CALIBRATION', 'fold':fold, 'group':fold+str(i),
             'predicate':'share_blocking', 'features':{'language':'en','prediction':'NO','input_type':'UNSTRUCTURED_NOTICE'},
             'correct':correct, 'origin':'AI_AUTHORED'}
            for fold, n in [('FIT', 400), ('EVALUATION', 200)] for i in range(n)]


def test_perfect_predictions_use_honest_constant_estimator_not_fake_errors(tmp_path):
    model = confidence.fit(rows(),identity='MODEL',population='AI_CONTROLLED',output=tmp_path/'cal.json')
    assert model['models']['share_blocking']['method']=='BETA_BINOMIAL_CONSTANT'
    feature={'features':rows()[0]['features'], 'force_review':False}
    p=confidence.predict(model,'share_blocking',feature,identity='MODEL',population='AI_CONTROLLED')
    assert .99 < p < 1
    feature['features']={**feature['features'],'prediction':'YES'}
    assert confidence.predict(model,'share_blocking',feature,identity='MODEL',population='AI_CONTROLLED') is None
    assert model['reports']['share_blocking']['support']['fit_wrong']==0


@pytest.mark.parametrize('mutate', ['nan','wrong-role','same-group','non-bool'])
def test_bad_calibration_inputs_rejected(tmp_path, mutate):
    r=rows()
    if mutate=='nan': r[0]['features']['native_top']=float('nan')
    if mutate=='wrong-role': r[0]['role']='FROZEN_TEST'
    if mutate=='same-group': r[-1]['group']=r[0]['group']
    if mutate=='non-bool': r[0]['correct']=1
    with pytest.raises(ValueError): confidence.fit(r,identity='X',population='X',output=tmp_path/'bad.json')


def operating_rows(role='VALIDATION'):
    from semantic_pipeline.schema import PREDICATES
    truth={k:'VOTABLE' if k=='votability' else 'YES' for k in PREDICATES}
    return [{'id':str(i),'role':role,'group':str(i),'confidence':.995,'force_review':False,
             'exact_correct':True,'truth':truth,'prediction':truth} for i in range(1000)]


def test_operating_policy_selected_on_validation_and_frozen_evaluated_only(tmp_path):
    selected=operating.select(operating_rows(),identity='M',calibrator_hash='C',output=tmp_path/'point.json')
    assert selected['selection']['coverage']==1 and selected['automation_enabled'] is False
    measured=operating.evaluate(operating_rows('FROZEN_TEST'),selected,identity='M',calibrator_hash='C')
    assert measured['wrong_accepted']==0
    assert measured['benchmark_gate_passed'] and not measured['automation_enabled']
    small=operating.evaluate(operating_rows('FROZEN_TEST')[:4],selected,identity='M',calibrator_hash='C')
    assert not small['benchmark_gate_passed'] and 'INSUFFICIENT_ACCEPTED_TEST_GROUPS' in small['reasons']
    with pytest.raises(ValueError,match='VALIDATION'): operating.select(operating_rows('FROZEN_TEST'),identity='M',calibrator_hash='C',output=tmp_path/'bad.json')
    with pytest.raises(ValueError,match='identity'): operating.evaluate(operating_rows('FROZEN_TEST'),selected,identity='OTHER',calibrator_hash='C')


def test_small_perfect_sample_cannot_select_high_precision_threshold(tmp_path):
    m=operating.select(operating_rows()[:4],identity='M',calibrator_hash='C',output=tmp_path/'point.json')
    assert m['selection'] is None and m['status']=='NO_SUPPORTED_OPERATING_POINT'


def test_complete_source_negative_basis_is_never_a_positive_quotation():
    from production.evidence_basis import negative_basis,valid_negative_basis
    text='Shareholders may send a ballot. The notice specifies no other arrangements.'
    p={'value':'NO','negative_basis':negative_basis(text,'EXPLICIT_TEST_MODEL')}
    assert valid_negative_basis(text,p)
    assert not valid_negative_basis(text+' changed',p)
    assert not valid_negative_basis(text,{**p,'value':'YES'})
    assert not valid_negative_basis(text,{**p,'truncated':True})
    f=confidence.feature_row(text,'share_blocking',p,language='en',input_type='UNSTRUCTURED_NOTICE')
    assert f['features']['complete_source_negative'] and f['features']['evidence_mode']=='COMPLETE_SOURCE_NEGATIVE'
    assert not f['features']['evidence_present'] and f['confidence'] is None


def test_quote_calibration_does_not_authorise_unseen_negative_basis(tmp_path):
    records=rows()
    for r in records:r['features']['evidence_mode']='QUOTE'
    cal=confidence.fit(records,identity='M',population='AI',output=tmp_path/'cal.json')
    f={'features':{**records[0]['features'],'evidence_mode':'COMPLETE_SOURCE_NEGATIVE'},'force_review':False}
    assert confidence.predict(cal,'share_blocking',f,identity='M',population='AI') is None
def test_training_diagnostic_exposes_missing_classes_without_inventing_supervision():
    from training.framework.trainers import training_label_support
    from tests.unit.test_training_framework import example
    rows=[example('train'),example('valid','VALIDATION')]
    support=training_label_support(rows)
    assert support['per_predicate']['share_blocking']['TRAIN']['YES']=={'examples':0,'groups':0}
    assert 'share_blocking:YES:NO_TRAINING_EXAMPLES' in support['warnings']
    assert support['per_predicate']['votability']['TRAIN']['VOTABLE']['groups']==1
    assert support['per_predicate']['votability']['VALIDATION']['NOT_VOTABLE']['examples']==1


def test_customer_language_scope_comes_from_calibration_not_research_english_default(tmp_path):
    text='Les actions ne sont pas bloquées.'
    pred={'value':'NO','source':'EXPLICIT_STATISTICAL_FIXTURE','scores':{},'evidence':[{'valid':True,'text':text}]}
    f=confidence.feature_row(text,'share_blocking',pred,language='fr',input_type='UNSTRUCTURED_NOTICE')
    assert not f['force_review']
    # This fixture qualifies software scope checks, not French model quality.
    records=[{'id':str(i),'group':str(i),'role':'CALIBRATION','fold':'FIT' if i<300 else 'EVALUATION',
              'predicate':'share_blocking','features':f['features'],'correct':True,'origin':'AI_SOFTWARE_FIXTURE'} for i in range(460)]
    cal=confidence.fit(records,identity='FR_TEST',population='SOFTWARE_FIXTURE',output=tmp_path/'fr.json')
    assert confidence.predict(cal,'share_blocking',f,identity='FR_TEST',population='SOFTWARE_FIXTURE') is not None
    english=confidence.feature_row(text,'share_blocking',pred,language='en',input_type='UNSTRUCTURED_NOTICE')
    assert confidence.predict(cal,'share_blocking',english,identity='FR_TEST',population='SOFTWARE_FIXTURE') is None

