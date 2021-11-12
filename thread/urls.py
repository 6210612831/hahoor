from django.urls import path

from . import views

app_name = 'thread'
urlpatterns = [path("", views.index, name="index"),
               path("<int:thread_id>", views.thread, name="thread"),
               path("my_thread", views.my_thread, name="my_thread"),
               path("create_thread", views.create_thread, name="create_thread"),
               path("reply_thread/<int:thread_id>",
                    views.reply_thread, name="reply_thread"),
               path("report_thread/<int:thread_id>",
                    views.report_thread, name="report_thread"),
               path("report_reply/<int:thread_id>/<int:subthread_id>",
                    views.report_subthread, name="report_subthread"),
               path("update/<int:thread_id>",
                    views.update_thread, name="update_thread"),
               path("delete_thread/<int:thread_id>",
                    views.delete_thread, name="delete_thread"),
               path("update_reply/<int:sub_thread_id>",
                    views.update_reply, name="update_reply"),
               path("delete_reply/<int:sub_thread_id>",
                    views.delete_reply, name="delete_reply"),


               path("reset_report_reply/<int:sub_thread_id>",
                    views.reset_report_reply, name="reset_report_reply"),
               path("reset_report_thread/<int:thread_id>",
                    views.reset_report_thread, name="reset_report_thread"),
               ]
