import typing

from . import tags as abjad_tags
from . import typings
from .bundle import LilyPondFormatBundle
from .duration import Offset
from .overrides import OverrideInterface
from .path import Path
from .score import Context
from .storage import FormatSpecification, StorageFormatManager
from .stringx import String
from .tag import Tag, activate, deactivate

token_type = typing.Union[None, int, typings.IntegerPair, typing.List[int]]

callable_type = typing.Union[str, typing.Callable, None]
activation_type = typing.Tuple[callable_type, str]


class Job:
    """
    Job.
    """

    ### CLASS VARIABLES ###

    __slots__ = (
        "_activate",
        "_deactivate",
        "_deactivate_first",
        "_message_zero",
        "_path",
        "_prepend_empty_chord",
        "_skip_file_name",
        "_title",
    )

    ### INITIALIZER ###

    def __init__(
        self,
        *,
        activate: activation_type = None,
        deactivate: activation_type = None,
        deactivate_first: bool = None,
        message_zero: bool = None,
        path: Path = None,
        prepend_empty_chord: bool = None,
        skip_file_name: str = None,
        title: str = None,
    ) -> None:
        self._activate = activate
        self._deactivate = deactivate
        self._deactivate_first = deactivate_first
        self._message_zero = message_zero
        self._path = path
        self._prepend_empty_chord = prepend_empty_chord
        self._skip_file_name = skip_file_name
        self._title = title

    ### SPECIAL METHODS ###

    def __call__(self) -> typing.List[String]:
        """
        Calls job on job ``path``.
        """
        messages = []
        if self.title is not None:
            messages.append(String(self.title).capitalize_start())
        total_count = 0
        if isinstance(self.path, str):
            text = self.path
        if self.deactivate_first is True:
            if self.deactivate is not None:
                assert isinstance(self.deactivate, tuple)
                match, name = self.deactivate
                if match is not None:
                    if isinstance(self.path, Path):
                        result = self.path.deactivate(
                            match,
                            indent=1,
                            message_zero=True,
                            name=name,
                            prepend_empty_chord=self.prepend_empty_chord,
                            skip_file_name=self.skip_file_name,
                        )
                        assert result is not None
                        count, skipped, messages_ = result
                        messages.extend(messages_)
                        total_count += count
                    else:
                        assert isinstance(self.path, str)
                        result = deactivate(
                            text,
                            match,
                            prepend_empty_chord=self.prepend_empty_chord,
                            skip_file_name=self.skip_file_name,
                            skipped=True,
                        )
                        assert result is not None
                        text, count, skipped = result
        if self.activate is not None:
            assert isinstance(self.activate, tuple)
            match, name = self.activate
            if match is not None:
                if isinstance(self.path, Path):
                    result = self.path.activate(
                        match,
                        indent=1,
                        message_zero=True,
                        name=name,
                        skip_file_name=self.skip_file_name,
                    )
                    assert result is not None
                    count, skipped, messages_ = result
                    messages.extend(messages_)
                    total_count += count
                else:
                    assert isinstance(self.path, str)
                    text, count, skipped = activate(
                        text, match, skip_file_name=self.skip_file_name, skipped=True,
                    )
        if self.deactivate_first is not True:
            if self.deactivate is not None:
                assert isinstance(self.deactivate, tuple)
                match, name = self.deactivate
                if match is not None:
                    if isinstance(self.path, Path):
                        result = self.path.deactivate(
                            match,
                            indent=1,
                            message_zero=True,
                            name=name,
                            prepend_empty_chord=self.prepend_empty_chord,
                            skip_file_name=self.skip_file_name,
                        )
                        assert result is not None
                        count, skipped, messages_ = result
                        messages.extend(messages_)
                        total_count += count
                    else:
                        assert isinstance(self.path, str)
                        text, count, skipped = deactivate(
                            text,
                            match,
                            prepend_empty_chord=self.prepend_empty_chord,
                            skip_file_name=self.skip_file_name,
                            skipped=True,
                        )
        if total_count == 0 and not self.message_zero:
            messages = []
        if isinstance(self.path, Path):
            return messages
        else:
            assert isinstance(self.path, str)
            return text

    def __repr__(self) -> str:
        """
        Gets interpreter representation.
        """
        return StorageFormatManager(self).get_repr_format()

    ### PUBLIC PROPERTIES ###

    @property
    def activate(self):
        """
        Gets activate match / message pair.
        """
        return self._activate

    @property
    def deactivate(self):
        """
        Gets deactivate match / message pair.
        """
        return self._deactivate

    @property
    def deactivate_first(self) -> typing.Optional[bool]:
        """
        Is true when deactivate runs first.
        """
        return self._deactivate_first

    @property
    def message_zero(self) -> typing.Optional[bool]:
        """
        Is true when job returns messages even when no matches are found.
        """
        return self._message_zero

    @property
    def path(self) -> typing.Optional[Path]:
        """
        Gets path.
        """
        return self._path

    @property
    def prepend_empty_chord(self) -> typing.Optional[bool]:
        """
        Is true when deactivate prepends LilyPond empty chord ``<>`` command.
        """
        return self._prepend_empty_chord

    @property
    def skip_file_name(self) -> typing.Optional[str]:
        """
        Gets skip file name.
        """
        return self._skip_file_name

    @property
    def title(self) -> typing.Optional[str]:
        """
        Gets title.
        """
        return self._title

    ### PUBLIC METHODS ###

    @staticmethod
    def color_clefs(path, undo=False) -> "Job":
        """
        Colors clefs.
        """
        name = "clef color"

        def match(tags):
            tags_ = abjad_tags.clef_color_tags(path)
            return bool(set(tags) & set(tags_))

        if undo:
            return Job(
                deactivate=(match, name), path=path, title="uncoloring clefs ...",
            )
        else:
            return Job(activate=(match, name), path=path, title="coloring clefs ...")

    @staticmethod
    def color_dynamics(path, undo=False) -> "Job":
        """
        Colors dynamics.
        """
        name = "dynamic color"

        def match(tags):
            tags_ = abjad_tags.dynamic_color_tags(path)
            return bool(set(tags) & set(tags_))

        if undo:
            return Job(
                deactivate=(match, name), path=path, title="uncoloring dynamics ...",
            )
        else:
            return Job(
                activate=(match, name), path=path, title="coloring dynamics ...",
            )

    @staticmethod
    def color_instruments(path, undo=False) -> "Job":
        """
        Colors instruments.
        """
        name = "instrument color"

        def match(tags):
            tags_ = abjad_tags.instrument_color_tags(path)
            return bool(set(tags) & set(tags_))

        if undo:
            return Job(
                deactivate=(match, name), path=path, title="uncoloring instruments ...",
            )
        else:
            return Job(
                activate=(match, name), path=path, title="coloring instruments ...",
            )

    @staticmethod
    def color_margin_markup(path, undo=False) -> "Job":
        """
        Colors margin markup.
        """
        name = "margin markup color"

        def match(tags):
            tags_ = abjad_tags.margin_markup_color_tags(path)
            return bool(set(tags) & set(tags_))

        if undo:
            return Job(
                deactivate=(match, name),
                path=path,
                title="uncoloring margin markup ...",
            )
        else:
            return Job(
                activate=(match, name), path=path, title="coloring margin markup ...",
            )

    @staticmethod
    def color_metronome_marks(path, undo=False) -> "Job":
        """
        Colors metronome marks.
        """

        def activate(tags):
            tags_ = abjad_tags.metronome_mark_color_expression_tags(path)
            return bool(set(tags) & set(tags_))

        def deactivate(tags):
            tags_ = abjad_tags.metronome_mark_color_suppression_tags(path)
            return bool(set(tags) & set(tags_))

        if undo:
            return Job(
                activate=(deactivate, "metronome mark color suppression"),
                deactivate=(activate, "metronome mark color expression"),
                path=path,
                title="uncoloring metronome marks ...",
            )
        else:
            return Job(
                activate=(activate, "metronome mark color expression"),
                deactivate=(deactivate, "metronome mark color suppression"),
                path=path,
                title="coloring metronome marks ...",
            )

    @staticmethod
    def color_persistent_indicators(path, undo=False) -> "Job":
        """
        Color persistent indicators.
        """
        name = "persistent indicator"
        activate_name = "persistent indicator color expression"

        def activate(tags):
            tags_ = abjad_tags.persistent_indicator_color_expression_tags(path)
            return bool(set(tags) & set(tags_))

        deactivate_name = "persistent indicator color suppression"

        def deactivate(tags):
            tags_ = abjad_tags.persistent_indicator_color_suppression_tags(path)
            return bool(set(tags) & set(tags_))

        if undo:
            return Job(
                activate=(deactivate, deactivate_name),
                deactivate=(activate, activate_name),
                path=path,
                title=f"uncoloring {name}s ...",
            )
        else:
            return Job(
                activate=(activate, activate_name),
                deactivate=(deactivate, deactivate_name),
                path=path,
                title=f"coloring {name}s ...",
            )

    @staticmethod
    def color_staff_lines(path, undo=False) -> "Job":
        """
        Colors staff lines.
        """
        name = "staff lines color"

        def match(tags):
            tags_ = abjad_tags.staff_lines_color_tags(path)
            return bool(set(tags) & set(tags_))

        if undo:
            return Job(
                deactivate=(match, name), path=path, title="uncoloring staff lines ...",
            )
        else:
            return Job(
                activate=(match, name), path=path, title="coloring staff lines ...",
            )

    @staticmethod
    def color_stage_number_markup(path, undo=False) -> "Job":
        """
        Colors stage number markup.
        """
        name = "stage number markup"

        def match(tags) -> bool:
            tags_ = [abjad_tags.STAGE_NUMBER]
            return bool(set(tags) & set(tags_))

        if undo:
            return Job(deactivate=(match, name), path=path, title=f"hiding {name} ...")
        else:
            return Job(activate=(match, name), path=path, title=f"showing {name} ...")

    @staticmethod
    def color_time_signatures(path, undo=False) -> "Job":
        """
        Colors time signatures.
        """
        name = "time signature color"

        def match(tags):
            tags_ = abjad_tags.time_signature_color_tags(path)
            return bool(set(tags) & set(tags_))

        if undo:
            return Job(
                deactivate=(match, name),
                path=path,
                title="uncoloring time signatures ...",
            )
        else:
            return Job(
                activate=(match, name), path=path, title="coloring time signatures ...",
            )

    @staticmethod
    def handle_edition_tags(path) -> "Job":
        """
        Handles edition tags.

        The logic here is important:

            * deactivations run first:

                -TAG (where TAG is either my directory or my buildtype)

                +TAG (where TAG is neither my directory nor my buildtype)

            * activations run afterwards:

                TAG_SET such that there exists at least one build-forbid
                    -TAG (equal to neither my directory nor my buildtype) in
                    TAG_SET and such that there exists no -TAG (equal to either
                    my directory or my buildtype) in TAG_SET

                +TAG (where TAG is either my directory or my buildtype)

            Notionally: first we deactivate anything that is tagged EITHER
            specifically against me OR specifically for another build; then we
            activate anything that is deactivated for editions other than me;
            then we activate anything is tagged specifically for me.

        ..  todo: Tests.

        """
        if path.parent.is_segment():
            my_name = "SEGMENT"
        elif path.is_score_build() or path.parent.is_score_build():
            my_name = "SCORE"
        elif path.is_parts() or path.is_part():
            my_name = "PARTS"
        else:
            raise Exception(path)
        this_edition = Tag(f"+{String(my_name).to_shout_case()}")
        not_this_edition = Tag(f"-{String(my_name).to_shout_case()}")
        if path.is_dir():
            directory_name = path.name
        else:
            directory_name = path.parent.name
        this_directory = Tag(f"+{String(directory_name).to_shout_case()}")
        not_this_directory = Tag(f"-{String(directory_name).to_shout_case()}")

        def deactivate(tags) -> bool:
            if not_this_edition in tags:
                return True
            if not_this_directory in tags:
                return True
            for tag in tags:
                if str(tag).startswith("+"):
                    return True
            return False

        def activate(tags) -> bool:
            for tag in tags:
                if tag in [not_this_edition, not_this_directory]:
                    return False
            for tag in tags:
                if str(tag).startswith("-"):
                    return True
            return bool(set(tags) & set([this_edition, this_directory]))

        return Job(
            activate=(activate, "this-edition"),
            deactivate=(deactivate, "other-edition"),
            deactivate_first=True,
            path=path,
            title="handling edition tags ...",
        )

    @staticmethod
    def handle_fermata_bar_lines(path) -> "Job":
        """
        Handles fermata bar lines.
        """
        if path.is__segments():
            path = path.parent

        def activate(tags):
            return bool(set(tags) & set([abjad_tags.FERMATA_MEASURE]))

        deactivate: typing.Optional[callable_type]
        # then deactivate non-EOL tags:
        bol_measure_numbers = path.get_metadatum("bol_measure_numbers")
        if bol_measure_numbers:
            eol_measure_numbers = [_ - 1 for _ in bol_measure_numbers[1:]]
            final_measure_number = path.get_metadatum("final_measure_number")
            if final_measure_number is not None:
                eol_measure_numbers.append(final_measure_number)
            eol_measure_numbers = [Tag(f"MEASURE_{_}") for _ in eol_measure_numbers]

            def deactivate(tags):
                if abjad_tags.FERMATA_MEASURE in tags:
                    if not bool(set(tags) & set(eol_measure_numbers)):
                        return True
                return False

        else:
            deactivate = None
        return Job(
            activate=(activate, "bar line adjustment"),
            deactivate=(deactivate, "EOL fermata bar line"),
            path=path,
            title="handling fermata bar lines ...",
        )

    @staticmethod
    def handle_mol_tags(path) -> "Job":
        """
        Handles MOL (middle-of-line) tags.
        """
        if path.is__segments():
            path = path.parent

        # activate all middle-of-line tags
        def activate(tags):
            tags_ = set([abjad_tags.NOT_MOL, abjad_tags.ONLY_MOL])
            return bool(set(tags) & tags_)

        deactivate: typing.Optional[callable_type]
        # then deactivate conflicting middle-of-line tags
        bol_measure_numbers = path.get_metadatum("bol_measure_numbers")
        if bol_measure_numbers:
            nonmol_measure_numbers = bol_measure_numbers[:]
            final_measure_number = path.get_metadatum("final_measure_number")
            if final_measure_number is not None:
                nonmol_measure_numbers.append(final_measure_number + 1)
            nonmol_measure_numbers = [
                Tag(f"MEASURE_{_}") for _ in nonmol_measure_numbers
            ]

            def deactivate(tags):
                if abjad_tags.NOT_MOL in tags:
                    if not bool(set(tags) & set(nonmol_measure_numbers)):
                        return True
                if abjad_tags.ONLY_MOL in tags:
                    if bool(set(tags) & set(nonmol_measure_numbers)):
                        return True
                return False

        else:
            deactivate = None
        return Job(
            activate=(activate, "MOL"),
            deactivate=(deactivate, "conflicting MOL"),
            path=path,
            title="handling MOL tags ...",
        )

    @staticmethod
    def handle_shifted_clefs(path) -> "Job":
        """
        Handles shifted clefs.
        """

        def activate(tags):
            return abjad_tags.SHIFTED_CLEF in tags

        deactivate: typing.Optional[typing.Callable]
        # then deactivate shifted clefs at BOL:
        if path.is__segments():
            metadata_source = path.parent
        else:
            metadata_source = path
        string = "bol_measure_numbers"
        bol_measure_numbers = metadata_source.get_metadatum(string)
        if bol_measure_numbers:
            bol_measure_numbers = [Tag(f"MEASURE_{_}") for _ in bol_measure_numbers]

            def deactivate(tags):
                if abjad_tags.SHIFTED_CLEF not in tags:
                    return False
                if any(_ in tags for _ in bol_measure_numbers):
                    return True
                return False

        else:
            deactivate = None
        return Job(
            activate=(activate, "shifted clef"),
            deactivate=(deactivate, "BOL clef"),
            path=path,
            title="handling shifted clefs ...",
        )

    @staticmethod
    def hide_default_clefs(path, undo=False) -> "Job":
        """
        Hides default clefs.
        """
        name = "default clef"

        def match(tags):
            tags_ = [abjad_tags.DEFAULT_CLEF]
            return bool(set(tags) & set(tags_))

        if undo:
            return Job(
                activate=(match, name), path=path, title="showing default clefs ...",
            )
        else:
            return Job(
                deactivate=(match, name), path=path, title="hiding default clefs ...",
            )

    @staticmethod
    def join_broken_spanners(path) -> "Job":
        """
        Joins broken spanners.
        """

        def activate(tags):
            tags_ = [abjad_tags.SHOW_TO_JOIN_BROKEN_SPANNERS]
            return bool(set(tags) & set(tags_))

        def deactivate(tags):
            tags_ = [abjad_tags.HIDE_TO_JOIN_BROKEN_SPANNERS]
            return bool(set(tags) & set(tags_))

        return Job(
            activate=(activate, "broken spanner expression"),
            deactivate=(deactivate, "broken spanner suppression"),
            path=path,
            title="joining broken spanners ...",
        )

    @staticmethod
    def show_clock_time_markup(path, undo=False) -> "Job":
        """
        Makes clock time markup job.
        """
        name = "clock time markup"

        def match(tags) -> bool:
            tags_ = [abjad_tags.CLOCK_TIME]
            return bool(set(tags) & set(tags_))

        if undo:
            return Job(deactivate=(match, name), path=path, title=f"hiding {name} ...")
        else:
            return Job(activate=(match, name), path=path, title=f"showing {name} ...")

    @staticmethod
    def show_figure_name_markup(path, undo=False) -> "Job":
        """
        Shows figure name markup.
        """
        name = "figure name markup"

        def match(tags) -> bool:
            tags_ = [abjad_tags.FIGURE_NAME]
            return bool(set(tags) & set(tags_))

        if undo:
            return Job(deactivate=(match, name), path=path, title=f"hiding {name} ...")
        else:
            return Job(activate=(match, name), path=path, title=f"showing {name} ...")

    @staticmethod
    def show_local_measure_number_markup(path, undo=False) -> "Job":
        """
        Shows local measure number markup.
        """
        name = "local measure number markup"

        def match(tags) -> bool:
            tags_ = [abjad_tags.LOCAL_MEASURE_NUMBER]
            return bool(set(tags) & set(tags_))

        if undo:
            return Job(deactivate=(match, name), path=path, title=f"hiding {name} ...")
        else:
            return Job(activate=(match, name), path=path, title=f"showing {name} ...")

    @staticmethod
    def show_measure_number_markup(path, undo=False) -> "Job":
        """
        Shows measure number markup.
        """
        name = "measure number markup"

        def match(tags) -> bool:
            tags_ = [abjad_tags.MEASURE_NUMBER]
            return bool(set(tags) & set(tags_))

        if undo:
            return Job(deactivate=(match, name), path=path, title=f"hiding {name} ...")
        else:
            return Job(activate=(match, name), path=path, title=f"showing {name} ...")

    @staticmethod
    def show_music_annotations(path, undo=False) -> "Job":
        """
        Shows music annotations.
        """
        name = "music annotation"

        def match(tags) -> bool:
            tags_ = abjad_tags.music_annotation_tags()
            return bool(set(tags) & set(tags_))

        def match_2(tags) -> bool:
            tags_ = [abjad_tags.INVISIBLE_MUSIC_COMMAND]
            return bool(set(tags) & set(tags_))

        if undo:
            return Job(
                activate=(match_2, name),
                deactivate=(match, name),
                path=path,
                title=f"hiding {name}s ...",
            )
        else:
            return Job(
                activate=(match, name),
                deactivate=(match_2, name),
                path=path,
                title=f"showing {name}s ...",
            )

    @staticmethod
    def show_spacing_markup(path, undo=False) -> "Job":
        """
        Shows spacing markup.
        """
        name = "spacing markup"

        def match(tags) -> bool:
            tags_ = abjad_tags.spacing_markup_tags()
            return bool(set(tags) & set(tags_))

        if undo:
            return Job(deactivate=(match, name), path=path, title=f"hiding {name} ...")
        else:
            return Job(activate=(match, name), path=path, title=f"showing {name} ...")

    @staticmethod
    def show_tag(
        path,
        tag,
        *,
        match=None,
        prepend_empty_chord=None,
        skip_file_name=None,
        undo=False,
    ) -> "Job":
        """
        Shows tag.
        """
        if isinstance(tag, str):
            assert match is not None, repr(match)
        else:
            assert isinstance(tag, Tag), repr(tag)
        name = str(tag)

        if match is None:

            def match(tags) -> bool:
                tags_ = [tag]
                return bool(set(tags) & set(tags_))

        if undo:
            return Job(
                deactivate=(match, name),
                path=path,
                prepend_empty_chord=prepend_empty_chord,
                skip_file_name=skip_file_name,
                title=f"hiding {name} tags ...",
            )
        else:
            return Job(
                activate=(match, name),
                path=path,
                skip_file_name=skip_file_name,
                title=f"showing {name} tags ...",
            )


class Momento:
    """
    Momento.
    """

    ### CLASS VARIABLES ###

    __slots__ = (
        "_context",
        "_edition",
        "_manifest",
        "_prototype",
        "_synthetic_offset",
        "_value",
    )

    ### INITIALIZER ###

    def __init__(
        self,
        context: str = None,
        edition: typing.Union[str, Tag] = None,
        manifest: str = None,
        prototype: str = None,
        synthetic_offset: Offset = None,
        value: typing.Any = None,
    ) -> None:
        if context is not None:
            assert isinstance(context, str), repr(context)
        self._context = context
        edition_ = None
        if edition is not None:
            edition_ = Tag(edition)
        self._edition = edition_
        if manifest is not None:
            assert isinstance(manifest, str), repr(manifest)
            assert prototype is None
        self._manifest = manifest
        if prototype is not None:
            assert isinstance(prototype, str), repr(prototype)
            assert manifest is None
        self._prototype = prototype
        if synthetic_offset is not None:
            assert isinstance(synthetic_offset, Offset), repr(synthetic_offset)
        self._synthetic_offset = synthetic_offset
        if value is not None:
            if not isinstance(value, (int, str, dict)):
                assert type(value).__name__ == "PersistentOverride", repr(value)
        self._value = value

    ### SPECIAL METHODS ###

    def __repr__(self) -> str:
        """
        Gets interpreter representation.
        """
        return StorageFormatManager(self).get_repr_format()

    ### PRIVATE METHODS###

    def _get_format_specification(self):
        return FormatSpecification(client=self)

    ### PUBLIC PROPERTIES ###

    @property
    def context(self) -> typing.Optional[str]:
        """
        Gets (name of local) context.
        """
        return self._context

    @property
    def edition(self) -> typing.Optional[Tag]:
        """
        Gets edition.
        """
        return self._edition

    @property
    def manifest(self) -> typing.Optional[str]:
        """
        Gets manifest.
        """
        return self._manifest

    @property
    def prototype(self) -> typing.Optional[str]:
        """
        Gets prototype.
        """
        return self._prototype

    @property
    def synthetic_offset(self) -> typing.Optional[Offset]:
        """
        Gets synthetic offset.
        """
        return self._synthetic_offset

    @property
    def value(self) -> typing.Union[int, str]:
        """
        Gets value.
        """
        return self._value


class Part:
    """
    Part.

    ..  container:: example

        >>> part = abjad.Part(
        ...     member=18,
        ...     section='FirstViolin',
        ...     section_abbreviation='VN-1',
        ...     )

        >>> abjad.f(part)
        abjad.Part(
            instrument='FirstViolin',
            member=18,
            section='FirstViolin',
            section_abbreviation='VN-1',
            )

    """

    ### CLASS VARIABLES ###

    __slots__ = (
        "_section_abbreviation",
        "_instrument",
        "_member",
        "_name",
        "_number",
        "_section",
        "_zfill",
    )

    ### INITIALIZER ###

    def __init__(
        self,
        instrument: str = None,
        member: int = None,
        number: int = None,
        section: str = None,
        section_abbreviation: str = None,
        zfill: int = None,
    ) -> None:
        instrument = instrument or section
        if instrument is not None:
            if not isinstance(instrument, str):
                message = "instrument must be string"
                message += f" (not {instrument!r})."
                raise Exception(message)
        self._instrument = instrument
        if member is not None:
            if not isinstance(member, int):
                message = "member must be integer"
                message += f" (not {member!r})."
                raise Exception(message)
        self._member = member
        if number is not None:
            assert isinstance(number, int), repr(number)
            assert 1 <= number, repr(number)
        self._number = number
        if section is not None:
            if not isinstance(section, str):
                raise Exception(f"section must be string (not {section!r}).")
        self._section = section
        if section_abbreviation is not None:
            if not isinstance(section_abbreviation, str):
                message = "section_abbreviation must be string"
                message += f" (not {section_abbreviation!r})."
                raise Exception(message)
        self._section_abbreviation = section_abbreviation
        if zfill is not None:
            assert isinstance(zfill, int), repr(zfill)
            assert 1 <= zfill, repr(zfill)
        self._zfill = zfill
        if member is not None:
            member_ = str(member)
            if self.zfill is not None:
                member_ = member_.zfill(self.zfill)
            name: typing.Optional[str] = f"{section}{member_}"
        else:
            name = section
        self._name = name

    ### SPECIAL METHODS ###

    def __eq__(self, argument) -> bool:
        """
        Is true when ``argument`` is a part with the same section and
        member as this part.

        ..  container:: example

            >>> part_1 = abjad.Part(
            ...     member=18,
            ...     section='FirstViolin',
            ...     section_abbreviation='VN-1',
            ...     )
            >>> part_2 = abjad.Part(
            ...     member=18,
            ...     section='FirstViolin',
            ...     section_abbreviation='VN-1',
            ...     )
            >>> part_3 = abjad.Part(
            ...     member=18,
            ...     section='SecondViolin',
            ...     section_abbreviation='VN-2',
            ...     )

            >>> part_1 == part_1
            True
            >>> part_1 == part_2
            True
            >>> part_1 == part_3
            False

            >>> part_2 == part_1
            True
            >>> part_2 == part_2
            True
            >>> part_2 == part_3
            False

            >>> part_3 == part_1
            False
            >>> part_3 == part_2
            False
            >>> part_3 == part_3
            True

        """
        if isinstance(argument, type(self)):
            if argument.section == self.section:
                return argument.member == self.member
        return False

    def __hash__(self):
        """
        Hashes part.
        """
        return super().__hash__()

    def __repr__(self) -> str:
        """
        Gets interpreter representation.
        """
        return StorageFormatManager(self).get_repr_format()

    ### PUBLIC PROPERTIES ###

    @property
    def identifier(self) -> str:
        """
        Gets identifier.

        ..  container:: example

            >>> part = abjad.Part(
            ...     instrument='Violin',
            ...     member=18,
            ...     section='FirstViolin',
            ...     section_abbreviation='VN-1',
            ...     )

            >>> part.identifier
            'VN-1-18'

        """
        assert isinstance(self.section_abbreviation, str)
        if self.member is None:
            return self.section_abbreviation
        else:
            assert isinstance(self.member, int)
            return f"{self.section_abbreviation}-{self.member}"

    @property
    def instrument(self) -> typing.Optional[str]:
        """
        Gets instrument.

        ..  container:: example

            >>> part = abjad.Part(
            ...     instrument='Violin',
            ...     member=18,
            ...     section='FirstViolin',
            ...     section_abbreviation='VN-1',
            ...     )

            >>> part.instrument
            'Violin'

        """
        return self._instrument

    @property
    def member(self) -> typing.Optional[int]:
        """
        Gets member.

        ..  container:: example

            >>> part = abjad.Part(
            ...     instrument='Violin',
            ...     member=18,
            ...     section='FirstViolin',
            ...     section_abbreviation='VN-1',
            ...     )

            >>> part.member
            18

        """
        return self._member

    @property
    def name(self) -> typing.Optional[str]:
        """
        Gets name.

        ..  container:: example

            >>> part = abjad.Part(
            ...     instrument='Violin',
            ...     member=1,
            ...     section='FirstViolin',
            ...     section_abbreviation='VN-1',
            ...     )

            >>> part.name
            'FirstViolin1'

            >>> part = abjad.Part(
            ...     instrument='Violin',
            ...     member=1,
            ...     zfill=2,
            ...     section='FirstViolin',
            ...     section_abbreviation='VN-1',
            ...     )

            >>> part.name
            'FirstViolin01'

        """
        return self._name

    @property
    def number(self) -> typing.Optional[int]:
        """
        Gets number.

        ..  container:: example

            >>> part = abjad.Part(
            ...     instrument='Violin',
            ...     member=18,
            ...     number=107,
            ...     section='FirstViolin',
            ...     section_abbreviation='VN-1',
            ...     )

            >>> part.number
            107

        """
        return self._number

    @property
    def section(self) -> typing.Optional[str]:
        """
        Gets section.

        ..  container:: example

            >>> part = abjad.Part(
            ...     instrument='Violin',
            ...     member=18,
            ...     section='FirstViolin',
            ...     section_abbreviation='VN-1',
            ...     )

            >>> part.section
            'FirstViolin'

        """
        return self._section

    @property
    def section_abbreviation(self) -> typing.Optional[str]:
        """
        Gets section_abbreviation.

        ..  container:: example

            >>> part = abjad.Part(
            ...     instrument='Violin',
            ...     member=18,
            ...     section='FirstViolin',
            ...     section_abbreviation='VN-1',
            ...     )

            >>> part.section_abbreviation
            'VN-1'

        """
        return self._section_abbreviation

    @property
    def zfill(self) -> typing.Optional[int]:
        """
        Gets zfill.

        ..  container:: example

            >>> part = abjad.Part(
            ...     instrument='Violin',
            ...     member=9,
            ...     number=99,
            ...     section='FirstViolin',
            ...     section_abbreviation='VN-1',
            ...     zfill=2,
            ...     )

            >>> part.zfill
            2

            >>> str(part.member).zfill(part.zfill)
            '09'

        """
        return self._zfill


class PartAssignment:
    """
    Part assignment.

    ..  container:: example

        >>> abjad.PartAssignment('Horn')
        PartAssignment('Horn')

        >>> abjad.PartAssignment('Horn', 1)
        PartAssignment('Horn', 1)

        >>> abjad.PartAssignment('Horn', 2)
        PartAssignment('Horn', 2)

        >>> abjad.PartAssignment('Horn', (3, 4))
        PartAssignment('Horn', (3, 4))

        >>> abjad.PartAssignment('Horn', [1, 3])
        PartAssignment('Horn', [1, 3])

    ..  container:: example

        >>> part_assignment = abjad.PartAssignment('Horn', [1, 3])

        >>> print(abjad.storage(part_assignment))
        abjad.PartAssignment('Horn', [1, 3])

    """

    ### CLASS VARIABLES ###

    __slots__ = ("_members", "_parts", "_section", "_token")

    ### INITIALIZER ###

    def __init__(self, section: str = None, token: token_type = None) -> None:
        self._section = section
        if token is not None:
            assert self._is_token(token), repr(token)
        self._token = token
        members = self._expand_members(token)
        self._members = members
        parts = self._expand_parts()
        assert isinstance(parts, list), repr(parts)
        self._parts = parts

    ### SPECIAL METHODS ###

    def __contains__(self, part: Part) -> bool:
        """
        Is true when part assignment contains ``part``.

        ..  container:: example

            >>> parts = [
            ...     abjad.Part(section='Horn', member= 1),
            ...     abjad.Part(section='Horn', member= 2),
            ...     abjad.Part(section='Horn', member= 3),
            ...     abjad.Part(section='Horn', member= 4),
            ...     ]

            >>> part_assignment = abjad.PartAssignment('Horn')
            >>> for part in parts:
            ...     part, part in part_assignment
            ...
            (Part(instrument='Horn', member=1, section='Horn'), True)
            (Part(instrument='Horn', member=2, section='Horn'), True)
            (Part(instrument='Horn', member=3, section='Horn'), True)
            (Part(instrument='Horn', member=4, section='Horn'), True)

            >>> part_assignment = abjad.PartAssignment('Horn', 1)
            >>> for part in parts:
            ...     part, part in part_assignment
            ...
            (Part(instrument='Horn', member=1, section='Horn'), True)
            (Part(instrument='Horn', member=2, section='Horn'), False)
            (Part(instrument='Horn', member=3, section='Horn'), False)
            (Part(instrument='Horn', member=4, section='Horn'), False)

            >>> part_assignment = abjad.PartAssignment('Horn', 2)
            >>> for part in parts:
            ...     part, part in part_assignment
            ...
            (Part(instrument='Horn', member=1, section='Horn'), False)
            (Part(instrument='Horn', member=2, section='Horn'), True)
            (Part(instrument='Horn', member=3, section='Horn'), False)
            (Part(instrument='Horn', member=4, section='Horn'), False)

            >>> part_assignment = abjad.PartAssignment('Horn', (3, 4))
            >>> for part in parts:
            ...     part, part in part_assignment
            ...
            (Part(instrument='Horn', member=1, section='Horn'), False)
            (Part(instrument='Horn', member=2, section='Horn'), False)
            (Part(instrument='Horn', member=3, section='Horn'), True)
            (Part(instrument='Horn', member=4, section='Horn'), True)

            >>> part_assignment = abjad.PartAssignment('Horn', [1, 3])
            >>> for part in parts:
            ...     part, part in part_assignment
            ...
            (Part(instrument='Horn', member=1, section='Horn'), True)
            (Part(instrument='Horn', member=2, section='Horn'), False)
            (Part(instrument='Horn', member=3, section='Horn'), True)
            (Part(instrument='Horn', member=4, section='Horn'), False)

        ..  container:: example

            Raises exception when input is not part:

            >>> part_assignment = abjad.PartAssignment('Horn')
            >>> 'Horn' in part_assignment
            Traceback (most recent call last):
                ...
            TypeError: must be part (not 'Horn').

        """
        if not isinstance(part, Part):
            raise TypeError(f"must be part (not {part!r}).")
        if part.section == self.section:
            if (
                part.member is None
                or self.members is None
                or part.member in self.members
                or []
            ):
                return True
            return False
        return False

    def __eq__(self, argument) -> bool:
        """
        Is true when ``argument`` is a part assignment with section and
        members equal to this part assignment.

        ..  container:: example

            >>> part_assignment_1 = abjad.PartAssignment('Horn', (1, 2))
            >>> part_assignment_2 = abjad.PartAssignment('Horn', [1, 2])
            >>> part_assignment_3 = abjad.PartAssignment('Horn')

            >>> part_assignment_1 == part_assignment_1
            True
            >>> part_assignment_1 == part_assignment_2
            True
            >>> part_assignment_1 == part_assignment_3
            False

            >>> part_assignment_2 == part_assignment_1
            True
            >>> part_assignment_2 == part_assignment_2
            True
            >>> part_assignment_2 == part_assignment_3
            False

            >>> part_assignment_3 == part_assignment_1
            False
            >>> part_assignment_3 == part_assignment_2
            False
            >>> part_assignment_3 == part_assignment_3
            True

        """
        if isinstance(argument, type(self)):
            if argument.section == self.section:
                return argument.members == self.members
        return False

    def __hash__(self) -> int:
        """
        Hashes part assignment.
        """
        return super().__hash__()

    def __iter__(self):
        """
        Iterates parts in assignment.

        ..  container:: example

            >>> part_assignment = abjad.PartAssignment('Horn', [1, 3])
            >>> for part in part_assignment:
            ...     part
            ...
            Part(instrument='Horn', member=1, section='Horn')
            Part(instrument='Horn', member=3, section='Horn')

        """
        return iter(self.parts)

    def __repr__(self) -> str:
        """
        Gets interpreter representation.
        """
        return StorageFormatManager(self).get_repr_format()

    ### PRIVATE METHODS ###

    @staticmethod
    def _expand_members(token):
        if token is None:
            return
        members = []
        if isinstance(token, int):
            members.append(token)
        elif isinstance(token, tuple):
            assert len(token) == 2, repr(token)
            for member in range(token[0], token[1] + 1):
                members.append(member)
        else:
            assert isinstance(token, list), repr(token)
            members.extend(token)
        return members

    def _expand_parts(self):
        parts = []
        if self.members is None:
            parts.append(Part(section=self.section))
        else:
            for member in self.members:
                part = Part(member=member, section=self.section)
                parts.append(part)
        return parts

    def _get_format_specification(self):
        repr_args_values = [self.section]
        if self.token is not None:
            repr_args_values.append(self.token)
        repr_is_indented = False
        repr_keyword_names = []
        return FormatSpecification(
            self,
            repr_args_values=repr_args_values,
            repr_is_indented=repr_is_indented,
            repr_keyword_names=repr_keyword_names,
            storage_format_args_values=repr_args_values,
            storage_format_is_indented=repr_is_indented,
            storage_format_keyword_names=repr_keyword_names,
        )

    @staticmethod
    def _is_token(argument):
        if isinstance(argument, int) and 1 <= argument:
            return True
        if (
            isinstance(argument, tuple)
            and len(argument) == 2
            and isinstance(argument[0], int)
            and isinstance(argument[1], int)
        ):
            return True
        if isinstance(argument, list):
            for item in argument:
                if not isinstance(item, int):
                    return False
                if not 1 <= item:
                    return False
            return True
        return False

    ### PUBLIC PROPERTIES ###

    @property
    def members(self) -> typing.Optional[typing.List[int]]:
        """
        Gets members.

        ..  container:: example

            >>> abjad.PartAssignment('Horn').members is None
            True

            >>> abjad.PartAssignment('Horn', 1).members
            [1]

            >>> abjad.PartAssignment('Horn', 2).members
            [2]

            >>> abjad.PartAssignment('Horn', (3, 4)).members
            [3, 4]

            >>> abjad.PartAssignment('Horn', [1, 3]).members
            [1, 3]

        """
        return self._members

    @property
    def parts(self) -> typing.List[Part]:
        """
        Gets parts.

        ..  container:: example

            >>> abjad.PartAssignment('Horn').parts
            [Part(instrument='Horn', section='Horn')]

            >>> abjad.PartAssignment('Horn', 1).parts
            [Part(instrument='Horn', member=1, section='Horn')]

            >>> abjad.PartAssignment('Horn', 2).parts
            [Part(instrument='Horn', member=2, section='Horn')]

            >>> abjad.PartAssignment('Horn', (3, 4)).parts
            [Part(instrument='Horn', member=3, section='Horn'), Part(instrument='Horn', member=4, section='Horn')]

            >>> abjad.PartAssignment('Horn', [1, 3]).parts
            [Part(instrument='Horn', member=1, section='Horn'), Part(instrument='Horn', member=3, section='Horn')]

        """
        return self._parts

    @property
    def section(self) -> typing.Optional[str]:
        """
        Gets section.

        ..  container:: example

            >>> abjad.PartAssignment('Horn').section
            'Horn'

            >>> abjad.PartAssignment('Horn', 1).section
            'Horn'

            >>> abjad.PartAssignment('Horn', 2).section
            'Horn'

            >>> abjad.PartAssignment('Horn', (3, 4)).section
            'Horn'

            >>> abjad.PartAssignment('Horn', [1, 3]).section
            'Horn'

        """
        return self._section

    @property
    def token(self) -> token_type:
        """
        Gets token.

        ..  container:: example

            >>> abjad.PartAssignment('Horn').token is None
            True

            >>> abjad.PartAssignment('Horn', 1).token
            1

            >>> abjad.PartAssignment('Horn', 2).token
            2

            >>> abjad.PartAssignment('Horn', (3, 4)).token
            (3, 4)

            >>> abjad.PartAssignment('Horn', [1, 3]).token
            [1, 3]

        """
        return self._token


class Section:
    """
    Section.

    ..  container:: example

        >>> abjad.Section(
        ...     abbreviation='VN-1',
        ...     count=18,
        ...     instrument='Violin',
        ...     name='FirstViolin',
        ...     )
        Section(abbreviation='VN-1', count=18, instrument='Violin', name='FirstViolin')

        >>> abjad.Section(
        ...     abbreviation='VN-2',
        ...     count=18,
        ...     instrument='Violin',
        ...     name='SecondViolin',
        ...     )
        Section(abbreviation='VN-2', count=18, instrument='Violin', name='SecondViolin')

        >>> abjad.Section(
        ...     abbreviation='VA',
        ...     count=18,
        ...     name='Viola',
        ...     )
        Section(abbreviation='VA', count=18, instrument='Viola', name='Viola')

        >>> abjad.Section(
        ...     abbreviation='VC',
        ...     count=14,
        ...     name='Cello',
        ...     )
        Section(abbreviation='VC', count=14, instrument='Cello', name='Cello')

        >>> abjad.Section(
        ...     abbreviation='CB',
        ...     count=6,
        ...     name='Contrabass',
        ...     )
        Section(abbreviation='CB', count=6, instrument='Contrabass', name='Contrabass')

    """

    ### CLASS VARIABLES ###

    __slots__ = ("_abbreviation", "_count", "_instrument", "_name", "_parts")

    ### INITIALIZER ###

    def __init__(
        self,
        abbreviation: str = None,
        count: int = 1,
        instrument: str = None,
        name: str = None,
    ) -> None:
        if abbreviation is not None:
            assert isinstance(abbreviation, str), repr(abbreviation)
        self._abbreviation = abbreviation
        if not isinstance(count, int):
            raise Exception(f"Count must be integer (not {count!r}).")
        if not 1 <= count:
            raise Exception(f"Count must be positive (not {count!r}).")
        self._count = count
        if instrument is not None:
            assert isinstance(instrument, str), repr(instrument)
        else:
            instrument = name
        self._instrument = instrument
        if name is not None:
            assert isinstance(name, str), repr(name)
        self._name = name
        parts = []
        if self.count is None:
            part = Part(self.name)
            parts.append(part)
        else:
            if 1 < len(str(self.count)):
                zfill: typing.Optional[int] = len(str(self.count))
            else:
                zfill = None
            for member in range(1, self.count + 1):
                part = Part(
                    member=member,
                    instrument=self.instrument,
                    section=self.name,
                    section_abbreviation=self.abbreviation,
                    zfill=zfill,
                )
                parts.append(part)
        self._parts = parts

    ### SPECIAL METHODS ###

    def __eq__(self, argument) -> bool:
        """
        Is true when ``argument`` is a section with the same name,
        abbreviation and count as this section.

        ..  container:: example

            >>> section_1 = abjad.Section(
            ...     abbreviation='VN-1',
            ...     count=18,
            ...     instrument='Violin',
            ...     name='FirstViolin',
            ...     )
            >>> section_2 = abjad.Section(
            ...     abbreviation='VN-1',
            ...     count=18,
            ...     instrument='Violin',
            ...     name='FirstViolin',
            ...     )
            >>> section_3 = abjad.Section(
            ...     abbreviation='VN-2',
            ...     count=18,
            ...     instrument='Violin',
            ...     name='SecondViolin',
            ...     )

            >>> section_1 == section_1
            True
            >>> section_1 == section_2
            True
            >>> section_1 == section_3
            False

            >>> section_2 == section_1
            True
            >>> section_2 == section_2
            True
            >>> section_2 == section_3
            False

            >>> section_3 == section_1
            False
            >>> section_3 == section_2
            False
            >>> section_3 == section_3
            True

        """
        if (
            isinstance(argument, type(self))
            and argument.name == self.name
            and argument.abbreviation == self.abbreviation
            and argument.count == self.count
        ):
            return True
        return False

    def __hash__(self):
        """
        Hashes section.
        """
        return super().__hash__()

    def __repr__(self) -> str:
        """
        Gets interpreter representation.
        """
        return StorageFormatManager(self).get_repr_format()

    ### PUBLIC PROPERTIES ###

    @property
    def abbreviation(self) -> typing.Optional[str]:
        """
        Gets abbreviation.

        ..  container:: example

            >>> section = abjad.Section(
            ...     abbreviation='VN-1',
            ...     count=18,
            ...     instrument='Violin',
            ...     name='FirstViolin',
            ...     )

            >>> section.abbreviation
            'VN-1'

        """
        return self._abbreviation

    @property
    def count(self) -> typing.Optional[int]:
        """
        Gets section count.

        ..  container:: example

            >>> section = abjad.Section(
            ...     abbreviation='VN-1',
            ...     count=18,
            ...     instrument='Violin',
            ...     name='FirstViolin',
            ...     )

            >>> section.count
            18

        """
        return self._count

    @property
    def instrument(self) -> typing.Optional[str]:
        """
        Gets section instrument.

        ..  container:: example

            >>> section = abjad.Section(
            ...     abbreviation='VN-1',
            ...     count=18,
            ...     instrument='Violin',
            ...     name='FirstViolin',
            ...     )

            >>> section.instrument
            'Violin'

        """
        return self._instrument

    @property
    def name(self) -> typing.Optional[str]:
        """
        Gets section name.

        ..  container:: example

            >>> section = abjad.Section(
            ...     abbreviation='VN-1',
            ...     count=18,
            ...     instrument='Violin',
            ...     name='FirstViolin',
            ...     )

            >>> section.name
            'FirstViolin'

        """
        return self._name

    @property
    def parts(self) -> typing.List[Part]:
        """
        Gets parts.

        ..  container:: example

            >>> section = abjad.Section(
            ...     abbreviation='VN-1',
            ...     count=18,
            ...     instrument='Violin',
            ...     name='FirstViolin',
            ...     )

            >>> for part in section.parts:
            ...     part
            ...
            Part(instrument='Violin', member=1, section='FirstViolin', section_abbreviation='VN-1', zfill=2)
            Part(instrument='Violin', member=2, section='FirstViolin', section_abbreviation='VN-1', zfill=2)
            Part(instrument='Violin', member=3, section='FirstViolin', section_abbreviation='VN-1', zfill=2)
            Part(instrument='Violin', member=4, section='FirstViolin', section_abbreviation='VN-1', zfill=2)
            Part(instrument='Violin', member=5, section='FirstViolin', section_abbreviation='VN-1', zfill=2)
            Part(instrument='Violin', member=6, section='FirstViolin', section_abbreviation='VN-1', zfill=2)
            Part(instrument='Violin', member=7, section='FirstViolin', section_abbreviation='VN-1', zfill=2)
            Part(instrument='Violin', member=8, section='FirstViolin', section_abbreviation='VN-1', zfill=2)
            Part(instrument='Violin', member=9, section='FirstViolin', section_abbreviation='VN-1', zfill=2)
            Part(instrument='Violin', member=10, section='FirstViolin', section_abbreviation='VN-1', zfill=2)
            Part(instrument='Violin', member=11, section='FirstViolin', section_abbreviation='VN-1', zfill=2)
            Part(instrument='Violin', member=12, section='FirstViolin', section_abbreviation='VN-1', zfill=2)
            Part(instrument='Violin', member=13, section='FirstViolin', section_abbreviation='VN-1', zfill=2)
            Part(instrument='Violin', member=14, section='FirstViolin', section_abbreviation='VN-1', zfill=2)
            Part(instrument='Violin', member=15, section='FirstViolin', section_abbreviation='VN-1', zfill=2)
            Part(instrument='Violin', member=16, section='FirstViolin', section_abbreviation='VN-1', zfill=2)
            Part(instrument='Violin', member=17, section='FirstViolin', section_abbreviation='VN-1', zfill=2)
            Part(instrument='Violin', member=18, section='FirstViolin', section_abbreviation='VN-1', zfill=2)

        """
        return list(self._parts)


class PartManifest:
    """
    Part manifest.

    ..  container:: example

        Initializes from parts:

        >>> part_manifest = abjad.PartManifest(
        ...    abjad.Part(section='BassClarinet', section_abbreviation='BCL'),
        ...    abjad.Part(section='Violin', section_abbreviation='VN'),
        ...    abjad.Part(section='Viola', section_abbreviation='VA'),
        ...    abjad.Part(section='Cello', section_abbreviation='VC'),
        ...    )
        >>> len(part_manifest)
        4

    ..  container:: example

        Initializes from orchestra sections:

        >>> part_manifest = abjad.PartManifest(
        ...    abjad.Section(
        ...         abbreviation='FL',
        ...         count=4,
        ...         name='Flute',
        ...         ),
        ...    abjad.Section(
        ...         abbreviation='OB',
        ...         count=3,
        ...         name='Oboe',
        ...         ),
        ...    abjad.Part(
        ...         section_abbreviation='EH',
        ...         section='EnglishHorn',
        ...         ),
        ...    abjad.Section(
        ...         abbreviation='VN-1',
        ...         count=18,
        ...         instrument='Violin',
        ...         name='FirstViolin',
        ...         ),
        ...    abjad.Section(
        ...         abbreviation='VN-2',
        ...         count=18,
        ...         instrument='Violin',
        ...         name='SecondViolin',
        ...         ),
        ...    )
        >>> len(part_manifest)
        44

    """

    ### CLASS VARIABLES ###

    __slots__ = ("_parts", "_sections")

    ### INITIALIZER ###

    def __init__(self, *arguments):
        parts, sections = [], []
        for argument in arguments:
            if isinstance(argument, Part):
                parts.append(argument)
            elif isinstance(argument, Section):
                sections.append(argument)
                parts.extend(argument.parts)
            else:
                raise TypeError(f"must be part or section (not {argument}).")
        for i, part in enumerate(parts):
            number = i + 1
            part._number = number
        self._parts = parts
        self._sections = sections

    ### SPECIAL METHODS ###

    def __iter__(self) -> typing.Iterator:
        """
        Iterates parts in manifest.

        ..  container:: example

            >>> part_manifest = abjad.PartManifest(
            ...    abjad.Section(
            ...         abbreviation='FL',
            ...         count=4,
            ...         name='Flute',
            ...         ),
            ...    abjad.Section(
            ...         abbreviation='OB',
            ...         count=3,
            ...         name='Oboe',
            ...         ),
            ...    abjad.Part(
            ...         section_abbreviation='EH',
            ...         section='EnglishHorn',
            ...         ),
            ...    abjad.Section(
            ...         abbreviation='VN-1',
            ...         count=18,
            ...         instrument='Violin',
            ...         name='FirstViolin',
            ...         ),
            ...    abjad.Section(
            ...         abbreviation='VN-2',
            ...         count=18,
            ...         instrument='Violin',
            ...         name='SecondViolin',
            ...         ),
            ...    )

            >>> for part in part_manifest:
            ...     part
            ...
            Part(instrument='Flute', member=1, number=1, section='Flute', section_abbreviation='FL')
            Part(instrument='Flute', member=2, number=2, section='Flute', section_abbreviation='FL')
            Part(instrument='Flute', member=3, number=3, section='Flute', section_abbreviation='FL')
            Part(instrument='Flute', member=4, number=4, section='Flute', section_abbreviation='FL')
            Part(instrument='Oboe', member=1, number=5, section='Oboe', section_abbreviation='OB')
            Part(instrument='Oboe', member=2, number=6, section='Oboe', section_abbreviation='OB')
            Part(instrument='Oboe', member=3, number=7, section='Oboe', section_abbreviation='OB')
            Part(instrument='EnglishHorn', number=8, section='EnglishHorn', section_abbreviation='EH')
            Part(instrument='Violin', member=1, number=9, section='FirstViolin', section_abbreviation='VN-1', zfill=2)
            Part(instrument='Violin', member=2, number=10, section='FirstViolin', section_abbreviation='VN-1', zfill=2)
            Part(instrument='Violin', member=3, number=11, section='FirstViolin', section_abbreviation='VN-1', zfill=2)
            Part(instrument='Violin', member=4, number=12, section='FirstViolin', section_abbreviation='VN-1', zfill=2)
            Part(instrument='Violin', member=5, number=13, section='FirstViolin', section_abbreviation='VN-1', zfill=2)
            Part(instrument='Violin', member=6, number=14, section='FirstViolin', section_abbreviation='VN-1', zfill=2)
            Part(instrument='Violin', member=7, number=15, section='FirstViolin', section_abbreviation='VN-1', zfill=2)
            Part(instrument='Violin', member=8, number=16, section='FirstViolin', section_abbreviation='VN-1', zfill=2)
            Part(instrument='Violin', member=9, number=17, section='FirstViolin', section_abbreviation='VN-1', zfill=2)
            Part(instrument='Violin', member=10, number=18, section='FirstViolin', section_abbreviation='VN-1', zfill=2)
            Part(instrument='Violin', member=11, number=19, section='FirstViolin', section_abbreviation='VN-1', zfill=2)
            Part(instrument='Violin', member=12, number=20, section='FirstViolin', section_abbreviation='VN-1', zfill=2)
            Part(instrument='Violin', member=13, number=21, section='FirstViolin', section_abbreviation='VN-1', zfill=2)
            Part(instrument='Violin', member=14, number=22, section='FirstViolin', section_abbreviation='VN-1', zfill=2)
            Part(instrument='Violin', member=15, number=23, section='FirstViolin', section_abbreviation='VN-1', zfill=2)
            Part(instrument='Violin', member=16, number=24, section='FirstViolin', section_abbreviation='VN-1', zfill=2)
            Part(instrument='Violin', member=17, number=25, section='FirstViolin', section_abbreviation='VN-1', zfill=2)
            Part(instrument='Violin', member=18, number=26, section='FirstViolin', section_abbreviation='VN-1', zfill=2)
            Part(instrument='Violin', member=1, number=27, section='SecondViolin', section_abbreviation='VN-2', zfill=2)
            Part(instrument='Violin', member=2, number=28, section='SecondViolin', section_abbreviation='VN-2', zfill=2)
            Part(instrument='Violin', member=3, number=29, section='SecondViolin', section_abbreviation='VN-2', zfill=2)
            Part(instrument='Violin', member=4, number=30, section='SecondViolin', section_abbreviation='VN-2', zfill=2)
            Part(instrument='Violin', member=5, number=31, section='SecondViolin', section_abbreviation='VN-2', zfill=2)
            Part(instrument='Violin', member=6, number=32, section='SecondViolin', section_abbreviation='VN-2', zfill=2)
            Part(instrument='Violin', member=7, number=33, section='SecondViolin', section_abbreviation='VN-2', zfill=2)
            Part(instrument='Violin', member=8, number=34, section='SecondViolin', section_abbreviation='VN-2', zfill=2)
            Part(instrument='Violin', member=9, number=35, section='SecondViolin', section_abbreviation='VN-2', zfill=2)
            Part(instrument='Violin', member=10, number=36, section='SecondViolin', section_abbreviation='VN-2', zfill=2)
            Part(instrument='Violin', member=11, number=37, section='SecondViolin', section_abbreviation='VN-2', zfill=2)
            Part(instrument='Violin', member=12, number=38, section='SecondViolin', section_abbreviation='VN-2', zfill=2)
            Part(instrument='Violin', member=13, number=39, section='SecondViolin', section_abbreviation='VN-2', zfill=2)
            Part(instrument='Violin', member=14, number=40, section='SecondViolin', section_abbreviation='VN-2', zfill=2)
            Part(instrument='Violin', member=15, number=41, section='SecondViolin', section_abbreviation='VN-2', zfill=2)
            Part(instrument='Violin', member=16, number=42, section='SecondViolin', section_abbreviation='VN-2', zfill=2)
            Part(instrument='Violin', member=17, number=43, section='SecondViolin', section_abbreviation='VN-2', zfill=2)
            Part(instrument='Violin', member=18, number=44, section='SecondViolin', section_abbreviation='VN-2', zfill=2)

        """
        return iter(self.parts)

    def __len__(self) -> int:
        """
        Gets number of parts in manifest.

        ..  container:: example

            >>> part_manifest = abjad.PartManifest(
            ...    abjad.Part(section='BassClarinet', section_abbreviation='BCL'),
            ...    abjad.Part(section='Violin', section_abbreviation='VN'),
            ...    abjad.Part(section='Viola', section_abbreviation='VA'),
            ...    abjad.Part(section='Cello', section_abbreviation='VC'),
            ...    )
            >>> len(part_manifest)
            4

        ..  container:: example

            >>> part_manifest = abjad.PartManifest(
            ...    abjad.Section(
            ...         abbreviation='FL',
            ...         count=4,
            ...         name='Flute',
            ...         ),
            ...    abjad.Section(
            ...         abbreviation='OB',
            ...         count=3,
            ...         name='Oboe',
            ...         ),
            ...    abjad.Part(
            ...         section_abbreviation='EH',
            ...         section='EnglishHorn',
            ...         ),
            ...    abjad.Section(
            ...         abbreviation='VN-1',
            ...         count=18,
            ...         instrument='Violin',
            ...         name='FirstViolin',
            ...         ),
            ...    abjad.Section(
            ...         abbreviation='VN-2',
            ...         count=18,
            ...         instrument='Violin',
            ...         name='SecondViolin',
            ...         ),
            ...    )

            >>> len(part_manifest)
            44

        """
        return len(self.parts)

    def __repr__(self) -> str:
        """
        Gets interpreter representation.
        """
        return StorageFormatManager(self).get_repr_format()

    ### PUBLIC PROPERTIES ###

    @property
    def parts(self) -> typing.List[Part]:
        """
        Gets parts in manifest.

        ..  container:: example

            >>> part_manifest = abjad.PartManifest(
            ...    abjad.Part(section='BassClarinet', section_abbreviation='BCL'),
            ...    abjad.Part(section='Violin', section_abbreviation='VN'),
            ...    abjad.Part(section='Viola', section_abbreviation='VA'),
            ...    abjad.Part(section='Cello', section_abbreviation='VC'),
            ...    )
            >>> for part in part_manifest:
            ...     part
            ...
            Part(instrument='BassClarinet', number=1, section='BassClarinet', section_abbreviation='BCL')
            Part(instrument='Violin', number=2, section='Violin', section_abbreviation='VN')
            Part(instrument='Viola', number=3, section='Viola', section_abbreviation='VA')
            Part(instrument='Cello', number=4, section='Cello', section_abbreviation='VC')

        ..  container:: example

            >>> part_manifest = abjad.PartManifest(
            ...    abjad.Section(
            ...         abbreviation='FL',
            ...         count=4,
            ...         name='Flute',
            ...         ),
            ...    abjad.Section(
            ...         abbreviation='OB',
            ...         count=3,
            ...         name='Oboe',
            ...         ),
            ...    abjad.Part(
            ...         section_abbreviation='EH',
            ...         section='EnglishHorn',
            ...         ),
            ...    abjad.Section(
            ...         abbreviation='VN-1',
            ...         count=18,
            ...         instrument='Violin',
            ...         name='FirstViolin',
            ...         ),
            ...    abjad.Section(
            ...         abbreviation='VN-2',
            ...         count=18,
            ...         instrument='Violin',
            ...         name='SecondViolin',
            ...         ),
            ...    )

            >>> for part in part_manifest.parts:
            ...     part
            ...
            Part(instrument='Flute', member=1, number=1, section='Flute', section_abbreviation='FL')
            Part(instrument='Flute', member=2, number=2, section='Flute', section_abbreviation='FL')
            Part(instrument='Flute', member=3, number=3, section='Flute', section_abbreviation='FL')
            Part(instrument='Flute', member=4, number=4, section='Flute', section_abbreviation='FL')
            Part(instrument='Oboe', member=1, number=5, section='Oboe', section_abbreviation='OB')
            Part(instrument='Oboe', member=2, number=6, section='Oboe', section_abbreviation='OB')
            Part(instrument='Oboe', member=3, number=7, section='Oboe', section_abbreviation='OB')
            Part(instrument='EnglishHorn', number=8, section='EnglishHorn', section_abbreviation='EH')
            Part(instrument='Violin', member=1, number=9, section='FirstViolin', section_abbreviation='VN-1', zfill=2)
            Part(instrument='Violin', member=2, number=10, section='FirstViolin', section_abbreviation='VN-1', zfill=2)
            Part(instrument='Violin', member=3, number=11, section='FirstViolin', section_abbreviation='VN-1', zfill=2)
            Part(instrument='Violin', member=4, number=12, section='FirstViolin', section_abbreviation='VN-1', zfill=2)
            Part(instrument='Violin', member=5, number=13, section='FirstViolin', section_abbreviation='VN-1', zfill=2)
            Part(instrument='Violin', member=6, number=14, section='FirstViolin', section_abbreviation='VN-1', zfill=2)
            Part(instrument='Violin', member=7, number=15, section='FirstViolin', section_abbreviation='VN-1', zfill=2)
            Part(instrument='Violin', member=8, number=16, section='FirstViolin', section_abbreviation='VN-1', zfill=2)
            Part(instrument='Violin', member=9, number=17, section='FirstViolin', section_abbreviation='VN-1', zfill=2)
            Part(instrument='Violin', member=10, number=18, section='FirstViolin', section_abbreviation='VN-1', zfill=2)
            Part(instrument='Violin', member=11, number=19, section='FirstViolin', section_abbreviation='VN-1', zfill=2)
            Part(instrument='Violin', member=12, number=20, section='FirstViolin', section_abbreviation='VN-1', zfill=2)
            Part(instrument='Violin', member=13, number=21, section='FirstViolin', section_abbreviation='VN-1', zfill=2)
            Part(instrument='Violin', member=14, number=22, section='FirstViolin', section_abbreviation='VN-1', zfill=2)
            Part(instrument='Violin', member=15, number=23, section='FirstViolin', section_abbreviation='VN-1', zfill=2)
            Part(instrument='Violin', member=16, number=24, section='FirstViolin', section_abbreviation='VN-1', zfill=2)
            Part(instrument='Violin', member=17, number=25, section='FirstViolin', section_abbreviation='VN-1', zfill=2)
            Part(instrument='Violin', member=18, number=26, section='FirstViolin', section_abbreviation='VN-1', zfill=2)
            Part(instrument='Violin', member=1, number=27, section='SecondViolin', section_abbreviation='VN-2', zfill=2)
            Part(instrument='Violin', member=2, number=28, section='SecondViolin', section_abbreviation='VN-2', zfill=2)
            Part(instrument='Violin', member=3, number=29, section='SecondViolin', section_abbreviation='VN-2', zfill=2)
            Part(instrument='Violin', member=4, number=30, section='SecondViolin', section_abbreviation='VN-2', zfill=2)
            Part(instrument='Violin', member=5, number=31, section='SecondViolin', section_abbreviation='VN-2', zfill=2)
            Part(instrument='Violin', member=6, number=32, section='SecondViolin', section_abbreviation='VN-2', zfill=2)
            Part(instrument='Violin', member=7, number=33, section='SecondViolin', section_abbreviation='VN-2', zfill=2)
            Part(instrument='Violin', member=8, number=34, section='SecondViolin', section_abbreviation='VN-2', zfill=2)
            Part(instrument='Violin', member=9, number=35, section='SecondViolin', section_abbreviation='VN-2', zfill=2)
            Part(instrument='Violin', member=10, number=36, section='SecondViolin', section_abbreviation='VN-2', zfill=2)
            Part(instrument='Violin', member=11, number=37, section='SecondViolin', section_abbreviation='VN-2', zfill=2)
            Part(instrument='Violin', member=12, number=38, section='SecondViolin', section_abbreviation='VN-2', zfill=2)
            Part(instrument='Violin', member=13, number=39, section='SecondViolin', section_abbreviation='VN-2', zfill=2)
            Part(instrument='Violin', member=14, number=40, section='SecondViolin', section_abbreviation='VN-2', zfill=2)
            Part(instrument='Violin', member=15, number=41, section='SecondViolin', section_abbreviation='VN-2', zfill=2)
            Part(instrument='Violin', member=16, number=42, section='SecondViolin', section_abbreviation='VN-2', zfill=2)
            Part(instrument='Violin', member=17, number=43, section='SecondViolin', section_abbreviation='VN-2', zfill=2)
            Part(instrument='Violin', member=18, number=44, section='SecondViolin', section_abbreviation='VN-2', zfill=2)

        ..  container:: example

            >>> abjad.Part(section='FirstViolin', member=18) in part_manifest.parts
            True

            >>> abjad.Part(section='FirstViolin', member=19) in part_manifest.parts
            False

        """
        return list(self._parts)

    @property
    def sections(self) -> typing.List[Section]:
        """
        Gets sections in manifest.

        ..  container:: example

            >>> part_manifest = abjad.PartManifest(
            ...    abjad.Part(section='BassClarinet', section_abbreviation='BCL'),
            ...    abjad.Part(section='Violin', section_abbreviation='VN'),
            ...    abjad.Part(section='Viola', section_abbreviation='VA'),
            ...    abjad.Part(section='Cello', section_abbreviation='VC'),
            ...    )
            >>> part_manifest.sections
            []

        ..  container:: example

            >>> part_manifest = abjad.PartManifest(
            ...    abjad.Section(
            ...         abbreviation='FL',
            ...         count=4,
            ...         name='Flute',
            ...         ),
            ...    abjad.Section(
            ...         abbreviation='OB',
            ...         count=3,
            ...         name='Oboe',
            ...         ),
            ...    abjad.Part(
            ...         section_abbreviation='EH',
            ...         section='EnglishHorn',
            ...         ),
            ...    abjad.Section(
            ...         abbreviation='VN-1',
            ...         count=18,
            ...         instrument='Violin',
            ...         name='FirstViolin',
            ...         ),
            ...    abjad.Section(
            ...         abbreviation='VN-2',
            ...         count=18,
            ...         instrument='Violin',
            ...         name='SecondViolin',
            ...         ),
            ...    )

            >>> for section in part_manifest.sections:
            ...     section
            ...
            Section(abbreviation='FL', count=4, instrument='Flute', name='Flute')
            Section(abbreviation='OB', count=3, instrument='Oboe', name='Oboe')
            Section(abbreviation='VN-1', count=18, instrument='Violin', name='FirstViolin')
            Section(abbreviation='VN-2', count=18, instrument='Violin', name='SecondViolin')

        ..  container:: example

            >>> section = abjad.Section(
            ...     abbreviation='VN-1',
            ...     count=18,
            ...     instrument='Violin',
            ...     name='FirstViolin',
            ...     )
            >>> section in part_manifest.sections
            True

            >>> section = abjad.Section(
            ...     abbreviation='VN-1',
            ...     count=36,
            ...     instrument='Violin',
            ...     name='FirstViolin',
            ...     )
            >>> section in part_manifest.sections
            False

        """
        return list(self._sections)

    ### PUBLIC METHODS ###

    def expand(self, part_assignment):
        """
        Expands ``part_assignment``.

        ..  container:: example

            >>> part_manifest = abjad.PartManifest(
            ...    abjad.Section(
            ...         abbreviation='FL',
            ...         count=4,
            ...         name='Flute',
            ...         ),
            ...    abjad.Section(
            ...         abbreviation='OB',
            ...         count=3,
            ...         name='Oboe',
            ...         ),
            ...    abjad.Part(
            ...         section_abbreviation='EH',
            ...         section='EnglishHorn',
            ...         ),
            ...    abjad.Section(
            ...         abbreviation='VN-1',
            ...         count=18,
            ...         instrument='Violin',
            ...         name='FirstViolin',
            ...         ),
            ...    abjad.Section(
            ...         abbreviation='VN-2',
            ...         count=18,
            ...         instrument='Violin',
            ...         name='SecondViolin',
            ...         ),
            ...    )

            >>> part_assignment = abjad.PartAssignment('Oboe')
            >>> for part in part_manifest.expand(part_assignment):
            ...     part
            ...
            Part(instrument='Oboe', member=1, number=5, section='Oboe', section_abbreviation='OB')
            Part(instrument='Oboe', member=2, number=6, section='Oboe', section_abbreviation='OB')
            Part(instrument='Oboe', member=3, number=7, section='Oboe', section_abbreviation='OB')

        """
        assert isinstance(part_assignment, PartAssignment)
        parts = []
        for part in self.parts:
            if part.section == part_assignment.section:
                if part_assignment.token is None:
                    parts.append(part)
                elif part.member in part_assignment.members:
                    parts.append(part)
        return parts


class PersistentOverride:
    """
    Persistent override.

    ..  container:: example

        >>> override = abjad.PersistentOverride(
        ...     attribute='bar_extent',
        ...     context='Staff',
        ...     grob='bar_line',
        ...     value=(-2, 0),
        ...     )

        >>> print(abjad.storage(override))
        abjad.PersistentOverride(
            attribute='bar_extent',
            context='Staff',
            grob='bar_line',
            value=(-2, 0),
            )

    """

    ### CLASS VARIABLES ###

    __slots__ = (
        "_after",
        "_attribute",
        "_context",
        "_grob",
        "_hide",
        "_value",
    )

    _persistent = True

    ### INITIALIZER ###

    def __init__(
        self,
        after: bool = None,
        attribute: str = None,
        context: str = None,
        grob: str = None,
        hide: bool = None,
        value: typing.Any = None,
    ) -> None:
        if after is not None:
            after = bool(after)
        self._after = after
        if attribute is not None:
            assert isinstance(attribute, str), repr(attribute)
        self._attribute = attribute
        if context is not None:
            assert isinstance(context, str), repr(context)
        self._context = context
        if grob is not None:
            assert isinstance(grob, str), repr(grob)
        self._grob = grob
        if hide is not None:
            hide = bool(hide)
        self._hide = hide
        self._value = value

    ### SPECIAL METHODS ###

    def __eq__(self, argument) -> bool:
        """
        Is true when ``argument`` is persistent override with attribute,
        context, grob, value equal to those of this persistent override.

        ..  container:: example

            >>> override_1 = abjad.PersistentOverride(
            ...     attribute='bar_extent',
            ...     context='Staff',
            ...     grob='bar_line',
            ...     value=(-2, 0),
            ...     )
            >>> override_2 = abjad.PersistentOverride(
            ...     attribute='bar_extent',
            ...     context='Staff',
            ...     grob='bar_line',
            ...     value=(-2, 0),
            ...     )
            >>> override_3 = abjad.PersistentOverride(
            ...     attribute='bar_extent',
            ...     context='Score',
            ...     grob='bar_line',
            ...     value=(-2, 0),
            ...     )

            >>> override_1 == override_1
            True
            >>> override_1 == override_2
            True
            >>> override_1 == override_3
            False

            >>> override_2 == override_1
            True
            >>> override_2 == override_2
            True
            >>> override_2 == override_3
            False

            >>> override_3 == override_1
            False
            >>> override_3 == override_2
            False
            >>> override_3 == override_3
            True

        """
        if not isinstance(argument, type(self)):
            return False
        if (
            self.attribute == argument.attribute
            and self.context == argument.context
            and self.grob == argument.grob
            and self.value == argument.value
        ):
            return True
        return False

    def __hash__(self) -> int:
        """
        Hashes persistent override.
        """
        return super().__hash__()

    def __repr__(self) -> str:
        """
        Gets interpreter representation.
        """
        return StorageFormatManager(self).get_repr_format()

    ### PRIVATE METHODS ###

    def _get_format_specification(self):
        return FormatSpecification(client=self)

    def _get_lilypond_format(self, context=None):
        if isinstance(context, Context):
            assert isinstance(context.lilypond_type, str), repr(context)
            lilypond_type = context.lilypond_type
        else:
            lilypond_type = self.context
        string = OverrideInterface.make_lilypond_override_string(
            self.grob, self.attribute, self.value, context=lilypond_type, once=False,
        )
        return string

    def _get_lilypond_format_bundle(self, component=None):
        bundle = LilyPondFormatBundle()
        if self.hide:
            return bundle
        strings = [self._get_lilypond_format()]
        if self.after:
            bundle.after.commands.extend(strings)
        else:
            bundle.before.commands.extend(strings)
        return bundle

    ### PUBLIC PROPERTIES ###

    @property
    def after(self) -> typing.Optional[bool]:
        r"""
        Is true when override formats after leaf.

        ..  container:: example

            Formats override before leaf:

            >>> override = abjad.PersistentOverride(
            ...     attribute='color',
            ...     grob='note_head',
            ...     value='red',
            ...     )

            >>> staff = abjad.Staff("c'4 d' e' f'")
            >>> abjad.attach(override, staff[0])
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    \override NoteHead.color = #red
                    c'4
                    d'4
                    e'4
                    f'4
                }

        ..  container:: example

            Formats override after leaf:

            >>> override = abjad.PersistentOverride(
            ...     after=True,
            ...     attribute='color',
            ...     grob='note_head',
            ...     value='red',
            ...     )

            >>> staff = abjad.Staff("c'4 d' e' f'")
            >>> abjad.attach(override, staff[0])
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    c'4
                    \override NoteHead.color = #red
                    d'4
                    e'4
                    f'4
                }

        """
        return self._after

    @property
    def attribute(self) -> typing.Optional[str]:
        """
        Gets attribute.

        ..  container:: example

            >>> override = abjad.PersistentOverride(
            ...     attribute='bar_extent',
            ...     context='Staff',
            ...     grob='bar_line',
            ...     value=(-2, 0),
            ...     )

            >>> override.attribute
            'bar_extent'

        """
        return self._attribute

    @property
    def context(self) -> typing.Optional[str]:
        """
        Gets context.

        ..  container:: example

            >>> override = abjad.PersistentOverride(
            ...     attribute='bar_extent',
            ...     context='Staff',
            ...     grob='bar_line',
            ...     value=(-2, 0),
            ...     )

            >>> override.context
            'Staff'

        """
        return self._context

    @property
    def grob(self) -> typing.Optional[str]:
        """
        Gets grob.

        ..  container:: example

            >>> override = abjad.PersistentOverride(
            ...     attribute='bar_extent',
            ...     context='Staff',
            ...     grob='bar_line',
            ...     value=(-2, 0),
            ...     )

            >>> override.grob
            'bar_line'

        """
        return self._grob

    @property
    def hide(self) -> typing.Optional[bool]:
        """
        Is true when staff lines should not appear in output.

        ..  container:: example

            >>> override = abjad.PersistentOverride(
            ...     attribute='bar_extent',
            ...     context='Staff',
            ...     grob='bar_line',
            ...     value=(-2, 0),
            ...     )

            >>> override.hide is None
            True

        """
        return self._hide

    @property
    def persistent(self) -> bool:
        """
        Is true.

        ..  container:: example

            >>> override = abjad.PersistentOverride(
            ...     attribute='bar_extent',
            ...     context='Staff',
            ...     grob='bar_line',
            ...     value=(-2, 0),
            ...     )

            >>> override.persistent
            True

        Class constant.
        """
        return self._persistent

    @property
    def value(self) -> typing.Optional[str]:
        """
        Gets value.

        ..  container:: example

            >>> override = abjad.PersistentOverride(
            ...     attribute='bar_extent',
            ...     context='Staff',
            ...     grob='bar_line',
            ...     value=(-2, 0),
            ...     )

            >>> override.value
            (-2, 0)

        """
        return self._value
