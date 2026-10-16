"""Verify the installed OCI manifest and weight layer by streaming SHA-256."""
import hashlib,json
from pathlib import Path
from semantic_pipeline.experiment import ROOT,read,write,now

if __name__=='__main__':
    cfg=read(Path('semantic_pipeline/llm-config.json'))
    store=Path.home()/'.ollama/models'
    manifest=store/'manifests/registry.ollama.ai/library/glm-4.7-flash/latest'
    raw=manifest.read_bytes();actual=hashlib.sha256(raw).hexdigest()
    assert actual==cfg['model_digest']
    blob=json.loads(raw);layers=[]
    for layer in blob['layers']:
        expected=layer['digest'].split(':')[1];path=store/'blobs'/layer['digest'].replace(':','-')
        h=hashlib.sha256()
        with path.open('rb') as f:
            for chunk in iter(lambda:f.read(8*1024*1024),b''):h.update(chunk)
        assert h.hexdigest()==expected,path
        layers.append({'digest':layer['digest'],'size':path.stat().st_size,'media_type':layer['mediaType'],'sha256_verified':True})
    write(ROOT/'OLLAMA-CHECKPOINT-INTEGRITY.json',{'verified_at':now(),'model_digest':actual,
        'manifest':blob,'layers':layers,'scope':'Installed bytes verified; no downloads or inference'})
    print('Ollama manifest and',len(layers),'layers verified')
