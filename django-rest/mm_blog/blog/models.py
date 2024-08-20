import django
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import Group
from enum import Enum



class UserRole(Enum):
    ADMIN = 0,
    USER = 1




class User(AbstractUser):
    email = models.EmailField(unique=True, blank=False)
    password = models.CharField(max_length=100)
    registration_date = models.DateTimeField("the date user is registered", default=django.utils.timezone.now)
    is_admin = models.BooleanField("is_admin", default=False)

    @property
    def role(self):
        if self.groups.first():
            return self.groups.first().name
        elif self.is_admin:
            return UserRole.ADMIN.name
        else:
            return None


    def __str__(self):
        return f"id: {self.pk}, username: {self.username}, email: {self.email}, password: {self.password}, registration_date: {self.registration_date}"


class Hashtag(models.Model):
    value = models.CharField(max_length=45)

    def __str__(self):
        return f"id: {self.pk}, value: {self.value}"


class BlogPost(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.TextField(max_length=240, default=None)
    text = models.TextField(max_length=1024)
    hashtags = models.ManyToManyField(Hashtag)

    

    def __str__(self):
        return f"id: {self.pk}, title: {self.title}, text: {self.text}, user_id: {self.user.pk}, hashtags: {self.hashtags.get_queryset()}"


class Comment(models.Model):
    text = models.TextField(max_length=1024)
    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class BlogPostVote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_post_voting_user')
    blog_post = models.ForeignKey(BlogPost, on_delete=models.CASCADE, related_name='blog_post_voting')
    status = models.BooleanField()

    def __str__(self):
        return f"vote_status: {self.status},  user: {self.user}, blog post: {self.blog_post}"
