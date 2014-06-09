# -*- encoding: utf-8 -*-
import os
from abjad import *
import scoremanager
score_manager = scoremanager.core.AbjadIDE(is_test=True)
metadata_py_path = os.path.join(
    score_manager._configuration.example_score_packages_directory,
    'red_example_score',
    'materials',
    'magic_numbers',
    '__metadata__.py',
    )


def test_MaterialPackageManager_add_metadatum_01():

    with systemtools.FilesystemState(keep=[metadata_py_path]):
        # make sure no flavor metadatum found
        input_ = 'red~example~score m magic~numbers mdg flavor <return> q'
        score_manager._run(input_=input_)
        assert 'None' in score_manager._transcript.contents

        # add flavor metadatum
        input_ = 'red~example~score m magic~numbers mda flavor cherry q'
        score_manager._run(input_=input_)

        # maker sure flavor metadatum now equal to 'cherry'
        input_ = 'red~example~score m magic~numbers mdg flavor <return> q'
        score_manager._run(input_=input_)
        assert "'cherry'" in score_manager._transcript.contents