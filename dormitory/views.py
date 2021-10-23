from django.shortcuts import render , get_object_or_404
from django.http import HttpResponse
from .models import *

# Create your views here.


def index(request):
    return render(request, "dormitory/index.html", {
        "dormitories": Dormitory.objects.order_by('seen')[:5]
    })


# use when render dormitory.html page
def dormitories(request):
    dorm_list = []
    # use when user search Dormitory
    if request.method == "POST":
        search = request.POST["search"]
        dorm_list = []
        for x in Dormitory.objects.all():
            if x.search(search):
                dorm_list.append(x)
    # use when user didnt search Dormitory so it will return all dormitory
    else:
        for n in Dormitory.objects.all():
            dorm_list.append(n)
    return render(request, "dormitory/dormitories.html", {"dorm_list": dorm_list})

def dormitory(request,dorm_title) :
    this_dorm = get_object_or_404(Dormitory,title = dorm_title)

    return render(request, "dormitory/dormitory.html", {
        "dormitory": this_dorm,
    })