# -*- encoding: utf-8 -*-
from abjad.tools.abctools import AbjadObject


class ChordQuality(AbjadObject):
    '''A chord quality, such as major, minor, dominant,
    diminished and so on.

    Value object that can not be changed after instantiation.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_quality_string',
        )

    _acceptable_quality_strings = (
        'augmented',
        'diminished',
        'dominant',
        'half diminished',
        'major',
        'minor',
        )

    _default_positional_input_arguments = (
        repr('dominant'),
        )

    _uppercase_quality_strings = (
        'augmented',
        'dominant',
        'major',
        )

    ### INITIALIZER ###

    def __init__(self, quality_string):
        if quality_string not in self._acceptable_quality_strings:
            message = 'can not initialize chord quality: {!r}.'
            message = message.format(quality_string)
            raise ValueError(message)
        self._quality_string = quality_string

    ### SPECIAL METHODS ###

    def __eq__(self, arg):
        if isinstance(arg, type(self)):
            if self.quality_string == arg.quality_string:
                return True
        return False

    def __ne__(self, arg):
        return not self == arg

    def __repr__(self):
        return '{}({})'.format(type(self).__name__, self.quality_string)

    ### PRIVATE PROPERTIES ###

    @property
    def _storage_format_specification(self):
        from abjad.tools import systemtools
        return systemtools.StorageFormatSpecification(
            self,
            positional_argument_values=(
                self.quality_string,
                )
            )

    ### PUBLIC PROPERTIES ###

    @property
    def is_uppercase(self):
        return self.quality_string in self._uppercase_quality_strings

    @property
    def quality_string(self):
        return self._quality_string
