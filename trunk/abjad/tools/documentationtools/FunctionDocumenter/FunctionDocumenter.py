import types
from abjad.tools.documentationtools.Documenter import Documenter


class FunctionDocumenter(Documenter):
    '''FunctionDocumenter generates an ReST entry for a given function:

    ::

        abjad> from abjad.tools.documentationtools import *

    ::

        abjad> from abjad.tools.notetools import make_notes
        abjad> documenter = FunctionDocumenter(make_notes)
        abjad> print documenter()
        notetools.make_notes
        ====================

        .. autofunction:: abjad.tools.notetools.make_notes

    Returns ``FunctionDocumenter``` instance.
    '''

    ### CLASS ATTRIBUTES ###

    __slots__ = ('_object', '_prefix')

    ### INITIALIZER ###

    def __init__(self, obj, prefix = 'abjad.tools.'):
        assert isinstance(obj, types.FunctionType)
        Documenter.__init__(self, obj, prefix)

    ### SPECIAL METHODS ###

    def __call__(self):
        '''Generate documentation.

        Returns string.
        '''

        stripped_function_name = self._shrink_module_name(self.object.__module__)
        
        result = []
        result.extend(self._format_heading(stripped_function_name, '='))
        result.append('.. autofunction:: %s' % self._object.__module__)
        result.append('')

        return '\n'.join(result)
