import abjad


def test_LogicalTie_leaves_01():

    staff = abjad.Staff("c' ~ c'16")

    assert abjad.inspect(staff[0]).logical_tie().leaves == tuple(staff[:])


def test_LogicalTie_leaves_02():

    staff = abjad.Staff("c'")

    assert abjad.inspect(staff[0]).logical_tie().leaves == (staff[0],)
