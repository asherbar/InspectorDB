from django.contrib.auth.forms import AuthenticationForm
from django.forms import ChoiceField

from app.logic.utils.db_env import DbEnv


class DbAuthenticationForm(AuthenticationForm):
    username = ChoiceField(choices=((db_name, db_name) for db_name in DbEnv().get_db_names()))
