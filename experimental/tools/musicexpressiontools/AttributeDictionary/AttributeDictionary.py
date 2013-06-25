import collections
from abjad.tools import timespantools
from abjad.tools.abctools.AbjadObject import AbjadObject
from experimental.tools.musicexpressiontools.AttributeNameEnumeration \
    import AttributeNameEnumeration


class AttributeDictionary(AbjadObject, collections.OrderedDict):
    '''Attribute dictionary.
    '''

    ### CLASS VARIABLES ##

    attributes = AttributeNameEnumeration()

    ### INITIALIZER ###

    def __init__(self):
        collections.OrderedDict.__init__(self)
        for attribute in self.attributes:
            self[attribute] = timespantools.TimespanInventory()
        assert 'time_signatures' in self

    ### SPECIAL METHODS ###

    def __repr__(self):
        return collections.OrderedDict.__repr__(self)

    def __setitem__(self, key, value):
        assert isinstance(key, str), repr(key)
        assert isinstance(value, list), repr(value)
        collections.OrderedDict.__setitem__(self, key, value)

    ### PRIVATE PROPERTIES ###

    @property
    def _positional_argument_values(self):
        return self.items()
