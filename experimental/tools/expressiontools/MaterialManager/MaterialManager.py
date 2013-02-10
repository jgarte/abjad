from abjad.tools import iotools
from abjad.tools.abctools import AbjadObject


class MaterialManager(AbjadObject):
    '''Material manager.
    '''

    ### INITIALIZER ###

    def __init__(self):
        pass

    ### PUBLIC METHODS ###

    def register_material(self, material):
        '''Register `material`.

        Change tuple or list to payload expression.

        Change parseable string to start-positioned rhythm payload expression.
        '''
        from experimental.tools import expressiontools
        if isinstance(material, (tuple, list)):
            return expressiontools.PayloadExpression(material)
        elif isinstance(material, (str)):
            component = iotools.p(material)
            return expressiontools.StartPositionedRhythmPayloadExpression([component], start_offset=0)
        else:
            raise TypeError(material)
