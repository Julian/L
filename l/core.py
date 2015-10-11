_INCLUDING_DOT_AND_DOTDOT = "..."


def ls(path):
    return path.children()


def show(paths):
    output = (_unhidden(ls(path=path)) for path in paths)
    if len(paths) > 1:
        output = _labelled(
            sorted(zip(paths, output), key=lambda (path, _) : path.path)
        )
    return "\n".join(output)


def _labelled(parents_and_children):
    return (
        "{parent.path}:\n{children}".format(parent=parent, children=children)
        for parent, children in parents_and_children
    )


def _unhidden(children):
    return _formatted_children(
        children=(
            child for child in children if not child.basename().startswith(".")
        )
    )


def _formatted_children(children):
    return "  ".join(sorted(path.basename() for path in children)) + "\n"
