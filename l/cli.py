from argparse import ArgumentParser

from bp.filepath import FilePath


parser = ArgumentParser(
    description="Project-oriented directory lister.",
)
parser.add_argument(
    "directory",
    nargs="*",
    type=FilePath,
    default=(FilePath("."),),
    help="the directory whose contents to list",
)
