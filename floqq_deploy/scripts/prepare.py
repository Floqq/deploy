"""Prepare the project for deploy.

Store the project referenced by .deploy/HEAD with all the specified environment
settings applied in:

   .deploy/current/

If there is no ref in HEAD then you need to first export your project. Run
`floqq-export -h` for more help.

Example:

    $ floqq-prepare production
    $ ls .deploy/current
    production
"""
import sys
import os
import argparse

from floqq_deploy.git import get_archive_filename
from floqq_deploy.db import head, unpack, get_current_path, get_settings_path
from floqq_deploy.settings import apply_settings
from floqq_deploy.scripts import formatter
from floqq_deploy.utils.scripts import is_valid_environment


def main(argv=None):
    if argv is None:
        argv = sys.argv[1:]
    parser = argparse.ArgumentParser(description=__doc__,
                                    formatter_class=formatter)
    parser.add_argument("env", type=is_valid_environment,
                        help="Environment name")

    args = parser.parse_args(argv)

    env = args.env

    filename = head()
    settings_path = os.path.join(get_settings_path(), env)
    project_path = os.path.join(get_current_path(), filename)
    if not filename:
        print "No ref found. Run `floqq-prepare -h` for more help."
        return 1

    if not os.path.isdir(settings_path):
        print "No settings found for %r environment." % env
        return 1

    output = os.path.join(get_current_path(), env)
    if not os.path.isdir(output):
        os.mkdir(output)
    if not os.path.exists(output):
        unpack(filename, output)
    apply_settings(settings_path, project_path)

    print "Project prepared at %r" % output


if __name__ == "__main__":
    sys.exit(main())
