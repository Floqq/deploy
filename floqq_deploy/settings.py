#
# Copyright (c) 2012 Floqq innovation SL. All Right Reserved
#

import os
import re
import glob
import shutil

from floqq_deploy.db import get_settings_path, get_current_path, config
from floqq_deploy.exceptions import UnsupportedUrl, NoSettingsUrl


def apply_settings(app_name, version):
    """Apply settings to a project.

    It searches the settings in:

        .deploy/settings/<app name>/

    and applies them to the project:

        .deploy/current/<app name>/

    Params
        app_name: Application.
        version: Application version.

    Raises
        ValueError if the settings or the unpacked project are not found.

    Returns
        the tuple (settings_path, project_path)
    """
    settings_path = os.path.join(get_settings_path(), app_name)
    if not os.path.isdir(settings_path):
        msg = "No settings found."
        raise ValueError(msg)
    project_path = os.path.join(get_current_path(), app_name)
    if not os.path.isdir(project_path):
        msg = "No unpacked project found."
        raise ValueError(msg)

    config_name = "app.yaml"
    for filename in glob.iglob("{0}/*".format(settings_path)):
        if config_name in filename:
            with open(filename) as src:
                dst_path = os.path.join(project_path, config_name)
                with open(dst_path, "w") as dst:
                    for line in src:
                        if re.match(r"^application:", line):
                            line = "application: {0}\n".format(app_name)
                        elif re.match(r"^version:", line):
                            line = "version: {0}\n".format(version)
                        dst.write(line)
        else:
            shutil.copy(filename, project_path)

    previous_version = config("current_version", section=app_name)
    config("previous_version", section=app_name, value=previous_version)
    config("current_version", section=app_name, value=version)

    return settings_path, project_path


def fetch(app_name):
    """Fetch settings for a given app.

    Fetch the settings and stores them in .deploy/settings/<app name>/

    Params
        app_name: Application name.

    Raises
        NoSettingsUrl if the `settings_url` param is not set in the config file.
        UnsupportedUrl if the url can't be handled.
    """
    url = config("settings_url", section=app_name)
    if not url:
        msg = "You need to set `settings_url` in the config"
        raise NoSettingsUrl(msg)
    settings_path = os.path.join(get_settings_path(), app_name)
    if os.path.isdir(url):
        src = url
        if os.path.exists(settings_path):
            shutil.rmtree(settings_path)
        shutil.copytree(src, settings_path)
    else:
        msg = "I don't know how to fetch this url {0!r}".format(url)
        raise UnsupportedUrl(msg)

    return url, settings_path
