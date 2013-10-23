# -*- encoding: utf-8 -*-


def timespan_2_starts_after_timespan_1_stops(
    timespan_1=None, 
    timespan_2=None, 
    hold=False,
    ):
    r'''Makes time relation indicating that `timespan_2` starts 
    after `timespan_1` stops.

    ::

        >>> relation = timerelationtools.timespan_2_starts_after_timespan_1_stops()
        >>> print relation.storage_format
        timerelationtools.TimespanTimespanTimeRelation(
            timerelationtools.CompoundInequality([
                timerelationtools.SimpleInequality('timespan_1.stop_offset <= timespan_2.start_offset')
                ],
                logical_operator='and'
                )
            )

    Returns time relation or boolean.
    '''
    from abjad.tools import timerelationtools

    inequality = timerelationtools.CompoundInequality([
        'timespan_1.stop_offset <= timespan_2.start_offset',
        ])

    time_relation = timerelationtools.TimespanTimespanTimeRelation(
        inequality,
        timespan_1=timespan_1,
        timespan_2=timespan_2,
        )

    if time_relation.is_fully_loaded and not hold:
        return time_relation()
    else:
        return time_relation
