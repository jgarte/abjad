# -*- encoding: utf-8 -*-
from abjad import *


def test_timerelationtools_Timespan___and___01():
    timespan_1 = timerelationtools.Timespan(0, 15)
    timespan_2 = timerelationtools.Timespan(-10, -5)
    result = timespan_1 & timespan_2
    assert result == timerelationtools.TimespanInventory([])

def test_timerelationtools_Timespan___and___02():
    timespan_1 = timerelationtools.Timespan(0, 15)
    timespan_2 = timerelationtools.Timespan(-10, 0)
    result = timespan_1 & timespan_2
    assert result == timerelationtools.TimespanInventory([])

def test_timerelationtools_Timespan___and___03():
    timespan_1 = timerelationtools.Timespan(0, 15)
    timespan_2 = timerelationtools.Timespan(-10, 5)
    result = timespan_1 & timespan_2
    assert result == timerelationtools.TimespanInventory([
        timerelationtools.Timespan(0, 5)
    ])

def test_timerelationtools_Timespan___and___04():
    timespan_1 = timerelationtools.Timespan(0, 15)
    timespan_2 = timerelationtools.Timespan(-10, 15)
    result = timespan_1 & timespan_2
    assert result == timerelationtools.TimespanInventory([
        timerelationtools.Timespan(0, 15)
    ])

def test_timerelationtools_Timespan___and___05():
    timespan_1 = timerelationtools.Timespan(0, 15)
    timespan_2 = timerelationtools.Timespan(-10, 25)
    result = timespan_1 & timespan_2
    assert result == timerelationtools.TimespanInventory([
        timerelationtools.Timespan(0, 15)
    ])

def test_timerelationtools_Timespan___and___06():
    timespan_1 = timerelationtools.Timespan(0, 15)
    timespan_2 = timerelationtools.Timespan(0, 10)
    result = timespan_1 & timespan_2
    assert result == timerelationtools.TimespanInventory([
        timerelationtools.Timespan(0, 10)
    ])

def test_timerelationtools_Timespan___and___07():
    timespan_1 = timerelationtools.Timespan(0, 15)
    timespan_2 = timerelationtools.Timespan(0, 15)
    result = timespan_1 & timespan_2
    assert result == timerelationtools.TimespanInventory([
        timerelationtools.Timespan(0, 15)
    ])

def test_timerelationtools_Timespan___and___08():
    timespan_1 = timerelationtools.Timespan(0, 15)
    timespan_2 = timerelationtools.Timespan(5, 10)
    result = timespan_1 & timespan_2
    assert result == timerelationtools.TimespanInventory([
        timerelationtools.Timespan(5, 10)
    ])

def test_timerelationtools_Timespan___and___09():
    timespan_1 = timerelationtools.Timespan(0, 15)
    timespan_2 = timerelationtools.Timespan(5, 15)
    result = timespan_1 & timespan_2
    assert result == timerelationtools.TimespanInventory([
        timerelationtools.Timespan(5, 15)
    ])

def test_timerelationtools_Timespan___and___10():
    timespan_1 = timerelationtools.Timespan(0, 15)
    timespan_2 = timerelationtools.Timespan(0, 25)
    result = timespan_1 & timespan_2
    assert result == timerelationtools.TimespanInventory([
        timerelationtools.Timespan(0, 15)
    ])

def test_timerelationtools_Timespan___and___11():
    timespan_1 = timerelationtools.Timespan(0, 15)
    timespan_2 = timerelationtools.Timespan(5, 25)
    result = timespan_1 & timespan_2
    assert result == timerelationtools.TimespanInventory([
        timerelationtools.Timespan(5, 15)
    ])

def test_timerelationtools_Timespan___and___12():
    timespan_1 = timerelationtools.Timespan(0, 15)
    timespan_2 = timerelationtools.Timespan(15, 25)
    result = timespan_1 & timespan_2
    assert result == timerelationtools.TimespanInventory([])

def test_timerelationtools_Timespan___and___13():
    timespan_1 = timerelationtools.Timespan(0, 15)
    timespan_2 = timerelationtools.Timespan(20, 25)
    result = timespan_1 & timespan_2
    assert result == timerelationtools.TimespanInventory([])
