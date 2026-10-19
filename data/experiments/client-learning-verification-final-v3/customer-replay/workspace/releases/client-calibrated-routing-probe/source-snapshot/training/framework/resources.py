"""One cross-process lease for experimental inference and training on this Mac."""
import json
import os
import uuid
from contextlib import contextmanager
from training.framework import jobs


@contextmanager
def model_resource(purpose, *, workspace=None):
    if jobs.active_experiments(): raise ValueError('Timed benchmark active; model execution deferred')
    from pathlib import Path
    path = Path(workspace or jobs.WORKSPACE) / 'model-training.lock'
    path.parent.mkdir(parents=True, exist_ok=True)
    token = str(uuid.uuid4())
    try:
        with path.open('x') as f:
            json.dump({'pid': os.getpid(), 'purpose': purpose, 'token': token, 'created_at': jobs.now()}, f)
    except FileExistsError:
        raise ValueError('Local model resource already owned; inspect the owning job before retrying')
    try:
        yield
    finally:
        if path.exists() and json.loads(path.read_text()).get('token') == token: path.unlink()
