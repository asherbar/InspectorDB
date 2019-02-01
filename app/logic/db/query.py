import psycopg2

from app.logic.utils.db_connection import get_connection
from app.logic.utils.logger_utils import get_logger
from project.common.exception import InspectorDbException

logger = get_logger(__name__)


class QueryExecutionError(InspectorDbException):
    def __init__(self, query_str):
        super().__init__(f'Error while trying to execute query "{query_str}"')


class Query:
    def __init__(self, db_name, query_str, limit=50):
        self._db_name = db_name
        self._limit = limit
        self._query_str = query_str
        self._rows_affected = None
        with get_connection(self._db_name) as c:
            self._cursor = c.cursor()
            try:
                self._cursor.execute(self._query_str)
            except psycopg2.ProgrammingError as e:
                logger.error('Error while trying to execute query "%s"', self._query_str, e)
                raise QueryExecutionError(self._query_str) from e

    def get_column_names(self):
        cursor_description = self._cursor.description
        return [] if cursor_description is None else [desc[0] for desc in cursor_description]

    def get_query_result(self):
        """
        :return: a list of retrieved rows for DQL statements (like SELECT) or the number of affected rows for DML
        statements (like UPDATE or INSERT)
        """
        return self._cursor.rowcount if self.is_dml else self._cursor.fetchmany(self._limit)

    @property
    def is_dml(self):
        return self._cursor.description is None
