# -*- encoding: utf-8 -*-
from abjad.tools import durationtools
from abjad.tools import selectiontools


def make_leaves_from_talea(
    talea, 
    talea_denominator,
    decrease_durations_monotonically=True, 
    tie_rests=False,
    forbidden_written_duration=None,
    ):
    r'''Make leaves from `talea`.

    Interpret positive elements in `talea` as notes numerators.

    Interpret negative elements in `talea` as rests numerators.

    Set the pitch of all notes to middle C.

    ..  container:: example
    
        **Example 1.** Make leaves from talea:

        ::

            >>> leaves = leaftools.make_leaves_from_talea([3, -3, 5, -5], 16)
            >>> staff = stafftools.RhythmicStaff(leaves)
            >>> time_signature = contexttools.TimeSignatureMark((4, 4))
            >>> time_signature.attach(staff)
            TimeSignatureMark((4, 4))(RhythmicStaff{6})
            >>> show(staff) # doctest: +SKIP

        ..  doctest::

            >>> f(staff)
            \new RhythmicStaff {
                \time 4/4
                c'8.
                r8.
                c'4 ~
                c'16
                r4
                r16
            }

    ..  container:: example
    
        **Example 2.** Increase durations monotonically:

        ::

            >>> leaves = leaftools.make_leaves_from_talea(
            ...     [3, -3, 5, -5], 16,
            ...     decrease_durations_monotonically=False)
            >>> staff = stafftools.RhythmicStaff(leaves)
            >>> time_signature = contexttools.TimeSignatureMark((4, 4))
            >>> time_signature.attach(staff)
            TimeSignatureMark((4, 4))(RhythmicStaff{6})
            >>> show(staff) # doctest: +SKIP

        ..  doctest::

            >>> f(staff)
            \new RhythmicStaff {
                \time 4/4
                c'8.
                r8.
                c'16 ~
                c'4
                r16
                r4
            }

    ..  container:: example
    
        **Example 3.** Forbid written durations greater than or equal 
        to a half note:

        ::

            >>> leaves = leaftools.make_leaves_from_talea(
            ...     [3, -3, 5, -5], 16,
            ...     forbidden_written_duration=Duration(1, 4))
            >>> staff = stafftools.RhythmicStaff(leaves)
            >>> time_signature = contexttools.TimeSignatureMark((4, 4))
            >>> time_signature.attach(staff)
            TimeSignatureMark((4, 4))(RhythmicStaff{8})
            >>> show(staff) # doctest: +SKIP

        ..  doctest::

            >>> f(staff)
            \new RhythmicStaff {
                \time 4/4
                c'8.
                r8.
                c'8 ~
                c'8 ~
                c'16
                r8
                r8
                r16
            }

    Returns list of leaves.
    '''
    from abjad.tools import leaftools

    assert all(x != 0 for x in talea), repr(talea)

    result = []
    for note_value in talea:
        if 0 < note_value:
            pitches = [0]
        else:
            pitches = [None]
        leaves = leaftools.make_leaves(
            pitches, 
            [durationtools.Duration(abs(note_value), talea_denominator)],
            decrease_durations_monotonically=decrease_durations_monotonically,
            tie_rests=tie_rests, 
            forbidden_written_duration=forbidden_written_duration,
            )
        result.extend(leaves)

    result = selectiontools.Selection(result)
    return result
