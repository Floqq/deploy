#
# Copyright (c) 2012 Floqq innovation SL. All Right Reserved
#

import os
import unittest

from floqq_deploy import security


class PadTest(unittest.TestCase):
    def test_pad_empty(self):
        "Pad an empty string"
        text = ""
        expected = 7 * security._PAD_BYTE + "8"
        self.assertEqual(expected, security.pad(text))

    def test_pad(self):
        "Pad a string with length not multiple of 8"
        text = "abc"
        expected = "abc" + 4 * security._PAD_BYTE + "5"
        self.assertEqual(expected, security.pad(text))

    def test_pad_with_pad_byte(self):
        "Pad a string with last char equal to padding char"
        text = "abc" + security._PAD_BYTE
        expected = "abc" + security._PAD_BYTE + 3 * security._PAD_BYTE + "4"
        self.assertEqual(expected, security.pad(text))

    def test_no_pad(self):
        "Pad a string with length multiple of 8"
        text = "abcdefgh"
        expected = "abcdefgh" + 7 * security._PAD_BYTE + "8"
        self.assertEqual(expected, security.pad(text))


class UnpadTest(unittest.TestCase):
    def test_unpad_empty(self):
        "Unpad an empty string"
        text = ""
        self.assertRaises(ValueError, security.unpad, text)

    def test_unpad(self):
        "Unpad a string"
        text = "abc" + 4 * security._PAD_BYTE + "5"
        expected = "abc"
        self.assertEqual(expected, security.unpad(text))

    def test_unpad_with_pad_byte(self):
        "Unpad a string with last char equal to padding char"
        text = "abc" + security._PAD_BYTE + 3 * security._PAD_BYTE + "4"
        expected = "abc" + security._PAD_BYTE
        self.assertEqual(expected, security.unpad(text))

