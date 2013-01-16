from abjad.tools import iotools
from abjad.tools import timespantools
from experimental.tools.settingtools.FinalizedRhythmRegionCommand import FinalizedRhythmRegionCommand


class ParseableStringRhythmRegionCommand(FinalizedRhythmRegionCommand):
    '''Parseable string rhythm region command.
    '''

    ### INITIALIZER ###

    def __init__(self, parseable_string=None, total_duration=None, voice_name=None, start_offset=None):
        self._parseable_string = parseable_string
        self._total_duration = total_duration
        self._voice_name = voice_name
        self._start_offset = start_offset

    ### PRIVATE METHODS ###

    def _get_payload(self, score_specification=None, voice_name=None):
        from experimental.tools import settingtools
        component = iotools.p(self.parseable_string)
        rhythm_region_product = settingtools.RhythmRegionProduct(
            payload=[component], voice_name=self.voice_name, start_offset=self.start_offset)
        # TODO: maybe create timespan here instead of just offset
        stop_offset = self.start_offset + self.total_duration
        # TODO: maybe use timespan comparisons here instead offset comparisons
        if rhythm_region_product.timespan.stops_before_offset(stop_offset):
            rhythm_region_product.repeat_to_stop_offset(stop_offset)
        elif rhythm_region_product.timespan.stops_after_offset(stop_offset):
            rhythm_region_product.set_offsets(stop_offset=stop_offset)
        return rhythm_region_product

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def parseable_string(self):
        return self._parseable_string

    @property
    def start_offset(self):
        return self._start_offset

    @property
    def total_duration(self):
        return self._total_duration

    @property
    def voice_name(self):
        return self._voice_name
