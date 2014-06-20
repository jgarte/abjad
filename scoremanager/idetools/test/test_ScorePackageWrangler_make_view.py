# -*- encoding: utf-8 -*-
import os
import pytest
from abjad import *
import scoremanager
# is_test=True is ok when testing the creation of views
score_manager = scoremanager.idetools.AbjadIDE(is_test=True)
views_file = os.path.join(
    score_manager._configuration.wrangler_views_directory,
    '__ScorePackageWrangler_views__.py',
    )
metadata_file = os.path.join(
    score_manager._configuration.wrangler_views_directory,
    '__metadata__.py',
    )


def test_ScorePackageWrangler_make_view_01():
    r'''Makes sure view creation menu title is correct.
    '''

    with systemtools.FilesystemState(keep=[views_file, metadata_file]):
        os.remove(metadata_file)
        input_ = 'vnew _test q' 
        score_manager._run(input_=input_)
        contents = score_manager._transcript.contents
        string = 'Abjad IDE - scores - views - _test (EDIT)'
        assert string in contents


def test_ScorePackageWrangler_make_view_02():
    r'''Makes sure at least one score appears in view creation menu.
    '''

    with systemtools.FilesystemState(keep=[views_file, metadata_file]):
        os.remove(metadata_file)
        input_ = 'vnew _test q' 
        score_manager._run(input_=input_)
        transcript = score_manager._transcript
        string = 'Red Example Score'
        assert string in transcript.contents