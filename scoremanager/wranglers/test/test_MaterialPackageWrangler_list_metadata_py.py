# -*- encoding: utf-8 -*-
import os
from abjad import *
import scoremanager
score_manager = scoremanager.core.AbjadIDE(is_test=True)


def test_MaterialPackageWrangler_list_metadata_py_01():

    metadata_py_path = os.path.join(
        score_manager._configuration.example_score_packages_directory,
        'red_example_score',
        'materials',
        '__metadata__.py',
        )

    input_ = 'red~example~score m mdls q'
    score_manager._run(input_=input_)
    contents = score_manager._transcript.contents

    assert metadata_py_path in contents


def test_MaterialPackageWrangler_list_metadata_py_02():

    metadata_py_path = os.path.join(
        score_manager._configuration.wrangler_views_directory,
        '__metadata__.py',
        )

    input_ = 'm mdls q'
    score_manager._run(input_=input_)
    contents = score_manager._transcript.contents

    assert metadata_py_path in contents