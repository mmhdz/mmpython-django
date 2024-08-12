from django.urls import path
from . import views

app_name = "blog_post_app"

urlpatterns = [
    path("", views.login, name="login_page"),
    path("register", views.register, name="registration_page"),
    path("register_post", views.register_post, name="registration_post")

]
