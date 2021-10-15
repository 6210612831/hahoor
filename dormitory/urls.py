from django.urls import path

from . import views

app_name = 'dormitory'
urlpatterns = [path("", views.index, name="index"),
               ]
