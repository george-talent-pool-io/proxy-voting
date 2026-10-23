"""A negated voting condition is not a negated voting opportunity."""
import pytest
from fast_cascade.laya import vote_conflicts
from hybrid.semantics import passages


def native(text,value):
    return [{'value':value,'confidence':.999,'truncated':False} for _ in passages(text)]


@pytest.mark.parametrize('text',[
    'Registration is not a voting prerequisite.',
    'No voting restriction applies.',
    'There is no voting deadline stated here.',
    'A POA is not a voting condition.',
    'The holder cannot vote unless registration is completed.',
    'No votes may be cast before the register opens.',
    'No ballot will be rejected because a POA was not arranged.',
    'No vote will be rejected because registration is unnecessary.',
])
def test_negated_conditions_do_not_contradict_current_vote(text):
    assert vote_conflicts(text,native(text,'NO'),'VOTABLE')==[]


@pytest.mark.parametrize('text',[
    'This is not a voting event.',
    'There is no voting opportunity.',
    'This notice is provided for information only.',
    'Shareholders cannot vote in this event.',
])
def test_explicit_current_denial_still_forces_conflict(text):
    assert vote_conflicts(text,native(text,'NO'),'VOTABLE')


def test_topic_statement_does_not_invent_a_voting_opportunity():
    text='Voting restrictions are described in the market guide.'
    assert vote_conflicts(text,native(text,'YES'),'NOT_VOTABLE')==[]
    text='Shareholders may cast votes at the meeting.'
    assert vote_conflicts(text,native(text,'YES'),'NOT_VOTABLE')
