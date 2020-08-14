import abjad


def test_Parentage_root_01():

    tuplet = abjad.Tuplet((2, 3), "c'8 d'8 e'8")
    staff = abjad.Staff([tuplet])
    leaves = abjad.select(staff).leaves()

    assert abjad.inspectx.parentage(staff).root is staff
    assert abjad.inspectx.parentage(tuplet).root is staff
    assert abjad.inspectx.parentage(leaves[0]).root is staff
    assert abjad.inspectx.parentage(leaves[1]).root is staff
    assert abjad.inspectx.parentage(leaves[2]).root is staff
