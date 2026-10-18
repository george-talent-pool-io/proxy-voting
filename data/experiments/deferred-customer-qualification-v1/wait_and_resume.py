"""One-shot local scheduling receipt; no model is loaded while waiting."""
import fcntl
import hashlib
import json
import os
from pathlib import Path
import signal
import subprocess
import sys
import time
from datetime import datetime, timezone

import psutil


HERE = Path(__file__).resolve().parent
PLAN = json.loads((HERE / 'plan.json').read_text())
ROOT = Path(PLAN['repository'])
OTHER = Path(PLAN['other_benchmark_repository']).resolve()
CHILD = None
STATE = {'status': 'STARTING', 'monitor_pid': os.getpid(), 'automation_enabled': False}


def save(**updates):
    STATE.update(updates)
    STATE['updated_at'] = datetime.now(timezone.utc).isoformat()
    tmp = HERE / 'status.tmp'
    tmp.write_text(json.dumps(STATE, indent=2) + '\n')
    tmp.replace(HERE / 'status.json')


def cancel(signum, _frame):
    save(status='CANCELLED_BY_SIGNAL', signal=signum)
    if CHILD is not None and CHILD.poll() is None:
        os.killpg(CHILD.pid, signal.SIGINT)
    raise SystemExit(130)


def blockers():
    found = []
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        try:
            if proc.pid == os.getpid():
                continue
            args = proc.info['cmdline'] or []
            name = (proc.info['name'] or '').lower()
            # Ignore terminal/tool processes that merely mention a command.
            if not any(s in name for s in ('python', 'ollama', 'llama', 'mlx')):
                continue
            cwd = Path(proc.cwd()).resolve()
            in_project = cwd == OTHER or OTHER in cwd.parents
            project_script = any(a.startswith(str(OTHER) + '/') for a in args[1:])
            if in_project or project_script:
                found.append({'pid': proc.pid, 'created_at': proc.create_time(),
                              'command': args, 'cwd': str(cwd)})
        except (psutil.NoSuchProcess, psutil.AccessDenied, FileNotFoundError):
            continue
    return found


def verify_inputs():
    for name, expected in PLAN['input_hashes'].items():
        path = ROOT / name
        if not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest() != expected:
            raise RuntimeError('Pinned input changed while paused: ' + name)


def main():
    global CHILD
    lock = (HERE / 'monitor.lock').open('a')
    fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
    signal.signal(signal.SIGINT, cancel)
    signal.signal(signal.SIGTERM, cancel)
    idle_since = None
    while True:
        active = blockers()
        if active:
            idle_since = None
        elif idle_since is None:
            idle_since = time.monotonic()
        idle = 0 if idle_since is None else time.monotonic() - idle_since
        save(status='WAITING_FOR_OTHER_BENCHMARK', blockers=active,
             idle_seconds=round(idle, 1), required_idle_seconds=PLAN['idle_grace_seconds'])
        if not active and idle >= PLAN['idle_grace_seconds']:
            break
        time.sleep(PLAN['poll_seconds'])
    verify_inputs()
    # Recheck immediately before launch; never stop or modify the other project.
    if blockers():
        raise RuntimeError('Other benchmark restarted immediately before launch; no experiment started')
    for step in PLAN['steps']:
        verify_inputs()
        log = ROOT / step['log']
        with log.open('xb') as stream:
            CHILD = subprocess.Popen(step['command'], cwd=ROOT, stdout=stream,
                                     stderr=subprocess.STDOUT, start_new_session=True)
            save(status='RUNNING', stage=step['name'], child_pid=CHILD.pid,
                 log=str(log), blockers=[])
            code = CHILD.wait()
        CHILD = None
        if code:
            save(status='FAILED', stage=step['name'], exit_code=code)
            return code
    save(status='COMPLETED', child_pid=None, completed_at=datetime.now(timezone.utc).isoformat())
    return 0


if __name__ == '__main__':
    try:
        sys.exit(main())
    except Exception as error:
        save(status='STOPPED_WITH_ERROR', error=str(error))
        raise
