from django.contrib.auth.forms import AuthenticationForm
from django.forms import ChoiceField

from inspector_db_app.logic.utils.postgresql_env import get_bound_db_names


class DbAuthenticationForm(AuthenticationForm):
    username = ChoiceField(choices=((db_name, db_name) for db_name in get_bound_db_names()))
