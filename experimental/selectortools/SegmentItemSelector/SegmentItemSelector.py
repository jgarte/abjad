from abjad.tools import durationtools
from experimental.selectortools.InequalitySelector import InequalitySelector


class SegmentItemSelector(InequalitySelector):
    r'''.. versionadded:: 1.0

    Select segment ``3``::

        >>> from experimental import *

    ::

        >>> selectortools.SegmentItemSelector(identifier=3)
        SegmentItemSelector(identifier=3)

    Select segment ``'red'``::

        >>> selectortools.SegmentItemSelector(identifier='red')
        SegmentItemSelector(identifier='red')

    Segment selectors are immutable.
    '''

    ### INITIALIZER ###

    def __init__(self, inequality=None, identifier=0):
        from experimental import specificationtools
        InequalitySelector.__init__(self, inequality=inequality)
        self._identifier = identifier
        self._klass = specificationtools.Segment

    ### SPECIAL METHODS ###

    def __eq__(self, expr):
        if isinstance(expr, type(self)):
            if self.klass == expr.klass:
                if self.identifier == expr.identifier:
                    return True
        return False

    ### READ-ONLY PROPERTIES ###

    @property
    def context_name(self):
        '''Return none.
        '''
        return

    @property
    def context_names(self):
        '''Return empty list.
        '''
        return []

    @property
    def identifier(self):
        return self._identifier

    @property
    def klass(self):
        return self._klass

    @property
    def segment_identifier(self):
        return self._identifier

    ### PUBLIC METHODS ###

    def get_duration(self, score_specification):
        segment_specification = score_specification.get_segment_specification(self)
        return segment_specification.duration

    def get_segment_start_offset(self, score_specification):
        return durationtools.Offset(0)

    def get_segment_stop_offset(self, score_specification):
        segment_specification = score_specification.get_segment_specification(self)
        return durationtools.Offset(segment_specification.duration)
