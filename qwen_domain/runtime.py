"""Exclusive local runtime switching; no overlapping large-model timed arms."""
import os,json,signal,time,subprocess,urllib.request
from pathlib import Path
from qwen_domain.protocol import ROOT,read,write
from qwen_domain.constrained import MODEL_BLOB
def request(base,path,data=None):
    opener=urllib.request.build_opener(urllib.request.ProxyHandler({}))
    req=urllib.request.Request(base+path,data=json.dumps(data).encode() if data is not None else None,headers={'Content-Type':'application/json'})
    with opener.open(req,timeout=10) as f:return json.load(f)
def stop_llama():
    path=ROOT/'artifacts/domain-llama-runtime.json'
    if path.exists():
        info=read(path)
        import psutil
        try:
            proc=psutil.Process(info['pid'])
            if 'llama-server' not in ' '.join(proc.cmdline()):raise RuntimeError('PID reused; refusing to stop another process')
            proc.terminate();proc.wait(20)
        except psutil.NoSuchProcess:pass
def select(mode):
    from scripts.start_cascade_runtime import ensure
    ensure()
    if mode=='BASE_QWEN_DIRECT':stop_llama();return
    for m in request('http://127.0.0.1:11435','/api/ps')['models']:
        request('http://127.0.0.1:11435','/api/generate',{'model':m['name'],'keep_alive':0})
    path=ROOT/'artifacts/domain-llama-runtime.json'
    try:
        request('http://127.0.0.1:11436','/health')
        if read(path).get('context')==32768:return
        stop_llama()
    except (OSError,ValueError):pass
    cmd=['/opt/homebrew/bin/llama-server','--model',str(MODEL_BLOB),'--host','127.0.0.1','--port','11436','--ctx-size','32768','--parallel','1','--n-gpu-layers','99','--jinja','--metrics','--slots','--offline','--no-webui','--ctx-checkpoints','8','--checkpoint-min-step','128']
    with (ROOT/'artifacts/domain-llama-runtime.log').open('ab',buffering=0) as f:p=subprocess.Popen(cmd,stdin=subprocess.DEVNULL,stdout=f,stderr=f,start_new_session=True)
    path.write_text(json.dumps({'pid':p.pid,'command':cmd,'context':32768,'version':'10210 (000547513)'},indent=2))
    for _ in range(120):
        try:
            request('http://127.0.0.1:11436','/health');return
        except OSError:time.sleep(.5)
    raise RuntimeError('Pinned constrained runtime did not start')
