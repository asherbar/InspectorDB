import os
import unittest
from unittest import mock

from project.options import Options


class TestOptions(unittest.TestCase):
    def test_get_debug_not_given(self):
        with mock.patch.dict('os.environ'):
            os.environ.pop('DEBUG', None)
            self.assertFalse(Options.get_debug())

    def test_get_debug_given_good_value(self):
        with mock.patch.dict('os.environ', {'DEBUG': '0'}):
            self.assertFalse(Options.get_debug())
        with mock.patch.dict('os.environ', {'DEBUG': '1'}):
            self.assertTrue(Options.get_debug())

    def test_get_debug_given_bad_value(self):
        with mock.patch.dict('os.environ', {'DEBUG': '?'}):
            self.assertFalse(Options.get_debug())

    def test_get_session_cookie_age_not_given(self):
        with mock.patch.dict('os.environ'):
            os.environ.pop('SESSION_COOKIE_AGE', None)
            self.assertEqual(Options.get_session_cookie_age(), 1209600)

    def test_get_session_cookie_age_given_good_value(self):
        with mock.patch.dict('os.environ', {'SESSION_COOKIE_AGE': '1000'}):
            self.assertEqual(Options.get_session_cookie_age(), 1000)

    def test_get_session_cookie_age_given_bad_value(self):
        with mock.patch.dict('os.environ', {'SESSION_COOKIE_AGE': '?'}):
            self.assertEqual(Options.get_session_cookie_age(), 1209600)

    def test_get_readonly_not_given(self):
        with mock.patch.dict('os.environ'):
            os.environ.pop('READONLY', None)
            self.assertTrue(Options.get_readonly())

    def test_get_readonly_given_good_value(self):
        with mock.patch.dict('os.environ', {'READONLY': '0'}):
            self.assertFalse(Options.get_readonly())
        with mock.patch.dict('os.environ', {'READONLY': '1'}):
            self.assertTrue(Options.get_readonly())

    def test_get_readonly_given_bad_value(self):
        with mock.patch.dict('os.environ', {'READONLY': '?'}):
            self.assertTrue(Options.get_readonly())
