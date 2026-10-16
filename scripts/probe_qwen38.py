"""Pre-freeze runtime/capability probe. Never uses challenge cases or truth."""
import json,hashlib
from pathlib import Path
from cascade.fallback import CommonFallback
ROOT=Path('data/experiments/cascade-v2')
if __name__=='__main__':
    import urllib.request
    with urllib.request.urlopen('http://127.0.0.1:11434/api/tags') as r:tags=json.load(r)['models']
    pre=json.loads((ROOT/'QWEN-PREFLIGHT.json').read_text());tag=next(x for x in tags if x['name']==pre['model']);assert tag['digest']==pre['digest']
    base={'runtime':'ollama','base_url':'http://127.0.0.1:11434','runtime_version':'0.34.3','num_ctx':32768,'num_predict':2048,'timeout_seconds':1200,'keep_alive':'30m','seed':42,'temperature':0,'think':False}
    old=json.loads(Path('semantic_pipeline/llm-config.json').read_text())
    configs={'GLM':{**old,**base,'condition':'GLM_DIRECT'},
        'QWEN_DIRECT':{**base,'model':pre['model'],'model_digest':pre['digest'],'checkpoint':pre['upstream'],'quantisation':'Q4_K_M','licence':'Apache-2.0','condition':'QWEN_DIRECT','temperature':.7,'top_p':.8,'top_k':20,'min_p':0,'presence_penalty':1.5,'repeat_penalty':1},
        'QWEN_THINKING':{**base,'model':pre['model'],'model_digest':pre['digest'],'checkpoint':pre['upstream'],'quantisation':'Q4_K_M','licence':'Apache-2.0','condition':'QWEN_THINKING','temperature':1.0,'top_p':.95,'top_k':20,'min_p':0,'presence_penalty':0,'repeat_penalty':1,'think':True,'num_predict':16384}}
    # Same context for all; thinking has a separate generous output budget, not cost-matched.
    for k,cfg in configs.items():
        if k=='GLM':continue
        model=CommonFallback(cfg);show=model.http('/api/show',{'model':cfg['model']})
        (ROOT/'QWEN-INSTALLED-SHOW.json').write_text(json.dumps(show,indent=2))
        source='Owners may submit proxy votes. Shares will be blocked until the meeting ends. A power of attorney is not required. Voting instructions are due by 24 November 2026.'
        r=model.analyse(original_text=source,narrative_text=source,structured_facts={},mode='INDEPENDENT')
        (ROOT/(k+'-PREFREEZE-PROBE.json')).write_text(json.dumps(r,indent=2))
        print(k,r['valid'],r.get('error'),r['latency_ms'],(r.get('raw_response') or {}).get('thinking_diagnostics'),flush=True)
    with (ROOT/'LLM-CONFIGS.json').open('x') as f:json.dump(configs,f,indent=2)
