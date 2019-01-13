from inspector_db_app.logic.db_connection import get_connection
from inspector_db_app.logic.logger_utils import get_logger

logger = get_logger(__name__)


class TableDoesNotExist(Exception):
    def __init__(self, table_name):
        super().__init__('No such table: {}'.format(table_name))


class Table:
    def __init__(self, table_name):
        self._table_name = table_name
        if not self._table_exists():
            logger.info('Table %s not found', table_name)
            raise TableDoesNotExist(table_name)

    def get_columns(self):
        with get_connection() as c:
            cursor = c.cursor()
            cursor.execute('SELECT * FROM {} LIMIT 1'.format(self._table_name))
            return [desc[0] for desc in cursor.description]

    def get_records(self, limit):
        with get_connection() as c:
            cursor = c.cursor()
            cursor.execute('SELECT * FROM {} LIMIT {}'.format(self._table_name, limit))
            return cursor.fetchmany(limit)

    def _table_exists(self):
        with get_connection() as c:
            cursor = c.cursor()
            cursor.execute("SELECT * FROM information_schema.tables WHERE table_name=%s", (self._table_name.lower(),))
            return bool(cursor.rowcount)
