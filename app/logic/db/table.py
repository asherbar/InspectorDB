import psycopg2.extras

from app.logic.utils.db_connection import get_connection
from app.logic.utils.logger_utils import get_logger
from project.common.exception import InspectorDbException

logger = get_logger(__name__)


class TableDoesNotExist(InspectorDbException):
    def __init__(self, table_name):
        super().__init__('No such table: {}'.format(table_name))


class Table:
    def __init__(self, db_name, table_name, limit=50):
        self._db_name = db_name
        self._table_name = table_name
        self._limit = limit
        if not self._table_exists():
            logger.info('Table %s not found', table_name)
            raise TableDoesNotExist(table_name)

    @property
    def table_name(self):
        return self._table_name

    def get_columns(self):
        with get_connection(self._db_name) as c:
            cursor = c.cursor()
            cursor.execute(f'SELECT * FROM {self._table_name} LIMIT 1')
            return [desc[0] for desc in cursor.description]

    def _table_exists(self):
        with get_connection(self._db_name) as c:
            cursor = c.cursor()
            cursor.execute("SELECT * FROM information_schema.tables WHERE table_name=%s", (self._table_name.lower(),))
            return bool(cursor.rowcount)

    def get_total_number_of_rows(self):
        with get_connection(self._db_name) as c:
            cursor = c.cursor(cursor_factory=psycopg2.extras.DictCursor)
            cursor.execute(f'SELECT COUNT (*) FROM {self._table_name}')
            return cursor.fetchone()['count']

    def get_records_by_page(self, page):
        with get_connection(self._db_name) as c:
            cursor = c.cursor()
            cursor.execute(f'SELECT * FROM {self._table_name} LIMIT {self.limit} OFFSET {(page - 1) * self.limit}')
            return cursor.fetchmany(self.limit)

    @property
    def limit(self):
        return self._limit
