import os
import glob
import tarfile


def configure(archive, directory):
    """Add all *.yaml and settings.py found in directory into a project tar.

    `archive` must be a tar archive.
    `directory` is a directory containing any .yaml file and/or a settings.py
    file that will be added recursively to the archive.
    """
    tar = tarfile.open(archive, "a")
    def _add_to_tarfile(filename):
        tar.add(filename, arcname=os.path.basename(filename), recursive=False)

    yaml = glob.iglob("%s/*.yaml" % directory)
    settings = glob.iglob("%s/settings.py" % directory)
    for filename in yaml:
        _add_to_tarfile(filename)
    for filename in settings:
        _add_to_tarfile(filename)
