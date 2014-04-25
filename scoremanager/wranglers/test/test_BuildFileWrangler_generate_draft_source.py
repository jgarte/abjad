# -*- encoding: utf-8 -*-
import filecmp
import os
import shutil
from abjad import *
import scoremanager
score_manager = scoremanager.core.ScoreManager(is_test=True)


def test_BuildFileWrangler_generate_draft_source_01():
    r'''Overwrites existing draft source.
    '''

    path = os.path.join(
        score_manager._configuration.example_score_packages_directory_path,
        'red_example_score',
        'build',
        'draft.tex',
        )
    backup_path = path + '.backup'

    assert os.path.isfile(path)
    assert not os.path.exists(backup_path)
    shutil.copyfile(path, backup_path)
    assert os.path.exists(backup_path)

    try:
        input_ = 'red~example~score u dg y y q'
        score_manager._run(pending_user_input=input_)
        contents = score_manager._transcript.contents
        assert 'Overwrite' in contents
        assert 'Will assemble segments in this order:' in contents
        assert 'Overwrote' in contents
        assert os.path.isfile(path)
        assert filecmp.cmp(path, backup_path)
    finally:
        shutil.move(backup_path, path)

    assert os.path.isfile(path)
    assert not os.path.exists(backup_path)


def test_BuildFileWrangler_generate_draft_source_02():
    r'''Works with empty build directory.

    (Blue Example Score segment views module is intentionally corrupt.)
    '''

    path = os.path.join(
        score_manager._configuration.example_score_packages_directory_path,
        'blue_example_score',
        'build',
        'draft.tex',
        )

    assert not os.path.exists(path)

    try:
        input_ = 'blue~example~score u dg y q'
        score_manager._run(pending_user_input=input_)
        contents = score_manager._transcript.contents
        message = 'SegmentPackageWrangler views module is corrupt.' 
        assert message not in contents
        assert 'Will assemble segments in this order:' in contents
        assert os.path.isfile(path)
    finally:
        if os.path.exists(path):
            os.remove(path)

    assert not os.path.exists(path)


def test_BuildFileWrangler_generate_draft_source_03():
    r'''Works when no segments have been created.
    '''

    path = os.path.join(
        score_manager._configuration.example_score_packages_directory_path,
        'etude_example_score',
        'build',
        'draft.tex',
        )
    backup_path = path + '.backup'

    assert os.path.isfile(path)
    assert not os.path.exists(backup_path)
    shutil.copyfile(path, backup_path)
    assert os.path.exists(backup_path)

    try:
        input_ = 'etude~example~score u dg y y q'
        score_manager._run(pending_user_input=input_)
        contents = score_manager._transcript.contents
        assert 'Overwrite' in contents
        assert 'No segments found:' in contents
        assert 'will generate source without segments' in contents
        assert 'Overwrote' in contents
        assert os.path.isfile(path)
        assert filecmp.cmp(path, backup_path)
    finally:
        shutil.move(backup_path, path)

    assert os.path.isfile(path)
    assert not os.path.exists(backup_path)