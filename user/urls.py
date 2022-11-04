"""Module with user app urls."""
from django.urls import path

from . import views

app = 'user'

urlpatterns = [
    path('', views.users_list, name='users_list'),
    path('login', views.sing_in, name='login'),
    path('logout', views.logout_view, name='logout'),
    path('upload-data', views.upload_files, name='upload_files'),
]
