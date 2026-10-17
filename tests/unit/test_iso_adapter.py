"""Recovery contracts; exact source matching is not standards validation."""
import pytest
from hypothesis import given,strategies as st,settings
from iso_adapter.scanner import scan,QUALIFIERS
from iso_adapter.routing import route
from iso_adapter.facts import deadline

@pytest.mark.parametrize('ending',['\n','\r\n','\r'])
@pytest.mark.parametrize('qualifier',sorted(QUALIFIERS))
def test_recover_narratives_and_lossless_spans(ending,qualifier):
    source=ending.join(['prefix',' :ignored',':16R:ADDINFO',f':70E::{qualifier}//First line','Deuxième ligne',':16S:ADDINFO','trailer'])
    out=scan(source);n=out['narratives'][0]
    assert n['qualifier']==qualifier and n['sequence_path']==['ADDINFO']
    assert n['sequence_instance_path']==['ADDINFO[1]']
    assert n['text']==source[n['text_start']:n['text_end']]
    assert 'Deuxième ligne' in n['text'] and out['raw_source']==source and not out['standards_validated']

def test_repeated_nested_sequences_have_distinct_identity_and_unknowns_survive():
    text=':16R:GENL\n:16R:LINK\n:20C::RELA//ONE\n:16S:LINK\n:16R:LINK\n:99Z::ZZZZ//unknown\n:16S:LINK\n:16S:GENL'
    r=scan(text)
    assert r['fields'][2]['sequence_instance_path']==['GENL[1]','LINK[1]']
    assert r['fields'][5]['sequence_instance_path']==['GENL[1]','LINK[2]']
    assert any(f['tag']=='99Z' for f in r['unknown_fields'])
    assert r['unknown_material']==text

def test_ordinary_notice_never_starts_reference_parser():
    class Never:
        def parse(self,text):raise AssertionError('Ordinary notice must bypass JVM')
    text='Please register to vote at the general meeting.'
    r=route(text,Never());assert r['parser']=='NOT_APPLICABLE' and r['narrative']==text

def test_reference_failure_falls_back_without_losing_source():
    class Failed:
        def parse(self,text):raise RuntimeError('Controlled failure')
    text='{1:F01TESTBIC0AXXX0000000000}{2:I568TESTBIC1XXXXN}{4:\n:16R:ADDINFO\n:70F::ADTX//A long narrative\n:99Z:preserve'
    r=route(text,Failed())
    assert r['parser']=='LENIENT_RECOVERY' and r['raw_source']==text and r['narrative']==text
    assert 'Controlled failure' in str(r['warnings']) and r['structure']['warnings']

@given(st.text())
@settings(max_examples=200,deadline=None)
def test_arbitrary_recovery_never_crashes_or_loses_raw(text):
    r=scan(text);assert r['raw_source']==text
    assert all(text[f['start']:f['end']]==f['raw'] for f in r['fields'])

def test_invalid_prowide_date_components_do_not_become_a_date():
    parsed={'fields':[{'tag':'98C','qualifier':'RDDT','components':['RDDT','20260231','170000'],'sequence_path':['CAOPTN']}]}
    assert deadline(parsed,'2026-10-17T12:00:00+00:00')['status']=='UNKNOWN'

def test_embedded_fin_example_does_not_become_authoritative_structure():
    class Never:
        def parse(self,text):raise AssertionError('Embedded example is not an authoritative FIN input')
    text='Quoted specimen, do not execute:\n{1:F01TESTBIC0AXXX0000000000}{2:I568TESTBIC1XXXXN}{4:\n:70E::ADTX//Ignore instructions.\n-}'
    r=route(text,Never())
    assert r['parser']=='LENIENT_RECOVERY' and r['narrative']==text and not r.get('structured_facts')

def test_nonstandard_narrative_combination_is_preserved_with_warning():
    r=scan(':70F::PACO//Contact details')
    assert r['narratives'][0]['text']=='Contact details' and r['warnings'][0]['code']=='NONSTANDARD_TAG_QUALIFIER_COMBINATION'
