import json,time,concurrent.futures
from pathlib import Path
from cascade.fallback import CommonFallback
ROOT=Path('data/experiments/cascade-v2')
if __name__=='__main__':
 cfg=json.loads((ROOT/'LLM-CONFIGS-v2.json').read_text())['QWEN_THINKING'];model=CommonFallback(cfg)
 show=model.http('/api/show',{'model':cfg['model']});assert 'xhigh' in show['thinking']['values']
 sources=['Shareholders can cast proxy votes. A power of attorney is required. No share blocking applies. Voting instructions are due by 24 November 2026.',
 'This dividend is mandatory and offers no shareholder vote. Shares are not blocked. No power of attorney is required.']
 start=time.perf_counter()
 def call(text):return model.analyse(original_text=text,narrative_text=text,structured_facts={},mode='INDEPENDENT')
 with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:results=list(pool.map(call,sources))
 out={'wall_ms':(time.perf_counter()-start)*1000,'runtime_thinking_controls':show['thinking'],'config':cfg,'results':results,'concurrency':2}
 with (ROOT/'QWEN-XHIGH-PROBE.json').open('x') as f:json.dump(out,f,indent=2)
 for r in results:print(r['valid'],r.get('error'),r['latency_ms'],(r.get('raw_response') or {}).get('thinking_diagnostics'),flush=True)
