"""Start only the isolated local study runtime if absent; never replace the normal service."""
import json,os,time,subprocess,urllib.request
from pathlib import Path
BASE='http://127.0.0.1:11435'
def version():
    opener=urllib.request.build_opener(urllib.request.ProxyHandler({}))
    with opener.open(BASE+'/api/version',timeout=2) as r:return json.load(r)['version']
def ensure():
    try:
        v=version()
        if v!='0.34.3':raise RuntimeError('Different runtime bound to isolated port; refusing substitution')
        return {'already_running':True,'version':v}
    except (urllib.error.URLError,TimeoutError,ConnectionError):pass
    log=Path('artifacts/cascade-isolated-runtime.log');log.parent.mkdir(exist_ok=True)
    with log.open('ab',buffering=0) as output:
        p=subprocess.Popen(['ollama','serve'],env={**os.environ,'OLLAMA_HOST':'127.0.0.1:11435','OLLAMA_NUM_PARALLEL':'2','OLLAMA_MAX_LOADED_MODELS':'1','OLLAMA_CONTEXT_LENGTH':'32768','OLLAMA_NO_CLOUD':'1'},
            stdin=subprocess.DEVNULL,stdout=output,stderr=subprocess.STDOUT,start_new_session=True)
    for _ in range(100):
        try:
            if version()!='0.34.3':raise RuntimeError('Wrong pinned runtime version')
            return {'pid':p.pid,'version':'0.34.3'}
        except (urllib.error.URLError,TimeoutError,ConnectionError):time.sleep(.1)
    raise RuntimeError('Isolated Ollama did not start; inspect '+str(log))
if __name__=='__main__':print(ensure())
