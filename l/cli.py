from argparse import ArgumentParser

from bp.filepath import FilePath


_INCLUDING_DOT_AND_DOTDOT = "..."

parser = ArgumentParser(
    description="Project-oriented directory and file information lister.",
)
parser.add_argument(
    "-a", "--all",
    action="store_const",
    dest="all",
    const=_INCLUDING_DOT_AND_DOTDOT,
    help="-A, but also display . and ..",
)
parser.add_argument(
    "-A", "--almost-all",
    action="store_true",
    dest="all",
    help="do not ignore entries that start with .",
)
parser.add_argument(
    "files",
    metavar="FILE",
    nargs="*",
    type=FilePath,
    default=(FilePath("."),),
    help="the directory whose contents to list",
)
