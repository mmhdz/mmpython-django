from django.urls import path
from . import views

app_name = "blog_post_app"

urlpatterns = [
    path("", views.login_view, name="login"),
    path("register/", views.get_registration_view, name="get-registration"),
    path("home_page/", views.get_home_view, name="get-home"),
    path("home_page/add", views.post_home_view, name="post-home"),
    path("home_page/comment/add/<int:post_pk>/", views.post_comment_view, name="post-comment"),
    path("home_page/positive_rating/<int:post_pk>", views.add_positive_rating_view, name="post-positive-rating"),
    path("home_page/negative_rating/<int:post_pk>", views.add_negative_rating_view, name="post-negative-rating")
]
