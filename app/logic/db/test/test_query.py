import unittest

from app.logic.db.query import Query
from project.test.test_db_utils import fill_test_db


class TestQuery(unittest.TestCase):
    column_names = ('aaa', 'bbb')
    db_name = 'test_db'
    data = [('a', 'b'), ('c', 'd')]

    @classmethod
    def setUpClass(cls):
        fill_test_db(cls.db_name, cls.column_names, cls.data)

    def test_query(self):
        object_under_test = Query(self.db_name, f'SELECT * FROM {self.db_name}')
        self.assertCountEqual(object_under_test.get_column_names(), self.column_names)
        self.assertCountEqual(object_under_test.get_records(), self.data)

    def test_query_with_limit(self):
        object_under_test = Query(self.db_name, f'SELECT * FROM {self.db_name}', 1)
        self.assertCountEqual(object_under_test.get_column_names(), self.column_names)
        self.assertCountEqual(object_under_test.get_records(), self.data[:1])
