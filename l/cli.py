from sys import stdout

import click

from l.core import show
from l.project import project


VARIADIC = -1  # click uses -1 for nargs which is very hard to read


class Project(click.ParamType):
    name = "project"
    convert = lambda self, value, param, ctx : project(value)


PROJECT = Project()


@click.command()
@click.option(
    "-a", "--all",
    flag_value="all",
    help="Like -A, but also display '.' and '..'",
)
@click.option(
    "-A", "--almost-all", "all",
    flag_value="almost",
    help="Do not ignore entries that start with '.'",
)
@click.argument(
    "paths",
    nargs=VARIADIC,
    type=PROJECT,
)
def run(all, paths, stdout=stdout):
    """
    Project-oriented directory and file information lister.

    """

    stdout.write(show(paths=paths or (project("."),)))
