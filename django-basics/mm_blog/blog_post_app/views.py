from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse

from .utils import Utils
from .models import *
from .forms import *


def login_view(request):

    if request.method == "POST":
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid() and form.user_cache is not None:
            user = form.user_cache
            if user.is_active:
                login(request, user)

                return HttpResponseRedirect(reverse("blog_post_app:get-home"))
    else:
        context = {'form': UserLoginForm(request, data=request.POST)}
        return render(request, "blog_post_app/login.html", context)


def get_registration_view(request):

    form = UserRegisterForm(request.POST)

    if form.is_valid():
        form.save()

    context = {'form': form}

    return render(request,  "blog_post_app/register.html", context)


@login_required
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
