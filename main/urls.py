from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name='index'),
    path("authorize", views.authorize, name='authorize'),
    path("get_rnd_number", views.get_rnd_number, name='get_rnd_number'),
]