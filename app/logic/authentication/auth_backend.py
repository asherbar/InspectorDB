from django.contrib.auth.models import User

from app.logic.utils.db_env import DbEnv
from app.logic.utils.logger_utils import get_logger

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
    def _is_correct_credentials(cls, db_name, db_password):
        db_credentials = DbEnv().get_db_credentials(db_name)
        if db_credentials is None:
            logger.info('Unable to authenticate db with name %s. Postgres credentials were not provided', db_name)
            return False
        return (db_name, db_password) == (db_credentials.dbname, db_credentials.password)
