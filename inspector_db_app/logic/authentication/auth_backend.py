from django.contrib.auth.models import User

from inspector_db_app.logic.utils.logger_utils import get_logger
from inspector_db_app.logic.utils.postgresql_env import postgresql_env_credentials

logger = get_logger(__name__)


# noinspection PyUnresolvedReferences
class DbAuthentication:
    def authenticate(self, _, username=None, password=None):

        if self._is_correct_credentials(username, password):
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                # Create a new user. There's no need to set a password
                # because only the password from Postgres is checked.
                user = User(username=username)
                user.save()
            return user
        return None

    @classmethod
    def get_user(cls, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

    @classmethod
    def _is_correct_credentials(cls, bd_name, db_password):
        if postgresql_env_credentials is None:
            logger.info('Unable to authenticate. Postgres credentials were not provided')
            return False
        return (bd_name, db_password) == (postgresql_env_credentials['dbname'], postgresql_env_credentials['password'])
