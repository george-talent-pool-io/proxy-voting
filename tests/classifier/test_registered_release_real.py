"""Opt-in REAL registered Laya/Qwen release inference, never a model double.

RUN_RELEASE_REAL_MODEL=1 uv run pytest tests/classifier/test_registered_release_real.py -q
Requires the completed release-learning-v1 campaign; never trains implicitly.
"""
import os
import pytest

pytestmark = [pytest.mark.model, pytest.mark.local_llm,
              pytest.mark.skipif(os.environ.get('RUN_RELEASE_REAL_MODEL') != '1', reason='Explicit real release execution required')]


@pytest.fixture(scope='module')
def actual_release():
    from training.framework import jobs, campaigns, releases
    from training.framework.event_data import load_inputs
    from training.framework.resources import model_resource
    state = campaigns.status(jobs.member('campaigns', 'release-learning-v1'))
    assert state['state'] == 'COMPLETED'
    root = jobs.member('releases', state['report']['candidates']['CASCADE_CONSERVATIVE'])
    _, inputs = load_inputs(jobs.member('event-datasets', state['plan']['spec']['dataset_id']), 'VALIDATION')
    row = inputs[0]
    from iso_adapter.facts import semantic_facts, deadline
    struct = row['active_structure']; explicit = deadline(struct, state['plan']['spec']['reference'])
    with model_resource('real-model-release-integration'):
        model = releases.ReleaseModel(root)
        try:
            result = model.analyse(row['text'], use_iso=False, structured_context=semantic_facts(struct),
                                   deadline_override=explicit, reference=state['plan']['spec']['reference'])
        finally: model.close()
    return row['text'], result


def test_real_registered_specialist_and_local_generative_model_execute(actual_release):
    _, r = actual_release
    assert r['laya']['passage_predictions'] and r['llm_stage']['llm']['invoked']
    assert r['release_identity'] and r['checkpoint_manifest_sha256']
    assert r['decision']['manual_review_required'] and not r['automation_enabled']


def test_real_release_has_native_scores_exact_evidence_and_honest_confidence(actual_release):
    text, r = actual_release
    for key, passages in r['laya']['passage_predictions'].items():
        for p in passages:
            assert abs(sum(p['scores'].values()) - 1) < .002
        for e in r['predicates'][key].get('evidence', []):
            if e.get('valid') and not str(r['predicates'][key].get('source')).startswith('PROWIDE'):
                assert e['text'] in text
    assert all(c['confidence'] is None for c in r['confidence'].values())  # tiny real cohort correctly refuses calibration
