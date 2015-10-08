from StringIO import StringIO
from textwrap import dedent
from unittest import TestCase

from bp.memory import MemoryFS, MemoryPath

from l import cli


class TestShow(TestCase):
    def setUp(self):
        self.fs = MemoryFS()
        self.root = MemoryPath(fs=self.fs, path=("test-dir",))
        self.root.createDirectory()

    def assertShows(self, result, **kwargs):
        stdout = StringIO()
        cli.show(stdout=stdout, **kwargs)
        self.assertEqual(
            stdout.getvalue(),
            dedent(result).strip("\n") + "\n",
        )

    def test_it_lists_directories(self):
        foo, bar = self.root.child("foo"), self.root.child("bar")
        foo.setContent("")
        bar.setContent("")

        self.assertShows(paths=[self.root], result="bar  foo")

    def test_it_lists_multiple_directories(self):
        one = self.root.child("one")
        one.createDirectory()
        one_two = one.child("two")
        one_two.setContent("")

        three = self.root.child("three")
        three.setContent("")

        self.assertShows(
            paths=[self.root, one],
            result="""
            /mem/test-dir:
            one  three

            /mem/test-dir/one:
            two
            """,
        )

