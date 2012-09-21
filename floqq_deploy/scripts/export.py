"""
Creates a tar file with the last committed changes of the branch of your
preference.
"""
import sys
import argparse

from floqq_deploy.utils.scripts import is_dir
from floqq_deploy import git


def main(argv=None):
    if argv is None:
        argv = sys.argv[1:]
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("app", type=is_dir,
                        help="Path to application")
    parser.add_argument("tree", help="Tree name from which get the changes")
    args = parser.parse_args(argv)

    app_dir = args.app
    tree = args.tree

    outputfile = git.get_archive_filename(app_dir, tree)
    print "Creating archive: %s" % outputfile
    git.archive(app_dir, tree, output=outputfile)


if __name__ == "__main__":
    sys.exit(main())
