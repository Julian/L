def ls(path):
    return [
        child for child in path.children()
        if not child.basename().startswith(".")
    ]


def ls_almost_all(path):
    return path.listdir()


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
