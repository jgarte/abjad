# -*- coding: utf-8 -*-


def select(indices=None, inverted=None):
    r'''Makes pattern that matches `indices`.

    ..  container:: example

        Selects index 2:

        ::

            >>> pattern = patterntools.select([2])

        ::

            >>> print(format(pattern))
            abjad.Pattern(
                indices=[2],
                )

    ..  container:: example

        Selects indices 2, 3 and 5:

        ::

            >>> pattern = patterntools.select([2, 3, 5])

        ::

            >>> print(format(pattern))
            abjad.Pattern(
                indices=[2, 3, 5],
                )

    Returns pattern.
    '''
    from abjad.tools import patterntools
    indices = indices or []
    return patterntools.Pattern(
        indices=indices,
        inverted=inverted,
        )
