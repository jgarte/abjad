from abjad.helpers.transfer_all_attributes import _transfer_all_attributes
from abjad.helpers.duration_token_unpack import _duration_token_unpack
from abjad.helpers.leaf_scale import leaf_scale, leaf_scale_binary
from abjad.leaf.leaf import _Leaf
from abjad.rational.rational import Rational


def leaf_split(split_dur, leaf):
   assert isinstance(leaf, _Leaf)
   split_dur = Rational(*_duration_token_unpack(split_dur))
   #unprolated_split_dur = leaf.duration - split_dur / leaf.duration.prolation
   unprolated_split_dur = split_dur / leaf.duration.prolation
   #print unprolated_split_dur

   #prolated_leaf_duration = leaf.duration.prolated
   #if split_dur == 0 or split_dur >= prolated_leaf_duration:
   #if split_dur == 0 or split_dur >= leaf.duration:
   if unprolated_split_dur == 0 or \
      unprolated_split_dur >= leaf.duration.written:
      return [leaf]
   else:
      l1 = leaf.copy()
      parent = leaf._parent
      if parent:
         #l1.spanners.die() ### only kill spanners if there's a parent?
         l1.spanners.clear() ### only kill spanners if there's a parent?
         indx = parent.index(leaf)
         parent.embed(indx, l1)

      l1 = leaf_scale(unprolated_split_dur, l1)
      #l2 = leaf_scale(prolated_leaf_duration - split_dur, leaf)
      #l2 = leaf_scale(leaf.duration.prolated - split_dur, leaf)
      #l2 = leaf_scale(leaf.duration - unprolated_split_dur, leaf)
      l2 = leaf_scale(leaf.duration.written - unprolated_split_dur, leaf)
      return [l1, l2]


def leaf_split_binary(split_dur, leaf):
   assert isinstance(leaf, _Leaf)
   split_dur = Rational(*_duration_token_unpack(split_dur))
   unprolated_split_dur = split_dur / leaf.duration.prolation
   ### TODO: check it unprolated_split_dur is m / 2**n?
   if unprolated_split_dur == 0 or \
      unprolated_split_dur >= leaf.duration.written:
      return [leaf]
   else:
      l1 = leaf.copy()
      ### remove afterGrace from l1 and Grace from leaf (l2)
      l1.grace.after = None
      leaf.grace.before = None
      parent = leaf._parent
      ### remove articulations and dynamics
      leaf.articulations = None
      leaf.dynamics = None
      if parent:
         #l1.spanners.die() 
         l1.spanners.clear() 
         ### if l1 is the only leaf spanned, spanner dies for ever...
         indx = parent.index(leaf)
         parent.embed(indx, l1)
      l1 = leaf_scale_binary(unprolated_split_dur, l1)
      #l2 = leaf_scale_binary(leaf.duration - unprolated_split_dur, leaf)
      l2 = leaf_scale_binary(leaf.duration.written - unprolated_split_dur, leaf)

      result = [ ] 
      #if isinstance(l1, list): result.extend(l1)
      #else: result.append(l1)
      #if isinstance(l2, list): result.extend(l2)
      #else: result.append(l2)
      result.append(l1)
      result.append(l2)
      return result
