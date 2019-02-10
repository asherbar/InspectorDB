from django.contrib.auth import views as auth_views
from django.urls import path

from app.logic.authentication.db_authentication_form import DbAuthenticationForm
from app.views.index_view import IndexView
from app.views.query_view import QueryView
from app.views.table_view import TableView

urlpatterns = [
    path('', IndexView.as_view(), name=IndexView.view_name),
    path('table/<table_name>', TableView.as_view(), name=TableView.view_name),
    path('query/', QueryView.as_view(), name=QueryView.view_name),
    path('login/', auth_views.LoginView.as_view(authentication_form=DbAuthenticationForm), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page=IndexView.view_name), name='logout'),
]
