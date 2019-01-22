import psycopg2
from psycopg2 import pool

from inspector_db_app.logic.utils.postgresql_env import postgresql_env_credentials


def _create_connection_pool():
    if postgresql_env_credentials is not None:
        return psycopg2.pool.ThreadedConnectionPool(1, 10, user=postgresql_env_credentials['username'],
                                                    password=postgresql_env_credentials['password'],
                                                    host=postgresql_env_credentials['hostname'],
                                                    port=postgresql_env_credentials['port'],
                                                    database=postgresql_env_credentials['dbname'])


_connection_pool = _create_connection_pool()


class _PooledConnection:
    def __init__(self, connection):
        self._connection = connection

    def __enter__(self):
        return self

    def __exit__(self, *_):
        _connection_pool.putconn(self._connection)

    def __getattr__(self, attr):
        return getattr(self._connection, attr)


def get_connection():
    connection = _connection_pool.getconn()

    return _PooledConnection(connection)
