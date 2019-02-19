import os

from django.conf import global_settings

from app.logic.utils.logger_utils import get_logger

logger = get_logger(__name__)


def _str_to_bool(val):
    return bool(int(val))


class Option:
    def __init__(self, key, default, from_str_converter):
        self.key = key
        self.default = default
        self.from_str_converter = from_str_converter

    def get_option(self):
        return self._get_environ_val(self.key, self.default, self.from_str_converter)

    @classmethod
    def _get_environ_val(cls, key, default, as_type):
        try:
            val = as_type(os.environ[key])
        except KeyError:
            logger.debug('No environ found with key %s. Default val %s will be used.', key, default)
            val = default
        except (ValueError, TypeError) as e:
            logger.warn('Error during conversion of environ %s to type %s. Default val %s will be used. '
                        'Error was %s', key, as_type, default, e)
            val = default
        return val


class OptionDebug(Option):
    def __init__(self):
        super().__init__('DEBUG', global_settings.DEBUG, _str_to_bool)


class OptionSessionCookieAge(Option):
    def __init__(self):
        super().__init__('SESSION_COOKIE_AGE', global_settings.SESSION_COOKIE_AGE, int)


class OptionReadOnly(Option):
    def __init__(self):
        super().__init__('READONLY', True, _str_to_bool)


class OptionVcapServiceLabel(Option):
    def __init__(self):
        super().__init__('VCAP_SERVICE_LABEL', 'postgresql', str)


class OptionDbCredentials(Option):
    ENV_KEY = 'DB_CREDENTIALS'

    def __init__(self):
        super().__init__(self.ENV_KEY, '', str)
