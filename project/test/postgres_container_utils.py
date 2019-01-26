import json
import os

import docker

from app.logic.utils.logger_utils import get_logger

logger = get_logger(__name__)


class PostgresContainerManager:
    def __init__(self):
        self.pg_password = 'test_pass'
        self.pg_db_name = 'test_db'
        self.port = None

        self._docker_client = docker.from_env()
        self._running_container = None

    def __enter__(self):
        self.run()
        return self

    def __exit__(self, *_):
        self.remove()

    def run(self):
        logger.info('Starting test container')
        container_port = '5432/tcp'
        running_container_id = self._docker_client.containers.run('postgres', detach=True,
                                                                  environment={'POSTGRES_PASSWORD': self.pg_password,
                                                                               'POSTGRES_USER': self.pg_db_name},
                                                                  ports={container_port: None}).id
        self._running_container = self._docker_client.containers.get(running_container_id)
        self.port = self._running_container.attrs['NetworkSettings']['Ports'][container_port][0]['HostPort']
        logger.info('Started test container with ID %s with port %s', running_container_id, self.port)
        self.add_environ_services_entry()

    def remove(self):
        if self._running_container is not None:
            logger.info('Removing test container')
            self._running_container.remove(force=True)
            logger.info('Successfully removed test container')

    def get_container_environment_dict(self):
        return {
            'credentials': {
                'dbname': self.pg_db_name,
                'hostname': 'localhost',
                'password': self.pg_password,
                'port': self.port,
                'username': self.pg_db_name
            }
        }

    def add_environ_services_entry(self):
        current_environ_services_entry = os.environ.get('VCAP_SERVICES', '{"postgresql": []}')
        parsed_environ_services = json.loads(current_environ_services_entry)
        parsed_environ_services['postgresql'].append(self.get_container_environment_dict())
        os.environ['VCAP_SERVICES'] = json.dumps(parsed_environ_services)


global_pcm = None
