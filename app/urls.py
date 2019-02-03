from django.contrib.auth import views as auth_views
from django.urls import path

from app.logic.authentication.db_authentication_form import DbAuthenticationForm
from . import views

urlpatterns = [
    path('', views.table_index, name=views.table_index.view_name),
    path('table/<table_name>', views.get_table, name=views.get_table.view_name),
    path('query/', views.execute_query, name=views.execute_query.view_name),
    path('login/', auth_views.LoginView.as_view(authentication_form=DbAuthenticationForm), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page=views.table_index.view_name), name='logout'),
]
