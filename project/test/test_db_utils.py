import psycopg2
from pypika import Table, Query

from app.logic.utils.logger_utils import get_logger
from project.test.postgres_container_utils import global_pcm

logger = get_logger(__name__)


class TestDbFiller:
    def __init__(self, table_name, column_names, data):
        self.table_name = table_name
        self.column_names = column_names
        self.data = data

    def __enter__(self):
        self.fill_test_db()
        return self

    def __exit__(self, *_):
        self.drop_test_table()

    def fill_test_db(self):
        typed_column_names = (cn + ' VARCHAR(255)' for cn in self.column_names)
        table = Table(self.table_name)

        insert_data_command = Query.into(table).insert(*self.data).get_sql()
        with psycopg2.connect(user=global_pcm.pg_db_name, password=global_pcm.pg_password, port=global_pcm.port,
                              host='localhost') as conn:
            with conn.cursor() as cur:
                create_table_command = 'CREATE TABLE {} ({})'.format(self.table_name, ', '.join(typed_column_names))
                logger.debug('Creating test database %s', self.table_name)
                cur.execute(create_table_command)
                if self.data:
                    logger.debug('Inserting test data %s', self.data)
                    cur.execute(insert_data_command)

    def drop_test_table(self):
        with psycopg2.connect(user=global_pcm.pg_db_name, password=global_pcm.pg_password, port=global_pcm.port,
                              host='localhost') as conn:
            with conn.cursor() as cur:
                drop_table_command = f'DROP TABLE {self.table_name}'
                logger.debug('Dropping test database %s', self.table_name)
                cur.execute(drop_table_command)
