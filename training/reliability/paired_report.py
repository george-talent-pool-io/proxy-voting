"""Post-freeze paired diagnostics; never selects models, rules or thresholds.

Refuses to read the frozen answer file until complete persisted predictions and
the operating freeze exist. All artifacts are private qualification material.
"""
import argparse
import json
import math
import statistics
from collections import Counter, defaultdict
from pathlib import Path

from training.framework.bundle import write, sha, jsonl
from semantic_pipeline.schema import PREDICATES
from semantic_pipeline.metrics import field_metrics
from qwen_domain.confidence import calibration_metrics


def lines(path):
    return [json.loads(s) for s in Path(path).read_text().splitlines() if s.strip()]


def load_completed(root, role):
    if not (root/'RESULT.json').exists() or not (root/'OPERATING_FREEZE.json').exists():
        raise ValueError('Complete frozen experiment required before post-hoc diagnostics')
    streams = {}
    for name in ('PRIMARY', 'HYBRID'):
        folder = root/(name+'-'+role)
        receipt = json.loads((folder/'PREDICTIONS_SAVED.json').read_text())
        if receipt['sha256'] != sha(folder/'predictions.jsonl'):
            raise ValueError('Persisted prediction drift')
        rows = lines(folder/'predictions.jsonl')
        if len(rows) != receipt['count'] or len({r['id'] for r in rows}) != len(rows):
            raise ValueError('Incomplete or duplicate predictions')
        for row in rows:
            h=__import__('hashlib').sha256(row['text'].encode()).hexdigest()
            if row['source_hash']!=h or row['result']['input_hash']!=h:
                raise ValueError('Source/model input hash mismatch')
        streams[name] = rows
    if [(r['id'], r['source_hash']) for r in streams['PRIMARY']] != [(r['id'], r['source_hash']) for r in streams['HYBRID']]:
        raise ValueError('Paired inputs differ')
    for a,b in zip(streams['PRIMARY'],streams['HYBRID']):
        h=__import__('hashlib').sha256(json.dumps(a['result']['llm_stage'],sort_keys=True).encode()).hexdigest()
        if b['result']['native_stage_replay']['stage_sha256']!=h:
            raise ValueError('Native generation replay hash mismatch')
    corpus = Path('data/qualification-corpora')/('fresh-evidence-v2-independent' if role == 'FROZEN_TEST' else 'fresh-evidence-v1')
    manifest = json.loads((corpus/'manifest.json').read_text())
    entry = manifest['files'][role]
    if sha(corpus/entry['labels']) != entry['labels_sha256']:
        raise ValueError('Protected truth drift')
    truth = {r['id']: r for r in lines(corpus/entry['labels'])}
    if set(truth) != {r['id'] for r in streams['PRIMARY']}:
        raise ValueError('Truth/prediction membership differs')
    return streams, truth


def values(result):
    return {k: result['predicates'][k]['value'] for k in PREDICATES}


def paired_analysis(primary, hybrid, truth):
    """Assertion-level oracle retains correct Laya; no deployment claim."""
    transitions = Counter()
    per_field = {k: Counter() for k in PREDICATES}
    errors = []
    raw = {'LAYA': defaultdict(list), 'QWEN': defaultdict(list), 'HYBRID': defaultdict(list)}
    perfect_calls = 0
    for a, b in zip(primary, hybrid):
        target = truth[a['id']]['expected']
        laya = values(b['result']['laya'])
        qwen = values(a['result'])
        combined = values(b['result'])
        invoked = bool((b['result'].get('llm') or {}).get('invoked'))
        any_error = False
        for k in PREDICATES:
            lc, qc, hc = laya[k] == target[k], qwen[k] == target[k], combined[k] == target[k]
            any_error |= not lc
            label = ('CORRECT' if lc else 'WRONG')+'_TO_'+('CORRECT' if hc else 'WRONG')
            transitions[label] += 1
            item = per_field[k]
            item['assertions'] += 1
            item['laya_correct'] += lc
            item['qwen_correct'] += qc
            item['hybrid_correct'] += hc
            item['oracle_correct'] += lc or qc
            item['laya_errors'] += not lc
            item['llm_capable_repairs'] += not lc and qc
            item['actual_invoked'] += invoked
            if invoked:
                item[label] += 1
            item['AGREE_CORRECT' if laya[k] == qwen[k] and lc else 'AGREE_WRONG' if laya[k] == qwen[k] else
                 'DISAGREE_LAYA_CORRECT' if lc else 'DISAGREE_QWEN_CORRECT' if qc else 'DISAGREE_BOTH_WRONG'] += 1
            for model, prediction in [('LAYA', laya[k]), ('QWEN', qwen[k]), ('HYBRID', combined[k])]:
                raw[model][k].append((target[k], prediction))
            if not all((lc, qc, hc)):
                errors.append({'id': a['id'], 'field': k, 'truth': target[k], 'text': a['text'],
                    'laya': b['result']['laya']['predicates'][k], 'qwen': a['result']['predicates'][k],
                    'hybrid': b['result']['predicates'][k], 'hybrid_llm_invoked': invoked,
                    'escalation': b['result']['escalation'], 'conflicts': b['result']['reconciliation']['conflicts']})
        perfect_calls += any_error
    metrics = {name: {k: field_metrics([x[0] for x in pairs], [x[1] for x in pairs],
                                      'VOTABLE' if k == 'votability' else 'YES') for k, pairs in fields.items()}
               for name, fields in raw.items()}
    return {'assertions': len(primary)*len(PREDICATES), 'cases': len(primary),
            'all_case_transitions': dict(transitions), 'per_predicate': {k: dict(v) for k,v in per_field.items()},
            'oracle_notice_calls': perfect_calls,
            'oracle_correct_assertions': sum(v['oracle_correct'] for v in per_field.values()),
            'oracle_scope': 'Perfect knowledge of raw Laya errors; retain correct Laya and take independent Qwen only where it repairs. Analytical upper bound, not a router.',
            'hybrid_logical_llm_calls': sum(bool((r['result'].get('llm') or {}).get('invoked')) for r in hybrid),
            'physical_qwen_generations': len(primary), 'metrics': metrics, 'errors': errors}


def confidence_analysis(rows, truth, risk, calibrator=None):
    by_id = {r['id']:r for r in rows}
    output = {}
    for key in (*PREDICATES, 'final_decision'):
        pairs = [];unsupported=Counter()
        for row in risk:
            p = row['predicate_confidence'][key]
            if p is not None:
                actual = by_id[row['id']]['result']
                t = truth[row['id']]
                ok = actual['decision']['classification'] == t['final_status'] if key == 'final_decision' else actual['predicates'][key]['value'] == t['expected'][key]
                pairs.append((ok, p))
            elif calibrator:
                from training.reliability.production_study import feature
                from production.confidence import stratum
                f=feature(by_id[row['id']],key);model=calibrator['models'].get(key)
                if f['force_review']:reason='EVIDENCE_CONFLICT_OR_OOD_REVIEW_GUARD'
                elif not model:reason='CALIBRATOR_NOT_VALIDATED'
                elif f['features']['prediction'] not in model.get('prediction_values',[]):reason='PREDICTION_CLASS_SUPPORT_INSUFFICIENT'
                elif stratum(f['features']) not in model.get('supported_strata',[]):reason='SOURCE_EVIDENCE_STRATUM_SUPPORT_INSUFFICIENT'
                else:reason='OTHER_CALIBRATION_SCOPE_GUARD'
                unsupported[reason]+=1
        output[key] = {'available':len(pairs),'total':len(rows),'availability':len(pairs)/len(rows),
            'unsupported_reasons':dict(unsupported),
            'held_out_supported_subset_metrics':calibration_metrics([p[0] for p in pairs],[p[1] for p in pairs]) if pairs else None}
    complete = sum(r['confidence'] is not None for r in risk)
    unresolved = sum(t['expected']['votability']=='UNCERTAIN' or
        (t['expected']['votability']=='VOTABLE' and (any(v=='UNKNOWN' for v in t['expected'].values()) or t['deadline_status']=='UNKNOWN'))
        for t in truth.values())
    return {'fields':output,'all_field_screening_score_available':complete,
            'screening_score_definition':'Minimum of supported field/decision correctness estimates. Not a calibrated joint all-fields-correct probability.',
            'truth_unresolved_records':unresolved,'truth_review_floor':unresolved/len(rows),
            'forced_review':sum(r['force_review'] for r in risk),
            'automation_enabled':False}


def latency(rows):
    ms = [r['request_ms'] for r in rows]
    diagnostics = [r['result'].get('llm',{}).get('generation_diagnostics',{}) for r in rows]
    return {'requests':len(ms),'median_seconds':statistics.median(ms)/1000,
            'mean_seconds':statistics.mean(ms)/1000,'min_seconds':min(ms)/1000,'max_seconds':max(ms)/1000,
            'p95_seconds':sorted(ms)[math.ceil(.95*len(ms))-1]/1000,
            'sequential_requests_per_hour_excluding_persistence':3600000/statistics.mean(ms),
            'max_reported_mlx_allocated_bytes':max(d.get('peak_mlx_allocated_bytes') or 0 for d in diagnostics),
            'scope':'Actual primary requests including lazy loads. General-purpose Mac; model-allocation diagnostics are not OS-wide peak unified memory.'}


def evidence_quality(rows):
    counts=Counter()
    for row in rows:
        llm=row['result'].get('llm') or {};schema=llm.get('schema_handling') or {}
        if llm.get('invoked'):
            counts['llm_invocations']+=1
            counts['first_pass_schema_success']+=bool(schema.get('first_pass_success'))
            counts['repair_attempts']+=schema.get('repair_attempts',0)
            counts['repair_success']+=bool(schema.get('repair_success'))
            counts['final_schema_failure']+=not llm.get('valid')
        for k in PREDICATES:
            pred=row['result']['predicates'][k];evidence=pred.get('evidence',[])
            counts['semantic_fields']+=1
            counts['fields_with_evidence']+=bool(evidence)
            counts['fields_without_quote']+=not bool(evidence)
            for e in evidence:
                exact=isinstance(e.get('text'),str) and bool(e['text']) and e['text'] in row['text']
                counts['quotations']+=1;counts['exact_source_matches']+=exact
                counts['invalid_source_quotations']+=not exact
                if e.get('valid') and not exact:raise ValueError('Displayed evidence is not an exact source substring')
    return {**dict(counts),'scope':'Canonical displayed evidence; exact match proves provenance, not entailment. Absence may be supported by an explicit complete-source-negative basis.'}


def plots(out, reports, root):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    palette={'PRIMARY':'#244d70','HYBRID':'#ad713a'}
    fig,axes=plt.subplots(2,5,figsize=(17,7),layout='constrained')
    for key,ax in zip((*PREDICATES,'final_decision'),axes.flat):
        ax.plot([0,1],[0,1],'--',color='#a8b1ba',linewidth=1)
        measured=False
        for name,color in palette.items():
            detail=reports['FROZEN_TEST']['confidence'][name]['fields'][key]
            q=detail['held_out_supported_subset_metrics']
            if q:
                bins=[b for b in q['bins'] if b['n']]
                ax.plot([b['mean_probability'] for b in bins],
                        [b['observed_correctness'] for b in bins],'o-',color=color,
                        label=f"{name} n={detail['available']}")
                measured=True
        if not measured:ax.text(.5,.5,'Numerical confidence\nunsupported',ha='center',va='center',fontsize=8)
        ax.set(xlim=(0,1),ylim=(0,1),title=key.replace('_',' '))
        ax.tick_params(labelsize=7);ax.title.set_size(8)
        if measured:ax.legend(fontsize=6,loc='lower right')
    fig.supxlabel('Scoped correctness estimate; constant estimators do not rank individual cases')
    fig.supylabel('Observed correctness on supported held-out cases')
    fig.suptitle('AI-authored frozen benchmark · confidence availability varies · no customer accuracy claim',fontsize=12)
    fig.savefig(out/'frozen-confidence-reliability.svg');plt.close(fig)
    fig,axes=plt.subplots(1,2,figsize=(11,4),layout='constrained')
    for name,color in palette.items():
        curve=json.loads((root/(name+'-FROZEN_TEST')/'coverage-curve.json').read_text())
        x=[p['threshold'] for p in curve]
        axes[0].plot(x,[100*p['coverage'] for p in curve],'o-',color=color,label=name)
        axes[1].plot(x,[100*p['correctness'] if p['correctness'] is not None else float('nan') for p in curve],
                     'o-',color=color,label=name)
    axes[0].set(title='Diagnostic coverage',ylabel='Accepted records (%)',xlabel='Screening threshold',ylim=(0,100))
    axes[1].set(title='Correctness among diagnostic acceptances',ylabel='All fields + deadline + status correct (%)',xlabel='Screening threshold',ylim=(0,101))
    for ax in axes:ax.legend(fontsize=8)
    fig.suptitle('AI-authored frozen benchmark · thresholds are diagnostics, not automation permission',fontsize=11)
    fig.savefig(out/'frozen-screening-coverage.svg');plt.close(fig)


def run(path):
    root=Path(path);out=root/'diagnostics';out.mkdir(exist_ok=False)
    reports={};md=['# Paired frozen-release diagnostic report',
        'AI-authored English controlled data. No customer accuracy or automation authorisation. No post-hoc changes to model, prompt, calibration or operating point.']
    for role in ('VALIDATION','FROZEN_TEST'):
        streams,t=load_completed(root,role)
        a=paired_analysis(streams['PRIMARY'],streams['HYBRID'],t)
        errors=a.pop('errors');jsonl(out/(role+'-errors.jsonl'),errors)
        confidences={name:confidence_analysis(rows,t,lines(root/(name+'-'+role)/'confidence.jsonl'),
            json.loads((root/(name+'-CALIBRATION')/'calibrator.json').read_text())) for name,rows in streams.items()}
        reports[role]={'paired':a,'confidence':confidences,'primary_latency':latency(streams['PRIMARY']),
                       'evidence_and_schema':{name:evidence_quality(rows) for name,rows in streams.items()}}
        md += ['\n## '+role,'\n| Predicate | Laya correct | Qwen correct | Hybrid correct | Laya→Qwen oracle | Total |',
               '|---|---:|---:|---:|---:|---:|']
        for k,v in a['per_predicate'].items():
            md.append(f"| {k} | {v['laya_correct']} | {v['qwen_correct']} | {v['hybrid_correct']} | {v['oracle_correct']} | {v['assertions']} |")
        md += [f"\nHybrid logical LLM calls: {a['hybrid_logical_llm_calls']}/{a['cases']}. One physical primary generation per case was reused; hybrid replay times exclude Qwen generation and are not end-to-end latency.",
               '\nEvery semantic error by any condition is in `'+role+'-errors.jsonl`. Published final-status and deadline errors remain in each architecture’s `metrics.json`.']
    write(out/'summary.json',reports)
    plots(out,reports,root)
    (out/'REPORT.md').write_text('\n'.join(md)+'\n')
    return reports


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('experiment');a=p.parse_args();run(a.experiment)
