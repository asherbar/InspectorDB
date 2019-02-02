import unittest

from app.logic.db.query import Query, QueryExecutionError
from project.test.postgres_container_utils import global_pcm
from project.test.test_db_utils import TestDbFiller


class TestQuery(unittest.TestCase):
    column_names = ('aaa', 'bbb')
    table_name = 'test_query'
    data = [('a', 'b'), ('c', 'd')]
    test_db_filler = TestDbFiller(table_name, column_names, data)

    @classmethod
    def setUpClass(cls):
        cls.test_db_filler.fill_test_db()

    @classmethod
    def tearDownClass(cls):
        cls.test_db_filler.drop_test_table()

    def test_query(self):
        object_under_test = Query(global_pcm.pg_db_name, f'SELECT * FROM {self.table_name}')
        self.assertCountEqual(object_under_test.get_column_names(), self.column_names)
        self.assertCountEqual(object_under_test.get_query_result(), self.data)

    def test_query_with_limit(self):
        object_under_test = Query(global_pcm.pg_db_name, f'SELECT * FROM {self.table_name}', 1)
        self.assertCountEqual(object_under_test.get_column_names(), self.column_names)
        self.assertCountEqual(object_under_test.get_query_result(), self.data[:1])

    def test_query_with_syntax_error(self):
        self.assertRaises(QueryExecutionError, Query, global_pcm.pg_db_name, 'OOPS *')

    def test_write_query(self):
        object_under_test = Query(
            global_pcm.pg_db_name,
            f"UPDATE {self.table_name} SET {self.column_names[0]} = 'c' WHERE {self.column_names[0]} = 'a'"
        )
        self.assertFalse(object_under_test.get_column_names())
        self.assertEqual(object_under_test.get_query_result(), 1)
        object_under_test = Query(global_pcm.pg_db_name, f'SELECT * FROM {self.table_name}')
        self.assertCountEqual(object_under_test.get_query_result(), [('c', 'b'), ('c', 'd')])

    def test_write_query_empty_table(self):
        empty_table_name = self.table_name + '2'
        column_names = ('x', 'y')
        with TestDbFiller(empty_table_name, column_names, []):
            object_under_test = Query(
                global_pcm.pg_db_name,
                f"UPDATE {empty_table_name} SET {column_names[0]} = 'c' WHERE {column_names[0]} = 'a'"
            )
            self.assertFalse(object_under_test.get_column_names())
            self.assertEqual(object_under_test.get_query_result(), 0)
