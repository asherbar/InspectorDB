import unittest
from unittest import mock

from app.logic.utils.db_env import DbEnv
from project.test_utils.postgres_container_utils import global_pcm, PostgresContainerManager


class TestInspectorDbEnv(unittest.TestCase):
    def test_get_bound_db_names(self):
        object_under_test = DbEnv()
        self.assertEqual(object_under_test.get_db_names(), [global_pcm.pg_db_name])

    def test_get_bound_db_names_multiple_bound_postgres(self):
        with PostgresContainerManager() as local_pcm:
            object_under_test = DbEnv()
            self.assertCountEqual(object_under_test.get_db_names(), [global_pcm.pg_db_name, local_pcm.pg_db_name])

    def test_get_bound_db_names_not_json(self):
        with mock.patch.dict('os.environ', {'DB_CREDENTIALS': 'NOT_JSON!'}):
            object_under_test = DbEnv()
            db_names = object_under_test.get_db_names()
            self.assertEqual(db_names, [])

        with mock.patch.dict('os.environ', {'VCAP_SERVICES': 'NOT_JSON!'}):
            object_under_test = DbEnv()
            db_names = object_under_test.get_db_names()
            self.assertEqual(db_names, [])

    def test_get_bound_db_names_missing_params(self):
        db_name_bad = 'bla'
        db_name = 'DB'
        username = 'UN'
        pswd = 'P'
        hostname = 'HN'
        port = 1234
        good_credentials = f'{{"dbname":"{db_name}","hostname":"{hostname}","password":"{pswd}","port":{port},' \
                           f'"username":"{username}"}}'
        bad_credentials = f'{{"dbname":"{db_name_bad}"}}'
        with mock.patch.dict('os.environ', {'DB_CREDENTIALS': f'[{good_credentials}, {bad_credentials}]'}):
            object_under_test = DbEnv()
            db_names = object_under_test.get_db_names()
            self.assertEqual(db_names, [db_name])

        with mock.patch.dict('os.environ', {'VCAP_SERVICES': f'{{"postgresql":[{{"credentials": {good_credentials}}}, '
                                                             f'{{"credentials": {bad_credentials}}}]}}'}):
            object_under_test = DbEnv()
            db_names = object_under_test.get_db_names()
            self.assertEqual(db_names, [db_name])

    def test_get_bound_db_names_not_list(self):
        db_name = 'DB'
        username = 'UN'
        pswd = 'P'
        hostname = 'HN'
        port = 1234
        with mock.patch.dict('os.environ',
                             {'DB_CREDENTIALS': f'{{"dbname":"{db_name}","hostname":"{hostname}",'
                                                f'"password":"{pswd}","port":{port},"username":"{username}"}}'}):
            object_under_test = DbEnv()
            db_names = object_under_test.get_db_names()
            self.assertEqual(db_names, [])

    def test_get_bound_db_names_missing_credentials_key(self):
        db_name = 'DB'
        username = 'UN'
        pswd = 'P'
        hostname = 'HN'
        port = 1234
        good_credentials = f'{{"dbname":"{db_name}","hostname":"{hostname}","password":"{pswd}","port":{port},' \
                           f'"username":"{username}"}}'
        with mock.patch.dict('os.environ', {'VCAP_SERVICES': f'{{"postgresql": [{{"CREDS": {good_credentials} }}] }}'}):
            object_under_test = DbEnv()
            db_names = object_under_test.get_db_names()
            self.assertEqual(db_names, [])

    def test_get_db_credentials_from_vcap(self):
        object_under_test = DbEnv()
        db_credentials = object_under_test.get_db_credentials(global_pcm.pg_db_name)
        self.assertEqual(db_credentials.dbname, global_pcm.pg_db_name)
        self.assertEqual(db_credentials.password, global_pcm.pg_password)

    def test_get_db_credentials_from_db_credentials(self):
        db_name = 'DB'
        username = 'UN'
        pswd = 'P'
        hostname = 'HN'
        port = 1234

        with mock.patch.dict('os.environ',
                             {'DB_CREDENTIALS': f'[{{"dbname":"{db_name}","hostname":"{hostname}",'
                                                f'"password":"{pswd}","port":{port},"username":"{username}"}}]'}):
            object_under_test = DbEnv()
            db_credentials = object_under_test.get_db_credentials(db_name)
            self.assertEqual(db_credentials.dbname, db_name)
            self.assertEqual(db_credentials.username, username)
            self.assertEqual(db_credentials.password, pswd)
            self.assertEqual(db_credentials.hostname, hostname)
            self.assertEqual(db_credentials.port, port)

    def test_get_db_credentials_from_db_credentials_not_json(self):
        with mock.patch.dict('os.environ', {'DB_CREDENTIALS': 'NOT_JSON!'}):
            object_under_test = DbEnv()
            db_credentials = object_under_test.get_db_credentials('ANY')
            self.assertIsNone(db_credentials)
