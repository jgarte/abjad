from abjad.tools import contexttools
from abjad.tools import markuptools
from abjad.tools import pitchtools
from abjad.tools.instrumenttools._BrassInstrument import _BrassInstrument


class Trumpet(_BrassInstrument):
    r'''.. versionadded:: 2.0

    Abjad model of the trumpet::

        abjad> staff = Staff("c'8 d'8 e'8 f'8")

    ::

        abjad> instrumenttools.Trumpet()(staff)
        Trumpet()(Staff{4})

    ::

        abjad> f(staff)
        \new Staff {
            \set Staff.instrumentName = \markup { Trumpet }
            \set Staff.shortInstrumentName = \markup { Tp. }
            c'8
            d'8
            e'8
            f'8
        }

    The trumpet targets staff context by default.
    '''

    def __init__(self, instrument_name=None, short_instrument_name=None,
        instrument_name_markup=None, short_instrument_name_markup=None, target_context=None):
        _BrassInstrument.__init__(self, instrument_name, short_instrument_name,
            instrument_name_markup=instrument_name_markup,
            short_instrument_name_markup=short_instrument_name_markup, target_context=target_context)
        self._default_instrument_name = 'trumpet'
        self._default_performer_names = ('trumpeter',)
        self._default_short_instrument_name = 'tp.'
        self._is_primary_instrument = True
        self.sounding_pitch_of_written_middle_c = pitchtools.NamedChromaticPitch("c'")
        self.primary_clefs = [contexttools.ClefMark('treble')]
        self._copy_primary_clefs_to_all_clefs()
        self.traditional_range = (-6, 26)
