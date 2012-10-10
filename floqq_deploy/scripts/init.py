"""Initializes the db in the current project path.

It will create a .deploy directory with the following structure:
    .deploy/
        config
        settings/
        versions/
        HEAD/
Where
    config: Is a file holding some configuration parameters.
    settings: A directory of settings to apply to the project.
    versions: Will contain all the git-exported trees named as
              <commit id>.tar.
    HEAD: Will contain what is actually gonna be deployed.
"""
import sys
import os
import argparse

from floqq_deploy.db import init


def main(argv=None):
    if argv is None:
        argv = sys.argv[1:]
    parser = argparse.ArgumentParser(description=__doc__)
    args = parser.parse_args(argv)

    project_root = os.getcwd()

    try:
        init(project_root)
    except ValueError:
        print "Deployment db already initialized in %r" % project_root
    

if __name__ == "__main__":
    sys.exit(main())
