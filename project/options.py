import os

from django.conf import global_settings

from app.logic.utils.logger_utils import get_logger

logger = get_logger(__name__)


def _str_to_bool(val):
    return bool(int(val))


class Options:
    readonly_default = True

    @classmethod
    def get_debug(cls):
        return cls._get_environ_val('DEBUG', global_settings.DEBUG, _str_to_bool)

    @classmethod
    def get_session_cookie_age(cls):
        return cls._get_environ_val('SESSION_COOKIE_AGE', global_settings.SESSION_COOKIE_AGE, int)

    @classmethod
    def get_readonly(cls):
        return cls._get_environ_val('READONLY', cls.readonly_default, _str_to_bool)

    @classmethod
    def _get_environ_val(cls, key, default, as_type):
        try:
            val = as_type(os.environ[key])
        except KeyError as e:
            logger.info('No environ found with key %s. Default val %s will be used.', key, default)
            val = default
        except (ValueError, TypeError) as e:
            logger.warn('Error during conversion of environ %s to type %s. Default val %s will be used. '
                        'Error was %s', key, as_type, default, e)
            val = default
        return val
