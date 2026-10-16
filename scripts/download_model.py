"""Download only the pinned official multilingual checkpoint; never sends notice data."""
from pathlib import Path
import hashlib
import json
from huggingface_hub import snapshot_download
REVISION = '7b928d828b7b0e022f929d9bd2e44165aa270148'
if __name__ == '__main__':
    p = snapshot_download('convaiinnovations/laya', revision=REVISION,
                          allow_patterns=['multilingual/*'], local_dir='data/models/laya')
    folder=Path(p)/'multilingual'
    expected='9d628fd971b700382ac6f65920a86f149777b2e748e0c955fb3b19695aa8f204'
    actual=hashlib.sha256((folder/'model.safetensors').read_bytes()).hexdigest()
    if actual!=expected:raise ValueError('Official checkpoint checksum mismatch')
    files={str(f.relative_to(folder)):hashlib.sha256(f.read_bytes()).hexdigest() for f in sorted(folder.rglob('*')) if f.is_file() and f.name!='model-manifest.json'}
    manifest={'repository':'convaiinnovations/laya','revision':REVISION,'subfolder':'multilingual','files':files}
    (folder/'model-manifest.json').write_text(json.dumps(manifest,indent=2))
    print(folder)
