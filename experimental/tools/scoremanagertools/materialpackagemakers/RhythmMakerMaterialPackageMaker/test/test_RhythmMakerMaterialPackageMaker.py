from abjad.tools import rhythmmakertools
from experimental import *


def test_RhythmMakerMaterialPackageMaker_01():

    score_manager = scoremanagertools.scoremanager.ScoreManager()
    assert not packagepathtools.package_exists('built_in_materials.testrhythmmaker')
    try:
        score_manager._run(user_input=
            'materials maker rhythm testrhythmmaker default '
            'testrhythmmaker omi talearhythmmaker '
            '[-1, 2, -3, 4] 16 [2, 3] [6] b default '
            'q '
            )
        mpp = scoremanagertools.materialpackagemakers.RhythmMakerMaterialPackageMaker('built_in_materials.testrhythmmaker')
        assert mpp.list_directory() == ['__init__.py', 'output_material.py', 'tags.py']
        maker = rhythmmakertools.TaleaRhythmMaker(
            [-1, 2, -3, 4],
            16,
            prolation_addenda=[2, 3],
            secondary_divisions=[6])
        assert mpp.output_material == maker
    finally:
        score_manager._run(user_input='m testrhythmmaker del remove default q')
        assert not packagepathtools.package_exists('built_in_materials.testrhythmmaker')
