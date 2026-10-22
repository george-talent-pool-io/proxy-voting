import copy
from training.framework.mlx_process import same_serving_condition
from training.framework.schema import TrainSpec


def test_new_laya_only_empty_default_does_not_break_pinned_llm_request():
    spec=TrainSpec(backend='MLX_QLORA',family='QWEN',model_path='PINNED_LOCAL_MODEL',base_model_id='PINNED_QWEN',base_revision='IMMUTABLE').model_dump()
    current={'spec':spec,'checkpoint':None};old=copy.deepcopy(current);old['spec'].pop('laya_task_multipliers')
    assert same_serving_condition(old,current)
    changed=copy.deepcopy(old);changed['spec']['generation_tokens']=4096
    assert not same_serving_condition(changed,current)
    changed=copy.deepcopy(old);changed['checkpoint']='OTHER_WEIGHTS'
    assert not same_serving_condition(changed,current)
    changed=copy.deepcopy(old);changed['spec']['invented_field']=True
    assert not same_serving_condition(changed,current)
