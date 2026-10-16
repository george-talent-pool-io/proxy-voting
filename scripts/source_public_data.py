"""Reproduce immutable public source downloads. Notice text is never uploaded."""
import hashlib
import json
from pathlib import Path
import urllib.request

REVISION='c90ac749f9056901c8c3ed22ae1ff7c894c9b696'
REPO='TheTokenFactory/sec-contracts-financial-extraction-instructions'
EXPECTED={'alpaca_financial_extraction.jsonl':'bfccfc9b70c35835596c11b424c48a797f0d5877a08339770f8a90f64df40e5b','alpaca_corrective.jsonl':'3410a95839530431ee31712e5615b0ca5f4e81a8ba992026106e1e97f344f813'}

def download():
    folder=Path('data/raw');folder.mkdir(parents=True,exist_ok=True)
    manifest=[]
    for name,expected in EXPECTED.items():
        url=f'https://huggingface.co/datasets/{REPO}/resolve/{REVISION}/data/{name}'
        dest=folder/name
        if not dest.exists():
            temp=dest.with_suffix('.download')
            urllib.request.urlretrieve(url,temp)
            actual=hashlib.sha256(temp.read_bytes()).hexdigest()
            if actual!=expected:raise ValueError(f'Checksum mismatch: {name}')
            temp.rename(dest)
        actual=hashlib.sha256(dest.read_bytes()).hexdigest()
        if actual!=expected:raise ValueError(f'Existing source differs from pinned release: {name}')
        manifest.append({'file':name,'sha256':actual,'url':url,'revision':REVISION,'license':'CC-BY-4.0'})
    (folder/'manifest.json').write_text(json.dumps(manifest,indent=2))
    card=folder/'SOURCE_CARD.md'
    if not card.exists():urllib.request.urlretrieve(f'https://huggingface.co/datasets/{REPO}/raw/{REVISION}/README.md',card)
    print(json.dumps(manifest,indent=2))
if __name__=='__main__':download()
