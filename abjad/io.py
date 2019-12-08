import datetime
import hashlib
import pathlib
import re
import subprocess
import tempfile
from typing import Sequence, Tuple

from uqbar.graphs import Grapher

from abjad.lilypondfile import Block
from abjad.system import AbjadConfiguration, IOManager, Timer

_configuration = AbjadConfiguration()


class LilyPondIO:

    ### INITIALIZER ###

    def __init__(self, illustrable, **keywords):
        if not hasattr(illustrable, "__illustrate__"):
            raise ValueError(r"Cannot illustrate {illustrable!r}")
        self.illustrable = illustrable
        self.keywords = keywords

    ### SPECIAL METHODS ###

    def __call__(self):
        with Timer() as format_timer:
            string = self.get_string()
        format_time = format_timer.elapsed_time
        render_prefix = self.get_render_prefix(string)
        output_directory_path = self.get_output_directory()
        render_directory_path = self.get_render_directory()
        input_path = render_directory_path / pathlib.Path(render_prefix).with_suffix(
            ".ly"
        )
        self.persist_string(string, input_path)
        lilypond_path = self.get_lilypond_path()
        render_command = self.get_render_command(input_path, lilypond_path)
        with Timer() as render_timer:
            log, success = self.run_command(render_command)
        render_time = render_timer.elapsed_time
        self.persist_string(log, input_path.with_suffix(".log"))
        output_paths = self.migrate_assets(render_directory_path, output_directory_path)
        openable_paths = []
        for output_path in self.get_openable_paths(output_paths):
            openable_paths.append(output_path)
            self.open_output_path(output_path)
        return openable_paths, format_time, render_time, success, log

    ### PUBLIC METHODS ###

    def get_lilypond_path(self):
        lilypond_path = _configuration.get("lilypond_path")
        if not lilypond_path:
            lilypond_paths = IOManager.find_executable("lilypond")
            if lilypond_paths:
                lilypond_path = lilypond_paths[0]
            else:
                lilypond_path = "lilypond"
        return lilypond_path

    def get_output_directory(self) -> pathlib.Path:
        return pathlib.Path(_configuration["abjad_output_directory"])

    def get_render_command(self, input_path, lilypond_path) -> str:
        parts = [
            str(lilypond_path),
            "-dno-point-and-click",
            "-o",
            str(input_path.with_suffix("")),
            str(input_path),
        ]
        return " ".join(parts)

    def get_render_directory(self):
        return pathlib.Path(tempfile.mkdtemp())

    def get_render_prefix(self, string) -> str:
        timestamp = re.sub(r"[^\w]", "-", datetime.datetime.now().isoformat())
        checksum = hashlib.md5(string.encode()).hexdigest()[:7]
        return f"{timestamp}-{checksum}"

    def get_string(self) -> str:
        lilypond_file = self.illustrable.__illustrate__(**self.keywords)
        return format(lilypond_file, "lilypond")

    def migrate_assets(
        self, render_directory, output_directory
    ) -> Sequence[pathlib.Path]:
        migrated_assets = []
        for old_path in render_directory.iterdir():
            new_path = output_directory / old_path.name
            migrated_assets.append(old_path.rename(new_path))
        return migrated_assets

    def open_output_path(self, output_path):
        IOManager.open_file(str(output_path))

    def persist_log(self, string, input_path):
        input_path.write_text(string)

    def persist_string(self, string, input_path):
        input_path.write_text(string)

    def run_command(self, command) -> Tuple[str, int]:
        completed_process = subprocess.run(
            command,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
        )
        return completed_process.stdout, completed_process.returncode == 0


class Illustrator(LilyPondIO):
    def get_openable_paths(self, output_paths) -> Sequence[pathlib.Path]:
        for path in output_paths:
            if path.suffix == ".pdf":
                yield path


class Player(LilyPondIO):
    def get_openable_paths(self, output_paths) -> Sequence[pathlib.Path]:
        for path in output_paths:
            if path.suffix in (".mid", ".midi"):
                yield path

    def get_string(self) -> str:
        lilypond_file = self.illustrable.__illustrate__(**self.keywords)
        assert hasattr(lilypond_file, "score_block")
        block = Block(name="midi")
        lilypond_file.score_block.items.append(block)
        return format(lilypond_file, "lilypond")


def graph(graphable, format_="pdf", layout="dot", verbose=False):
    return Grapher(
        graphable,
        format_=format_,
        layout=layout,
        output_directory=".",
        verbose=verbose,
    )()


def play(illustrable, return_timing=False, **keywords):
    player = Player(illustrable, **keywords)
    _, format_time, render_time, success, log = player()
    if not success:
        print(log)
    if return_timing:
        return format_time, render_time


def show(illustrable, return_timing=False, **keywords):
    illustrator = Illustrator(illustrable, **keywords)
    _, format_time, render_time, success, log = illustrator()
    if not success:
        print(log)
    if return_timing:
        return format_time, render_time
