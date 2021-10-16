from django.urls import path

from . import views

app_name = 'user'
urlpatterns = [path("", views.index, name="index"),
                path("about", views.index, name="about"),
               ]
