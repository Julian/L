_INCLUDING_DOT_AND_DOTDOT = "..."


def ls(files, show_all=False):
    for file in files:
        files = file.listdir()
        if show_all == _INCLUDING_DOT_AND_DOTDOT:
            print ".  .. ",
        elif not show_all:
            files = [file for file in files if not file.startswith(".")]

        print "  ".join(files)
