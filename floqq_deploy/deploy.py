import sys
import shlex
import shutil
import tempfile
import tarfile
import subprocess


def run(app_path):
    """Runs google's appcfg.py program to deploy an app.

    Params
        app_path: Path to the application directory.

    Raises:
        Any exception raised by the appcfg.py program.
    """
    run_appcfg(app_path)


def run_appcfg(app_path):
    """Runs appcfg.py program.

    `app` is the path to the app.
    """
    from google.appengine.tools import appcfg

    argv = ["appcfg.py", "update", app_path]
    try:
        appcfg.AppCfgApp(argv).Run()
    except KeyboardInterrupt:
        appcfg.StatusUpdate("Interrupted")
