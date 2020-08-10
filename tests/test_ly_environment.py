import abjad


def test_ly_environment_01():

    assert abjad.lyscrape.contexts is not None
    print(abjad.lyscrape.contexts)

    assert abjad.lyscrape.current_module is not None
    print(abjad.lyscrape.current_module)

    assert abjad.lyscrape.engravers is not None
    print(abjad.lyscrape.engravers)

    assert abjad.lyscrape.grob_interfaces is not None
    print(abjad.lyscrape.grob_interfaces)

    assert abjad.lyscrape.interface_properties is not None
    print(abjad.lyscrape.interface_properties)

    assert abjad.lyscrape.language_pitch_names is not None
    print(abjad.lyscrape.language_pitch_names)

    assert abjad.lyscrape.markup_functions is not None
    print(abjad.lyscrape.markup_functions)

    assert abjad.lyscrape.markup_list_functions is not None
    print(abjad.lyscrape.markup_list_functions)

    assert abjad.lyscrape.music_glyphs is not None
    print(abjad.lyscrape.music_glyphs)
