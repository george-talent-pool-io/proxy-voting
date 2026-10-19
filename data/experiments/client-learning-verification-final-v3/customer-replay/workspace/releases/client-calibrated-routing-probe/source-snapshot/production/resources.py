"""Container-safe device ownership: flock lifetime survives PID namespaces.

Training children inherit the guard FD. Only a stale lease explicitly owned by
the previous guarded task/job may be reclaimed; unknown leases fail closed.
"""
import fcntl
import json
import os
from contextlib import contextmanager
from functools import wraps
from training.framework import jobs

_FD = None


@contextmanager
def device(purpose):
    global _FD
    jobs.WORKSPACE.mkdir(parents=True, exist_ok=True)
    with (jobs.WORKSPACE / 'customer-device.lock').open('a') as lock:
        try: fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError: raise ValueError('Managed model device busy')
        marker = jobs.WORKSPACE / 'customer-device-owner.json'
        lease = jobs.WORKSPACE / 'model-training.lock'
        if lease.exists():
            previous = json.loads(marker.read_text()) if marker.exists() else {}
            owner = json.loads(lease.read_text())
            if owner.get('purpose') not in previous.get('allowed_purposes', []) and owner.get('job') not in previous.get('jobs', []):
                raise ValueError('Unrecognised model lease; explicit operator inspection required')
            jobs.events(jobs.WORKSPACE, {'state':'STALE_MANAGED_LEASE_RECLAIMED','previous_owner':owner})
            lease.unlink()
        marker.write_text(json.dumps({'purpose':purpose,'allowed_purposes':[purpose,'customer-validation'], 'jobs':[]}))
        _FD = lock.fileno()
        try: yield
        finally: _FD = None


def note_job(path):
    if _FD is None: raise ValueError('No guarded device ownership')
    marker = jobs.WORKSPACE / 'customer-device-owner.json'
    value = json.loads(marker.read_text()); value['jobs'].append(str(path)); marker.write_text(json.dumps(value))


def inherited_fd():
    if _FD is None: raise ValueError('Training child requires guarded device ownership')
    return _FD


def owned(fn):
    @wraps(fn)
    def run(*args, **kwargs):
        with device('customer-development'): return fn(*args, **kwargs)
    return run
