from collections import Iterable
from numbers import Number
from abjad import Fraction
from abjad.core import _Immutable
from abjad.tools.containertools import Container
from abjad.tools.contexttools import TempoMark
from abjad.tools.leaftools._Leaf import _Leaf
from abjad.tools.quantizationtools.QEvent import QEvent
from abjad.tools.quantizationtools.milliseconds_to_q_events import milliseconds_to_q_events
from abjad.tools.quantizationtools.millisecond_pitch_pairs_to_q_events import millisecond_pitch_pairs_to_q_events
from abjad.tools.quantizationtools.tempo_scaled_leaves_to_q_events import tempo_scaled_leaves_to_q_events
from abjad.tools.quantizationtools.tempo_scaled_rationals_to_q_events import tempo_scaled_rationals_to_q_events


class _Quantizer(_Immutable):

   ## OVERRIDES ##

   def __call__(self, *args, **kwargs):
      # Q-events
      if all([isinstance(x, QEvent) for x in args]):
         q_events = list(sorted(args, key = lambda x: (x.offset, x.duration)))

      # milliseconds
      elif all([isinstance(x, Number) for x in args]):
         q_events = milliseconds_to_q_events(args)

      # millisecond-pitch pairs
      elif all([isinstance(x, Iterable) for x in args]) and \
         all([len(x) == 2 for x in args]):
         q_events = millisecond_pitch_pairs_to_q_events(args)

      # tempo-scaled rationals
      elif all([isinstance(x, (int, Fraction)) for x in args]) and \
         tempo in kwargs and \
         isinstance(kwargs['tempo'], TempoMark):
         q_events = tempo_scaled_rationals_to_q_events()

      # tempo-scaled leaves
      elif len(args) == 1 and isinstance(args[0], Container):
         leaves = args[0].leaves
         if tempo in kwargs:
            q_events = tempo_scaled_leaves_to_q_events(leaves, kwargs['tempo'])
         else:
            q_events = tempo_scaled_leaves_to_q_events(leaves)

      elif 1 < len(args) and all([isinstance(x, _Leaf) for x in args]):
         leaves = args
         if tempo in kwargs:
            q_events = tempo_scaled_leaves_to_q_events(leaves, kwargs['tempo'])
         else:
            q_events = tempo_scaled_leaves_to_q_events(leaves)
         
      else:
         raise ValueError("Can't quantize from %s" % repr(args))

      if verbose in kwargs and kwargs['verbose']:
         self._quantize(q_events, verbose = True)
      else:
         self._quantize(q_events)

   def __repr__(self):
      return '%s(%s)' % (self.__class__.__name__, self._format_string)

   ## PRIVATE ATTRIBUTES ##

   @property
   def _format_string(self):
      return ' '

   ## PUBLIC METHODS ##

   def _quantize(self, q_events, verbose = False):
      return q_events, verbose
