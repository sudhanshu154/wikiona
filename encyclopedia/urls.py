from django.urls import path

from . import views

app_name = 'wiki'

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>",views.entry,name="entry"),    
    path("search/", views.search, name="search"),
    path("search/wiki/<str:title>", views.entry, name="searchen"),
    path("random", views.random, name="random"),
    path("create", views.create, name="create"),
    path("wiki/<str:entry>/edit", views.edit, name="edit"),

]
