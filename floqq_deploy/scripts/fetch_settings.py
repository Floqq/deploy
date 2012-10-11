"""Fetch project settings for each environment.

The settings per each enviroment are stored in:

   .deploy/settings/<environment name>/

The path to the settings are specified in the configuration using the
`settings_url` param.

Example:

You can specify an URL for the production environment and a local path to the
testing one:

    $ floqq-config production.settings_url https://myserver
    $ floqq-config testing.settings_url project/configuration/settings
    $ floqq-fetch-settings
    $ ls .deploy/settings
    production
    testing
"""
import sys
import os
import argparse

from floqq_deploy.db import ENVIRONMENTS, fetch_settings, config
from floqq_deploy.exceptions import UnsupportedUrl
from floqq_deploy.scripts import formatter
from floqq_deploy.utils.scripts import is_valid_environment


def fetch(env):
    print "Fetching %r settings..." % env,
    url = config("settings_url", env)
    try:
        fetch_settings(url, env)
    except ValueError:
        print "FAILED"
    except UnsupportedUrl, e:
        print e.message
    else:
        print


def main(argv=None):
    if argv is None:
        argv = sys.argv[1:]
    parser = argparse.ArgumentParser(description=__doc__,
                                    formatter_class=formatter)
    parser.add_argument("env", type=is_valid_environment, nargs="?",
                        help="Environment name")

    args = parser.parse_args(argv)

    env = args.env
    if env is None:
        for env in ENVIRONMENTS:
            fetch(env)
    else:
        fetch(env)


if __name__ == "__main__":
    sys.exit(main())
