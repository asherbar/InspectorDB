from django.test import TestCase, Client
from pypika import Query

from project.test.postgres_container_utils import global_pcm
from project.test.test_db_utils import TestDbFiller


class TestTableView(TestCase):

    def tearDown(self):
        c = Client()
        c.logout()

    def test_get_table(self):
        table_name = 'test_table_view'
        column_names = ('a', 'b')
        with TestDbFiller(table_name, column_names, []):
            c = Client()
            logged_in = c.login(username=global_pcm.pg_db_name, password=global_pcm.pg_password)
            self.assertTrue(logged_in)
            response = c.get(f'/app/table/{table_name}')
            self.assertEqual(response.status_code, 200)

    def test_get_non_existing_table(self):
        c = Client()
        logged_in = c.login(username=global_pcm.pg_db_name, password=global_pcm.pg_password)
        self.assertTrue(logged_in)
        response = c.get('/app/table/oops')
        self.assertEqual(response.status_code, 404)

    def test_get_table_not_authenticated(self):
        c = Client()
        response = c.get(f'/app/table/any', follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertCountEqual(response.redirect_chain, [('/app/login/?next=/app/table/any', 302)])


class TestQueryView(TestCase):
    table_name = 'test_query_view'
    column_names = ('a', 'b')
    data = [('aaa', 'bbb')]
    test_db_filler = TestDbFiller(table_name, column_names, data)

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.test_db_filler.fill_test_db()

    @classmethod
    def tearDownClass(cls):
        cls.test_db_filler.drop_test_table()
        super().tearDownClass()

    def tearDown(self):
        c = Client()
        c.logout()

    def test_execute_query(self):
        c = Client()
        logged_in = c.login(username=global_pcm.pg_db_name, password=global_pcm.pg_password)
        self.assertTrue(logged_in)
        q = Query.from_(self.table_name).select(self.column_names[0])
        response = c.get(f'/app/query/?query={q}')
        self.assertEqual(response.status_code, 200)

    def test_query_non_existing_table(self):
        c = Client()
        logged_in = c.login(username=global_pcm.pg_db_name, password=global_pcm.pg_password)
        self.assertTrue(logged_in)
        q = Query.from_('oops').select('a')
        response = c.get(f'/app/query/?query={q}')
        self.assertEqual(response.status_code, 400)

    def test_query_syntax_error(self):
        c = Client()
        logged_in = c.login(username=global_pcm.pg_db_name, password=global_pcm.pg_password)
        self.assertTrue(logged_in)
        response = c.get(f'/app/query/?query=nonsense')
        self.assertEqual(response.status_code, 400)

    def test_query_update_table(self):
        c = Client()
        logged_in = c.login(username=global_pcm.pg_db_name, password=global_pcm.pg_password)
        self.assertTrue(logged_in)
        q = Query.update(self.table_name).set(self.column_names[0], 'ccc')
        response = c.get(f'/app/query/?query={q}')
        self.assertEqual(response.status_code, 200)

    def test_execute_query_not_authenticated(self):
        c = Client()
        response = c.get('/app/query/?query=any', follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertCountEqual(response.redirect_chain, [('/app/login/?next=/app/query/%3Fquery%3Dany', 302)])
