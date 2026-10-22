"""Reproducible source delivery including uncommitted reviewed workspace files.

Never packages datasets, private keys, credentials, model bases or job artifacts.
The source archive is separate from the protected operational data backup.
"""
import argparse
import gzip
import hashlib
import io
import json
import subprocess
import tarfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def package(output):
    output = Path(output); output.parent.mkdir(parents=True, exist_ok=True)
    paths = set()
    for folder in ['apps', 'classifier', 'training', 'evaluation', 'semantic_pipeline', 'semantic_runtime', 'hybrid',
                   'cascade', 'fast_cascade', 'qwen_domain', 'iso15022', 'iso_adapter', 'scripts', 'docs', 'tests', 'production', 'deploy']:
        for p in (ROOT / folder).rglob('*'):
            if p.is_file() and not any(s in p.parts for s in ['__pycache__', '.pytest_cache']) and p.suffix in (
                    '.py', '.js', '.css', '.html', '.json', '.txt', '.md', '.sh', '.yml', '.yaml', '.lock', '.conf'):
                if any(s in p.relative_to(ROOT).parts for s in ('secrets', 'tls')): continue
                paths.add(p.relative_to(ROOT))
    paths.add(Path('deploy/Dockerfile'))
    paths.update(Path('data/reports') / name for name in ('CLIENT_PRODUCTION_GAP_PLAN.md', 'CLIENT_PRODUCTION_READINESS.md', 'FROZEN_CHECKPOINT_LEARNING_EVALUATION.md', 'FRAMEWORK_E2E_AND_MODEL_READINESS.md')
                 if (ROOT / 'data/reports' / name).is_file())
    for name in ['README.md', 'LICENSE', 'NOTICE', 'COMMERCIAL-LICENSE', '.dockerignore', '.gitignore', 'pyproject.toml', 'uv.lock', 'Dockerfile', 'docker-compose.yml']:
        if (ROOT / name).is_file(): paths.add(Path(name))
    paths.add(Path('tools/prowide/pom.xml'))
    paths.update(p.relative_to(ROOT) for p in (ROOT / 'tools/prowide/src').rglob('*.java'))
    jar = Path('tools/prowide/target/prowide-helper-1.0.0.jar')
    if (ROOT / jar).exists(): paths.add(jar)
    # Input-only challenge fingerprints are training exclusion configuration,
    # not answer keys or source notices. Keep the leakage barrier on clean installs.
    paths.update(p.relative_to(ROOT) for p in (ROOT / 'data/training/exclusions').glob('*.jsonl'))
    data = {p.as_posix(): (ROOT / p).read_bytes() for p in sorted(paths)}
    manifest = {'version': 'local-learning-source-v1', 'files': {k: hashlib.sha256(v).hexdigest() for k, v in data.items()},
                'git_commit': subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip(),
                'workspace_dirty': bool(subprocess.check_output(['git', 'status', '--porcelain'], cwd=ROOT, text=True).strip()),
                'data_included': False, 'input_only_exclusion_configuration_included': True,
                'models_included': False, 'automation_enabled': False}
    data['SOURCE-MANIFEST.json'] = (json.dumps(manifest, indent=2, sort_keys=True) + '\n').encode()
    with output.open('xb') as f:
        with gzip.GzipFile(fileobj=f, mode='wb', mtime=0, filename='') as gz:
            with tarfile.open(fileobj=gz, mode='w') as archive:
                for name, content in sorted(data.items()):
                    info = tarfile.TarInfo(name); info.size = len(content); info.mode = 0o644
                    archive.addfile(info, io.BytesIO(content))
    receipt = {'archive_sha256': hashlib.sha256(output.read_bytes()).hexdigest(), 'file_count': len(data), **manifest}
    with output.with_suffix(output.suffix + '.json').open('x') as f: json.dump(receipt, f, indent=2)
    return receipt


if __name__ == '__main__':
    p = argparse.ArgumentParser(); p.add_argument('output'); a = p.parse_args()
    r = package(a.output); print(json.dumps({k: r[k] for k in ['archive_sha256', 'file_count', 'workspace_dirty']}))
