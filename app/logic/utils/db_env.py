import json
import os

from app.logic.utils.logger_utils import get_logger
from project.options.option import OptionVcapServiceLabel, OptionDbCredentials

logger = get_logger(__name__)


def refresh_env(func):
    def wrapper(self, *args, **kwargs):
        self._db_credentials_list = DbCredentials.build_credentials_from_env()
        return func(self, *args, **kwargs)

    return wrapper


class DbEnv:

    def __init__(self):
        self._db_credentials_list = None

    @refresh_env
    def get_db_names(self):
        return list(map(lambda db_credentials: db_credentials.dbname, self._db_credentials_list))

    @refresh_env
    def get_db_credentials(self, db_name):
        return next((
            db_credentials for db_credentials in self._db_credentials_list if db_credentials.dbname == db_name), None)


class DbCredentials:
    def __init__(self, username, password, hostname, port, dbname, **_):
        self.username = username
        self.password = password
        self.hostname = hostname
        self.port = port
        self.dbname = dbname

    @classmethod
    def build_credentials_from_env(cls):
        db_credentials_option = OptionDbCredentials().get_option()
        if db_credentials_option:
            db_credentials_list = cls._get_credentials_list_from_db_credentials(db_credentials_option)
        else:
            db_credentials_list = cls._get_db_credentials_list_from_vcap_services()
        built_instances = []
        for db_credentials in db_credentials_list:
            try:
                built_instances.append(DbCredentials(**db_credentials))
            except TypeError:
                logger.exception('Unable to build DbCredentials object from %s', db_credentials)
        return built_instances

    @classmethod
    def _get_db_credentials_list_from_vcap_services(cls):
        logger.debug('Db Credentials option not found')
        vcap_services_key = 'VCAP_SERVICES'
        vcap_services_value = os.getenv(vcap_services_key, '{}')
        try:
            vcap_services = json.loads(vcap_services_value)
        except json.decoder.JSONDecodeError:
            logger.exception('The value of key %s must be a valid JSON, instead it is %s',
                             vcap_services_key, vcap_services_value)
            db_credentials_list = []
        else:
            service_label = OptionVcapServiceLabel().get_option()
            db_credentials_list = []
            for service in vcap_services.get(service_label, []):
                try:
                    db_credentials_list.append(service['credentials'])
                except KeyError:
                    logger.debug('"credentials" key missing from %s', service)
        return db_credentials_list

    @classmethod
    def _get_credentials_list_from_db_credentials(cls, db_credentials_option):
        logger.debug('Db Credentials option found')
        try:
            db_credentials_list = json.loads(db_credentials_option)
        except json.decoder.JSONDecodeError:
            logger.exception('The value of key %s must be a valid JSON list, instead it is %s',
                             OptionDbCredentials.ENV_KEY, db_credentials_option)
            db_credentials_list = []
        if not isinstance(db_credentials_list, list):
            logger.error('Expected a list, instead got: %s', db_credentials_list)
            db_credentials_list = []
        return db_credentials_list
