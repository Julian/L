from unittest import TestCase

from bp.memory import MemoryFS, MemoryPath

from l import project


class TestProjectDetection(TestCase):
    def setUp(self):
        self.fs = MemoryFS()
        self.root = MemoryPath(fs=self.fs, path=("test-dir",))
        self.root.createDirectory()

    def test_it_detects_git_repositories(self):
        self.root.child(".git").createDirectory()
        self.assertEqual(
            project.from_path(self.root),
            project.GitPath(
                git_dir=self.root.child(".git"),
                path=self.root,
            ),
        )

    def test_it_detects_hg_repositories(self):
        self.root.child(".hg").createDirectory()
        self.assertEqual(
            project.from_path(self.root),
            project.HgPath(hg_dir=self.root.child(".hg")),
        )

    def test_it_detects_normal_directories(self):
        self.assertEqual(project.from_path(self.root), self.root)
