import re
from thread.models import *
from dormitory.models import *
from django.shortcuts import render
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib import messages
import sys
sys.path.append('../')
# Create your views here.


def index(request):
    return HttpResponse("THIS IS USER INDEX PAGE")


def about(request):
    return render(request, "user/about.html")


def login(request):
    return render(request, "dormitory/index.html")


def login_check(request):
    # Check user is already login
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse("dormitory:index"))
    # Check this view use when submit login or not if not return to index
    if request.method == "POST":
        # login process
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
        else:
            messages.warning(request, "Invalid credential")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

    return render(request, "dormitory/index.html")


def register(request):
    # Check this view use when call register page or use when submit register form
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        re_password = request.POST["re_password"]
        email = request.POST["email"]
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        # Check username is already taken
        if User.objects.filter(username=username).first():
            return render(request, "user/register.html", {"fail_username": "This username is already taken"})
        # Check the validity of a Password
        if (len(password) < 8):
            return render(request, "user/register.html", {"fail_password": "Password must have at least 8"})
        elif not re.search("[a-z]", password):
            return render(request, "user/register.html", {"fail_password": "Password must have at least 1 of a-z"})
        elif not re.search("[A-Z]", password):
            return render(request, "user/register.html", {"fail_password": "Password must have at least 1 of A-Z"})
        elif not re.search("[0-9]", password):
            return render(request, "user/register.html", {"fail_password": "Password must have at least 1 of 0-9"})
        # Check re-password is same as password
        if password != re_password:
            return render(request, "user/register.html", {"fail_re_password": "Invalid password confirm"})
        # Check email is already taken
        if User.objects.filter(email=email).first():
            return render(request, "user/register.html", {"fail_email": "This email is already taken"})
        # Add Object User
        add_user = User(username=username, email=email,
                        first_name=first_name, last_name=last_name)
        add_user.set_password(password)
        add_user.save()
        return render(request, "dormitory/index.html")
    return render(request, "user/register.html")


def logout(request):
    auth_logout(request)
    messages.warning(request, "Logged out")
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


def register_view(request):
    return render(request, "user/register.html")


def admin_view(request):
    if not request.user.is_authenticated:
        messages.warning(request, "Login First to proceed")
        return HttpResponseRedirect(reverse("dormitory:index"))

    if not request.user.is_superuser:
        messages.warning(request, "Permission needed")
        return HttpResponseRedirect(reverse("dormitory:index"))

    return render(request, "dormitory/admin.html", {
        "dormitories": Dormitory.objects.all().order_by('-date'),
        "reported_threads": Thread.objects.filter(report__gt=10).order_by('-date'),
        "reported_sub_threads": Sub_thread.objects.filter(report__gt=10).order_by('-date'),
        "reported_reviews" : Review.objects.filter(report__gt=10).order_by('-date')
    })
