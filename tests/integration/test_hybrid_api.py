import pytest

def test_hybrid_summary_separates_sources(client):
    h=client.get('/api/hybrid/summary').json();assert not h['automation_enabled'];assert not h['llm_enabled']
    if h['public_parser']:assert h['public_parser']['records']==7683;assert h['public_parser']['laya_executions']==0

def test_public_example_provenance_and_source(client):
    h=client.get('/api/hybrid/example?id=clearstream-dscl-excerpt').json()
    assert h['source']['source_type']=='OFFICIAL_EXAMPLE';assert h['analysis']['parsed']['message_type']=='MT564'
    assert not h['analysis']['decision']['automation_enabled']
    assert client.get('/api/hybrid/example?id=../../secret').status_code==404

def test_blind_hides_hybrid(client):
    assert client.get('/api/notice?id=test&blind=true').json()['hybrid_inspection'] is None
    assert client.get('/api/notice?id=test').json()['hybrid_inspection']['parsed']['kind']=='UNSTRUCTURED_NOTICE'

@pytest.mark.requires_artifact('data/experiments/iso-hybrid-v1/base-challenge.jsonl')
def test_hybrid_errors_trace_scores(client):
    r=client.get('/api/hybrid/errors?model=base').json()
    assert r['n']==31
    for row in r['items']:
        assert row['failures'];assert row['source_type']=='AUTHORED_CHALLENGE'
        for f in row['failures']:assert 'scores' in f;assert f['expected']!=f['predicted']
    assert client.get('/api/hybrid/errors?model=../../secret').status_code==400

@pytest.mark.requires_artifact('data/experiments/iso-hybrid-v1/fine-challenge.jsonl')
def test_derived_restriction_has_no_invented_probability(client):
    d=client.get('/api/hybrid/errors?model=fine').json()
    for row in d['items']:
        for f in row['failures']:
            if f['field']=='other_restriction':assert f['confidence'] is None;assert f['margin'] is None
