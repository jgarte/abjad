from abjad.tools.intervaltreetools.TimeInterval import TimeInterval
from abjad.tools.intervaltreetools.TimeIntervalTree import TimeIntervalTree
from abjad.tools.intervaltreetools.all_are_intervals_or_trees_or_empty import all_are_intervals_or_trees_or_empty
from abjad.tools.intervaltreetools.compute_depth_of_intervals_in_interval import compute_depth_of_intervals_in_interval
from abjad.tools.intervaltreetools.fuse_tangent_or_overlapping_intervals import fuse_tangent_or_overlapping_intervals


def compute_logical_or_of_intervals_in_interval(intervals, interval):
    '''Compute the logical OR of a collection of intervals,
    cropped within `interval`.
    '''

    assert all_are_intervals_or_trees_or_empty(intervals)
    if isinstance(intervals, TimeIntervalTree):
        tree = intervals
    else:
        tree = TimeIntervalTree(intervals)
    if not tree:
        return tree

    depth_tree = compute_depth_of_intervals_in_interval(tree, interval)
    #logic_tree = TimeIntervalTree(filter(lambda x: 1 <= x['depth'], depth_tree))
    logic_tree = TimeIntervalTree([x for x in depth_tree if 1 <= x['depth']])

    return logic_tree

#   if not logic_tree:
#      return logic_tree
#   return fuse_tangent_or_overlapping_intervals(logic_tree)
