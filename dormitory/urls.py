from django.urls import path

from . import views

app_name = 'dormitory'
urlpatterns = [
                path("", views.index, name="index"),
                path("dormitories", views.dormitories, name="dormitories"),
                path("<str:dorm_title>", views.dormitory,name = "dormitory"),
                path("dormitory/create_dormitory",views.create_dormitory,name = "create_dormitory"),
]
