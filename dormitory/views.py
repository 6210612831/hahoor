from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import *
from .forms import MarkdownForm
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse

import folium
import datetime

# Create your views here.


def index(request):
    map_location = folium.Map(width=1000, height=600, location=[
                              14.0656662, 100.605382], zoom_start=90)
    folium.Marker(location=[14.0656662, 100.605382], tooltip='Click for more',
                  popup='หอพักรอบเชียงรากน้อย', icon=folium.Icon(color='orange')).add_to(map_location)
    map_location = map_location._repr_html_()

    return render(request, "dormitory/index.html", {
        "dormitories": Dormitory.objects.filter(status=True).order_by('-seen')[:5],
        "map": map_location
    })


# use when render dormitory.html page
def dormitories(request):
    dorm_list = []
    # use when user search Dormitory
    if request.method == "POST":
        search = request.POST["search"]
        dorm_list = []
        for x in Dormitory.objects.all():
            if x.search(search) and x.status == True:
                dorm_list.append(x)
    # use when user didnt search Dormitory so it will return all dormitory
    else:
        for n in Dormitory.objects.all():
            if n.status == True :
                dorm_list.append(n)
    return render(request, "dormitory/dormitories.html", {"dorm_list": dorm_list})


def dormitory(request, dorm_title):
    this_dorm = get_object_or_404(Dormitory, title=dorm_title)

    return render(request, "dormitory/dormitory.html", {
        "dormitory": this_dorm,
    })


def create_dormitory(request):
    if not request.user.is_authenticated:
        return render(request, "dormitory/index.html", {"fail_login": "Login First to proceed"})

    if request.method == "POST":
        title = request.POST["title"]
        desc = request.POST["desc"]
        content = MarkdownForm(request.POST)
        icon = request.FILES['icon_d']
        if Dormitory.objects.filter(title=title).first():
            return render(request,'dormitory/create_dormitory.html', {
                "fail_title": "This title is already taken",
                "form" : content
                })
        if content.is_valid():
            new_dorm = Dormitory(title=title, desc=desc, content=content,
                                 author=request.user, seen=0, date=datetime.datetime.now(), icon=icon)
            new_dorm.save()

            return HttpResponseRedirect(reverse("dormitory:dormitory", kwargs={'dorm_title': title}))
    else:
        content = MarkdownForm()
    return render(request, 'dormitory/create_dormitory.html', {'form': content})
