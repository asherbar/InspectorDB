from django.contrib.auth.forms import AuthenticationForm, UsernameField

from inspector_db_app.apps import DEFAULT_USERNAME


class DbAuthenticationForm(AuthenticationForm):
    username = UsernameField(disabled=True, initial=DEFAULT_USERNAME)
