import os
import subprocess

from bp.filepath import FilePath
from characteristic import Attribute, attributes


def from_path(path):
    git_dir = path.child(".git")
    if git_dir.isdir():
        return GitPath(git_dir=git_dir, path=path)
    else:
        git = subprocess.Popen(
            ["git", "rev-parse", "--is-inside-work-tree"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            cwd=path.path,
        )
        stdout, _ = git.communicate()
        if stdout == "true\n":
            return GitPath(path=path)

    hg_dir = path.child(".hg")
    if hg_dir.isdir():
        return HgPath(hg_dir=hg_dir)

    return path


# TODO: Really betterpath should have a separate interface for like,
#       file systems, or listable things.
@attributes(
    [
        Attribute(name="_git_dir", default_value=None),
        Attribute(name="_path"),
    ],
)
class GitPath(object):
    @property
    def path(self):
        return self._path.path

    @property
    def basename(self):
        return self._path.basename

    def listdir(self):
        argv = ["git"]
        if self._git_dir is not None:
            argv.extend(["--git-dir", self._git_dir.path])
        argv.extend(["ls-tree", "--name-only", "HEAD", self.path])
        return subprocess.check_output(argv).splitlines()

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
        paths = subprocess.check_output(
            [
                "hg", "--repository", self.path,
                "files", "--include", "*", "--exclude", "*/*",
            ],
        )
        return (os.path.basename(path) for path in paths.splitlines())

    def children(self):
        return [FilePath(path) for path in self.listdir()]
