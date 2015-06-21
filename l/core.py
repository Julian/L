from subprocess import check_output
import os

from l.cli import _INCLUDING_DOT_AND_DOTDOT


def run(arguments):
    for directory in arguments["directory"]:
        git_dir = directory.child(".git")
        if git_dir.isdir():
            files = check_output(
                [
                    "git", "--git-dir", git_dir.path,
                    "ls-tree", "--name-only", "HEAD",
                ],
            ).splitlines()
        else:
            files = directory.listdir()

        show_all = arguments["all"]
        if show_all == _INCLUDING_DOT_AND_DOTDOT:
            print ".\n.."
        elif not show_all:
            files = [file for file in files if not file.startswith(".")]

        print "  ".join(files)
