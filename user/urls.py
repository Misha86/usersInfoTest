
from django.urls import path
from . import views

app = 'user'


urlpatterns = [
    path('', views.hello, name="hello"),
]
