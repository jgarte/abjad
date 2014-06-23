# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager
score_manager = scoremanager.idetools.AbjadIDE(is_test=True)


def test_MakerFileWrangler_go_to_score_segments_01():
    r'''Goes from score maker files to score segments.
    '''

    input_ = 'red~example~score k g q'
    score_manager._run(input_=input_)
    titles = [
        'Abjad IDE - scores',
        'Red Example Score (2013)',
        'Red Example Score (2013) - maker files',
        'Red Example Score (2013) - segments',
        ]
    assert score_manager._transcript.titles == titles