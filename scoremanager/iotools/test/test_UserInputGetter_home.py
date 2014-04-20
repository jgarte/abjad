# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager


def test_UserInputGetter_home_01():

    score_manager = scoremanager.core.ScoreManager(is_test=True)
    input_ = 'red~example~score m tempo~inventory mae 1 d h q'
    score_manager._run(pending_user_input=input_)
    assert score_manager._transcript.signature == (15, (0, 13))