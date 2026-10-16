"""Strict prediction commits; permit only append-only operational event history."""
import hashlib
from pathlib import Path
from semantic_pipeline.experiment import sha


def verify_prediction_commit(commit,root):
    results={}
    for name,expected in commit['files'].items():
        p=Path(name)
        if sha(p)==expected:
            results[name]={'verification':'EXACT_HASH'}
            continue
        if p.resolve()!=(Path(root)/'EXECUTION-EVENTS.jsonl').resolve():
            raise AssertionError(f'Immutable prediction artifact changed: {p}')
        # The original commit included this live log. Preserve that commit and
        # verify its exact byte prefix, without exempting it from integrity checks.
        digest=hashlib.sha256();size=0;found=False
        with p.open('rb') as stream:
            for line in stream:
                digest.update(line);size+=len(line)
                if digest.hexdigest()==expected:
                    found=True;break
        if not found:raise AssertionError(f'Committed operational log prefix changed: {p}')
        results[name]={'verification':'EXACT_COMMITTED_PREFIX_THEN_APPEND_ONLY','committed_prefix_bytes':size,
            'current_bytes':p.stat().st_size,'reason':'Operational events continue after the prediction commit; predictions remain immutable.'}
    return results
