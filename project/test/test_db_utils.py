import psycopg2
from pypika import Table, Query

from app.logic.utils.logger_utils import get_logger
from project.test.postgres_container_utils import global_pcm

logger = get_logger(__name__)


def fill_test_db(table_name, column_names, data):
    typed_column_names = (cn + ' VARCHAR(255)' for cn in column_names)
    table = Table(table_name)

    insert_data_command = Query.into(table).insert(*data).get_sql()
    with psycopg2.connect(user=global_pcm.pg_db_name, password=global_pcm.pg_password, port=global_pcm.port,
                          host='localhost') as conn:
        with conn.cursor() as cur:
            create_table_command = 'CREATE TABLE {} ({})'.format(table_name, ', '.join(typed_column_names))
            logger.debug('Creating test database %s', table_name)
            cur.execute(create_table_command)
            if data:
                logger.debug('Inserting test data %s', data)
                cur.execute(insert_data_command)
