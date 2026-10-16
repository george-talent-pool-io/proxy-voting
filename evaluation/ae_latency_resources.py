"""Summarise actual recorded warm generation durations, without cache substitution."""
import statistics
from semantic_pipeline.experiment import ROOT,lines,write,now

def med(values):return statistics.median(values) if values else None
def p95(values):return sorted(values)[min(len(values)-1,int(.95*len(values)))] if values else None

def analyse():
    out={}
    for dataset in ('challenge','synthetic-development','complete'):
        out[dataset]={}
        for arm in 'ABCDE':
            rows=lines(ROOT/f'{dataset}-{arm}.jsonl');times=[r['result']['latencies']['total_ms'] for r in rows]
            calls=[r['result']['llm'] for r in rows if (r['result'].get('llm') or {}).get('invoked')]
            token_rates=[]
            for l in calls:
                raw=l['raw_response']
                if raw.get('eval_duration'):token_rates.append(raw.get('eval_count',0)/(raw['eval_duration']/1e9))
            out[dataset][arm]={'rows':len(rows),'median_ms':med(times),'p95_ms':p95(times),'records_per_second_sequential':len(rows)/(sum(times)/1000),
                'llm_invocations':len(calls),'llm_median_ms':med([l['latency_ms'] for l in calls]),'llm_p95_ms':p95([l['latency_ms'] for l in calls]),
                'prompt_tokens_total':sum(l['raw_response'].get('prompt_eval_count',0) for l in calls),
                'generated_tokens_total':sum(l['raw_response'].get('eval_count',0) for l in calls),
                'median_generated_tokens_per_second':med(token_rates),'runtime_load_median_ms':med([l['raw_response'].get('load_duration',0)/1e6 for l in calls]),
                'time_to_first_token':None,'time_to_first_token_reason':'Nonstreaming API; unavailable. Not approximated from total duration.',
                'timing_scope':'Actual warmed per-notice wall time, sequential; no cached result latency. Model load separately recorded.'}
    write(ROOT/'LATENCY-RESOURCES.json',{'created_at':now(),'latency':out,
        'cold_start_probe':'RELOAD-REPRODUCIBILITY.json first LLM response after explicit keep_alive=0 unload includes load_duration',
        'resource_sampling':'REPEATABILITY-RESOURCE-SUMMARY.json process_peak_rss_bytes and runtime_model_allocation',
        'hardware':'Apple M3 Max / 64 GiB unified memory; runtime device allocation is shared memory, not discrete VRAM.'})
    return out
if __name__=='__main__':analyse()
