"""Profile public source rows before any classification. Exclude extraction targets."""
import collections
import json
import re
from pathlib import Path
import numpy as np
from langdetect import detect, DetectorFactory
from classifier.preprocessing import normalise, source_hash
from training.split import duplicate_groups, partition
DetectorFactory.seed = 0
REVISION = 'c90ac749f9056901c8c3ed22ae1ff7c894c9b696'
BASE = 'https://huggingface.co/datasets/TheTokenFactory/sec-contracts-financial-extraction-instructions'

def enrich_publishers(records):
    """Fill missing display company only from consistent publisher metadata for the same filing.
    Original provenance_metadata and model text remain unchanged; conflicting names stay unknown.
    """
    from collections import defaultdict
    companies=defaultdict(dict)
    for r in records:
        company=(r.get('provenance_metadata',{}).get('company') or '').strip()
        if company and r.get('source_file'):companies[r['source_file']].setdefault(company,r['id'])
    filled=0
    for r in records:
        own=(r.get('provenance_metadata',{}).get('company') or '').strip()
        candidates=companies.get(r.get('source_file'),{})
        if not own and len(candidates)==1:
            company,source_id=next(iter(candidates.items()))
            r['issuer']=company;r['issuer_provenance']={'kind':'consistent publisher metadata for same source_file','record_id':source_id};filled+=1
    return filled

def build():
    records, raw_schema = [], {}
    for path in sorted(Path('data/raw').glob('alpaca*.jsonl')):
        for i,line in enumerate(path.open()):
            row = json.loads(line)
            raw_schema.update({k:type(v).__name__ for k,v in row.items()})
            m = row['metadata']
            # Only input is source text. Instruction/output and extraction confidence are excluded.
            records.append(dict(id=f'{path.stem}:{i+1}', text=row['input'],
                source_hash=source_hash(row['input']), issuer=m.get('company') or m.get('ticker') or 'Unknown',
                ticker=m.get('ticker'), source_file=m.get('source_file'),
                event_type='Proxy excerpt' if m.get('pipeline')=='proxy' else 'Contract excerpt',
                country='UNKNOWN', market='UNKNOWN', isin=None, meeting_date=None,
                source_url=f'{BASE}/blob/{REVISION}/data/{path.name}',
                source_revision=REVISION, source_row=i+1, source_dataset='Public SEC excerpts',
                language='UNKNOWN', unit='filing excerpt', provenance_metadata=m))
    issuer_fills=enrich_publishers(records)
    texts = [normalise(x['text']) for x in records]
    langs = {}
    for r,t in zip(records,texts):
        h=source_hash(t)
        if h not in langs:
            try: langs[h] = detect(t[:5000]) if t else 'UNKNOWN'
            except Exception: langs[h]='UNKNOWN'
        r['language']=langs[h]
    groups=duplicate_groups(records)
    for r,g in zip(records,groups): r.update(group_id=g,split=partition(g),grouping_version='exact-prefix-jaccard-v2')
    lengths=[len(t) for t in texts]
    counts=collections.Counter(texts)
    report = dict(grouping_version='exact-prefix-jaccard-v2',source=BASE, revision=REVISION, raw_schema=raw_schema, records=len(records),
        unit='Source filing excerpts, repeated across extraction tasks; NOT events, custodian notices or voting instructions.',
        fields=dict(text='input (unaltered source excerpt)',id='derived source filename + 1-based row',
            issuer='metadata.company or ticker; missing company completed only from consistent same-filing publisher metadata, with source record ID; may remain unknown',event_type='metadata.pipeline (document type, not corporate-action type)',
            country='UNKNOWN: SEC filing does not prove issuer domicile', market='UNKNOWN: not supplied',
            dates='not mapped; fiscal years and historic dates are not deadlines', isin='not supplied',
            labels='output contains generated extraction targets, NOT verified votability labels; excluded from model'),
        issuer_metadata_fills=issuer_fills,unique_texts=len(counts), exact_duplicate_rows=len(texts)-len(counts), duplicate_groups=len(set(groups)),
        near_duplicate_method='Complete exact Jaccard threshold join at 0.85 using global-frequency prefix filtering and integer comparisons; five-word shingles with numeric masking; exact text, transitive and same-filing union. Does not detect every semantic paraphrase.',
        largest_groups=collections.Counter(groups).most_common(5), missing_text=sum(not t for t in texts),
        html_rows=sum(bool(re.search(r'<[a-zA-Z][^>]*>',t)) for t in [r['text'] for r in records]),
        replacement_character_rows=sum('\ufffd' in t for t in texts), mojibake_suspect_rows=sum(any(s in t for s in ['Ã','Â','â€']) for t in texts),
        malformed_rows=0, language_detection='langdetect heuristic, seed=0; requires human verification',
        languages=dict(collections.Counter(r['language'] for r in records)),
        document_types=dict(collections.Counter(r['event_type'] for r in records)),
        splits=dict(collections.Counter(r['split'] for r in records)),
        text_characters={str(q):float(np.percentile(lengths,q)) for q in [0,50,95,99,100]},
        long_over_12000_chars=sum(n>12000 for n in lengths),
        repeated_openings=collections.Counter(t[:100] for t in texts).most_common(10),
        leakage='Extraction instruction, output, task labels and publisher confidence never enter Laya. Same source filing and duplicate groups allocated together.',
        taxonomy='Provisional factorised schema: voting eligibility, independent restrictions, deadline status. Seven operational statuses are derived with explicit precedence. Public excerpts cannot validate exclusivity.',
        limitations=['Not the requested 15,022-record customer corpus.', 'US regulatory filing excerpts overrepresent compensation and historical governance; not comprehensive global corporate-action coverage.', 'No human-verified votability labels. Accuracy and safe automation remain unknown.', 'Publisher generated extraction targets with Gemma; these targets are not used as ground truth or model input. No external inference in this application.'])
    Path('data/normalised/public.jsonl').write_text(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in records))
    Path('data/reports/profile.json').write_text(json.dumps(report,indent=2,ensure_ascii=False))
    Path('data/reports/PROFILE.md').write_text('# Public dataset profile\n\n'+ '\n\n'.join(f'**{k}**: {json.dumps(v,ensure_ascii=False)}' for k,v in report.items()))
    print(json.dumps({k:report[k] for k in ['records','unique_texts','exact_duplicate_rows','duplicate_groups','document_types','languages','text_characters','splits']},indent=2))
if __name__=='__main__': build()
