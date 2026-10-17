"""Input-only training exclusions from already-persisted benchmark inputs.

No answer, prediction or score field is accessed. The trainer receives only
hashes/fingerprints, never the challenge truth or its output predictions.
"""
import json
from pathlib import Path
from classifier.preprocessing import source_hash, normalise
from training.framework.event_data import fingerprint
from training.framework.bundle import sha, jsonl


def build():
    source = Path('data/experiments/local-llm-v1/challenge-A.jsonl')
    values = []
    for line in source.read_text().splitlines():
        record = json.loads(line)
        text, ident = record['text'], record['id']
        values.append({'identity': 'CHALLENGE57:' + ident, 'role': 'FROZEN_CHALLENGE',
                       'source_hash': source_hash(text), 'normalised_hash': source_hash(normalise(text)),
                       'message_hashes': [], 'group_id': 'CHALLENGE57:' + ident, 'family': 'CHALLENGE57:' + ident,
                       'lexical_fingerprint': sorted(fingerprint(text)), 'input_provenance': str(source),
                       'input_provenance_sha256': sha(source), 'labels_accessed': False})
    if len(values) != 57 or len({r['identity'] for r in values}) != 57: raise ValueError('Challenge membership changed')
    target = Path('data/training/exclusions/challenge57-input-fingerprints-v1.jsonl')
    target.parent.mkdir(parents=True, exist_ok=True); jsonl(target, values)
    print('Registered 57 input-only training exclusions; no challenge labels exported')


if __name__ == '__main__': build()
