"""Export only reviewed training groups. Test labels never enter fine-tuning input."""
import json
import hashlib
from pathlib import Path
from apps.api.store import connect,dumps,now
from classifier.laya_classifier import load_config
from classifier.schema import Decision
from training.split import verify_isolation

def export_dataset(output,path=None):
    output=Path(output);output.mkdir(parents=True,exist_ok=False)
    cfg=load_config()
    with connect(path) as c:
        rows=[dict(r) for r in c.execute("SELECT n.*,r.id AS revision,r.label,r.reviewer,r.reviewed_at,r.context FROM notices n JOIN reviews r ON r.id=(SELECT max(id) FROM reviews WHERE record_id=n.id) WHERE r.action='VERIFY'")]
    verify_isolation(rows)
    all_rows={'train':[],'validation':[],'test':[]}
    manifests=[]; seen=set()
    from classifier.preprocessing import normalise,source_hash
    for r in rows:
        d=Decision.model_validate_json(r['label'])
        context=json.loads(r.get('context') or '{}')
        if context.get('evaluation_date',cfg['evaluation_date'])!=cfg['evaluation_date']:raise ValueError('Golden reference date differs from training config')
        h=source_hash(normalise(r['text']))
        identity=(h,r['split'])
        values=d.model_dump(exclude={'manual_review_required'})
        # Refuse conflicting labels on exact duplicates instead of duplicating contradictory targets.
        prior=next((x for x in manifests if x['normalised_hash']==h),None)
        if prior and prior['decision']!=values: raise ValueError('Conflicting golden labels on duplicate input')
        manifests.append(dict(record_id=r['id'],group_id=r['group_id'],split=r['split'],revision=r['revision'],source_hash=r['source_hash'],normalised_hash=h,decision=values))
        if identity in seen:continue
        seen.add(identity)
        expected={k:('UNKNOWN' if v is None else 'YES' if v is True else 'NO' if v is False else v) for k,v in values.items()}
        state=f'Reference date (UTC): {cfg["evaluation_date"]}\n\nNotice:\n{normalise(r["text"])}'
        all_rows[r['split']].append({'state':state,'questions':cfg['questions'],'expected':expected})
    for split,data in all_rows.items():
        (output/f'{split}.jsonl').write_text(''.join(json.dumps(r,ensure_ascii=False,allow_nan=False)+'\n' for r in data))
    file_hashes={f'{split}.jsonl':hashlib.sha256((output/f'{split}.jsonl').read_bytes()).hexdigest() for split in all_rows}
    manifest={'file_hashes':file_hashes,'created_at':now(),'config':cfg,'label_revisions':manifests,'counts':{k:len(v) for k,v in all_rows.items()}}
    (output/'manifest.json').write_text(dumps(manifest))
    return manifest

if __name__=='__main__':
    import argparse
    p=argparse.ArgumentParser();p.add_argument('output');a=p.parse_args();print(export_dataset(a.output)['counts'])
