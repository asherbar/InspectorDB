import json
import os

from cfenv import AppEnv, Service

from inspector_db_app.logic.utils.logger_utils import get_logger


# A place holder until https://github.com/jmcarp/py-cfenv/pull/6 is approved
class ExtendedAppEnv(AppEnv):
    def __init__(self):
        super().__init__()
        env_services = json.loads(os.getenv('VCAP_SERVICES', '{}'))
        self.named_services = {service_name: list(map(Service, services_list))
                               for service_name, services_list in env_services.items()}


pg_service = ExtendedAppEnv().get_service(label='postgresql')

logger = get_logger(__name__)
logger.info('PG service is {}'.format(pg_service))

postgresql_env_credentials = None if pg_service is None else pg_service.credentials


def get_bound_db_names():
    return [s.credentials['dbname'] for s in ExtendedAppEnv().named_services.get('postgresql', []) if
            'dbname' in s.credentials]
