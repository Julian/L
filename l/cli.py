from argparse import ArgumentParser
from subprocess import check_output

from bp.filepath import FilePath

from l.core import _INCLUDING_DOT_AND_DOTDOT, ls


def project(raw_path):
    path = FilePath(raw_path)
    git_dir = path.child(".git")
    if git_dir.isdir():
        return GitPath(git_dir)
    return path


class GitPath(object):
    def __init__(self, path):
        self.path = path

    def listdir(self):
        return check_output(
            [
                "git", "--git-dir", self.path.path,
                "ls-tree", "--name-only", "HEAD",
            ],
        ).splitlines()


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
    type=project,
    default=(project("."),),
    help="the directory whose contents to list",
)


def run():
    arguments = vars(parser.parse_args())
    ls(
        files=arguments["files"],
        show_all=arguments["all"],
    )
