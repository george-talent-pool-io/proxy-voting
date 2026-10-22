"""Report only completed immutable prediction/answer receipts; no selection."""
import json
from pathlib import Path
from training.framework.bundle import write,sha
from scripts.qualify_frozen_learning import lines
from semantic_pipeline.schema import PREDICATES
from production import operating
from qwen_domain.confidence import calibration_metrics
from training.reliability.production_study import ROOT,CORPUS,answers


def run():
    summary={};errors=['# Fresh evidence-routing qualification errors\n',
        'AI-authored controlled data; not customer accuracy. Complete source, stages and scores are retained below.\n']
    records={}
    for name in ('SPECIALIST','HYBRID'):
        source=ROOT/(name+'-FROZEN_TEST');predictions=lines(source/'predictions.jsonl')
        truth=answers('FROZEN_TEST',source/'PREDICTIONS_SAVED.json')
        confidence_rows=lines(source/'confidence.jsonl');by_id={r['id']:r for r in confidence_rows}
        metrics=json.loads((source/'metrics.json').read_text())
        cal=json.loads((ROOT/(name+'-CALIBRATION')/'calibrator.json').read_text())
        quality={}
        for key in (*PREDICATES,'final_decision'):
            supported=[r for r in predictions if by_id[r['id']]['predicate_confidence'][key] is not None]
            correct=[r['result']['decision']['classification']==truth[r['id']]['final_status'] if key=='final_decision' else
                     r['result']['predicates'][key]['value']==truth[r['id']]['expected'][key] for r in supported]
            quality[key]={**calibration_metrics(correct,[by_id[r['id']]['predicate_confidence'][key] for r in supported]),
                          'available':len(supported),'total':len(predictions)}
        write(source/'calibration-quality.json',quality)
        llm=[r for r in predictions if (r['result'].get('llm') or {}).get('invoked')]
        valid_quotes=[e for r in predictions for k in PREDICATES for e in r['result']['predicates'][k].get('evidence',[]) if e.get('valid')]
        llm_flags=[(r['result'].get('llm') or {}).get('schema_handling',{}) for r in llm]
        summary[name]={'metrics':metrics,'confidence_available_all_fields_and_decision':sum(r['confidence'] is not None for r in confidence_rows),
            'calibration_quality':quality,'llm_invocations':len(llm),'records':len(predictions),'llm_invocation_rate':len(llm)/len(predictions),
            'schema_first_pass_success':sum(f.get('first_pass_success',False) for f in llm_flags),
            'schema_repairs':sum(f.get('repair_attempts',0) for f in llm_flags),
            'schema_final_failures':sum(not r['result']['llm']['valid'] for r in llm),
            'verified_quotation_count':len(valid_quotes),
            'operating':json.loads((source/'operating-evaluation.json').read_text()),
            'coverage_curve':json.loads((source/'coverage-curve.json').read_text()),
            'latency':json.loads((source/'PREDICTIONS_SAVED.json').read_text()),
            'calibration_reports':cal['reports']}
        records[name]={r['id']:r for r in predictions}
    transitions={};rows=[]
    for key in PREDICATES:
        counts={k:0 for k in ('REPAIR','DAMAGE','BOTH_CORRECT','BOTH_WRONG')}
        for ident,a in records['SPECIALIST'].items():
            b=records['HYBRID'][ident];expected=truth[ident]['expected'][key]
            left=a['result']['predicates'][key]['value']==expected;right=b['result']['predicates'][key]['value']==expected
            category='REPAIR' if not left and right else 'DAMAGE' if left and not right else 'BOTH_CORRECT' if left else 'BOTH_WRONG'
            counts[category]+=1
            if not left or not right:
                errors.extend([f'\n## {ident} — {key}\n',f'```text\n{a["text"]}\n```\n',f'Truth: `{expected}`.\n',
                    '```json\n'+json.dumps({'SPECIALIST':a['result']['predicates'][key],'HYBRID':b['result']['predicates'][key],
                    'llm_invoked':bool(b['result'].get('llm')),'llm':b['result'].get('llm'),
                    'reconciliation':b['result']['reconciliation']},ensure_ascii=False,indent=2)+'\n```\n'])
        transitions[key]=counts
    for ident,a in records['SPECIALIST'].items():
        b=records['HYBRID'][ident];expected=truth[ident]['final_status']
        if a['result']['decision']['classification']!=expected or b['result']['decision']['classification']!=expected:
            errors.extend([f'\n## {ident} — final status\n',f'```text\n{a["text"]}\n```\n',
                '```json\n'+json.dumps({'truth':expected,'SPECIALIST':a['result']['decision'],
                    'HYBRID':b['result']['decision'],'conflicts':b['result']['reconciliation']['conflicts']},indent=2)+'\n```\n'])
    write(ROOT/'FRESH_REPAIR_DAMAGE.json',transitions)
    (ROOT/'FRESH_ERRORS.md').write_text('\n'.join(errors))
    write(ROOT/'FRESH_RESULTS.json',summary)
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    fig,axes=plt.subplots(1,2,figsize=(11,4),layout='constrained')
    for name,s in summary.items():
        c=s['coverage_curve'];axes[0].plot([r['threshold'] for r in c],[r['coverage']*100 for r in c],marker='o',label=name)
        axes[1].plot([r['coverage']*100 for r in c],[r['correctness']*100 if r['correctness'] is not None else float('nan') for r in c],marker='o',label=name)
    axes[0].set(xlabel='Diagnostic confidence threshold',ylabel='Supported would-accept coverage (%)',ylim=(-1,101))
    axes[1].set(xlabel='Supported would-accept coverage (%)',ylabel='Observed complete-output correctness (%)',ylim=(-1,101))
    for ax in axes:ax.grid(alpha=.2);ax.legend()
    fig.suptitle('AI-authored held-out benchmark · diagnostic curves, no automation approval')
    fig.savefig(ROOT/'fresh-confidence-coverage.png',dpi=160)
    plt.close(fig)
    return {k:{'assertions':v['metrics']['correct_assertions'],'final_status':v['metrics']['final_status'],
               'llm_calls':v['llm_invocations'],'operating':v['operating']} for k,v in summary.items()}


if __name__=='__main__':print(json.dumps(run(),indent=2))
