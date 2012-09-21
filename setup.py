import os
import sys

from setuptools import setup, find_packages

py_version = sys.version_info[:2]

here = os.path.abspath(os.path.dirname(__file__))

try:
    README = open(os.path.join(here, "README.txt")).read()
except IOError:
    README = ""

dependencies = [
]

scripts = {
    "console_scripts": [
        "floqq-export = floqq_deploy.scripts.export:main",
        "floqq-configure = floqq_deploy.scripts.configure:main",
        "floqq-deploy = floqq_deploy.scripts.deploy:main",
    ]
}


setup(name="floqq_deploy",
      version="1.0",
      description="Deployment script for Floqq",
      long_description=README,
      author="Anler Hernandez Peral",
      author_email="anler86@gmail.com",
      packages=find_packages(exclude=["tests"]),
      entry_points=scripts,
      test_suite="floqq_deploy.tests",
      install_requires=dependencies)
