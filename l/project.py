from subprocess import check_output
import os

from bp.filepath import FilePath
from characteristic import Attribute, attributes


def from_path(path):
    git_dir = path.child(".git")
    if git_dir.isdir():
        return GitPath(git_dir=git_dir)

    hg_dir = path.child(".hg")
    if hg_dir.isdir():
        return HgPath(hg_dir=hg_dir)

    return path


# TODO: Really betterpath should have a separate interface for like,
#       file systems, or listable things.
@attributes(
    [
        Attribute(name="_git_dir"),
    ],
)
class GitPath(object):
    @property
    def path(self):
        return self._git_dir.path

    @property
    def basename(self):
        return self._git_dir.basename

    def listdir(self):
        return check_output(
            [
                "git", "--git-dir", self.path,
                "ls-tree", "--name-only", "HEAD",
            ],
        ).splitlines()

    def children(self):
        return [FilePath(path) for path in self.listdir()]


@attributes(
    [
        Attribute(name="_hg_dir"),
    ],
)
class HgPath(object):
    @property
    def path(self):
        return self._hg_dir.path

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
