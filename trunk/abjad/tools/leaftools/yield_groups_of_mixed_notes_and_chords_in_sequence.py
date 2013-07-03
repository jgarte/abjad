from abjad.tools import componenttools


def yield_groups_of_mixed_notes_and_chords_in_sequence(sequence):
    r'''.. versionadded:: 2.0

    Yield groups of mixed notes and chords in `sequence`::

        >>> staff = Staff("c'8 d'8 r8 r8 <e' g'>8 <f' a'>8 g'8 a'8 r8 r8 <b' d''>8 <c'' e''>8")

    ::

        >>> f(staff)
        \new Staff {
            c'8
            d'8
            r8
            r8
            <e' g'>8
            <f' a'>8
            g'8
            a'8
            r8
            r8
            <b' d''>8
            <c'' e''>8
        }

    ::

        >>> for group in leaftools.yield_groups_of_mixed_notes_and_chords_in_sequence(staff):
        ...     group
        ...
        (Note("c'8"), Note("d'8"))
        (Chord("<e' g'>8"), Chord("<f' a'>8"), Note("g'8"), Note("a'8"))
        (Chord("<b' d''>8"), Chord("<c'' e''>8"))

    Return generator.
    '''
    from abjad.tools import chordtools
    from abjad.tools import notetools

    return componenttools.yield_groups_of_mixed_classes_in_sequence(sequence, (notetools.Note, chordtools.Chord))
