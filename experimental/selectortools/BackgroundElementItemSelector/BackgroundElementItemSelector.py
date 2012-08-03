from abc import ABCMeta
from abc import abstractmethod
from abjad.tools import introspectiontools
from experimental import helpertools
from experimental.selectortools.InequalitySelector import InequalitySelector
from experimental.selectortools.ItemSelector import ItemSelector


class BackgroundElementItemSelector(ItemSelector, InequalitySelector):
    r'''.. versionadded:: 1.0

    Select exactly one background element.
    '''

    ### CLASS ATTRIBUTES ###

    __metaclass__ = ABCMeta

    ### INITIALIZER ###
    
    @abstractmethod
    def __init__(self, klass=None, inequality=None, identifier=0):
        from experimental import selectortools
        assert helpertools.is_background_element_klass(klass), repr(klass)
        ItemSelector.__init__(self, identifier=identifier)
        InequalitySelector.__init__(self, inequality=inequality)
        if isinstance(klass, tuple):
            klass = helpertools.KlassInventory(klass)
        self._klass = klass

    ### SPECIAL METHODS ###

    def __eq__(self, expr):
        if isinstance(expr, type(self)):
            if self.klass == expr.klass:
                if self.identifier == expr.identifier:
                    return True
        return False

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def klass(self):
        '''Background element selector class initialized by user.

        Return segment, measure or division class.
        '''
        return self._klass
