from abjad import *
import copy


def test_IntervalClass___copy___01( ):

   ic1 = pitchtools.IntervalClass(1)
   new = copy.copy(ic1)

   assert ic1 == new
   assert not ic1 is new
