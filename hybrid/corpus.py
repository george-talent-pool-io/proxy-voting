"""Reproducible parser fixtures; never a source of semantic training labels."""
import hashlib,json
from pathlib import Path
ROOT=Path('data/iso15022_corpus')
DATE='2026-10-16'
ISO='https://www.iso20022.org/15022/uhb/'

def fixture(i):
    mt=['564','568','565','567'][i%4];event=['MEET','OMET','XMET','BMET','CMET','DVCA','TEND'][i%7]
    function='REPL' if i%11==0 and mt in {'564','568'} else 'CANC' if i%13==0 and mt in {'564','565','568'} else 'RMDR' if i%17==0 and mt in {'564','568'} else 'INST' if mt=='567' else 'NEWM'
    seme=f'S{i:010d}';corp=f'C{i//4:010d}'
    lines=[':16R:GENL',f':20C::SEME//{seme}',f':20C::CORP//{corp}',f':23G:{function}',f':22F::CAEV//{event}']
    if mt=='564':lines+=[':22F::CAMV//VOLU',':25D::PROC//COMP']
    if function in {'REPL','CANC','RMDR'} or mt=='567':lines+=[':16R:LINK',f':20C::PREV//S{max(0,i-4):010d}',':16S:LINK']
    if mt=='567':lines+=[':16R:STAT',':25D::IPRC//PACK',':16S:STAT']
    lines+=[':16S:GENL']
    if mt in {'564','565'} or i%3==0:lines+=[':16R:USECU',':35B:ISIN GB0002634946','SYNTHETIC PARSER SECURITY',':16S:USECU']
    if mt=='564':
        lines+=[':16R:CADETL',':98A::MEET//20261030',':98A::RDTE//20261001',':16S:CADETL']
        for j in range(1,2+i%3):
            tag,val=[('98A','20261020'),('98C','20261020170000'),('98E','20261020170000,000/01')][(i+j)%3]
            lines+=[':16R:CAOPTN',f':13A::CAON//{j:03d}',':22F::CAOP//NOAC',':17B::DFLT//N',f':{tag}::RDDT//{val}',':16S:CAOPTN']
    if mt=='565':lines+=[':16R:CAINST',':13A::CAON//001',':22F::CAOP//NOAC',':16S:CAINST']
    narrative=['No power of attorney is required.','Shares will be blocked until the meeting.','Registration is required before voting.','The meeting agenda will follow separately.'][i%4]
    qualifier=['ADTX','REGI','COMP'][i%3]
    if mt=='568' or i%5:
        import textwrap
        lines+=[':16R:ADDINFO',f':70E::{qualifier}//'+ '\n'.join(textwrap.wrap(narrative,35)),':16S:ADDINFO']
    raw='\n'.join(lines)+'\n'
    if i%2==0:raw='{1:F01TESTBIC0XXXX0000000000}{2:I'+mt+'TESTBIC0XXXXN}{4:\n'+raw+'-}'
    if i%5==0:raw=raw.replace('\n','\r\n')
    # These are deliberate partial messages; no claim of network-valid fixtures.
    return {'id':f'derived-{i:04d}','source_type':'STANDARDS_DERIVED_SYNTHETIC','source_url':ISO+f'finmt{mt}.htm','source_organisation':'ISO15022 dictionary; locally authored fixture','retrieved_at':DATE,'message_type':'MT'+mt,'notes':'Structurally generated PARTIAL message. Missing full mandatory/account/network requirements; parser subset only. Never semantic training data.','raw':raw,'expected':{'seme':seme,'corp':corp,'caev':event,'function':function,'kind':'PARTIAL_ISO15022','narrative': ('\r\n' if i%5==0 else '\n').join(__import__('textwrap').wrap(narrative,35)) if mt=='568' or i%5 else None}}


def generate():
    for sub in ['official_examples','public_examples','standards_derived','malformed']:(ROOT/sub).mkdir(parents=True,exist_ok=True)
    for i in range(1000):
        row=fixture(i);(ROOT/'standards_derived'/f'{row["id"]}.json').write_text(json.dumps(row,ensure_ascii=False,indent=2)+'\n')
    for i in range(500):
        row=fixture(i);mode=i%5
        mutations=[lambda t:t.replace(':16S:GENL',':16S:WRONG'),lambda t:t.replace(':20C::SEME//',':20C:??SEME//'),lambda t:t.replace(':16S:ADDINFO',''),lambda t:t.replace('20261030','20261399'),lambda t:t+'\n:99Z::WHAT//preserve me\n']
        row['raw']=mutations[mode](row['raw']);row['id']=f'mutated-{i:04d}';row['notes']=f'Mutation mode {mode}; may be tolerated/partial rather than rejected. No semantic ground truth.';row['expected']={'unknown_preserved':True};row['mutation']=mode
        (ROOT/'malformed'/f'{row["id"]}.json').write_text(json.dumps(row,ensure_ascii=False,indent=2)+'\n')
    official={'id':'clearstream-dscl-excerpt','source_type':'OFFICIAL_EXAMPLE','source_url':'https://www.clearstream.com/caas/v1/media/2224604/data/9829e51a4582a1ade84615ea7d7cb3bf/c20019-c20030-l20022-l20033-d20039-mt564-example.pdf','source_organisation':'Clearstream','retrieved_at':DATE,'message_type':'MT564','notes':'Short literal field excerpt from right column, page 1; not full message, not production. Copyright Clearstream, no redistribution licence identified; full PDF remains outside corpus. Published SEME is 17 characters versus dictionary 16x: preserved UNKNOWN, not normalised into compliance.','raw':':16R:GENL\n:20C::CORP//810651611\n:20C::SEME//EBDSCL00120191004\n:23G:NEWM\n:22F::CAEV//DSCL\n:22F::CAMV//MAND\n:98C::PREP//20191004094253\n:25D::PROC//COMP\n:16S:GENL\n','expected':{'corp':'810651611','caev':'DSCL','kind':'PARTIAL_ISO15022'}}
    (ROOT/'official_examples'/f'{official["id"]}.json').write_text(json.dumps(official,indent=2)+'\n')
    rows=[]
    for folder in ['official_examples','public_examples','standards_derived','malformed']:
        for p in sorted((ROOT/folder).glob('*.json')):
            r=json.loads(p.read_text());rows.append({**{k:r[k] for k in ['id','source_type','source_url','source_organisation','retrieved_at','message_type','notes']},'path':str(p.relative_to(ROOT)),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'raw_sha256':hashlib.sha256(r['raw'].encode()).hexdigest()})
    (ROOT/'sources.jsonl').write_text(''.join(json.dumps(r)+'\n' for r in rows))
    return {'standards_derived_partial':1000,'mutated':500,'official_excerpt':1,'public_production':0}
if __name__=='__main__':print(generate())
