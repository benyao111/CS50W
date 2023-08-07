from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.landingpage, name="landingpage"),
    path("createnewpage", views.createnewpage, name="createnewpage"),
    path("wiki/<str:title>/edit", views.edit, name="edit"),
    path("random", views.randomm, name="random")
]
