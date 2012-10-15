"""Exports a git tree and save it into the database.

Create a tar file with the last committed changes of the branch you specify,
saves it in .deploy/versions/ for future manipulation and updates the HEAD ref.

Example:
    
    $ floqq-export master
    $ ls .deploy/versions
    $ cat .deploy/HEAD
    <tree commit id>

"""
import os
import sys
import argparse

from floqq_deploy import git
from floqq_deploy.db import get_versions_path, head
from floqq_deploy.utils.scripts import is_dir
from floqq_deploy.scripts import formatter
from floqq_deploy.exceptions import CommandFailed


def handle(args):
    tree = args.tree
    filename = git.get_archive_filename(tree)
    print "Creating archive: %s" % filename
    outputfile = os.path.join(get_versions_path(), filename)
    git.archive(tree, output=outputfile, format="zip")
    head(filename)


def main(argv=None):
    if argv is None:
        argv = sys.argv[1:]
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=formatter)
    parser.add_argument("tree", help="Git tree name")
    args = parser.parse_args(argv)
    try:
        handle(args)
    except CommandFailed, e:
        print(e.message)
        return 1


if __name__ == "__main__":
    sys.exit(main())
