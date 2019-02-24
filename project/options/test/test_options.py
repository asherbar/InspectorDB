import os
import unittest
from unittest import mock

from project.options.option import OptionDebug, OptionSessionCookieAge, OptionReadOnly, OptionVcapServiceLabel, \
    OptionSslRedirect


class TestOptionDebug(unittest.TestCase):
    def test_get_option_not_given(self):
        with mock.patch.dict('os.environ'):
            os.environ.pop('DEBUG', None)
            self.assertIs(OptionDebug().get_option(), False)

    def test_get_option_given_good_value(self):
        with mock.patch.dict('os.environ', {'DEBUG': '0'}):
            self.assertIs(OptionDebug().get_option(), False)
        with mock.patch.dict('os.environ', {'DEBUG': '1'}):
            self.assertIs(OptionDebug().get_option(), True)

    def test_get_option_given_bad_value(self):
        with mock.patch.dict('os.environ', {'DEBUG': '?'}):
            self.assertIs(OptionDebug().get_option(), False)


class TestOptionSessionCookieAge(unittest.TestCase):
    def test_get_option_not_given(self):
        with mock.patch.dict('os.environ'):
            os.environ.pop('SESSION_COOKIE_AGE', None)
            self.assertEqual(OptionSessionCookieAge().get_option(), 1209600)

    def test_get_option_given_good_value(self):
        with mock.patch.dict('os.environ', {'SESSION_COOKIE_AGE': '1000'}):
            self.assertEqual(OptionSessionCookieAge().get_option(), 1000)

    def test_get_option_given_bad_value(self):
        with mock.patch.dict('os.environ', {'SESSION_COOKIE_AGE': '?'}):
            self.assertEqual(OptionSessionCookieAge().get_option(), 1209600)


class TestOptionReadOnly(unittest.TestCase):
    def test_get_option_not_given(self):
        with mock.patch.dict('os.environ'):
            os.environ.pop('READONLY', None)
            self.assertIs(OptionReadOnly().get_option(), True)

    def test_get_option_given_good_value(self):
        with mock.patch.dict('os.environ', {'READONLY': '0'}):
            self.assertIs(OptionReadOnly().get_option(), False)
        with mock.patch.dict('os.environ', {'READONLY': '1'}):
            self.assertIs(OptionReadOnly().get_option(), True)

    def test_get_option_given_bad_value(self):
        with mock.patch.dict('os.environ', {'READONLY': '?'}):
            self.assertIs(OptionReadOnly().get_option(), True)


class TestOptionVcapServiceLabel(unittest.TestCase):
    def test_get_option_not_given(self):
        with mock.patch.dict('os.environ'):
            os.environ.pop('VCAP_SERVICE_LABEL', None)
            self.assertEqual(OptionVcapServiceLabel().get_option(), 'postgresql')

    def test_get_option_given_good_value(self):
        with mock.patch.dict('os.environ', {'VCAP_SERVICE_LABEL': '2000'}):
            self.assertEqual(OptionVcapServiceLabel().get_option(), '2000')


class TestOptionSslRedirect(unittest.TestCase):
    def test_get_option_not_given(self):
        with mock.patch.dict('os.environ'):
            os.environ.pop('SECURE_SSL_REDIRECT', None)
            self.assertEqual(OptionSslRedirect().get_option(), True)

    def test_get_option_given_good_value(self):
        with mock.patch.dict('os.environ', {'SECURE_SSL_REDIRECT': '0'}):
            self.assertEqual(OptionSslRedirect().get_option(), False)
