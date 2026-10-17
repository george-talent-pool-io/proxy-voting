import sqlite3,pytest
from fast_cascade.protocol import digest

def test_experimental_route_off_and_status_is_read_only(client):
    r=client.post('/api/fast-cascade/analyse',json={'record_id':'train'});assert r.status_code==403
    r=client.get('/api/fast-cascade/status').json();assert r['automation_enabled'] is False and r['customer_accuracy'] is None
    assert client.get('/api/fast-cascade/cases?split=TRAIN').status_code==422

def test_saved_trace_survives_reconnect_and_is_immutable(client):
    from apps.api import store
    from apps.api.fast_cascade_views import persist
    source=client.get('/api/notice?id=train').json()['text']
    result={'input_hash':digest(source),'predicates':{},'automation_enabled':False,'customer_accuracy':None}
    saved=persist('train',source,result)
    assert client.get('/api/notice?id=train').json()['fast_cascade_execution']['id']==saved['id']
    assert client.get('/api/notice?id=train&blind=true').json()['fast_cascade_execution'] is None
    with store.connect() as c:
        with pytest.raises(sqlite3.IntegrityError,match='immutable'):c.execute('UPDATE fast_cascade_executions SET result=?',('{}',))
        with pytest.raises(sqlite3.IntegrityError,match='immutable'):c.execute('DELETE FROM fast_cascade_executions')
    assert client.get('/api/notice?id=train').json()['fast_cascade_execution']['source_hash']==digest(source)
    with pytest.raises(ValueError,match='source hash'):persist('train','different',result)
