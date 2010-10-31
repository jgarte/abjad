def get_indices_of_sequence_elements_equal_to_true(sequence):
   '''Get indices of `sequence` elements equal to true::

      abjad> seqtools.get_indices_of_sequence_elements_equal_to_true([0, 0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1])
      (3, 4, 5, 9, 10, 11)

   Get indices `sequence` elements equal to true::

      abjad> seqtools.get_indices_of_sequence_elements_equal_to_true([0, 0, 0, 0, 0, 0])
      ( )

   Return newly constructed tuple.

   .. versionchanged:: 1.1.2
      renamed ``listtools.true_indices( )`` to
      ``seqtools.get_indices_of_sequence_elements_equal_to_true( )``.
   '''

   result = [ ]
   for i, x in enumerate(sequence):
      if bool(x):
         result.append(i)
   return tuple(result)
