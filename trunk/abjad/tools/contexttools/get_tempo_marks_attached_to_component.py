from abjad.tools.contexttools.TempoMark import TempoMark
from abjad.tools.contexttools.get_context_marks_attached_to_component import get_context_marks_attached_to_component


def get_tempo_marks_attached_to_component(component):
    r'''.. versionadded:: 2.3

    Get tempo marks attached to `component`::

        abjad> score = Score([])
        abjad> staff = Staff("c'8 d'8 e'8 f'8")
        abjad> score.append(staff)

    ::

        abjad> contexttools.TempoMark(Duration(1, 8), 52)(staff)
        TempoMark(Duration(1, 8), 52)(Staff{4})

    ::

        abjad> f(score)
        \new Score <<
            \new Staff {
                \tempo 8=52
                c'8
                d'8
                e'8
                f'8
            }
        >>

    ::

        abjad> contexttools.get_tempo_marks_attached_to_component(staff)
        (TempoMark(Duration(1, 8), 52)(Staff{4}),)

    Return tuple of zero or more tempo marks.
    '''

    return get_context_marks_attached_to_component(component, klasses=(TempoMark,))
