from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("random", views.random, name="random"),
    path("create", views.create, name="create"),
    path("<str:title>", views.show, name="show"),
]
