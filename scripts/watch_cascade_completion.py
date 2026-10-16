"""One-shot local delivery requested by the user; no model calls or chat API.

Only reports completion after the study's final verification gate. macOS alerts
are best-effort: successful osascript execution is not a delivery receipt.
"""
import json,os,subprocess,time
from pathlib import Path
from datetime import datetime,timezone
ROOT=Path(__file__).resolve().parents[1]
STUDY=ROOT/'data/experiments/cascade-v2'
ARTIFACTS=ROOT/'artifacts'
REPORTS=ROOT/'data/reports'

def pct(v):return 'N/A' if v is None else f'{v:.1%}'
def count(m):return f'{m.get("correct",0)}/{m.get("n",0)}'

def write_full_summary(summary,reports):
    md=['# Complete Laya / GLM / Qwen experiment summary','',
        '**Authored challenge and synthetic benchmarks only. Customer accuracy UNKNOWN. Automation disabled.**','',
        'A/B retain the same whole-notice checkpoints. C1/C2/C3 always escalate with identical whole-notice Laya context; D1/D2/D3 are independent. Model 1 = GLM-4.7-Flash, 2 = Qwen3.8 Direct, 3 = Qwen3.8 xhigh Thinking. C_SELECTIVE/E_SELECTIVE use the declared capable specialist. These are different experimental conditions, not one aggregate accuracy.','']
    for dataset,arms in summary['datasets'].items():
        md += [f'## {dataset}: quality and latency','',
            '| Condition | Labelled assertions correct | Partial/all-labelled cases satisfied | LLM calls | Median / p95 seconds |',
            '|---|---:|---:|---:|---:|']
        for name,m in arms.items():
            md.append(f'| {name} | {m["correct_assertions"]}/{m["assertions"]} | {m["cases_satisfying_all_supplied_assertions"]}/{m["cases"]} | {m["llm_invocations"]}/{m["cases"]} | {m["median_latency_ms"]/1000:.2f} / {m["p95_latency_ms"]/1000:.2f} |')
        md += ['', 'The challenge has 95 labelled assertions over 57 cases and only four explicit final-status labels. The complete synthetic benchmark has 528 assertions over 48 cases. No unlabelled predicate is counted as correct.','',
            '### Fallback semantic repairs and damage','',
            'Counts compare the pre-fallback specialist with the final reconciled semantic output on invoked, labelled assertions. They exclude deadline/status assertions; reconciliation contributes, so they are not a pure raw-LLM causal attribution.','',
            '| Condition | Semantic transitions scored | Wrong → correct | Correct → wrong | Correct preserved | Wrong still wrong |',
            '|---|---:|---:|---:|---:|---:|']
        for name,t in summary['transitions'].get(dataset,{}).items():
            c=t['semantic_transitions'];md.append(f'| {name} | {sum(c.values())} | {c.get("wrong -> correct",0)} | {c.get("correct -> wrong",0)} | {c.get("correct -> correct",0)} | {c.get("wrong -> wrong",0)} |')
        md += ['', '### Critical-positive recall by predicate','',
            '| Condition | Predicate | Positive support | Positive recall | Positive precision | Misses incl. abstention | False positives | Unsupported outputs |',
            '|---|---|---:|---:|---:|---:|---:|---:|']
        for name,m in arms.items():
            for key,f in m['fields'].items():
                if key in ('deadline_status','classification'):continue
                a=m.get('critical_asymmetry',{}).get(key,{})
                md.append(f'| {name} | {key} | {f["positive_support"]} | {pct(f["positive_recall"])} | {pct(f["positive_precision"])} | {a.get("false_negatives_including_abstention","N/A")} | {a.get("false_positives","N/A")} | {f["not_supported"]} |')
        md += ['', '### Native Laya aggregation: before / after','',
            '| Predicate | Correct before | Correct after | Affirmative recall before → after | Positive support |',
            '|---|---:|---:|---:|---:|']
        for key,x in summary['aggregation_only_predicate_deltas'].get(dataset,{}).items():
            a,b=x['before'],x['after'];md.append(f'| {key} | {count(a)} | {count(b)} | {pct(a["positive_recall"])} → {pct(b["positive_recall"])} | {b["positive_support"]} |')
        md += ['', '### Selective coverage and oracle routing','',
            '| Condition | No-LLM coverage | Correct fast-path cases / accepted | Indecisive fast paths | Oracle correct / labelled assertions | Laya errors repairable by LLM |',
            '|---|---:|---:|---:|---:|---:|']
        for name in ['C_SELECTIVE','E_SELECTIVE']:
            m=arms.get(name);t=summary['transitions'].get(dataset,{}).get(name)
            if not m or not t:continue
            o=summary['ORACLE_ROUTING'][dataset][name]['all_assertions']
            md.append(f'| {name} | {pct(1-m["llm_invocations"]/m["cases"])} | {t["fast_path_correct"]}/{t["fast_path_count"]} | {t["fast_path_indecisive_count"]} | {o.get("oracle_correct",0)}/{o.get("assertions",0)} | {o.get("llm_correct_on_errors",0)}/{o.get("laya_errors",0)} |')
        md += ['', 'Oracle routing is a non-deployable, assertion-wise analytical ceiling. No-LLM coverage is not automation: every record still requires human review under the customer quality gate. Per-predicate oracle and model-complementarity counts remain in SUMMARY.json.','']
    selection=summary['primary_selection'];routing=summary['routing_selection']
    md += ['## Validation-only selection','',f'Experimental primary: **{selection["selected"]}**. {selection["ranking"]}',
        '',f'Selected validation no-LLM coverage {pct(routing["selected"]["laya_only_coverage"])}; semantic agreement {pct(routing["selected"]["semantic_agreement"])} versus always-fallback {pct(routing["always"]["semantic_agreement"])}. Routing was frozen before new challenge inference.','',
        '## Detailed experiment report','']
    md.append((reports/'AGGREGATION_SELECTIVE_CASCADE_EVALUATION.md').read_text())
    md += ['', '## Detailed supporting files','',
        '- [All GLM/Qwen disagreement examples](GLM_VS_QWEN_DISAGREEMENTS.md)',
        '- [Thinking repair and damage examples](QWEN_THINKING_REPAIR_DAMAGE.md)',
        '- [Primary-model selection](GLM_QWEN_MODEL_SELECTION.md)',
        '- [Every assertion failure](CASCADE_V2_ASSERTION_ERRORS.md)',
        '- [Historical C gain attribution](C_GAIN_DECOMPOSITION.md)',
        '- Full machine-readable metrics: `data/experiments/cascade-v2/SUMMARY.json`.']
    target=reports/'FULL_CASCADE_RESULTS.md'
    text='\n'.join(md)+'\n'
    if target.exists():
        if target.read_text()!=text:raise RuntimeError('Existing full result delivery differs; refusing overwrite')
    else:
        with target.open('x') as f:f.write(text)
    return target


def main():
    lock=ARTIFACTS/'cascade-completion-watcher.lock'
    if lock.exists():
        try:os.kill(int(lock.read_text()),0)
        except (ProcessLookupError,ValueError):lock.unlink()
        else:raise RuntimeError('A completion watcher is already running')
    with lock.open('x') as f:f.write(str(os.getpid()))
    try:
        while True:
            try:state=json.loads((STUDY/'LIVE-STATUS.json').read_text())
            except (FileNotFoundError,json.JSONDecodeError):time.sleep(30);continue
            if state['state']=='FAILED':
                outcome={'status':'STUDY_FAILED_NO_COMPLETE_RESULTS','details':state};break
            if state['state']=='COMPLETE':
                verification=json.loads((STUDY/'FINAL-VERIFICATION.json').read_text())
                assert verification['status']=='RESEARCH_COMPLETION_GATE_MET'
                summary=json.loads((STUDY/'SUMMARY.json').read_text())
                assert summary['customer_accuracy'] is None and not summary['automation_enabled']
                target=write_full_summary(summary,REPORTS)
                message='Complete local results are saved in data/reports/FULL_CASCADE_RESULTS.md. Synthetic/challenge research only; automation remains disabled.'
                script='on run argv\n display notification (item 1 of argv) with title (item 2 of argv)\nend run'
                alert=subprocess.run(['/usr/bin/osascript','-e',script,message,'Laya / GLM / Qwen comparison complete'],capture_output=True,text=True)
                outcome={'status':'FULL_REPORT_SAVED','report':str(target),'macos_alert_command_returncode':alert.returncode,
                    'alert_stderr':alert.stderr,'delivery_scope':'Local file plus best-effort macOS alert; no automatic chat message and no OS delivery receipt.'};break
            time.sleep(30)
        outcome['timestamp']=datetime.now(timezone.utc).isoformat()
        (ARTIFACTS/'cascade-completion-delivery.json').write_text(json.dumps(outcome,indent=2))
    finally:lock.unlink(missing_ok=True)

if __name__=='__main__':main()
