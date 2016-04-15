import errno
import os
import subprocess

from bp.abstract import IFilePath
from bp.filepath import FilePath
from bp.generic import genericWalk
from characteristic import Attribute, attributes
from zope.interface import implementer


def from_path(path):
    git_dir = path.child(".git")
    if git_dir.isdir():
        return GitPath(git_dir=git_dir, path=path)

    try:
        git = subprocess.Popen(
            ["git", "rev-parse", "--is-inside-work-tree"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            cwd=path.path,
        )
    except OSError as error:
        # The cwd didn't exist
        if error.errno != errno.ENOENT:
            raise
    else:
        stdout, _ = git.communicate()
        if stdout == "true\n":
            return GitPath(path=path)

    hg_dir = path.child(".hg")
    if hg_dir.isdir():
        return HgPath(hg_dir=hg_dir)

    return path


# TODO: Really betterpath should have a separate interface for like,
#       file systems, or listable things.
@implementer(IFilePath)
@attributes(
    [
        Attribute(name="_git_dir", default_value=None, exclude_from_repr=True),
        Attribute(name="_path"),
    ],
)
class GitPath(object):
    def listdir(self):
        argv = ["git"]
        if self._git_dir is not None:
            argv.extend(["--git-dir", self._git_dir.path])
        argv.extend(["ls-tree", "--name-only", "HEAD", self.path])
        return subprocess.check_output(argv).splitlines()

    def children(self):
        return [FilePath(path) for path in self.listdir()]


@implementer(IFilePath)
@attributes(
    [
        Attribute(name="_hg_dir", exclude_from_repr=True),
    ],
)
class HgPath(object):
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


def _proxy_for_attribute(name):
    return property(lambda self: getattr(self._path, name))


for attribute in [
    "basename",
    "changed",
    "child",
    "createDirectory",
    "exists",
    "getAccessTime",
    "getContent",
    "getModificationTime",
    "getStatusChangeTime",
    "getsize",
    "isdir",
    "isfile",
    "islink",
    "open",
    "parent",
    "path",
    "realpath",
    "remove",
    "setContent",
    "sibling",
    "walk",
]:
    proxy = _proxy_for_attribute(name=attribute)
    setattr(GitPath, attribute, proxy)
    setattr(HgPath, attribute, proxy)
