import json
from collections import defaultdict
from training.reliability.corpus import make, build
from training.split import duplicate_groups
from classifier.preprocessing import source_hash
from semantic_pipeline.schema import PREDICATES


def test_fact_first_corpus_reproducible_evidence_and_balanced_votability():
    rows=[make(715200+i) for i in range(500)]
    assert rows[0]==make(715200)
    assert set(r['expected']['votability'] for r in rows)=={'VOTABLE','NOT_VOTABLE','UNCERTAIN'}
    for label in ('VOTABLE','NOT_VOTABLE','UNCERTAIN'):
        values=[r for r in rows if r['expected']['votability']==label]
        assert len(values)>80
        assert set(r['length_kind'] for r in values)=={'SHORT','MEDIUM','LONG'}
    for r in rows:
        assert r['source_hash']==source_hash(r['text']) and r['origin']=='AI_AUTHORED'
        assert set(r['expected'])==set(PREDICATES)
        assert all(q in r['text'] for quotes in r['target']['evidence'].values() for q in quotes)


def test_all_near_duplicate_components_share_role_and_calibration_fold(tmp_path):
    m=build(tmp_path/'corpus',500);groups=defaultdict(set)
    all_rows=[]
    for role,entry in m['files'].items():
        rows=[json.loads(x) for x in ((tmp_path/'corpus')/entry['labels']).read_text().splitlines()]
        for r in rows:groups[r['group']].add((r['role'],r['fold']));all_rows.append(r)
        if role not in ('TRAIN','VALIDATION'):assert entry['labels'].startswith('private/')
    assert all(len(v)==1 for v in groups.values())
    external=defaultdict(set)
    for r,g in zip(all_rows,duplicate_groups(all_rows)):external[g].add(r['role'])
    assert all(len(v)==1 for v in external.values())
    assert m['customer_accuracy'] is None and not m['automation_enabled']
