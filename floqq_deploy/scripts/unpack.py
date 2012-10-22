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


def get_parser(parent=None):
    """Get the argument parser.

    Params
        parent (optional): object returned by another parser `add_subparsers`
                           method.

    Returns
        The argument parser object.
    """
    kwargs = dict(description=__doc__, formatter_class=formatter)
    if parent is not None:
        parser = parent.add_parser("unpack", **kwargs)
    else:
        parser = argparse.ArgumentParser(**kwargs)
    parser.add_argument("app_name", help="Application name")

    return parser

def handle(args):
    app_name = args.app_name
    return process(app_name)


def process(app_name):
    try:
        output = project_unpack(app_name)
    except ValueError, e:
        raise CommandFailed(e.message)

    print("Project unpacked at {0!r}".format(output))
    return output


def main(argv=None):
    if argv is None:
        argv = sys.argv[1:]
    args = parser.parse_args(argv)
    try:
        handle(args)
    except CommandFailed, e:
        print(e.message)
        return 1


if __name__ == "__main__":
    sys.exit(main())
