from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib import messages
from .models import *
import datetime
from .forms import MarkdownForm
# Create your views here.


def index(request):
    thread_list = []
    # use when user search Dormitory
    if request.method == "POST":
        search = request.POST["search"]
        thread_list = []
        for x in Thread.objects.all():
            if x.search(search) and x.report < 10:
                thread_list.append(x)
    # use when user didnt search Dormitory so it will return all dormitory
    else:
        for n in Thread.objects.all():
            if n.report < 10:
                thread_list.append(n)
    return render(request, "thread/index.html", {"thread_list": thread_list})

def thread(request,thread_id) :
    this_thread = get_object_or_404(Thread, id=thread_id)

    return render(request, "thread/thread.html", {
        "thread": this_thread,
    })