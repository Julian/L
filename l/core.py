class _FakeFilePath(object):
    """
    A thing that isn't really a path but which we trick outputting for.

    """

    def __init__(self, path):
        self.path = path

    def basename(self):
        return self.path

    def isdir(self):
        return False


def ls(path):
    return [
        child for child in ls_almost_all(path=path)
        if not child.basename().startswith(".")
    ]


def ls_almost_all(path):
    return path.children()


def ls_all(path):
    return [_FakeFilePath("."), _FakeFilePath("..")] + path.children()


def columnized(paths):
    if len(paths) == 1:
        (_, children), = paths
        return _tabularized(children)
    return "\n".join(_labelled(sorted(paths)))


def _labelled(parents_and_children):
    return (
        "{parent.path}:\n{children}".format(
            parent=parent,
            children=_tabularized(children),
        )
        for parent, children in parents_and_children
    )


def _tabularized(children):
    return "  ".join(sorted(child.basename() for child in children)) + "\n"


def one_per_line(parents_and_children):
    if len(parents_and_children) == 1:
        paths = (
            child.basename()
            for _, children in parents_and_children
            for child in sorted(children)
        )
    else:
        paths = sorted(
            child.path
            for _, children in parents_and_children
            for child in children
        )

    return "\n".join(paths) + "\n"


def recurse(path, ls):
    working = [path]
    while working:
        path = working.pop()
        children = ls(path=path)
        yield path, children
        working.extend(child for child in children if child.isdir())


def flat(path, ls):
    return [(path, ls(path=path))]
