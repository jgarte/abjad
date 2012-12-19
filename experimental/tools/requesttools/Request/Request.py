import abc
import copy
from abjad.tools import datastructuretools
from abjad.tools import durationtools
from abjad.tools import mathtools
from abjad.tools import sequencetools
from abjad.tools.abctools.AbjadObject import AbjadObject
from experimental.tools import helpertools


class Request(AbjadObject):
    r'''.. versionadded:: 1.0

    Base class from which other request classes inherit.

    Requests function as setting sources.
    '''

    ### CLASS ATTRIBUTES ###

    __metaclass__ = abc.ABCMeta

    attributes = helpertools.AttributeNameEnumeration()

    ### INITIALIZER ###

    @abc.abstractmethod
    def __init__(self, modifications=None, index=None, count=None):
        assert isinstance(index, (int, type(None))), repr(index)
        assert isinstance(count, (int, type(None))), repr(count)
        modifications = modifications or []
        self._modifications = datastructuretools.ObjectInventory(modifications)
        self._index = index
        self._count = count

    ### SPECIAL METHODS ###

    def __eq__(self, expr):
        '''True when mandatory and keyword arguments compare equal.
        Otherwise false.

        Return boolean.
        '''
        if not isinstance(expr, type(self)):
            return False
        if not self._positional_argument_values == expr._positional_argument_values:
            return False
        return self._keyword_argument_values == expr._keyword_argument_values

    def __getitem__(self, expr):
        '''Return copy of request with appended modification.
        '''
        modification = 'result = target.__getitem__({!r})'.format(expr)
        result = self._clone()
        result.modifications.append(modification)
        return result

    ### PRIVATE READ-ONLY PROPERTIES ###

    @property
    def _keyword_argument_name_value_strings(self):
        result = AbjadObject._keyword_argument_name_value_strings.fget(self)
        if 'modifications=ObjectInventory([])' in result:
            result = list(result)
            result.remove('modifications=ObjectInventory([])')
        return tuple(result)

    ### PRIVATE METHODS ###

    def _clone(self):
        return copy.deepcopy(self)

    def _get_tools_package_qualified_keyword_argument_repr_pieces(self, is_indented=True):
        '''Do not show empty modifications list.
        '''
        filtered_result = []
        result = AbjadObject._get_tools_package_qualified_keyword_argument_repr_pieces(
            self, is_indented=is_indented)
        for string in result:
            if not 'modifications=datastructuretools.ObjectInventory([])' in string:
                filtered_result.append(string)
        return filtered_result

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def count(self):
        return self._count

    @property
    def index(self):
        return self._index

    @property
    def modifications(self):
        return self._modifications

    ### PUBLIC METHODS ###

    def repeat_to_length(self, length):
        '''Return copy of request with appended modification.
        '''
        assert mathtools.is_nonnegative_integer(length)
        modification = 'result = sequencetools.repeat_sequence_to_length(target, {!r})'.format(length)
        result = self._clone()
        result.modifications.append(modification)
        return result
        
    def reverse(self):
        '''Return copy of request with appended modification.
        '''
        modification = 'result = target.reverse()'
        result = self._clone()
        result.modifications.append(modification)
        return result

    def rotate(self, index):
        '''Return copy of request with appended modification.
        '''
        from experimental.tools import settingtools
        assert isinstance(index, (int, durationtools.Duration, settingtools.RotationIndicator))
        #modification = 'result = target.rotate({!r})'.format(index)    
        modification = 'result = request._rotate(target, {!r})'.format(index)    
        result = self._clone()
        result.modifications.append(modification)
        return result

    def _rotate(self, sequence, n):
        if hasattr(sequence, 'rotate'):
            return sequence.rotate(n)
        else:
            return sequencetools.rotate_sequence(sequence, n)
