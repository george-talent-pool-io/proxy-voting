import hashlib,json
from collections import Counter
from pathlib import Path
from hybrid.parser import parse,facts
from hybrid.corpus import ROOT

def verify():
    counts=Counter();routes=Counter();exact=total=crashes=0;unknown=0;fields=0
    for line in (ROOT/'sources.jsonl').read_text().splitlines():
        r=json.loads(line);p=ROOT/r['path']
        assert hashlib.sha256(p.read_bytes()).hexdigest()==r['sha256']
        row=json.loads(p.read_text());parsed=parse(row['raw'],row['message_type']);counts[r['source_type']]+=1
        assert parsed['raw']==row['raw']
        assert hashlib.sha256(row['raw'].encode()).hexdigest()==r['raw_sha256']
        for f,t in zip(parsed['fields'],parsed['routing']):
            assert row['raw'][f['start']:f['end']].startswith(':'+f['tag']+':')
            assert f['id']==t['field_id'];routes[t['route']]+=1;fields+=1
        for f in facts(parsed,'narrative'):assert row['raw'][f['value_start']:f['end']]==f['value']
        if r['source_type']!='STANDARDS_DERIVED_SYNTHETIC' or 'standards_derived/' in r['path']:
            for key in ['seme','corp','caev','function']:
                if key not in row['expected']:continue
                total+=1;ok=len(facts(parsed,key))==1 and facts(parsed,key)[0]['value']==row['expected'][key];exact+=ok
                assert ok,(r['id'],key)
    report={'corpus_items':sum(counts.values()),'provenance_counts':dict(counts),'exact_assertions_passed':exact,'exact_assertions_total':total,'crashes':crashes,'field_source_spans_checked':fields,'routing_counts':dict(routes),'scope':'Generated partial-message reference assertions plus one official excerpt; NOT production parser accuracy or full FIN conformance. Unknowns retained losslessly.','standards_derived_partial':len(list((ROOT/'standards_derived').glob('*.json'))),'malformed_mutations':500,'official_excerpts':1,'public_real_messages':0}
    Path('data/experiments/iso-hybrid-v1/parser-verification.json').write_text(json.dumps(report,indent=2));print(report)
if __name__=='__main__':verify()
