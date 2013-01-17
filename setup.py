import os
import sys

from setuptools import setup, find_packages

py_version = sys.version_info[:2]

here = os.path.abspath(os.path.dirname(__file__))

try:
    README = open(os.path.join(here, "README.md")).read()
except IOError:
    README = ""

dependencies = ['pycrypto == 2.6']

scripts = {
    "console_scripts": [
        "floqq-init = floqq_deploy.scripts.init:main",
        "floqq-config = floqq_deploy.scripts.config:main",
        "floqq-export = floqq_deploy.scripts.export:main",
        "floqq-fetch-settings = floqq_deploy.scripts.fetch_settings:main",
        "floqq-apply-settings = floqq_deploy.scripts.apply_settings:main",
        "floqq-unpack = floqq_deploy.scripts.unpack:main",
        "floqq-prepare = floqq_deploy.scripts.prepare:main",
        "floqq-deploy = floqq_deploy.scripts.deploy:main",
        "floqq-upload = floqq_deploy.scripts.upload:main",
        "floqq-encrypt-settings = floqq_deploy.scripts.encrypt_settings:main",
        "floqq-decrypt-settings = floqq_deploy.scripts.decrypt_settings:main",
        "floqq-compilemessages = floqq_deploy.scripts.compilemessages:main",
        "floqq = floqq_deploy.scripts.floqq:main",
    ]
}


setup(name="floqq_deploy",
      version="1.1",
      description="Deployment script for Floqq",
      long_description=README,
      author="Anler Hernandez Peral",
      author_email="anler86@gmail.com",
      packages=find_packages(exclude=["tests"]),
      package_data={"floqq_deploy": ["template/**/*"]},
      entry_points=scripts,
      test_suite="floqq_deploy.tests",
      install_requires=dependencies)
