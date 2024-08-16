import django
from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    email = models.EmailField(unique=True, blank=False)
    password = models.CharField(max_length=100)
    registration_date = models.DateTimeField("the date user is registered", default=django.utils.timezone.now)

    def __str__(self):
        return f"id: {self.pk}, username: {self.username}, email: {self.email}, password: {self.password}, registration_date: {self.registration_date}"


class BlogPost(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.TextField(max_length=240, default=None)
    text = models.TextField(max_length=1024)

    def __str__(self):
        return f"id: {self.pk}, title: {self.title}, text: {self.text}"


class Comment(models.Model):
    text = models.TextField(max_length=1024)
    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Hashtag(models.Model):
    value = models.CharField(max_length=45)
    blog_posts = models.ManyToManyField(BlogPost)

    def __str__(self):
        return f"id: {self.pk}, value: {self.value}"


class BlogPostVoting(models.Model):
    positive_rating = models.IntegerField(default=0)
    negative_rating = models.IntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    blog_post = models.OneToOneField(BlogPost, on_delete=models.CASCADE, related_name='blog_post_voting')
