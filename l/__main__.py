import os
import sys

from l.cli import run


def main():
    run()
    sys.exit(os.EX_OK)


if __name__ == "__main__":
    main()
