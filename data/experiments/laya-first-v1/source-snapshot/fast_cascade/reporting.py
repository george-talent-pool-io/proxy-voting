"""Reports never turn pending measurements or simulated latencies into results."""
import json
from collections import defaultdict
from fast_cascade.protocol import *
from fast_cascade.study import cached,label_cases,inputs
from fast_cascade.evaluation import values
from qwen_domain.metrics import metrics
from semantic_pipeline.schema import PREDICATES

def optional(p):return read(p) if p.exists() else None

def table(headers,rs):return '\n'.join(['| '+' | '.join(headers)+' |','|'+'|'.join(['---']*len(headers))+'|']+['| '+' | '.join(str(v) for v in r)+' |' for r in rs])
def pct(v):return 'N/A' if v is None else f'{100*v:.1f}%'

def corrected():
    out={}
    for split in ['VALIDATION','CHALLENGE']:
        if not cached(split,'LAYA'):continue
        if split=='CHALLENGE' and not (STUDY/'SELECTION.json').exists():continue
        truth={r['id']:r for r in label_cases(split)}
        for name in ['LAYA','BASE_LAYA']:
            data=cached(split,name)
            if not data:continue
            fields={}
            for k in PREDICATES:
                pairs=[]
                for r in data:
                    c=truth[r['id']]
                    if k not in c['expected']:continue
                    p=r['result'];before=p['predicates'][k]['value'] if k=='votability' else p['legacy_narrow_predicates'][k]['value']
                    pairs.append((c['expected'][k],before,p['predicates'][k]['value']))
                if pairs:fields[k]={'before':metrics([a for a,b,z in pairs],[b for a,b,z in pairs],k),'after':metrics([a for a,b,z in pairs],[z for a,b,z in pairs],k),'scope':'Same cached native passage predictions; only reducer changes. Whole-notice votability unchanged.'}
            out[split+'-'+name]=fields
    return out

def signals():
    truth={r['id']:r for r in label_cases('VALIDATION')};by=defaultdict(lambda:[0,0])
    from fast_cascade.routing import signal
    for r in cached('VALIDATION','LAYA'):
        c=truth[r['id']]
        for k,p in r['result']['predicates'].items():
            f=signal(c['text'],k,p,c['language']);good=p['value']==c['expected'][k]
            for feature,value in [('raw_score_bin',int(10*(f['top_score'] or 0))),('evidence',f['evidence_available']),('contradiction',f['contradiction']),('UNKNOWN',f['unknown']),('absence',p.get('aggregation_reason')=='DOCUMENT_ABSENCE_NOT_EXPLICIT_NEGATION')]:
                slot=by[(k,feature,str(value))];slot[0]+=1;slot[1]+=good
    return [{'predicate':k,'feature':f,'value':v,'support':n,'correct':a,'correctness':a/n} for (k,f,v),(n,a) in by.items()]

def laya_coverage():
    from fast_cascade.routing import Policy,assess,CRITICAL
    truth={r['id']:r for r in label_cases('VALIDATION')};out=[];data=cached('VALIDATION','LAYA')
    for threshold in [.7,.8,.9,.95,.98,.995]:
        accepted=[];whole=0
        for r in data:
            c=truth[r['id']];gates=[]
            policy=Policy('DESCRIPTIVE_THRESHOLD',threshold,.4,min(1,threshold+.005),allow_absence=True)
            for k,p in r['result']['predicates'].items():
                a=assess(c['text'],k,p,policy,language=c['language'])['accepted_for_research'];gates.append(a)
                if a:accepted.append((k,c['expected'][k],p['value']))
            whole+=all(gates)
        out.append({'raw_score_threshold':threshold,'accepted_assertions':len(accepted),'assertion_coverage':len(accepted)/(len(data)*len(PREDICATES)) if data else 0,
            'accepted_assertion_correctness':sum(y==p for k,y,p in accepted)/len(accepted) if accepted else None,'whole_notices_without_qwen':whole,'notices':len(data),
            'accepted_critical_false_negatives':sum(k in CRITICAL and y in ('YES','VOTABLE') and p!=y for k,y,p in accepted)})
    return out

def plots(selection,coverage):
    import matplotlib;matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    if selection:
        rs=selection['policies'];fig,axes=plt.subplots(1,2,figsize=(11,4))
        for r in rs:
            m=r['metrics'];x=1-m['gear3_notice_rate'];y=m['assertion_correctness'];axes[0].scatter(x,y);axes[0].annotate(r['policy']['name'],(x,y),fontsize=6)
            axes[1].scatter(m['gear2_notice_rate'],m['gear3_notice_rate']);axes[1].annotate(r['policy']['name'],(m['gear2_notice_rate'],m['gear3_notice_rate']),fontsize=6)
        axes[0].set(xlabel='Full-Qwen calls avoided (notice fraction)',ylabel='Labelled assertion correctness',title='Synthetic VALIDATION; not customer accuracy');axes[1].set(xlabel='Gear 2 notice rate',ylabel='Gear 3 notice rate',title='Counterfactual routing comparison');fig.tight_layout();fig.savefig(STUDY/'routing-coverage.png',dpi=170);plt.close(fig)
    if coverage:
        bins=defaultdict(list)
        for r in coverage['records']:
            if r['confidence'] is not None:bins[min(9,int(r['confidence']*10))].append(r)
        fig,ax=plt.subplots(figsize=(5,4));ax.plot([0,1],[0,1],'--',color='gray')
        if bins:ax.plot([sum(r['confidence'] for r in v)/len(v) for k,v in sorted(bins.items())],[sum(r['correct'] for r in v)/len(v) for k,v in sorted(bins.items())],'o-')
        else:ax.text(.05,.6,'No predicate has validated numeric confidence')
        ax.set(xlabel='Predicted correctness probability',ylabel='Observed correctness',title='Synthetic held-out calibration evaluation');fig.tight_layout();fig.savefig(STUDY/'calibration-reliability.png',dpi=170);plt.close(fig)

def report():
    dest=ROOT/'data/reports/LAYA_FIRST_CASCADE_EVALUATION.md';dest.parent.mkdir(parents=True,exist_ok=True)
    live=optional(STUDY/'LIVE-STATUS.json') or {};sel=optional(STUDY/'SELECTION.json');cal=optional(STUDY/'CALIBRATION.json');coverage=optional(STUDY/'CONFIDENCE-COVERAGE.json');batch=optional(STUDY/'LAYA-BATCH-BENCHMARK.json');native=optional(STUDY/'NATIVE-CACHE-EVIDENCE-BENCHMARK.json')
    lines=['# Laya-first cascade evaluation',f'\nUpdated: {now()}\n',f"**State: {live.get('state','PREPARING')} — {live.get('stage','implementation')}**. Completion gate remains open until all measurements and regressions are recorded.",
        '\nAutomation is disabled. Every result remains subject to human review. Customer accuracy is unknown. Synthetic and authored results below do not estimate customer quality.',
        '\nThe stopped Qwen domain study is preserved. This is a separately versioned experiment in `data/experiments/laya-first-v1`; no model is retrained.',
        '\n## Historical quality ceiling',table(['Condition','Labelled assertions correct /95','Cases satisfying supplied assertions /57'],[['Base whole-notice Laya',59,30],['Fine-tuned whole-notice Laya',73,37],['Independent Qwen Direct',92,54]]),
        '\nOnly four challenge cases have explicit final-status truth. These historical whole-notice Laya outputs are distinct from the corrected narrow-predicate pipeline; reducer repairs do not change a whole-notice head.',
        '\n## Corrected Laya and specialist coverage','\nSame native passage inference is reduced before/after, avoiding checkpoint or batching confounds. Three narrow targets were supervised: votability, share blocking, POA. Six other targets are transfer-only, including registration. Whole-notice votability remains its own supervised head.']
    comp=corrected()
    for name,fields in comp.items():
        lines+=['\n### '+name,table(['Predicate','Support','Before correct','After correct','Before positive recall','After positive recall'],[[k,v['after']['n'],v['before']['correct'],v['after']['correct'],pct(v['before']['positive_recall']),pct(v['after']['positive_recall'])] for k,v in fields.items()])]
    if not comp:lines+=['Pending new labelled validation/challenge predictions. The previously investigated 11 positive blocking cases changed 0/11→11/11 using unchanged weights; this is not a new corpus-wide quality result.']
    if comp:atomic(STUDY/'CORRECTED-LAYA-METRICS.json',comp)
    lines+=['\n## Trust signals and safe coverage','Raw winning scores/margins are not calibrated confidence. All passage scores, current/historical states, evidence offsets, support/opposition and UNKNOWN outputs are persisted. Acceptance is a research simulation. Known cross-model disagreements require sufficient validation preference or review.']
    if sel:
        atomic(STUDY/'TRUST-SIGNAL-ANALYSIS.json',signals())
        trust=laya_coverage();atomic(STUDY/'LAYA-TRUST-COVERAGE.json',trust)
        lines+=[table(['Laya raw threshold','Accepted assertions','Assertion coverage','Accepted correctness','Whole notices avoiding Qwen','Accepted critical misses'],[[r['raw_score_threshold'],r['accepted_assertions'],pct(r['assertion_coverage']),pct(r['accepted_assertion_correctness']),f"{r['whole_notices_without_qwen']}/{r['notices']}",r['accepted_critical_false_negatives']] for r in trust])]
        lines+=[f"\nSelection: **{sel['status']}**; experimental policy `{sel['selected_policy']['name']}`.",table(['Policy','Correct / assertions','Gear 2','Gear 3','Unresolved review','Reference gate','Estimated median ms'],[[r['policy']['name'],f"{r['metrics']['correct_assertions']}/{r['metrics']['assertions']}",pct(r['metrics']['gear2_notice_rate']),pct(r['metrics']['gear3_notice_rate']),pct(r['metrics']['semantic_review_rate']),r['metrics']['passed_reference_gate'],round(r['metrics']['median_latency_ms'])] for r in sel['policies']]),'\nLatency in this policy table is a counterfactual sum of measured components; it is not an actual end-to-end throughput benchmark. Policies were compared on VALIDATION only. A failed reference gate does not become safe merely because it saves calls.','\n![Coverage/quality](../experiments/laya-first-v1/routing-coverage.png)']
    else:lines+=['\nRouting comparison and safe-coverage estimate pending. No coverage percentage is claimed.']
    lines+=['\n## Actual local speed, batching and prefix reuse']
    if batch:lines+=[table(['SDK batch','Notices/sec','Seconds','Label changes vs batch1'],[[x['sdk_batch_size'],round(x['notices_per_second'],3),round(x['wall_seconds'],2),x['label_changes_from_batch1']] for x in batch['results']]),f"\nSelected batch: {batch['selected_sdk_batch_size']}; batch-amortised latency is explicitly separate from completion latency."]
    if native:lines+=['\nGear 2 uses the exact same Qwen GGUF/native process as Gear 3, via the pinned Ollama internal native server. Class mapping A=YES(token32), B=NO(33), C=UNKNOWN(34), checked against official and native tokenizers. All three native alternatives are retained, then normalised over allowed token mass; this is `raw_model_probability`, not calibrated correctness.','\nAutomatic longest-prefix KV reuse is supported in one native slot. This is not a multi-branch encode-once API; full-generation calls may evict it. The private native endpoint is version-pinned and requires compatibility checks on upgrades.',table(['TRAIN case length','Cache enabled','Three-call wall ms','Native prompt cache tokens'],[[r['text_chars'],r['cache_prompt'],round(r['wall_ms']),[c['raw_runtime_response'].get('tokens_cached') for c in r['calls']]] for r in native['measurements']])]
    else:lines+=['\nFull constrained latency/cache benchmark pending. Initial real one-token probe succeeded (~2.8s cold-prefix on one short constructed source), which is not a workload latency estimate.']
    lines+=['\n## Evidence, reconciliation and confidence','\nGear 2 reuses an exact native Laya passage when both document predictions agree; otherwise one context-aware passage scoring call is attempted. The literal candidate and offsets are checked. Missing support escalates; unsupported quotations are never shown. Exact matching verifies quotation identity, not semantic entailment. Supersession/route conflicts remain review reasons.','\nGear 3 uses the pinned independent common semantic prompt, without Laya answers, preventing anchoring. Its output is schema/evidence-validated. Dates remain deterministic. Structure is optional and authoritative conflicts remain visible. Ordinary notices bypass ISO parsing.']
    if cal:lines+=[table(['Predicate','Calibration status'],[[k,v['status']] for k,v in cal.items()]),'\nCalibration population is synthetic only. Unsupported predicates keep null confidence and heuristic bands. Minimum decisive predicate trust is not a calibrated joint probability of final status.']
    else:lines+=['\nCalibration fitting/evaluation pending. All numeric correctness confidence is null.']
    if coverage:lines+=[table(['Threshold','Accepted / assertions','Coverage','Measured correctness','Review','Accepted critical misses'],[[r['threshold'],f"{r['accepted']}/{r['assertions']}",pct(r['coverage']),pct(r['measured_correctness']),pct(r['review_rate']),r['accepted_critical_false_negatives']] for r in coverage['coverage']]),'\n![Reliability](../experiments/laya-first-v1/calibration-reliability.png)']
    lines+=['\n## Frozen comparison, critical recall, repair/damage and oracles']
    for split in ['SYNTHETIC_FROZEN_TEST','ADVERSARIAL_TEST','OOD_TEST','CHALLENGE']:
        m=optional(STUDY/f'{split}-METRICS.json')
        if not m:lines+=[f'\n{split}: pending.'];continue
        lines+=['\n### '+split,table(['Condition','Correct / assertions','Supplied cases passed','Gear 2','Gear 3','Unresolved review'],[[name,f"{x['correct_assertions']}/{x['assertions']}",f"{x['cases_satisfying_supplied_assertions']}/{x['cases']}",pct(x['gear2_notice_rate']),pct(x['gear3_notice_rate']),pct(x['semantic_review_rate'])] for name,x in m.items() if name in ('cascade','full_qwen','laya','constrained')]),table(['Predicate','Positive support','Positive recall','False negatives','False positives'],[[k,x['positive_support'],pct(x['positive_recall']),x['positive_false_negatives'],x['positive_false_positives']] for k,x in m['cascade']['fields'].items() if k in PREDICATES]),f"\nAnalytical oracle totals (nine factorised semantic predicates only; excludes derived broad-other, dates and final status): `{json.dumps(m['oracle']['total'])}`. Per-predicate transition matrices are in `{split}-METRICS.json`. These perfect per-assertion routers are not deployable policies.",f"\nObserved escalation transitions: `{json.dumps(m['stage_transitions'])}`. Every final error is retained in `{split}-ERRORS.json`."]
    lines+=['\n## Actual 100 / 1,000-notice throughput']
    for n in [100,1000]:
        r=optional(STUDY/f'THROUGHPUT_{n}-MEASUREMENT.json')
        lines+=[f'\n{n} notices: '+(f"{r['total_measured_active_seconds']:.1f}s; {r['notices_per_hour']:.1f} notices/hour; {r['constrained_notice_calls']} Gear-2 and {r['full_qwen_calls']} full-Qwen calls; median/p95 service {r['median_service_latency_ms']:.1f}/{r['p95_service_latency_ms']:.1f} ms; {r['semantic_review_count']} semantically unresolved; all {n} still require review." if r else 'pending; no extrapolated throughput is presented.')]
    lines+=['\n## Training priority and remaining limits','\nNo weights are changed in this phase. Training priority requires validation evidence of repeatable specialist errors and a useful routing opportunity. Missing supervised narrow heads are a distinct limitation; a 92/95 authored Qwen ceiling alone does not justify Qwen fine-tuning.','\nISO/Prowide remains a separate future-feed adapter. The existing 7,683 public excerpts previously contained zero recognised ISO15022 structure. Public throughput data has no independent expert truth; it establishes speed and persistence only.','\nNo safe customer acceptance coverage, customer error rate or production readiness can be claimed from these synthetic/authored experiments. The next external quality gate requires representative independently expert-labelled real notices.','\n## Completion gate',f"\nCurrent persisted state: `{json.dumps(live,ensure_ascii=False)}`",'\nRegression/browser results are recorded separately in `REGRESSION-RESULTS.json` when executed. This report is deliberately a live report until every required measurement completes.']
    dest.write_text('\n\n'.join(lines)+'\n');plots(sel,coverage)
