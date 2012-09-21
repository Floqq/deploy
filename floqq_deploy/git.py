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


def archive(path, tree, output):
    """Creates an archive of the files currently in the project index.

    Equivalent to:
        git archive --format=tar -o <name>
    """
    cwd = os.getcwd()
    os.chdir(path)
    local("git archive --format=tar -o %s %s" % (output, tree))
    os.chdir(cwd)


def rev_parse(tree):
    """Returns the current ref id of the given tree"""
    return local("git rev-parse %s" % tree)


def get_archive_filename(app_dir, tree, ext="tar"):
    """Generates a name suitable for use with the archive function.

    The name of the archive will be:
        <name of the app enclosing directory>-<last commit id>.<extension>
    """
    enclosing_dir = os.path.basename(os.path.abspath(app_dir))
    app_id = rev_parse(tree)
    filename = "%s-%s.%s" % (enclosing_dir, app_id, ext)
    return filename
