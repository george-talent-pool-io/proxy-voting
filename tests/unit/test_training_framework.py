"""Framework integrity tests. Doubles never establish domain-model quality."""
import copy
import json
from pathlib import Path

import pytest
from pydantic import ValidationError

from classifier.preprocessing import source_hash
from semantic_pipeline.schema import PREDICATES
from training.framework.bundle import create_bundle, load_bundle, allowed_path, sha
from training.framework.schema import Example, Provenance, TrainSpec


def example(ident='a', split='TRAIN'):
    text = ('Custodian operating memo: the eligible owner can lodge a ballot on the acquisition resolution.'
            if split == 'TRAIN' else 'This treasury distribution advice merely reports a credit to the cash ledger.')
    target = {k: 'VOTABLE' if k == 'votability' and split == 'TRAIN' else
              'NOT_VOTABLE' if k == 'votability' else 'NO' for k in PREDICATES}
    target.update(evidence={k: [text] if k == 'votability' else [] for k in PREDICATES},
                  deadline_information={'deadline_mentioned': False, 'deadline_text': None}, ambiguities=[])
    return Example(id=ident, text=text, source_hash=source_hash(text), group_id=ident, split=split,
        target=target, provenance=Provenance(origin='AI_AUTHORED', author='test fixture author',
            model_id='test-only-not-an-inference', method='Unit fixture', source_reference='unit-fixture', revision='1'))


@pytest.fixture
def bundle(tmp_path):
    p = tmp_path / 'bundle'
    create_bundle([example(), example('b', 'VALIDATION')], p)
    return p


def spec(tmp_path, backend='LAYA_SDK'):
    return TrainSpec(backend=backend, family='LAYA' if backend == 'LAYA_SDK' else 'QWEN',
                     model_path=str(tmp_path / 'missing-model'), base_model_id='test-only-model', base_revision='test-sha')


def test_ai_labels_require_model_identity_and_cannot_attest_expertise():
    p = example().provenance.model_dump()
    p['model_id'] = None
    with pytest.raises(ValidationError, match='model identity'):
        Provenance.model_validate(p)
    p.update(model_id='test', expert_attested=True)
    with pytest.raises(ValidationError, match='human expertise'):
        Provenance.model_validate(p)
    p.update(origin='EXPERT_REVIEWED', expert_attested=False)
    with pytest.raises(ValidationError, match='expertise attestation'):
        Provenance.model_validate(p)


@pytest.mark.parametrize('change', ['hash', 'evidence', 'positive-without-evidence'])
def test_annotation_rejects_inconsistent_source(change):
    e = example().model_dump(mode='json')
    if change == 'hash': e['source_hash'] = 'wrong'
    if change == 'evidence': e['target']['evidence']['poa_required'] = ['fabricated quotation']
    if change == 'positive-without-evidence': e['target']['share_blocking'] = 'YES'
    with pytest.raises(ValidationError):
        Example.model_validate(e)


def test_bundle_both_backends_have_all_nine_labels_and_no_temporal_target(bundle):
    m, records = load_bundle(bundle)
    assert m['label_origins'] == {'AI_AUTHORED': 2}
    assert m['customer_accuracy'] is None and m['automation_enabled'] is False
    assert not list(bundle.glob('*test*'))
    laya = json.loads((bundle / 'laya-train.jsonl').read_text())
    llm = json.loads((bundle / 'llm-train.jsonl').read_text())
    assert list(laya['questions']) == list(PREDICATES) == list(laya['expected'])
    assert 'deadline_status' not in laya['expected']
    assistant = json.loads(llm['messages'][-1]['content'])
    assert all(k in assistant for k in PREDICATES)
    assert 'confidence' not in assistant and 'deadline_status' not in assistant
    assert records[0].provenance.origin.value == 'AI_AUTHORED'


@pytest.mark.parametrize('identity', ['group', 'exact', 'family', 'normalised', 'near'])
def test_group_exact_family_normalised_and_near_duplicates_cannot_cross_splits(tmp_path, identity):
    a, b = example(), example('b', 'VALIDATION')
    if identity == 'group': b.group_id = a.group_id
    if identity == 'family': a.generation_family = b.generation_family = 'same-generator-family'
    if identity in ('exact', 'normalised', 'near'):
        b.text = a.text if identity == 'exact' else '  ' + a.text + ' \n' if identity == 'normalised' else a.text + ' Supplemental.'
        b.source_hash = source_hash(b.text)
        b.target.evidence.votability = [b.text]
    with pytest.raises(ValueError, match='leakage'):
        create_bundle([a, b], tmp_path / 'blocked-bundle')


@pytest.mark.parametrize('name', ['synthetic_frozen_test_100.csv', 'ANSWER_KEY.csv', 'private/labels.jsonl', 'CALIBRATION.jsonl', 'semantic.json'])
def test_protected_paths_rejected(tmp_path, name):
    with pytest.raises(ValueError, match='Protected'):
        allowed_path(tmp_path / name)


def test_rendered_target_tampering_rejected_even_with_recomputed_checksum(bundle):
    file = bundle / 'laya-train.jsonl'
    row = json.loads(file.read_text()); row['expected']['poa_required'] = 'YES'
    file.write_text(json.dumps(row) + '\n')
    p = bundle / 'manifest.json'; m = json.loads(p.read_text()); m['files'][file.name] = sha(file); p.write_text(json.dumps(m))
    with pytest.raises(ValueError, match='Rendered training content'):
        load_bundle(bundle)


def test_changed_file_is_rejected(bundle):
    (bundle / 'llm-train.jsonl').write_text('{}\n')
    with pytest.raises(ValueError, match='checksum'):
        load_bundle(bundle)


def test_manifest_count_lie_rejected(bundle):
    p = bundle / 'manifest.json'; m = json.loads(p.read_text()); m['counts']['TRAIN'] = 3000; p.write_text(json.dumps(m))
    with pytest.raises(ValueError, match='counts'):
        load_bundle(bundle)


def test_provenance_cannot_be_relabelled_human_in_manifest(bundle):
    p = bundle / 'manifest.json'; m = json.loads(p.read_text()); m['label_origins'] = {'EXPERT_REVIEWED': 2}; p.write_text(json.dumps(m))
    with pytest.raises(ValueError, match='provenance'):
        load_bundle(bundle)


def test_bundle_never_overwrites_history(bundle):
    with pytest.raises(FileExistsError):
        create_bundle([example(), example('b', 'VALIDATION')], bundle)


def test_chat_loss_masks_prompt_and_never_truncates():
    from training.framework.trainers import encode_chat
    class Tokenizer:
        def apply_chat_template(self, messages, **kwargs):
            return [1, 2, 3] if kwargs['add_generation_prompt'] else [1, 2, 3, 4, 5]
    assert encode_chat(Tokenizer(), [{}, {}], 10)['labels'] == [-100, -100, -100, 4, 5]
    with pytest.raises(ValueError, match='no truncation'):
        encode_chat(Tokenizer(), [{}, {}], 4)
    class BrokenTemplate(Tokenizer):
        def apply_chat_template(self, messages, **kwargs):
            return [6, 7] if kwargs['add_generation_prompt'] else [1, 2, 3]
    with pytest.raises(ValueError, match='masked assistant prefix'):
        encode_chat(BrokenTemplate(), [{}, {}], 10)


def test_job_preparation_is_not_training_and_rejects_missing_weights(bundle, tmp_path):
    from training.framework.jobs import prepare, status
    output = tmp_path / 'job'
    plan = prepare(bundle, spec(tmp_path), output)
    assert not plan['model_execution_started']
    assert status(output)['state'] == 'BLOCKED'
    assert not (output / 'checkpoint').exists()
    assert 'LOCAL_TRAINABLE_CHECKPOINT_MISSING' in plan['preflight']['reasons']


def test_execution_refuses_active_benchmark_without_loading_models(bundle, tmp_path, monkeypatch):
    from training.framework import jobs
    output = tmp_path / 'job'
    jobs.prepare(bundle, spec(tmp_path), output)
    monkeypatch.setattr(jobs, 'active_experiments', lambda: [{'pid': 123, 'command': 'explicit unit double'}])
    with pytest.raises(ValueError, match='Timed model experiment active'):
        jobs.execute(output)
    assert jobs.status(output)['state'] == 'FAILED'
    assert not (output / 'checkpoint').exists()


def test_reprepared_sources_and_dataset_are_checked(bundle, tmp_path):
    from training.framework import jobs
    output = tmp_path / 'job'; jobs.prepare(bundle, spec(tmp_path), output)
    (bundle / 'manifest.json').write_text('{}')
    with pytest.raises(ValueError, match='dataset changed'):
        jobs.verify_plan(output)


def test_model_spec_cannot_replace_laya_with_llm(tmp_path):
    value = spec(tmp_path).model_dump(); value['family'] = 'QWEN'
    with pytest.raises(ValidationError, match='official SDK'):
        TrainSpec.model_validate(value)


def test_official_laya_backend_receives_train_and_separate_validation(bundle, tmp_path, monkeypatch):
    import laya.train
    import training.framework.trainers as trainers
    from training.framework.trainers import train_laya
    calls = []
    def finetune(data, model, output, config, device):
        assert model != spec(tmp_path).model_path  # SDK gets a private working copy.
        calls.append((data, config))
        Path(output).mkdir()
        return {'kind': 'explicit trainer contract double, not a real model', 'updates': 1}
    monkeypatch.setattr(laya.train, 'finetune', finetune)
    monkeypatch.setattr(trainers, 'validate_laya_encoding', lambda *args: None)
    monkeypatch.setattr(trainers, 'validate_laya_reload', lambda *args: {'passed': True, 'scope': 'reload contract double'})
    Path(spec(tmp_path).model_path).mkdir()
    result = train_laya(bundle, tmp_path / 'checkpoint', spec(tmp_path))
    assert calls[0][0].endswith('laya-train.jsonl')
    config = calls[0][1]
    assert config.eval_data.endswith('laya-validation.jsonl')
    assert config.calib_frac == config.calib_max == 0
    assert result['reload_parity']['passed']


def test_job_registers_artifact_then_validation_scoring_preserves_predictions(bundle, tmp_path, monkeypatch):
    from training.framework import jobs, trainers
    monkeypatch.setattr(jobs, 'WORKSPACE', tmp_path / 'isolated-training-workspace')
    from training.framework.runtime import verify_checkpoint
    from training.framework.evaluate import evaluate_validation
    base = tmp_path / 'base'; base.mkdir()
    (base / 'model.safetensors').write_bytes(b'explicit unit-only fake model')
    (base / 'rl_agent_config.json').write_text('{}')
    value = spec(tmp_path).model_dump(); value['model_path'] = str(base)
    root = tmp_path / 'job'
    jobs.prepare(bundle, value, root)
    monkeypatch.setattr(jobs, 'active_experiments', lambda: [])
    def fake_train(bundle, output, config):
        output.mkdir(); (output / 'model.safetensors').write_bytes(b'explicit unit-only trained artifact double')
        return {'scope': 'CONTRACT_DOUBLE_NOT_REAL_TRAINING'}
    monkeypatch.setattr(trainers, 'train_laya', fake_train)
    model = jobs.execute(root)
    assert model['status'] == 'EXPERIMENTAL_NOT_PROMOTED' and model['calibrator'] is None
    assert jobs.status(root)['state'] == 'COMPLETED'
    verify_checkpoint(root)
    class ValidationDouble:
        def analyse(self, text):
            from semantic_pipeline.decision import decide
            factors = {k: {'value': 'NOT_VOTABLE' if k == 'votability' else 'NO', 'scores': {},
                           'confidence': None} for k in PREDICATES}
            return {'reconciliation': {'predicates': factors, 'conflicts': []},
                    'deadline': {'status': 'UNKNOWN'}, 'decision': decide(factors, {'status': 'UNKNOWN'}),
                    'escalation': {'reasons': []}, 'latencies': {'total_ms': .1}}
    result = evaluate_validation(root, tmp_path / 'validation-result', model=ValidationDouble())
    assert result['assertions'] == 9 and result['correct_assertions'] == 9
    assert result['final_status_labelled_cases'] == 0
    saved = json.loads((tmp_path / 'validation-result/predictions.jsonl').read_text())
    assert 'expected' not in saved and saved['id'] == 'b'
    assert result['label_origins'] == {'AI_AUTHORED': 1}
    assert result['training_label_origins'] == {'AI_AUTHORED': 2}
    (root / 'checkpoint/model.safetensors').write_bytes(b'changed')
    with pytest.raises(ValueError, match='checkpoint files changed'):
        verify_checkpoint(root)


def test_laya_length_guard_prevents_silent_sdk_truncation(bundle, tmp_path, monkeypatch):
    import transformers
    from training.framework.trainers import validate_laya_encoding
    class Tokenizer:
        def encode(self, *a, **k): return list(range(1000))
    monkeypatch.setattr(transformers.AutoTokenizer, 'from_pretrained', lambda *a, **k: Tokenizer())
    value = spec(tmp_path).model_dump(); value['max_length'] = 512
    with pytest.raises(ValueError, match='complete source plus head exceeds context'):
        validate_laya_encoding(bundle, TrainSpec.model_validate(value))
