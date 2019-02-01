from django.test import TestCase, Client

from project.test.postgres_container_utils import global_pcm
from project.test.test_db_utils import fill_test_db


class TestTableViews(TestCase):

    def tearDown(self):
        c = Client()
        c.logout()

    def test_get_table(self):
        table_name = 'test_table_view'
        column_names = ('a', 'b')
        fill_test_db(table_name, column_names, [])
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
