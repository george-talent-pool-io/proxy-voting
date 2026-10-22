import json
import pytest
from pydantic import ValidationError
from training.framework.schema import TrainSpec
from training.framework.trainers import laya_training_input
from training.framework.bundle import sha
from tests.unit.test_training_framework import bundle, spec


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
