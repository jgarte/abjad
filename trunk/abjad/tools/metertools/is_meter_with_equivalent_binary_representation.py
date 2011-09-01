from abjad.tools import durtools
from abjad.tools import mathtools


def is_meter_with_equivalent_binary_representation(expr):
    '''True when `expr` is a meter with binary-valued duration::

        abjad> from abjad.tools import metertools

    ::

        abjad> metertools.is_meter_with_equivalent_binary_representation(contexttools.TimeSignatureMark((3, 12)))
        True

    Otherwise false::

        abjad> metertools.is_meter_with_equivalent_binary_representation(contexttools.TimeSignatureMark((4, 12)))
        False

    ::

        abjad> metertools.is_meter_with_equivalent_binary_representation('text')
        False

    Return boolean.
    '''
    from abjad.tools import contexttools

    # check input
    if not isinstance(expr, contexttools.TimeSignatureMark):
        return False

    # express meter as rational and reduce to relatively prime terms
    meter_as_rational = durtools.Duration(expr.numerator, expr.denominator)

    # return True if reduced meter denominator is power of two
    return mathtools.is_nonnegative_integer_power_of_two(meter_as_rational.denominator)


