import click

from l.core import _INCLUDING_DOT_AND_DOTDOT, ls
from l.project import project


@click.command()
@click.option(
    "-a", "--all",
    flag_value=_INCLUDING_DOT_AND_DOTDOT,
    help="Like -A, but also display '.' and '..'",
)
@click.option(
    "-A", "--almost-all", "all",
    flag_value=True,
    help="Do not ignore entries that start with '.'",
)
@click.argument("files", nargs=-1)
def run(all, files):
    """
    Project-oriented directory and file information lister.

    """

    ls(files=files, show_all=all)
