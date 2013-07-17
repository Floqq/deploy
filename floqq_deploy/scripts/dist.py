#
# Copyright (c) 2012 Floqq innovation SL. All Right Reserved
#

"""Concatenate, minify and add revision to static files.

This command will execute grunt and bower. It basically installs all
bower dependencies and then prepares a dist by running grunt:

    $ bower install
    $ grunt dist

This command is equivalent to django `manage.py compilemessages [options]`
"""
from __future__ import print_function
import sys
import os
import argparse

from floqq_deploy.dist import grunt, bower
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
        parser = parent.add_parser("dist", **kwargs)
    else:
        parser = argparse.ArgumentParser(**kwargs)
    parser.add_argument("app_name", help="Application name.")

    return parser


def handle(args):
    app_name = args.app_name
    return process(app_name)


def process(app_name):
    app_path = os.path.join(get_current_path(), app_name)
    if os.path.isdir(app_path):
        bower(app_path)
        grunt(app_path)
    else:
        raise CommandFailed("Can't find {0!r}".format(app_path))


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
