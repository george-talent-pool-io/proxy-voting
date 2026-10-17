"""Publish measured progress and held-out confidence diagnostics only."""
import json,statistics
from collections import Counter,defaultdict
from qwen_domain.protocol import ROOT,STUDY,CORPUS,read,rows,write,now,sha
from qwen_domain.confidence import CorrectnessCalibrator,confidence_output,calibration_metrics

def atomic(path,value):
    temp=path.with_suffix(path.suffix+'.tmp');temp.write_text(json.dumps(value,ensure_ascii=False,indent=2,allow_nan=False)+'\n');temp.replace(path)

def confidence_diagnostics(architecture,split='CALIBRATION'):
    m=read(CORPUS/'MANIFEST.json');truth={r['id']:r for r in rows(CORPUS/m['splits'][split]['labels'])}
    predictions=rows(STUDY/'predictions'/f'{architecture}-{split}.jsonl');cal=CorrectnessCalibrator.load(STUDY/f'{architecture}-calibrator.joblib',predictions[0]['result']['model_identity']);observations=[]
    for p in predictions:
        t=truth[p['id']]
        if split=='CALIBRATION' and t['calibration_fold']!='EVALUATION':continue
        for key,c in p['result']['confidence'].items():
            f=c['features'];prob=None if c['force_review'] else cal.predict(key,f,p['result']['model_identity'])
            observations.append({'id':p['id'],'predicate':key,'correct':c['value']==t['expected'][key],'probability':prob,'critical_false_negative':key in ('votability','share_blocking','poa_required','registration_required') and t['expected'][key] in ('YES','VOTABLE') and c['value']!=t['expected'][key]})
    curve=[]
    for threshold in [.7,.8,.9,.95,.98]:
        accepted=[r for r in observations if r['probability'] is not None and r['probability']>=threshold]
        curve.append({'threshold':threshold,'assertions':len(observations),'accepted_assertions':len(accepted),'coverage':len(accepted)/len(observations),
            'measured_correctness':sum(r['correct'] for r in accepted)/len(accepted) if accepted else None,'review_rate':1-len(accepted)/len(observations),'accepted_critical_false_negatives':sum(r['critical_false_negative'] for r in accepted),'note':'Would-accept simulation; automation remains disabled. Predicate assertions, not whole-notice automation.'})
    valid=[r for r in observations if r['probability'] is not None]
    result={'architecture':architecture,'split':split,'evaluation_only':True,'scope':'Synthetic population only','coverage':curve,'reliability':calibration_metrics([r['correct'] for r in valid],[r['probability'] for r in valid]),'numeric_confidence_available':len(valid),'assertions':len(observations)}
    result['by_predicate']={}
    for key in sorted({r['predicate'] for r in observations}):
        rs=[r for r in observations if r['predicate']==key];vs=[r for r in rs if r['probability'] is not None]
        result['by_predicate'][key]={'assertions':len(rs),'numeric_confidence_available':len(vs),'reliability':calibration_metrics([r['correct'] for r in vs],[r['probability'] for r in vs]),
            'coverage':[{'threshold':threshold,'accepted':sum(r['probability'] is not None and r['probability']>=threshold for r in rs),'critical_false_negatives':sum(r['critical_false_negative'] and r['probability'] is not None and r['probability']>=threshold for r in rs)} for threshold in [.7,.8,.9,.95,.98]]}
    path=STUDY/f'{architecture}-{split}-CONFIDENCE-DIAGNOSTICS.json'
    if not path.exists():write(path,result)
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    figure,axes=plt.subplots(1,2,figsize=(10,4),layout='constrained');bins=result['reliability']['bins']
    axes[0].plot([0,1],[0,1],color='#9aabbb',linestyle='--')
    if bins:axes[0].scatter([b['mean_probability'] for b in bins],[b['observed_correctness'] for b in bins],color='#287f79')
    else:axes[0].text(.5,.4,'No supported numerical confidence',ha='center',wrap=True)
    axes[0].set(xlabel='Predicted correctness probability',ylabel='Held-out observed correctness',xlim=(0,1),ylim=(0,1),title='Synthetic reliability')
    axes[1].plot([r['threshold'] for r in curve],[r['coverage'] for r in curve],label='Predicate coverage',color='#287f79')
    points=[r for r in curve if r['measured_correctness'] is not None]
    if points:axes[1].plot([r['threshold'] for r in points],[r['measured_correctness'] for r in points],label='Observed correctness',color='#526477')
    axes[1].set(xlabel='Confidence threshold',ylabel='Fraction of assertions',ylim=(0,1),title='Would-accept simulation; automation disabled');axes[1].legend()
    for suffix in ['svg','png']:figure.savefig(STUDY/f'{architecture}-{split}-confidence.{suffix}',dpi=160)
    plt.close(figure)
    return result

def publish_progress(state,stage,**extra):
    counts={p.stem:sum(1 for _ in p.open()) for p in (STUDY/'predictions').glob('*.jsonl')}
    atomic(STUDY/'LIVE-STATUS.json',{'timestamp':now(),'state':state,'stage':stage,'persisted_rows':counts,'automation_enabled':False,'customer_accuracy':None,**extra})

def reports():
    """Safe to call before completion: absence of artifacts remains explicit."""
    live=read(STUDY/'LIVE-STATUS.json') if (STUDY/'LIVE-STATUS.json').exists() else {'state':'PREPARING','stage':'Formal benchmark not yet started'}
    manifest=read(CORPUS/'MANIFEST.json');decision=read(STUDY/'TRAINING-DECISION.json') if (STUDY/'TRAINING-DECISION.json').exists() else None
    scored=read(STUDY/'SCORED.json') if (STUDY/'SCORED.json').exists() else None
    summary={'created_at':now(),'state':live,'splits':{k:{q:v[q] for q in ('n','groups','languages','difficulty')} for k,v in manifest['splits'].items()},'training_decision':decision['status'] if decision else 'PENDING_BASE_AND_CONSTRAINED_VALIDATION','frozen_metrics':scored,'automation_enabled':False,'customer_accuracy':None}
    atomic(STUDY/'SUMMARY.json',summary)
    lines=['# Qwen domain optimisation','',f"State: **{live['state']}** — {live['stage']}.",'','Automation is disabled. Customer/production accuracy is UNKNOWN. This report is updated from persisted artifacts; an unfinished run is not a completed result.','',
        '## Corpus and truth','', '5,760 unique fact-first constructed texts, 2,880 controlled pairs, six languages, 48 generation families. Authored semantic atoms are composed by deterministic software; these are not 5,760 independent frontier-model generations or domain-expert reviews. English is the primary confidence population. Foreign-language writing has not been certified by native domain experts.','',
        '| Split | Records | Duplicate/family groups | Languages |','|---|---:|---:|---|']
    for k,v in manifest['splits'].items():lines.append(f"| {k} | {v['n']} | {v['groups']} | {v['languages']} |")
    lines+=['','Exact hashes, lexical MinHash/Jaccard and full-document chunk-mean local MiniLM checks group notices before splitting. Minimal pairs and generation families stay together. English MiniLM is not a guarantee of multilingual semantic equivalence. Only a few independent held-out families remain; atom reuse limits external validity. Earlier rejected drafts are preserved and were not benchmarked for model selection.','',
        'TRAIN and VALIDATION labels have separate loaders. Frozen/OOD/adversarial answer paths are physically separate and rejected by training loaders. Sealed base predictions may be collected before any training, but frozen answer scoring waits for a final model-selection freeze. This resolves the plan’s base-benchmark/model-selection ordering without using test errors to choose training.','',
        '## Exact model and baseline','', 'The immutable QWEN_DIRECT_PRE_DOMAIN_TRAINING manifest pins the installed Qwen3.8:27b-q4_K_M digest, upstream Qwen/Qwen3.8-27B lineage, original common prompt, schema, normalization, rules, checkpoints and historical predictions. Historical Direct achieved92/95 labelled assertions and54/57 case conjunctions; only4 cases supplied a final-status label. It is not customer accuracy. No Laya weights were changed.','',
        '## Benchmark, training and calibration','',f"Training decision: **{summary['training_decision']}**.",'',
        'Normal Qwen uses independent mode and receives no Laya outputs. Constrained Qwen uses the identical installed language weights through a pinned local llama.cpp runtime. It receives no labels. Both use the same ten-field truth and deterministic deadline reference. All native requests, scores, evidence, latency and schema outcomes are persisted. All-predicate exact match excludes the separately reported derived customer status.','',
        'Numerical confidence is null before support and held-out calibration gates pass. HIGH/MEDIUM/LOW/UNRESOLVED are heuristic bands. Correctness calibrators fit only CALIBRATION/FIT and are evaluated on disjoint duplicate groups in CALIBRATION/EVALUATION. Unsupported languages/OOD/conflicts/schema failures force review. Minimum decisive-predicate confidence is a trust score, not a calibrated joint decision probability.','',
        'No domain adapter, learning curve, base/domain repair result, completed stability estimate or calibrated performance is claimed unless the corresponding committed artifact exists. If validation establishes a training target, the run stops short of model selection until data and exact-checkpoint trainer compatibility are audited. Full27B bf16 weights alone need approximately54GB; full-precision training is unsuitable for comfortable64GB operation. Quantized LoRA feasibility remains to be demonstrated.','',
        '## Current measured artifacts','',f"Persisted benchmark rows: `{live.get('persisted_rows',{})}`.",'',
        ('Formal normal/constrained frozen metrics have been committed below. Other completed artifacts must be inspected separately; no domain adapter is implied.' if scored else 'The complete formal normal-vs-constrained benchmark, consistency study, calibrated coverage curves, final training decision and independent frozen evaluation remain pending while their jobs run.')+' Preflight measurements are software/TRAIN probes and do not establish held-out model quality.','',
        '## Parser addendum','', 'Prowide is implemented as a local isolated JVM adapter, but disabled in the frozen primary domain experiment. It introduces no new prompt/data condition here. The separate ISO15022_PROWIDE_EVALUATION report records parser/recovery tests and the7,683-record verification. No parser/source transformation is retroactively applied to historical Qwen results.','',
        '## What remains unproven','', 'Synthetic and AI-assisted labels do not establish customer accuracy, customer calibration or production readiness. Independently expert-labelled representative real notices remain the highest-value external validation. Automation remains false, even if a synthetic calibration gate passes.']
    if scored:
        lines+=['','## Frozen results','', '| Dataset | Architecture | Correct / assertions | All-field exact / records |','|---|---|---:|---:|']
        for split,arms in scored.items():
            for a,m in arms.items():lines.append(f"| {split} | {a} | {m['correct_assertions']} / {m['assertions']} | {m['ALL_PREDICATES_EXACT_MATCH']} / {m['n']} |")
        lines+=['','Per-field supports, confusion matrices and every failure are in SCORED.json; no predicate is silently excluded.']
    (ROOT/'data/reports/QWEN_DOMAIN_OPTIMISATION.md').write_text('\n'.join(lines)+'\n')
    return summary
