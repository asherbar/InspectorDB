import json
import os

from cfenv import AppEnv, Service


def refresh_env(func):
    def wrapper(self, *args, **kwargs):
        self._app_env = AppEnv()
        env_services = json.loads(os.getenv('VCAP_SERVICES', '{}'))
        self._named_services = {service_name: list(map(Service, services_list))
                                for service_name, services_list in env_services.items()}
        return func(self, *args, **kwargs)

    return wrapper


class InspectorDbAppEnv:

    def __init__(self):
        self._app_env = None
        self._named_services = None

    @refresh_env
    def get_bound_db_names(self):
        return [s.credentials['dbname'] for s in self._named_services.get('postgresql', []) if
                'dbname' in s.credentials]

    @refresh_env
    def get_service(self, db_name):
        return next((s for s in self._app_env.services if s.credentials.get('dbname') == db_name), None)
