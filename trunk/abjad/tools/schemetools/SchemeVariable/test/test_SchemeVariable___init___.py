from abjad import *


def test_SchemeVariable___init____01( ):

   t = Note(0, (1, 4))
   t.override.stem.direction = schemetools.SchemeVariable('DOWN')

   r'''
   \once \override Stem #'direction = #DOWN
   c'4
   '''

   assert t.format == "\\once \\override Stem #'direction = #DOWN\nc'4"
