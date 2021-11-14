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

def my_profile(request) :

    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("dormitory:index"))

    return render(request, "user/my_user.html")

def update_profile(request) :

    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("dormitory:index"))

    check_update = 1
    if request.method == "POST":
        new_first_name = request.POST["new_first_name"]
        new_last_name = request.POST["new_last_name"]
        new_email = request.POST["new_email"]

        this_user = User.objects.get(username = request.user.username)
        this_user.first_name = new_first_name
        this_user.last_name = new_last_name
        this_user.email = new_email
        this_user.save()

        messages.info(request, "อัพเดตโปรไฟล์แล้ว")
        return HttpResponseRedirect(reverse("user:my_profile"))

    return render(request, "user/my_user.html",
    { "check_update" :check_update })
    

def change_password(request) :
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("dormitory:index"))

    check_change_password = 1
    if request.method == "POST":
        old_password = request.POST["old_password"]
        new_password = request.POST["new_password"]
        new_re_password = request.POST["new_re_password"]
        

        this_user = User.objects.get(username=request.user.username)

        check_user = authenticate(request, username=request.user.username, password=old_password)
        if check_user is not None:
            if old_password == new_password :    
                return render(request, "user/my_user.html", {"check_change_password": check_change_password, "fail_password": "Password can't be same as before"})

            if (len(new_password) < 8):
                return render(request, "user/my_user.html", {"check_change_password": check_change_password, "fail_password": "Password must have at least 8"})
            elif not re.search("[a-z]", new_password):
                return render(request, "user/my_user.html", {"check_change_password": check_change_password, "fail_password": "Password must have at least 1 of a-z"})
            elif not re.search("[A-Z]", new_password):
                return render(request, "user/my_user.html", {"check_change_password": check_change_password, "fail_password": "Password must have at least 1 of A-Z"})
            elif not re.search("[0-9]", new_password):
                return render(request, "user/my_user.html", {"check_change_password": check_change_password, "fail_password": "Password must have at least 1 of 0-9"})
        # Check re-password is same as password
            if new_password != new_re_password:
                return render(request, "user/my_user.html", {"check_change_password": check_change_password, "fail_password": "Invalid password confirm"})

            this_user.set_password(new_password)
            this_user.save()

            user = authenticate(
                request, username=request.user.username, password=new_password)
            auth_login(request, user)

            messages.info(request, "เปลี่ยนรหัสผ่านแล้ว")
            return HttpResponseRedirect(reverse("user:my_profile"))

        else :
            return render(request, "user/my_user.html",
                          {"check_change_password": check_change_password,
                           "wrong_password": "Invalid Credential",
                           })

    return render(request, "user/my_user.html",
                  {"check_change_password": check_change_password,
                  })


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
