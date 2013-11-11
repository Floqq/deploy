#
# Copyright (c) 2012 Floqq innovation SL. All Right Reserved
#

"""Compile .po files to .mo files for use with builtin gettext support.

This command is equivalent to django `manage.py compilemessages [options]`
"""
from __future__ import print_function
import sys
import os
import argparse

from floqq_deploy.translation import django_compilemessages
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
        parser = parent.add_parser("compilemessages", **kwargs)
    else:
        parser = argparse.ArgumentParser(**kwargs)
    parser.add_argument("app_name", help="Application name.")
    parser.add_argument("-l", "--locale", help=("The locale to process. "
                                                "Default is to process all."))

    return parser


def handle(args):
    app_name = args.app_name
    locale = args.locale
    return process(app_name, locale)


def process(app_name, locale=None):
    app_path = os.path.join(get_current_path(), app_name)
    if os.path.isdir(app_path):
        print("Compiling .po files")
        django_compilemessages(app_path, locale)
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
