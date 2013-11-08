# -*- encoding: utf-8 -*-
from abjad import *


def test_marktools_Dynamic___repr___01():
    r'''Dynamic mark returns nonempty string repr.
    '''

    repr = Dynamic('f').__repr__()
    assert isinstance(repr, str) and 0 < len(repr)
