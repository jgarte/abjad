# -*- encoding: utf-8 -*-
from abjad.tools import pitchtools
from scoremanager import getters
from scoremanager.editors.ObjectInventoryEditor import ObjectInventoryEditor
from scoremanager.editors.OctaveTranspositionMappingEditor \
    import OctaveTranspositionMappingEditor


class OctaveTranspositionMappingInventoryEditor(ObjectInventoryEditor):
    r'''OctaveTranspositionMappingInventory editor.
    '''

    ### CLASS VARIABLES ###

    item_class = pitchtools.OctaveTranspositionMapping

    item_creator_class = OctaveTranspositionMappingEditor

    item_editor_class = OctaveTranspositionMappingEditor

    item_identifier = 'octave transposition mapping'

    ### PUBLIC PROPERTIES ###

    @property
    def target_manifest(self):
        return self.TargetManifest(
            pitchtools.OctaveTranspositionMappingInventory,
            target_attribute_name='name',
            )
