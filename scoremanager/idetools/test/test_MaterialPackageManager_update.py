# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager
score_manager = scoremanager.idetools.AbjadIDE(is_test=True)
score_manager._session._is_repository_test = True


def test_MaterialPackageManager_update_01():

    input_ = 'red~example~score m magic~numbers rup q'
    score_manager._run(input_=input_)
    assert score_manager._session._attempted_to_update