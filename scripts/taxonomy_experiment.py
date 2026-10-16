"""Zero-shot ablation only. Challenge expectations are never changed or trained on."""
import json,time
from pathlib import Path
from apps.api.store import dumps,now
from classifier.laya_classifier import LayaClassifier,load_config,config_version
from scripts.semantic_benchmark import benchmark

def main():
    root=Path('data/experiments/taxonomy-v1');root.mkdir(parents=True,exist_ok=False)
    cfg=load_config('classifier/config-factorised-v2.json')
    (root/'factorised-v2-config.json').write_text(dumps(cfg))
    v2=benchmark(root/'factorised-v2-challenge.json',cfg)
    model=LayaClassifier();base=load_config()
    labels=['VOTABLE','NOT_VOTABLE','VOTABLE_WITH_RESTRICTION','POA_REQUIRED','SHARE_BLOCKING','DEADLINE_PASSED','UNCERTAIN_MANUAL_REVIEW']
    criteria=dict(zip(labels,[
      'Current shareholder voting opportunity with no stated restrictions or passed deadline',
      'No current shareholder voting opportunity; informational or historical only',
      'Current voting opportunity with multiple restrictions or other eligibility restrictions',
      'Current voting opportunity requiring a power of attorney',
      'Current voting opportunity requiring shares blocked from trading',
      'Voting opportunity whose controlling voting deadline has passed relative to reference date',
      'Ambiguous or insufficient information to choose one operational status']))
    question={'classification':{'type':'choice','instructions':'Classify this notice into one operational status. Resolve overlapping conditions with precedence UNCERTAIN, NOT_VOTABLE, DEADLINE_PASSED, multiple or other restrictions, POA_REQUIRED, SHARE_BLOCKING, VOTABLE. Do not treat meeting or record dates as instruction deadlines.','criteria':criteria}}
    fixtures=json.loads(Path('tests/fixtures/semantic.json').read_text());rows=[]
    for i in range(0,len(fixtures),2):
        chunk=fixtures[i:i+2];start=time.perf_counter()
        results=model.agent.predict_batch([f'Reference date (UTC): {base["evaluation_date"]}\n\nNotice:\n{x["text"]}' for x in chunk],question,batch_size=2,max_len=base['max_len'],head_max_len=base['head_max_len'],sort_by_length=True)
        elapsed=(time.perf_counter()-start)*1000/len(chunk)
        for x,r in zip(chunk,results):
            a=r['answers']['classification'];rows.append({'id':x['id'],'expected_status':x['expected'].get('classification'),'prediction':a['choice'],'scores':a['probabilities'],'raw_answer':a,'latency_ms':elapsed})
    subset=[r for r in rows if r['expected_status'] is not None]
    factor=json.loads(Path('data/reports/semantic-challenge.json').read_text())
    baseby={x['id']:x for x in factor['examples']};v2by={x['id']:x for x in v2['examples']}
    report={'created_at':now(),'kind':'challenge-informed zero-shot taxonomy/date ablation; not independent accuracy','model_version':base['checkpoint_revision'],
      'flat_question':question,'flat_config_hash':config_version({**base,'questions':question}), 'rows':rows,
      'shared_explicit_status_subset':{'n':len(subset),'flat_correct':sum(r['prediction']==r['expected_status'] for r in subset),'factorised_v1_correct':sum(baseby[r['id']]['observed']['classification']==r['expected_status'] for r in subset),'factorised_v2_correct':sum(v2by[r['id']]['observed']['classification']==r['expected_status'] for r in subset)},
      'all_partial_field_cases':{'factorised_v1_passed':factor['passed'],'factorised_v2_passed':v2['passed'],'n':57,'flat':'Cannot recover independent restriction factors from a single status; no fabricated all-field comparison'},
      'limitations':['Native Laya probabilities only.','Flat and factorised prompts differ; results confound task formulation and prompt effects.','No human-labelled test set exists.','Date rules informed by challenge failures; improvements on it are regression results, not independent evidence.']}
    (root/'taxonomy-comparison.json').write_text(dumps(report));print(dumps({k:v for k,v in report.items() if k not in ['rows','flat_question']}))
if __name__=='__main__':main()
