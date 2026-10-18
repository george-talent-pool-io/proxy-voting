"""Nested specialist/final calibration must not share evaluation outcomes."""
import json
from pathlib import Path
import pytest
from training.framework.event_data import write_calibration_parts,load_calibration_answers


def test_partition_keys_are_physical_disjoint_and_preserve_connected_families(tmp_path,monkeypatch):
    (tmp_path/'private').mkdir()
    rows=[];answers=[]
    for i in range(100):
        for variant in range(2):
            ident=f'{i}-{variant}'
            rows.append({'id':ident,'snapshot_hash':ident,'text':f'Distinct instrument {i} administrative item {variant} '+chr(65+i%26)*20,
                         'split':'CALIBRATION','group_id':str(i),'generation_family':str(i)})
            answers.append({'id':ident,'snapshot_hash':ident,'split':'CALIBRATION','target':{}})
    parts=write_calibration_parts(tmp_path,rows,answers)
    a=set(parts['LAYA_STAGE']['ids']);b=set(parts['CASCADE_FINAL']['ids'])
    assert a and b and not a&b and a|b=={r['id'] for r in rows}
    assert all((f'{i}-0' in a)==(f'{i}-1' in a) for i in range(100))
    original=Path.read_text
    def guard(path,*args,**kwargs):
        assert path.name not in ('calibration-answers.jsonl','calibration-cascade_final-answers.jsonl'), 'Stage reader opened final/aggregate outcomes'
        return original(path,*args,**kwargs)
    monkeypatch.setattr(Path,'read_text',guard)
    keys=load_calibration_answers(tmp_path,{'calibration_parts':parts},'LAYA_STAGE',[r for r in rows if r['id'] in a])
    assert set(keys)==a


def test_stage_reader_rejects_legacy_aggregate_and_modified_membership(tmp_path):
    with pytest.raises(ValueError,match='migration'):
        load_calibration_answers(tmp_path,{},'LAYA_STAGE',[])
    with pytest.raises(ValueError,match='Unknown'):
        load_calibration_answers(tmp_path,{},'FROZEN_TEST',[])
