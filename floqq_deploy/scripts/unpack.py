"""Unpacks the project for deploy.

Store the project referenced by .deploy/HEAD in:

   .deploy/current/<gae app name>/

If there is no ref in HEAD then you need to first export your project. Run
`floqq-export -h` for more help.

Example:

    $ floqq-prepare floqq-api
    $ ls .deploy/current
    floqq-api
"""
from __future__ import print_function
import sys
import os
import argparse

from floqq_deploy.git import get_archive_filename
from floqq_deploy.db import project_unpack
from floqq_deploy.scripts import formatter


def main(argv=None):
    if argv is None:
        argv = sys.argv[1:]
    parser = argparse.ArgumentParser(description=__doc__,
                                    formatter_class=formatter)
    parser.add_argument("app_name", help="Application name")

    args = parser.parse_args(argv)

    app_name = args.app_name
    try:
        output = project_unpack(app_name)
    except ValueError:
        print("No ref found. Run `floqq-prepare -h` for more help.")
        return 1

    print("Project unpacked at {0!r}".format(output))


if __name__ == "__main__":
    sys.exit(main())
