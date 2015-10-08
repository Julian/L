from sys import stdout

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
    "paths",
    nargs=VARIADIC,
    type=PROJECT,
)
def run(all, paths):
    """
    Project-oriented directory and file information lister.

    """

    show(paths=paths or (project("."),))


def show(paths, stdout=stdout):
    if len(paths) == 1:
        output = _formatted_children(ls(path=paths[0]))
    else:
        contents = sorted(
            ((path, ls(path=path)) for path in paths),
            key=lambda (path, _) : path.path,
        )
        output = "\n".join(
            "{parent.path}:\n{children}".format(
                parent=parent, children=_formatted_children(children=children),
            ) for parent, children in contents
        )
    stdout.write(output)


def _formatted_children(children):
    return "  ".join(sorted(path.basename() for path in children)) + "\n"
