from django.db import models


class User(models.Model):
    username = models.EmailField(max_length=200)
    password = models.CharField(max_length=100)
    registration_date = models.DateTimeField("the date user is registered")

    def __str__(self):
        return f"username {self.username}, password {self.password}, registration_date {self.registration_date}"


class BlogPost(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(max_length=1024)
    positive_rating = models.IntegerField(default=0)
    negative_rating = models.IntegerField(default=0)


class Link(models.Model):
    link_address = models.URLField(name="link")
    blog_post = models.ForeignKey(BlogPost, on_delete=models.CASCADE)


class Comment(models.Model):
    text = models.TextField(max_length=1024)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE)


class Hashtag(models.Model):
    value = models.CharField(max_length=45)
    blog_posts = models.ManyToManyField(BlogPost)

