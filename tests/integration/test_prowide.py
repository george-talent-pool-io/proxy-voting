"""Real local JVM integration, with no model or network call."""
import pytest
from iso_adapter.prowide import Prowide
from iso_adapter.benchmark import fin
from iso_adapter.routing import route
from iso_adapter.facts import project,deadline
from qwen_domain.protocol import ROOT,read

@pytest.fixture
def helper():
    h=Prowide()
    try:yield h
    finally:h.close()

@pytest.mark.parametrize('mt',[*range(540,549),564,565,566,568])
def test_category5_envelope_and_typed_components(helper,mt):
    # Partial body; not a complete mandatory-field conformance fixture.
    text=fin(':16R:GENL\n:20C::SEME//EXAMPLE\n:23G:NEWM\n:16S:GENL',str(mt));r=helper.parse(text)
    assert r['message_type']==f'MT{mt}' and r['parse_status']=='PARSED_NOT_VALIDATED'
    assert r['references']['SEME'][0]['components']==['SEME','EXAMPLE']
    assert r['raw_source']==text and r['standards_validated'] is False

def test_publisher_category5_message_and_restart(helper):
    item=read(ROOT/'data/iso15022_corpus/prowide_reference/prowide-mt564.json');text=item['raw']
    a=helper.parse(text);helper.close();b=helper.parse(text)
    for key in ['fields','narratives','references','security','event','dates','options']:assert a[key]==b[key]
    assert sum(f['tag']=='16R' for f in a['fields'])==6
    assert a['references']['CORP'][0]['components']==['CORP','D455103']
    assert a['security']['isins'][0]['value']=='CH0011075394'
    assert all(text[f['start']:f['end']]==f['source_text'] for f in a['fields'] if 'start' in f)
    assert all(text[n['text_start']:n['text_end']]==n['text'] for n in a['narratives'])

def test_repeated_options_and_timezone_aware_deadline(helper):
    text=fin(':16R:CAOPTN\n:22F::CAOP//PROX\n:98E::RDDT//20261020170000,000/00\n:16S:CAOPTN\n:16R:CAOPTN\n:22F::CAOP//ABST\n:98E::RDDT//20261020170000,000/00\n:16S:CAOPTN')
    r=helper.parse(text);facts=project(r)
    assert len(r['options'])==2
    assert [f['sequence_path'] for f in facts if f['name']=='caop']==[['CAOPTN[1]'],['CAOPTN[2]']]
    assert deadline(r,'2026-10-17T12:00:00+00:00')['status']=='OPEN'

def test_unmatched_sequence_is_recovered_not_validated(helper):
    text=fin(':16R:ADDINFO\n:70E::ADTX//POA required.\n:16S:WRONG')
    r=route(text,helper)
    assert r['parser']=='LENIENT_RECOVERY' and r['raw_source']==text and r['warnings']

@pytest.mark.parametrize('ending',['\n','\r\n','\r'])
def test_multiline_source_offsets_survive_fin_line_endings(helper,ending):
    text=fin(':16R:ADDINFO\n:70E::ADTX//First narrative line\nSecond narrative line\n:16S:ADDINFO','568').replace('\n',ending)
    routed=route(text,helper);r=routed['structure']
    assert r['raw_source']==text
    # Lone CR is a damaged excerpt representation, not standard FIN CRLF.
    # Core fails to separate its fields; the production path must recover it.
    assert routed['parser']==('LENIENT_RECOVERY' if ending=='\r' else 'PROWIDE')
    assert r['narratives'] and r['narratives'][0]['text']=='First narrative line'+ending+'Second narrative line'+ending
    n=r['narratives'][0];assert text[n['text_start']:n['text_end']]==n['text']
