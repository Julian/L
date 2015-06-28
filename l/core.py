from subprocess import check_output
import os

from l.cli import _INCLUDING_DOT_AND_DOTDOT


def run(arguments):
    for file in arguments["files"]:
        git_dir = file.child(".git")
        if git_dir.isdir():
            files = check_output(
                [
                    "git", "--git-dir", git_dir.path,
                    "ls-tree", "--name-only", "HEAD",
                ],
            ).splitlines()
        else:
            files = file.listdir()

        show_all = arguments["all"]
        if show_all == _INCLUDING_DOT_AND_DOTDOT:
            print ".  .. ",
        elif not show_all:
            files = [file for file in files if not file.startswith(".")]

        print "  ".join(files)
