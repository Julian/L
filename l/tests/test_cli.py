from StringIO import StringIO
from textwrap import dedent
from unittest import TestCase

from bp.memory import MemoryFS, MemoryPath
from hypothesis import given, strategies

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

    def children(self, *new, **kwargs):
        of = kwargs.pop("of", self.root)
        assert not kwargs

        of.createDirectory()
        for child in new:
            path = of.child(child)
            path.setContent("")
            yield path

    def test_it_lists_directories(self):
        foo, bar = self.children("foo", "bar")
        self.assertShows(paths=[self.root], result="bar  foo")

    def test_it_lists_multiple_directories(self):
        one = self.root.child("one")
        two, four = self.children("two", "four", of=one)

        three, = self.children("three")

        self.assertShows(
            paths=[self.root, one],
            result="""
            /mem/test-dir:
            one  three

            /mem/test-dir/one:
            four  two
            """,
        )


    def test_it_ignores_hidden_files_by_default(self):
        foo, hidden = self.children("foo", ".hidden")
        self.assertShows(paths=[self.root], result="foo")
