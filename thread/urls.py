from django.urls import path

from . import views

app_name = 'thread'
urlpatterns = [ path("", views.index, name="index"),
                path("<int:thread_id>", views.thread,name = "thread"),
                path("my_thread",views.my_thread,name = "my_thread"),
               ]
