from django.contrib.auth.models import User

from app.logic.utils.logger_utils import get_logger
from app.logic.utils.postgresql_env import InspectorDbAppEnv

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
        db_service_env = InspectorDbAppEnv().get_service(db_name)
        if db_service_env is None:
            logger.info('Unable to authenticate db with name %s. Postgres credentials were not provided', db_name)
            return False
        return (db_name, db_password) == (
            db_service_env.credentials.get('dbname'), db_service_env.credentials.get('password'))
