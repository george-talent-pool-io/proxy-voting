"""Integrity checks on persisted model experiments; no fabricated semantic passes."""
import hashlib,json,math
from pathlib import Path
import pytest
ROOT=Path('data/experiments/iso-hybrid-v1')

@pytest.mark.parametrize('name',['base','fine'])
def test_challenge_complete_native_scores_evidence_and_reload(name):
    path=ROOT/f'{name}-challenge.jsonl'
    if not path.exists():pytest.skip('Run the frozen hybrid benchmark first')
    source={r['id']:r for r in json.loads(Path('tests/fixtures/semantic.json').read_text())}
    rows=[json.loads(x) for x in path.read_text().splitlines()]
    assert len(rows)==57;assert {r['id'] for r in rows}==set(source)
    for row in rows:
        assert row['expected']==source[row['id']]['expected'];assert row['text']==source[row['id']]['text']
        assert row['passed']==all(row['checks'].values())
        for key,answer in row['result']['semantic_analysis'].get('predicates',{}).items():
            ev=answer.get('evidence')
            if ev:assert row['text'][ev['start']:ev['end']]==ev['text']
            scores=answer['scores']
            assert all(math.isfinite(v) and 0<=v<=1 for v in scores.values())
            if scores:assert abs(sum(scores.values())-1)<.002
        assert not row['result']['decision']['automation_enabled']
    assert json.loads((ROOT/f'{name}-reload.json').read_text())['identical']

def test_hybrid_runtime_freeze_unchanged():
    p=ROOT/'PIPELINE-FREEZE.json'
    if not p.exists():pytest.skip('Hybrid experiment not frozen')
    for name,digest in json.loads(p.read_text())['files'].items():assert hashlib.sha256(Path(name).read_bytes()).hexdigest()==digest

def test_narrow_training_membership_and_no_challenge_training():
    p=Path('data/experiments/narrow-v1/protocol.json')
    if not p.exists():pytest.skip('Narrow experiment not prepared')
    protocol=json.loads(p.read_text());assert protocol['targets']==['votable','share_blocking','poa_required']
    assert len(protocol['membership']['train'])==300;assert len(protocol['membership']['validation'])==100
    assert set(protocol['membership'])=={'train','validation'}
    challenge={hashlib.sha256(r['text'].encode()).hexdigest() for r in json.loads(Path('tests/fixtures/semantic.json').read_text())}
    assert not challenge & {r['source_hash'] for split in protocol['membership'].values() for r in split}
    for name,digest in protocol['files'].items():assert hashlib.sha256((p.parent/name).read_bytes()).hexdigest()==digest
