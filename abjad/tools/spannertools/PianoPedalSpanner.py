import typing
from .Spanner import Spanner
from abjad.tools.lilypondnametools.LilyPondContextSetting import \
    LilyPondContextSetting
from abjad.tools.schemetools.SchemeSymbol import SchemeSymbol


class PianoPedalSpanner(Spanner):
    r'''
    Piano pedal spanner.

    ..  container:: example

        >>> staff = abjad.Staff("c'8 d'8 e'8 f'8")
        >>> spanner = abjad.PianoPedalSpanner()
        >>> abjad.tweak(spanner).color = 'blue'
        >>> abjad.tweak(spanner).sustain_pedal_line_spanner.staff_padding = 5
        >>> abjad.attach(spanner, staff[:])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(staff)
            \new Staff
            {
                \set Staff.pedalSustainStyle = #'mixed
                c'8
                - \tweak SustainPedalLineSpanner.staff-padding #5
                - \tweak color #blue
                \sustainOn
                d'8
                e'8
                f'8
                \sustainOff
            }

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_kind',
        '_style',
        )

    _kinds = {
        'sustain': (r'\sustainOn', r'\sustainOff'),
        'sostenuto': (r'\sostenutoOn', r'\sostenutoOff'),
        'corda': (r'\unaCorda', r'\treCorde'),
        }

    _styles = (
        'text',
        'bracket',
        'mixed',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        kind: str = 'sustain',
        leak: bool = None,
        style: str = 'mixed',
        ) -> None:
        Spanner.__init__(self, leak=leak)
        if kind not in list(self._kinds.keys()):
            raise ValueError(f'kind must be in {list(self._kinds.keys())!r}.')
        self._kind = kind
        if style not in self._styles:
            raise ValueError(f'style must be in {self._styles!r}.')
        self._style = style

    ### PRIVATE METHODS ###

    def _copy_keyword_args(self, new):
        new._kind = self.kind
        new._style = self.style

    def _get_lilypond_format_bundle(self, leaf):
        bundle = self._get_basic_lilypond_format_bundle(leaf)
        if self._is_my_only(leaf):
            style = SchemeSymbol(self.style)
            context_setting = LilyPondContextSetting(
                lilypond_type='Staff',
                context_property='pedalSustainStyle',
                value=style,
                )
            bundle.update(context_setting)
            string = self.start_command()
            bundle.right.spanner_starts.append(string)
            string = self.stop_command()
            bundle.right.spanner_starts.append(string)
        elif leaf is self[0]:
            style = SchemeSymbol(self.style)
            context_setting = LilyPondContextSetting(
                lilypond_type='Staff',
                context_property='pedalSustainStyle',
                value=style,
                )
            bundle.update(context_setting)
            string = self.start_command()
            bundle.right.spanner_starts.append(string)
        elif leaf is self[-1]:
            string = self.stop_command()
            bundle.right.spanner_stops.append(string)
        return bundle

    ### PUBLIC PROPERTIES ###

    @property
    def kind(self) -> str:
        r'''
        Gets kind of piano pedal spanner.

        ..  container:: example

            Sustain pedal:

            >>> staff = abjad.Staff("c'8 d'8 e'8 f'8")
            >>> spanner = abjad.PianoPedalSpanner(kind='sustain')
            >>> abjad.tweak(spanner).color = 'blue'
            >>> abjad.tweak(spanner).sustain_pedal_line_spanner.staff_padding = 5
            >>> abjad.attach(spanner, staff[:])
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    \set Staff.pedalSustainStyle = #'mixed
                    c'8
                    - \tweak SustainPedalLineSpanner.staff-padding #5
                    - \tweak color #blue
                    \sustainOn
                    d'8
                    e'8
                    f'8
                    \sustainOff
                }

        ..  container:: example

            Sostenuto pedal:

            >>> staff = abjad.Staff("c'8 d'8 e'8 f'8")
            >>> spanner = abjad.PianoPedalSpanner(kind='sostenuto')
            >>> abjad.tweak(spanner).color = 'blue'
            >>> abjad.tweak(spanner).sostenuto_pedal_line_spanner.staff_padding = 5
            >>> abjad.attach(spanner, staff[:])
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    \set Staff.pedalSustainStyle = #'mixed
                    c'8
                    - \tweak SostenutoPedalLineSpanner.staff-padding #5
                    - \tweak color #blue
                    \sostenutoOn
                    d'8
                    e'8
                    f'8
                    \sostenutoOff
                }

        ..  container:: example

            Una corda / tre corde pedal:

            >>> staff = abjad.Staff("c'8 d'8 e'8 f'8")
            >>> spanner = abjad.PianoPedalSpanner(kind='corda')
            >>> abjad.attach(spanner, staff[:])
            >>> abjad.override(staff[0]).staff.una_corda_pedal.color = 'blue'
            >>> abjad.override(staff[0]).staff.una_corda_pedal_line_spanner.staff_padding = 5
            >>> abjad.override(staff[-1]).staff.una_corda_pedal.color = 'blue'
            >>> abjad.override(staff[-1]).staff.una_corda_pedal_line_spanner.staff_padding = 5
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    \once \override Staff.UnaCordaPedal.color = #blue
                    \once \override Staff.UnaCordaPedalLineSpanner.staff-padding = #5
                    \set Staff.pedalSustainStyle = #'mixed
                    c'8
                    \unaCorda
                    d'8
                    e'8
                    \once \override Staff.UnaCordaPedal.color = #blue
                    \once \override Staff.UnaCordaPedalLineSpanner.staff-padding = #5
                    f'8
                    \treCorde
                }

            Note that when no visible bracket connects start-text and stop-text
            indications (as above) that the first and last leaves in spanner
            must be overriden independently. (Note also that ``abjad.tweak()``
            will apply to only the pedal-down indication and will leave the
            pedal-up indication unmodified.)

        Returns ``'sustain'``, ``'sostenuto'`` or ``'corda'``.
        '''
        return self._kind

    @property
    def leak(self) -> typing.Optional[bool]:
        r'''
        Is true when piano pedal spanner leaks one leaf to the right.

        ..  container:: example

            Without leak

            >>> staff = abjad.Staff("c'8 d'8 r8 f'8")
            >>> spanner = abjad.PianoPedalSpanner(kind='sustain')
            >>> abjad.tweak(spanner).sustain_pedal_line_spanner.staff_padding = 5
            >>> abjad.attach(spanner, staff[:2])
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    \set Staff.pedalSustainStyle = #'mixed
                    c'8
                    - \tweak SustainPedalLineSpanner.staff-padding #5
                    \sustainOn
                    d'8
                    \sustainOff
                    r8
                    f'8
                }

            With leak:

            >>> staff = abjad.Staff("c'8 d'8 r8 f'8")
            >>> spanner = abjad.PianoPedalSpanner(kind='sustain', leak=True)
            >>> abjad.tweak(spanner).sustain_pedal_line_spanner.staff_padding = 5
            >>> abjad.attach(spanner, staff[:2])
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    \set Staff.pedalSustainStyle = #'mixed
                    c'8
                    - \tweak SustainPedalLineSpanner.staff-padding #5
                    \sustainOn
                    d'8
                    <> \sustainOff
                    r8
                    f'8
                }

        '''
        return super(PianoPedalSpanner, self).leak

    @property
    def style(self) -> str:
        r'''
        Gets style of piano pedal spanner.

        ..  container:: example

            Mixed style:

            >>> staff = abjad.Staff("c'8 d'8 e'8 f'8")
            >>> spanner = abjad.PianoPedalSpanner(style='mixed')
            >>> abjad.tweak(spanner).sustain_pedal_line_spanner.staff_padding = 5
            >>> abjad.attach(spanner, staff[:])
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    \set Staff.pedalSustainStyle = #'mixed
                    c'8
                    - \tweak SustainPedalLineSpanner.staff-padding #5
                    \sustainOn
                    d'8
                    e'8
                    f'8
                    \sustainOff
                }

        ..  container:: example

            Bracket style:

            >>> staff = abjad.Staff("c'8 d'8 e'8 f'8")
            >>> spanner = abjad.PianoPedalSpanner(style='bracket')
            >>> abjad.tweak(spanner).sustain_pedal_line_spanner.staff_padding = 5
            >>> abjad.attach(spanner, staff[:])
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    \set Staff.pedalSustainStyle = #'bracket
                    c'8
                    - \tweak SustainPedalLineSpanner.staff-padding #5
                    \sustainOn
                    d'8
                    e'8
                    f'8
                    \sustainOff
                }

        ..  container:: example

            Text style:

            >>> staff = abjad.Staff("c'8 d'8 e'8 f'8")
            >>> spanner = abjad.PianoPedalSpanner(style='text')
            >>> abjad.override(staff[0]).staff.sustain_pedal_line_spanner.staff_padding = 5
            >>> abjad.override(staff[-1]).staff.sustain_pedal_line_spanner.staff_padding = 5
            >>> abjad.attach(spanner, staff[:])
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    \once \override Staff.SustainPedalLineSpanner.staff-padding = #5
                    \set Staff.pedalSustainStyle = #'text
                    c'8
                    \sustainOn
                    d'8
                    e'8
                    \once \override Staff.SustainPedalLineSpanner.staff-padding = #5
                    f'8
                    \sustainOff
                }

            Note that when no visible bracket connects start-text and stop-text
            indications (as above) that the first and last leaves in spanner
            must be overriden independently. (Note also that ``abjad.tweak()``
            will apply to only the pedal-down indication and will leave the
            pedal-up indication unmodified.)

        Returns ``'mixed'``, ``'bracket'`` or ``'text'``.
        '''
        return self._style

    ### PUBLIC METHODS ###

    def start_command(self) -> typing.Optional[str]:
        r'''
        Gets start command.

        ..  container:: example

            >>> abjad.PianoPedalSpanner(kind='sustain').start_command()
            '\\sustainOn'

            >>> abjad.PianoPedalSpanner(kind='sostenuto').start_command()
            '\\sostenutoOn'

            >>> abjad.PianoPedalSpanner(kind='corda').start_command()
            '\\unaCorda'

        '''
        return self._kinds[self.kind][0]

    def stop_command(self) -> typing.Optional[str]:
        r'''
        Gets stop command.

        ..  container:: example

            >>> abjad.PianoPedalSpanner(kind='sustain').stop_command()
            '\\sustainOff'

            >>> abjad.PianoPedalSpanner(kind='sostenuto').stop_command()
            '\\sostenutoOff'

            >>> abjad.PianoPedalSpanner(kind='corda').stop_command()
            '\\treCorde'

            With leak:

            >>> spanner =abjad.PianoPedalSpanner(kind='sustain', leak=True)
            >>> spanner.stop_command()
            '<> \\sustainOff'

            >>> spanner =abjad.PianoPedalSpanner(kind='sostenuto', leak=True)
            >>> spanner.stop_command()
            '<> \\sostenutoOff'

            >>> spanner =abjad.PianoPedalSpanner(kind='corda', leak=True)
            >>> spanner.stop_command()
            '<> \\treCorde'

        '''
        string = self._kinds[self.kind][1]
        string = self._add_leak(string)
        return string
