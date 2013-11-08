# -*- encoding: utf-8 -*-
from abjad import *


def test_marktools_Tempo_duration_01():
    r'''Duration of tempo mark is read / write.
    '''

    tempo = Tempo(Duration(1, 8), 52)
    assert tempo.duration == Duration(1, 8)

    tempo.duration = Duration(1, 4)
    assert tempo.duration == Duration(1, 4)

    tempo.duration = None
    assert tempo.duration is None
