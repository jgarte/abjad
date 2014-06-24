# -*- encoding: utf-8 -*-
import os
from abjad import *
import scoremanager
# must be is_test=False for view tests
score_manager = scoremanager.idetools.AbjadIDE(is_test=False)


def test_ScorePackageWrangler_set_view_01():
    r'''Makes sure only select scores are visible.
    '''
    
    views_file = os.path.join(
        score_manager._configuration.wrangler_views_directory,
        '__ScorePackageWrangler_views__.py',
        )
    metadata_file = os.path.join(
        score_manager._configuration.wrangler_views_directory,
        '__metadata__.py',
        )
    with systemtools.FilesystemState(keep=[views_file, metadata_file]):
        os.remove(views_file)
        os.remove(metadata_file)
        input_ = 'va add _test'
        input_ += ' add Red~Example~Score~(2013) done done'
        input_ += ' vs _test q'
        score_manager._run(input_=input_)
        transcript = score_manager._transcript
        lines = [
            'Abjad IDE - scores [_test]',
            '',
            '   1: Red Example Score (2013)',
            '',
            '      scores - copy (cp)',
            '      scores - new (new)',
            '      scores - remove (rm)',
            '      scores - rename (ren)',
            '',
            ]
        assert any(_.lines == lines for _ in transcript)