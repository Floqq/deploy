#
# Copyright (c) 2012 Floqq innovation SL. All Right Reserved
#

"""Decrypt settings.

Decrypt all the settings whose name is in the config file under
security.secure_settings param.
"""
from __future__ import print_function
import sys
import os
import argparse
import getpass

from floqq_deploy.security import decrypt_settings
from floqq_deploy.scripts import formatter
from floqq_deploy.exceptions import CommandFailed


def handle(args):
    settings_filename = "settings.py"
    app_name = args.app_name
    password = getpass.getpass("Decryption password: ")
    decrypt_settings(app_name, filename=settings_filename, key=password)


def main(argv=None):
    if argv is None:
        argv = sys.argv[1:]
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=formatter)
    parser.add_argument("app_name", help="Application name.")

    args = parser.parse_args(argv)
    try:
        handle(args)
    except CommandFailed, e:
        print(e.message)
        return 1


if __name__ == "__main__":
    sys.exit(main())
