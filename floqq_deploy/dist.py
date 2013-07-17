#
# Copyright (c) 2012 Floqq innovation SL. All Right Reserved
#

import os
import shlex
import subprocess

from floqq_deploy.utils.commands import cd


def bower(app_path):
    """Run `bower install` inside `app_path`

    Params
        app_path: Application path.

    Raises
        ValueError if the app can't be found in .deploy/current
    """
    with cd(app_path):
        subprocess.call(shlex.split("bower install"))

def grunt(app_path):
    """Run `grunt dist`  program inside `app_path`.

    Params
        app_path: Application path.

    Raises
        ValueError if the app can't be found in .deploy/current
    """
    cwd = os.getcwd()
    app_node_modules = os.path.join(cwd, "node_modules")
    app_dist_node_modules = os.path.join(cwd, app_path, "node_modules")
    symlink = "ln -s {} {}".format(app_node_modules, app_dist_node_modules)
    subprocess.call(shlex.split(symlink))
    with cd(app_path):
        subprocess.call(shlex.split("grunt dist"))
