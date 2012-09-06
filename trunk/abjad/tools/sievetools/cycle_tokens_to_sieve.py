def cycle_tokens_to_sieve(*cycle_tokens):
    '''.. versionadded:: 2.0

    Make Xenakis sieve from arbitrarily many `cycle_tokens`::

        >>> from abjad.tools import sievetools

    ::

        >>> cycle_token_1 = (6, [0, 4, 5])
        >>> cycle_token_2 = (10, [0, 1, 2], 6)
        >>> sievetools.cycle_tokens_to_sieve(cycle_token_1, cycle_token_2)
        {ResidueClass(6, 0) | ResidueClass(6, 4) | ResidueClass(6, 5) | 
         ResidueClass(10, 6) | ResidueClass(10, 7) | ResidueClass(10, 8)}

    Cycle token comprises mandatory `modulo`, mandatory `residues` and optional `offset`.
    '''
    from abjad.tools import sievetools
    from abjad.tools.sievetools._cycle_token_to_sieve import _cycle_token_to_sieve

    sieves = []
    for cycle_token in cycle_tokens:
        sieve = _cycle_token_to_sieve(cycle_token)
        sieves.append(sieve)

    if sieves:
        cur_sieve = sieves[0]
        for sieve in sieves[1:]:
            cur_sieve = cur_sieve | sieve
    else:
        cur_sieve = sievetools.ResidueClassExpression([])

    return cur_sieve
