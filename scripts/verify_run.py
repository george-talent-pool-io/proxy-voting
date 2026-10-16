"""Verify persisted predictions, factor probabilities, input counts and split assignments."""
import argparse
import json
from apps.api.store import connect,latest_run,dumps
from classifier.schema import ClassificationResult
from classifier.preprocessing import source_hash
from training.split import verify_isolation,duplicate_groups

def verify(run_id=None,path=None):
    with connect(path) as c:
        run=c.execute('SELECT * FROM runs WHERE id=?',(run_id,)).fetchone() if run_id else latest_run(c)
        if not run:raise ValueError('No run')
        inputs=[dict(r) for r in c.execute('SELECT * FROM run_inputs WHERE run_id=?',(run['id'],))]
        rows=[dict(r) for r in c.execute('SELECT * FROM predictions WHERE run_id=?',(run['id'],))]
        notices={r['id']:dict(r) for r in c.execute('SELECT * FROM notices')}
        assert len(inputs)==len(rows),'Output/input count mismatch'
        assert {r['record_id'] for r in rows}=={r['record_id'] for r in inputs}
        for r in rows:
            assert r['source_hash']==source_hash(notices[r['record_id']]['text'])
            assert not r['error'],f'Failed classification: {r["record_id"]}'
            result=ClassificationResult.model_validate_json(r['result'])
            assert result.configuration_version==run['config_version']
            assert result.model_version==run['model_version']
        nrows=[{**r,'source_file':json.loads(r['metadata']).get('source_file')} for r in notices.values()]
        verify_isolation(nrows)
        recomputed=duplicate_groups(nrows)
        verify_isolation([{**r,'group_id':g} for r,g in zip(nrows,recomputed)])
        from classifier.laya_classifier import config_version,prepare_config
        assert config_version(prepare_config(json.loads(run['config'])))==run['config_version'],'Configuration order/fingerprint mismatch'
        return {'run_id':run['id'],'valid_input_rows':len(inputs),'output_rows':len(rows),'failed_rows':0,
            'invalid_probabilities':0,'source_hash_mismatches':0,'split_leakage_detected':False,'exact_grouping_recomputed':True,
            'checks':'Pydantic score validation, immutable ledger, source hashes, group/source-file/hash split isolation',
            'limitations':'Exact grouping at the configured shingle threshold does not prove absence of all semantic paraphrases.'}
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--run');p.add_argument('--output');a=p.parse_args();result=verify(a.run)
    if a.output:
        with open(a.output,'x') as f:f.write(dumps(result))
    print(dumps(result))
