from django.urls import path

from . import views

app_name = 'dormitory'
urlpatterns = [
    path("", views.index, name="index"),
    path("dormitories", views.dormitories, name="dormitories"),
    path("<str:dorm_title>", views.dormitory, name="dormitory"),
    path("dormitory/create_dormitory",
         views.create_dormitory, name="create_dormitory"),
    path("dormitory/my_dormitory", views.my_dormitory, name="my_dormitory"),
    path("dormitory/my_review", views.my_review, name="my_review"),
    path("dormitory/remove_dormitory/<int:dormitory_id>",
         views.remove_dormitory, name="remove_dormitory"),
    path("dormitory/change_status/<int:dormitory_id>",
         views.change_status_dormitory, name="change_status_dormitory"),
    path("dormitory/review/<int:dormitory_id>",
         views.review_dormitory, name="review_dormitory"),
    path("dormitory/report_review/<int:review_id>",
         views.report_review, name="report_review"),

    path("dormitory/update_dormitory/<int:dormitory_id>",
         views.update_dormitory, name="update_dormitory"),



    path("dormitory/update_review/<int:review_id>",
         views.update_review, name="update_review"),


    path("dormitory/delete_review/<int:reviews_id>",
         views.delete_review, name="delete_review"),



    path("dormitory/delete_dormitory/<int:dormitory_id>",
         views.delete_dormitory, name="delete_dormitory"),

    path("dormitory/reset_report_review/<int:review_id>",
         views.reset_report_review, name="reset_report_review"),
]
