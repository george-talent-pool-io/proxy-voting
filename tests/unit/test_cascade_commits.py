import pytest
from cascade.commits import verify_prediction_commit
from semantic_pipeline.experiment import sha


def test_prediction_bytes_remain_strict_even_if_operational_log_can_append(tmp_path):
    log=tmp_path/'EXECUTION-EVENTS.jsonl';log.write_text('{"state":"BEFORE_COMMIT"}\n')
    pred=tmp_path/'predictions.jsonl';pred.write_text('{"value":"YES"}\n')
    commit={'files':{str(log):sha(log),str(pred):sha(pred)}}
    with log.open('a') as f:f.write('{"state":"AFTER_COMMIT"}\n')
    result=verify_prediction_commit(commit,tmp_path)
    assert result[str(log)]['verification']=='EXACT_COMMITTED_PREFIX_THEN_APPEND_ONLY'
    assert result[str(pred)]['verification']=='EXACT_HASH'
    pred.write_text('{"value":"NO"}\n')
    with pytest.raises(AssertionError,match='Immutable prediction'):verify_prediction_commit(commit,tmp_path)


def test_mutating_earlier_operational_history_is_rejected(tmp_path):
    log=tmp_path/'EXECUTION-EVENTS.jsonl';log.write_text('original\n')
    commit={'files':{str(log):sha(log)}}
    log.write_text('modified\nmore events\n')
    with pytest.raises(AssertionError,match='prefix changed'):verify_prediction_commit(commit,tmp_path)
