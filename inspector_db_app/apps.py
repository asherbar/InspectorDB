from django.apps import AppConfig

from inspector_db_app.logic.utils.logger_utils import get_logger
from inspector_db_app.logic.utils.postgresql_env import postgresql_env_credentials

DEFAULT_USERNAME = 'a'

logger = get_logger(__name__)


def create_default_user():
    from django.contrib.auth.models import User
    if postgresql_env_credentials is None:
        logger.info('Postgres credentials not found. Using default password instead')
        password = 'p'
    else:
        password = postgresql_env_credentials['password']
    # noinspection PyUnresolvedReferences
    try:
        default_user = User.objects.get_by_natural_key(DEFAULT_USERNAME)
    except User.DoesNotExist:
        logger.info('Default user not found. Creating it now...')
        default_user = User.objects.create_user(DEFAULT_USERNAME, 'a@sap.com')

    logger.info("Updating default user's password")
    default_user.set_password(password)
    default_user.save()


class InspectordbappConfig(AppConfig):
    name = 'inspector_db_app'
    verbose_name = "Inspector D.B."

    def ready(self):
        create_default_user()
