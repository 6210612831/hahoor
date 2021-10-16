from django.urls import path

from . import views

app_name = 'user'
urlpatterns = [path("", views.index, name="index"),
               path("about", views.about, name="about"),
               path("login", views.login, name="login"),
               path("login_check", views.login_check, name="login_check"),
               path("register", views.register, name="register"),
               ]
