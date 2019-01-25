from django.urls import path
from django.contrib.auth import views as auth_views

from app.logic.authentication.db_authentication_form import DbAuthenticationForm
from . import views

urlpatterns = [
    path('', views.table_index, name='table_index'),
    path('table/<table_name>', views.get_table, name='table'),
    path('query/', views.execute_query, name='query'),
    path('login/', auth_views.LoginView.as_view(authentication_form=DbAuthenticationForm), name='login', ),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]
