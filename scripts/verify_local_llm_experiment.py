"""Post-hoc artifact verification; never changes frozen inference or truth."""
import hashlib
import json
import math
from pathlib import Path
from datetime import datetime
from semantic_pipeline.experiment import ROOT, read, lines, sha, verify, write, now
from semantic_pipeline.schema import SemanticResult
from semantic_pipeline.evidence import verify_evidence


def main():
    freeze=verify();commit=read(ROOT/'PREDICTION-COMMIT.json')
    for p,h in commit['files'].items():assert sha(p)==h,p
    count=0;calls=0;completed=0;invalid=0;exact_quotes=0;unsupported=0;errors=[]
    run_ids=set();pins=read(Path('semantic_pipeline/llm-config.json'))
    for dataset,name,n in [('challenge','challenge.json',57),('synthetic-development','synthetic-test-inputs.json',100),('complete','complete-benchmark.json',48)]:
        source=read(ROOT/name);assert len(source)==n
        expected={r['id']:r for r in source}
        for arm in 'ABCDE':
            rows=lines(ROOT/f'{dataset}-{arm}.jsonl');assert len(rows)==n
            assert len({r['id'] for r in rows})==n
            for row in rows:
                count+=1;r=row['result'];raw=expected[row['id']]['text']
                assert row['text']==raw
                assert row['input_hash']==r['input_hash']==hashlib.sha256(raw.encode()).hexdigest()
                assert row['frozen_manifest_sha256']==sha(ROOT/'FREEZE.json')
                assert row['architecture']==r['architecture']==arm
                assert datetime.fromisoformat(row['timestamp'])>=datetime.fromisoformat(freeze['created_at'])
                assert not r['automation_enabled'];assert not r['decision']['automation_enabled'];assert r['decision']['manual_review_required']
                run_ids.add(row['run_id'])
                for a in r['reconciliation']['predicates'].values():
                    unsupported+=a['value']=='NOT_SUPPORTED'
                    for ev in a.get('evidence',[]):
                        assert ev['valid'];assert raw[ev['start']:ev['end']]==ev['text'];exact_quotes+=1
                laya=r.get('laya')
                if laya:
                    for a in laya['predicates'].values():
                        scores=a.get('scores',{})
                        if scores:
                            assert all(math.isfinite(v) and 0<=v<=1 for v in scores.values())
                            assert abs(sum(scores.values())-1)<.002
                    assert laya['model_version']
                llm=r.get('llm')
                if llm:
                    calls+=llm.get('invoked',False);completed+=bool(llm.get('raw_response'))
                    invalid+=not llm['valid']
                    assert llm['model_digest']==pins['model_digest'];assert llm['confidence'] is None
                    context=json.loads(llm['request']['messages'][1]['content'])
                    assert 'expected' not in context
                    if arm=='D':assert context['mode']=='INDEPENDENT' and 'laya_diagnostic' not in context
                    if arm in 'CE':assert context['mode']=='FALLBACK' and 'laya_diagnostic' in context
                    if llm['valid']:
                        SemanticResult.model_validate(llm['parsed'])
                        assert llm['raw_response']['eval_count']>0
                    else:errors.append({'dataset':dataset,'architecture':arm,'id':row['id'],'error':llm.get('error')})
    out={'verified_at':now(),'frozen_files':len(freeze['files']),'prediction_records':count,
        'expected_prediction_records':1025,'run_ids':sorted(run_ids),'llm_attempts':calls,
        'llm_completed_responses':completed,'invalid_llm_results':invalid,'llm_errors':errors,
        'displayable_exact_substring_evidence':exact_quotes,'unsupported_factors_retained':unsupported,
        'input_counts_hashes_pins_timestamps_scores_evidence_verified':True,
        'automation_enabled':False,'customer_accuracy':None,
        'scope':'Artifact integrity and software conformance, not semantic correctness. Semantic failures remain in SUMMARY.json.'}
    write(ROOT/'VERIFICATION.json',out);print(json.dumps(out,indent=2))

if __name__=='__main__':main()
