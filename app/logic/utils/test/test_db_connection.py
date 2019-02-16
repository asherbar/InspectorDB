import unittest
from unittest import mock

from app.logic.utils.db_connection import get_connection
from project.test_utils.postgres_container_utils import global_pcm


class TestDbConnection(unittest.TestCase):
    def test_get_connection(self):
        self.assertIsNotNone(get_connection(global_pcm.pg_db_name))

    def test_get_connection_wrong_db_name(self):
        self.assertRaises(KeyError, get_connection, 'oops')

    def test_non_int_readonly_env(self):
        with mock.patch.dict('os.environ', {'READONLY': '?'}):
            connection = get_connection(global_pcm.pg_db_name)
            self.assertIsNotNone(connection)
            self.assertTrue(connection.readonly)
