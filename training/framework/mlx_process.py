"""Local JSONL boundary for the isolated MLX serving environment."""
import json
import select
import subprocess
import threading
from pathlib import Path

from training.framework.bundle import ROOT, write


class MlxProcess:
    def __init__(self, root, spec):
        self.lock = threading.RLock()
        request = Path(root) / 'mlx-serving-request.json'
        value = {'spec': spec.model_dump(), 'checkpoint': str(Path(root) / 'checkpoint')}
        if request.exists():
            if json.loads(request.read_text()) != value:
                raise ValueError('Existing serving configuration differs from registered checkpoint')
        else:
            write(request, value)
        with (Path(root) / 'mlx-serving.log').open('ab', buffering=0) as log:
            self.process = subprocess.Popen([spec.runtime_python, '-m', 'training.framework.mlx_worker',
                    'serve', str(request)], cwd=ROOT, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                    stderr=log, text=True, encoding='utf-8', bufsize=1)
        try:
            if not self.read(180).get('ready'):
                raise RuntimeError('MLX worker did not report readiness')
        except BaseException:
            self.close(); raise

    def read(self, timeout):
        if not select.select([self.process.stdout], [], [], timeout)[0]:
            raise TimeoutError('MLX worker response timeout')
        line = self.process.stdout.readline()
        if not line:
            raise RuntimeError('MLX worker exited; inspect serving log')
        return json.loads(line)

    def generate(self, messages):
        with self.lock:
            self.process.stdin.write(json.dumps({'messages': messages}, ensure_ascii=False) + '\n')
            self.process.stdin.flush()
            value = self.read(600)
            if 'error' in value:
                raise ValueError(value['error'])
            return value

    def close(self):
        if self.process.poll() is None:
            self.process.terminate()
            try: self.process.wait(10)
            except subprocess.TimeoutExpired: self.process.kill(); self.process.wait()
