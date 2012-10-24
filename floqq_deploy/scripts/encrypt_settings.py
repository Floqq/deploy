#
# Copyright (c) 2012 Floqq innovation SL. All Right Reserved
#

"""Encrypt settings.

Modifies settings file in:
    
    .deploy/current/<app name>
    
By encrypting the settings which name is in the config file under:
    
    security.secure_settings param.
"""
from __future__ import print_function
import sys
import os
import argparse
import getpass

from floqq_deploy.security import encrypt_settings
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
        parser = parent.add_parser("encrypt-settings", **kwargs)
    else:
        parser = argparse.ArgumentParser(**kwargs)
    parser.add_argument("app_name", help="Application name.")

    return parser


def handle(args):
    app_name = args.app_name
    return process(app_name)


def process(app_name, settings_filename=None):
    if settings_filename is None:
        settings_filename = "settings.py"
    password = getpass.getpass("Encryption password: ")
    if password:
        print("Encrypting...")
        encrypt_settings(app_name, filename=settings_filename, key=password)
    else:
        print("Encryption skipped.")


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
