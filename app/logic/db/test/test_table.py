import unittest

from app.logic.db.table import Table, TableDoesNotExist
from project.test.postgres_container_utils import global_pcm
from project.test.test_db_utils import TestDbFiller


class TestTable(unittest.TestCase):
    column_names = ('aaa', 'bbb')
    table_name = 'test_table'
    data = [('a', 'b'), ('c', 'd')]
    test_db_filler = TestDbFiller(table_name, column_names, data)

    @classmethod
    def setUpClass(cls):
        cls.test_db_filler.fill_test_db()

    @classmethod
    def tearDownClass(cls):
        cls.test_db_filler.drop_test_table()

    def test_table(self):
        object_under_test = Table(global_pcm.pg_db_name, self.table_name)
        self.assertCountEqual(object_under_test.get_all_records(), self.data)
        self.assertCountEqual(object_under_test.get_columns(), self.column_names)
        self.assertEqual(object_under_test.table_name, self.table_name)

    def test_table_limit(self):
        object_under_test = Table(global_pcm.pg_db_name, self.table_name, 1)
        self.assertCountEqual(object_under_test.get_all_records(), self.data[:1])
        self.assertCountEqual(object_under_test.get_columns(), self.column_names)

    def test_table_doesnt_exist(self):
        self.assertRaises(TableDoesNotExist, Table, global_pcm.pg_db_name, self.table_name + 'oops')

    def test_empty_table(self):
        empty_table_name = self.table_name + '2'
        column_names = ('x', 'y')
        with TestDbFiller(empty_table_name, column_names, []):
            object_under_test = Table(global_pcm.pg_db_name, empty_table_name)
            self.assertCountEqual(object_under_test.get_columns(), column_names)
            self.assertEqual(object_under_test.get_all_records(), [])
