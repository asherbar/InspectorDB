from django.contrib.auth.forms import AuthenticationForm
from django.forms import ChoiceField

from app.logic.utils.postgresql_env import InspectorDbAppEnv


class DbAuthenticationForm(AuthenticationForm):
    username = ChoiceField(choices=((db_name, db_name) for db_name in InspectorDbAppEnv().get_bound_db_names()))
