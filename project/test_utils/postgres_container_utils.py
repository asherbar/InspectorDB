import json
import os
from time import time as now, sleep

import docker
import docker.errors
import psycopg2
import requests

from app.logic.utils.logger_utils import get_logger

logger = get_logger(__name__)


class PostgresContainerManager:
    def __init__(self):
        self.hostname = 'localhost'
        self.pg_password = 'test_pass'
        self.pg_db_name = 'test_db'
        self.port = None
        self._wait_timeout_sec = 10

        self._docker_client = docker.from_env()
        self._running_container = None

    def __enter__(self):
        self._run()
        return self

    def __exit__(self, *_):
        self._remove()

    def _run(self):
        try:
            postgres_image = self._docker_client.images.get('postgres')
        except docker.errors.ImageNotFound:
            logger.info('postgres docker image not found. Trying to pull the image')
            postgres_image = self._docker_client.images.pull('postgres', 'latest')
        except requests.exceptions.ConnectionError:
            logger.error('Unable to connect to docker client. Make sure docker is installed and running')
            raise
        logger.info('Starting test container')
        container_port = '5432/tcp'
        running_container_id = self._docker_client.containers.run(postgres_image, detach=True,
                                                                  environment={'POSTGRES_PASSWORD': self.pg_password,
                                                                               'POSTGRES_USER': self.pg_db_name},
                                                                  ports={container_port: None}).id
        self._running_container = self._docker_client.containers.get(running_container_id)
        self.port = self._running_container.attrs['NetworkSettings']['Ports'][container_port][0]['HostPort']
        logger.info('Started test container with ID %s with port %s', running_container_id, self.port)
        self._add_environ_services_entry()
        self._wait_for_db()

    def _remove(self):
        if self._running_container is not None:
            logger.info('Removing test container')
            self._running_container.remove(force=True)
            logger.info('Successfully removed test container')
            self.remove_environ_services_entry()

    def _get_container_environment_dict(self):
        return {
            'credentials': {
                'dbname': self.pg_db_name,
                'hostname': self.hostname,
                'password': self.pg_password,
                'port': self.port,
                'username': self.pg_db_name
            }
        }

    def _add_environ_services_entry(self):
        current_environ_services_entry = os.environ.get('VCAP_SERVICES', '{"postgresql": []}')
        parsed_environ_services = json.loads(current_environ_services_entry)
        parsed_environ_services['postgresql'].append(self._get_container_environment_dict())
        os.environ['VCAP_SERVICES'] = json.dumps(parsed_environ_services)

    def _wait_for_db(self):
        """ Wait for database to accept connections. Raises socket.timeout if not able to connect within
        self._wait_timeout_sec
        """
        end = now() + self._wait_timeout_sec

        while True:
            next_timeout = end - now()
            if next_timeout < 0:
                raise TimeoutError(f'Unable to connect within {self._wait_timeout_sec} seconds')
            try:
                with psycopg2.connect(user=self.pg_db_name, password=self.pg_password, port=self.port,
                                      host=self.hostname):
                    logger.info('Connection test passed successfully')
                    return
            except psycopg2.OperationalError as e:
                logger.info('Error while testing connection: %s', e)
                sleep(1)

    def remove_environ_services_entry(self):
        current_environ_services_entry = os.environ.get('VCAP_SERVICES', '{"postgresql": []}')
        parsed_environ_services = json.loads(current_environ_services_entry)
        parsed_environ_services['postgresql'].remove(self._get_container_environment_dict())
        os.environ['VCAP_SERVICES'] = json.dumps(parsed_environ_services)


global_pcm = None
