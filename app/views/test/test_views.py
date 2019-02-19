from unittest import mock
from unittest.mock import patch

from django.test import TestCase, Client
from pypika import Query

from app.logic.db.db import Db
from app.logic.utils.db_connection import DbConnectionError
from project.test_utils.postgres_container_utils import global_pcm
from project.test_utils.test_db_utils import TestDbFiller


class TestIndexView(TestCase):
    path = '/app/'

    def test_no_tables(self):
        c = Client()
        logged_in = c.login(username=global_pcm.pg_db_name, password=global_pcm.pg_password)
        self.assertTrue(logged_in)
        response = c.get(self.path)
        self.assertContains(response, 'No tables in database... yet!')

    def test_not_authenticated(self):
        c = Client()
        response = c.get(self.path, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertCountEqual(response.redirect_chain, [('/app/login/?next=/app/', 302)])

    def test_connection_error(self):
        c = Client()
        logged_in = c.login(username=global_pcm.pg_db_name, password=global_pcm.pg_password)
        self.assertTrue(logged_in)
        with patch.object(Db, 'get_public_tables', side_effect=DbConnectionError({'some': 'creds'})) as mock_method:
            response = c.get(self.path)
        self.assertContains(response, 'Unable to connect to database')
        mock_method.assert_called()

    def test_has_tables(self):
        c = Client()
        logged_in = c.login(username=global_pcm.pg_db_name, password=global_pcm.pg_password)
        self.assertTrue(logged_in)
        table_name = 'test_table_view'
        column_names = ('a', 'b')
        with TestDbFiller(table_name, column_names, []):
            response = c.get(self.path, follow=True)
            self.assertEqual(response.status_code, 200)
            self.assertCountEqual(response.redirect_chain, [(f'/app/table/{table_name}', 302)])


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

    def test_get_table_page(self):
        table_name = 'test_table_view'
        column_names = ('a', 'b')
        with TestDbFiller(table_name, column_names, list((str(i), str(i)) for i in range(100))):
            c = Client()
            logged_in = c.login(username=global_pcm.pg_db_name, password=global_pcm.pg_password)
            self.assertTrue(logged_in)
            response = c.get(f'/app/table/{table_name}?page=1')
            self.assertEqual(response.status_code, 200)
            response = c.get(f'/app/table/{table_name}?page=2')
            self.assertEqual(response.status_code, 200)
            response = c.get(f'/app/table/{table_name}?page=200')
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
        self.assertContains(response, r'relation \"oops\" does not exist')

    def test_query_syntax_error(self):
        c = Client()
        logged_in = c.login(username=global_pcm.pg_db_name, password=global_pcm.pg_password)
        self.assertTrue(logged_in)
        response = c.get(f'/app/query/?query=nonsense')
        self.assertContains(response, r'syntax error at or near \"nonsense\"')

    def test_query_update_table(self):
        c = Client()
        logged_in = c.login(username=global_pcm.pg_db_name, password=global_pcm.pg_password)
        self.assertTrue(logged_in)
        with mock.patch.dict('os.environ', {'READONLY': '0'}):
            q = Query.update(self.table_name).set(self.column_names[0], 'ccc')
            response = c.get(f'/app/query/?query={q}')
            self.assertEqual(response.status_code, 200)

    def test_query_update_readonly_table(self):
        c = Client()
        logged_in = c.login(username=global_pcm.pg_db_name, password=global_pcm.pg_password)
        self.assertTrue(logged_in)
        q = Query.update(self.table_name).set(self.column_names[0], 'ccc')
        response = c.get(f'/app/query/?query={q}')
        self.assertContains(response, r'cannot execute UPDATE in a read-only transaction')

    def test_execute_query_not_authenticated(self):
        c = Client()
        response = c.get('/app/query/?query=any', follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertCountEqual(response.redirect_chain, [('/app/login/?next=/app/query/%3Fquery%3Dany', 302)])


class TestLogoutView(TestCase):
    def test_next_page(self):
        c = Client()
        logged_in = c.login(username=global_pcm.pg_db_name, password=global_pcm.pg_password)
        self.assertTrue(logged_in)
        response = c.get('/app/logout', follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertCountEqual(response.redirect_chain,
                              [('/app/logout/', 301), ('/app/', 302), ('/app/login/?next=/app/', 302)])
