"""
Deploy a project archive.
"""
import sys
import argparse

from floqq_deploy.utils.scripts import is_tar
from floqq_deploy import deploy


def main(argv=None):
    if argv is None:
        argv = sys.argv[1:]
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("tarfile", type=is_tar,
                        help="Tar file of the project")

    args = parser.parse_args(argv)

    print "Deploying"
    deploy.run(args.path)


if __name__ == "__main__":
    sys.exit(main())
