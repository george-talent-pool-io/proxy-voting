"""Atomic publication of one immutable execution; readers never see a partial row."""
import json,os,uuid
from pathlib import Path

def persist(folder,row):
    folder=Path(folder);folder.mkdir(parents=True,exist_ok=True)
    ident=str(uuid.UUID(row['run_id']));target=folder/(ident+'.jsonl');temporary=folder/(ident+'.pending');owned=False
    try:
        with temporary.open('x') as f:
            owned=True
            f.write(json.dumps(row,ensure_ascii=False,allow_nan=False)+'\n');f.flush();os.fsync(f.fileno())
        # Atomic no-replace publication on the same filesystem, followed by directory sync.
        os.link(temporary,target)
        fd=os.open(folder,os.O_RDONLY)
        try:os.fsync(fd)
        finally:os.close(fd)
    finally:
        if owned:temporary.unlink(missing_ok=True)
    return target
