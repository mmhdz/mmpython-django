from django.urls import path, include

from .views import *
from rest_framework import routers

app_name = "blog"


comment_list_create = CommentView.as_view({
    'get': 'list',
    'post': 'create',
})

comment_update_delete = CommentView.as_view({
    'put': 'update',
    'delete': 'destroy',
})

route = routers.SimpleRouter()
route.register(r'post', PostView)


urlpatterns = [
    path('post/<int:pk>/comments/', comment_list_create),
    path('comment/<int:pk>', comment_update_delete),
    path('hashtag/<int:pk>', DeleteHashtagsView.as_view()),
    path('post/<int:pk>/votes', VoteOnPost.as_view()),
    path('post/<int:pk>/votes/<str:is_positive>', VoteOnPost.as_view()),
    path('', include(route.urls)),
]