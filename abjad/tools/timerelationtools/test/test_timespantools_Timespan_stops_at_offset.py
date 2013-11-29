# -*- encoding: utf-8 -*-
from abjad import *


def test_timerelationtools_Timespan_stops_at_offset_01():
    timespan = timerelationtools.Timespan(0, 10)
    offset = durationtools.Offset(-5)
    assert not timespan.stops_at_offset(offset)

def test_timerelationtools_Timespan_stops_at_offset_02():
    timespan = timerelationtools.Timespan(0, 10)
    offset = durationtools.Offset(0)
    assert not timespan.stops_at_offset(offset)

def test_timerelationtools_Timespan_stops_at_offset_03():
    timespan = timerelationtools.Timespan(0, 10)
    offset = durationtools.Offset(5)
    assert not timespan.stops_at_offset(offset)

def test_timerelationtools_Timespan_stops_at_offset_04():
    timespan = timerelationtools.Timespan(0, 10)
    offset = durationtools.Offset(10)
    assert timespan.stops_at_offset(offset)

def test_timerelationtools_Timespan_stops_at_offset_05():
    timespan = timerelationtools.Timespan(0, 10)
    offset = durationtools.Offset(15)
    assert not timespan.stops_at_offset(offset)
