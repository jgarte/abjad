# -*- coding: utf-8 -*-


def select_first(n=1, inverted=None):
    r'''Makes pattern that matches the first `n` indices.

    ..  container:: example

        Selects first division for tie creation:

        ::

            >>> pattern = abjad.select_first()

        ::

            >>> print(format(pattern))
            abjad.Pattern(
                indices=[0],
                )

        ::

            >>> maker = rhythmmakertools.NoteRhythmMaker(
            ...     tie_specifier=rhythmmakertools.TieSpecifier(
            ...         tie_across_divisions=pattern,
            ...         use_messiaen_style_ties=True,
            ...         ),
            ...     )
            >>> divisions = [(7, 16), (3, 8), (7, 16), (3, 8)]
            >>> music = maker(divisions)
            >>> lilypond_file = rhythmmakertools.make_lilypond_file(
            ...     music,
            ...     divisions,
            ...     )
            >>> show(lilypond_file) # doctest: +SKIP

        ..  doctest::

            >>> f(lilypond_file[Staff])
            \new RhythmicStaff {
                {
                    \time 7/16
                    c'4..
                }
                {
                    \time 3/8
                    c'4. \repeatTie
                }
                {
                    \time 7/16
                    c'4..
                }
                {
                    \time 3/8
                    c'4.
                }
            }
            
    ..  container:: example

        Selects first two divisions for tie creation:

        ::

            >>> pattern = abjad.select_first(n=2)

        ::

            >>> print(format(pattern))
            abjad.Pattern(
                indices=[0, 1],
                )

        ::

            >>> maker = rhythmmakertools.NoteRhythmMaker(
            ...     tie_specifier=rhythmmakertools.TieSpecifier(
            ...         tie_across_divisions=pattern,
            ...         use_messiaen_style_ties=True,
            ...         ),
            ...     )
            >>> divisions = [(7, 16), (3, 8), (7, 16), (3, 8)]
            >>> music = maker(divisions)
            >>> lilypond_file = rhythmmakertools.make_lilypond_file(
            ...     music,
            ...     divisions,
            ...     )
            >>> show(lilypond_file) # doctest: +SKIP

        ..  doctest::

            >>> f(lilypond_file[Staff])
            \new RhythmicStaff {
                {
                    \time 7/16
                    c'4..
                }
                {
                    \time 3/8
                    c'4. \repeatTie
                }
                {
                    \time 7/16
                    c'4.. \repeatTie
                }
                {
                    \time 3/8
                    c'4.
                }
            }

    ..  container:: example

        Selects no divisions for tie creation:

        ::

            >>> pattern = abjad.select_first(n=0)

        ::

            >>> print(format(pattern))
            abjad.Pattern(
                indices=[],
                )

        ::

            >>> maker = rhythmmakertools.NoteRhythmMaker(
            ...     tie_specifier=rhythmmakertools.TieSpecifier(
            ...         tie_across_divisions=pattern,
            ...         use_messiaen_style_ties=True,
            ...         ),
            ...     )
            >>> divisions = [(7, 16), (3, 8), (7, 16), (3, 8)]
            >>> music = maker(divisions)
            >>> lilypond_file = rhythmmakertools.make_lilypond_file(
            ...     music,
            ...     divisions,
            ...     )
            >>> show(lilypond_file) # doctest: +SKIP

        ..  doctest::

            >>> f(lilypond_file[Staff])
            \new RhythmicStaff {
                {
                    \time 7/16
                    c'4..
                }
                {
                    \time 3/8
                    c'4.
                }
                {
                    \time 7/16
                    c'4..
                }
                {
                    \time 3/8
                    c'4.
                }
            }

    Returns pattern.
    '''
    from abjad.tools import patterntools
    indices = list(range(n))
    return patterntools.Pattern(
        indices=indices,
        inverted=inverted,
        )
