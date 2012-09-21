import sys
import shlex
import shutil
import tempfile
import tarfile
import subprocess

from google.appengine.tools import appcfg


def run(archive_path):
    """Runs google's appcfg.py program to deploy a tar archived project.

    The tar file first is unpackaged in a system's temp directory and after
    finishing the deployment is removed.

    `archive_path` is the path to the project tar.

    Raises:
        Any exception raised by the appcfg.py program
    """
    app = unpack_archive(archive_path)
    try:
        run_appcfg(app)
    finally:
        cleanup(app)


def unpack_archive(archive_path):
    """Unpack a tar into a system temp directory.
    
    Retuns the absolute path to that directory.
    """
    path = tempfile.mkdtemp()
    tar = tarfile.open(archive_path)
    tar.extractall(path)
    return path


def run_appcfg(app):
    """Runs appcfg.py program.

    `app` is the path to the app.
    """
    argv = ["appcfg.py", "update", app]
    try:
        appcfg.AppCfgApp(argv).Run()
    except KeyboardInterrupt:
        appcfg.StatusUpdate("Interrupted")


def cleanup(path):
    """Remove a directory tree"""
    shutil.rmtree(path)
