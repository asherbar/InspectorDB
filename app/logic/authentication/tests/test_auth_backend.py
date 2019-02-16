import django.test as django_test

from app.logic.authentication.auth_backend import DbAuthentication
from project.test_utils.postgres_container_utils import PostgresContainerManager, global_pcm


class TestDbAuthentication(django_test.TestCase):

    def test_authenticate_wrong_db(self):
        object_under_test = DbAuthentication()
        self.assertIsNone(object_under_test.authenticate(None, 'wrong', 'wrong'))

    def test_authenticate_wrong_password(self):
        object_under_test = DbAuthentication()
        self.assertIsNone(object_under_test.authenticate(None, global_pcm.pg_db_name, 'wrong'))

    def test_authenticate_correct_credentials(self):
        object_under_test = DbAuthentication()
        authenticated_user = object_under_test.authenticate(None, global_pcm.pg_db_name,
                                                            global_pcm.pg_password)
        self.assertFalse(authenticated_user.password)
        self.assertEqual(authenticated_user.username, global_pcm.pg_db_name)
        self.assertEqual(object_under_test.get_user(authenticated_user.id), authenticated_user)

    def test_authenticate_multiple_dbs(self):
        with PostgresContainerManager() as local_pcm:
            object_under_test = DbAuthentication()
            authenticated_user_1 = object_under_test.authenticate(None, global_pcm.pg_db_name,
                                                                  global_pcm.pg_password)
            self.assertFalse(authenticated_user_1.password)
            self.assertEqual(authenticated_user_1.username, global_pcm.pg_db_name)
            self.assertEqual(object_under_test.get_user(authenticated_user_1.id), authenticated_user_1)

            authenticated_user_2 = object_under_test.authenticate(None, local_pcm.pg_db_name,
                                                                  local_pcm.pg_password)
            self.assertFalse(authenticated_user_2.password)
            self.assertEqual(authenticated_user_2.username, local_pcm.pg_db_name)
            self.assertEqual(object_under_test.get_user(authenticated_user_2.id), authenticated_user_2)
