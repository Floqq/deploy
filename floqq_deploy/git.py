import os
import shlex
import subprocess
from cStringIO import StringIO


def local(command):
    """Runs command in a new process.

    Returns the tuple:
        (output, returncode)
    Raises:
        RuntimeError if the command return code is not 0
    """
    pipe = subprocess.Popen(shlex.split(command), stdout=subprocess.PIPE)
    output, retcode = pipe.communicate()
    if retcode:
        msg = "'%s' failed:: %d %s" % (command, retcode, output)
        raise RuntimeError(msg)
    return output.strip()


def archive(tree, output, format="tar"):
    """Creates an archive of the files currently in the project index.

    Equivalent to:
        git archive -o <name>
    """
    local("git archive --format=%s -o %s %s" % (format, output, tree))


def rev_parse(tree):
    """Returns the current ref id of the given tree"""
    return local("git rev-parse %s" % tree)


def get_archive_filename(tree):
    """Generates a name suitable for use with the archive function.

    The name of the archive will be:
        <tree commit id>
    """
    filename = rev_parse(tree)

    return filename
