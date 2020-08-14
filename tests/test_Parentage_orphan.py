import abjad


def test_Parentage_orphan_01():

    staff = abjad.Staff("c'8 d'8 e'8 f'8")

    assert abjad.inspectx.parentage(staff).orphan
    for note in staff:
        assert not abjad.inspectx.parentage(note).orphan
