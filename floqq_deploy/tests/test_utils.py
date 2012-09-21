import os
import unittest
import tempfile
import shutil
import tarfile
from argparse import ArgumentTypeError

from floqq_deploy.utils import scripts


class IsDirTest(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_valid_dir(self):
        "Test that when given a valid dir path returns a that path"
        self.assertEqual(scripts.is_dir(self.test_dir), self.test_dir)

    def test_invalid_dir(self):
        """Test that raises a argparse.ArgumentTypeError if given an invalid
        directory
        """
        self.assertRaises(ArgumentTypeError, scripts.is_dir, "fakedir")


class IsTarTest(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.test_tar = os.path.join(self.test_dir, "_tar.tar")
        self.test_file = os.path.join(self.test_dir, "file")
        scripts.touch_tar(self.test_tar)
        scripts.touch(self.test_file)

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_valid_dir(self):
        "Test that when given a valid tar path returns a that path"
        self.assertEqual(scripts.is_tar(self.test_tar), self.test_tar)

    def test_invalid_dir(self):
        """Test that raises a argparse.ArgumentTypeError if given an invalid
        tar
        """
        self.assertRaises(ArgumentTypeError, scripts.is_tar, self.test_file)


class TouchTest(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_valid(self):
        "Test that creates a file if not exists"
        filename = os.path.join(self.test_dir, "testfile")
        self.assertFalse(os.path.isfile(filename))
        scripts.touch(filename)
        self.assertTrue(os.path.isfile(filename))


class TouchTarTest(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_valid(self):
        "Test that creates a tar file if not exists"
        filename = os.path.join(self.test_dir, "testfile")
        self.assertFalse(os.path.isfile(filename))
        scripts.touch_tar(filename)
        self.assertTrue(os.path.isfile(filename))
        self.assertTrue(tarfile.is_tarfile(filename))
