"""Set configuration parameters.

Configuration parameters are stored in:
    
    .deploy/config
    
With this command you modify or add new parameters to it.

Parameters are named using the format <gae app name>.<param name> where
`gae app name` is the name of your GAE application.

Examples:

    $ floqq-config mysuperapp.settings_url http://myurl...
    $ floqq-config mysuperapp.current_version awesome
    $ floqq-config mysuperapp.previous_version not-so-awesome
"""
import sys
import os
import argparse

from floqq_deploy.db import config
from floqq_deploy.scripts import formatter
from floqq_deploy.utils.scripts import is_valid_param_name
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
        parser = parent.add_parser("config", **kwargs)
    else:
        parser = argparse.ArgumentParser(**kwargs)
    parser.add_argument("-d", "--delete", action="store_true",
                        help="Delete this parameter from settings.")
    parser.add_argument("name", type=is_valid_param_name,
                        help="Parameter name")
    parser.add_argument("value", nargs="?", help="Parameter value")

    return parser


def handle(args):
    section, name = args.name.split(".", 1)
    value = args.value
    delete = args.delete
    option = config(name=name, section=section, value=value, delete=delete)
    if value is None:
        print option


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
