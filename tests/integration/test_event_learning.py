"""Real Prowide + SQLite lifecycle; model/queue doubles are explicitly identified."""
import json
import sqlite3
from pathlib import Path

import pytest

from scripts.build_event_learning_corpus import message, specification
from training.framework import events, event_data, jobs, queue, selection, comparison
from training.framework.bundle import sha, write, load_bundle


@pytest.fixture
def learning(db, tmp_path, monkeypatch):
    from apps.api import training_views
    monkeypatch.setattr(jobs, 'WORKSPACE', tmp_path / 'workspace')
    monkeypatch.setattr(training_views, 'WORKSPACE', jobs.WORKSPACE)
    monkeypatch.setattr(jobs, 'active_experiments', lambda: [])
    return Path(db)


def ingest(db, seme='N1', *, corp='CORP1', raw=None, split='TRAIN', group='family1', **kw):
    raw = raw or message(seme, corp, 'NEWM', 'Shareholders can vote. No share blocking is required.')
    return events.ingest(raw, sender='TEST-SENDER', source_type='STANDARDS_DERIVED_SYNTHETIC',
                         group_id=group, family=group, split=split, source_reference='Explicit engineering fixture', database=db, **kw)


def annotate(db, event, *, revision=None, text='Shareholders can vote.'):
    view = events.get(event, db)
    target = {k: 'VOTABLE' if k == 'votability' else 'NO' for k in events.PREDICATES}
    target.update(evidence={k: [text] if k == 'votability' else [] for k in events.PREDICATES},
                  deadline_information={'deadline_mentioned': False, 'deadline_text': None}, ambiguities=[])
    return events.review(event, {'snapshot_hash': view['snapshot_hash'], 'expected_revision': revision, 'target': target,
        'provenance': {'origin': 'AI_REVIEWED', 'author': 'Explicit test annotation', 'model_id': 'TEST_DOUBLE',
                       'method': 'Test fixture, not a human review', 'source_reference': event, 'revision': str(revision)}}, db)


def test_real_prowide_link_replacement_cancellation_and_exact_source(learning):
    first = ingest(learning)
    eid = first['event_id']
    ingest(learning, 'S1', raw=message('S1', 'CORP1', 'NEWM', 'Old POA terms apply.', mt='MT568', prev='N1'))
    old = events.get(eid, learning)
    assert len(old['operative_message_ids']) == 2
    replacement = message('R1', 'CORP1', 'REPL', 'Shareholders can vote. No POA is required.', prev='N1')
    ingest(learning, 'R1', raw=replacement)
    current = events.get(eid, learning)
    assert 'Old POA' not in current['current_text']
    assert current['messages'][0]['raw_source'] == first['raw_source']
    assert current['messages'][-1]['raw_source'] == replacement
    assert any(f['name'] == 'rddt' and not f['current'] for f in current['facts'])
    links = events.evidence_links(current, 'No POA is required.')
    assert links and replacement[links[0]['start']:links[0]['end']] == links[0]['text']
    assert not events.evidence_links(current, 'Old POA terms apply.')
    stale = ingest(learning, 'STALE', raw=message('STALE', 'CORP1', 'REPL', 'Wrong stale replacement.', prev='N1'))
    assert stale['state'] == 'QUARANTINED'
    ingest(learning, 'C1', raw=message('C1', 'CORP1', 'CANC', 'Meeting cancelled.', prev='R1'))
    cancelled = events.get(eid, learning)
    assert cancelled['cancelled'] and not cancelled['current_text']
    assert len(cancelled['messages']) == 5


def test_narrative_replacement_only_replaces_that_supplement_and_instructions_do_not_cancel(learning):
    eid = ingest(learning)['event_id']
    ingest(learning, 'S1', raw=message('S1', 'CORP1', 'NEWM', 'Shares will be blocked.', mt='MT568', prev='N1'))
    ingest(learning, 'S2', raw=message('S2', 'CORP1', 'REPL', 'No blocking applies.', mt='MT568', prev='S1'))
    value = events.get(eid, learning)
    assert 'Shares will be blocked.' not in value['current_text'] and 'No blocking applies.' in value['current_text']
    ingest(learning, 'S3', raw=message('S3', 'CORP1', 'NEWM', 'Registration is required.', mt='MT568', prev='S2'))
    value = events.get(eid, learning)
    assert 'No blocking applies.' in value['current_text'] and 'Registration is required.' in value['current_text']
    assert value['policy'].endswith('supplement-additions-v2')
    r = ingest(learning, 'I1', raw=message('I1', 'CORP1', 'CANC', 'Cancel my instruction.', mt='MT565', prev='N1'))
    assert r['state'] == 'OBSERVATION' and not events.get(eid, learning)['cancelled']


def test_recovery_is_not_authoritative_and_ordinary_notice_bypasses_parser(learning):
    r = ingest(learning, raw=':20C::SEME//N1\n:70E::ADTX//Shareholders can vote.', declared={'corp': 'CORP1', 'seme': 'N1'})
    assert r['payload']['parser'] == 'LENIENT_RECOVERY' and r['state'] == 'QUARANTINED'
    from tests.unit.test_learning_comparison import result
    class Model:
        def analyse(self, text, **kwargs):
            assert kwargs['structured_context'] == {} and 'Shareholders can vote.' in text
            return result()
    trace = events.classify(r['event_id'], 'explicit-double', reference='2026-10-17T12:00:00+00:00', database=learning, model=Model())
    assert trace['payload']['result']['event_context_kind'] == 'RECOVERED_REVIEW_CONTEXT'
    assert trace['payload']['result']['decision']['classification'] == 'UNCERTAIN_MANUAL_REVIEW'
    r = ingest(learning, 'U1', corp='PLAIN', raw='Ordinary notice: shareholders can vote.', group='plain', declared={'corp': 'PLAIN', 'seme': 'U1'})
    assert r['payload']['parser'] == 'NOT_APPLICABLE' and r['state'] == 'APPLIED'


def test_identity_collision_sender_scope_and_split_freeze(learning):
    a = ingest(learning)
    assert ingest(learning)['id'] == a['id']
    with pytest.raises(ValueError, match='collision'): ingest(learning, raw=message('N1', 'CORP1', 'NEWM', 'Changed'))
    with pytest.raises(ValueError, match='frozen'): ingest(learning, 'N2', split='VALIDATION')
    with pytest.raises(ValueError, match='leakage'): ingest(learning, 'N3', corp='OTHER', split='VALIDATION')
    with sqlite3.connect(learning) as c:
        with pytest.raises(sqlite3.IntegrityError): c.execute('DELETE FROM learning_messages')


def test_review_revision_evidence_origin_and_previous_prediction(learning):
    eid = ingest(learning)['event_id']
    r = annotate(learning, eid)
    assert r['payload']['validation_type'] == 'AI_ASSISTED_NOT_HUMAN_GOLD'
    assert r['payload']['evidence_links']['votability'][0]['valid']
    with pytest.raises(ValueError, match='revision conflict'): annotate(learning, eid)
    r2 = annotate(learning, eid, revision=r['id'])
    assert r2['previous_revision'] == r['id']
    with pytest.raises(ValueError, match='exact operative'): annotate(learning, eid, revision=r2['id'], text='fabricated quotation')
    body = r2['payload']; body['provenance']['expert_attested'] = True
    with pytest.raises(ValueError, match='human expertise'): events.review(eid, body, learning)


def test_current_snapshot_review_guard(learning):
    eid = ingest(learning)['event_id']; old = events.get(eid, learning)
    r = annotate(learning, eid)
    ingest(learning, 'R1', raw=message('R1', 'CORP1', 'REPL', 'Shareholders can vote.', prev='N1'))
    value = {k: v for k, v in r['payload'].items() if k in events.Review.model_fields}
    value['snapshot_hash'] = old['snapshot_hash']
    with pytest.raises(ValueError, match='Event changed'): events.review(eid, value, learning)


def test_frozen_registry_blocks_renamed_hash_and_group(learning, tmp_path):
    eid = ingest(learning, split='FROZEN_TEST')['event_id']; annotate(learning, eid)
    root = tmp_path / 'dataset'; event_data.freeze_dataset(root, learning)
    from tests.unit.test_training_framework import example
    e = example(); e.text = events.get(eid, learning)['current_text']; e.source_hash = source_hash(e.text)
    with pytest.raises(ValueError, match='Protected event'): event_data.reject_protected([e])
    e = example(); e.generation_family = 'family1'
    with pytest.raises(ValueError, match='Protected event'): event_data.reject_protected([e])
    m, rows = event_data.load_inputs(root, 'FROZEN_TEST')
    assert 'target' not in rows[0] and 'expected_final_status' not in rows[0]
    (root / 'inputs.jsonl').write_text('tampered')
    with pytest.raises(ValueError, match='changed'): event_data.load_inputs(root, 'FROZEN_TEST')


def test_event_review_export_only_reads_development_roles(learning, tmp_path):
    for f, role in [(0, 'TRAIN'), (1, 'VALIDATION'), (2, 'FROZEN_TEST'), (3, 'CALIBRATION')]:
        spec = specification(f, 1)
        r = ingest(learning, f'N{f}', corp=f'CORP{f}', raw=message(f'N{f}', f'CORP{f}', 'NEWM', spec['narrative']), split=role, group=f'F{f}')
        v = events.get(r['event_id'], learning)
        events.review(v['id'], {'snapshot_hash': v['snapshot_hash'], 'target': spec['target'],
            'provenance': {'origin': 'AI_AUTHORED', 'author': 'Fixture', 'model_id': 'TEST_DOUBLE', 'method': 'Construction', 'source_reference': 'test', 'revision': '1'}}, learning)
    result = event_data.export_reviews(tmp_path / 'bundle', learning)
    assert result['counts'] == {'TRAIN': 1, 'VALIDATION': 1}
    assert result['source_manifest']['held_out_answers_opened'] is False


def test_job_cancel_is_durable_and_no_implicit_resume(learning, tmp_path, monkeypatch):
    from tests.unit.test_training_framework import example
    from training.framework.bundle import create_bundle
    from training.framework.schema import TrainSpec
    bundle = tmp_path / 'bundle'; create_bundle([example(), example('b', 'VALIDATION')], bundle)
    path = jobs.WORKSPACE / 'jobs/job1'
    jobs.prepare(bundle, TrainSpec(backend='LAYA_SDK', family='LAYA', model_path='missing', base_model_id='test', base_revision='test'), path)
    # Contract fixture bypasses preflight ONLY to verify queue state, never trains.
    monkeypatch.setattr(jobs, 'verify_plan', lambda p: (path, {'preflight': {'ready': True}}))
    monkeypatch.setattr(jobs, 'status', lambda p: {'state': 'PREPARED'})
    r = queue.submit('job1', learning)
    queue.cancel(r['id'], learning)
    assert queue.listing(learning)[0]['state'] == 'CANCELLED'
    queue.run(learning)
    assert queue.listing(learning)[0]['state'] == 'CANCELLED'
    assert not (path / 'execution.lock').exists()


def test_dead_worker_becomes_interrupted_and_is_not_requeued(learning):
    queue.tables(learning)
    with store.connect(learning) as c:
        c.execute("INSERT INTO learning_tasks VALUES('t','j','RUNNING','x','x',999999,1,0,'{}')")
    assert queue.listing(learning)[0]['state'] == 'INTERRUPTED'
    assert queue.listing(learning)[0]['detail']['automatic_resume'] is False


def test_learning_api_default_off_and_labelled_holdouts_hidden(client, learning):
    eid = ingest(learning, split='FROZEN_TEST')['event_id']; annotate(learning, eid)
    value = client.get('/api/learning/events/' + eid).json()
    assert value['held_out_labels_hidden'] and not value['reviews']
    assert client.post('/api/learning/dispatch').status_code == 403
    assert client.post('/api/learning/events/' + eid + '/analyse', json={}).status_code == 403
    assert client.get('/api/learning/status').json()['automation_enabled'] is False


def test_current_deadline_and_prediction_source_links_reach_review(learning):
    eid = ingest(learning, raw=message('N1', 'CORP1', 'NEWM', 'Old terms.', date='20250901170000'))['event_id']
    ingest(learning, 'R1', raw=message('R1', 'CORP1', 'REPL', 'Shareholders can vote.', prev='N1', date='20261124170000'))
    from tests.unit.test_learning_comparison import result
    from semantic_pipeline.evidence import verify_evidence
    seen = []
    class Model:
        def analyse(self, text, **kwargs):
            seen.append(kwargs)
            r = result(); r['predicates']['votability']['evidence'] = [verify_evidence(text, 'Shareholders can vote.')]
            return r
    execution = events.classify(eid, 'explicit-test-job', reference='2026-10-17T12:00:00+00:00', database=learning, model=Model())
    assert seen[0]['use_iso'] is False and seen[0]['deadline_override']['status'] == 'OPEN'
    assert execution['payload']['result']['predicates']['votability']['evidence'][0]['event_source_links'][0]['seme'] == 'R1'
    r = annotate(learning, eid)
    assert r['payload']['previous_prediction']['id'] == execution['id']
    assert r['payload']['ai_exact_match'] is True
    assert all(v['confidence'] is None for v in execution['payload']['result']['confidence'].values())


def test_malformed_external_identity_is_validation_error(client):
    body = {'raw': 'An ordinary notice', 'sender': 'test', 'source_type': 'USER_PROVIDED',
            'source_reference': 'test', 'family': 'a', 'group_id': 'a', 'split': 'TRAIN',
            'declared': {'corp': 7, 'seme': ['bad']}}
    assert client.post('/api/learning/messages', json=body).status_code == 422


def test_inference_failure_is_persisted_without_invented_prediction(learning):
    eid = ingest(learning)['event_id']
    class Broken:
        def analyse(self, *a, **kw): raise ValueError('Context limit; source was not truncated')
    r = events.classify(eid, 'explicit-broken-double', reference='2026-10-17T12:00:00+00:00', database=learning, model=Broken())
    assert r['payload']['result']['execution_error']['type'] == 'ValueError'
    assert r['payload']['result']['decision']['classification'] == 'UNCERTAIN_MANUAL_REVIEW'
    assert events.get(eid, learning)['executions'][-1]['id'] == r['id']
    assert all(not p['scores'] for p in r['payload']['result']['predicates'].values())


def test_corpus_rebuild_preserves_sources_reviews_and_input_hashes(learning, tmp_path):
    from scripts.build_event_learning_corpus import build
    a = build(learning, tmp_path / 'first-version')
    b = build(learning, tmp_path / 'second-version')
    assert a['roles'] == b['roles'] == {'TRAIN': 96, 'VALIDATION': 32, 'CALIBRATION': 16, 'FROZEN_TEST': 16}
    assert a['input_sha256'] == b['input_sha256']
    with store.connect(learning) as c:
        assert c.execute('SELECT count(*) FROM learning_messages').fetchone()[0] == 640
        assert c.execute('SELECT count(*) FROM learning_reviews').fetchone()[0] == 160


from classifier.preprocessing import source_hash
from apps.api import store
