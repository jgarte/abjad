from abjad.tools.marktools.get_lilypond_command_marks_attached_to_component import get_lilypond_command_marks_attached_to_component


def is_component_with_lilypond_command_mark_attached(expr, command_name_string = None):
   '''True when `expr` is component with LilyPond command mark attached::

      abjad> note = Note(0, (1, 4))
      abjad> marktools.LilyPondCommandMark('stemUp')(note)
      LilyPondCommandMark('stemUp')(c'4)

   ::

      abjad> marktools.is_component_with_lilypond_command_mark_attached(note)
      True

   False otherwise::

      abjad> note = Note(0, (1, 4))
   
   ::

      abjad> marktools.is_component_with_lilypond_command_mark_attached(note)
      False

   Return boolean.
   '''
   from abjad.tools.componenttools._Component import _Component

   if isinstance(expr, _Component):
      for mark in get_lilypond_command_marks_attached_to_component(expr):
         if mark.command_name_string == command_name_string or command_name_string is None:
            return True
      
   return False
