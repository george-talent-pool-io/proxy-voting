import json
import pytest
from pydantic import ValidationError
from training.framework.schema import TrainSpec
from training.framework.trainers import laya_training_input
from training.framework.bundle import sha
from tests.unit.test_training_framework import bundle, spec, example


def test_weighting_uses_only_training_questions_and_preserves_input_bytes(bundle,tmp_path):
    s=spec(tmp_path).model_copy(update={'laya_task_multipliers':{'votability':4}})
    original={p.name:sha(p) for p in bundle.iterdir() if p.is_file()}
    path,receipt=laya_training_input(bundle,tmp_path/'checkpoint',s)
    rows=[json.loads(l) for l in path.read_text().splitlines()]
    assert len(rows)==4 and receipt['unique_training_notices']==1
    assert receipt['effective_question_items']==12
    assert all(r['state']==rows[0]['state'] for r in rows)
    assert all(set(r['questions'])=={'votability'} for r in rows[1:])
    assert {p.name:sha(p) for p in bundle.iterdir() if p.is_file()}==original
    assert receipt['validation_resampled'] is False


@pytest.mark.parametrize('weights',[{'votability':True},{'votability':0},{'votability':9},{'invented':2}])
def test_invalid_task_weights_are_rejected(tmp_path,weights):
    with pytest.raises(ValidationError):
        TrainSpec.model_validate({**spec(tmp_path).model_dump(),'laya_task_multipliers':weights})


def test_evidence_training_projects_only_annotated_train_predicates(bundle,tmp_path):
    s=spec(tmp_path).model_copy(update={'laya_evidence_passage_multiplier':3})
    original={p.name:sha(p) for p in bundle.iterdir() if p.is_file()}
    path,receipt=laya_training_input(bundle,tmp_path/'checkpoint',s)
    rows=[json.loads(l) for l in path.read_text().splitlines()]
    assert receipt['unique_training_notices']==1
    assert receipt['evidence_training']['unique_passage_questions']==1
    assert receipt['evidence_training']['effective_question_items']==3
    assert len(rows)==4 and all(set(r['questions'])=={'votability'} for r in rows[1:])
    assert all(r['expected']=={'votability':'VOTABLE'} for r in rows[1:])
    provenance=[json.loads(s) for s in (tmp_path/'laya-evidence-training-provenance.jsonl').read_text().splitlines()]
    assert {r['source_id'] for r in provenance}=={'a'}
    assert {r['role'] for r in provenance}=={'TRAIN'}
    assert {p.name:sha(p) for p in bundle.iterdir() if p.is_file()}==original


def test_context_dependent_evidence_cannot_be_projected_to_conflicting_labels(bundle,tmp_path,monkeypatch):
    from training.framework import bundle as module
    a=example();b=a.model_copy(deep=True);b.id='conflicting-context';b.target.votability='NOT_VOTABLE'
    monkeypatch.setattr(module,'load_bundle',lambda p:({},[a,b]))
    with pytest.raises(ValueError,match='conflicting labels'):
        laya_training_input(bundle,tmp_path/'checkpoint',spec(tmp_path).model_copy(update={'laya_evidence_passage_multiplier':1}))


@pytest.mark.parametrize('multiplier',[-1,9,True,1.5])
def test_invalid_evidence_training_multiplier_rejected(tmp_path,multiplier):
    with pytest.raises(ValidationError):
        TrainSpec.model_validate({**spec(tmp_path).model_dump(),'laya_evidence_passage_multiplier':multiplier})


def test_llm_cannot_silently_enable_laya_projection(tmp_path):
    with pytest.raises(ValidationError,match='Evidence passage training'):
        TrainSpec.model_validate({**spec(tmp_path,'TRANSFORMERS_PEFT').model_dump(),'laya_evidence_passage_multiplier':1})
