from django.urls import path
from . import views

app_name = "blog_post_app"

urlpatterns = [
    path("", views.login_view, name="login"),
    path("register/", views.registration_view, name="register"),
    path("home_page/", views.get_home_view, name="get-home"),
    path("home_page/add", views.post_home_view, name="post-home"),
    path("home_page/comment/add/<int:post_pk>/", views.post_comment_view, name="add-comment"),
    path("home_page/positive_rating/<int:post_pk>/<str:is_positive>", views.blog_post_voting_view,
         name="add-rating"),
]
