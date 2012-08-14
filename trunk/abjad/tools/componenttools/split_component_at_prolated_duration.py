from abjad.tools import durationtools
from abjad.tools import mathtools


def split_component_at_prolated_duration(component, duration, fracture_spanners=False, tie_after=False):
    r'''.. versionadded:: 1.1
        
    Split `component` at prolated `duration`.

    General component duration split algorithm.
    Works on leaves, tuplets, measures, contexts and unqualified containers.
    Keywords control spanner behavior at split-time.

    Split `component` at `prolated_duration` and do not fracture crossing spanners::

        >>> staff = Staff(Measure((2, 8), notetools.make_repeated_notes(2)) * 2)
        >>> pitchtools.set_ascending_named_diatonic_pitches_on_nontied_pitched_components_in_expr(staff)

    ::

        >>> beamtools.BeamSpanner(staff[0])
        BeamSpanner(|2/8(2)|)
        >>> beamtools.BeamSpanner(staff[1])
        BeamSpanner(|2/8(2)|)
        >>> spannertools.SlurSpanner(staff.leaves)
        SlurSpanner(c'8, d'8, e'8, f'8)

    ::

        >>> f(staff)
        \new Staff {
            {
                \time 2/8
                c'8 [ (
                d'8 ]
            }
            {
                e'8 [
                f'8 ] )
            }
        }

    ::

        >>> halves = componenttools.split_component_at_prolated_duration(
        ... staff.leaves[0], Duration(1, 32), fracture_spanners=False)

    ::

        >>> f(staff)
        \new Staff {
            {
                \time 2/8
                c'32 [ (
                c'16.
                d'8 ]
            }
            {
                e'8 [
                f'8 ] )
            }
        }

    Example 2. Split component at prolated duration at fracture crossing spanners::

        >>> staff = Staff(Measure((2, 8), notetools.make_repeated_notes(2)) * 2)
        >>> pitchtools.set_ascending_named_diatonic_pitches_on_nontied_pitched_components_in_expr(staff)

    ::

        >>> beamtools.BeamSpanner(staff[0])
        BeamSpanner(|2/8(2)|)
        >>> beamtools.BeamSpanner(staff[1])
        BeamSpanner(|2/8(2)|)
        >>> spannertools.SlurSpanner(staff.leaves)
        SlurSpanner(c'8, d'8, e'8, f'8)

    ::

        >>> f(staff)
        \new Staff {
            {
                \time 2/8
                c'8 [ (
                d'8 ]
            }
            {
                e'8 [
                f'8 ] )
            }
        }

    ::

        >>> halves = componenttools.split_component_at_prolated_duration(
        ... staff.leaves[0], Duration(1, 32), fracture_spanners=True)

    ::

        >>> f(staff)
        \new Staff {
            {
                \time 2/8
                c'32 ( ) [
                c'16. (
                d'8 ]
            }
            {
                e'8 [
                f'8 ] )
            }
        }

    Return pair of left and right part-lists.
    '''
    from abjad.tools import componenttools
    from abjad.tools import containertools
    from abjad.tools import leaftools
    from abjad.tools import measuretools
    from abjad.tools import spannertools
    from abjad.tools import tietools
    from abjad.tools.leaftools.split_leaf_at_prolated_duration import split_leaf_at_prolated_duration

    duration = durationtools.Duration(duration)
    assert 0 <= duration

    # if zero duration then return component
    if duration == 0:
        # TODO: this one case should be ([], component)
        return (component, )

    # get global position of duration split in score
    global_split_point = component.start_offset + duration

    # get duration crossers, if any
    contents = componenttools.get_improper_descendents_of_component_that_cross_offset(
        component, duration)

    #print component, global_split_point, contents

    # get duration crossing measures, if any
    measures = [x for x in contents if isinstance(x, measuretools.Measure)]

    # if we must split a binary measure at a nonbinary split point
    # go ahead and transform the binary measure to nonbinary equiavlent now;
    # code that crawls and splits later on will be happier
    if len(measures) == 1:
        measure = measures[0]
        split_point_in_measure = global_split_point - measure.start_offset
        split_point_denominator = split_point_in_measure.denominator
        if measure.is_nonbinary:
            measure_multiplier = measure.multiplier
            split_point_multiplier = durationtools.positive_integer_to_implied_prolation_multipler(
                split_point_denominator)
            if not measure_multiplier == split_point_multiplier:
                raise NotImplementedError
        elif not mathtools.is_nonnegative_integer_power_of_two(split_point_denominator):
            nonbinary_factors = mathtools.factors(
                mathtools.remove_powers_of_two(split_point_denominator))
            nonbinary_product = 1
            for nonbinary_factor in nonbinary_factors:
                nonbinary_product *= nonbinary_factor
            measuretools.scale_measure_denominator_and_adjust_measure_contents(
                measure, nonbinary_product)
            # rederive duration crosses with possibly new measure contents
            contents = componenttools.get_improper_descendents_of_component_that_cross_offset(
                component, duration)
    elif 1 < len(measures):
        raise ContainmentError('measures can not nest.')

    # if leaf duration crosser, will be at end of list
    bottom = contents[-1]

    did_split_leaf = False

    # if split point necessitates leaf split
    if isinstance(bottom, leaftools.Leaf):
        assert isinstance(bottom, leaftools.Leaf)
        did_split_leaf = True
        split_point_in_bottom = global_split_point - bottom.start_offset
        left_list, right_list = split_leaf_at_prolated_duration(bottom,
            split_point_in_bottom, fracture_spanners=fracture_spanners, tie_after=tie_after)
        right = right_list[0]
        leaf_right_of_split = right
        leaf_left_of_split = left_list[-1]
        duration_crossing_containers = contents[:-1]
        if not len(duration_crossing_containers):
            return left_list, right_list
    # if split point falls between leaves
    # then find leaf to immediate right of split point
    # in order to start upward crawl through duration-crossing containers
    else:
        duration_crossing_containers = contents[:]
        for leaf in leaftools.iterate_leaves_forward_in_expr(bottom):
            if leaf.start_offset == global_split_point:
                leaf_right_of_split = leaf
                leaf_left_of_split = leaftools.get_nth_leaf_in_thread_from_leaf(leaf_right_of_split, -1)
                break
        else:
            raise ContainmentError('can not split empty container {!r}.'.format(bottom))

    # find component to right of split that is also immediate child of last duration-crossing container
    for component in componenttools.get_improper_parentage_of_component(leaf_right_of_split):
        if component.parent is duration_crossing_containers[-1]:
            highest_level_component_right_of_split = component
            break
    else:
        raise ValueError('should we be able to get here?')

    # fracture leaf spanners if requested
    if fracture_spanners:
        spannertools.fracture_spanners_attached_to_component(leaf_right_of_split, direction='left')

    # crawl back up through duration-crossing containers and split each
    #prev = leaf_right_of_split
    prev = highest_level_component_right_of_split
    for duration_crossing_container in reversed(duration_crossing_containers):
        assert isinstance(duration_crossing_container, containertools.Container)
        i = duration_crossing_container.index(prev)
        left, right = containertools.split_container_at_index(
            duration_crossing_container, i, fracture_spanners=fracture_spanners)
        prev = right

    # NOTE: If tie chain here is convenience, then fusing is good.
    #       If tie chain here is user-given, then fusing is less good.
    #       Maybe later model difference between user tie chains and not.
    leaftools.fuse_leaves_in_tie_chain_by_immediate_parent_big_endian(
        tietools.get_tie_chain(leaf_left_of_split))
    leaftools.fuse_leaves_in_tie_chain_by_immediate_parent_big_endian(
        tietools.get_tie_chain(leaf_right_of_split))

    # crawl above will kill any tie applied to leaves;
    # reapply tie here if necessary
    # TODO: Possibly replace this with tietools.apply_tie_spanner_to_leaf_pair()?
    if did_split_leaf:
        if tie_after:
            leaves_at_split = [leaf_left_of_split, leaf_right_of_split]
            if not tietools.are_components_in_same_tie_spanner(leaves_at_split):
                if all([tietools.is_component_with_tie_spanner_attached(x) for x in leaves_at_split]):
                    leaf_left_of_split_tie_spanner = \
                        spannertools.get_the_only_spanner_attached_to_component(
                        leaf_left_of_split, tietools.TieSpanner)
                    leaf_right_of_split_tie_spanner = \
                        spannertools.get_the_only_spanner_attached_to_component(
                        leaf_right_of_split, tietools.TieSpanner)
                    leaf_left_of_split_tie_spanner.fuse(leaf_right_of_split_tie_spanner)
                else:
                    tietools.TieSpanner(leaves_at_split)

    # return pair of left and right list-wrapped halves of container
    return ([left], [right])
