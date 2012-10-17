"""Floqq

docs here
"""
from __future__ import print_function
import sys
import os
import argparse

from floqq_deploy.scripts import formatter
from floqq_deploy.scripts import (init, config, deploy, fetch_settings,
                                  compilemessages)
from floqq_deploy.exceptions import CommandFailed

_subcommands = {"init": init, "config": config, "deploy": deploy,
                "fetch-settings": fetch_settings,
                "compilemessages": compilemessages}

def handle(args):
    subcommand = args.subcommand
    _subcommands[args.subcommand].handle(args)


def main(argv=None):
    if argv is None:
        argv = sys.argv[1:]
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=formatter)
    subparsers = parser.add_subparsers(dest="subcommand",
                                       help="available commands")

    init_parser = init.get_parser(subparsers)
    config_parser = config.get_parser(subparsers)
    deploy_parser = deploy.get_parser(subparsers)
    fetch_settings_parser = fetch_settings.get_parser(subparsers)
    compilemessages_parser = compilemessages.get_parser(subparsers)

    args = parser.parse_args(argv)
    try:
        handle(args)
    except CommandFailed, e:
        print(e.message)
        return 1


if __name__ == "__main__":
    sys.exit(main())
