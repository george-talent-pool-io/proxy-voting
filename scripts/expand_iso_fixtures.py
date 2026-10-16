"""Linked event chains, separately authored from verified field templates."""
import json,hashlib
from pathlib import Path
from hybrid.corpus import ROOT,DATE,ISO

def expand():
    for event in range(25):
        for step in range(4):
            mt='568' if step==1 else '564';fn=['NEWM','NEWM','REPL','CANC'][step]
            seme=f'CHAIN{event:03d}S{step}';corp=f'CHAIN{event:03d}'
            lines=[':16R:GENL',f':20C::SEME//{seme}',f':20C::CORP//{corp}',f':23G:{fn}',':22F::CAEV//MEET']
            if mt=='564':lines+=[':22F::CAMV//VOLU']
            if step:
                qualifier='RELA' if step==1 else 'PREV';prev=f'CHAIN{event:03d}S{0 if step<3 else 2}'
                lines+=[':16R:LINK',':13A::LINK//564',f':20C::{qualifier}//{prev}',':16S:LINK']
            lines+=[':16S:GENL']
            if step in {0,2}:
                lines+=[':16R:USECU',':35B:ISIN GB0002634946',':16S:USECU',':16R:CADETL',':98A::MEET//20261030',':16S:CADETL']
                for option,code in [(1,'PROX'),(2,'ABST')]:lines+=[':16R:CAOPTN',f':13A::CAON//{option:03d}',f':22F::CAOP//{code}',':17B::DFLT//N',f':98E::RDDT//202610{15 if step==0 else 18}170000,000/00',':16S:CAOPTN']
            if step==1:lines+=[':16R:ADDINFO',':70E::ADTX//A power of attorney is required', 'to vote at this meeting.',':16S:ADDINFO']
            raw='{2:I'+mt+'TESTBIC0XXXXN}{4:\n'+'\n'.join(lines)+'\n-}'
            row={'id':f'chain-{event:03d}-{step}','source_type':'STANDARDS_DERIVED_SYNTHETIC','source_url':ISO+f'finmt{mt}.htm','source_organisation':'ISO dictionary; locally authored partial chain','retrieved_at':DATE,'message_type':'MT'+mt,'notes':'Generated partial event lifecycle scenario, not production data. Same sender/CORP; distinct SEME; narrative RELA linkage; replacements/cancellation PREV. Excluded from ML training.','raw':raw,'expected':{'seme':seme,'corp':corp,'function':fn,'caev':'MEET','kind':'PARTIAL_ISO15022'}}
            (ROOT/'standards_derived'/f'{row["id"]}.json').write_text(json.dumps(row,indent=2)+'\n')
    # Rebuild per-item provenance manifest, including original fixtures.
    rows=[]
    for folder in ['official_examples','public_examples','standards_derived','malformed']:
        for p in sorted((ROOT/folder).glob('*.json')):
            r=json.loads(p.read_text());rows.append({**{k:r[k] for k in ['id','source_type','source_url','source_organisation','retrieved_at','message_type','notes']},'path':str(p.relative_to(ROOT)),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'raw_sha256':hashlib.sha256(r['raw'].encode()).hexdigest()})
    (ROOT/'sources.jsonl').write_text(''.join(json.dumps(r)+'\n' for r in rows))
    return len(rows)
if __name__=='__main__':print(expand())
