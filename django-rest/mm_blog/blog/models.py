import django
from django.db import models
from django.contrib.auth.models import AbstractUser
from enum import Enum


class UserRole(Enum):
    ADMIN = 0,
    USER = 1


class User(AbstractUser):
    email = models.EmailField(unique=True, blank=False)
    password = models.CharField(max_length=100)
    created_at = models.DateTimeField("The date user is registered", default=django.utils.timezone.now)
    is_staff = models.BooleanField("is_staff", default=False)

    @property
    def role(self):
        if self.is_staff:
            return UserRole.ADMIN
        else:
            return UserRole.USER

    def __str__(self):
        return f"id: {self.pk}, username: {self.username}, email: {self.email}, password: {self.password}, role: {self.role} registration_date: {self.created_at}"


class Hashtag(models.Model):
    value = models.CharField(max_length=45, unique=True)

    def __str__(self):
        return f"id: {self.pk}, value: {self.value}"


class BlogPost(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.TextField(max_length=240, default=None)
    text = models.TextField(max_length=1024)
    hashtags = models.ManyToManyField(Hashtag)
    created_at = models.DateTimeField(default=django.utils.timezone.now)

    def thumbs_up(self):
        return self.blog_post_voting.filter(status=True).count()
    
    @property
    def is_hot(self):
        if self.thumbs_up() >= 5 and self.comments.all().count() >= 2:
            return True
        else:
            return False

    def __str__(self):
        return f"id: {self.pk}, title: {self.title}, text: {self.text}, user_id: {self.user.pk}, hashtags: {self.hashtags.get_queryset()}"


class Comment(models.Model):
    text = models.TextField(max_length=1024)
    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"pk: {self.pk}, text: {self.text}, post_id: {self.post.pk}, user_id: {self.user.pk}"


class Vote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_post_voting_user')
    blog_post = models.ForeignKey(BlogPost, on_delete=models.CASCADE, related_name='votes')
    status = models.BooleanField()

    def __str__(self):
        return f"vote_status: {self.status},  user: {self.user}, blog post: {self.blog_post}"
