"""Prepare the project for deploy.

Equivalent to run:

    $ floqq-export
    $ floqq-fetch-settings
    $ floqq-unpack
    $ floqq-apply-settings
    $ floqq-decrypt-settings
    $ floqq-compilemessages
    $ floqq-dist
"""
from __future__ import print_function
import sys
import os
import argparse

from floqq_deploy.db import project_unpack
from floqq_deploy.settings import apply_settings
from floqq_deploy.scripts import (formatter, fetch_settings, decrypt_settings,
                                  apply_settings, compilemessages, unpack,
                                  export, dist)
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
        parser = parent.add_parser("prepare", **kwargs)
    else:
        parser = argparse.ArgumentParser(**kwargs)
    parser.add_argument("tree", help="Git tree name")
    parser.add_argument("app_name", help="Application name")
    parser.add_argument("version", help="Application version")
    parser.add_argument("-s", "--settings", help=("Different name of settings "
                                                  "to use."))
    parser.add_argument("-n", "--skip-dist", action="store_true",
                        help="Don't run dist subcommand")

    return parser


def handle(args):
    tree = args.tree
    app_name = args.app_name
    settings = args.settings
    version = args.version
    skip_dist = args.skip_dist
    return process(tree, app_name, version, settings, skip_dist=skip_dist)


def process(tree, app_name, version, settings=None, skip_dist=False):
    if settings is None:
        settings = app_name
    export.process(tree)
    fetch_settings.process(settings)
    output = unpack.process(app_name)
    apply_settings.process(app_name, version, settings)
    decrypt_settings.process(app_name)
    compilemessages.process(app_name)
    if not skip_dist:
        dist.process(app_name)

    print("Project prepared at {0!r}".format(output))


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
