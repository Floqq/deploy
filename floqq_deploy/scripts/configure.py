"""
Apply settings to the project.
Adds recursively the specified settings file to the project archive.
"""
import sys
import argparse

from floqq_deploy import settings
from floqq_deploy.utils.scripts import is_tar, is_dir


def main(argv=None):
    if argv is None:
        argv = sys.argv[1:]
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("tarfile", type=is_tar,
                        help="Tar file of the project")
    parser.add_argument("settings", type=is_dir,
                        help="Path to the directory containing the settings")

    args = parser.parse_args(argv)

    archive = args.tarfile
    directory = args.settings
    settings.configure(archive, directory)
    print "Applied settings in: %r" % directory
    

if __name__ == "__main__":
    sys.exit(main())
