#
# Copyright (c) 2012 Floqq innovation SL. All Right Reserved
#

import os
import unittest
import tempfile
import shutil
import tarfile
import textwrap

from floqq_deploy.db import init, get_config_path, config


class InitTest(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_init(self):
        "Test that the db is initialized correctly"
        init(project_path=self.test_dir)

        self.assertTrue(os.path.isdir(os.path.join(self.test_dir, ".deploy")))

    def test_settings(self):
        "Test that the db is initialized with the settings dir"
        init(project_path=self.test_dir)

        self.assertTrue(os.path.isdir(
            os.path.join(self.test_dir, ".deploy", "settings")))

    def test_versions(self):
        "Test that the db is initialized with the versions dir"
        init(project_path=self.test_dir)

        self.assertTrue(os.path.isdir(
            os.path.join(self.test_dir, ".deploy", "versions")))

    def test_head(self):
        "Test that the db is initialized with the HEAD dir"
        init(project_path=self.test_dir)

        self.assertTrue(os.path.isdir(
            os.path.join(self.test_dir, ".deploy", "HEAD")))

    def test_config(self):
        "Test that the db is initialized with the config file"
        init(project_path=self.test_dir)

        self.assertTrue(os.path.isfile(
            os.path.join(self.test_dir, ".deploy", "config")))

    def test_raises(self):
        "Test that a ValueError exception is raised if .deploy already exists"
        os.mkdir(os.path.join(self.test_dir, ".deploy"))

        self.assertRaises(ValueError, init, project_path=self.test_dir)


class GetConfigPathTest(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_get_path(self):
        "Test that we can find the path to the config file"
        self.cwd = os.getcwd()
        os.chdir(self.test_dir)

        path = get_config_path()

        os.chdir(self.cwd)

        self.assertIn("config", path)


class ConfigTest(unittest.TestCase):
    _config = """\
        [production]
        settings_url=
    """

    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.cwd = os.getcwd()
        os.chdir(self.test_dir)
        os.mkdir(".deploy")
        with open(os.path.join(".deploy", "config"), "w") as config:
            config.write(textwrap.dedent(self._config))

    def tearDown(self):
        os.chdir(self.cwd)
        shutil.rmtree(self.test_dir)

    def test_get(self):
        "Test that we get the right value from the config file"
        self.assertEqual("", config("settings_url", "production"))

    def test_get_nonexistent(self):
        "Test that we get None if the setting doesn't exist"
        self.assertIsNone(config("nothing", "production"))

    def test_set(self):
        "Test that we can set new values"
        value = "url"
        config("settings_url", "production", value)

        self.assertEqual(value, config("settings_url", "production"))

    def test_set_returns_previous(self):
        "Test that the old value is returned when new one is set"
        value = "url"
        previous = config("settings_url", "production", value)

        self.assertEqual("", previous)

    def test_delete(self):
        "Test that we can delete values"
        config("settings_url", "production", delete=True)

        self.assertIsNone(config("settings_url", "production"))

    def test_delete_returns_previous(self):
        "Test that the old value is returned when setting is deleted"
        previous = config("settings_url", "production", delete=True)

        self.assertEqual("", previous)

    def test_raises(self):
        "Test that ValueError is raised if the environment is incorrect"
        self.assertRaises(ValueError, config, name="name", environment="none")
