"""Data-only report postprocessing. Never calls a model or resumes an experiment.

The inference protocol/source files remain frozen. This observer clarifies runtime
counters and writes delivery status as the independent study completes.
"""
import argparse,time,json,os,re
from pathlib import Path
from fast_cascade.protocol import ROOT,STUDY,read,now,atomic

def optional(path):
    try:return read(path)
    except (FileNotFoundError,json.JSONDecodeError):return None

def annotate():
    status=optional(STUDY/'LIVE-STATUS.json') or {};selection=optional(STUDY/'SELECTION.json');report=ROOT/'data/reports/LAYA_FIRST_CASCADE_EVALUATION.md'
    if not report.exists():return
    marker='\n\n<!-- data-only-results-interpretation-v1 -->'
    text=report.read_text().split(marker)[0]
    text=re.sub(r'\*\*State: [^\n]*?\*\*',f"**State: {status.get('state','UNKNOWN')} — {status.get('stage','Not recorded')}**",text,count=1)
    # Native tokens_cached is retained state, not reused prefix count.
    text=text.replace('Native prompt cache tokens','Retained state tokens (not reused prefix)')
    extra=['## Measurement interpretation and current completion status',f"Data-only report revision: {now()}. Inference source, models, predictions and selection criteria are unchanged.",
        f"Current stage: `{status.get('stage')}`. Persisted rows: `{json.dumps(status.get('persisted_rows',{}))}`.",
        'For actual prefix reuse use `raw_runtime_response.timings.cache_n`; `tokens_cached` is retained state after prompt evaluation. The measured short/medium notices reused zero tokens. The longest TRAIN notice reused663–667tokens per call; three-call wall time fell28.78→17.53seconds. This single sequential probe does not establish a general speedup. See [runtime notes](LAYA_FIRST_CASCADE_RUNTIME_NOTES.md).']
    pending=[]
    expected=['PROTOCOL.json','LAYA-BATCH-BENCHMARK.json','NATIVE-CACHE-EVIDENCE-BENCHMARK.json','SELECTION.json','CALIBRATION.json','CONFIDENCE-COVERAGE.json','OPERATING-CONFIGURATION-FREEZE.json','SYNTHETIC_FROZEN_TEST-METRICS.json','ADVERSARIAL_TEST-METRICS.json','OOD_TEST-METRICS.json','CHALLENGE-METRICS.json','THROUGHPUT_100-MEASUREMENT.json','THROUGHPUT_1000-MEASUREMENT.json','REGRESSION-RESULTS.json']
    pending=[p for p in expected if not (STUDY/p).exists()]
    base=STUDY/'predictions/CHALLENGE-BASE_LAYA.jsonl'
    if not base.exists() or sum(1 for line in base.open() if line.strip())!=57:pending.append('Complete corrected base-Laya challenge inference')
    if selection:
        rows=selection['policies'];chosen=next(r for r in rows if r['policy']['name']==selection['selected_policy']['name']);m=chosen['metrics'];ref=selection['reference']
        extra += [f"Validation conclusion: **{selection['status']}**. Selected research policy `{chosen['policy']['name']}` scored{m['correct_assertions']}/{m['assertions']} supplied assertions, versus{ref['correct_assertions']}/{ref['assertions']} for full Qwen. Gear2 call rate:{m['gear2_notice_rate']:.1%}; full-Qwen call rate:{m['gear3_notice_rate']:.1%}; semantically unresolved:{m['semantic_review_rate']:.1%}. Actual human-review rate remains100%."]
        if selection['status']=='NO_VALIDATED_CASCADE':extra+=['No candidate met the predeclared reference-quality/critical-miss gate. This is evidence against deploying the tested acceptance policies. The selected policy remains a measurement condition, not a validated customer route. Do not infer that the most accurate candidate passed.']
        if not chosen['policy']['gear2']:extra+=['Validation selected the simpler Laya→full-Qwen path. Constrained classification did not justify its extra stage under the predeclared quality/latency comparison. The constrained adapter and measurements remain available as experimental benchmarks.']
        critical=['votability','share_blocking','poa_required','registration_required']
        misses=sum(selection['laya']['fields'][k]['positive_false_negatives'] for k in critical)
        repairs=sum(max(0,selection['laya']['fields'][k]['positive_false_negatives']-ref['fields'][k]['positive_false_negatives']) for k in critical)
        extra += [f"Training priority evidence: Laya has{misses} critical-positive false negatives on the validation sample; full Qwen reduces the per-predicate critical miss counts by{repairs} in total (overlapping records may contribute more than once). No weights were changed. "+('If pursuing specialist training, first audit and expand the Laya predicate labels/formulation, especially transfer-only heads; these results do not justify automatic Qwen fine-tuning.' if repairs else 'No convincing priority for domain training follows from critical-miss reduction alone. Inspect validation error families before training either model.')]
    measurement=optional(STUDY/'THROUGHPUT_1000-MEASUREMENT.json')
    if measurement:
        n=measurement['n'];extra+=[f"Actual1000-notice workload: any-Qwen calls avoided{1-measurement['any_qwen_notice_calls']/n:.1%}; full-Qwen calls avoided{1-measurement['full_qwen_calls']/n:.1%}; mean measured elapsed{measurement['total_measured_active_seconds']*1000/n:.0f}ms per notice. This population has no verified voting labels; no quality follows from its throughput."]
    resources=STUDY/'MODEL-RESOURCE-MEASUREMENTS.jsonl'
    if resources.exists():
        # Stream records, do not load potentially large model outputs into memory.
        minimum=None;peak={};calls=0
        for line in resources.open():
            try:r=json.loads(line)['resources']
            except (json.JSONDecodeError,KeyError):continue
            calls+=1;value=r.get('minimum_system_available_bytes')
            if value is not None:minimum=value if minimum is None else min(minimum,value)
            for key,value in r.get('peak_rss_bytes_by_process',{}).items():peak[key]=max(peak.get(key,0),value)
        atomic(STUDY/'RESOURCE-SUMMARY.json',{'sampled_notice_intervals':calls,'minimum_system_available_bytes':minimum,'peak_rss_bytes_by_process':peak,'caveat':'Apple unified memory; RSS must not be summed across shared mappings. Includes other machine activity. Cache-only references have no new full-model resource measurement.'})
    regression=optional(STUDY/'REGRESSION-RESULTS.json')
    if regression:extra += [f"Recorded verification: {regression['software']['passed']} ordinary tests;{regression['browser']['passed']} browser tests;{regression['real_local_models']['passed']} real Laya/native-Qwen/full-Qwen integration test ({regression['real_local_models']['seconds']}s). Authored model-quality failures are benchmark outcomes, not deleted or counted as software passes."]
    if pending:extra+=['**Completion gate OPEN.** Remaining artefacts/measurements: '+', '.join(pending)+'.']
    else:extra+=['All required measurement artefacts are present. A negative validation result remains a negative result; automation and customer accuracy are unchanged.']
    extra+=['This study does not establish customer accuracy, safe customer auto-acceptance, calibration on real notices, or production readiness. Representative independently expert-labelled customer notices are still required.']
    report.write_text(text+marker+'\n\n'+'\n\n'.join(extra)+'\n')
    atomic(STUDY/'DELIVERY-STATUS.json',{'timestamp':now(),'execution_state':status.get('state'),'completion_gate':'OPEN' if pending else 'MEASUREMENT_ARTEFACTS_PRESENT','remaining':pending,'report':str(report.relative_to(ROOT)),'automation_enabled':False,'customer_accuracy':None})

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--pid',type=int);args=parser.parse_args();import psutil
    stamp=None
    while True:
        p=ROOT/'data/reports/LAYA_FIRST_CASCADE_EVALUATION.md';s=STUDY/'LIVE-STATUS.json';current=(p.stat().st_mtime_ns if p.exists() else None,s.stat().st_mtime_ns if s.exists() else None)
        status=optional(STUDY/'LIVE-STATUS.json') or {}
        if current!=stamp:annotate();stamp=(p.stat().st_mtime_ns if p.exists() else None,s.stat().st_mtime_ns if s.exists() else None)
        if args.pid is None or not psutil.pid_exists(args.pid):
            annotate();break
        time.sleep(15)
if __name__=='__main__':main()
