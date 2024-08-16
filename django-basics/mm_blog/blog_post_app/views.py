from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse

from .utils import Utils
from .models import *
from .forms import *


def login_view(request):
    form = UserLoginForm(request, data=request.POST)
    if form.is_valid() and form.user_cache is not None:
        user = form.user_cache
        if user.is_active:
            login(request, user)

            return HttpResponseRedirect(reverse("blog_post_app:get-home"))
    else:
        context = {'form': form }
        return render(request, "blog_post_app/login.html", context)


def registration_view(request):
    form = UserRegisterForm(request.POST)
    if form.is_valid():
        form.save()

    context = {'form': form}

    return render(request,  "blog_post_app/register.html", context)


@login_required
def get_home_view(request):
    blog_posts = BlogPost.objects.all()
    negative_count = BlogPost.objects.filter(blog_post_voting__status=False).count()
    positive_count = BlogPost.objects.filter(blog_post_voting__status=True).count()

    context = {
        "blog_post": BlogPost(),
        "blog_posts": blog_posts,
        "comment_text": str(),
        "hashtag_string": str(),
        "negative_count": negative_count,
        "positive_count": positive_count
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


def blog_post_voting_view(request, post_pk: int, is_positive: str):
    votes = BlogPostVote.objects.filter(blog_post__pk=post_pk, user=request.user)
    is_positive = is_positive.lower() == 'true'

    if not votes.exists():
        BlogPostVote.objects.create(user=request.user, blog_post_id=post_pk, status=is_positive)
    else:
        vote = votes.first()
        if vote.status != is_positive:
            vote.delete()
            BlogPostVote.objects.create(user=request.user, blog_post_id=post_pk, status=is_positive)

    return HttpResponseRedirect(reverse("blog_post_app:get-home"))

