from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse

from .utils import Utils
from .models import *


def get_login_view(request):
    context = {
        "login_user_dto": User()
    }

    return render(request, "blog_post_app/login.html", context)


def post_login_view(request):
    username = request.POST.get('login_user_dto.username')
    password = request.POST.get('login_user_dto.password')
    user = authenticate(username=username, password=password)

    if user is not None:
        login(request, user)
        return get_home_view(request)

    context = {
        "has_authenticated": False
    }

    return render(request, "blog_post_app/login.html", context)


def get_registration_view(request):
    context = {
        "registration_user": User()
    }
    return render(request,  "blog_post_app/register.html", context)


def post_registration_view(request):
    username = request.POST.get('registration_user.username')
    password = request.POST.get('registration_user.password')

    found_user = User.objects.filter(username=username)
    if found_user.count() > 0:
        context = {"has_user_exists": True}
        return render(request,  "blog_post_app/register.html", context)

    User.objects.create_user(username=username, password=password)

    return HttpResponseRedirect(reverse("blog_post_app:get-login"))


def get_home_view(request):
    blog_posts = BlogPost.objects.all()

    context = {
        "blog_post": BlogPost(),
        "blog_posts": blog_posts,
        "comment_text": str(),
        "hashtag_string": str()
    }

    return render(request, "blog_post_app/home.html", context)


def post_home_view(request):
    title = request.POST.get('blog_post.title')
    text = request.POST.get('blog_post.text')
    hashtag_string = request.POST.get("hashtag_string")

    hashtags = Utils.modify_hashtag_raw_string(hashtag_string)
    print(hashtags)
    blog_post = BlogPost.objects.create(title=title, text=text, user=request.user)

    for hashtag in hashtags:
        saved_hashtag = Hashtag.objects.create(value=hashtag)
        blog_post.hashtag_set.add(saved_hashtag)

    blog_post.save()

    return HttpResponseRedirect(reverse("blog_post_app:get-home"))


def post_comment_view(request, post_pk):
    comment_text = request.POST.get('comment_text')
    found_blog_post = get_object_or_404(BlogPost, pk=post_pk)
    new_comment = Comment(text=comment_text, post=found_blog_post, user=request.user)
    new_comment.save()

    return HttpResponseRedirect(reverse("blog_post_app:get-home"))


def add_positive_rating_view(request, post_pk):
    post = BlogPost.objects.get(pk=post_pk)
    post.positive_rating += 1
    post.save()

    return HttpResponseRedirect(reverse("blog_post_app:get-home"))


def add_negative_rating_view(request, post_pk):
    post = BlogPost.objects.get(pk=post_pk)
    post.negative_rating += 1
    post.save()

    return HttpResponseRedirect(reverse("blog_post_app:get-home"))
