# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager


def test_Selector_make_performer_selector_01():

    session = scoremanager.core.Session()
    session.current_score_snake_case_name = 'red_example_score'
    selector = scoremanager.iotools.Selector
    selector = selector.make_performer_selector(session=session)
    result = selector._run(pending_user_input='hornist')

    performer = instrumenttools.Performer(
        name='hornist', 
        instruments=[instrumenttools.FrenchHorn()]
        )
    assert result == performer
