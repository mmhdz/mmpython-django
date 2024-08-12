from django.contrib.auth import authenticate, login
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import *
from datetime import datetime


def login_view(request):
    context = {
        "login_user_dto": User()
    }

    if request.POST:
        username = request.POST.get('login_user_dto.username')
        password = request.POST.get('login_user_dto.password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)

            context = {
                "comments": list(),
                "blog_post": BlogPost()

            }
            return render(request, "blog_post_app/home.html", context)
        else:
            return render(request, "blog_post_app/login.html", context)
    else:
        return render(request, "blog_post_app/login.html", context)


def register_get_page(request):
    context = {
        "registration_user": User()
    }
    return render(request,  "blog_post_app/register.html", context)


def register_post_request(request):
    username = request.POST.get('registration_user.username')
    password = request.POST.get('registration_user.password')

    found_user = User.objects.filter(username=username)
    if found_user.count() > 0:
        context = {"has_user_exists": True}
        return render(request,  "blog_post_app/register.html", context)

    User.objects.create_user(username=username, password=password, registration_date=datetime.now())

    return HttpResponseRedirect(reverse("blog_post_app:login_page"))


def create_blog_post(request):
    return HttpResponse(request.user.username + " response")
