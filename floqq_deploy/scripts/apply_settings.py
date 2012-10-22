"""Apply settings to an unpacked project.

The project is expected to be unpacked in:

   .deploy/current/<gae app name>/

If there is no settings found for `gae app name` then you need to configure
that, run `floqq-config -h` and `floqq-fetch-settings -h` for more help.

Example:

    $ floqq-apply-settings floqq-api
    Settings `.deploy/settings/floqq-api` applied to `.deploy/current/floqq-api`
"""
from __future__ import print_function
import sys
import os
import argparse

from floqq_deploy.settings import apply_settings
from floqq_deploy.exceptions import CommandFailed
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
        parser = parent.add_parser("apply-settings", **kwargs)
    else:
        parser = argparse.ArgumentParser(**kwargs)
    parser.add_argument("app_name", help="Application name")
    parser.add_argument("version", help="Application version")

    return parser


def handle(args):
    app_name = args.app_name
    version = args.version
    return process(app_name, version, settings=app_name)


def process(app_name, version, settings):
    try:
        settings, output = apply_settings(app_name, version, settings)
    except ValueError, e:
        raise CommandFailed(e.message)

    print("Settings {0!r} applied to {1!r}".format(settings, output))
    return settings, output


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
