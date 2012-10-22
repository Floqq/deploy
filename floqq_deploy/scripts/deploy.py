"""Deploy the project.

Equivalent to:

    $ floqq-export
    $ floqq-prepare
    $ floqq-upload

Deploys the prepared project stored in .deploy/current/.
"""
from __future__ import print_function
import sys
import os
import argparse

from floqq_deploy import deploy
from floqq_deploy.db import get_current_path
from floqq_deploy.scripts import formatter, export, prepare, upload
from floqq_deploy.exceptions import CommandFailed


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
        parser = parent.add_parser("deploy", **kwargs)
    else:
        parser = argparse.ArgumentParser(**kwargs)
    parser.add_argument("tree", help="Git tree name")
    parser.add_argument("app_name", help="Application name.")
    parser.add_argument("version", help="Application version.")
    parser.add_argument("-l", "--locale", help=("The locale to process. "
                                                "Default is to process all."))
    parser.add_argument("-s", "--settings", help=("Different name of settings "
                                                  "to use."))

    return parser


def handle(args):
    export.handle(args)
    prepare.handle(args)
    upload.handle(args)


def main(argv=None):
    if argv is None:
        argv = sys.argv[1:]
    parser = get_parser()
    args = parser.parse_args(argv)
    try:
        handle(args)
    except CommandFailed, e:
        print(e.message)
        return 1


if __name__ == "__main__":
    sys.exit(main())
