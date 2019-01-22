from operator import itemgetter

from inspector_db_app.logic.utils.db_connection import get_connection
from inspector_db_app.logic.utils.logger_utils import get_logger

logger = get_logger(__name__)


class Tables:
    def __init__(self):
        self._limit = 100

    def get_public_tables(self):
        with get_connection() as c:
            cursor = c.cursor()
            cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='public'")
            if cursor.rowcount > self._limit:
                logger.warning('There are more tables than the limit allows. Only first %d will be returned (fetched: '
                               '%d)', self._limit, cursor.rowcount)
            return map(itemgetter(0), cursor.fetchmany(self._limit))
