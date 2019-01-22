from cfenv import AppEnv

from inspector_db_app.logic.utils.logger_utils import get_logger

pg_service = AppEnv().get_service(label='postgresql')

logger = get_logger(__name__)
logger.info('PG service is {}'.format(pg_service))

postgresql_env_credentials = None if pg_service is None else pg_service.credentials
