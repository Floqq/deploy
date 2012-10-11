#
# Copyright (c) 2012 Floqq innovation SL. All Right Reserved
#

import os
import glob
import shutil

from floqq_deploy.db import get_settings_path


def apply_settings(settings_path, project_path):
    """Apply the specified settings to a project.

    Params
        settings_path: Settings directory path.
        project_path: Project directory path.
    """
    for filename in glob.iglob("%s/*" % settings_path):
        shutil.copy(filename, project_path)
