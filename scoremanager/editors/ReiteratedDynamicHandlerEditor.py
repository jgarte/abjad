# -*- encoding: utf-8 -*-
from experimental.tools import handlertools
from scoremanager import getters
from scoremanager.editors.Editor import Editor


class ReiteratedDynamicHandlerEditor(Editor):
    r'''ReiteratedDynamicHandler editor.
    '''

    ### PUBLIC PROPERTIES ###

    @property
    def target_manifest(self):
        return self.TargetManifest(
            handlertools.ReiteratedDynamicHandler,
            ('dynamic_name', None, 'dy', getters.get_dynamic, True),
            ('minimum_duration', None, 'md', getters.get_duration, True),
            )
