from sys import stdout

import click

from l.core import (
    columnized, ls, ls_almost_all, ls_all, one_per_line, recurse, flat,
)
from l.project import project


VARIADIC = -1  # click uses -1 for nargs which is very hard to read


class Project(click.ParamType):
    name = "project"
    convert = lambda self, value, param, ctx : project(value)


PROJECT = Project()


def run(paths, recurse, output, ls=ls, stdout=stdout):
    """
    Project-oriented directory and file information lister.

    """

    contents = [
        path_and_children
        for path in paths or (project("."),)
        for path_and_children in recurse(path=path, ls=ls)
    ]
    stdout.write(output(contents))


I_hate_everything = [
    click.command(context_settings=dict(help_option_names=["-h", "--help"])),
    click.option(
        "-1", "--one-per-line", "output",
        flag_value=one_per_line,
        help="Force output to be one entry per line. "
            "Note that unlike ls, when recursively listing directories, "
            "also forces output to not be grouped by subdirectory.",
    ),
    click.option(
        "--many-per-line", "output",
        flag_value=columnized,
        default=True,
        help="Show human-readable, labelled output.",
    ),
    click.option(
        "-a", "--all", "ls",
        flag_value=ls_all,
        help="Like -A, but also display '.' and '..'",
    ),
    click.option(
        "-A", "--almost-all", "ls",
        flag_value=ls_almost_all,
        help="Do not ignore entries that start with '.'",
    ),
    click.option(
        "--some", "ls",
        flag_value=ls,
        default=True,
        help="Ignore entities that start with '.'",
    ),
    click.option(
        "-R", "--recursive", "recurse",
        flag_value=recurse,
        help="Recursively list the project.",
    ),
    click.option(
        "--no-recursive", "recurse",
        flag_value=flat,
        default=True,
        help="Do not recursively list the project.",
    ),
    click.argument(
        "paths",
        nargs=VARIADIC,
        type=PROJECT,
    ),
]

main = run
for add_cli_thing_to in reversed(I_hate_everything):
    main = add_cli_thing_to(main)
