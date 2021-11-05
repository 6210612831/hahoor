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
            if n.report < 20:
                thread_list.append(n)
    return render(request, "thread/index.html", {"thread_list": thread_list[::-1]})

def thread(request,thread_id) :
    this_thread = get_object_or_404(Thread, id=thread_id)

    return render(request, "thread/thread.html", {
        "thread": this_thread,
    })

def my_thread(request):
    if not request.user.is_authenticated:
        messages.warning(request, "Login First to proceed")
        return HttpResponseRedirect(reverse("dormitory:index"))

    return render(request, "thread/my_thread.html", {
        "my_threads": Thread.objects.filter(author=request.user),
        "my_replies" : Sub_thread.objects.filter(author=request.user)
    })

def create_thread(request):
    if not request.user.is_authenticated:
        messages.warning(request, "Login First to proceed")
        return render(request, "dormitory/index.html")

    if request.method == "POST":
        header = request.POST["header"]
        
        content = MarkdownForm(request.POST)
        
        if Thread.objects.filter(header=header).first():
            return render(request, 'thread/create_thread.html', {
                "fail_header": "This header is already taken",
                "form": content
            })
        if content.is_valid():
            content = content.cleaned_data['Content']
            new_thread = Thread(header=header,content=content,author=request.user,date=datetime.datetime.now(datetime.timezone.utc))
            new_thread.save()

            return HttpResponseRedirect(reverse("thread:my_thread"))
    else:
        content = MarkdownForm()
    return render(request, 'thread/create_thread.html', {'form': content})

def reply_thread(request,thread_id):
    if not request.user.is_authenticated:
        messages.warning(request, "Login First to proceed")
        return render(request, "dormitory/index.html")
    if request.method == "POST":
        
        content = request.POST["content"]

        this_thread = Thread.objects.get(id=thread_id)
        new_subthread = Sub_thread(replyto = this_thread,content=content,author=request.user,date=datetime.datetime.now(datetime.timezone.utc))
        new_subthread.save()
        this_thread.reply.add(new_subthread)

        return HttpResponseRedirect(reverse("thread:thread",args = (thread_id,)))

    return HttpResponseRedirect(reverse("thread:thread",args = (thread_id,)))
    
def report_thread(request,thread_id) :
    if not request.user.is_authenticated:
        messages.warning(request, "Login First to proceed")
        return HttpResponseRedirect(reverse("dormitory:index"))

    this_thread = get_object_or_404(Thread, id=thread_id)
    this_thread.report += 1
    this_thread.save()
    return HttpResponseRedirect(reverse("thread:thread",args = (thread_id,)))


def report_subthread (request,thread_id,subthread_id):
    if not request.user.is_authenticated:
        messages.warning(request, "Login First to proceed")
        return HttpResponseRedirect(reverse("dormitory:index"))

    this_subthread = get_object_or_404(Sub_thread, id=subthread_id)
    this_subthread.report += 1
    this_subthread.save()
    return HttpResponseRedirect(reverse("thread:thread",args = (thread_id,)))
