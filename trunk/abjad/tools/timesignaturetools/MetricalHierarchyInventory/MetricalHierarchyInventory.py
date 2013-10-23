# -*- encoding: utf-8 -*-
from abjad.tools.datastructuretools.TypedList import TypedList


class MetricalHierarchyInventory(TypedList):
    r'''An ordered list of metrical hierarchies.

    ::

        >>> inventory = timesignaturetools.MetricalHierarchyInventory(
        ...     [(4, 4), (3, 4), (6, 8)])

    ::

        >>> print inventory.storage_format
        timesignaturetools.MetricalHierarchyInventory([
            timesignaturetools.MetricalHierarchy(
                '(4/4 (1/4 1/4 1/4 1/4))'
                ),
            timesignaturetools.MetricalHierarchy(
                '(3/4 (1/4 1/4 1/4))'
                ),
            timesignaturetools.MetricalHierarchy(
                '(6/8 ((3/8 (1/8 1/8 1/8)) (3/8 (1/8 1/8 1/8))))'
                )
            ])

    MetricalHierarchy inventories implement the list interface and 
    are mutable.
    '''

    ### PRIVATE PROPERTIES ##

    @property
    def _item_callable(self):
        from abjad.tools import timesignaturetools
        return timesignaturetools.MetricalHierarchy
