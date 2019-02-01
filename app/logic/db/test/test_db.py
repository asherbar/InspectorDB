import unittest

from app.logic.db.db import Db
from project.test.postgres_container_utils import global_pcm
from project.test.test_db_utils import TestDbFiller


class TestDb(unittest.TestCase):
    def tearDown(self):
        for test_db_filler in self.test_db_fillers:
            test_db_filler.drop_test_table()

    def test_get_public_tables(self):
        column_names = ('a', 'b')
        table_names = list(['test_db_' + str(i) for i in range(10)])
        self.test_db_fillers = tuple(TestDbFiller(table_name, column_names, []) for table_name in table_names)
        for test_db_filler in self.test_db_fillers:
            test_db_filler.fill_test_db()
        object_under_test = Db(global_pcm.pg_db_name)
        self.assertCountEqual(object_under_test.get_public_tables(), table_names)
