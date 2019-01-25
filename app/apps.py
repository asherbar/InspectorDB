from django.apps import AppConfig

from app.logic.utils.logger_utils import get_logger


logger = get_logger(__name__)


class InspectordbappConfig(AppConfig):
    name = 'app'
    verbose_name = "Inspector D.B."
