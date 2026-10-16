"""Version derived grouping before any labels exist; retain original input/report artifacts."""
import json
import shutil
from pathlib import Path
from collections import Counter
from training.split import duplicate_groups,partition
from apps.api.store import connect

def main():
    with connect() as c:
        if c.execute('SELECT count(*) FROM reviews').fetchone()[0]:raise ValueError('Cannot migrate reviewed corpus')
    source=Path('data/normalised/public.jsonl');legacy=source.with_name('public-lsh-v1.jsonl')
    if legacy.exists():raise ValueError('Legacy grouping already preserved')
    shutil.copy2(source,legacy)
    for name in ['profile.json','PROFILE.md']:shutil.copy2(Path('data/reports')/name,Path('data/reports')/('legacy-lsh-v1-'+name))
    rows=[json.loads(x) for x in source.read_text().splitlines()]
    groups=duplicate_groups(rows)
    for r,g in zip(rows,groups):r.update(group_id=g,split=partition(g),grouping_version='exact-prefix-jaccard-v2')
    Path('data/normalised/public-v2.jsonl').write_text(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in rows))
    report=json.loads(Path('data/reports/profile.json').read_text())
    report.update(duplicate_groups=len(set(groups)),largest_groups=Counter(groups).most_common(5),splits=dict(Counter(r['split'] for r in rows)),
        grouping_version='exact-prefix-jaccard-v2',near_duplicate_method='Complete exact Jaccard threshold join at 0.85 using global-frequency prefix filtering and integer comparisons; numeric-masked five-word shingles; transitive and same-filing union. Does not detect every semantic paraphrase.',
        grouping_correction='An independent exact audit found two cross-split near-duplicate pairs and seventeen ungrouped pairs in the initial LSH protocol. Splits were rebuilt before any human labels or training; old source and profile versions are retained.')
    Path('data/reports/profile.json').write_text(json.dumps(report,indent=2,ensure_ascii=False))
    Path('data/reports/PROFILE.md').write_text('# Public dataset profile\n\n'+'\n\n'.join(f'**{k}**: {json.dumps(v,ensure_ascii=False)}' for k,v in report.items()))
    print({'groups':len(set(groups)),'splits':report['splits']})
if __name__=='__main__':main()
