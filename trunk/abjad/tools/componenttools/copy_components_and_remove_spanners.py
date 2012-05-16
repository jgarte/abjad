from abjad.tools.componenttools._ignore_parentage_of_components import _ignore_parentage_of_components
from abjad.tools.componenttools._restore_parentage_to_components_by_receipt import _restore_parentage_to_components_by_receipt
from abjad.tools.marktools._reattach_blinded_marks_to_components_in_expr import _reattach_blinded_marks_to_components_in_expr
import copy


def copy_components_and_remove_spanners(components, n=1):
    r'''.. versionadded:: 1.1

    Clone `components` and remove all spanners.

    The `components` must be thread-contiguous.

    The steps taken by this function are as follows.
    Withdraw all components at any level in `components` from spanners.
    Deep copy unspanned components in `components`.
    Reapply spanners to all components at any level in `components`. ::

        abjad> voice = Voice(Measure((2, 8), notetools.make_repeated_notes(2)) * 3)
        abjad> pitchtools.set_ascending_named_diatonic_pitches_on_nontied_pitched_components_in_expr(voice)
        abjad> beam = spannertools.BeamSpanner(voice.leaves[:4])
        abjad> f(voice)
        \new Voice {
            {
                \time 2/8
                c'8 [
                d'8
            }
            {
                e'8
                f'8 ]
            }
            {
                g'8
                a'8
            }
        }

    ::

        abjad> result = componenttools.copy_components_and_remove_spanners(voice.leaves[2:4])
        abjad> result
        (Note("e'8"), Note("f'8"))

    ::

        abjad> new_voice = Voice(result)
        abjad> f(new_voice)
        \new Voice {
            e'8
            f'8
        }

    ::

        abjad> voice.leaves[2] is new_voice.leaves[0]
        False

    Clone `components` a total of `n` times. ::

        abjad> result = componenttools.copy_components_and_remove_spanners(voice.leaves[2:4], n = 3)
        abjad> result
        (Note("e'8"), Note("f'8"), Note("e'8"), Note("f'8"), Note("e'8"), Note("f'8"))

    ::

        abjad> new_voice = Voice(result)
        abjad> f(new_voice)
        \new Voice {
            e'8
            f'8
            e'8
            f'8
            e'8
            f'8
        }


    .. versionchanged:: 2.0
        renamed ``clone.unspan()`` to
        ``componenttools.copy_components_and_remove_spanners()``.

    .. versionchanged:: 2.0
        renamed ``componenttools.clone_components_and_remove_all_spanners()`` to
        ``componenttools.copy_components_and_remove_spanners()``.

    .. versionchanged:: 2.9
        renamed ``componenttools.copy_components_and_remove_all_spanners()`` to
        ``componenttools.copy_components_and_remove_spanners()``.
    '''
    from abjad.tools import componenttools

    if n < 1:
        return []

    assert componenttools.all_are_thread_contiguous_components(components)

    result = copy.deepcopy(components)

    for i in range(n - 1):
        result += copy_components_and_remove_spanners(components)

    return result
