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
def run(all, paths, stdout=stdout):
    """
    Project-oriented directory and file information lister.

    """

    stdout.write(show(paths=paths or (project("."),)))


def show(paths):
    if len(paths) == 1:
        children = (
            child for child in ls(path=paths[0])
            if not child.basename().startswith(".")
        )
        output = _formatted_children(children)
    else:
        contents = sorted(
            ((path, ls(path=path)) for path in paths),
            key=lambda (path, _) : path.path,
        )
        output = "\n".join(
            "{parent.path}:\n{children}".format(
                parent=parent,
                children=_formatted_children(
                    children=(
                        child for child in children
                        if not child.basename().startswith(".")
                    )
                )
            ) for parent, children in contents
        )
    return output


def _formatted_children(children):
    return "  ".join(sorted(path.basename() for path in children)) + "\n"
