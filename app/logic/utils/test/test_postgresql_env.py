import unittest

from app.logic.utils.postgresql_env import InspectorDbAppEnv
from project.test_utils.postgres_container_utils import global_pcm, PostgresContainerManager


class TestInspectorDbAppEnv(unittest.TestCase):
    def test_get_bound_db_names(self):
        object_under_test = InspectorDbAppEnv()
        self.assertEqual(object_under_test.get_bound_db_names(), [global_pcm.pg_db_name])

    def test_get_bound_db_names_multiple_bound_postgres(self):
        with PostgresContainerManager() as local_pcm:
            object_under_test = InspectorDbAppEnv()
            self.assertCountEqual(object_under_test.get_bound_db_names(), [global_pcm.pg_db_name, local_pcm.pg_db_name])

    def test_get_service(self):
        object_under_test = InspectorDbAppEnv()
        db_service_env = object_under_test.get_service(global_pcm.pg_db_name)
        self.assertEqual(db_service_env.credentials.get('dbname'), global_pcm.pg_db_name)
        self.assertEqual(db_service_env.credentials.get('password'), global_pcm.pg_password)
