from abjad import *
from abjad.tools.timeintervaltools import *
import py.test


def test_timeintervaltools_explode_intervals_compactly_01():
    '''Number of resulting trees is equal to the maximum depth of the source tree.
    '''
    tree = TimeIntervalTree(timeintervaltools.make_test_intervals())
    dtree = tree.compute_depth()
    xtrees = explode_intervals_compactly(tree)
    assert len(xtrees) == max([interval['depth'] for interval in dtree])

def test_timeintervaltools_explode_intervals_compactly_02():
    '''All resulting trees are non-zero in length.
    '''
    tree = TimeIntervalTree(timeintervaltools.make_test_intervals())
    xtrees = explode_intervals_compactly(tree)
    assert all(len(xtree) for xtree in xtrees)

def test_timeintervaltools_explode_intervals_compactly_03():
    '''All intervals in the source tree appear in the resulting trees once and only once.
    '''
    tree = TimeIntervalTree(timeintervaltools.make_test_intervals())
    xtrees = explode_intervals_compactly(tree)
    collapsed_tree = TimeIntervalTree(xtrees)
    assert tree[:] == collapsed_tree[:]
