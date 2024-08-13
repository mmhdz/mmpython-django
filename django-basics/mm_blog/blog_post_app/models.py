import django
from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    username = models.EmailField(max_length=200, unique=True)
    password = models.CharField(max_length=100)
    registration_date = models.DateTimeField("the date user is registered", default=django.utils.timezone.now)

    def __str__(self):
        return f"id: {self.pk}, username: {self.username}, password: {self.password}, registration_date: {self.registration_date}"


class BlogPost(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.TextField(max_length=240, default=None)
    text = models.TextField(max_length=1024)
    positive_rating = models.IntegerField(default=0)
    negative_rating = models.IntegerField(default=0)

    def __str__(self):
        return f"id: {self.pk}, title: {self.title}, text: {self.text}, positive_rating: {self.positive_rating}, negative_rating: {self.negative_rating}"


class Comment(models.Model):
    text = models.TextField(max_length=1024)
    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE)


class Hashtag(models.Model):
    value = models.CharField(max_length=45)
    blog_posts = models.ManyToManyField(BlogPost)

    def __str__(self):
        return f"id: {self.pk}, value: {self.value}"


