from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import *
from .forms import DormitoryForm, MarkdownForm
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib import messages

import folium
import datetime

# Create your views here.


def index(request):
    map_location = folium.Map(width=1000, height=600, location=[
                              14.0656662, 100.605382], zoom_start=90)
    folium.Marker(location=[14.0656662, 100.605382], tooltip='Click for more',
                  popup='หอพักรอบเชียงรากน้อย', icon=folium.Icon(color='purple')).add_to(map_location)
    map_location = map_location._repr_html_()

    return render(request, "dormitory/index.html", {
        "dormitories": Dormitory.objects.filter(status=True).order_by('-seen')[:6],
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
            if n.status == True:
                dorm_list.append(n)
    return render(request, "dormitory/dormitories.html", {"dorm_list": dorm_list})


def dormitory(request, dorm_title):
    this_dorm = get_object_or_404(Dormitory, title=dorm_title)
    this_dorm.seen += 1
    this_dorm.save()
    check_my_dormitory = 0
    if request.user.username == this_dorm.author.username:
        check_my_dormitory += 1
    return render(request, "dormitory/dormitory.html", {
        "dormitory": this_dorm,
        "check_my_dormitory": check_my_dormitory,
    })


def create_dormitory(request):
    if not request.user.is_authenticated:
        messages.warning(request, "Login First to proceed")
        return HttpResponseRedirect(reverse("dormitory:index"))

    if request.method == "POST":
        title = request.POST["title"]
        desc = request.POST["desc"]
        content = MarkdownForm(request.POST)
        icon = request.FILES['icon_d']
        if Dormitory.objects.filter(title=title).first():
            return render(request, 'dormitory/create_dormitory.html', {
                "fail_title": "This title is already taken",
                "form": content
            })
        if content.is_valid():
            content = content.cleaned_data['Content']
            new_dorm = Dormitory.objects.create(title=title, desc=desc, content=content,
                                                author=request.user, seen=0, date=datetime.datetime.now(datetime.timezone.utc), icon=icon)
            new_dorm.save()

            return HttpResponseRedirect(reverse("dormitory:my_dormitory"))
    else:
        content = MarkdownForm()
    return render(request, 'dormitory/create_dormitory.html', {'form': content})


def my_dormitory(request):
    if not request.user.is_authenticated:
        messages.warning(request, "Login First to proceed")
        return HttpResponseRedirect(reverse("dormitory:index"))

    return render(request, "dormitory/my_dormitory.html", {
        "my_dormitories": Dormitory.objects.filter(author=request.user)
    })


def my_review(request):
    if not request.user.is_authenticated:
        messages.warning(request, "Login First to proceed")
        return HttpResponseRedirect(reverse("dormitory:index"))

    return render(request, "dormitory/my_review.html", {
        "my_review": Review.objects.filter(author=request.user)
    })


def remove_dormitory(request, dormitory_id):

    if not request.user.is_authenticated:
        messages.warning(request, "Login First to proceed")
        return HttpResponseRedirect(reverse("dormitory:index"))

    if not request.user.is_superuser:
        messages.warning(request, "Permission needed")
        return HttpResponseRedirect(reverse("dormitory:index"))
    Dormitory.objects.get(id=dormitory_id).icon.delete(save=True)
    Dormitory.objects.get(id=dormitory_id).delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


def change_status_dormitory(request, dormitory_id):

    if not request.user.is_authenticated:
        messages.warning(request, "Login First to proceed")
        return HttpResponseRedirect(reverse("dormitory:index"))

    if not request.user.is_superuser:
        messages.warning(request, "Permission needed")
        return HttpResponseRedirect(reverse("dormitory:index"))

    this_dorm = get_object_or_404(Dormitory, id=dormitory_id)

    this_dorm.status = not(this_dorm.status)

    this_dorm.save()
    return HttpResponseRedirect(reverse("user:admin"))


def review_dormitory(request, dormitory_id):
    if not request.user.is_authenticated:
        messages.warning(request, "Login First to proceed")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

    this_dorm = Dormitory.objects.get(id=dormitory_id)

    if request.method == "POST":
        stars = 1
        if request.POST.get("stars"):
            stars = request.POST["stars"]
        content = request.POST["content"]

        new_review = Review.objects.create(reviewto=this_dorm, stars=stars, content=content, author=request.user,
                                           date=datetime.datetime.now(datetime.timezone.utc))
        new_review.save()
        this_dorm.reviews.add(new_review)

        return HttpResponseRedirect(reverse("dormitory:dormitory", args=(this_dorm.title,)))

    return HttpResponseRedirect(reverse("dormitory:dormitory", args=(this_dorm.title,)))


def report_review(request, review_id):
    if not request.user.is_authenticated:
        messages.warning(request, "Login First to proceed")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

    this_review = get_object_or_404(Review, id=review_id)
    this_review.report += 1
    this_review.save()

    return HttpResponse('<script language="javascript">self.close();</script>')


def update_dormitory(request, dormitory_id):
    this_dormitory = get_object_or_404(Dormitory, id=dormitory_id)
    check_update = 1
    # Check user is own this dormitory
    if request.user.username != this_dormitory.author.username:
        return HttpResponseRedirect(reverse("dormitory:dormitory", args=(this_dormitory.title,)))

    # If user submit update form
    if request.method == "POST":
        form = DormitoryForm(request.POST)

        if form.is_valid():
            title = form.cleaned_data['title']
            desc = form.cleaned_data['desc']
            content = form.cleaned_data['content']
            # Update  This Thread
            this_dormitory.title = title
            this_dormitory.desc = desc
            this_dormitory.content = content
            this_dormitory.save()

            return HttpResponseRedirect(reverse("dormitory:dormitory", args=(this_dormitory.title,)))
    else:
        content = DormitoryForm(request.POST or None, instance=this_dormitory)

    return render(request, "dormitory/dormitory.html", {
        "dormitory": this_dormitory,
        "check_update_dorm": check_update,
        "form": content,

    })


def update_review(request, review_id):
    check_update = 1
    if not request.user.is_authenticated:
        messages.warning(request, "Login First to proceed")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

    this_review = Review.objects.get(id=review_id)

    if request.user.username != this_review.author.username:
        return HttpResponseRedirect(reverse("dormitory:dormitory", args=(this_review.reviewto.title,)))

    if request.method == "POST":
        stars = this_review.stars
        if request.POST.get("stars"):
            stars = request.POST["stars"]
        content = request.POST["content"]

        this_review.stars = stars
        this_review.content = content
        this_review.save()
        return HttpResponseRedirect(reverse("dormitory:dormitory", args=(this_review.reviewto.title,)))

    return render(request, "dormitory/dormitory.html", {
        "dormitory": this_review.reviewto,
        "check_update_review": check_update,
        "review_id": review_id,
    })


def delete_review(request, reviews_id):
    if not request.user.is_authenticated:
        messages.warning(request, "Login First to proceed")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

    this_review = Review.objects.get(id=reviews_id)

    if request.user.username != this_review.author.username:
        return HttpResponseRedirect(reverse("dormitory:dormitory", args=(this_review.reviewto.title,)))

    this_review.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


def delete_dormitory(request, dormitory_id):
    if not request.user.is_authenticated:
        messages.warning(request, "Login First to proceed")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

    this_dorm = Dormitory.objects.get(id=dormitory_id)

    if request.user.username != this_dorm.author.username:
        return HttpResponseRedirect(reverse("dormitory:dormitory", args=(this_dorm.title,)))
    this_dorm.icon.delete(save=True)
    this_dorm.delete()
    return HttpResponseRedirect(reverse("dormitory:index"))


def reset_report_review(request, review_id):
    if not request.user.is_authenticated:
        messages.warning(request, "Login First to proceed")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

    this_review = get_object_or_404(Review, id=review_id)
    this_review.report = 0
    this_review.save()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
