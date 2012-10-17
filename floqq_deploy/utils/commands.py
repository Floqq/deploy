#
# Copyright (c) 2012 Floqq innovation SL. All Right Reserved
#

import os

from contextlib import contextmanager


@contextmanager
def cd(path):
    """Context manager that cd into `path` and at the end goes to previous dir.

    Params
        path: Path to cd into.
    """
    wd = os.getcwd()
    os.chdir(path)
    yield
    os.chdir(wd)
