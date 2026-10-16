import json
import pytest
from apps.api import store
from scripts.migrate_grouping import migrate
from scripts.run_batch import run_batch
from tests.integration.test_workflow import factory,review
from training.split import partition

def test_versioned_grouping_migration_preserves_inference(db,tmp_path):
    run=run_batch(db,classifier_factory=factory)
    with store.connect(db) as c:
        original=[dict(r) for r in c.execute('SELECT * FROM notices')]
        old_predictions=[dict(r) for r in c.execute('SELECT * FROM predictions ORDER BY record_id')]
    rows=[]
    for r in original:
        row=json.loads(r['metadata']);group='new-'+r['group_id']
        rows.append({**row,'text':r['text'],'group_id':group,'split':partition(group),'grouping_version':'exact-prefix-jaccard-v2'})
    path=tmp_path/'v2.jsonl';path.write_text(''.join(json.dumps(r)+'\n' for r in rows))
    target=tmp_path/'v2.sqlite'
    result=migrate(db,target,path,tmp_path/'history')
    assert result['changed_group_rows']==3
    assert result['original_text_and_hashes_identical'] is True
    with store.connect(target) as c:
        assert [dict(r) for r in c.execute('SELECT * FROM predictions ORDER BY record_id')]==old_predictions
        assert c.execute('SELECT count(*) FROM dataset_revisions').fetchone()[0]==1
    with store.connect(db) as c:
        assert [dict(r) for r in c.execute('SELECT * FROM notices')]==original

def test_migration_refuses_labelled_source(db,client,tmp_path):
    assert review(client).status_code==201
    with pytest.raises(ValueError,match='reviewed'):migrate(db,tmp_path/'v2.sqlite',tmp_path/'unused',tmp_path/'history')

def test_migration_refuses_active_job(db,tmp_path):
    run=run_batch(db,classifier_factory=factory)
    with store.connect(db) as c:c.execute("UPDATE runs SET status='RUNNING'")
    with pytest.raises(ValueError,match='active'):migrate(db,tmp_path/'v2.sqlite',tmp_path/'unused',tmp_path/'history')
