import json
from pathlib import Path
import pytest
from hypothesis import given,settings,strategies as st
from hybrid.parser import parse,facts,date_value,deadline_status
from hybrid.corpus import fixture


def sample(extra='',mt='564'):
    return f'{{2:I{mt}TESTBIC0XXXXN}}{{4:\n:16R:GENL\n:20C::SEME//ONE\n:20C::CORP//EVENT\n:23G:NEWM\n:22F::CAEV//MEET\n:16S:GENL\n'+extra+'-}'

def test_parse_message_type():assert parse(sample())['message_type']=='MT564'
def test_parse_sequences():assert not parse(sample())['errors']
def test_parse_nested_sequences():
    p=parse(sample(':16R:CAOPTN\n:16R:CASHMOVE\n:99Z:KEEP\n:16S:CASHMOVE\n:16S:CAOPTN\n'))
    assert next(f for f in p['fields'] if f['tag']=='99Z')['path']==['CAOPTN[1]','CASHMOVE[1]']
@pytest.mark.parametrize('name,value',[('caev','MEET'),('corp','EVENT'),('seme','ONE')])
def test_parse_references(name,value):assert facts(parse(sample()),name)[0]['value']==value

def test_parse_isin_security_description():
    p=parse(sample(':16R:USECU\n:35B:ISIN GB0002634946\nTEST SECURITY\n:16S:USECU\n'))
    assert facts(p,'security')[0]['value']=={'isin':'GB0002634946','description':'TEST SECURITY'}
def test_parse_meeting_date():
    p=parse(sample(':16R:CADETL\n:98A::MEET//20261030\n:16S:CADETL\n'))
    assert facts(p,'meet')[0]['value']['iso']=='2026-10-30'
def test_parse_response_deadline():
    p=parse(sample(':16R:CAOPTN\n:98E::RDDT//20261020170000,000/01\n:16S:CAOPTN\n'))
    assert deadline_status(p,'2026-10-20T16:00:01Z')['status']=='PASSED'
    assert deadline_status(p,'2026-10-20T15:59:59Z')['status']=='OPEN'
def test_local_time_not_utc():
    p=parse(sample(':16R:CAOPTN\n:98C::RDDT//20261020170000\n:16S:CAOPTN\n'))
    assert deadline_status(p,'2026-10-30T12:00:00Z')['status']=='UNKNOWN'
def test_options_repeated_fields():
    p=parse(sample(':16R:CAOPTN\n:13A::CAON//001\n:22F::CAOP//NOAC\n:16S:CAOPTN\n:16R:CAOPTN\n:13A::CAON//002\n:16S:CAOPTN\n'))
    assert [f['value'] for f in facts(p,'option_number')]==['001','002']
    assert len({tuple(f['path']) for f in facts(p,'option_number')})==2

def test_narrative_multiple_exact_offsets():
    raw=sample(':16R:ADDINFO\n:70E::ADTX//ü😀 Evidence\ncontinuation\n:70E::REGI//not required\n:16S:ADDINFO\n')
    p=parse(raw)
    assert len(facts(p,'narrative'))==2
    for f in facts(p,'narrative'):assert raw[f['value_start']:f['end']]==f['value']

def test_partial_missing_envelope():assert parse(':16R:GENL\n:20C::SEME//X\n:16S:GENL')['kind']=='PARTIAL_ISO15022'
def test_unknown_qualifier():
    p=parse(sample(':98A::ZZZZ//20261030\n:99Z::WHAT//opaque\n'))
    assert p['routing'][-1]['route']=='UNKNOWN_FIELDS'
    assert not facts(p,'zzzz')
@pytest.mark.parametrize('s',['20260230','20261301','202610','bogus','20261020176000'])
def test_parse_malformed_date(s):assert date_value('98A' if len(s)==8 else '98C',s) is None

def test_no_timezone_injected():assert not date_value('98E','20261020170000')['offset_known']
def test_date_offsets():assert date_value('98E','20261020170000,1/N0530')['iso']=='2026-10-20T17:00:00.100000-05:30'
def test_scope_and_dss():
    p=parse(sample(':16R:ADDINFO\n:98A::MEET//20261030\n:22F::CAEV/VENDOR/MEET\n:16S:ADDINFO\n'))
    assert not facts(p,'meet')
    assert len(facts(p,'caev'))==1

@pytest.mark.parametrize('path',sorted(Path('data/iso15022_corpus/standards_derived').glob('*.json'))+sorted(Path('data/iso15022_corpus/official_examples').glob('*.json')),ids=lambda p:p.stem)
def test_standards_derived_exact(path):
    r=json.loads(path.read_text());p=parse(r['raw'],r['message_type'])
    assert p['raw']==r['raw'];assert not p['errors'];assert p['kind']==r['expected']['kind']
    for key in ['seme','corp','caev','function']:
        if key in r['expected']:assert facts(p,key)[0]['value']==r['expected'][key]
    if r['expected'].get('narrative') is not None:assert facts(p,'narrative')[0]['value']==r['expected']['narrative']
    for f in p['fields']:assert r['raw'][f['start']:f['end']].startswith(':'+f['tag']+':')
    assert len(p['routing'])==len(p['fields'])

@pytest.mark.parametrize('path',sorted(Path('data/iso15022_corpus/malformed').glob('*.json')),ids=lambda p:p.stem)
def test_malformed_corpus_lossless(path):
    r=json.loads(path.read_text());p=parse(r['raw'],r['message_type']);assert p['raw']==r['raw']
    assert len(p['routing'])==len(p['fields'])

@settings(max_examples=250,deadline=None)
@given(st.text(max_size=15000))
def test_arbitrary_unicode_never_crashes(raw):
    p=parse(raw);assert p['raw']==raw
    for f in p['fields']:assert 0<=f['start']<=f['end']<=len(raw)

@settings(max_examples=75,deadline=None)
@given(st.sampled_from(['\n','\r\n','\r']),st.booleans(),st.text(alphabet='abc é😀\t',max_size=30))
def test_line_endings_envelope_unicode(newline,envelope,suffix):
    raw=sample(':16R:ADDINFO\n:70E::ADTX//'+suffix+'\n:16S:ADDINFO\n')
    if not envelope:raw=raw[raw.index(':16R:'):raw.rindex('-}')]
    raw=raw.replace('\n',newline);p=parse(raw)
    assert facts(p,'seme')[0]['value']=='ONE';assert not p['errors']

@pytest.mark.parametrize('value',[None,42,{},[],b'bytes'])
def test_non_string(value):assert parse(value)['kind']=='UNRECOGNISED'


@settings(max_examples=100,deadline=None)
@given(st.dates(min_value=__import__('datetime').date(2000,1,1),max_value=__import__('datetime').date(2099,12,31)))
def test_valid_date_property(d):assert date_value('98A',d.strftime('%Y%m%d'))['iso']==d.isoformat()

@settings(max_examples=100,deadline=None)
@given(st.integers(min_value=0,max_value=999),st.sampled_from(['\r\n','\n','\r']))
def test_field_spans_cover_body_losslessly(i,newline):
    r=fixture(i);raw=r['raw'].replace('\r\n','\n').replace('\n',newline);p=parse(raw,r['message_type'])
    segments=p['segments']
    if segments:
        assert all(a['end']==b['start'] for a,b in zip(segments,segments[1:]))
        assert ''.join(raw[s['start']:s['end']] for s in segments)==raw[segments[0]['start']:segments[-1]['end']]

def test_reference_too_long_preserved_unknown():
    raw=sample(':20C::SEME//ABCDEFGHIJKLMNOPQ\n');p=parse(raw)
    assert len(facts(p,'seme'))==1
    assert p['fields'][-1]['value']=='ABCDEFGHIJKLMNOPQ'
    assert p['routing'][-1]['route']=='UNKNOWN_FIELDS'
