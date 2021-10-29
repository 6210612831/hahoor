from django.urls import path

from . import views

app_name = 'user'
urlpatterns = [path("", views.index, name="index"),
               path("login", views.login, name="login"),
               path("login_check", views.login_check, name="login_check"),
               path("register", views.register_view, name="register"),
               path("confirm_register", views.register, name="confirm_register"),
               path("about", views.about, name="about"),
               path("logout", views.logout, name="logout"),
               path("admin",views.admin_view,name="admin")
               ]
