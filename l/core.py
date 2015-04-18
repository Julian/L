from subprocess import check_output
import os


def run(arguments):
    for directory in arguments["directory"]:
        git_dir = directory.child(".git")
        if git_dir.isdir():
            files = check_output(
                ["git", "--git-dir", git_dir.path, "ls-files"],
            ).splitlines()
        else:
            files = directory.listdir()

        for file in files:
            print file
