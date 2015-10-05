import click

from l.core import _INCLUDING_DOT_AND_DOTDOT, ls
from l.project import project


VARIADIC = -1  # click uses -1 for nargs which is very hard to read


class Project(click.ParamType):
    name = "project"
    convert = lambda self, value, param, ctx : project(value)


PROJECT = Project()


@click.command()
@click.option(
    "-a", "--all",
    flag_value=_INCLUDING_DOT_AND_DOTDOT,
    help="Like -A, but also display '.' and '..'",
)
@click.option(
    "-A", "--almost-all", "all",
    flag_value="almost",
    help="Do not ignore entries that start with '.'",
)
@click.argument(
    "files",
    nargs=VARIADIC,
    type=PROJECT,
)
def run(all, files):
    """
    Project-oriented directory and file information lister.

    """

    ls(
        files=files or (project("."),),
        show_all=True if all == "almost" else all,
    )
