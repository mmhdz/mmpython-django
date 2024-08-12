from django.urls import path
from . import views

app_name = "blog_post_app"

urlpatterns = [
    path("", views.login_view, name="login_page"),
    path("register", views.register_get_page, name="registration_page"),
    path("register_post", views.register_post_request, name="registration_post"),
    path("home_page", views.create_blog_post, name="blog_home")

]
