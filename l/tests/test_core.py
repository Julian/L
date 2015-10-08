from unittest import TestCase

from bp.memory import MemoryFS, MemoryPath

from l.core import ls


class TestLS(TestCase):
    def setUp(self):
        self.fs = MemoryFS()
        self.root = MemoryPath(fs=self.fs, path=("test-dir",))
        self.root.createDirectory()

    def test_it_lists_directories(self):
        one, two = self.root.child("one"), self.root.child("two")
        one.setContent("")
        two.setContent("")

        files = ls(path=self.root)

        self.assertEqual(files, [one, two])
