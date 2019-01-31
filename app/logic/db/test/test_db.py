import unittest

from app.logic.db.db import Db
from project.test.postgres_container_utils import global_pcm
from project.test.test_db_utils import fill_test_db


class TestDb(unittest.TestCase):
    def test_get_public_tables(self):
        column_names = ('a', 'b')
        table_names = list(['test_db_' + str(i) for i in range(10)])
        for table_name in table_names:
            fill_test_db(table_name, column_names, [])
        object_under_test = Db(global_pcm.pg_db_name)
        self.assertCountEqual(object_under_test.get_public_tables(), table_names)
