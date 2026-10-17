"""Small TRAIN/VALIDATION-only engineering cohort, not a quality benchmark."""
import json
from collections import Counter
from pathlib import Path

from semantic_pipeline.schema import PREDICATES
from training.framework.bundle import load_bundle, create_bundle, sha, write


def prepare(source, output, train_n=12, validation_n=4):
    manifest, rows = load_bundle(source)
    chosen = []
    for split, n in [('TRAIN', train_n), ('VALIDATION', validation_n)]:
        pool = sorted([r for r in rows if r.split == split and len(r.text) <= 1600],
                      key=lambda r: (len(r.text), r.id))
        covered = set()
        for _ in range(n):
            if not pool: raise ValueError('Insufficient source examples for declared cohort')
            # Label stratification is permitted on development data only. Prefer
            # new field/class combinations, then shorter complete notices.
            e = max(pool, key=lambda r: (len({(k, getattr(r.target, k)) for k in PREDICATES} - covered), -len(r.text), r.id))
            pool.remove(e); chosen.append(e)
            covered.update((k, getattr(e.target, k)) for k in PREDICATES)
    result = create_bundle(chosen, output, source_manifest={
        'source_bundle_manifest_sha256': sha(Path(source) / 'manifest.json'),
        'selection': 'TRAIN/VALIDATION only; greedy field/class coverage then short complete text <=1600 characters',
        'purpose': 'Execution and adapter qualification, not an independent performance estimate',
        'held_out_answers_opened': False})
    write(Path(output) / 'cohort-description.json', {'ids': [e.id for e in chosen],
        'field_support': {s: {k: dict(Counter(getattr(e.target, k) for e in chosen if e.split == s))
                               for k in PREDICATES} for s in ['TRAIN','VALIDATION']},
        'purpose': 'Engineering qualification; AI-authored labels only'})
    return result


if __name__ == '__main__':
    import argparse
    p = argparse.ArgumentParser(); p.add_argument('source'); p.add_argument('output'); args = p.parse_args()
    print(json.dumps(prepare(args.source, args.output), indent=2))
