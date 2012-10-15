"""Initializes the db in the current project path.

It will create a .deploy directory with the following structure:

    .deploy/
        config
        settings/
        versions/
        HEAD/

Where:

    config: Is a file holding some configuration parameters.
    settings: A directory of settings to apply to the project.
    versions: Will contain all the git-exported trees named as
              <commit id>.tar.
    HEAD: Will contain what is actually gonna be deployed.

Example:

    $ cd myproject
    $ floqq-init
    $ tree .deploy
    +--.deploy
       +--HEAD/
       +--config
       +--settings/
       +--versions/
"""
from __future__ import print_function
import sys
import os
import argparse

from floqq_deploy.db import init
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
        parser = parent.add_parser("init", **kwargs)
    else:
        parser = argparse.ArgumentParser(**kwargs)
    return parser


def handle(args):
    project_root = os.getcwd()
    try:
        init(project_root)
    except ValueError:
        msg = "DB already initialized in {0!r}".format(project_root)
        raise CommandFailed(msg)


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
