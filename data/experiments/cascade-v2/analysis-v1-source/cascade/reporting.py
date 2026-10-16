"""Post-freeze analysis. Never feeds labels or challenge results into selection."""
import copy,json,statistics,hashlib
from collections import Counter,defaultdict
from pathlib import Path
from sklearn.metrics import roc_auc_score
from semantic_pipeline.experiment import lines,read,write,append,sha,now
from semantic_pipeline.metrics import observed,truth,summarize,field_metrics
from semantic_pipeline.pipeline import prepare,resolve_deadline,diagnostic
from semantic_pipeline.reconcile import reconcile
from semantic_pipeline.decision import decide
from semantic_pipeline.schema import PREDICATES
from cascade.study import ROOT,OLD,verify_core,model_metrics
from cascade.fallback import CommonFallback
from evaluation.ae_scoring import project
CONDITIONS=['A','B','D1','D2','D3','C1','C2','C3','C_SELECTIVE','E_SELECTIVE','E_AGGREGATION_ONLY']

def persist(name,value):
    path=ROOT/name
    if not path.exists():write(path,value)
    return read(path)
def load(dataset,condition):
    rs=lines(ROOT/f'{dataset}-{condition}.jsonl')
    if condition.startswith('C'):rs=project(rs,'C')[0]
    return sorted(rs,key=lambda r:r['id'])
def fmt(v):return 'N/A' if v is None else f'{v:.1%}'
def med(v):return statistics.median(v) if v else None
def expected_rows(dataset):return 57 if dataset=='challenge' else 48

def warmup_stats():
    """Native load timings distinguish actual reloads from retained-model warmups."""
    groups=defaultdict(list)
    for row in lines(ROOT/'COLD-WARMUP-CALLS.jsonl'):
        result=row['result'];raw=result.get('raw_response') or {}
        groups[row['condition']].append({'dataset':row['dataset'],'timestamp':row['timestamp'],
            'latency_ms':result['latency_ms'],'native_load_ms':raw.get('load_duration',0)/1e6,
            'valid':result['valid'],'request_model':result.get('request',{}).get('model')})
    return {'per_condition':dict(groups),'scope':'Preparatory warmup calls excluded from warmed architecture latencies. Retained-model warmups are not cold starts; native load_duration identifies actual reload cost.'}

def inference_stats(rows):
    calls=[r['result']['llm'] for r in rows if (r['result'].get('llm') or {}).get('invoked')]
    timings=sorted(l['latency_ms'] for l in calls);schema=Counter();evidence=Counter();tokens=Counter();failure_kinds=Counter();rates=[];first=[]
    for l in calls:
        schema.update({k:int(v) for k,v in l.get('schema_handling',{}).items()})
        attempt=l.get('first_attempt') or l
        if not attempt.get('valid'):
            raw_first=attempt.get('raw_response')
            kind='RUNTIME_OR_CONTEXT_FAILURE' if not raw_first else 'INCOMPLETE_GENERATION' if raw_first.get('done_reason')!='stop' else 'SCHEMA_FAILURE'
            failure_kinds[kind]+=1
        for name in ('raw_response','repair_raw_response'):
            raw=l.get(name)
            if not raw:continue
            tokens['prompt_tokens']+=raw.get('prompt_eval_count',0);tokens['total_generated_tokens_including_reasoning']+=raw.get('eval_count',0)
            if raw.get('eval_duration'):rates.append(raw.get('eval_count',0)/(raw['eval_duration']/1e9))
            t=raw.get('thinking_diagnostics',{});tokens['reasoning_characters']+=t.get('characters',0)
            if t.get('time_to_first_token_ms') is not None:first.append(t['time_to_first_token_ms'])
        if l.get('valid'):
            for k,quotes in l['evidence_validation']['predicates'].items():
                evidence['quotes_supplied']+=len(quotes);evidence['exact_match']+=sum(q['valid'] for q in quotes)
                evidence['invalid_quotes']+=sum(not q['valid'] for q in quotes)
                evidence['missing_positive_evidence']+=l['parsed'][k] in ('YES','VOTABLE','NOT_VOTABLE') and not any(q['valid'] for q in quotes)
    times=[r['result']['latencies']['total_ms'] for r in rows]
    return {'llm_calls':len(calls),'llm_call_rate':len(calls)/len(rows),'median_llm_ms':med(timings),'p95_llm_ms':timings[min(len(timings)-1,int(.95*len(timings)))] if timings else None,
        'schema':dict(schema),'first_pass_failure_categories':dict(failure_kinds),'evidence':dict(evidence),'tokens':dict(tokens),'median_generated_tokens_per_second':med(rates),'median_time_to_first_token_ms':med(first),
        'native_reasoning_tokens':'NOT_EXPOSED_SEPARATELY; eval_count includes reasoning and final answer','records_per_second':len(rows)/(sum(times)/1000),
        'scope':'Actual sequential warmed end-to-end latency; model reload warmups recorded separately. No cached LLM outputs in timed arms.'}

def before_result(row):
    r=copy.deepcopy(row['result']);p=prepare(row['text'],r.get('parser') is not None)
    merged=reconcile(p['structured'],r['laya'],None);deadline=resolve_deadline(row['text'],p)
    r.update(reconciliation=merged,deadline=deadline,decision=decide(merged['predicates'],deadline,merged['conflicts'],p['quarantined']))
    return r

def transition(rows):
    per=defaultdict(Counter);accepted=[];matrix=Counter()
    for row in rows:
        r=row['result'];before=observed(before_result(row));after=observed(r);gold=truth(row['expected']);invoked=bool((r.get('llm') or {}).get('invoked'))
        passed_before=all(before.get(k)==v for k,v in gold.items());passed_after=all(after.get(k)==v for k,v in gold.items())
        if invoked:matrix[f'{"correct" if passed_before else "wrong"} -> {"correct" if passed_after else "wrong"}']+=1
        else:accepted.append({'id':row['id'],'text':row['text'],'all_supplied_assertions_correct':passed_after,
            'indecisive_fast_path':r['decision']['classification']=='UNCERTAIN_MANUAL_REVIEW','failures':{k:{'expected':v,'predicted':after.get(k)} for k,v in gold.items() if after.get(k)!=v},
            'predicates':r['laya']['predicates']})
        if not invoked:continue
        for k,v in gold.items():
            if k not in PREDICATES and k!='other_restriction':continue
            per[k][f'{"correct" if before.get(k)==v else "wrong"} -> {"correct" if after.get(k)==v else "wrong"}']+=1
    total=Counter()
    for c in per.values():total.update(c)
    return {'semantic_transitions':dict(total),'per_predicate':dict(per),'case_transitions':dict(matrix),
        'fast_path_count':len(accepted),'fast_path_correct':sum(a['all_supplied_assertions_correct'] for a in accepted),
        'fast_path_indecisive_count':sum(a['indecisive_fast_path'] for a in accepted),'every_fast_path_record':accepted}

def paired_comparison(arms,pair):
    left,right=pair;by={a:{r['id']:r for r in arms[a]} for a in pair};counts=defaultdict(Counter);diff=[]
    for ident,row in by[left].items():
        y=truth(row['expected']);a=observed(row['result']);b=observed(by[right][ident]['result'])
        for k,v in y.items():
            ca=a.get(k)==v;cb=b.get(k)==v;counts[k]['both_correct' if ca and cb else 'left_only_correct' if ca else 'right_only_correct' if cb else 'both_wrong']+=1
            if a.get(k)==b.get(k):continue
            def evidence(r):
                l=r['result'].get('llm') or {};validation=l.get('evidence_validation') or {}
                return {'parsed_output':l.get('parsed'),'predicate_evidence':validation.get('predicates',{}).get(k,[]),'deadline':validation.get('deadline'),'reconciled':r['result']['reconciliation']['predicates'].get(k)}
            diff.append({'id':ident,'source':row['text'],'field':k,'truth':v,'left':left,'left_result':a.get(k),'left_correct':ca,'left_evidence':evidence(row),
                'right':right,'right_result':b.get(k),'right_correct':cb,'right_evidence':evidence(by[right][ident])})
    total=Counter()
    for m in counts.values():total.update(m)
    return {'pair':pair,'per_predicate':dict(counts),'all_assertions':dict(total),'disagreements':diff,
        'TWO_LLM_ORACLE':{'correct':total['both_correct']+total['left_only_correct']+total['right_only_correct'],'assertions':sum(total.values()),'deployable':False}}

def oracle_models(arms,specialists):
    d2={r['id']:r for r in arms['D2']};d3={r['id']:r for r in arms['D3']};cap={r['id']:r for r in specialists};fields=defaultdict(Counter)
    for ident,row in d2.items():
        laya=cap[ident]['capable'];p=prepare(row['text'],False);merged=reconcile({},laya,None);deadline=resolve_deadline(row['text'],p)
        native={'reconciliation':merged,'deadline':deadline,'decision':decide(merged['predicates'],deadline,merged['conflicts'])}
        values=[observed(native),observed(row['result']),observed(d3[ident]['result'])]
        for k,v in truth(row['expected']).items():
            fields[k]['assertions']+=1;fields[k]['laya_correct']+=values[0].get(k)==v
            fields[k]['oracle_correct']+=any(x.get(k)==v for x in values)
    total=Counter()
    for m in fields.values():total.update(m)
    return {'name':'LAYA_QWEN_DIRECT_THINKING_ORACLE','deployable':False,'per_predicate':dict(fields),'all_assertions':dict(total),
        'scope':'Optimistic assertion-wise choice among capable specialist, independent Direct and independent Thinking; not necessarily one coherent final record.'}

def actual_oracles(all_data,selected):
    cache={r['request_hash']:r['llm'] for r in lines(ROOT/'ORACLE-COUNTERFACTUALS.jsonl')}
    for d in ['challenge','complete']:
        for row in lines(ROOT/f'{d}-CAPABLE-ALWAYS-REFERENCE.jsonl'):
            l=row['result'].get('llm')
            if l and l.get('request_hash'):cache[l['request_hash']]=l
    cfg=read(ROOT/'LLM-CONFIGS-v3.json')[selected];llm_model=CommonFallback(cfg);out={}
    for dataset,arms in all_data.items():
        out[dataset]={}
        for condition in ('C_SELECTIVE','E_SELECTIVE'):
            fields=defaultdict(Counter);case=Counter()
            for row in arms[condition]:
                r=row['result'];gold=truth(row['expected']);a=observed(before_result(row));wrong=any(a.get(k)!=v for k,v in gold.items())
                if not wrong:
                    for k in gold:fields[k]['assertions']+=1;fields[k]['laya_correct']+=1;fields[k]['oracle_correct']+=1
                    case['specialist_correct']+=1;case['oracle_correct']+=1;continue
                candidate=r.get('llm')
                if not candidate:
                    kwargs={'original_text':row['text'],'narrative_text':r['narrative_text'],'structured_facts':r['structured_facts'],'laya_result':diagnostic(r['laya']),'mode':'FALLBACK'}
                    request=llm_model.request(kwargs['original_text'],kwargs['narrative_text'],kwargs['structured_facts'],kwargs['laya_result'],'FALLBACK')
                    from semantic_pipeline.fallback import digest
                    h=digest(request);candidate=cache.get(h)
                    if not candidate:
                        candidate=llm_model.analyse(**kwargs);cache[h]=candidate
                        append(ROOT/'ORACLE-COUNTERFACTUALS.jsonl',{'dataset':dataset,'condition':condition,'id':row['id'],'request_hash':h,'llm':candidate,
                            'expected_answer_supplied':False,'purpose':'POST_TEST_ORACLE_ONLY_NEVER_ROUTING','timestamp':now()})
                        print('Post-test oracle',dataset,condition,row['id'],candidate['valid'],flush=True)
                p=prepare(row['text'],r.get('parser') is not None);merged=reconcile(p['structured'],None,candidate);deadline=resolve_deadline(row['text'],p,candidate)
                b=observed({'reconciliation':merged,'deadline':deadline,'decision':decide(merged['predicates'],deadline,merged['conflicts'],p['quarantined'])})
                case['specialist_wrong']+=1;case['llm_correct_on_specialist_wrong']+=all(b.get(k)==v for k,v in gold.items())
                case['oracle_correct']+=all(b.get(k)==v for k,v in gold.items())
                for k,v in gold.items():
                    c=fields[k];c['assertions']+=1;c['laya_correct']+=a.get(k)==v
                    if a.get(k)!=v:
                        c['laya_errors']+=1;c['llm_correct_on_errors']+=b.get(k)==v;c['llm_incorrect_on_errors']+=b.get(k)!=v
                    c['oracle_correct']+=a.get(k)==v or b.get(k)==v
            total=Counter()
            for c in fields.values():total.update(c)
            out[dataset][condition]={'name':'ORACLE_ROUTING','deployable':False,'per_predicate':dict(fields),'all_assertions':dict(total),'case_switching':dict(case),
                'scope':'Truth-selected perfect gate; missing accepted-case outputs generated post-test with actual fallback context. Excluded from timed comparison and never used to tune a gate.'}
    return out

def signal_analysis():
    rows=lines(ROOT/'ROUTING-ASSERTION-DATASET.jsonl');out={}
    for key in PREDICATES:
        data=[r for r in rows if r['predicate']==key];fields={}
        for name in ['top_score','margin','supporting_passage_count','contradicting_passage_count','text_length']:
            valid=[r for r in data if r[name] is not None];y=[r['LAYA_CORRECT'] for r in valid]
            fields[name]={'n':len(valid),'correctness_auc':float(roc_auc_score(y,[r[name] for r in valid])) if len(set(y))==2 else None}
        fields['evidence_strata']={str(v):{'n':sum(r['evidence_available']==v for r in data),'correct':sum(r['evidence_available']==v and r['LAYA_CORRECT'] for r in data)} for v in [False,True]}
        out[key]=fields
    return out

def aggregation_delta(dataset):
    fields=defaultdict(lambda:{'before_y':[],'after_y':[],'truth':[]})
    for row in lines(ROOT/f'{dataset}-SPECIALISTS.jsonl'):
        for k,v in truth(row['expected']).items():
            if k not in PREDICATES and k!='other_restriction':continue
            def value(view):
                ps=view['predicates']
                if k=='other_restriction':
                    vals=[ps[n]['value'] for n in PREDICATES if n not in ('votability','share_blocking','poa_required')]
                    return 'YES' if 'YES' in vals else 'NO' if all(x=='NO' for x in vals) else 'UNKNOWN'
                return ps[k]['value']
            q=fields[k];q['truth'].append(v);q['before_y'].append(value(row['narrow']));q['after_y'].append(value(row['fixed_narrow']))
    return {k:{'before':field_metrics(m['truth'],m['before_y'],'VOTABLE' if k=='votability' else 'YES'),
        'after':field_metrics(m['truth'],m['after_y'],'VOTABLE' if k=='votability' else 'YES')} for k,m in fields.items()}

def report_disagreements(comparisons):
    md=['# GLM versus Qwen disagreements','','All rows refer to frozen authored/synthetic test inputs, identical truth and common prompt/schema. No customer accuracy. Pair counts are per labelled assertion. Evidence validity is shown; invalid quotations are diagnostic only. Hidden reasoning is never included.']
    repair=['# Qwen Thinking repair and damage sets','','Direct versus explicit xhigh Thinking. Both independent (D2/D3) and same-specialist always-fallback (C2/C3) comparisons are shown. These sets are post-test diagnostics, never prompt/routing training.']
    for dataset,pairs in comparisons.items():
        for name,c in pairs.items():
            target=repair if name in ('D2_vs_D3','C2_vs_C3') else md
            target += ['',f'## {dataset}: {name}','','Counts: `'+json.dumps(c['all_assertions'])+'`. TWO_LLM_ORACLE: `'+json.dumps(c['TWO_LLM_ORACLE'])+'`.']
            for row in c['disagreements']:
                if target is repair:
                    if row['right_correct'] and not row['left_correct']:kind='THINKING REPAIR'
                    elif row['left_correct'] and not row['right_correct']:kind='THINKING DAMAGE'
                    else:kind='BOTH WRONG / DIFFERENT OUTPUT'
                else:kind='MODEL DISAGREEMENT'
                target += ['',f'### {row["id"]} / {row["field"]} — {kind}','','```text',row['source'],'```','','```json',json.dumps({k:v for k,v in row.items() if k!='source'},ensure_ascii=False,indent=2),'```']
    Path('data/reports/GLM_VS_QWEN_DISAGREEMENTS.md').write_text('\n'.join(md)+'\n')
    Path('data/reports/QWEN_THINKING_REPAIR_DAMAGE.md').write_text('\n'.join(repair)+'\n')

def make_plots():
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    d=read(ROOT/'ROUTING-SELECTION.json');c=d['candidates'];fig,axes=plt.subplots(1,2,figsize=(11,4),layout='constrained')
    for name,colour in [('CONSERVATIVE','#355a75'),('MODERATE','#278066'),('AGGRESSIVE','#a46635'),('ALWAYS','#6e617e')]:
        rows=sorted([r for r in c if r['policy']['name']==name],key=lambda r:r['laya_only_coverage'])
        axes[0].scatter([100*r['laya_only_coverage'] for r in rows],[100*r['semantic_agreement'] for r in rows],label=name,c=colour,s=30,alpha=.7)
        recall=[1-r['positive_misses']['share_blocking']/max(1,r['fields']['share_blocking']['positive_support']) for r in rows]
        axes[1].scatter([100*r['llm_call_rate'] for r in rows],[100*x for x in recall],label=name,c=colour,s=30,alpha=.7)
    axes[0].set(xlabel='Not sent to LLM (%)',ylabel='Labelled semantic agreement (%)',title='Synthetic validation coverage / quality')
    axes[1].set(xlabel='LLM invocation rate (%)',ylabel='Blocking affirmative recall (%)',title='Synthetic validation restriction recall')
    for ax in axes:ax.grid(alpha=.2);ax.set_xlim(-2,102);ax.legend(fontsize=7)
    fig.suptitle('Experimental routing only — no customer accuracy or automation claim',fontsize=10)
    fig.savefig(ROOT/'COVERAGE-QUALITY.png',dpi=160);fig.savefig(ROOT/'COVERAGE-QUALITY.svg');plt.close(fig)

def report():
    from cascade.always_reference import build
    references=build()
    verify_core();commit=read(ROOT/'PREDICTION-COMMIT.json')
    for path,h in commit['files'].items():assert sha(path)==h,path
    all_data={d:{c:load(d,c) for c in CONDITIONS} for d in ['challenge','complete']}
    for d,arms in all_data.items():
        for c,rows in arms.items():assert len(rows)==expected_rows(d),(d,c)
        assert all([(r['id'],r['input_hash']) for r in rows]==[(r['id'],r['input_hash']) for r in arms['A']] for rows in arms.values())
    selection=read(ROOT/'PRIMARY-MODEL-SELECTION.json');routing=read(ROOT/'ROUTING-SELECTION.json');metrics={};transitions={};pairs={};threeway={};deltas={}
    errors=['# Every phase-v2 assertion failure','','Frozen authored/synthetic benchmarks only. These examples are not labels for subsequent tuning. Source-exact evidence is provenance, not proof of correct interpretation.']
    for dataset,arms in all_data.items():
        metrics[dataset]={};transitions[dataset]={};pairs[dataset]={}
        for c,rows in arms.items():
            m=summarize(rows);m['inference']=inference_stats(rows)
            asymmetry={}
            for k,f in m['fields'].items():
                if k not in PREDICATES and k!='other_restriction':continue
                pos='VOTABLE' if k=='votability' else 'YES';neg='NOT_VOTABLE' if k=='votability' else 'NO'
                pairs_for_field=[(truth(r['expected'])[k],observed(r['result']).get(k)) for r in rows if k in truth(r['expected'])]
                asymmetry[k]={'false_negatives_including_abstention':sum(y==pos and p!=pos for y,p in pairs_for_field),'explicit_positive_to_negative':sum(y==pos and p==neg for y,p in pairs_for_field),'false_positives':sum(y!=pos and p==pos for y,p in pairs_for_field)}
            m['critical_asymmetry']=asymmetry
            raw_pairs={};verified_pairs={}
            for rr in rows:
                l=rr['result'].get('llm');g=truth(rr['expected'])
                if not l or not l.get('valid'):continue
                facts=llm_factors(l)
                for key in PREDICATES:
                    if key not in g:continue
                    raw_pairs.setdefault(key,([],[]));verified_pairs.setdefault(key,([],[]))
                    raw_pairs[key][0].append(g[key]);raw_pairs[key][1].append(l['parsed'][key])
                    verified_pairs[key][0].append(g[key]);verified_pairs[key][1].append(facts[key]['value'])
            m['raw_llm_semantics']={k:field_metrics(y,p,'VOTABLE' if k=='votability' else 'YES') for k,(y,p) in raw_pairs.items()}
            m['evidence_validated_llm_semantics']={k:field_metrics(y,p,'VOTABLE' if k=='votability' else 'YES') for k,(y,p) in verified_pairs.items()}
            m['layer_metrics_scope']='Raw/verified LLM metrics cover only invoked schema-valid cases with that field labelled; final pipeline metrics keep every input and unsupported/error outcomes.'
            if dataset=='complete':m['all_factor_exact_match_excluding_status']=sum(all(observed(r['result']).get(k)==v for k,v in truth(r['expected']).items() if k!='classification') for r in rows)
            metrics[dataset][c]=m
            if c.startswith('C') or c.startswith('E'):transitions[dataset][c]=transition(rows)
            for failure in m['failures']:
                row=next(r for r in rows if r['id']==failure['id']);r=row['result']
                errors += ['',f'## {dataset} / {c} / {failure["id"]} / {failure["field"]}','','```text',row['text'],'```','', '```json',json.dumps({'failure':failure,'laya':r.get('laya'),'llm':r.get('llm'),'reconciliation':r['reconciliation'],'decision':r['decision']},ensure_ascii=False,indent=2),'```']
        for left,right in [('D1','D2'),('D1','D3'),('C1','C2'),('C1','C3'),('D2','D3'),('C2','C3')]:pairs[dataset][left+'_vs_'+right]=paired_comparison(arms,(left,right))
        threeway[dataset]=oracle_models(arms,lines(ROOT/f'{dataset}-SPECIALISTS.jsonl'));deltas[dataset]=aggregation_delta(dataset)
    actual=actual_oracles(all_data,selection['selected'])
    summary={'created_at':now(),'status':'SCORED','datasets':metrics,'primary_selection':selection,'routing_selection':routing,
        'transitions':transitions,'paired_comparisons':pairs,'THREE_MODEL_ORACLE':threeway,'ORACLE_ROUTING':actual,
        'aggregation_only_predicate_deltas':deltas,'validation_signal_analysis':signal_analysis(),
        'aggregation_matched_absence_control':read(ROOT/'AGGREGATION-MATCHED-ABSENCE-CONTROL.json') if (ROOT/'AGGREGATION-MATCHED-ABSENCE-CONTROL.json').exists() else None,
        'preparatory_warmups':warmup_stats(),
        'capable_always_quality_reference':{d:summarize(rs) for d,rs in references.items()},
        'always_reference_timing_scope':'Quality-only control; invoked outputs reused and missing accepted cases generated. Not a separately timed architecture.',
        'resources':lines(ROOT/'RESOURCE-MEASUREMENTS.jsonl'),'common_freeze_sha256':sha(ROOT/'COMMON-CONDITION-FREEZE.json'),
        'final_selection_freeze_sha256':sha(ROOT/'FINAL-SELECTION-FREEZE.json'),'automation_enabled':False,'customer_accuracy':None,
        'scope':'Authored partial-assertion challenge and complete synthetic benchmark; no expert-labelled production accuracy.',
        'artifact_label_note':'E_AGGREGATION_ONLY means the fixed narrow specialist plus selected router/fallback; it is not a pure full-stack aggregation-only ablation. Pure reducer attribution uses the saved native before/after deltas.'}
    persist('SUMMARY.json',summary);Path('data/reports/CASCADE_V2_ASSERTION_ERRORS.md').write_text('\n'.join(errors)+'\n');report_disagreements(pairs);make_plots()
    md=['# Aggregation, Qwen and selective-cascade evaluation','','**Automation disabled. Customer/production accuracy UNKNOWN. All results below are authored or synthetic, not customer accuracy.**','',
        'Historical results are preserved under the git tag and manifest PRE_AGGREGATION_FIX_BASELINE. No Laya training, checkpoint modification, challenge modification or challenge-based prompt/routing tuning occurred. The historical scorer-v2 correction remains explicit; old predictions are never overwritten.','',
        '## Experimental conditions','',
        'D1/C1: GLM-4.7-Flash Q4_K_M direct. D2/C2: Qwen3.8-27B Q4_K_M Direct. D3/C3: the same Qwen weights in explicit supported xhigh Thinking. All share proxy_semantic_common_v1 and the identical typed schema/evidence verifier. C1–C3 always escalate and receive identical whole-notice Laya diagnostics; D1–D3 are genuinely independent.','',
        'Qwen library tag qwen3.8:27b-q4_K_M, manifest 25b843619e944cd0ae6069f94ff4e5e26a16e109ccbc0a66a0f05979ed70098e; language-model metadata 27,320,697,856 parameters; upstream Qwen/Qwen3.8-27B revision 1d4bf0f2ff6012fd82039f2fa52739d0dd7c60c0, Apache-2.0. Native runtime architecture qwen35 is expected for this official model lineage. All five installed blobs were SHA-256 verified.','',
        'An isolated local Ollama 0.34.3 instance uses port 11435. Qwen runtime forces one request slot, so all timed conditions use one client request at a time. Mac: M3 Max, 64 GiB Apple unified memory. Both models get 32,768 context. GLM and Qwen Direct get 2,048 output tokens; Thinking gets 16,384 and xhigh. GLM retains historical temperature 0; Qwen uses its official recommended Direct/Thinking sampling presets with seed42. These are explicit supported-configuration conditions, not a weights-only identical-sampling experiment. Thinking quality is not penalised for extra compute.','',
        'Native eval_count includes reasoning plus final answer; separate native reasoning-token count is unavailable. Reasoning text and invalid free-form output are not persisted or displayed: only hashes, character counts, timings and schema-valid structured answers. Native JSON/schema success, bounded repair and final failures are measured separately. No numerical LLM self-assessment is treated as confidence.','',
        '`E_AGGREGATION_ONLY` is an artifact label for the fixed narrow specialist with its old votability head plus the selected router/fallback. It is not a pure full-stack aggregation-only ablation. Only the saved native passage before/after comparison isolates aggregation. C1–C3 retain whole-notice specialist context for the controlled LLM comparison; C_SELECTIVE/E_SELECTIVE use the separately declared capable specialist.','',
        '## Validation and freeze','',
        'Aggregation: 100 supplied synthetic validation notices plus 80 separately authored complete synthetic validation notices. The supplied validation has historical train overlap. Reducers are compared on the same saved native passage outputs. Only contract-qualified reducers can be selected; simple max/last comparators fail the explicit supersession/conflict/route contracts. Strategy and thresholds were fixed without challenge results.','',
        f'Primary fallback selected from 40 balanced complete validation notices in both modes, with label repeatability probes: **{selection["selected"]}**. Then its capable-specialist fallback was run on all 80 complete validation notices to select an interpretable route. Selection was frozen before new challenge/complete evaluation. The 48-case complete benchmark is not validation. The old exposed/leaky synthetic100 test is retained as historical development evidence and not reused as a new headline test.',
        '', 'The composite specialist uses the same whole FT checkpoint for votability and the same narrow checkpoint with corrected evidence reduction for eight restriction questions. Six expanded predicates remain transfer inference, not newly supervised heads. Separate native aggregation-only deltas isolate the reducer; the composite change is labelled separately. Validation votability favoured whole-notice inference (176/180 vs 152/180 narrow), before challenge evaluation.',
        '', '## Aggregation defect and effect','',
        'MAX_POSITIVE and ANY_STRONG_POSITIVE coincide under the shared strong-passage eligibility threshold in these comparators; they are not independent evidence of superiority. The corrected reducer distinguishes absent mention from explicit negative statements, preserves native scores/offsets/evidence for every passage, scopes historical/background text, honours explicit later supersession and abstains on unresolved current contradictions or unspecified voting routes. It never turns a native NO into a regex-generated YES. Every displayed quotation is checked against the unchanged source.','',
        'The eleven supplied affirmative blocking validation examples improve 0/11→11/11 with unchanged weights. A and B are whole-notice classifiers and never used the defective sentence reducer; they are rerun unchanged, not relabelled as improved aggregation models. The clean narrow-before/narrow-after per-predicate comparison is separate from LLM/routing/composite changes.','']
    md += ['The original six-comparator table also varies document-absence handling. A matched-absence validation-only control is preserved in AGGREGATION-MATCHED-ABSENCE-CONTROL.json and AGGREGATION_VALIDATION.md. It shows that the large raw comparator gap is primarily an absence-policy effect; it must not be advertised as evidence that supersession logic alone creates that gain. This diagnostic changed no frozen inference configuration.','']
    for dataset,arms in metrics.items():
        md += [f'## {dataset}','','| Condition | Correct labelled assertions | Cases satisfying supplied assertions | Blocking YES recall | POA YES recall | LLM calls | Median / p95 ms |','|---|---:|---:|---:|---:|---:|---:|']
        for c,m in arms.items():
            f=m['fields'];md.append(f'| {c} | {m["correct_assertions"]}/{m["assertions"]} | {m["cases_satisfying_all_supplied_assertions"]}/{m["cases"]} | {fmt(f["share_blocking"]["positive_recall"])} (n={f["share_blocking"]["positive_support"]}) | {fmt(f["poa_required"]["positive_recall"])} (n={f["poa_required"]["positive_support"]}) | {m["llm_invocations"]}/{m["cases"]} | {m["median_latency_ms"]:.0f} / {m["p95_latency_ms"]:.0f} |')
        md += ['', 'Challenge = 95 supplied assertions over 57 cases, only four explicit final-status labels. Complete = 528 labelled assertions over 48 fully labelled synthetic cases (9 semantic fields, deadline and status). Missing capabilities count as NOT_SUPPORTED errors. Neither case conjunction is customer accuracy. Per-field support, accuracy/F1, specificity, positive precision/recall, balanced accuracy and confusion matrices are preserved in SUMMARY.json.','']
        if dataset=='complete':md += ['All-factor exact match (nine semantics + deadline, excluding separately scored final status): '+', '.join(f'{c} {m["all_factor_exact_match_excluding_status"]}/48' for c,m in arms.items())+'.','']
        md += ['### Native narrow aggregation before / after','','| Predicate | Before correct/n | After correct/n | Delta correct | Affirmative recall before→after |','|---|---:|---:|---:|---:|']
        for k,z in deltas[dataset].items():md.append(f'| {k} | {z["before"]["correct"]}/{z["before"]["n"]} | {z["after"]["correct"]}/{z["after"]["n"]} | {z["after"]["correct"]-z["before"]["correct"]:+d} | {fmt(z["before"]["positive_recall"])} → {fmt(z["after"]["positive_recall"])} |')
    md += ['', '## Genuine selective routing and limits','',
        f'Selected policy: `{json.dumps(routing["selected"]["policy"])}`. Validation invocation rate {fmt(routing["selected"]["llm_call_rate"])}, semantic agreement {fmt(routing["selected"]["semantic_agreement"])} against always-fallback {fmt(routing["always"]["semantic_agreement"])}. The predeclared selection minimises calls only within one percentage point semantic agreement and with no additional affirmative misses for any labelled semantic predicate. No target call percentage was imposed.','',
        'A same-capable-specialist always-fallback quality reference is also calculated. Actual invoked C_SELECTIVE outcomes are reused because the semantic request/reconciliation is identical; every missing gate-accepted case gets a fresh fallback generation regardless of truth. This isolates the gate from specialist-composition changes without redundant calls. Its mixed/recomposed latency is excluded from timed architecture comparisons. A reduced invocation rate is not automatically automation coverage. Fast paths ending in UNCERTAIN_MANUAL_REVIEW are counted separately. The customer quality gate keeps every manual_review_required flag true regardless of experimental gate acceptance. The coverage chart is validation research, not a production precision guarantee.','']
    for d,arms in transitions.items():
        ref=summarize(references[d]);chosen=metrics[d]['C_SELECTIVE']
        md.append(f'- {d}: same-specialist always-fallback quality {ref["correct_assertions"]}/{ref["assertions"]}, selected cascade {chosen["correct_assertions"]}/{chosen["assertions"]}; reference adds no separate architecture latency claim.')
        for c in ['C_SELECTIVE','E_SELECTIVE']:
            t=arms[c];md += [f'- {d}/{c}: no-LLM {t["fast_path_count"]}/{expected_rows(d)}, correct on all supplied assertions {t["fast_path_correct"]}/{t["fast_path_count"]}; indecisive fast paths {t["fast_path_indecisive_count"]}; invoked-case semantic transitions `{json.dumps(t["semantic_transitions"])}`.']
    md += ['', '![Synthetic validation coverage and quality](../experiments/cascade-v2/COVERAGE-QUALITY.png)', '', '| Policy | Score / margin | Calls /80 | No-LLM coverage | Semantic agreement | Blocking YES recall | POA YES recall | Positive misses (all semantic fields) |', '|---|---:|---:|---:|---:|---:|---:|---:|']
    for candidate in routing['candidates']:
        p=candidate['policy'];f=candidate['fields'];md.append(f'| {p["name"]} | {p["min_score"]} / {p["min_margin"]} | {candidate["llm_invocations"]} | {fmt(candidate["laya_only_coverage"])} | {fmt(candidate["semantic_agreement"])} | {fmt(f["share_blocking"]["positive_recall"])} | {fmt(f["poa_required"]["positive_recall"])} | {sum(candidate["positive_misses"].values())} |')
    md += ['', 'Validation feature strata and score/margin correctness AUC are reported per predicate with support. Native Laya scores are not calibrated correctness probabilities; saturation and absent evidence limit threshold usefulness. The final challenge outcomes were never fed back into routing.','',
        '## Oracle and model complementarity','',
        'TWO_LLM_ORACLE is calculated for GLM/Direct and GLM/Thinking, independently and with identical Laya fallback context. The Laya+Direct+Thinking oracle is an assertion-wise analytical ceiling, not a deployable ensemble. No two-LLM production chain was implemented. Actual-context ORACLE_ROUTING generates missing accepted-case fallback outputs only after test selection/freeze and excludes them from timed call rates. All per-predicate counts, repairs and remaining errors are in SUMMARY.json.','',
        'Every Direct→Thinking repair and damage example, source, truth and evidence is in QWEN_THINKING_REPAIR_DAMAGE.md. GLM/Qwen disagreements are in GLM_VS_QWEN_DISAGREEMENTS.md. Every assertion failure and accepted specialist failure is retained; no expected assertion was changed to match a model.','',
        '## Attribution, resources and conclusion','',
        'The historical C +12 is decomposed separately in C_GAIN_DECOMPOSITION.md: +8 deterministic date assertions, +4 reconciliation, +2 direct semantic repairs, −2 LLM damage; five changed assertions remain wrong. This accounting is explicit and order-dependent, not a claim that an LLM alone adds twelve. Historical C has zero aggregation difference from B.','',
        'All native prompt/generated counts, reasoning-character diagnostics, first-token time, tokens/s, schema/evidence reliability, sampled process RSS and unified-memory pressure are stored per run. Peak process RSS must not be summed as distinct physical memory; system pressure includes unrelated applications. Cold model reloads are separate from warmed sequential wall time. Native model allocation uses Apple unified memory, not discrete VRAM.','',
        'The parser is NOT_APPLICABLE for unstructured notices; missing ISO fields never cause semantic uncertainty. Its structure is only used for detected tagged messages. Previous scanning recognised zero ISO15022 records among 7,683 public excerpts; the parser cannot contribute extracted structure to that corpus. The eight ISO examples in the complete benchmark remain standards-derived synthetic fixtures.','',
        'GLM Thinking was not evaluated in this phase; model and mode recommendations apply only to the pinned conditions, not to every possible runtime/prompt configuration. This experiment can choose an experimental local fallback and quantify call/quality trade-offs on authored data. It cannot establish customer accuracy, operational precision, regulated-service suitability or production readiness. If the selected frontier saves few calls or loses critical recall, that negative result is retained. The highest-value subsequent evidence remains independently expert-labelled representative real notices, grouped by event/near duplicate; no further tuning on these 57 cases.','',
        '## Reproduction and application','',
        'Use the frozen baseline tag/manifest and COMMON-CONDITION-FREEZE.json, FINAL-SELECTION-FREEZE.json, per-run manifests, raw stage records and PREDICTION-COMMIT.json. `python -m scripts.run_cascade_phase` resumes missing work without replacing results; an active-runner lock prevents concurrent duplicate studies. Status/events are operational files, not model results.','',
        'The existing application defaults remain unchanged. Explicit SEMANTIC_PIPELINE_VERSION=v2 with CLASSIFICATION_ARCHITECTURE=LAYA_LLM or FULL_HYBRID selects the frozen cascade; LLM_ENABLED controls real local calls and remains false by default. Selection must be frozen before this path can run. All normal persisted Notice Detail trace and human-review functionality remains available. Model Lab exposes phase-v2 progress/results separately from preserved historical A–E results.']
    Path('data/reports/AGGREGATION_SELECTIVE_CASCADE_EVALUATION.md').write_text('\n'.join(md)+'\n')
    selection_md=['# GLM / Qwen primary fallback selection','','Selection uses validation only, never the frozen challenge. No customer accuracy or automation claim.','',f'Selected experimental primary: **{selection["selected"]}**.','',selection['ranking'],'', 'All candidates use the same common prompt/schema/verifier. Qwen Direct and xhigh Thinking use the same quantised weights. Recommended sampling differs by supported mode and is pinned. No model-specific prompt tuning was performed.','','```json',json.dumps(selection['metrics'],indent=2),'```','',
        'Reproducibility probes compare semantic labels and full parsed outputs separately. Exact reasoning text is intentionally unavailable; only final output and permitted aggregate diagnostics are retained. Model/runtime/source pins are in LLM-CONFIGS-v3.json and QWEN-INSTALLED-INTEGRITY.json. Selection is experimental and does not automatically switch the customer demo.']
    Path('data/reports/GLM_QWEN_MODEL_SELECTION.md').write_text('\n'.join(selection_md)+'\n')
    print('All phase-v2 reports generated',flush=True)
if __name__=='__main__':report()
