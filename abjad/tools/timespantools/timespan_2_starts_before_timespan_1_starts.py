# -*- coding: utf-8 -*-


def timespan_2_starts_before_timespan_1_starts(
    timespan_1=None,
    timespan_2=None,
    hold=False,
    ):
    r'''Makes time relation indicating that `timespan_2` starts
    before `timespan_1` starts.

    ::

        >>> relation = timespantools.timespan_2_starts_before_timespan_1_starts()
        >>> f(relation)
        abjad.TimespanTimespanTimeRelation(
            inequality=abjad.CompoundInequality(
                [
                    abjad.Inequality('timespan_2.start_offset < timespan_1.start_offset'),
                    ],
                logical_operator='and',
                ),
            )

    Returns time relation or boolean.
    '''
    from abjad.tools import timespantools

    inequality = timespantools.CompoundInequality([
        'timespan_2.start_offset < timespan_1.start_offset',
        ])

    time_relation = timespantools.TimespanTimespanTimeRelation(
        inequality,
        timespan_1=timespan_1,
        timespan_2=timespan_2,
        )

    if time_relation.is_fully_loaded and not hold:
        return time_relation()
    else:
        return time_relation
