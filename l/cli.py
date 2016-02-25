from sys import stdout
import errno

from appdirs import user_config_dir
from bp.filepath import FilePath
import click
import toml

from l import core, project


_I_STILL_HATE_EVERYTHING = object()  # click uses None for "no flag_value"
VARIADIC = -1  # click uses -1 for nargs which is very hard to read


class Project(click.ParamType):
    name = "project"

    def convert(self, value, param, context):
        return project.from_path(value)


PROJECT = Project()


def run(
    paths,
    output=_I_STILL_HATE_EVERYTHING,
    recurse=core.flat,
    sort_by=lambda x : x,
    ls=core.ls,
    stdout=stdout,
):
    """
    Project-oriented directory and file information lister.

    """

    if output is _I_STILL_HATE_EVERYTHING:
        output = core.columnized if stdout.isatty() else core.one_per_line

    def _sort_by(thing):
        return not getattr(thing, "_always_sorts_first", False), sort_by(thing)

    contents = [
        path_and_children
        for path in paths or (project.from_path(FilePath(".")),)
        for path_and_children in recurse(path=path, ls=ls)
    ]
    for line in output(contents, sort_by=_sort_by):
        stdout.write(line)
        stdout.write("\n")


I_hate_everything = [
    click.command(context_settings=dict(help_option_names=["-h", "--help"])),
    click.option(
        "-1", "--one-per-line", "output",
        flag_value=core.one_per_line,
        help="Force output to be one entry per line. "
            "Note that unlike ls, when recursively listing directories, "
            "also forces output to not be grouped by subdirectory.",
    ),
    click.option(
        "--many-per-line", "output",
        flag_value=core.columnized,
        help="Show human-readable, labelled output.",
    ),
    click.option(
        "--tree", "output",
        flag_value=core.as_tree,
        help="Output contents as a tree, like tree(1)",
    ),
    click.option(
        "--auto-output", "output",
        flag_value=_I_STILL_HATE_EVERYTHING,
        default=True,
        help="Pick an output format intelligently.",
    ),
    click.option(
        "-a", "--all", "ls",
        flag_value=core.ls_all,
        help="Like -A, but also display '.' and '..'",
    ),
    click.option(
        "-A", "--almost-all", "ls",
        flag_value=core.ls_almost_all,
        help="Do not ignore entries that start with '.'",
    ),
    click.option(
        "--some", "ls",
        flag_value=core.ls,
        default=True,
        help="Ignore entities that start with '.'",
    ),
    click.option(
        "-R", "--recursive", "recurse",
        flag_value=core.recurse,
        help="Recursively list the project.",
    ),
    click.option(
        "--no-recursive", "recurse",
        flag_value=core.flat,
        default=True,
        help="Do not recursively list the project.",
    ),
    click.option(
        "--group-directories-first", "sort_by",
        flag_value=core.group_directories_first,
        help="Show directories first in output",
    ),
    click.option(
        "--no-group-directories-first", "sort_by",
        flag_value=lambda thing : thing,
        default=True,
        help="Show content in alphabetical order regardless of type",
    ),
    click.argument(
        "paths",
        nargs=VARIADIC,
        type=PROJECT,
    ),
]

_main = run
for add_cli_thing_to in reversed(I_hate_everything):
    _main = add_cli_thing_to(_main)


def main():
    config_dir = FilePath(user_config_dir("l"))
    try:
        contents = config_dir.child("config.toml").getContent()
    except IOError as error:
        if error.errno != errno.ENOENT:
            raise
        config = {}
    else:
        config = toml.loads(contents)
    _main(default_map=config)
