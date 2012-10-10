"""Set configuration parameters.

Configuration parameters are stored in .deploy/config, with this command you
modify or add new parameters to it.

Parameters are named using the format <environment>.<param name> where
environment should be one of the possible environments (production, staging,
testing)

Example:
    config production.settings_url http://myurl...
"""
import sys
import os
import argparse

from floqq_deploy.db import config
from floqq_deploy.scripts import formatter
from floqq_deploy.utils.scripts import is_valid_param_name


def main(argv=None):
    if argv is None:
        argv = sys.argv[1:]
    parser = argparse.ArgumentParser(description=__doc__,
                                    formatter_class=formatter)
    parser.add_argument("-d", "--delete", action="store_true",
                        help="Delete this parameter from settings.")
    parser.add_argument("name", type=is_valid_param_name, help="Parameter name")
    parser.add_argument("value", nargs="?", help="Parameter value")

    args = parser.parse_args(argv)

    env, name = args.name.split(".")
    value = args.value
    delete = args.delete

    option = config(name=args.name, environment=env, value=value, delete=delete)

    if value is None:
        print option


if __name__ == "__main__":
    sys.exit(main())
