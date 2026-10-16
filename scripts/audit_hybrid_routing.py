import json,hashlib,time
from pathlib import Path
from hybrid.pipeline import analyse
from hybrid.rules import RESTRICTIONS
OUT=Path('data/experiments/iso-hybrid-v1')

def audit():
    total=det=planned=0;beg=time.perf_counter();slots=2+len(RESTRICTIONS)
    with (OUT/'public-routing-audit.jsonl').open('x') as dest:
        for line in Path('data/normalised/public.jsonl').open():
            row=json.loads(line);h=analyse(row['text']);total+=1
            resolved=int(h['deadline']['status']!='UNKNOWN')+int('votable' in h['structured_facts']);det+=resolved
            pending=(1+len(RESTRICTIONS))-int('votable' in h['structured_facts']) if h['narrative_text'] else 0;planned+=pending
            dest.write(json.dumps({'id':row['id'],'source_hash':row['source_hash'],'kind':h['parsed']['kind'],'deterministic_nonunknown_fact_outputs':resolved,'planned_laya_predicate_slots':pending,'laya_executed':False,'deadline':h['deadline'],'decision':h['decision']})+'\n')
    summary={'records':total,'decision_fact_slots_per_record':slots,'total_decision_fact_slots':total*slots,'deterministic_nonunknown_fact_outputs':det,'deterministic_output_fraction':det/(total*slots),'planned_laya_predicate_slots':planned,'planned_laya_slot_fraction':planned/(total*slots),'laya_executions':0,'llm_escalations':0,'human_review_cases':total,'human_review_fraction':1.0,'elapsed_seconds':time.perf_counter()-beg,'scope':'Rule outputs and intended routing, NOT verified fact accuracy. Narrow Laya not run across public corpus. Date rule outputs require review and may reflect extraction errors. Slot denominator is vote + seven restrictions + deadline, not ISO metadata fields.'}
    (OUT/'public-routing-summary.json').write_text(json.dumps(summary,indent=2));print(summary)
if __name__=='__main__':audit()
