#
# Copyright (c) 2012 Floqq innovation SL. All Right Reserved
#

import os
import shutil
import zipfile
from ConfigParser import SafeConfigParser

from floqq_deploy.exceptions import UnsupportedUrl


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
    return os.path.join(".deploy", "config")


def get_versions_path():
    """Returns the path to the .deploy/versions directory."""
    return os.path.join(".deploy", "versions")


def get_settings_path():
    """Returns the path to the .deploy/settings directory."""
    return os.path.join(".deploy", "settings")


def get_head_path():
    """Returns the path to the .deploy/HEAD file."""
    return os.path.join(".deploy", "HEAD")


def get_current_path():
    """Returns the path to the .deploy/current directory."""
    return os.path.join(".deploy", "current")


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


def fetch_settings(url, env):
    """Copy the referenced settings by `url`.

    Params
        url: Url pointing to the settings.
        env: Environment name of these settings.

    Raises
        ValueError if the url is not valid.
        UnsupportedUrl if the url can't be handled.
    """
    if not url:
        msg = "Invalid URL"
        raise ValueError(msg)
    dst = os.path.join(get_settings_path(), env)
    if os.path.isdir(url):
        src = url
        if os.path.exists(dst):
            shutil.rmtree(dst)
        shutil.copytree(src, dst)
    else:
        msg = "I don't know how to fetch this url %r" % url
        raise UnsupportedUrl(msg)


def head(filename=None):
    """Gets/Updates the HEAD ref.
    
    The HEAD ref is a file called HEAD inside of .deploy that holds the name of
    the last exported tree.
    If `filename` is given the HEAD will point to the given filename otherwise
    the current filename is returned.

    Params
        filename: name of the archive.
    """
    if filename is None:
        with open(get_head_path()) as head:
            return head.read().strip()
    else:
        with open(get_head_path(), "w") as head:
            head.write("%s\n" % filename)


def unpack(filename, output):
    """Unpacks the exported `filename` project in the .deploy/current directory.

    Params
        filename: Name of the exported project.

    Raises
        ValueError: If the project can't be found in the .deploy/versions
        directory.
    """
    archive = os.path.join(get_versions_path(), filename)
    if not os.path.exists(archive):
        msg = "%r project can't be found"
        raise ValueError(msg)

    with zipfile.ZipFile(archive) as f:
        f.extractall(path=output)
