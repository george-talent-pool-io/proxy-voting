"""Opt-in real CPU LoRA training; random tiny model, NOT Qwen/GLM quality."""
import json
import os
from pathlib import Path

import pytest

pytestmark = pytest.mark.skipif(os.environ.get('RUN_TRAINER_SMOKE') != '1',
                               reason='Explicit tiny CPU trainer smoke test; optional PEFT environment')


def test_real_cpu_lora_training_and_adapter_reload(tmp_path):
    import torch
    from tokenizers import Tokenizer, models, pre_tokenizers
    from transformers import PreTrainedTokenizerFast, GPT2Config, GPT2LMHeadModel
    from tests.unit.test_training_framework import example
    from training.framework.bundle import create_bundle, messages, PROMPT
    from training.framework.schema import TrainSpec
    from training.framework.trainers import train_peft, versions
    torch.set_num_threads(1)
    examples = [example(), example('b', 'VALIDATION')]
    bundle = tmp_path / 'bundle'
    create_bundle(examples, bundle)
    text = ' '.join(m['content'] for e in examples for m in messages(e, PROMPT.read_text()))
    vocab = {token: i for i, token in enumerate(['[UNK]', '[EOS]', '[PAD]', 'system:', 'user:', 'assistant:'] + sorted(set(text.split()) - {'[UNK]', '[EOS]', '[PAD]', 'system:', 'user:', 'assistant:'}))}
    tokenizer = Tokenizer(models.WordLevel(vocab, unk_token='[UNK]'))
    tokenizer.pre_tokenizer = pre_tokenizers.WhitespaceSplit()
    tokenizer = PreTrainedTokenizerFast(tokenizer_object=tokenizer, unk_token='[UNK]',
                eos_token='[EOS]', pad_token='[PAD]')
    tokenizer.chat_template = "{% for message in messages %}{{ message['role'] + ': ' + message['content'] + ' ' }}{% endfor %}{% if add_generation_prompt %}{{ 'assistant: ' }}{% endif %}"
    model = GPT2LMHeadModel(GPT2Config(vocab_size=len(vocab), n_positions=8192,
                            n_embd=16, n_layer=1, n_head=2, bos_token_id=1, eos_token_id=1, pad_token_id=2))
    base = tmp_path / 'tiny-random-base'
    model.save_pretrained(base); tokenizer.save_pretrained(base)
    del model
    spec = TrainSpec(backend='TRANSFORMERS_PEFT', family='OTHER_CAUSAL_LM', model_path=str(base),
                    base_model_id='LOCAL_RANDOM_GPT2_16D_TEST_ONLY', base_revision='created-in-test',
                    device='cpu', dtype='float32', max_steps=1, max_length=8192,
                    gradient_accumulation=1, target_modules=['c_attn'], lora_rank=2, lora_alpha=4)
    result = train_peft(bundle, tmp_path / 'adapter', spec)
    assert result['optimiser_steps'] == 1 and result['trainable_parameters'] > 0
    assert result['reload_parity']['passed']
    assert (tmp_path / 'adapter/adapter_model.safetensors').exists()
    assert result['curve'][0]['validation_token_cross_entropy'] > 0
    receipt = {'scope': 'REAL TRAINER EXECUTION ONLY; random tiny CPU model, not Qwen/GLM compatibility or quality',
               'versions': versions(), 'result': result, 'automation_enabled': False,
               'customer_accuracy': None, 'weights_downloaded': False}
    Path('artifacts').mkdir(exist_ok=True)
    Path('artifacts/training-framework-real-smoke.json').write_text(json.dumps(receipt, indent=2))
