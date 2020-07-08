import math
import typing

import quicktions

from .. import mathtools, typings
from ..duration import Duration, Multiplier, NonreducedFraction
from ..overrides import TweakInterface, override, tweak
from ..storage import FormatSpecification
from ..tags import Tag
from .Container import Container
from .Leaf import Leaf
from .Rest import Rest


class Tuplet(Container):
    r"""
    Tuplet.

    ..  container:: example

        A tuplet:

        >>> tuplet = abjad.Tuplet("3:2", "c'8 d'8 e'8")
        >>> abjad.show(tuplet) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(tuplet)
            \times 2/3 {
                c'8
                d'8
                e'8
            }

    ..  container:: example

        A nested tuplet:

        >>> second_tuplet = abjad.Tuplet("7:4", "g'4. ( a'16 )")
        >>> tuplet.insert(1, second_tuplet)
        >>> abjad.show(tuplet) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(tuplet)
            \tweak edge-height #'(0.7 . 0)
            \times 2/3 {
                c'8
                \times 4/7 {
                    g'4.
                    (
                    a'16
                    )
                }
                d'8
                e'8
            }


    ..  container:: example

        A doubly nested tuplet:

            >>> third_tuplet = abjad.Tuplet("5:4", [])
            >>> third_tuplet.extend("e''32 [ ef''32 d''32 cs''32 cqs''32 ]")
            >>> second_tuplet.insert(1, third_tuplet)
            >>> abjad.show(tuplet) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(tuplet)
            \tweak edge-height #'(0.7 . 0)
            \times 2/3 {
                c'8
                \tweak edge-height #'(0.7 . 0)
                \times 4/7 {
                    g'4.
                    (
                    \times 4/5 {
                        e''32
                        [
                        ef''32
                        d''32
                        cs''32
                        cqs''32
                        ]
                    }
                    a'16
                    )
                }
                d'8
                e'8
            }

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = "Containers"

    __slots__ = (
        "_denominator",
        "_force_fraction",
        "_hide",
        "_multiplier",
        "_tweaks",
    )

    ### INITIALIZER ###

    def __init__(
        self,
        multiplier=(2, 3),
        components=None,
        *,
        denominator: int = None,
        force_fraction: bool = None,
        hide: bool = None,
        tag: Tag = None,
        tweaks: TweakInterface = None,
    ) -> None:
        Container.__init__(self, components, tag=tag)
        if isinstance(multiplier, str) and ":" in multiplier:
            strings = multiplier.split(":")
            numbers = [int(_) for _ in strings]
            multiplier = Multiplier(numbers[1], numbers[0])
        else:
            multiplier = Multiplier(multiplier)
        self.multiplier = multiplier
        self.denominator = denominator
        self.force_fraction = force_fraction
        self.hide = hide
        if tweaks is not None:
            assert isinstance(tweaks, TweakInterface), repr(tweaks)
        self._tweaks = TweakInterface.set_tweaks(self, tweaks)

    ### SPECIAL METHODS ###

    def __getnewargs__(self) -> tuple:
        """
        Gets new arguments of tuplet.
        """
        return (self.multiplier,)

    ### PRIVATE METHODS ###

    def _format_after_slot(self, bundle):
        result = []
        result.append(("grob reverts", bundle.grob_reverts))
        result.append(("commands", bundle.after.commands))
        result.append(("comments", bundle.after.comments))
        return tuple(result)

    def _format_before_slot(self, bundle):
        result = []
        result.append(("comments", bundle.before.comments))
        result.append(("commands", bundle.before.commands))
        result.append(("grob overrides", bundle.grob_overrides))
        result.append(("context settings", bundle.context_settings))
        return tuple(result)

    def _format_close_brackets_slot(self, bundle):
        result = []
        if self.multiplier:
            strings = ["}"]
            if self.tag is not None:
                strings = Tag.tag(strings, tag=self.tag)
            result.append([("self_brackets", "close"), strings])
        return tuple(result)

    def _format_closing_slot(self, bundle):
        result = []
        result.append(("commands", bundle.closing.commands))
        result.append(("comments", bundle.closing.comments))
        return self._format_slot_contributions_with_indent(result)

    def _format_lilypond_fraction_command_string(self):
        if self.hide:
            return ""
        if "text" in vars(override(self).tuplet_number):
            return ""
        if (
            self.augmentation()
            or not self._get_power_of_two_denominator()
            or self.multiplier.denominator == 1
            or self.force_fraction
        ):
            return r"\tweak text #tuplet-number::calc-fraction-text"
        return ""

    def _format_open_brackets_slot(self, bundle):
        result = []
        if self.multiplier:
            if self.hide:
                contributor = (self, "hide")
                scale_durations_command_string = (
                    self._get_scale_durations_command_string()
                )
                contributions = [scale_durations_command_string]
            else:
                contributor = ("self_brackets", "open")
                contributions = []
                fraction_command_string = (
                    self._format_lilypond_fraction_command_string()
                )
                if fraction_command_string:
                    contributions.append(fraction_command_string)
                edge_height_tweak_string = self._get_edge_height_tweak_string()
                if edge_height_tweak_string:
                    contributions.append(edge_height_tweak_string)
                strings = tweak(self)._list_format_contributions(directed=False)
                contributions.extend(strings)
                times_command_string = self._get_times_command_string()
                contributions.append(times_command_string)
            if self.tag is not None:
                contributions = Tag.tag(contributions, tag=self.tag)
            result.append([contributor, contributions])
        return tuple(result)

    def _format_opening_slot(self, bundle):
        result = []
        result.append(("comments", bundle.opening.comments))
        result.append(("commands", bundle.opening.commands))
        return self._format_slot_contributions_with_indent(result)

    def _get_compact_representation(self):
        if not self:
            return f"{{ {self.multiplier!s} }}"
        return f"{{ {self.multiplier!s} {self._get_contents_summary()} }}"

    def _get_edge_height_tweak_string(self):
        duration = self._get_preprolated_duration()
        denominator = duration.denominator
        if not mathtools.is_nonnegative_integer_power_of_two(denominator):
            return r"\tweak edge-height #'(0.7 . 0)"

    def _get_format_specification(self):
        return FormatSpecification(
            client=self,
            repr_args_values=[self.multiplier, self._get_contents_summary()],
            storage_format_args_values=[self.multiplier, self[:]],
            storage_format_kwargs_names=[],
        )

    def _get_lilypond_format(self):
        self._update_now(indicators=True)
        return self._format_component()

    def _get_multiplier_fraction_string(self):
        if self.denominator is not None:
            inverse_multiplier = Multiplier(
                self.multiplier.denominator, self.multiplier.numerator
            )
            nonreduced_fraction = NonreducedFraction(inverse_multiplier)
            nonreduced_fraction = nonreduced_fraction.with_denominator(self.denominator)
            denominator, numerator = nonreduced_fraction.pair
        else:
            numerator = self.multiplier.numerator
            denominator = self.multiplier.denominator
        return f"{numerator}/{denominator}"

    def _get_power_of_two_denominator(self):
        if self.multiplier:
            numerator = self.multiplier.numerator
            return mathtools.is_nonnegative_integer_power_of_two(numerator)
        else:
            return True

    def _get_preprolated_duration(self):
        return self.multiplied_duration

    def _get_ratio_string(self):
        multiplier = self.multiplier
        if multiplier is not None:
            numerator = multiplier.numerator
            denominator = multiplier.denominator
            ratio_string = f"{denominator}:{numerator}"
            return ratio_string
        else:
            return None

    def _get_scale_durations_command_string(self):
        multiplier = self.multiplier
        numerator = multiplier.numerator
        denominator = multiplier.denominator
        string = rf"\scaleDurations #'({numerator} . {denominator}) {{"
        return string

    def _get_summary(self):
        if 0 < len(self):
            return ", ".join([str(x) for x in self.components])
        else:
            return ""

    def _get_times_command_string(self):
        string = rf"\times {self._get_multiplier_fraction_string()} {{"
        return string

    def _scale(self, multiplier):
        multiplier = Multiplier(multiplier)
        for component in self[:]:
            if isinstance(component, Leaf):
                component._scale(multiplier)
        self.normalize_multiplier()

    ### PUBLIC PROPERTIES ###

    @property
    def denominator(self) -> typing.Optional[int]:
        r"""
        Gets and sets preferred denominator of tuplet.

        ..  container:: example

            Gets preferred denominator of tuplet:

            >>> tuplet = abjad.Tuplet("3:2", "c'8 d'8 e'8")
            >>> tuplet.denominator is None
            True
            >>> abjad.show(tuplet) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(tuplet)
                \times 2/3 {
                    c'8
                    d'8
                    e'8
                }

        ..  container:: example

            Sets preferred denominator of tuplet:

            >>> tuplet = abjad.Tuplet("3:2", "c'8 d'8 e'8")
            >>> abjad.show(tuplet) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(tuplet)
                \times 2/3 {
                    c'8
                    d'8
                    e'8
                }

            >>> tuplet.denominator = 4
            >>> abjad.show(tuplet) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(tuplet)
                \times 4/6 {
                    c'8
                    d'8
                    e'8
                }

        """
        return self._denominator

    @denominator.setter
    def denominator(self, argument):
        if isinstance(argument, int):
            if not 0 < argument:
                raise ValueError(argument)
        elif not isinstance(argument, type(None)):
            raise TypeError(argument)
        self._denominator = argument

    @property
    def force_fraction(self) -> typing.Optional[bool]:
        r"""
        Gets and sets force fraction flag.

        ..  container:: example

            The ``default.ily`` stylesheet included in all Abjad API examples
            includes the following:

            ``\override TupletNumber.text = #tuplet-number::calc-fraction-text``

            This means that even simple tuplets format as explicit fractions:

            >>> staff = abjad.Staff()
            >>> staff.append(abjad.Tuplet((2, 3), "c'4 d' e'"))
            >>> staff.append(abjad.Tuplet((2, 3), "c'4 d' e'"))
            >>> staff.append(abjad.Tuplet((2, 3), "c'4 d' e'"))
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    \times 2/3 {
                        c'4
                        d'4
                        e'4
                    }
                    \times 2/3 {
                        c'4
                        d'4
                        e'4
                    }
                    \times 2/3 {
                        c'4
                        d'4
                        e'4
                    }
                }

            To illustrate the effect of Abjad's force fraction property, we can
            temporarily restore LilyPond's default tuplet number formatting
            like this:

            >>> staff = abjad.Staff()
            >>> staff.append(abjad.Tuplet((2, 3), "c'4 d' e'"))
            >>> staff.append(abjad.Tuplet((2, 3), "c'4 d' e'"))
            >>> staff.append(abjad.Tuplet((2, 3), "c'4 d' e'"))
            >>> string = 'tuplet-number::calc-denominator-text'
            >>> abjad.override(staff).tuplet_number.text = string
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                \with
                {
                    \override TupletNumber.text = #tuplet-number::calc-denominator-text
                }
                {
                    \times 2/3 {
                        c'4
                        d'4
                        e'4
                    }
                    \times 2/3 {
                        c'4
                        d'4
                        e'4
                    }
                    \times 2/3 {
                        c'4
                        d'4
                        e'4
                    }
                }

            Which makes it possible to see the effect of setting force fraction
            to true on a single tuplet:

            >>> tuplet = staff[1]
            >>> tuplet.force_fraction = True
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                \with
                {
                    \override TupletNumber.text = #tuplet-number::calc-denominator-text
                }
                {
                    \times 2/3 {
                        c'4
                        d'4
                        e'4
                    }
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 2/3 {
                        c'4
                        d'4
                        e'4
                    }
                    \times 2/3 {
                        c'4
                        d'4
                        e'4
                    }
                }

        ..  container:: example

            Ignored when tuplet number text is overridden explicitly:

            >>> tuplet = abjad.Tuplet((2, 3), "c'8 d'8 e'8")
            >>> duration = abjad.inspect(tuplet).duration()
            >>> from abjad.illustrate import duration_to_score_markup
            >>> markup = duration_to_score_markup(duration)
            >>> abjad.override(tuplet).tuplet_number.text = markup
            >>> staff = abjad.Staff([tuplet])
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    \override TupletNumber.text = \markup {
                        \score
                            {
                                \new Score
                                \with
                                {
                                    \override SpacingSpanner.spacing-increment = #0.5
                                    proportionalNotationDuration = ##f
                                }
                                <<
                                    \new RhythmicStaff
                                    \with
                                    {
                                        \remove Time_signature_engraver
                                        \remove Staff_symbol_engraver
                                        \override Stem.direction = #up
                                        \override Stem.length = #5
                                        \override TupletBracket.bracket-visibility = ##t
                                        \override TupletBracket.direction = #up
                                        \override TupletBracket.minimum-length = #4
                                        \override TupletBracket.padding = #1.25
                                        \override TupletBracket.shorten-pair = #'(-1 . -1.5)
                                        \override TupletBracket.springs-and-rods = #ly:spanner::set-spacing-rods
                                        \override TupletNumber.font-size = #0
                                        \override TupletNumber.text = #tuplet-number::calc-fraction-text
                                        tupletFullLength = ##t
                                    }
                                    {
                                        c'4
                                    }
                                >>
                                \layout {
                                    indent = #0
                                    ragged-right = ##t
                                }
                            }
                        }
                    \times 2/3 {
                        c'8
                        d'8
                        e'8
                    }
                    \revert TupletNumber.text
                }

        """
        return self._force_fraction

    @force_fraction.setter
    def force_fraction(self, argument):
        if isinstance(argument, (bool, type(None))):
            self._force_fraction = argument
        else:
            raise TypeError(f"force fraction must be boolean (not {argument!r}).")

    @property
    def hide(self) -> typing.Optional[bool]:
        r"""
        Is true when tuplet bracket hides.

        ..  container:: example

            >>> tuplet = abjad.Tuplet((2, 3), "c'8 d'8 e'8")
            >>> abjad.show(tuplet) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(tuplet)
                \times 2/3 {
                    c'8
                    d'8
                    e'8
                }

            >>> tuplet.hide is None
            True

        ..  container:: example

            >>> tuplet_1 = abjad.Tuplet((2, 3), "c'4 d'4 e'4")
            >>> tuplet_2 = abjad.Tuplet((2, 3), "d'4 e'4 f'4")
            >>> staff = abjad.Staff([tuplet_1, tuplet_2])
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    \times 2/3 {
                        c'4
                        d'4
                        e'4
                    }
                    \times 2/3 {
                        d'4
                        e'4
                        f'4
                    }
                }

            >>> staff[0].hide = True
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    \scaleDurations #'(2 . 3) {
                        c'4
                        d'4
                        e'4
                    }
                    \times 2/3 {
                        d'4
                        e'4
                        f'4
                    }
                }

        Hides tuplet bracket and tuplet number when true.
        """
        return self._hide

    @hide.setter
    def hide(self, argument):
        assert isinstance(argument, (bool, type(None))), repr(argument)
        self._hide = argument

    @property
    def implied_prolation(self) -> Multiplier:
        r"""
        Gets implied prolation of tuplet.

        ..  container:: example

            Defined equal to tuplet multiplier:

            >>> tuplet = abjad.Tuplet((2, 3), "c'8 d'8 e'8")
            >>> abjad.show(tuplet) # doctest: +SKIP

            >>> tuplet.implied_prolation
            Multiplier(2, 3)

        """
        return self.multiplier

    @property
    def multiplied_duration(self) -> Duration:
        r"""
        Gets multiplied duration of tuplet.

        ..  container:: example

            >>> tuplet = abjad.Tuplet((2, 3), "c'8 d'8 e'8")

            >>> abjad.show(tuplet) # doctest: +SKIP

            >>> tuplet.multiplied_duration
            Duration(1, 4)

        """
        return self.multiplier * self._get_contents_duration()

    @property
    def multiplier(self) -> Multiplier:
        r"""
        Gets and sets multiplier of tuplet.

        ..  container:: example

            Gets tuplet multiplier:

                >>> tuplet = abjad.Tuplet((2, 3), "c'8 d'8 e'8")
                >>> abjad.show(tuplet) # doctest: +SKIP

            >>> tuplet.multiplier
            Multiplier(2, 3)

        ..  container:: example

            Sets tuplet multiplier:

                >>> tuplet.multiplier = abjad.Multiplier(4, 3)
                >>> abjad.show(tuplet) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(tuplet)
                \tweak text #tuplet-number::calc-fraction-text
                \times 4/3 {
                    c'8
                    d'8
                    e'8
                }

        """
        return self._multiplier

    @multiplier.setter
    def multiplier(self, argument):
        if isinstance(argument, (int, quicktions.Fraction)):
            rational = Multiplier(argument)
        elif isinstance(argument, tuple):
            rational = Multiplier(argument)
        else:
            raise ValueError(f"can not set tuplet multiplier: {argument!r}.")
        if 0 < rational:
            self._multiplier = rational
        else:
            raise ValueError(f"tuplet multiplier must be positive: {argument!r}.")

    @property
    def tag(self) -> typing.Optional[Tag]:
        r"""
        Gets tag.

        ..  container:: example

            >>> tuplet = abjad.Tuplet(
            ...     (2, 3), "c'4 d' e'", tag=abjad.Tag('RED')
            ... )
            >>> abjad.show(tuplet) # doctest: +SKIP

            >>> abjad.f(tuplet, strict=20)
            \times 2/3 {        %! RED
                c'4
                d'4
                e'4
            }                   %! RED

        """
        return super().tag

    @property
    def tweaks(self) -> typing.Optional[TweakInterface]:
        r"""
        Gets tweaks.

        ..  container:: example

            >>> tuplet_1 = abjad.Tuplet((2, 3), "c'4 ( d'4 e'4 )")
            >>> abjad.tweak(tuplet_1).color = 'red'
            >>> abjad.tweak(tuplet_1).staff_padding = 2

            >>> tuplet_2 = abjad.Tuplet((2, 3), "c'4 ( d'4 e'4 )")
            >>> abjad.tweak(tuplet_2).color = 'green'
            >>> abjad.tweak(tuplet_2).staff_padding = 2

            >>> tuplet_3 = abjad.Tuplet((5, 4), [tuplet_1, tuplet_2])
            >>> abjad.tweak(tuplet_3).color = 'blue'
            >>> abjad.tweak(tuplet_3).staff_padding = 4

            >>> staff = abjad.Staff([tuplet_3])
            >>> leaves = abjad.select(staff).leaves()
            >>> abjad.attach(abjad.TimeSignature((5, 4)), leaves[0])
            >>> literal = abjad.LilyPondLiteral(r'\set tupletFullLength = ##t')
            >>> abjad.attach(literal, staff)
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    \set tupletFullLength = ##t
                    \tweak text #tuplet-number::calc-fraction-text
                    \tweak color #blue
                    \tweak staff-padding #4
                    \times 5/4 {
                        \tweak color #red
                        \tweak staff-padding #2
                        \times 2/3 {
                            \time 5/4
                            c'4
                            (
                            d'4
                            e'4
                            )
                        }
                        \tweak color #green
                        \tweak staff-padding #2
                        \times 2/3 {
                            c'4
                            (
                            d'4
                            e'4
                            )
                        }
                    }
                }

            ..  todo:: Report LilyPond bug that results from removing
                tupletFullLength in the example above: blue tuplet bracket
                shrinks to encompass only the second underlying tuplet.

        """
        return self._tweaks

    ### PUBLIC METHODS ###

    def append(self, component, preserve_duration=False) -> None:
        r"""
        Appends ``component`` to tuplet.

        ..  container:: example

            Appends note to tuplet:

            >>> tuplet = abjad.Tuplet((2, 3), "c'4 ( d'4 f'4 )")
            >>> abjad.show(tuplet) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(tuplet)
                \times 2/3 {
                    c'4
                    (
                    d'4
                    f'4
                    )
                }

            >>> tuplet.append(abjad.Note("e'4"))
            >>> abjad.show(tuplet) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(tuplet)
                \tweak edge-height #'(0.7 . 0)
                \times 2/3 {
                    c'4
                    (
                    d'4
                    f'4
                    )
                    e'4
                }

        ..  container:: example

            Appends note to tuplet and preserves tuplet duration:

            >>> tuplet = abjad.Tuplet((2, 3), "c'4 ( d'4 f'4 )")
            >>> abjad.show(tuplet) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(tuplet)
                \times 2/3 {
                    c'4
                    (
                    d'4
                    f'4
                    )
                }

            >>> tuplet.append(abjad.Note("e'4"), preserve_duration=True)
            >>> abjad.show(tuplet) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(tuplet)
                \times 1/2 {
                    c'4
                    (
                    d'4
                    f'4
                    )
                    e'4
                }

        """
        if preserve_duration:
            old_duration = self._get_duration()
        Container.append(self, component)
        if preserve_duration:
            new_duration = self._get_contents_duration()
            multiplier = old_duration / new_duration
            self.multiplier = multiplier
            assert self._get_duration() == old_duration

    def augmentation(self) -> bool:
        r"""
        Is true when tuplet multiplier is greater than ``1``.

        ..  container:: example

            Augmented tuplet:

            >>> tuplet = abjad.Tuplet((4, 3), "c'8 d'8 e'8")
            >>> abjad.show(tuplet) # doctest: +SKIP

            >>> tuplet.augmentation()
            True

        ..  container:: example

            Diminished tuplet:

            >>> tuplet = abjad.Tuplet((2, 3), "c'4 d'4 e'4")
            >>> abjad.show(tuplet) # doctest: +SKIP

            >>> tuplet.augmentation()
            False

        ..  container:: example

            Trivial tuplet:

            >>> tuplet = abjad.Tuplet((1, 1), "c'8. d'8. e'8.")
            >>> abjad.show(tuplet) # doctest: +SKIP

            >>> tuplet.augmentation()
            False

        """
        if self.multiplier:
            return 1 < self.multiplier
        else:
            return False

    def diminution(self) -> bool:
        r"""
        Is true when tuplet multiplier is less than ``1``.

        ..  container:: example

            Augmented tuplet:

            >>> tuplet = abjad.Tuplet((4, 3), "c'8 d'8 e'8")
            >>> abjad.show(tuplet) # doctest: +SKIP

            >>> tuplet.diminution()
            False

        ..  container:: example

            Diminished tuplet:

            >>> tuplet = abjad.Tuplet((2, 3), "c'4 d'4 e'4")
            >>> abjad.show(tuplet) # doctest: +SKIP

            >>> tuplet.diminution()
            True

        ..  container:: example

            Trivial tuplet:

            >>> tuplet = abjad.Tuplet((1, 1), "c'8. d'8. e'8.")
            >>> abjad.show(tuplet) # doctest: +SKIP

            >>> tuplet.diminution()
            False

        """
        if self.multiplier:
            return self.multiplier < 1
        else:
            return False

    def extend(self, argument, preserve_duration=False) -> None:
        r"""
        Extends tuplet with ``argument``.

        ..  container:: example

            Extends tuplet with three notes:

            >>> tuplet = abjad.Tuplet((2, 3), "c'4 ( d'4 f'4 )")
            >>> abjad.show(tuplet) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(tuplet)
                \times 2/3 {
                    c'4
                    (
                    d'4
                    f'4
                    )
                }

            >>> notes = [abjad.Note("e'32"), abjad.Note("d'32"), abjad.Note("e'16")]
            >>> tuplet.extend(notes)
            >>> abjad.show(tuplet) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(tuplet)
                \tweak edge-height #'(0.7 . 0)
                \times 2/3 {
                    c'4
                    (
                    d'4
                    f'4
                    )
                    e'32
                    d'32
                    e'16
                }

        ..  container:: example

            Extends tuplet with three notes and preserves tuplet duration:

            >>> tuplet = abjad.Tuplet((2, 3), "c'4 ( d'4 f'4 )")
            >>> abjad.show(tuplet) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(tuplet)
                \times 2/3 {
                    c'4
                    (
                    d'4
                    f'4
                    )
                }

            >>> notes = [abjad.Note("e'32"), abjad.Note("d'32"), abjad.Note("e'16")]
            >>> tuplet.extend(notes, preserve_duration=True)
            >>> abjad.show(tuplet) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(tuplet)
                \times 4/7 {
                    c'4
                    (
                    d'4
                    f'4
                    )
                    e'32
                    d'32
                    e'16
                }

        """
        if preserve_duration:
            old_duration = self._get_duration()
        Container.extend(self, argument)
        if preserve_duration:
            new_duration = self._get_contents_duration()
            multiplier = old_duration / new_duration
            self.multiplier = multiplier
            assert self._get_duration() == old_duration

    @staticmethod
    def from_duration(
        duration: typings.DurationTyping, components, *, tag: Tag = None
    ) -> "Tuplet":
        r"""
        Makes tuplet from ``duration`` and ``components``.

        ..  container:: example

            Makes diminution:

            >>> tuplet = abjad.Tuplet.from_duration((2, 8), "c'8 d' e'")
            >>> abjad.show(tuplet) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(tuplet)
                \times 2/3 {
                    c'8
                    d'8
                    e'8
                }

        """
        if not len(components):
            raise Exception(f"components must be nonempty: {components!r}.")
        target_duration = Duration(duration)
        tuplet = Tuplet(1, components, tag=tag)
        contents_duration = tuplet._get_duration()
        multiplier = target_duration / contents_duration
        tuplet.multiplier = multiplier
        return tuplet

    def normalize_multiplier(self) -> None:
        r"""
        Normalizes tuplet multiplier.

        ..  container:: example

            >>> tuplet = abjad.Tuplet((1, 3), "c'4 d' e'")
            >>> abjad.show(tuplet) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(tuplet)
                \times 1/3 {
                    c'4
                    d'4
                    e'4
                }

            >>> tuplet.multiplier.normalized()
            False

            >>> tuplet.normalize_multiplier()
            >>> abjad.show(tuplet) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(tuplet)
                \times 2/3 {
                    c'8
                    d'8
                    e'8
                }

            >>> tuplet.multiplier.normalized()
            True

        ..  container:: example

            >>> tuplet = abjad.Tuplet((8, 3), "c'32 d'32 e'32")
            >>> abjad.show(tuplet) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(tuplet)
                \tweak text #tuplet-number::calc-fraction-text
                \times 8/3 {
                    c'32
                    d'32
                    e'32
                }

            >>> tuplet.multiplier.normalized()
            False

            >>> tuplet.normalize_multiplier()
            >>> abjad.show(tuplet) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(tuplet)
                \tweak text #tuplet-number::calc-fraction-text
                \times 4/3 {
                    c'16
                    d'16
                    e'16
                }

            >>> tuplet.multiplier.normalized()
            True

        ..  container:: example

            >>> tuplet = abjad.Tuplet((5, 12), "c'4 d'4 e'4")
            >>> abjad.show(tuplet) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(tuplet)
                \tweak text #tuplet-number::calc-fraction-text
                \times 5/12 {
                    c'4
                    d'4
                    e'4
                }

            >>> tuplet.multiplier.normalized()
            False

            >>> tuplet.normalize_multiplier()
            >>> abjad.show(tuplet) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(tuplet)
                \tweak text #tuplet-number::calc-fraction-text
                \times 5/6 {
                    c'8
                    d'8
                    e'8
                }

            >>> tuplet.multiplier.normalized()
            True

        """
        # find tuplet multiplier
        integer_exponent = int(math.log(self.multiplier, 2))
        leaf_multiplier = Multiplier(2) ** integer_exponent
        # scale leaves in tuplet by power of two
        for component in self:
            if isinstance(component, Leaf):
                old_written_duration = component.written_duration
                new_written_duration = leaf_multiplier * old_written_duration
                multiplier = new_written_duration / old_written_duration
                component._scale(multiplier)
        numerator, denominator = leaf_multiplier.pair
        multiplier = Multiplier(denominator, numerator)
        self.multiplier *= multiplier

    def rest_filled(self) -> bool:
        r"""
        Is true when tuplet is rest-filled.

        ..  container:: example

            >>> tuplet = abjad.Tuplet((3, 2), "r4 r r")
            >>> abjad.show(tuplet) # doctest: +SKIP

            ..  container:: example

                >>> abjad.f(tuplet)
                \tweak text #tuplet-number::calc-fraction-text
                \times 3/2 {
                    r4
                    r4
                    r4
                }

            >>> tuplet.rest_filled()
            True

        """
        return all(isinstance(_, Rest) for _ in self)

    def rewrite_dots(self) -> None:
        r"""
        Rewrites dots.

        ..  container:: example

            Rewrites single dots as 3:2 prolation:

            >>> tuplet = abjad.Tuplet(1, "c'8. c'8.")
            >>> abjad.show(tuplet) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(tuplet)
                \tweak text #tuplet-number::calc-fraction-text
                \times 1/1 {
                    c'8.
                    c'8.
                }

            >>> tuplet.rewrite_dots()
            >>> abjad.show(tuplet) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(tuplet)
                \tweak text #tuplet-number::calc-fraction-text
                \times 3/2 {
                    c'8
                    c'8
                }

        ..  container:: example

            Rewrites double dots as 7:4 prolation:

            >>> tuplet = abjad.Tuplet(1, "c'8.. c'8..")
            >>> abjad.show(tuplet) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(tuplet)
                \tweak text #tuplet-number::calc-fraction-text
                \times 1/1 {
                    c'8..
                    c'8..
                }

            >>> tuplet.rewrite_dots()
            >>> abjad.show(tuplet) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(tuplet)
                \tweak text #tuplet-number::calc-fraction-text
                \times 7/4 {
                    c'8
                    c'8
                }

        ..  container:: example

            Does nothing when dot counts differ:

            >>> tuplet = abjad.Tuplet(1, "c'8. d'8. e'8")
            >>> abjad.show(tuplet) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(tuplet)
                \tweak text #tuplet-number::calc-fraction-text
                \times 1/1 {
                    c'8.
                    d'8.
                    e'8
                }

            >>> tuplet.rewrite_dots()
            >>> abjad.show(tuplet) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(tuplet)
                \tweak text #tuplet-number::calc-fraction-text
                \times 1/1 {
                    c'8.
                    d'8.
                    e'8
                }

        ..  container:: example

            Does nothing when leaves carry no dots:

            >>> tuplet = abjad.Tuplet((3, 2), "c'8 d' e'")
            >>> abjad.show(tuplet) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(tuplet)
                \tweak text #tuplet-number::calc-fraction-text
                \times 3/2 {
                    c'8
                    d'8
                    e'8
                }

            >>> tuplet.rewrite_dots()
            >>> abjad.show(tuplet) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(tuplet)
                \tweak text #tuplet-number::calc-fraction-text
                \times 3/2 {
                    c'8
                    d'8
                    e'8
                }

        Not yet implemented for multiply nested tuplets.
        """
        dot_counts = set()
        for component in self:
            if isinstance(component, Tuplet):
                return
            dot_count = component.written_duration.dot_count
            dot_counts.add(dot_count)
        if 1 < len(dot_counts):
            return
        assert len(dot_counts) == 1
        global_dot_count = dot_counts.pop()
        if global_dot_count == 0:
            return
        dot_multiplier = Multiplier.from_dot_count(global_dot_count)
        self.multiplier *= dot_multiplier
        dot_multiplier_reciprocal = dot_multiplier.reciprocal
        for component in self:
            component.written_duration *= dot_multiplier_reciprocal

    def set_minimum_denominator(self, denominator) -> None:
        r"""
        Sets preferred denominator of tuplet to at least ``denominator``.

        ..  container:: example

            Sets preferred denominator of tuplet to ``8`` at least:

            >>> tuplet = abjad.Tuplet((3, 5), "c'4 d'8 e'8 f'4 g'2")
            >>> abjad.show(tuplet) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(tuplet)
                \tweak text #tuplet-number::calc-fraction-text
                \times 3/5 {
                    c'4
                    d'8
                    e'8
                    f'4
                    g'2
                }

            >>> tuplet.set_minimum_denominator(8)
            >>> abjad.show(tuplet) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(tuplet)
                \tweak text #tuplet-number::calc-fraction-text
                \times 6/10 {
                    c'4
                    d'8
                    e'8
                    f'4
                    g'2
                }

        """
        assert mathtools.is_nonnegative_integer_power_of_two(denominator)
        self.force_fraction = True
        durations = [
            self._get_contents_duration(),
            self._get_preprolated_duration(),
            Duration(1, denominator),
        ]
        nonreduced_fractions = Duration.durations_to_nonreduced_fractions(durations)
        self.denominator = nonreduced_fractions[1].numerator

    def toggle_prolation(self) -> None:
        r"""
        Changes augmented tuplets to diminished;
        changes diminished tuplets to augmented.

        ..  container:: example

            Changes augmented tuplet to diminished:

            >>> tuplet = abjad.Tuplet((4, 3), "c'8 d'8 e'8")
            >>> abjad.show(tuplet) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(tuplet)
                \tweak text #tuplet-number::calc-fraction-text
                \times 4/3 {
                    c'8
                    d'8
                    e'8
                }

            >>> tuplet.toggle_prolation()
            >>> abjad.show(tuplet) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(tuplet)
                \times 2/3 {
                    c'4
                    d'4
                    e'4
                }

            Multiplies the written duration of the leaves in tuplet
            by the least power of ``2`` necessary to diminshed tuplet.

        ..  container:: example

            Changes diminished tuplet to augmented:

            >>> tuplet = abjad.Tuplet((2, 3), "c'4 d'4 e'4")
            >>> abjad.show(tuplet) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(tuplet)
                \times 2/3 {
                    c'4
                    d'4
                    e'4
                }

            >>> tuplet.toggle_prolation()
            >>> abjad.show(tuplet) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(tuplet)
                \tweak text #tuplet-number::calc-fraction-text
                \times 4/3 {
                    c'8
                    d'8
                    e'8
                }

            Divides the written duration of the leaves in tuplet
            by the least power of ``2`` necessary to diminshed tuplet.

        ..  container:: example

            REGRESSION. Leaves trivial tuplets unchanged:

            >>> tuplet = abjad.Tuplet(1, "c'4 d'4 e'4")
            >>> abjad.show(tuplet) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(tuplet)
                \tweak text #tuplet-number::calc-fraction-text
                \times 1/1 {
                    c'4
                    d'4
                    e'4
                }

            >>> tuplet.toggle_prolation()
            >>> abjad.show(tuplet) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(tuplet)
                \tweak text #tuplet-number::calc-fraction-text
                \times 1/1 {
                    c'4
                    d'4
                    e'4
                }

        Does not yet work with nested tuplets.
        """
        from .Iteration import Iteration

        if self.diminution():
            while self.diminution():
                self.multiplier *= 2
                for leaf in Iteration(self).leaves():
                    leaf.written_duration /= 2
        elif self.augmentation():
            while not self.diminution():
                self.multiplier /= 2
                for leaf in Iteration(self).leaves():
                    leaf.written_duration *= 2

    def trivial(self) -> bool:
        r"""
        Is true when tuplet multiplier is equal to ``1`` and no multipliers
        attach to any leaves in tuplet.

        ..  container:: example

            >>> tuplet = abjad.Tuplet((1, 1), "c'8 d'8 e'8")
            >>> abjad.show(tuplet) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(tuplet)
                \tweak text #tuplet-number::calc-fraction-text
                \times 1/1 {
                    c'8
                    d'8
                    e'8
                }

            >>> tuplet.trivial()
            True

        ..  container:: example

            Tuplet is not trivial when multipliers attach to tuplet leaves:

            >>> tuplet = abjad.Tuplet((1, 1), "c'8 d'8 e'8")
            >>> tuplet[0].multiplier = (3, 2)
            >>> tuplet[-1].multiplier = (1, 2)
            >>> abjad.show(tuplet) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(tuplet)
                \tweak text #tuplet-number::calc-fraction-text
                \times 1/1 {
                    c'8 * 3/2
                    d'8
                    e'8 * 1/2
                }

            >>> tuplet.trivial()
            False

        """
        from .Iteration import Iteration

        for leaf in Iteration(self).leaves():
            if leaf.multiplier is not None:
                return False
        return self.multiplier == 1

    def trivializable(self) -> bool:
        r"""
        Is true when tuplet is trivializable (can be rewritten with a ratio of
        1:1).

        ..  container:: example

            Redudant tuplet:

            >>> tuplet = abjad.Tuplet((3, 4), "c'4 c'4")
            >>> abjad.attach(abjad.TimeSignature((3, 8)), tuplet[0])
            >>> staff = abjad.Staff([tuplet])
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(tuplet)
                \tweak text #tuplet-number::calc-fraction-text
                \times 3/4 {
                    \time 3/8
                    c'4
                    c'4
                }

            >>> tuplet.trivializable()
            True

            Can be rewritten without a tuplet bracket:

            >>> staff = abjad.Staff("c'8. c'8.")
            >>> abjad.attach(abjad.TimeSignature((3, 8)), staff[0])
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    \time 3/8
                    c'8.
                    c'8.
                }

        ..  container:: example

            Nontrivializable tuplet:

            >>> tuplet = abjad.Tuplet((3, 5), "c'4 c'4 c'4 c'4 c'4")
            >>> abjad.attach(abjad.TimeSignature((3, 4)), tuplet[0])
            >>> staff = abjad.Staff([tuplet])
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 3/5 {
                        \time 3/4
                        c'4
                        c'4
                        c'4
                        c'4
                        c'4
                    }
                }

            >>> tuplet.trivializable()
            False

            Can not be rewritten without a tuplet bracket.

        ..  container:: example

            REGRESSION. Nontrivializable tuplet:

            >>> tuplet = abjad.Tuplet((3, 4), "c'2. c4")
            >>> abjad.attach(abjad.TimeSignature((3, 4)), tuplet[0])
            >>> staff = abjad.Staff([tuplet])
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 3/4 {
                        \time 3/4
                        c'2.
                        c4
                    }
                }

            >>> tuplet.trivializable()
            False

        """
        for component in self:
            if isinstance(component, Tuplet):
                continue
            assert isinstance(component, Leaf), repr(component)
            duration = component.written_duration * self.multiplier
            if not duration.is_assignable:
                return False
        return True

    def trivialize(self) -> None:
        r"""
        Trivializes tuplet.

        ..  container:: example

            >>> tuplet = abjad.Tuplet((3, 4), "c'2")
            >>> abjad.show(tuplet) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(tuplet)
                \tweak text #tuplet-number::calc-fraction-text
                \times 3/4 {
                    c'2
                }

            >>> tuplet.trivializable()
            True

            >>> tuplet.trivialize()
            >>> abjad.show(tuplet) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(tuplet)
                \tweak text #tuplet-number::calc-fraction-text
                \times 1/1 {
                    c'4.
                }

        """
        if not self.trivializable():
            return
        for component in self:
            if isinstance(component, Tuplet):
                component.multiplier *= self.multiplier
            elif isinstance(component, Leaf):
                component.written_duration *= self.multiplier
            else:
                raise TypeError(component)
        self.multiplier = Multiplier(1)
