"""
Module to support call with :file:`__main__.py`. Used to support the following
call:

$ python3 -m semver ...
"""
import os.path
import sys
from typing import List

from semver import cli


def main(cliargs: List[str] = None) -> int:
    if __package__ == "":
        path = os.path.dirname(os.path.dirname(__file__))
        sys.path[0:0] = [path]

    return cli.main(cliargs)


if __name__ == "__main__":
    sys.exit(main(sys.argv))
