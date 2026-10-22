"""Evidence selection must preserve native labels without hiding real conflicts."""
import pytest
from cascade.aggregation import AggregationConfig
from fast_cascade.aggregation import aggregate
from hybrid.semantics import passages
from training.framework.passage_runtime import document_with_passage_evidence


def combine(text, values, document='YES', key='share_blocking', route=None):
    assert len(list(passages(text))) == len(values)
    native = [{'value': v, 'scores': {c: .98 if c == v else .01 for c in ('YES','NO','UNKNOWN')},
               'confidence': .98, 'margin': .97, 'truncated': False} for v in values]
    diagnostic = aggregate(text, key, native, AggregationConfig(voting_route=route))
    return document_with_passage_evidence({'value': document, 'scores': {'YES': .98, 'NO': .01, 'UNKNOWN': .01},
                                           'evidence': []}, diagnostic)


def test_unrelated_negative_is_not_contrary_evidence():
    p = combine('Shares will be blocked. Registration is unnecessary.', ['YES','NO'])
    assert p['value'] == 'YES' and not p['conflict']
    assert p['evidence'][0]['text'] == 'Shares will be blocked.'


@pytest.mark.parametrize('key,positive,negative', [
    ('share_blocking','Shares will be blocked.','Shares will not be blocked.'),
    ('poa_required','A power of attorney is mandatory.','No power of attorney is required.'),
    ('registration_required','Registration is mandatory.','Registration is not required.'),
    ('beneficial_owner_disclosure_required','Beneficial owner disclosure is mandatory.','Beneficial owner disclosure is not required.'),
    ('securities_lending_recall_required','Securities on loan must be recalled.','No recall is required.'),
])
def test_current_opposing_passages_are_visible(key,positive,negative):
    p = combine(positive+' '+negative, ['YES','NO'], key=key)
    assert p['value'] == 'YES' and p['conflict'] and not p['evidence']
    assert p['passage_diagnostic']['conflict']


def test_document_disagrees_with_current_negative_requires_review():
    p = combine('Shares will not be blocked.', ['NO'])
    assert p['value'] == 'YES' and p['document_passage_disagreement'] and p['conflict']


def test_historic_positive_cannot_be_displayed_as_current_support():
    p = combine('Historically shares were blocked. Final terms confirm no blocking applies.', ['YES','NO'], document='NO')
    assert p['value'] == 'NO' and not p['conflict']
    assert p['evidence'][0]['text'] == 'Final terms confirm no blocking applies.'


def test_explicit_supersession_preserved():
    p = combine('Shares will be blocked. The amended terms confirm no blocking applies.', ['YES','NO'], document='NO')
    assert not p['conflict'] and p['passage_diagnostic']['aggregation_reason'] == 'EXPLICIT_LATER_SUPERSESSION'
    assert p['evidence'][0]['text'].startswith('The amended')


def test_unresolved_route_is_not_evidence_of_unconditional_requirement():
    text='Shares will be blocked only if physical attendance is requested. Electronic proxy voting does not cause blocking.'
    p=combine(text,['YES','NO'])
    assert p['conflict'] and not p['evidence']
    selected=combine(text,['YES','NO'],document='NO',route='ELECTRONIC_PROXY')
    assert not selected['conflict'] and selected['evidence']


def test_missing_positive_evidence_is_not_invented():
    p=combine('The service desk is open.', ['NO'])
    assert p['value']=='YES' and not p['evidence'] and not p['conflict']


@pytest.mark.parametrize('unrelated', ['No power of attorney is required.',
    'The agent waives recall of securities on loan.',
    'No restriction on splitting votes applies.',
    'Beneficial-owner disclosure is not required for the current vote.'])
def test_named_waiver_is_not_negative_evidence_for_residual_restriction(unrelated):
    text='Only professional investors are eligible to vote. '+unrelated
    p=combine(text,['YES','NO'],key='other_voting_restriction')
    assert not p['conflict'] and p['evidence'][0]['text'].startswith('Only professional')
    state=p['passage_diagnostic']['passage_states'][1]
    assert state['native_value']=='NO' and state['state']=='UNKNOWN'


def test_genuine_residual_waiver_still_conflicts():
    text='Only professional investors are eligible to vote. No professional-investor eligibility restriction applies.'
    p=combine(text,['YES','NO'],key='other_voting_restriction')
    assert p['conflict'] and not p['evidence']


def test_one_residual_waiver_does_not_remove_an_independent_condition():
    text='Only professional investors are eligible to vote. No residency eligibility restriction applies.'
    p=combine(text,['YES','NO'],key='other_voting_restriction')
    assert not p['conflict'] and p['evidence'][0]['text'].startswith('Only professional')


def test_explicit_other_scope_not_discarded_alongside_named_topic():
    text='No other voting restrictions apply; the POA is optional.'
    p=combine(text,['NO'],document='NO',key='other_voting_restriction')
    assert p['evidence'] and not p['conflict']
