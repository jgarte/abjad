def expr_starts_when_timespan_stops():
    r'''.. versionadded:: 1.0

    Make timespan inequality indicating that expression happens during timespan::

        >>> from experimental import timespantools

    ::

        >>> timespantools.expr_starts_when_timespan_stops()
        TimespanInequalityTemplate('expr.start == t.stop')

    Return timespan inequality.
    '''
    from experimental import timespantools

    return timespantools.TimespanInequalityTemplate('expr.start == t.stop')
