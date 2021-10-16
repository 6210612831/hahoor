from django.shortcuts import render
from django.http import HttpResponse
from .models import *

# Create your views here.
def index(request):
    return render(request, "dormitory/index.html",{
        "dormitories" : Dormitory.objects.order_by('seen')[:5]
    })
