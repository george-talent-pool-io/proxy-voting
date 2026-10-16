import json,hashlib
from pathlib import Path
from datetime import datetime,timezone
ROOT=Path('data/experiments/cascade-v2');store=Path.home()/'.ollama/models'
if __name__=='__main__':
 pre=json.loads((ROOT/'QWEN-PREFLIGHT.json').read_text());path=store/'manifests/registry.ollama.ai/library/qwen3.8/27b-q4_K_M'
 raw=path.read_bytes();assert hashlib.sha256(raw).hexdigest()==pre['digest'];manifest=json.loads(raw);out=[]
 for layer in [manifest['config']]+manifest['layers']:
  p=store/'blobs'/layer['digest'].replace(':','-');h=hashlib.sha256()
  with p.open('rb') as f:
   for part in iter(lambda:f.read(8*1024*1024),b''):h.update(part)
  assert 'sha256:'+h.hexdigest()==layer['digest'];assert p.stat().st_size==layer['size']
  out.append({'digest':layer['digest'],'size':layer['size'],'verified':True})
 with (ROOT/'QWEN-INSTALLED-INTEGRITY.json').open('x') as f:json.dump({'verified_at':datetime.now(timezone.utc).isoformat(),'manifest_digest':pre['digest'],'blobs':out},f,indent=2)
 print('Manifest and',len(out),'downloaded blobs verified')
