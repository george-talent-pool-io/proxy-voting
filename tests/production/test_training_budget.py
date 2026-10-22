"""Real harmless child processes exercise timeout/cancellation; no model double."""
import subprocess
import sys
import time
import pytest
from production.learning import wait_for_training


def test_individual_stage_budget_is_distinct_from_campaign_budget():
    child=subprocess.Popen([sys.executable,'-c','import time;time.sleep(5)'])
    try:
        with pytest.raises(TimeoutError,match='Individual training-stage'):
            wait_for_training(child,lambda:None,time.monotonic(),.02)
        assert child.poll() is None  # Caller owns process-group cleanup.
    finally:child.terminate();child.wait(timeout=5)


def test_campaign_cancellation_still_interrupts_individual_stage_wait():
    child=subprocess.Popen([sys.executable,'-c','import time;time.sleep(5)'])
    def stop():raise InterruptedError('Requested')
    try:
        with pytest.raises(InterruptedError):wait_for_training(child,stop,time.monotonic(),100)
    finally:child.terminate();child.wait(timeout=5)
