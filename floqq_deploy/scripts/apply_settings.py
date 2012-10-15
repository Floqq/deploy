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
from floqq_deploy.scripts import formatter


def main(argv=None):
    if argv is None:
        argv = sys.argv[1:]
    parser = argparse.ArgumentParser(description=__doc__,
                                    formatter_class=formatter)
    parser.add_argument("app_name", help="Application name")
    parser.add_argument("version", help="Application version")

    args = parser.parse_args(argv)

    try:
        settings, output = apply_settings(args.app_name, version=args.version)
    except ValueError:
        print("No settings found. Run `floqq-fetch-settings -h` for more help.")
        return 1

    print("Settings {0!r} applied to {1!r}".format(settings, output))


if __name__ == "__main__":
    sys.exit(main())
