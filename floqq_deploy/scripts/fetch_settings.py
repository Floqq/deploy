"""Fetch project settings for a given app name.

The settings per each app are stored in:

   .deploy/settings/<app name>/

The path to the settings are specified in the configuration using the
`settings_url` param.

Example:

You can specify an URL for the floqq-api app and a local path to the
floqq-testing one:

    $ floqq-config floqq-api.settings_url https://myserver
    $ floqq-config floqq-testing.settings_url project/configuration/settings
    $ floqq-fetch-settings
    $ ls .deploy/settings
    floqq-api
    floqq-testing
"""
import sys
import os
import argparse

from floqq_deploy.settings import fetch
from floqq_deploy.exceptions import UnsupportedUrl, NoSettingsUrl, CommandFailed
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
        parser = parent.add_parser("fetch-settings", **kwargs)
    else:
        parser = argparse.ArgumentParser(**kwargs)
    parser.add_argument("app_name", help="Application name.")

    return parser


def handle(args):
    app_name = args.app_name
    process(app_name)


def process(app_name):
    try:
        url, settings_path = fetch(app_name)
    except (NoSettingsUrl, UnsupportedUrl), e:
        raise CommandFailed(e.message)

    print("Stored settings from {0!r} into {1!r}".format(url, settings_path))


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
