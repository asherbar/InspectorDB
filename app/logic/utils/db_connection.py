import psycopg2
import psycopg2.pool

from app.logic.utils.logger_utils import get_logger
from app.logic.utils.postgresql_env import InspectorDbAppEnv
from project.common.exception import InspectorDbException
from project.options import Options

logger = get_logger(__name__)


class DbConnectionError(InspectorDbException):
    def __init__(self, db_credentials):
        super().__init__(f'Error while trying to connect to DB with credentials {db_credentials}')


def _create_connection_pools():
    connection_pools = {}
    db_app_env = InspectorDbAppEnv()
    for bound_db in db_app_env.get_bound_db_names():
        db_credentials = db_app_env.get_service(bound_db).credentials
        try:
            connection_pools[bound_db] = psycopg2.pool.ThreadedConnectionPool(1, 10,
                                                                              user=db_credentials['username'],
                                                                              password=db_credentials['password'],
                                                                              host=db_credentials['hostname'],
                                                                              port=db_credentials['port'],
                                                                              database=db_credentials['dbname'])
        except KeyError as e:
            logger.error('Unable to initialize DB with name %s. Missing "%s" key from credentials. Got: %s', bound_db,
                         e.args[0], db_credentials)
        except psycopg2.OperationalError as e:
            logger.exception('Error while trying to connect to DB with credentials %s', db_credentials)
            raise DbConnectionError(db_credentials) from e

    return connection_pools


_connection_pools = None


class _PooledConnection:
    def __init__(self, connection, db_name):
        self._db_name = db_name
        self._connection = connection

    def __enter__(self):
        return self

    def __exit__(self, *_):
        _connection_pools[self._db_name].putconn(self._connection)

    def __getattr__(self, attr):
        return getattr(self._connection, attr)


def get_connection(db_name):
    global _connection_pools
    if _connection_pools is None:
        _connection_pools = _create_connection_pools()
    connection = _connection_pools[db_name].getconn()
    connection.readonly = Options.get_readonly()
    return _PooledConnection(connection, db_name)
