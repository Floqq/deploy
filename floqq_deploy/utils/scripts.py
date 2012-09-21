import os
import tarfile
import argparse


def is_dir(path):
    """Checks if path is a valid directory.

    Raises:
        argparse.ArgumentTypeError if is not a valid directory
    """
    if not os.path.isdir(path):
        msg = "%r is not a valid directory" % path
        raise argparse.ArgumentTypeError(msg)
    return path


def is_tar(path):
    """Checks if path is a valid tar file.

    Raises:
        argparse.ArgumentTypeError if is not a valid tar file
    """
    if not tarfile.is_tarfile(path):
        msg = "%r is not a valid tar file" % path
        raise argparse.ArgumentTypeError(msg)
    return path


def touch(filename):
    """Create a file if not exists"""
    open(filename, "w").close()


def touch_tar(filename):
    """Create a tar file if not exists"""
    tarfile.open(filename, "w").close()
