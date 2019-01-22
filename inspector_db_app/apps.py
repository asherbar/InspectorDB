from django.apps import AppConfig

from inspector_db_app.logic.utils.logger_utils import get_logger


logger = get_logger(__name__)


class InspectordbappConfig(AppConfig):
    name = 'inspector_db_app'
    verbose_name = "Inspector D.B."
