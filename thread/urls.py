from django.urls import path

from . import views

app_name = 'thread'
urlpatterns = [path("", views.index, name="index"),
               ]
