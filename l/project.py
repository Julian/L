from subprocess import check_output

from bp.filepath import FilePath


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
