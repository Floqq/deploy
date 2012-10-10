#
# Copyright (c) 2012 Floqq innovation SL. All Right Reserved
#

import os
import shutil
from ConfigParser import SafeConfigParser


ENVIRONMENTS = set(("production", "staging", "testing"))


def init(project_path):
    """Copy the template directory as <project_path>/.deploy
    
    Params
        project_path: Path where to create the .deploy directory

    Raises
        ValueError if the .deploy directory already exists.
    """
    src = os.path.join(os.path.dirname(__file__), "template")
    dst = os.path.join(project_path, ".deploy")
    if os.path.exists(dst):
        msg = "%r already exists" % dst
        raise ValueError(msg)
    else:
        shutil.copytree(src, dst)


def get_config_path():
    """Returns the path to the .deploy/config file."""
    return os.path.join(os.getcwd(), ".deploy", "config")


def config(name, environment, value=None, delete=False):
    """Get/Set/Modify a setting on the given environment.

    To get a setting just pass the name and the environment.
    To set a setting pass the name, the environment and a value.
    To delete a setting pass the name, the environment and the `delete` flag to
    True.

    Params
        name: name of the setting.
        environment: environment (section) from which get the setting.
        value (optional): value of the setting.

    Raises
        ValueError: if environment is not one of the supported environments

    Returns
        The value of the setting when "getting".
        The previous value of the setting when "setting".
        The previous value of the setting when "deleting".
    """
    if environment not in ENVIRONMENTS:
        msg = "`environment` must be one of %s" % ", ".join(ENVIRONMENTS)
        raise ValueError(msg)

    config_path = get_config_path()
    config = SafeConfigParser()
    config.read([config_path])

    if config.has_option(environment, name):
        option = config.get(environment, name)
    else:
        option = None
    if value is not None:
        config.set(environment, name, value)
    elif delete:
        config.remove_option(environment, name)

    with open(config_path, "w") as f:
        config.write(f)

    return option
