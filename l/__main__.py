import os
import sys

from l.cli import parser
from l.core import run


def main():
    run(arguments=vars(parser.parse_args()))
    sys.exit(os.EX_OK)


if __name__ == "__main__":
    main()
