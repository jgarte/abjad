def all_are_residue_class_expressions(expr):
    '''.. versionadded:: 2.6

    True when `expr` is a sequence of Abjad residue class expressions::

        >>> from abjad.tools import sievetools

    ::

        >>> sieve = sievetools.ResidueClass(3, 0) | sievetools.ResidueClass(2, 0)

    ::

        >>> sieve
        {ResidueClass(2, 0) | ResidueClass(3, 0)}

    ::

        >>> sievetools.all_are_residue_class_expressions([sieve])
        True

    True when `expr` is an empty sequence::

        >>> sievetools.all_are_residue_class_expressions([])
        True

    Otherwise false::

        >>> sievetools.all_are_residue_class_expressions('foo')
        False

    Return boolean.
    '''
    from abjad.tools import sievetools

    return all([isinstance(x, sievetools.ResidueClassExpression) for x in expr])
