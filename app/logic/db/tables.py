from operator import itemgetter

from app.logic.utils.db_connection import get_connection
from app.logic.utils.logger_utils import get_logger

logger = get_logger(__name__)


class Tables:
    def __init__(self, db_name):
        self._db_name = db_name
        self._limit = 100

    def get_public_tables(self):
        with get_connection(self._db_name) as c:
            cursor = c.cursor()
            cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='public'")
            if cursor.rowcount > self._limit:
                logger.warning('There are more tables than the limit allows. Only first %d will be returned (fetched: '
                               '%d)', self._limit, cursor.rowcount)
            return map(itemgetter(0), cursor.fetchmany(self._limit))
