"""MLX configuration and shared decision path without importing a GPU model."""
import json
from pathlib import Path

import pytest
from semantic_pipeline.schema import PREDICATES
from training.framework.schema import TrainSpec
from training.framework.bundle import laya_questions


def test_mlx_spec_is_separate_from_generic_transformers():
    s = TrainSpec(backend='MLX_QLORA', family='QWEN', model_path='weights', base_model_id='declared-base',
                  base_revision='pinned', runtime_python='/local/python', lora_layers=1, device='mps')
    assert s.backend == 'MLX_QLORA' and s.lora_layers == 1


def test_qwen_direct_training_masks_actual_empty_thinking_prefix():
    from training.framework.trainers import encode_chat
    class QwenTemplate:
        eos_token_id = 9
        def apply_chat_template(self, messages, **kwargs):
            if not kwargs['tokenize']: return 'prefix<think>\n\n</think>\n\n'
            return [1, 2, 3] if kwargs['add_generation_prompt'] else [1, 8, 7]
        def encode(self, text, **kwargs): return [4, 5]
    result = encode_chat(QwenTemplate(), [{'role': 'user'}, {'role': 'assistant', 'content': '{}'}], 100)
    assert result['input_ids'] == [1, 2, 3, 4, 5, 9]
    assert result['labels'] == [-100, -100, -100, 4, 5, 9]


def test_external_runtime_preserves_venv_python_symlink(tmp_path, monkeypatch):
    import sys
    from types import SimpleNamespace
    from training.framework import trainers
    link = tmp_path / 'venv-python'; link.symlink_to(sys.executable)
    seen = []
    def run(command, **kwargs):
        seen.append(command)
        return SimpleNamespace(stdout='{"mlx":"test","mlx_lm":"test","metal_available":true}')
    monkeypatch.setattr(trainers.subprocess, 'run', run)
    assert trainers.probe_mlx(str(link))['metal_available']
    assert seen[0][0] == str(link.absolute())


def test_pinned_reference_facts_take_precedence_and_remain_traceable(tmp_path):
    from training.framework.runtime import RegisteredModel
    from iso_adapter.benchmark import fin
    model = RegisteredModel.__new__(RegisteredModel)
    model.root = tmp_path
    (tmp_path / 'model-manifest.json').write_text('{}')
    model.spec = TrainSpec(backend='LAYA_SDK', family='LAYA', model_path='unused', base_model_id='contract', base_revision='contract')
    model.plan = {'job_id': 'explicit-unit-contract'}
    model.questions = laya_questions()
    class Agent:
        def predict_batch(self, states, questions, **kwargs):
            answers = {}
            for k, q in questions.items():
                choice = 'UNCERTAIN' if k == 'votability' else 'NO'
                answers[k] = {'choice': choice, 'probabilities': {v: .98 if v == choice else .01 for v in q['criteria']}}
            return [{'answers': answers, 'usage': {'truncated': False}}]
    model.agent = Agent()
    text = fin(':16R:CAOPTN\n:22F::CAOP//PROX\n:98E::RDDT//20261020170000,000/00\n:16S:CAOPTN')
    result = model.analyse(text)
    assert result['parser']['parser'] == 'PROWIDE'
    assert result['predicates']['votability']['value'] == 'VOTABLE'
    assert result['predicates']['votability']['semantic_diagnostic']['value'] == 'UNCERTAIN'
    assert result['deadline']['status'] == 'OPEN'
    assert result['decision']['classification'] == 'VOTABLE'
    assert not result['automation_enabled']  # Customer permission is checked by the worker, not semantic rules.
    span = result['predicates']['votability']['evidence'][0]
    assert text[span['start']:span['end']] == span['text']


@pytest.mark.parametrize('second_valid', [True, False])
@pytest.mark.parametrize('fenced', [True, False])
def test_registered_mlx_schema_repair_is_bounded_and_keeps_review(tmp_path, second_valid, fenced):
    from training.framework.runtime import RegisteredModel
    model = RegisteredModel.__new__(RegisteredModel)
    model.root = tmp_path
    (tmp_path / 'model-manifest.json').write_text('{}')
    (tmp_path / 'semantic-prompt.txt').write_text('Classification contract fixture only.')
    model.plan = {'job_id': 'repair-contract-only', 'bundle': str(tmp_path)}
    model.spec = TrainSpec(backend='MLX_QLORA', family='QWEN', model_path='unused', base_model_id='contract-only', base_revision='contract')
    valid = {k: 'NOT_VOTABLE' if k == 'votability' else 'NO' for k in PREDICATES}
    valid.update(evidence={k: [] for k in PREDICATES}, ambiguities=[],
                 deadline_information={'deadline_mentioned': False, 'deadline_text': None})
    calls = []
    class Worker:
        def generate(self, messages):
            calls.append(messages)
            answer = json.dumps(valid) if len(calls) == 2 and second_valid else '{bad-json'
            if fenced and len(calls) == 2: answer = '```json\n' + answer + '\n```'
            return {'answer': answer, 'latency_ms': .1}
    model.worker = Worker()
    result = model.analyse('Custody ledger balance advice.', use_iso=False)
    assert len(calls) == 2
    assert result['llm']['schema_handling']['repair_attempts'] == 1
    assert result['llm']['valid'] is second_valid
    assert not result['automation_enabled']
    if not second_valid:
        assert result['decision']['manual_review_required']
        assert result['llm']['raw_output'] is None
        assert 'LLM_OUTPUT_SCHEMA_FAILURE' in result['reconciliation']['conflicts']
