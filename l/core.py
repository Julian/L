def ls(path):
    for child in path.children():
        name = child.basename()
        if name.startswith("."):
            continue
        yield name


def ls_almost_all(path):
    return path.listdir()


def show(paths):
    output = (_formatted_children(ls(path=path)) for path in paths)
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


def _formatted_children(children):
    return "  ".join(sorted(children)) + "\n"
