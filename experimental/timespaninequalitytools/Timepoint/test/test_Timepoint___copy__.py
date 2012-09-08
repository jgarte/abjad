from experimental import timespaninequalitytools
from fractions import Fraction
import copy


def test_Timepoint___copy___01():

    timepoint_1 = timespaninequalitytools.Timepoint(edge=Right, multiplier=Fraction(1, 3))
    timepoint_2 = copy.deepcopy(timepoint_1)

    assert isinstance(timepoint_1, timespaninequalitytools.Timepoint)
    assert isinstance(timepoint_2, timespaninequalitytools.Timepoint)
    assert not timepoint_1 is timepoint_2
    assert timepoint_1 == timepoint_2
