from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import *
from datetime import datetime


def login(request):
    context = {
        "login_user_dto": User()
    }

    if request.POST:
        username = request.POST.get('login_user_dto.username')
        password = request.POST.get('login_user_dto.password')

        found_user = User.objects.filter(username=username)
        if found_user.count() > 0 and found_user.get().password == password:
            return None # Return home page
        else:
            return render(request, "blog_post_app/login.html", context)
    else:
        return render(request, "blog_post_app/login.html", context)


def register(request):
    context = {
        "registration_user": User()
    }
    return render(request,  "blog_post_app/register.html", context)


def register_post(request):
    username = request.POST.get('registration_user.username')
    password = request.POST.get('registration_user.password')

    found_user = User.objects.filter(username=username)
    if found_user.count() > 0:
        context = {"has_user_exists": True}
        return render(request,  "blog_post_app/register.html", context)

    u = User(username=username, password=password, registration_date=datetime.now())
    u.save()

    return HttpResponseRedirect(reverse("blog_post_app:login_page"))
