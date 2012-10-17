#
# Copyright (c) 2012 Floqq innovation SL. All Right Reserved
#

import os
import shlex
import subprocess

from floqq_deploy.utils.commands import cd


def django_compilemessages(app_path, locale=None):
    """Run django compilemessages program inside `app_path`.

    Params
        app_path: Application path.
        locale: --locale option to pass to compilemessages program.

    Raises
        ValueError if the app can't be found in .deploy/current
    """
    if locale is None:
        locale = ""
    else:
        locale = " -l {0}".format(locale)
    cmd = "python manage.py compilemessages{0}".format(locale)
    with cd(app_path):
        subprocess.call(shlex.split(cmd))
