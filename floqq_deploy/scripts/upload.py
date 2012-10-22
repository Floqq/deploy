#
# Copyright (c) 2012 Floqq innovation SL. All Right Reserved
#

"""Upload the project to GAE.

Uploads the prepared project stored in .deploy/current/.
"""
from __future__ import print_function
import sys
import os
import argparse

from floqq_deploy import deploy
from floqq_deploy.db import get_current_path
from floqq_deploy.scripts import formatter
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
        parser = parent.add_parser("upload", **kwargs)
    else:
        parser = argparse.ArgumentParser(**kwargs)
    parser.add_argument("app_name", help="Application name.")

    return parser


def handle(args):
    app_name = args.app_name
    app_path = os.path.join(get_current_path(), app_name)
    return process(app_name, app_path)


def process(app_name, app_path):
    if os.path.isdir(app_path):
        deploy.run(app_path)
    else:
        raise CommandFailed("{0!r} is not prepared for deployment".format(
                            app_name))


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
