"""An explicitly synthetic persistent lifecycle demonstration, never customer data."""
import json
from pathlib import Path
from hybrid.events import EventLedger
from hybrid.pipeline import analyse
from hybrid.semantics import NarrowLaya
ROOT=Path('data/experiments/iso-hybrid-v1')

def seed():
    ledger=EventLedger('data/iso15022-demo.sqlite');event=None
    for step in range(3):
        p=Path(f'data/iso15022_corpus/standards_derived/chain-000-{step}.json');r=json.loads(p.read_text())
        event=ledger.ingest(r['raw'],'STANDARDS_DERIVED_SYNTHETIC_DEMO',r['message_type'])
    state=EventLedger('data/iso15022-demo.sqlite').event(event['event_id'])
    assert len(state['messages'])==3
    (ROOT/'event-demo.json').write_text(json.dumps({'source_type':'STANDARDS_DERIVED_SYNTHETIC','note':'Persisted, reloaded synthetic event; not public production data','state':state},indent=2))
    model=NarrowLaya('data/models/narrow-v1')
    for identifier in ['clearstream-dscl-excerpt','derived-0002','derived-0004']:
        folder='official_examples' if identifier.startswith('clearstream') else 'standards_derived'
        row=json.loads((Path('data/iso15022_corpus')/folder/(identifier+'.json')).read_text())
        result=analyse(row['raw'],model,row['message_type'])
        for pred in result['semantic_analysis']['predicates'].values():
            ev=pred.get('evidence')
            if ev:assert row['raw'][ev['start']:ev['end']]==ev['text']
        with (ROOT/f'demo-{identifier}.json').open('x') as f:json.dump(result,f,indent=2)
if __name__=='__main__':seed()
