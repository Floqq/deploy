#
# Copyright (c) 2012 Floqq innovation SL. All Right Reserved
#


class UnsupportedUrl(Exception):
    """Exception raised when don't know how to fetch the contents of an URL"""


class NoSettingsUrl(Exception):
    """Exception raised when the `settings_url` param isn't in the config"""


class CommandFailed(Exception):
    """Exception raised when a command run failed"""
