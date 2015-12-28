from subprocess import check_output
import os

from bp.filepath import FilePath


def project(raw_path):
    path = FilePath(raw_path)

    git_dir = path.child(".git")
    if git_dir.isdir():
        return GitPath(git_dir)

    hg_dir = path.child(".hg")
    if hg_dir.isdir():
        return HgPath(path)

    return path


# TODO: Really betterpath should have a separate interface for like,
#       file systems, or listable things.
class GitPath(object):
    def __init__(self, path):
        self._path = path

    @property
    def path(self):
        return self._path.path

    @property
    def basename(self):
        return self._path.basename

    def listdir(self):
        return check_output(
            [
                "git", "--git-dir", self.path,
                "ls-tree", "--name-only", "HEAD",
            ],
        ).splitlines()

    def children(self):
        return [FilePath(path) for path in self.listdir()]


class HgPath(object):
    def __init__(self, path):
        self._path = path

    @property
    def path(self):
        return self._path.path

    def listdir(self):
        paths = check_output(
            [
                "hg", "--repository", self.path,
                "files", "--include", "*", "--exclude", "*/*",
            ],
        )
        return (os.path.basename(path) for path in paths.splitlines())

    def children(self):
        return [FilePath(path) for path in self.listdir()]
