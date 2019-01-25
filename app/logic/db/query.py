from app.logic.utils.db_connection import get_connection


class Query:
    def __init__(self, query_str, limit=50):
        self._limit = limit
        self._query_str = query_str
        with get_connection() as c:
            self._cursor = c.cursor()
            self._cursor.execute(self._query_str)

    def get_column_names(self):
        return [desc[0] for desc in self._cursor.description]

    def get_records(self):
        return self._cursor.fetchmany(self._limit)
