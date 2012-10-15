"""Prepare the project for deploy.

Equivalent to run:

    $ floqq-fetch-settings
    $ floqq-unpack
    $ floqq-apply-settings
"""
from __future__ import print_function
import sys
import os
import argparse

from floqq_deploy.db import project_unpack
from floqq_deploy.settings import apply_settings
from floqq_deploy.scripts import formatter, fetch_settings
from floqq_deploy.exceptions import CommandFailed


def handle(args):
    app_name = args.app_name
    fetch_settings.handle(args)
    try:
        output = project_unpack(app_name)
        apply_settings(app_name, version=args.version)
    except ValueError, e:
        raise CommandFailed(e.message)

    print("Project prepared at {0!r}".format(output))


def main(argv=None):
    if argv is None:
        argv = sys.argv[1:]
    parser = argparse.ArgumentParser(description=__doc__,
                                    formatter_class=formatter)
    parser.add_argument("app_name", help="Application name")
    parser.add_argument("version", help="Application version")

    args = parser.parse_args(argv)
    try:
        handle(args)
    except CommandFailed, e:
        print(e.message)
        return 1


if __name__ == "__main__":
    sys.exit(main())
