# -*- encoding: utf-8 -*-
from abjad import *


def test_marktools_Clef_list_clef_names_01():

    assert 'treble' in Clef.list_clef_names()
