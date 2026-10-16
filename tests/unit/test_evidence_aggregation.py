import pytest
from hybrid.semantics import passages
from cascade.aggregation import aggregate,AggregationConfig,STRATEGIES

def native(labels):
    return [{'value':v,'scores':{'YES':.98 if v=='YES' else .01,'NO':.98 if v=='NO' else .01,'UNKNOWN':.98 if v=='UNKNOWN' else .01},'confidence':.98,'margin':.97,'truncated':False} for v in labels]

@pytest.mark.parametrize('text,labels,expected',[
    ('Shares will be blocked until completion of the meeting.',['YES'],'YES'),
    ('Shares will not be blocked.',['NO'],'NO'),
    ('The preliminary notice stated that shares would be blocked. The final terms confirm that no blocking applies.',['YES','NO'],'NO'),
    ('The general market guide mentions share blocking. No blocking applies to this event.',['YES','NO'],'NO'),
    ('Please read the meeting agenda. Shares will be blocked until the meeting ends.',['NO','YES'],'YES'),
    ('Shares will be blocked. The above preliminary condition has been withdrawn. Shares will NOT be blocked.',['YES','NO','NO'],'NO'),
    ('Shares will be blocked. Shares will not be blocked.',['YES','NO'],'UNKNOWN'),
    ('Historically shares were blocked. Current terms are unavailable.',['YES','UNKNOWN'],'UNKNOWN'),
])
def test_scope_and_supersession(text,labels,expected):
    assert len(list(passages(text)))==len(labels)
    r=aggregate(text,'share_blocking',native(labels));assert r['value']==expected
    for e in r['evidence']:assert text[e['start']:e['end']]==e['text']

@pytest.mark.parametrize('predicate,positive,negative',[
    ('poa_required','A power of attorney is required.','No power of attorney is required.'),
    ('registration_required','Registration is mandatory.','Registration is not required.'),
    ('beneficial_owner_disclosure_required','Beneficial owner disclosure is required.','No beneficial owner disclosure is required.'),
    ('securities_lending_recall_required','Loaned securities must be recalled.','Securities recall is not required.'),
    ('holding_confirmation_required','Proof of holdings is required.','Proof of holdings is not required.'),
])
def test_equivalent_restrictions(predicate,positive,negative):
    text='Read the agenda. '+positive
    assert aggregate(text,predicate,native(['NO','YES']))['value']=='YES'
    text=positive+' Final terms: '+negative
    assert aggregate(text,predicate,native(['YES','NO']))['value']=='NO'

@pytest.mark.parametrize('route,expected',[(None,'UNKNOWN'),('ELECTRONIC_PROXY','NO'),('PHYSICAL_ATTENDANCE','YES')])
def test_conditional_routes(route,expected):
    text='Shares will be blocked only if physical attendance is requested. Electronic proxy voting does not cause blocking.'
    r=aggregate(text,'share_blocking',native(['YES','NO']),AggregationConfig(voting_route=route));assert r['value']==expected

@pytest.mark.parametrize('strategy',STRATEGIES)
def test_comparator_strategies_preserve_native_scores(strategy):
    r=aggregate('Shares will be blocked.','share_blocking',native(['YES']),AggregationConfig(strategy=strategy))
    assert r['value']=='YES';assert r['scores']==native(['YES'])[0]['scores'];assert r['passage_states'][0]['start']==0

def test_no_label_inversion_or_regex_positive_override():
    r=aggregate('Shares will be blocked.','share_blocking',native(['NO']))
    assert r['value']!='YES'

def test_source_alignment_mismatch_rejected():
    with pytest.raises(ValueError):aggregate('One sentence.','share_blocking',native(['YES','NO']))


def test_history_of_unrelated_predicate_does_not_create_a_restriction():
    text='Historically shares were blocked. Owners may vote this year.'
    assert aggregate(text,'poa_required',native(['NO','NO']))['value']=='NO'
    assert aggregate(text,'share_blocking',native(['YES','NO']))['value']=='UNKNOWN'


def test_relevant_unexplained_native_no_is_not_a_verified_waiver():
    r=aggregate('Beneficial owner identity disclosure is required.','beneficial_owner_disclosure_required',native(['NO']))
    assert r['value']=='UNKNOWN'


from hypothesis import given,strategies as st,settings
@settings(max_examples=100,deadline=None)
@given(st.text(alphabet=st.characters(blacklist_categories=('Cs',)),max_size=250))
def test_arbitrary_unicode_never_inverts_all_native_no(text):
    spans=list(passages(text));r=aggregate(text,'share_blocking',native(['NO']*len(spans)))
    assert r['value'] in ('NO','UNKNOWN')
    for e in r['evidence']:assert text[e['start']:e['end']]==e['text']

@settings(max_examples=50,deadline=None)
@given(st.text(alphabet='abcdefghijklmnpqrstuvwxyz ',min_size=3,max_size=100).filter(lambda s:bool(s.strip())))
def test_unrelated_absence_cannot_cancel_positive(header):
    text=header.strip()+'. Shares will be blocked.'
    assert aggregate(text,'share_blocking',native(['NO','YES']))['value']=='YES'
